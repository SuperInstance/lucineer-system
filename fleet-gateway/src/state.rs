use crate::breaker::{Breaker, BreakerState, Decision};
use crate::config::{GatewayConfig, ProviderConfig};
use crate::spool::SpoolWriter;
use crate::GatewayError;
use std::collections::HashMap;
use std::sync::{Mutex, MutexGuard};
use std::time::{Duration, Instant};

/// One API key, resolved from an environment variable at startup.
/// `value` is key material: it must never be logged, serialized, or emitted.
pub struct KeyEntry {
    pub env_name: String,
    pub value: String,
    pub dead: bool,
}

pub struct ProviderInner {
    pub keys: Vec<KeyEntry>,
    /// Invariant: index of the first live key, or keys.len() when all dead.
    pub current: usize,
    pub breaker: Breaker,
}

/// Details of a key rotation, for logging/spool events. Env var names only.
pub struct Rotation {
    pub from_env: String,
    pub to_env: String,
    pub reason: &'static str,
}

pub struct ProviderHealth {
    pub breaker: BreakerState,
    pub consecutive: u32,
    pub cooldown_remaining: Option<Duration>,
    pub live_keys: usize,
    pub total_keys: usize,
}

pub struct Provider {
    pub config: ProviderConfig,
    inner: Mutex<ProviderInner>,
}

impl Provider {
    pub fn new(config: ProviderConfig) -> Self {
        let mut keys = Vec::new();
        for env_name in &config.keys {
            match std::env::var(env_name) {
                Ok(value) if !value.is_empty() => {
                    keys.push(KeyEntry {
                        env_name: env_name.clone(),
                        value,
                        dead: false,
                    });
                }
                _ => {
                    tracing::warn!(
                        "provider {}: env var {} not set or empty; skipping that key",
                        config.name,
                        env_name
                    );
                }
            }
        }
        let mut breaker = Breaker::new(
            config.breaker_threshold,
            Duration::from_secs(config.breaker_cooldown_secs),
        );
        if keys.is_empty() {
            tracing::warn!(
                "provider {}: zero resolvable keys; starting with circuit breaker OPEN",
                config.name
            );
            breaker.open_initial();
        }
        Self {
            config,
            inner: Mutex::new(ProviderInner {
                keys,
                current: 0,
                breaker,
            }),
        }
    }

    fn lock(&self) -> MutexGuard<'_, ProviderInner> {
        self.inner.lock().unwrap_or_else(|e| e.into_inner())
    }

    pub fn decide(&self) -> Decision {
        self.lock().breaker.before_request()
    }

    pub fn cooldown_remaining(&self) -> Option<Duration> {
        self.lock().breaker.cooldown_remaining()
    }

    /// Current key material, advancing past dead keys. Returns a clone so
    /// the lock is never held across an upstream await.
    pub fn current_key(&self) -> Option<String> {
        let mut inner = self.lock();
        let idx = (inner.current..inner.keys.len()).find(|&i| !inner.keys[i].dead);
        match idx {
            Some(i) => {
                inner.current = i;
                Some(inner.keys[i].value.clone())
            }
            None => None,
        }
    }

    /// 401/403: the current key is dead. Mark it, advance to the next live
    /// key, and return rotation details (env names only) if one exists.
    pub fn mark_dead_and_advance(&self) -> Option<Rotation> {
        let mut inner = self.lock();
        let cur = inner.current;
        if cur >= inner.keys.len() || inner.keys[cur].dead {
            return None;
        }
        inner.keys[cur].dead = true;
        let next = (cur + 1..inner.keys.len()).find(|&i| !inner.keys[i].dead)?;
        let rotation = Rotation {
            from_env: inner.keys[cur].env_name.clone(),
            to_env: inner.keys[next].env_name.clone(),
            reason: "auth_rejected",
        };
        inner.current = next;
        Some(rotation)
    }

    /// 429: rate-limited, not dead. Move to the next live key without
    /// killing this one; it may recover.
    pub fn soft_advance(&self) -> Option<Rotation> {
        let mut inner = self.lock();
        let cur = inner.current;
        if cur >= inner.keys.len() {
            return None;
        }
        let next = (cur + 1..inner.keys.len()).find(|&i| !inner.keys[i].dead)?;
        let rotation = Rotation {
            from_env: inner.keys[cur].env_name.clone(),
            to_env: inner.keys[next].env_name.clone(),
            reason: "rate_limited",
        };
        inner.current = next;
        Some(rotation)
    }

    /// Returns true if the breaker just closed (emit breaker_closed).
    pub fn on_upstream_success(&self) -> bool {
        self.lock().breaker.on_success()
    }

    /// Returns true if the breaker just opened (emit breaker_open).
    pub fn on_upstream_failure(&self) -> bool {
        self.lock().breaker.on_failure()
    }

    pub fn health(&self) -> ProviderHealth {
        let inner = self.lock();
        ProviderHealth {
            breaker: inner.breaker.state(),
            consecutive: inner.breaker.consecutive(),
            cooldown_remaining: inner.breaker.cooldown_remaining(),
            live_keys: inner.keys.iter().filter(|k| !k.dead).count(),
            total_keys: inner.keys.len(),
        }
    }
}

pub struct AppState {
    pub providers: HashMap<String, std::sync::Arc<Provider>>,
    pub client: reqwest::Client,
    pub spool: SpoolWriter,
    pub started: Instant,
}

impl AppState {
    pub fn from_config(config: &GatewayConfig) -> Result<Self, GatewayError> {
        config.validate()?;
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(config.gateway.request_timeout_secs))
            .build()
            .map_err(|e| GatewayError::Invalid(format!("cannot build HTTP client: {}", e)))?;
        let providers = config
            .providers
            .iter()
            .map(|p| (p.name.clone(), std::sync::Arc::new(Provider::new(p.clone()))))
            .collect();
        Ok(Self {
            providers,
            client,
            spool: SpoolWriter::new(&config.gateway.spool_dir),
            started: Instant::now(),
        })
    }
}
