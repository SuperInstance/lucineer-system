use clap::Parser;
use fleet_cns::{Daemon, DaemonConfig};
use std::path::PathBuf;
use std::process;
use std::time::Duration;
use tracing_subscriber::EnvFilter;

#[derive(Parser)]
#[command(
    name = "fleet-cns",
    about = "Fleet CNS spool monitor: tails JSONL spools with dead-letter, backoff, circuit breaker, and checkpointed offsets"
)]
struct Cli {
    /// Directory of append-only JSONL spool files to tail
    #[arg(long, default_value = "/home/eileen/.openclaw/state/cns-spool")]
    spool_dir: PathBuf,

    /// Directory for daemon state (offsets.json)
    #[arg(long, default_value = "/home/eileen/.openclaw/state/cns")]
    state_dir: PathBuf,

    /// Create the spool directory if it does not exist
    #[arg(long)]
    create: bool,

    /// Poll interval between spool scans, in milliseconds
    #[arg(long, default_value_t = 250)]
    poll_interval_ms: u64,

    /// Consecutive identical internal errors before the circuit breaker opens
    #[arg(long, default_value_t = 5)]
    breaker_threshold: u32,
}

fn init_logging() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("fleet_cns=info"));
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

    let config = DaemonConfig {
        spool_dir: cli.spool_dir,
        state_dir: cli.state_dir,
        create: cli.create,
        poll_interval: Duration::from_millis(cli.poll_interval_ms),
        breaker_threshold: cli.breaker_threshold,
        ..DaemonConfig::default()
    };

    // Unrecoverable configuration faults exit non-zero; everything else is
    // retried forever under backoff/breaker inside the run loop.
    let mut daemon = match Daemon::new(config) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("fleet-cns: fatal configuration fault: {}", e);
            process::exit(2);
        }
    };

    if let Err(e) = daemon.run(shutdown_signal()).await {
        eprintln!("fleet-cns: fatal error during shutdown: {}", e);
        process::exit(1);
    }
}
