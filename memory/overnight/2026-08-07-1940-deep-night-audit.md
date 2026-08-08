# Deep Night Audit — 2026-08-07 19:40 AKDT

## Repo Audited: `study-vessel-prototype`
**Repository:** https://github.com/SuperInstance/vessel-prototype.git  
**Commit:** `09e2314` on `main`  
**Language:** Python 3.14.4  

## What It Does
Agent/Vessel separation architecture for the Cocapn Fleet. An `AgentSoul` (behavior, goals, memory) can migrate between `Vessel` instances (hardware/runtime). A `FleetScheduler` handles scheduling souls onto vessels based on capability requirements and preferences.

## Bug Found & Fixed

### 🐛 CRITICAL: Python 3.14 Dataclass Field/Method Name Collision
**File:** `agent.py`, class `Vessel`  
**Impact:** Module completely fails to import on Python 3.14+

The `Vessel` dataclass had a field `host: str` (hostname/IP) and a method `host(self, soul)` (host an agent). In Python 3.14, the dataclass decorator became stricter about detecting class-level values as defaults. It sees the `host` method in the class namespace and treats it as a default value for the `host` field. Then `os` (a field without a default) follows `host` (which now appears to have a default), triggering:

```
TypeError: non-default argument 'os' follows default argument 'host'
```

**Fix:** Renamed `Vessel.host()` → `Vessel.host_agent()`. Updated all call sites in `FleetScheduler.migrate()` and `demo()`.

This was a silent killer — the repo has a GitHub Actions CI workflow but it was presumably running on an older Python or never got triggered after the Python upgrade.

## Tests Written
**64 tests** in `test_agent.py`, all passing in 0.07s.

### Coverage:
| Area | Tests | Key Areas |
|------|-------|-----------|
| `Capability` | 3 | Defaults, custom values, metadata independence |
| `AgentSoul` | 8 | `can_run_on` (present/missing/unavailable/empty), `score_vessel` (negative/zero/positive/unavailable preferred) |
| `Vessel` | 13 | `has_cap`, `get_cap`, `add_cap` (overwrite), `can_host` (full/wrong caps), `host_agent` (success/failure), `release` (existing/nonexistent/one-of-many), `max_agents` defaults |
| `FleetScheduler` | 16 | Registration, `find_best_vessel` (basic/exclude/empty/tiebreaker/higher-score), `migrate` (success/unknown/no-source/excludes-source/nowhere-to-go/full), `get_fleet_status` (empty/with-vessels/after-hosting/caps) |
| Integration | 4 | Full scheduling scenario, degradation (GPU failure → migration), cascading failure (multi-vessel), capacity exhaustion & recovery |
| Edge Cases | 6 | Duplicate registration, phantom agent migration, room-after-release, negative priority caps, duplicate hosting (documented current behavior), bare vessel status |
| Smoke | 2 | `demo()` and `main()` run without errors |

### Notable Edge Case Documented
`test_same_soul_hosted_twice_on_same_vessel` — the current implementation allows hosting the same soul twice on a vessel (no dedup guard). This is documented as current behavior, not fixed. Future work could add a guard.

## Files Changed
- `agent.py` — 3 edits (method rename + 2 call sites)
- `test_agent.py` — new file, 705 insertions

## Outcome
✅ Bug fixed (Python 3.14 import blocked)  
✅ 64 tests passing  
✅ Pushed to `origin/main`
