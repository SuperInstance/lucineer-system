use crate::CnsError;
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Per-file byte offsets, persisted to `<state_dir>/offsets.json`.
///
/// Flushes are batched: callers mark offsets dirty with `advance`, and
/// `maybe_flush` writes at most every `flush_every` dirtied lines or every
/// `flush_interval`, whichever comes first. Writes are atomic (tmp + rename).
pub struct Checkpointer {
    path: PathBuf,
    offsets: HashMap<String, u64>,
    dirty: u32,
    last_flush: Instant,
    flush_every: u32,
    flush_interval: Duration,
}

impl Checkpointer {
    pub fn load(state_dir: &Path, flush_every: u32, flush_interval: Duration) -> Result<Self, CnsError> {
        let path = state_dir.join("offsets.json");
        let offsets = match std::fs::read_to_string(&path) {
            Ok(content) => match serde_json::from_str(&content) {
                Ok(map) => map,
                Err(e) => {
                    tracing::warn!(
                        "offsets.json is corrupt ({}), starting from offset 0 for all files",
                        e
                    );
                    HashMap::new()
                }
            },
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => HashMap::new(),
            Err(e) => return Err(e.into()),
        };
        Ok(Self {
            path,
            offsets,
            dirty: 0,
            last_flush: Instant::now(),
            flush_every,
            flush_interval,
        })
    }

    pub fn offset(&self, file: &str) -> u64 {
        self.offsets.get(file).copied().unwrap_or(0)
    }

    pub fn advance(&mut self, file: &str, offset: u64) {
        self.offsets.insert(file.to_string(), offset);
        self.dirty += 1;
    }

    pub fn reset(&mut self, file: &str) {
        self.offsets.insert(file.to_string(), 0);
        self.dirty += 1;
    }

    pub fn offsets(&self) -> &HashMap<String, u64> {
        &self.offsets
    }

    pub fn maybe_flush(&mut self) -> Result<(), CnsError> {
        if self.dirty > 0
            && (self.dirty >= self.flush_every || self.last_flush.elapsed() >= self.flush_interval)
        {
            self.flush()?;
        }
        Ok(())
    }

    pub fn flush(&mut self) -> Result<(), CnsError> {
        let tmp = self.path.with_extension("json.tmp");
        let content = serde_json::to_string_pretty(&self.offsets)?;
        std::fs::write(&tmp, content)?;
        std::fs::rename(&tmp, &self.path)?;
        self.dirty = 0;
        self.last_flush = Instant::now();
        tracing::debug!("offsets checkpointed to {}", self.path.display());
        Ok(())
    }
}
