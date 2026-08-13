use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, Ordering};

/// Append-only writer for CNS spool events (`<spool_dir>/gateway.jsonl`).
/// Telemetry must never kill the gateway: a missing/read-only spool dir
/// produces one warning, then silence.
pub struct SpoolWriter {
    path: PathBuf,
    warned: AtomicBool,
}

impl SpoolWriter {
    pub fn new(spool_dir: &Path) -> Self {
        Self {
            path: spool_dir.join("gateway.jsonl"),
            warned: AtomicBool::new(false),
        }
    }

    /// Append one JSONL event. O(1) per event, infallible by design.
    pub fn emit(&self, event: serde_json::Value) {
        let line = match serde_json::to_string(&event) {
            Ok(l) => l,
            Err(e) => {
                tracing::warn!("cannot serialize spool event: {}", e);
                return;
            }
        };
        let result = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.path)
            .and_then(|mut f| {
                use std::io::Write;
                writeln!(f, "{}", line)
            });
        if let Err(e) = result {
            if !self.warned.swap(true, Ordering::Relaxed) {
                tracing::warn!(
                    "cannot write CNS spool event to {}: {} (further spool warnings suppressed)",
                    self.path.display(),
                    e
                );
            }
        }
    }
}
