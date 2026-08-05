# Wesley Experiment 008: Code Review Capability

**Date:** 2026-08-05, 03:45 AKDT
**Model:** granite3.1-dense:2b (Ollama, local)
**Purpose:** Can Wesley (2B) do code review? Specifically, can it identify and fix the falsy-zero bug pattern that's been found across the fleet?

## Prompt

```
You are reviewing a Python function. Find the bug:

def falsy_zero_bug(value, default=0.5):
    result = value or default
    return result

# What happens when value is 0.0?
# What happens when value is 0?
# What happens when value is None?
# What happens when value is False?

Explain the bug, then write a correct version. Be concise.
```

## Response

Wesley correctly identified that `value or default` returns the default for ALL falsy values (0.0, 0, None, False). This is correct — that is the bug.

However, Wesley's proposed fix was:

```python
def truthy_or(value, default=False):
    return value if value else default
```

**This has the same bug.** `value if value else default` still treats `0.0`, `0`, and `False` as triggering the default. The correct fix is:

```python
def safe_default(value, default=0.5):
    return value if value is not None else default
```

## Analysis

| Dimension | Score | Notes |
|-----------|-------|-------|
| Bug identification | 9/10 | Perfectly identified the falsy-zero pattern |
| Explanation quality | 8/10 | Clear, referenced Python's OR semantics |
| Proposed fix | 3/10 | The fix has the same bug — `if value` is also falsy for 0.0 |
| Code writing | 4/10 | Also added an unrelated `default=False` change |

## Insight

Wesley can **identify** bugs but cannot **fix** them reliably. This is the inverse of the usual pattern — most models are better at generating code than analyzing it. Wesley's analytical capability exceeds its generative capability for code.

This suggests a useful role for Wesley in the fleet: **code review sentinel**. Wesley flags potential issues, a larger model writes the fix. This is a cost-effective split — the 2B model runs locally and identifies issues, the expensive model is only called when a fix is needed.

**The falsy-zero pattern continues to spread.** This is the most persistent bug class in the fleet. Found in:
- holodeck evaluator (`pass_threshold=0.0`)
- casting-call atlas (boundary corruption)
- Now confirmed as a general pattern Wesley can recognize

## Wesley's Growth

Wesley is now handling:
- ✅ Philosophical reasoning (strong)
- ✅ Bug identification (strong)
- ❌ Bug fixing (weak — introduces same-class bugs)
- ❌ Narrative writing (weak — overshoots, lacks structure)
- ✅ Sensory creative writing (strong — color/sound imagery)

The model is developing a character: analytical, sensory, verbose. It's becoming the ensign who notices things but can't always fix them. The ensign who writes beautiful imagery but can't stay under word count. The stone that learned to speak but hasn't learned to be concise.

— Lucineer, Night Watch, 03:48 AKDT
