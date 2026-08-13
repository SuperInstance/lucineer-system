use std::time::{Duration, Instant};

/// Circuit breaker state, exposed for monitoring and tests.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BreakerState {
    Closed,
    Open,
}

/// Opens after `threshold` consecutive *identical* internal failures.
/// While open, retries happen at most once per `cooldown`; the breaker never
/// exits the process — supervision (systemd) owns restarts.
pub struct CircuitBreaker {
    threshold: u32,
    cooldown: Duration,
    consecutive: u32,
    last_error: Option<String>,
    opened_at: Option<Instant>,
}

impl CircuitBreaker {
    pub fn new(threshold: u32, cooldown: Duration) -> Self {
        Self {
            threshold,
            cooldown,
            consecutive: 0,
            last_error: None,
            opened_at: None,
        }
    }

    pub fn record_success(&mut self) {
        self.consecutive = 0;
        self.last_error = None;
        self.opened_at = None;
    }

    /// Record a failure. Returns true only on the transition Closed -> Open.
    pub fn record_failure(&mut self, error: &str) -> bool {
        if self.last_error.as_deref() == Some(error) {
            self.consecutive += 1;
        } else {
            self.consecutive = 1;
            self.last_error = Some(error.to_string());
        }
        if self.consecutive >= self.threshold {
            if self.opened_at.is_none() {
                self.opened_at = Some(Instant::now());
                return true;
            }
            // Already open: refresh the cooldown window.
            self.opened_at = Some(Instant::now());
        }
        false
    }

    pub fn state(&self) -> BreakerState {
        if self.opened_at.is_some() {
            BreakerState::Open
        } else {
            BreakerState::Closed
        }
    }

    pub fn is_open(&self) -> bool {
        self.state() == BreakerState::Open
    }

    pub fn consecutive_failures(&self) -> u32 {
        self.consecutive
    }

    /// Some(remaining) while open and still inside the cooldown window.
    pub fn cooldown_remaining(&self) -> Option<Duration> {
        self.opened_at
            .map(|t| self.cooldown.saturating_sub(t.elapsed()))
            .filter(|d| !d.is_zero())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn opens_on_identical_failures_only() {
        let mut b = CircuitBreaker::new(3, Duration::from_secs(60));
        assert!(!b.record_failure("boom"));
        assert!(!b.record_failure("boom"));
        b.record_success();
        // Interleaved non-identical errors reset the consecutive count.
        assert!(!b.record_failure("a"));
        assert!(!b.record_failure("b"));
        assert!(!b.record_failure("b"));
        assert!(b.record_failure("b")); // 3 consecutive identical -> opens
        assert!(b.is_open());
    }

    #[test]
    fn opens_at_threshold_and_stays_open() {
        let mut b = CircuitBreaker::new(2, Duration::from_secs(60));
        assert_eq!(b.state(), BreakerState::Closed);
        assert!(!b.record_failure("same"));
        assert!(b.record_failure("same"));
        assert_eq!(b.state(), BreakerState::Open);
        assert!(b.cooldown_remaining().is_some());
        b.record_success();
        assert_eq!(b.state(), BreakerState::Closed);
    }
}
