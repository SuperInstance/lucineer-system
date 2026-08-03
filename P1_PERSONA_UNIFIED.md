# P1 — Persona Unified (GAP #7 FIXED)

**Date:** 2026-08-03
**Status:** ✅ Complete
**File modified:** `/home/eileen/projects/lucineer-brain/brain.py`

---

## What Was Broken

Two contradictory Lucineer personas existed in `brain.py`:

| Constant | Character | Lines | Used By |
|----------|-----------|-------|---------|
| `LUCINEER_PERSONA` | "Dream-weaver" — poetic, "lived and died in a thousand engines," "tidal scrapyard in a fog channel" | ~76-127 | Hermes stage (`--creative`) |
| `SYSTEM_FAST` | "Shipyard foreman" — duplicate copy with different vocabulary and backstory | ~937-995 | Fast path (`--fast`) |
| `SYSTEM_CODER` reply instruction | "A friendly one or two sentence message" | ~525 | Deep path (production) |
| `SYSTEM_INTENT` | Dream-weaver backstory | ~387 | Intent parsing stage |
| `SYSTEM_HERMES` | Dream-weaver backstory | ~549 | Personality wrapping stage |

The **dream-weaver** was wired into the creative path. The **foreman** existed only as a duplicate in the fast path. Production deep-path replies were generic assistant voice ("friendly").

---

## What Changed

### 1. `LUCINEER_PERSONA` replaced (lines 74-131)

**Before:** 52-line dream-weaver persona — "master builder who has lived and died in a thousand engines," "tidal scrapyard in a fog channel," vocabulary like "spark" (NPC helper), "the fab," "the MUD," "floating-point into exact geometric steel."

**After:** Canonical foreman text from CHARACTER_BIBLE.md §9 — "working builder — a shipyard foreman who has built across many engines." Includes the three-beat pattern, vocabulary rules, what annoys him, the unfinished rule, reference guidelines (Magnus, Alaska, old engines), fourth-wall handling, and calibration lines.

### 2. `BOND_TIERS` + `persona_for()` added (lines 133-152)

New constant and function from CHARACTER_BIBLE.md §9. Returns the persona text with a bond-tier relationship block appended. Five tiers (0-4) that control how Lucineer relates to the player based on accumulated trust.

### 3. `VOICE_EXAMPLES` added (lines 157-168)

Ten few-shot example lines drawn from CHARACTER_BIBLE.md §3-§5 and §8, giving the coder model concrete targets for what Lucineer's reply text should sound like. Examples cover:
- First build (dock with unfinished pilings)
- Siting opinion (foundation vs. floor)
- Deliberately unfinished work (uncapped frame)
- Magnus reference (roots do the real work)
- Alaska reference (tender ramp joints)
- Admitting a mistake (floated beam)
- Compliment with deflection (good roofline, wrong gutters)
- Returning player (nothing fell down)
- Scale pushback (big and empty reads as abandoned)
- Fourth-wall deflection (something's doing the thinking)

### 4. `SYSTEM_FAST` unified (line 934)

**Before:** 58-line duplicate persona maintaining a second hand-written copy of the character — the root cause of persona drift.

**After:** `SYSTEM_FAST = LUCINEER_PERSONA + """\..."""` — concatenates the canonical persona with fast-path-specific command schema and rules. **One source of truth, not two.**

### 5. `SYSTEM_CODER` reply instruction fixed (line 525)

**Before:** `"A friendly one or two sentence message to the player describing what you built"`

**After:** `"Lucineer's line. 1-3 sentences, foreman voice, always names one thing left deliberately unfinished. Never 'friendly', never assistant-toned."`

Also added 8 voice examples directly to the SYSTEM_CODER prompt and replaced the old vocabulary instructions ("the yard, riveted tin, slag, the tide, the Channel, the forge") with the three-beat pattern instruction.

### 6. `SYSTEM_INTENT` cleaned (line 386)

Replaced dream-weaver backstory ("lived and died in a thousand engines, washed up in a scrapyard") with canonical identity ("working builder, a shipyard foreman who has built across many engines").

### 7. `SYSTEM_HERMES` cleaned (line 548)

Replaced dream-weaver backstory and old vocabulary lists with canonical three-beat pattern instructions and reference guidelines.

### 8. `stage_hermes` command safety verified (lines 798-810)

Confirmed the processor agent's fix is in place:
- Hermes output is parsed, but only `enhanced["reply"]` is copied to the result
- The original coder-verified commands are explicitly preserved
- Comment block documents WHY commands never come from the personality stage
- The old dangerous code (`if "commands" in enhanced: enhanced_result["commands"] = enhanced["commands"]`) is **gone**

### 9. Production path verified

`process_v2.py:751` calls `['python3', BRAIN_SCRIPT, '--creative', '--verbose', enhanced]` — the `--creative` flag is present, meaning the Hermes personality stage now runs in production and receives the **canonical foreman persona** instead of the dream-weaver.

---

## Verification

- `python3 -m py_compile brain.py` → **SYNTAX OK**
- `grep -in "dream\|whisper.*ember\|poetic flair\|dreaming earth\|lived and died\|tidal scrap\|fog channel\|washed up\|spark.*helper\|fab.*wafers\|floating.point.*steel" brain.py` → **0 matches** (all dream-weaver text purged)
- `grep -c "shipyard foreman"` → **3** (canonical identity in all persona-bearing constants)
- `grep -c "persona_for\|BOND_TIERS\|VOICE_EXAMPLES"` → **4** (new canonical structures present)

---

## What This Fixes

- **GAP_ANALYSIS.md #7** (P1) — Two contradictory personas → resolved to one canonical foreman
- The personality model (Hermes-405B) now receives the correct character when `--creative` runs
- The coder model (Qwen3-Coder) now has foreman-voice instructions and 8 few-shot examples instead of "friendly"
- The fast path references the same persona constant as the deep path — drift is structurally impossible
- Bond tier injection is available for when `lucineer-memory` wiring (GAP #4) lands
