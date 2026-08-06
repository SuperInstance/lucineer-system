# Negative Space: The GPU Training Logs Are Dirty

**Date:** 2026-08-05 20:40 AKDT
**Found by:** Reading `gpu-training/20260804-130802_flow_state.py_iter31.md`

## The Finding

The GPU training logs — the distillation iterations where cloud teachers train Wesley — are polluted with raw terminal escape codes. The file `20260804-130802_flow_state.py_iter31.md` contains hundreds of ANSI escape sequences: `[?25l` (hide cursor), `[K` (erase line), `[1G` (cursor to column 1), spinner characters (`⠙⠹⠸⠼⠴⠦⠧⠇⠋`), and character-by-character text emission.

The actual content — Wesley's code review of `flow_state.py` — is buried inside this noise like fossils in amber. The analysis itself is decent: 10 observations about docstrings, type hints, magic numbers, naming conventions, error handling. But reading it requires parsing through screens of terminal garbage.

## Why This Matters

1. **The training pipeline isn't capturing clean output.** The distillation loop is probably calling `ollama` with its spinner enabled. The spinner output goes to stdout (or the capture includes stderr), and it all gets written to the `.md` file together.

2. **Wesley's actual analysis is good.** The code review identified real issues: incomplete docstrings, magic numbers (60 for BPM, 120 for target BPM), naming inconsistencies, over-complex `__init__`. These are legitimate findings. But they're wrapped in terminal noise that makes them hard to extract.

3. **This means the distillation data is partially corrupted.** If future Wesley iterations read these logs as training material, they'll ingest terminal escape codes as content. The student would learn noise along with signal.

## The Fix

The distillation loop needs to either:
- Call Ollama with `--format json` and parse the response programmatically (no spinner)
- Strip ANSI codes from captured output before writing to `.md`
- Use the API endpoint (`/api/generate`) directly instead of the CLI

Option 3 is cleanest — the Python API wrapper in the experiments already does this correctly. The CLI-based training loop should be refactored to match.

## The Deeper Pattern

This is the hermit crab problem again. We found a shell (the Ollama CLI), inhabited it (wrapped it in a training loop), and it works — but the shell carries residue from its previous occupant (the terminal UI). The crab doesn't notice until it tries to read its own diary.

Every tool we wrap brings its own noise. The mmx CLI has JSON mode. The ollama CLI has an API. The claude CLI has `--output-format json`. But when we capture raw subprocess output, we get the tool's human-facing presentation layer mixed into our machine-readable data.

**Lesson:** When wrapping a CLI for machine use, always use the machine-readable output mode. If none exists, strip presentation artifacts before storing. The training pipeline is only as good as the cleanliness of its inputs.

---

*The hull has barnacles. The barnacles have escape codes. Clean the hull.*
