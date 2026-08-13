use crate::breaker::{BreakerState, CircuitBreaker};
use crate::checkpoint::Checkpointer;
use crate::spool;
use crate::CnsError;
use std::fs::File;
use std::path::PathBuf;
use std::time::{Duration, Instant};
use tracing::{error, info, warn};

/// Daemon tuning. `Default` matches the documented production defaults;
/// tests override the timing knobs.
#[derive(Debug, Clone)]
pub struct DaemonConfig {
    pub spool_dir: PathBuf,
    pub state_dir: PathBuf,
    /// Create the spool directory if it is missing.
    pub create: bool,
    pub poll_interval: Duration,
    pub breaker_threshold: u32,
    pub breaker_cooldown: Duration,
    pub backoff_initial: Duration,
    pub backoff_max: Duration,
    pub heartbeat_interval: Duration,
    /// Flush offsets.json at least every N consumed lines...
    pub flush_every_lines: u32,
    /// ...or every this-long, whichever comes first.
    pub flush_interval: Duration,
}

impl Default for DaemonConfig {
    fn default() -> Self {
        Self {
            spool_dir: PathBuf::from("/home/eileen/.openclaw/state/cns-spool"),
            state_dir: PathBuf::from("/home/eileen/.openclaw/state/cns"),
            create: false,
            poll_interval: Duration::from_millis(250),
            breaker_threshold: 5,
            breaker_cooldown: Duration::from_secs(60),
            backoff_initial: Duration::from_millis(100),
            backoff_max: Duration::from_secs(30),
            heartbeat_interval: Duration::from_secs(60),
            flush_every_lines: 32,
            flush_interval: Duration::from_secs(5),
        }
    }
}

/// Cumulative counters, exposed for tests and the heartbeat log.
#[derive(Debug, Default, Clone, Copy)]
pub struct Stats {
    pub files_tailed: u64,
    pub lines_processed: u64,
    pub lines_dead_lettered: u64,
}

/// Outcome of one `tick`: a full scan-and-process pass with breaker
/// bookkeeping applied.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TickOutcome {
    /// Pass succeeded; number of lines consumed (processed + dead-lettered).
    Processed(u64),
    /// Pass failed with an internal error; the breaker has been fed.
    Failed,
}

pub struct Daemon {
    config: DaemonConfig,
    checkpointer: Checkpointer,
    breaker: CircuitBreaker,
    stats: Stats,
    backoff: Duration,
    dead_letter: Option<File>,
}

impl Daemon {
    pub fn new(config: DaemonConfig) -> Result<Self, CnsError> {
        if !config.spool_dir.is_dir() {
            if config.create {
                std::fs::create_dir_all(&config.spool_dir)?;
            } else {
                return Err(CnsError::SpoolDirMissing(config.spool_dir.clone()));
            }
        }
        std::fs::create_dir_all(&config.state_dir)?;
        let checkpointer = Checkpointer::load(
            &config.state_dir,
            config.flush_every_lines,
            config.flush_interval,
        )?;
        let breaker = CircuitBreaker::new(config.breaker_threshold, config.breaker_cooldown);
        Ok(Self {
            backoff: config.backoff_initial,
            config,
            checkpointer,
            breaker,
            stats: Stats::default(),
            dead_letter: None,
        })
    }

    pub fn stats(&self) -> Stats {
        self.stats
    }

    pub fn breaker_state(&self) -> BreakerState {
        self.breaker.state()
    }

    pub fn checkpointer(&self) -> &Checkpointer {
        &self.checkpointer
    }

    pub fn flush_offsets(&mut self) -> Result<(), CnsError> {
        self.checkpointer.flush()
    }

    /// One scan + process pass over all spool files, with breaker bookkeeping.
    /// Pure bookkeeping — no sleeping; the async run loop owns timing.
    pub fn tick(&mut self) -> TickOutcome {
        let result = self
            .process_once()
            .and_then(|n| self.checkpointer.maybe_flush().map(|_| n));
        match result {
            Ok(consumed) => {
                self.breaker.record_success();
                self.backoff = self.config.backoff_initial;
                TickOutcome::Processed(consumed)
            }
            Err(e) => {
                let opened = self.breaker.record_failure(&e.to_string());
                if opened {
                    error!(
                        error = %e,
                        threshold = self.config.breaker_threshold,
                        cooldown_secs = self.config.breaker_cooldown.as_secs(),
                        "CIRCUIT BREAKER OPEN: consecutive internal failures hit threshold; \
                         retrying at cooldown instead of spinning"
                    );
                } else {
                    warn!(
                        error = %e,
                        consecutive = self.breaker.consecutive_failures(),
                        "processing pass failed"
                    );
                }
                TickOutcome::Failed
            }
        }
    }

