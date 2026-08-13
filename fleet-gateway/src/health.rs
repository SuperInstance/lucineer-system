use crate::state::AppState;
use axum::extract::State;
use axum::Json;
use std::sync::Arc;

/// Health snapshot. Reports breaker state, failure counts, cooldown, and
/// key COUNTS — never key material.
pub async fn healthz(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let mut providers = serde_json::Map::new();
    for (name, provider) in &state.providers {
        let h = provider.health();
        providers.insert(
            name.clone(),
            serde_json::json!({
                "breaker": h.breaker.as_str(),
                "consecutive_failures": h.consecutive,
                "cooldown_remaining_secs": h.cooldown_remaining.map(|d| d.as_secs()).unwrap_or(0),
                "live_keys": h.live_keys,
                "total_keys": h.total_keys,
            }),
        );
    }
    Json(serde_json::json!({
        "status": "ok",
        "uptime_secs": state.started.elapsed().as_secs(),
        "providers": providers,
    }))
}
