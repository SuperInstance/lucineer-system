use crate::GatewayError;
use serde::Deserialize;
use std::collections::HashMap;
use std::path::{Path, PathBuf};

fn default_threshold() -> u32 {
    5
}
fn default_cooldown_secs() -> u64 {
    60
}
fn default_replay_cap() -> usize {
    1024 * 1024 // 1 MiB
}
fn default_spool_dir() -> PathBuf {
    PathBuf::from("/home/eileen/.openclaw/state/cns-spool")
}
fn default_timeout_secs() -> u64 {
    30
}

/// Gateway-wide settings (`[gateway]` table in the TOML).
#[derive(Debug, Clone, Deserialize)]
pub struct GatewaySection {
    /// CNS spool directory; events are appended to `gateway.jsonl` inside it.
    #[serde(default = "default_spool_dir")]
    pub spool_dir: PathBuf,
    #[serde(default = "default_timeout_secs")]
    pub request_timeout_secs: u64,
}

impl Default for GatewaySection {
    fn default() -> Self {
        Self {
            spool_dir: default_spool_dir(),
            request_timeout_secs: default_timeout_secs(),
        }
    }
}

/// One upstream vendor. SECURITY: `keys` holds ENVIRONMENT VARIABLE NAMES,
/// never literal API keys — values are resolved from the environment at
/// startup.
#[derive(Debug, Clone, Deserialize)]
pub struct ProviderConfig {
    pub name: String,
    pub base_url: String,
    #[serde(default)]
    pub keys: Vec<String>,
    #[serde(default = "default_threshold")]
    pub breaker_threshold: u32,
    #[serde(default = "default_cooldown_secs")]
    pub breaker_cooldown_secs: u64,
    /// Extra headers injected on every upstream request (e.g. OpenAI-Organization).
    #[serde(default)]
    pub extra_headers: HashMap<String, String>,
    /// Request bodies up to this size are buffered so they can be replayed
    /// after a key rotation; larger bodies fail fast with 502.
    #[serde(default = "default_replay_cap")]
    pub replay_buffer_cap_bytes: usize,
}

#[derive(Debug, Clone, Deserialize)]
pub struct GatewayConfig {
    #[serde(default)]
    pub gateway: GatewaySection,
    #[serde(rename = "provider", default)]
    pub providers: Vec<ProviderConfig>,
}

impl GatewayConfig {
    pub fn load(path: &Path) -> Result<Self, GatewayError> {
        let content = std::fs::read_to_string(path)?;
        let config: GatewayConfig = toml::from_str(&content)?;
        config.validate()?;
        Ok(config)
    }

    pub fn validate(&self) -> Result<(), GatewayError> {
        if self.providers.is_empty() {
            return Err(GatewayError::NoProviders);
        }
        let mut seen = std::collections::HashSet::new();
        for p in &self.providers {
            if p.name.is_empty() {
                return Err(GatewayError::Invalid("provider with empty name".into()));
            }
            if !seen.insert(p.name.clone()) {
                return Err(GatewayError::Invalid(format!(
                    "duplicate provider name: {}",
                    p.name
                )));
            }
            if !(p.base_url.starts_with("http://") || p.base_url.starts_with("https://")) {
                return Err(GatewayError::Invalid(format!(
                    "provider {}: base_url must start with http:// or https://",
                    p.name
                )));
            }
            // Reject malformed extra header names/values now, not per-request.
            for (k, v) in &p.extra_headers {
                if http::header::HeaderName::try_from(k.as_str()).is_err() {
                    return Err(GatewayError::Invalid(format!(
                        "provider {}: invalid extra header name {:?}",
                        p.name, k
                    )));
                }
                if http::header::HeaderValue::try_from(v.as_str()).is_err() {
                    return Err(GatewayError::Invalid(format!(
                        "provider {}: invalid value for extra header {:?}",
                        p.name, k
                    )));
                }
            }
        }
        Ok(())
    }
}
