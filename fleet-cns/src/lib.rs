//! fleet-cns: supervised JSONL spool monitor daemon.
//!
//! Tails a directory of append-only JSONL spool files and processes events
//! reliably: malformed lines go to a dead-letter file, offsets are
//! checkpointed, consecutive failures feed exponential backoff, and a circuit
//! breaker stops hot loops on persistent internal faults.

pub mod breaker;
pub mod checkpoint;
pub mod daemon;
pub mod spool;

mod error;

pub use breaker::{BreakerState, CircuitBreaker};
pub use checkpoint::Checkpointer;
pub use daemon::{Daemon, DaemonConfig, Stats, TickOutcome};
pub use error::CnsError;
