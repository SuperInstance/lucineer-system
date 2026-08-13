use thiserror::Error;

#[derive(Error, Debug)]
pub enum CnsError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("spool directory does not exist: {0} (pass --create to create it)")]
    SpoolDirMissing(std::path::PathBuf),
    #[error("state serialization failed: {0}")]
    State(#[from] serde_json::Error),
}
