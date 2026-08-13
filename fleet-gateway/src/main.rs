use clap::Parser;
use fleet_gateway::{AppState, GatewayConfig};
use std::path::PathBuf;
use std::process;
use std::sync::Arc;
use tracing_subscriber::EnvFilter;

#[derive(Parser)]
#[command(
    name = "fleet-gateway",
    about = "Fleet API gateway sidecar: localhost reverse proxy with per-provider key chains and circuit breakers"
)]
struct Cli {
    /// Path to the TOML config file
    #[arg(long, default_value = "/home/eileen/.openclaw/state/gateway.toml")]
    config: PathBuf,

    /// Listen address
    #[arg(long, default_value = "127.0.0.1:8787")]
    bind: String,
}

fn init_logging() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("fleet_gateway=info"));
    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(true)
        .compact()
        .init();
}

async fn shutdown_signal() {
    use tokio::signal::unix::{signal, SignalKind};
    let mut sigterm = match signal(SignalKind::terminate()) {
        Ok(s) => s,
        Err(e) => {
            tracing::warn!("cannot install SIGTERM handler ({}); only SIGINT is handled", e);
            let _ = tokio::signal::ctrl_c().await;
            return;
        }
    };
    tokio::select! {
        _ = tokio::signal::ctrl_c() => {}
        _ = sigterm.recv() => {}
    }
}

#[tokio::main]
async fn main() {
    init_logging();
    let cli = Cli::parse();

    // Startup faults are unrecoverable: exit non-zero and let the
    // supervisor surface it.
    let config = match GatewayConfig::load(&cli.config) {
        Ok(c) => c,
        Err(e) => {
            eprintln!(
                "fleet-gateway: fatal configuration fault in {}: {}",
                cli.config.display(),
                e
            );
            process::exit(2);
        }
    };
    let bind = match cli.bind.parse() {
        Ok(b) => b,
        Err(e) => {
            eprintln!("fleet-gateway: invalid --bind {:?}: {}", cli.bind, e);
            process::exit(2);
        }
    };
    let state = match AppState::from_config(&config) {
        Ok(s) => Arc::new(s),
        Err(e) => {
            eprintln!("fleet-gateway: fatal startup fault: {}", e);
            process::exit(2);
        }
    };

    let provider_names: Vec<&str> = state.providers.keys().map(|k| k.as_str()).collect();
    tracing::info!(
        providers = ?provider_names,
        bind = %bind,
        "fleet-gateway starting"
    );
    state.spool.emit(serde_json::json!({
        "ts": chrono::Utc::now().to_rfc3339(),
        "kind": "startup",
        "bind": bind.to_string(),
        "providers": provider_names,
    }));

    if let Err(e) = fleet_gateway::serve(state, bind, shutdown_signal()).await {
        eprintln!("fleet-gateway: serve failed: {}", e);
        process::exit(1);
    }
    tracing::info!("fleet-gateway stopped");
}