    /// Scan the spool dir and drain every file. Returns lines consumed.
    pub fn process_once(&mut self) -> Result<u64, CnsError> {
        let files = spool::list_spool_files(&self.config.spool_dir)?;
        self.stats.files_tailed = files.len() as u64;
        let mut consumed = 0;
        for path in files {
            let outcome = self.process_file(&path)?;
            consumed += outcome.processed + outcome.dead_lettered;
        }
        Ok(consumed)
    }

    fn process_file(&mut self, path: &std::path::Path) -> Result<spool::FileOutcome, CnsError> {
        let name = path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_else(|| path.display().to_string());
        let len = std::fs::metadata(path)?.len();
        let mut offset = self.checkpointer.offset(&name);
        if len < offset {
            warn!(
                spool_file = %name,
                old_offset = offset,
                new_len = len,
                "spool file smaller than checkpoint (rotated/truncated); resetting offset to 0"
            );
            self.checkpointer.reset(&name);
            offset = 0;
        }

        let spool_dir = self.config.spool_dir.clone();
        let stats = &mut self.stats;
        let checkpointer = &mut self.checkpointer;
        let dead_letter = &mut self.dead_letter;
        let mut processed = 0u64;
        let mut dead = 0u64;

        let outcome = spool::drain_file(
            path,
            offset,
            |value| {
                processed += 1;
                info!(spool_file = %name, event = %value, "processed event");
            },
            |raw, byte_offset| {
                let handle = open_dead_letter(dead_letter, &spool_dir)?;
                spool::write_dead_letter(handle, &name, byte_offset, raw)?;
                dead += 1;
                warn!(
                    spool_file = %name,
                    byte_offset,
                    "malformed event quarantined to dead-letter"
                );
                Ok(())
            },
            |new_offset| checkpointer.advance(&name, new_offset),
        )?;
        stats.lines_processed += processed;
        stats.lines_dead_lettered += dead;
        Ok(outcome)
    }

    fn log_heartbeat(&self) {
        info!(
            files_tailed = self.stats.files_tailed,
            lines_processed = self.stats.lines_processed,
            lines_dead_lettered = self.stats.lines_dead_lettered,
            backoff_ms = self.backoff.as_millis() as u64,
            breaker = ?self.breaker.state(),
            breaker_consecutive_failures = self.breaker.consecutive_failures(),
            "heartbeat"
        );
    }

    /// Main loop. Every iteration ends in a sleep (poll, backoff, or breaker
    /// cooldown) or the shutdown signal — the loop structurally cannot spin.
    pub async fn run(
        &mut self,
        shutdown: impl std::future::Future<Output = ()>,
    ) -> Result<(), CnsError> {
        tokio::pin!(shutdown);
        let mut last_heartbeat = Instant::now();
        info!(
            spool_dir = %self.config.spool_dir.display(),
            state_dir = %self.config.state_dir.display(),
            poll_interval_ms = self.config.poll_interval.as_millis() as u64,
            breaker_threshold = self.config.breaker_threshold,
            "fleet-cns starting"
        );
        loop {
            if last_heartbeat.elapsed() >= self.config.heartbeat_interval {
                self.log_heartbeat();
                last_heartbeat = Instant::now();
            }

            let sleep_for = match self.tick() {
                TickOutcome::Processed(_) => self.config.poll_interval,
                TickOutcome::Failed => {
                    if let Some(remaining) = self.breaker.cooldown_remaining() {
                        remaining
                    } else {
                        let current = self.backoff;
                        self.backoff = (self.backoff * 2).min(self.config.backoff_max);
                        current
                    }
                }
            };

            tokio::select! {
                _ = tokio::time::sleep(sleep_for) => {}
                _ = &mut shutdown => {
                    info!("shutdown signal received");
                    break;
                }
            }
        }
        self.checkpointer.flush()?;
        info!(
            lines_processed = self.stats.lines_processed,
            lines_dead_lettered = self.stats.lines_dead_lettered,
            "offsets flushed; fleet-cns stopping"
        );
        Ok(())
    }
}

/// Lazily open (and keep open) the dead-letter append handle.
fn open_dead_letter<'a>(
    handle: &'a mut Option<File>,
    spool_dir: &std::path::Path,
) -> Result<&'a mut File, CnsError> {
    if handle.is_none() {
        let file = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(spool_dir.join(spool::DEAD_LETTER_FILE))?;
        *handle = Some(file);
    }
    Ok(handle.as_mut().expect("dead-letter handle just opened"))
}
