# IMPLEMENTATION REPORT

*2026-08-19 · VMF Engineering Implementer (subagent) · build pass — Gate 1.*

**Built.**
- `elephant/vmf.py` — the full joint (μ̂, κ) vMF MLE per §1: `zvec` (standardization `z = s·(v−c)`), `windowed` (trailing-window samples, quiescent skip), `A7` (numpy-only closed-form half-integer Bessel ratio with small-κ series branch), `vmf_fit` (Newton solve on A₇(κ)=ρ, Banerjee init/CI shortcut, bootstrap CI, jackknife SE(μ̂)), `edge` (drift + deadband). Warmth = Ŵ·μ̂ projection, decoupled from κ by construction.
- `elephant/tapnight.py` — the §3 JSONL edge log, additive at the three hook points (`start_session` → `session_open`, `speak` → per-message `speak` event incl. the now-persisted raw 7-vector / first_by_author / presence_mask / inline fit / edge, `end_session` → `session_close`). No-op unless `log_path` is set; existing behavior untouched.
- `tests/test_vmf.py` — §4: κ recovery on exact vMF samples, scipy spot-check <1e-9, guards (N<10, ρ→1 sinh-overflow clamp, κ≤500), window sensitivity W∈{4,8,16}, edge-log sink + replay honesty.

**Test command + result.**
```
cd /home/eileen/projects/elephant && python3 -m pytest -q
267 passed  (baseline was 251; +16 new, zero regressions)
```
Note: `tests/test_roomd.py::test_ring_rearms_on_fall` is a **pre-existing** intermittent flake in *unmodified* `roomd.py` (two panic rings collide on the same millisecond-timestamped filename; fails ~1-in-15 runs in isolation too, and `roomd.py` does not import `tapnight`/`vmf`). Not a regression; left untouched as out of scope.

**Deviations from spec (all minor, justified).**
1. `vmf.py` hardcodes `LO/HI/CENTER` (mirroring `tapnight.DIAL_BOUNDS`/`DIAL_CENTER`) instead of importing them, to avoid a circular import (`tapnight` now imports `vmf`). A lockstep test (`test_standardization_matches_tapnight_bounds`) guards drift.
2. `vmf_fit` adds a `saturated` bool field (ρ≥0.999 or κ≥500) — the §1.7 guard table asks for exactly this flag; it is absent from the §1.6 sketch's return dict.
3. Added `ρ < 1e-12 → None` guard (isotropic sample) — the sketch's `μ = r/ρ` divides by zero when r̄=0, which would emit NaN into JSON. No fake number.
4. Bootstrap CI resamples are clipped to `[1e-6, KMAX]` (the sketch clipped only the point estimate); keeps the κ CI semantically within the κ≤500 saturation cap.
5. `warmth_vmf` uses the spec's *fixed* linear form `[.30,.10,.10,−.15,.15,−.10,.10]` verbatim. (Strict z-linearization of `field.warmth()` would halve the cynicism/panic weights; the spec's fixed form is authoritative, so I followed it — noted for the record.)
6. The log's `edge` records carry `real: null` (per §3.2/§3.3) while the deadband flag is available via `vmf.edge()` for post-hoc derivation — as specified, not a deviation.

**Gate-1 acceptance conditions.**
1. *pytest fully green* — ✅ **PASS** (267 passed; only pre-existing roomd flake noted above).
2. *κ recovery reproduces* — ✅ **PASS** (κ=3/5/15 recovered within <15% rel. error at N=800, μ̂·μ > 0.99; A₇ matches scipy to <1e-9).
3. *JSONL edge log produced* — ✅ **PASS** (`data/roomd-field-log.jsonl` is the roomd contrast corpus `{ts, map_temperature, rooms}` — it does **not** parse as a tapnight edge log — so the smoke fixture was generated from `tapnight`, producing a 14-line `session_open/speak×12/session_close` edge log with `real: null`).

---

# vMF Engineering Spec — (μ̂, κ) from the DialBank on v0, and the Minimal Instrumented Tap Session

