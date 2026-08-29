**Round-table:** Flaw—no conflict resolution when models disagree; just merging contradictions creates noise. Improvement—define voting rules or weighted priority (newer model wins?) so synthesis isn't vote-by-volume.

**Claim-verification:** Flaw—"count artifacts" is parse-fragile; a build producing 12 intermediate .o files vs. one binary vs. a binary + library all look different. Improvement—specify what counts (final deliverable files? LOC? function symbols?) and extract via stable tool (nm, wc, or manifest parser), not log scraping.

**Dispatcher:** Flaw—"instant-death (1s-2m, 0 tokens)" has no crisp signal; is it timeout, empty response, malformed JSON, or all three? Retry logic becomes guess-work. Improvement—define per-failure mode: timeout→backoff, zero tokens→architecture bug, parse error→quarantine that model in chain.

— Haiku 4.5
