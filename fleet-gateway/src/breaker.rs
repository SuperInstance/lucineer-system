use std::time::{Duration, Instant};

/// Hard cap on cooldown growth after repeated failed probes.
const MAX_COOLDOWN: Duration = Duration::from_secs(15 * 60);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BreakerState {
    Closed,
    Open,
    HalfOpen,
}

impl BreakerState {
    pub fn as_str(&self) -> &'static str {
        match self {
            BreakerState::Closed => "closed",
            BreakerState::Open => "open",
            BreakerState::HalfOpen => "half-open",
        }
    }
}

/// Gate decision for an incoming request.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    /// Normal traffic, or the single half-open probe after cooldown.
    Allow,
    /// Breaker open (or a probe already in flight): answer 503 immediately.
    Reject,
}

/// Per-provider circuit breaker, mirroring fleet-cns semantics:
/// threshold consecutive failures -> open -> cooldown -> one half-open
/// probe. A failed probe re-opens with doubled cooldown (capped); success
/// closes and resets everything.
pub struct Breaker {
    threshold: u32,
    base_cooldown: Duration,
    current_cooldown: Duration,
    state: BreakerState,
    consecutive: u32,
    open_until: Option<Instant>,
}

impl Breaker {
    pub fn new(threshold: u32, cooldown: Duration) -> Self {
        Self {
            threshold,
            base_cooldown: cooldown,
            current_cooldown: cooldown,
            state: BreakerState::Closed,
            consecutive: 0,
            open_until: None,
        }
    }

    /// Start open (provider with zero resolvable keys).
    pub fn open_initial(&mut self) {
        self.state = BreakerState::Open;
        self.open_until = Some(Instant::now() + self.current_cooldown);
    }

    pub fn before_request(&mut self) -> Decision {
        match self.state {
            BreakerState::Closed => Decision::Allow,
            BreakerState::Open => match self.open_until {
                Some(until) if Instant::now() >= until => {
                    self.state = BreakerState::HalfOpen;
                    Decision::Allow // this request is the probe
                }
                _ => Decision::Reject,
            },
            // One probe at a time; the rest get 503.
            BreakerState::HalfOpen => Decision::Reject,
        }
    }

    /// Upstream interaction succeeded (any non-5xx response). Returns true
    /// on the transition back to Closed (emit a breaker_closed event).
    pub fn on_success(&mut self) -> bool {
        let was_broken = matches!(self.state, BreakerState::Open | BreakerState::HalfOpen);
        self.state = BreakerState::Closed;
        self.consecutive = 0;
        self.current_cooldown = self.base_cooldown;
        self.open_until = None;
        was_broken
    }

    /// Upstream 5xx / timeout / auth exhaustion. Returns true on the
    /// transition to Open (emit a breaker_open event).
    pub fn on_failure(&mut self) -> bool {
        self.consecutive += 1;
        match self.state {
            BreakerState::HalfOpen => {
                self.current_cooldown = (self.current_cooldown * 2).min(MAX_COOLDOWN);
                self.open();
                true
            }
            BreakerState::Open => false, // already open; rejected requests don't reach here
            BreakerState::Closed => {
                if self.consecutive >= self.threshold {
                    self.open();
                    true
                } else {
                    false
                }
            }
        }
    }

    fn open(&mut self) {
        self.state = BreakerState::Open;
        self.open_until = Some(Instant::now() + self.current_cooldown);
    }

    pub fn state(&self) -> BreakerState {
        self.state
    }

    pub fn consecutive(&self) -> u32 {
        self.consecutive
    }

    pub fn current_cooldown(&self) -> Duration {
        self.current_cooldown
    }

    /// Time until a half-open probe is allowed; None when not open.
    pub fn cooldown_remaining(&self) -> Option<Duration> {
        if self.state != BreakerState::Open {
            return None;
        }
        self.open_until
            .map(|u| u.saturating_duration_since(Instant::now()))
            .filter(|d| !d.is_zero())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn opens_at_threshold_then_probe_then_close() {
        let mut b = Breaker::new(2, Duration::from_millis(10));
        assert_eq!(b.before_request(), Decision::Allow);
        assert!(!b.on_failure());
        assert_eq!(b.state(), BreakerState::Closed);
        assert!(b.on_failure()); // threshold hit
        assert_eq!(b.state(), BreakerState::Open);
        assert_eq!(b.before_request(), Decision::Reject); // inside cooldown
        std::thread::sleep(Duration::from_millis(15));
        assert_eq!(b.before_request(), Decision::Allow); // half-open probe
        assert_eq!(b.state(), BreakerState::HalfOpen);
        assert_eq!(b.before_request(), Decision::Reject); // one probe at a time
        assert!(b.on_success());
        assert_eq!(b.state(), BreakerState::Closed);
        assert_eq!(b.consecutive(), 0);
    }

    #[test]
    fn failed_probe_doubles_cooldown_and_success_resets() {
        let mut b = Breaker::new(1, Duration::from_millis(10));
        assert!(b.on_failure());
        assert_eq!(b.current_cooldown(), Duration::from_millis(10));
        std::thread::sleep(Duration::from_millis(15));
        assert_eq!(b.before_request(), Decision::Allow); // probe
        assert!(b.on_failure()); // probe failed
        assert_eq!(b.current_cooldown(), Duration::from_millis(20));
        std::thread::sleep(Duration::from_millis(25));
        assert_eq!(b.before_request(), Decision::Allow);
        b.on_success();
        assert_eq!(b.current_cooldown(), Duration::from_millis(10));
    }

    #[test]
    fn cooldown_caps_at_fifteen_minutes() {
        let mut b = Breaker::new(1, Duration::from_secs(10 * 60));
        assert!(b.on_failure());
        b.state = BreakerState::HalfOpen; // simulate elapsed cooldown + probe
        assert!(b.on_failure());
        assert_eq!(b.current_cooldown(), MAX_COOLDOWN);
    }
}