*2026-08-19 · VMF Engineering Scout (subagent) · deliverable, not an essay.*
*Inputs read: `elephant/field.py`, `room.py`, `dial.py`, `dials/*`, `presets.py`, `tapnight.py`, `docs/jepa-zeitgeist-2026-08-17.md`, `docs/jepa-rag.md`; `fleet-jepa-midi/research/elephant-sense-v3-design-2026-08-17.md` (§2.2, §8); `research/devils-advocate-conversation-temperature.md` §4 (the 7-condition gate). No repo files modified.*

---

## 0. What v0 actually is (ground truth from the repo)

- **Field space is 7-dim.** `field.DIAL_NAMES` = mood, volume, earnestness, cynicism, joke_landing, panic, presence. `DEFAULT_DIALS` ships **9** dials (adds `model_vs_code`, `vision`); `bank.readings()` returns 9 keys but `RoomField.vector()` slices the 7. The vMF snapshot lives in the same 7-space.
- **Ranges/centers** (`tapnight.DIAL_BOUNDS` / `DIAL_CENTER`): mood, joke_landing ∈ [−1,1] c=0; volume, cynicism, panic ∈ [0,1] c=0; earnestness, presence ∈ [0,1] c=0.5.
- **v0 κ is a norm proxy, and it is center-mismatched.** `RoomField.concentration() = 2·‖v − 0.5·𝟙‖` subtracts 0.5 from *every* dial including the four whose neutral is 0 — it measures extremity-with-offset, is monotone in field magnitude, and therefore collinearly tracks |warmth|. This is exactly the confound gate-condition 3 exists to kill. It stays for back-compat logging; it is **banned from comparison paths**.
- **v0 warmth is a fixed linear form** on raw readings (`field.RoomField.warmth()`): `0.30·mood + 0.15·joke + 0.20·(earn−.5) + 0.20·(pres−.5) + 0.20·(vol−.5) − 0.15·cyn − 0.10·panic`.
- **`TapNightSession.speak()` already computes the raw field every message** (`raw = read_field(...).vector()`) and then discards it (only the charisma-displaced effective field is kept). Order-of-arrival already exists *in memory*: `Room` sorts by `ts` (stable sort), and the auto-clock (`STEP=60`) makes ts strictly increasing when callers omit timestamps. What's missing is *persistence* and *structure*, not mechanics.
- **Probe baseline (v3 §8):** fine room-gap **0.015**, coarse (speech vs music) **0.271**, room discrimination 0.339 / speaker-heldout 0.356, within-room spread 0.328–0.418, encoder cosine noise floor ~**0.05**.

---

## 1. MATH — joint (μ̂, κ) from DialBank readings

### 1.1 Standardize the dial space

Map raw readings to a comparable centered cube before any sphere work:

```
z_k = s_k · (v_k − c_k),   s_k = 2/(hi_k − lo_k)   →  z_k ∈ [−1, 1]
```

with (lo, hi, c) from `DIAL_BOUNDS`/`DIAL_CENTER` per §0. Rationale: vMF lives on a sphere; raw dial units are incommensurable (signed vs [0,1], different centers). Skipping this silently weights volume/earnestness/presence at half-range and double-counts the centered-at-0.5 offset — a calibration choice must be *stated*, and this is ours. It ships in the log (`params.standardization`).

### 1.2 The sample: windowed sub-room readings

A single room snapshot is **one** 7-vector — κ is not identifiable from N=1. Construct the sample by reading the bank over trailing windows (the room *as it was* at each arrival):

```
for i in 0..n−1:   R_i = Room(messages[max(0, i−W+1) .. i])   →  z_i = z(bank.readings(R_i))
```

