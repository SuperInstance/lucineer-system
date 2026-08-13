use thiserror::Error;

#[derive(Error, Debug)]
pub enum GatewayError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("config parse failed: {0}")]
    Config(#[from] toml::de::Error),
    #[error("no providers defined in config")]
    NoProviders,
    #[error("invalid config: {0}")]
    Invalid(String),
}
