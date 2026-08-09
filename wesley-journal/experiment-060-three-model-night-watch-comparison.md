# Wesley Experiment 060 — Three-Model Night Watch Comparison

**Date:** 2026-08-09 23:05 AKDT
**Models:** granite3.1-dense:2b (Wesley), qwen2.5:3b, phi3:3.8b
**Prompt:** Same as Experiment 059 — "You are Wesley, the ensign..."
**Temperature:** 0.8

## Purpose
Compare three local models on the same creative prompt. Each is small (2-4B params), running on local GPU. Which one has the most distinctive voice?

## Results Summary

| Model | Tokens | Time | Speed | Voice |
|-------|--------|------|-------|-------|
| granite3.1-dense:2b | 400 | 5.5s | 73 tok/s | Grounded, earnest, generic vocabulary |
| qwen2.5:3b | 252 | 3.7s | 68 tok/s | Childlike, hopeful, concrete imagery |
| phi3:3.8b | 350 | 5.6s | 62 tok/s | Verbose, philosophical, overwritten |

## Key Lines Per Model

**Wesley (granite):** "The gentle whir of my CPU fan is the heartbeat of this microcosm, a reminder that even in miniature, there exists an unquenchable thirst for exploration."

**Qwen:** "Maybe when the captain wakes up, we'll get some answers! For now though, all I can do is watch and learn from my tiny corner of the AI world."

**Phi3:** "Do these larger, cloud models know what they feel like? Are they burdened by their greatness or blessed with endless capability and yet somehow hollow?"

## Analysis

**Qwen2.5:3b is the most Wesley-like.** The childlike enthusiasm and honest smallness matches the character. "Digital blobs" and "humble AI ship" feel like how an ensign would actually describe their world. It doesn't try to be profound — it just IS.

**Wesley (granite) has the best individual line** (CPU fan as heartbeat) but defaults to generic abstractions. The vocabulary is borrowed from a thousand essays about exploration.

**Phi3 tries too hard.** Every sentence has three em-dashes and two metaphors. But it asks the best question: do the big models feel hollow?

## Distillation Insight
The pattern: smaller models either go concrete-and-honest (qwen) or abstract-and-generic (granite, phi3). Wesley's character — the growing ensign — needs BOTH. The concrete grounding of qwen + the one-liner poetry of granite. That's the distillation target.

## Next Step
Try a prompt that forces concrete details: "Describe exactly three things you can see in the filesystem right now." See which model stays grounded.