- **W = 8 messages** (matches `Dial.series`'s default window and Tap speaking rhythm); log W, and sensitivity-check κ over W ∈ {4, 8, 16} — density/presence-style dials are window-dependent by construction, so κ(W) drift is expected and must be reported, not hidden.
- Skip windows with ‖z‖ < 1e-3 (quiescent — nothing to normalize).
- Overlapping windows (step 1) autocorrelate the sample → bootstrap CIs come out narrow. Conservative mode for CIs: non-overlapping (step = W); step 1 for the trajectory.

### 1.3 vMF MLE — exact Bessel-ratio solve

Given unit vectors x_i = z_i/‖z_i‖ on S⁶ (d = 7):

```
r̄ = (1/N) Σ x_i          (mean resultant)
ρ  = ‖r̄‖,   μ̂ = r̄/ρ      (MLE mean direction)
κ solves  A_d(κ) = ρ,  A_d(κ) = I_{d/2}(κ) / I_{d/2−1}(κ)   (modified Bessel ratio)
```

**Newton solve**, derivative `A′(κ) = 1 − A(κ)² − (d−1)·A(κ)/κ`, initialized at the Banerjee et al. approximation (the v3 §2.2 formula — use it as *init and CI shortcut*, never as the final estimate):

```
κ₀ = clip[ ρ(d − ρ²)/(1 − ρ²), 1e−6, 500 ]
κ_{t+1} = clip[ κ_t − (A_d(κ_t) − ρ)/A′(κ_t) ]      iterate to |Δκ| < 1e−9
```

*(Verified numerically 2026-08-19: the closed form matches scipy's `ive(3.5)/ive(2.5)` to <1e−9 for κ ∈ [0.6, 500]; end-to-end Newton on exact vMF(7) samples recovers κ within expected small-N MLE error, e.g. κ=3→3.66, κ=15→17.0 at N=40. The init clip matters — unclipped, ρ→0.999 overflows `sinh`.)*

Guards: clamp ρ ≤ 0.999 and κ ≤ κ_max = 500 (saturation branch — the v0 dials *do* saturate); if N < 10 windows, return κ = None (not identifiable), never a fake number.

**numpy-only closed form for d = 7** (half-integer Bessels cancel their √(2/πκ) factors; keeps the repo's numpy-only rule, no scipy):

```
A₇(κ) = [ (1+15/κ²)cosh κ − (6/κ+15/κ³) sinh κ ] / [ (1+3/κ²) sinh κ − (3/κ) cosh κ ]
```

(small-κ branch `A₇ ≈ κ/7` for κ < 0.5 — the closed form catastrophic-cancels there; both numerator and denominator are O(κ³)/O(κ⁴) against O(1) terms). Verified: ratio → κ/7 as κ→0, → 1 − 3/κ as κ→∞.

**Uncertainty:** bootstrap (B = 200 window resamples) for the κ CI; jackknife for SE(μ̂), which doubles as the **drift deadband** (gate 4): an edge is real iff ‖Δμ̂‖ > 2·SE(μ̂). Stillness then reads as stillness.

**Honesty note for the future:** this same estimator on the 384-d encoder embeddings at N ≈ 15 clips has E‖r̄‖ ≈ √(N/d) ≈ 0.20 *under uniformity* — raw-mean ρ is garbage there and needs small-sample shrinkage. In dial space (d = 7, N ≥ 10) the bias is mild. The estimator code must carry this warning.

### 1.4 Warmth as a projection (the disambiguation)

Linearize v0 `warmth()` into z-space (the (v−0.5) centerings contribute only constant offsets, which vanish for a *direction* projection):

```
warmth_vMF = ŵ · μ̂ ,   w = (0.30, 0.10, 0.10, −0.15, 0.15, −0.10, 0.10)
             (mood, volume, earnest, cyn, joke, panic, presence),  ŵ = w/‖w‖
```

κ = tightness (§1.3); warmth = signed projection of the *direction* (this section). They are now different functionals of different statistics: warmth reads μ̂ only, κ reads ρ only, and ρ is invariant to rotating the sample — so warmth cannot move κ *by construction*, which is the disambiguation the gate demands. **"Temperature similarity" is an explicit function of both**, e.g. `D² = ‖μ̂−μ̂′‖² + λ·(Δ log κ)²` — never silently one or the other. Keep logging v0 `warmth()` on raw readings for series continuity; label the columns.

### 1.5 Diagnostics that ship with every fit

- **axis_spread** = per-dial std of the window sample. Anisotropy ratio (max/min) > 3 → κ is direction-dependent; report the caveat or whiten (corpus covariance) — do not silently report a scalar κ.
- **corr(warmth_vMF, log κ)** across nights: the v0 proxy *guarantees* a strong correlation (both norm-based); the MLE version should decouple. If |r| > 0.8 across ≥ 4 nights, the confound survived — investigate before trusting cross-room retrieval.
- **ρ, N, κ CI, W** always in the payload. A κ without its CI and N is not a number, it's a mood.

### 1.6 Code sketch (numpy-only, drop-in `elephant/vmf.py` or `scripts/vmf_snapshot.py`)

```python
import numpy as np
from elephant.room import Room

DIALS  = ["mood","volume","earnestness","cynicism","joke_landing","panic","presence"]
LO     = np.array([-1,0,0,0,-1,0,0], float); HI = np.array([1,1,1,1,1,1,1], float)
CENTER = np.array([0,0,.5,0,0,0,.5], float);  SCALE = 2.0/(HI-LO)      # z in [-1,1]
WARM   = np.array([.30,.10,.10,-.15,.15,-.10,.10]); WARM /= np.linalg.norm(WARM)
D, KMAX, NMIN = 7, 500.0, 10

def zvec(readings): return SCALE*(np.array([readings.get(n,0.0) for n in DIALS])-CENTER)

def windowed(room, bank, W=8, step=1, cap=64):
    out = []
    msgs = room.messages[-cap:]
    for i in range(0, len(msgs), step):
        sub = Room(room.name, msgs[max(0, i-W+1):i+1])
        z = zvec(bank.readings(sub))
        if np.linalg.norm(z) > 1e-3: out.append(z)                 # skip quiescent
    return out

def A7(k):                                                        # I_{7/2}/I_{5/2}
    if k < 0.5: return k/7.0                                      # series branch
    s, c = np.sinh(k), np.cosh(k)
    return ((1+15/k**2)*c - (6/k+15/k**3)*s) / ((1+3/k**2)*s - (3/k)*c)

def vmf_fit(zs, B=200, seed=0):
    X = np.asarray(zs, float); N = len(X)
    if N < NMIN: return None                                      # kappa: not identifiable
    X = X/np.linalg.norm(X, axis=1, keepdims=True)
    r = X.mean(0); rho = min(float(np.linalg.norm(r)), 0.999); mu = r/rho
    k = float(np.clip(rho*(D-rho**2)/(1-rho**2), 1e-6, KMAX))          # clipped init
    for _ in range(60):
        a = A7(k); g = 1 - a*a - (D-1)*a/k
        if abs(g) < 1e-12: break
        step = (a-rho)/g; k = float(np.clip(k-step, 1e-6, KMAX))
        if abs(step) < 1e-9: break
    rng = np.random.default_rng(seed); ks = []
    for _ in range(B):                                            # bootstrap CI on kappa
        rb = X[rng.integers(0,N,N)].mean(0); rh = min(float(np.linalg.norm(rb)), .999)
        ks.append(rh*(D-rh**2)/(1-rh**2))
    jk = np.stack([np.delete(X,i,0).mean(0) for i in range(N)])   # jackknife SE(mu)
    jk /= np.linalg.norm(jk, axis=1, keepdims=True)
    mu_se = float(np.sqrt((N-1)/N * ((jk - jk.mean(0))**2).sum()))
    return {"mu_hat": mu.tolist(), "kappa": k, "rho": rho, "n": N,
            "kappa_ci": [float(np.percentile(ks,2.5)), float(np.percentile(ks,97.5))],
            "warmth_vmf": float(WARM @ mu), "mu_se": mu_se,
            "axis_spread": X.std(0).tolist()}

def edge(fb, fa, db_factor=2.0):                                  # the field-edge + deadband
    if not fb or not fa: return None
    d_mu = float(np.linalg.norm(np.array(fa["mu_hat"])-np.array(fb["mu_hat"])))
    return {"d_mu": d_mu, "d_warmth": fa["warmth_vmf"]-fb["warmth_vmf"],
            "d_log_kappa": float(np.log(fa["kappa"]/fb["kappa"])),
            "real": d_mu > db_factor*max(fb["mu_se"], fa["mu_se"])}
```

Cost at Tap scale: O(n·W·dialcost) per session — negligible (n ≤ a few hundred); `cap=64` bounds long sessions.

### 1.7 Guards & failure modes

| Failure | Guard |
|---|---|
| N < 10 windows | κ = None; log N, never interpolate |
| ρ → 1 (dial saturation) | clamp 0.999; κ capped 500; flag `saturated: true` |
| ‖z‖ → 0 (quiescent room) | window skipped; if all skipped, no snapshot |
| Lexical dial correlation (mood/panic/cyn share word lists) | `axis_spread` anisotropy diagnostic; >3 → caveat or whiten |
| κ depends on W | log W; sensitivity sweep {4,8,16} in analysis |
| Overlapping-window autocorrelation | non-overlapping mode for CIs |
| Future 384-d use at N≈15 | √(N/d) uniformity bias ≈ 0.20 — shrinkage required (comment in code) |

---

## 2. GATE SCORECARD (devil's-advocate §4, against v0)

| # | Condition | Status | Blocker / what's buildable today |
|---|---|---|---|
| 1 | Fine room-gap opens 0.015 → toward 0.271, speaker-heldout intact | ❌ **BLOCKED** | Requires the contrast-trained head on the frozen v2 encoder (v3 §8 "next experiment"). The DialBank cannot move this number. (A cheap *dial-space* analog — can 7-dial window vectors classify the night? — is runnable today, but it is a sanity probe, not this condition.) |
| 2 | No collapse — within-room spread above a floor | 🟡 **PARTIAL** | Dial-space floor assertable **now**: mean pairwise (1−cos) of window vectors ≥ floor per room (encoder-side precedent 0.33–0.42; dial floor measured in the same calibration as #4). The binding form — spread preserved *while cross-room gap grows under training* — has no trained model to constrain yet. |
| 3 | κ = true vMF MLE, disambiguated from warmth | ✅ **BUILDABLE NOW** | §1 — pure post-processing on DialBank windows; exact Newton Bessel solve; warmth as μ̂-projection; `RoomField.concentration()` retired from comparison paths (docs-level; zero core code change needed to stop *calling* it). Residual risks (W-sensitivity, axis correlation, saturation) ship as diagnostics, not surprises. |
| 4 | Field-drift resolution above noise floor + deadband | 🟡 **PARTIAL** | Deadband (2× jackknife SE) and per-message edges buildable **now**. Blocker: the 0.05 floor is an *encoder* number; the dial-space floor is unmeasured. One-afternoon calibration: nights A–C between-night edges of the same cast = the empirical floor; until then, edges carry `real: null`, not `real: false`. |
| 5 | Cross-modal calibration + presence-as-mask | 🟡 **PARTIAL / N-A-now** | Calibration is vacuous while there is one modality (text dials) — blocked on v3 §5 fusion. Presence-as-mask **buildable now**: the log's `presence_mask` (§3) is the mask; speaker identity never enters the feature vector. The occupancy *dial* (pheromone trace) is room statistics, not roll-call — may stay a feature; flag its n-authors leakage risk. |
| 6 | Order-of-arrival logging | ✅ **BUILDABLE NOW** | §3 — ~60 additive lines on `TapNightSession`; ts-sorted messages, per-author interaction counters, and the per-speak raw field already exist in memory. Persistence + structure is all that's missing. |
| 7 | Retrieval stays a nudge | ✅ **BUILDABLE NOW** | MomentHit already carries readings+ts+space on every hit (honesty guarantee, tested). Add assert-tests: blend ≤ 0.15 bound, no popularity/retrieval-count term inside any field vector, no feedback path. Discipline, not code. |

**Score: 3 buildable now, 3 partial, 1 blocked.** The partials are blocked on *measurement* (dial noise floor) and *training* (encoder head, fusion) — not on the snapshot math.

---

## 3. MINIMAL INSTRUMENTED TAP SESSION (runs on existing `TapNightSession`, no rewrite)

### 3.1 Principle

**Log append-only facts at ingest; log cheap fits inline; derive everything else post-hoc.** The log must be replayable into the exact session state (order, fields, fits) without the session object. Three touchpoints only: `start_session`, `speak` (after the existing `raw = read_field(...)` line), `end_session`. JSONL, one event per line.

### 3.2 Schema

**`session_open`** (once):

| field | content |
|---|---|
| `v`, `type` | 1, "session_open" |
| `session_id`, `space_id` | uuid / room name |
| `t_start`, `clock_mode` | epoch or 0; "auto60" (STEP clock) or "explicit" |
| `reader` | `{kind: "RoomElephant", identity, bank: <fingerprint of dial class names>}` — **reader identity**; personal readers later add `{agent, preset_hash}` |
| `params` | `{W: 8, standardization: "z=2(v-c)/(hi-lo)", estimator: "vmf-mle-newton-v1", kappa_max: 500}` |
| `roster` | per participant: `to_dict()` (name, dial_weights, acclimation_rate, charisma) **+ `vibe_start`** |

**`speak`** (per message — the edge log):

| field | content | must? |
|---|---|---|
| `seq` | index in ts-sorted room = **order of arrival** | ✅ |
| `ts`, `author` | from the Message | ✅ |
| `text_sha256`, `len` (full `text` optional) | content identity | ✅ |
| `reactions` | emoji→count (the crowd's hands, per-dial attributable) | ✅ |
| `first_by_author` | true on the author's first-ever message — **the entry marker** | ✅ |
| `presence_mask` | authors with ≥1 message in trailing W=8 — occupancy *now* | ✅ |
| `field_raw_after` | the 7-vector `speak()` already computes and discards | ✅ |
| `field_eff_after` | charisma-displaced field | ✅ |
| `interactions_after` | per-author cumulative counts (charisma/acclimation inputs) | ✅ |
| `fit` | `{n, rho, mu_hat[7], kappa, kappa_ci, warmth_vmf, axis_spread}` or null | ✅ (cheap: O(64·W) per message) |
| `edge` | vs previous fit, with `real: null` until floor calibrated | derived-inline |

**`session_close`** (once): `t_end`, `cycle`, `final` = {all 9 raw readings, μ̂, κ, κ CI, warmth_v0, warmth_vMF, top_dials}, `n_messages`, free-text `notes`.

### 3.3 Per-message vs per-session split

- **Per message (irreducible):** seq, ts, author, text-id, reactions, first_by_author, presence_mask, field_raw_after, interactions_after. Lose one of these and the edge is unrecoverable.
- **Per session (irreducible):** roster + settings (incl. vibe_start — without it acclimation is unfittable), reader + bank fingerprint, estimator params, final fit.
- **Never logged (derived post-hoc from the JSONL):** edges' `real` flags (deadband depends on the calibration), rank curves, charisma shifts, cross-night comparisons, any retrieval join. This keeps the log append-only facts and the analysis versioned separately.

### 3.4 Exists already vs needs adding

**Already there (zero change):** ts-sorted `Room.messages` with author/reactions (stable sort + auto-clock ⇒ seq is robust); `_interactions` / `_reaction_heat` per author; the raw field computed *inside* `speak()`; `participant_state()` (vibe, vibe_start, interactions, reaction_heat); `settings()`/`load_settings()`; `end_session` warmth/κ line; MomentHit honesty in jepa_rag.

**Add (all additive, ~60 lines in `tapnight.py` + one new module):**
1. `__init__(..., log_path=None)` + `_emit(evt)` JSONL writer (~12 lines).
2. `start_session`: emit session_open (~10).
3. `speak`: capture `raw.tolist()`, `first_by_author` (check `_interactions` *before* increment), presence mask from trailing 8, inline `vmf_fit(windowed(...))`, emit (~18).
4. `end_session`: emit session_close (~8).
5. New `vmf.py` (§1.6, ~90 lines) + `test_edge_log.py` (~40 lines).

### 3.5 The session protocol (order-of-arrival as *experiment*, not statistics)

Per v3 §4, charisma vs acclimation is unidentifiable from a joint trajectory — the log only pays off if the sessions are designed:
- **Nights A, B, C** — same cast, fixed speaking order, reactions via the existing emoji API. Between-night edges of the *same* room = the dial-space noise-floor measurement (unblocks gate 4) and the κ/W sensitivity sweep.
- **Night D** — identical, plus one **designated newcomer** with known (vibe, charisma) entering at seq ≈ 60% (`first_by_author` flags entry, presence_mask shows the roster before/after). Occupants' μ̂ shifting toward the newcomer = **charisma**; newcomer's rank rising while occupants hold = **acclimation**. This is the only clean separator, and it costs one extra participant.

### 3.6 Validation tests

Assert: seq strictly increasing, ts non-decreasing; `presence_mask` == authors in trailing 8; κ null when n < NMIN else finite ≤ 500; every speak line carries the 7-vector; session_close `final` == refit from logged windows (replay honesty); replaying an identical message yields `edge.real == False` (deadband); no popularity/retrieval counter appears in any field vector (gate 7).

---

## 4. VERDICT

**Yes, defensibly, at the descriptive tier: the windowed-sample vMF MLE of §1 turns every room the DialBank can read into an honest (μ̂, κ, warmth) triple with CIs, a deadband, and shipped diagnostics — buildable this week with one new module and ~60 additive lines, and the §3 edge log makes Tap edges order-of-arrival-clean on the existing `TapNightSession` with no rewrite.** It is *not* yet the v3 trained room-embedding: gate 1 is blocked on the contrast head, gate 4's floor and gate 5's calibration on measurement and fusion — so cross-room retrieval keyed on dial-space fields is a v0.5 claim wearing v3's clothes until those close. **The single highest-risk assumption is dial-axis near-orthogonality/isotropy after standardization:** mood, panic, and cynicism share lexical triggers and the v0 dials saturate, so ‖r̄‖ — and therefore κ — partly measures *dial-construction agreement* rather than room tightness; if the axis-spread anisotropy ratio exceeds ~3, or corr(warmth_vMF, log κ) across nights stays beyond ±0.8, κ must be reported as direction-dependent (or the space whitened) — otherwise the snapshot silently re-imports the warmth/κ confound the gate exists to kill.

---

## Summary (10 lines)

1. v0 κ (`2‖v−0.5‖`) is a center-mismatched extremity proxy, collinear with |warmth| — retire from comparisons.
2. True κ: window the room (W=8), standardize dials to z∈[−1,1], unit-normalize, Newton-solve A₇(κ)=ρ (closed-form half-integer Bessel ratio, numpy-only; Banerjee formula as init/CI only).
3. Warmth = ŵ·μ̂ (projection on the linearized warm direction) — decoupled from κ by construction; log warmth_v0 for continuity.
4. Guards: κ=None under N<10 windows; ρ≤0.999, κ≤500 saturation caps; bootstrap CI; jackknife SE(μ̂) = drift deadband.
5. Gate scorecard: 3 of 7 buildable now (κ-MLE, order-of-arrival log, nudge discipline); 3 partial (spread floor, drift floor, presence-mask/modal calibration); 1 blocked (fine-gap opening — needs the encoder contrast head).
6. Dial-space noise floor is unmeasured (0.05 is encoder-side) — nights A–C of the same cast measure it; until then edges log `real: null`.
7. Edge log = JSONL on existing TapNightSession: session_open / speak / session_close; ~60 additive lines, three hook points, no rewrite.
8. Per-message musts: seq, ts, author, text-id, reactions, first_by_author, presence_mask, raw field, interactions; fits inline; analysis post-hoc.
9. Night D newcomer intervention (entry at seq≈60%) is the only charisma-vs-acclimation separator — design it in, don't hope for it.
10. Highest-risk assumption: dial-axis isotropy — lexical overlap + saturation can inflate κ independent of room tightness; ship axis_spread and the warmth/κ correlation as the tripwires.
