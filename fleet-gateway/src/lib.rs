//! fleet-gateway: localhost API gateway sidecar.
//!
//! Sits between fleet processes and external API vendors. Owns two failure
//! modes: dead API keys with no fallback (per-provider ordered key chain,
//! resolved from environment variables — never literal secrets in config)
//! and missing circuit breakers (per-provider breaker with half-open probes
//! and exponentially growing cooldown).

pub mod breaker;
pub mod config;
pub mod error;
pub mod health;
pub mod proxy;
pub mod spool;
pub mod state;

pub use config::GatewayConfig;
pub use error::GatewayError;
pub use state::AppState;

use axum::routing::{any, get};
use axum::Router;
use std::net::SocketAddr;
use std::sync::Arc;

pub fn build_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/healthz", get(health::healthz))
        .route("/v1/{provider}/{*path}", any(proxy::proxy_handler))
        .with_state(state)
}

pub async fn serve(
    state: Arc<AppState>,
    bind: SocketAddr,
    shutdown: impl std::future::Future<Output = ()> + Send + 'static,
) -> Result<(), GatewayError> {
    let listener = tokio::net::TcpListener::bind(bind).await?;
    tracing::info!("fleet-gateway listening on http://{}", bind);
    axum::serve(listener, build_router(state))
        .with_graceful_shutdown(shutdown)
        .await?;
    Ok(())
}
