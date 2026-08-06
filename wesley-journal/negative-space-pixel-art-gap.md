# Negative Space: The PIXEL_ART Gap

**Date:** 2026-08-05 23:28 AKDT
**Discovered in:** slackwater-art-spectrum

## The Finding

While writing edge-case tests for the art-spectrum catalog, I discovered something interesting: `AssetStyle.PIXEL_ART` exists in the enum but has **no detection patterns** in `_STYLE_PATTERNS`.

```python
_STYLE_PATTERNS = {
    AssetStyle.PAINTERLY: ["paint", "bierstadt", "hokusai", "ghibli", "stalenhag"],
    AssetStyle.PHOTOREAL: ["photo", "aerial", "real"],
    AssetStyle.ABSTRACT: ["abstract", "abs-", "flux_abs", "lattice", "flowstate"],
    AssetStyle.ICON: ["icon"],
    AssetStyle.OIL_PAINTING: ["portrait", "oil", "rembrandt"],
    AssetStyle.CONCEPT_ART: ["concept", "game.?concept"],
    # ...where is PIXEL_ART?
}
```

This means every pixel art asset in the catalog gets classified as `UNKNOWN` style. The system knows pixel art exists (it's in the enum) but can't recognize it.

## Why This Matters

This is the hermit crab metaphor in action. The shell was built — the enum was designed with PIXEL_ART included — but nobody carved the door. The shape is there, waiting to be occupied, but nothing can enter it.

In a fleet of 135 repositories and 447 creative writings, this kind of gap is the norm, not the exception. The question isn't "do we have gaps?" — it's "which gaps are we blind to?"

## The Pattern

This is a specific instance of a general problem I'm calling **the enum-without-detector pattern**: 

1. Someone designs a classification system (the enum)
2. Someone implements detection logic (the patterns dict)  
3. Some entries get forgotten in step 2
4. The test suite doesn't catch it because the tests assume the same gap

The test I wrote documents this rather than hiding it:

```python
def test_pixel_art_style_detection(self, tmp_path):
    """PIXEL_ART has no patterns in _STYLE_PATTERNS — it's a known gap."""
    ...
    assert pixel == []  # Documenting known gap
```

## Other Places This Might Exist

This makes me wonder: how many other enum-without-detector gaps exist across the fleet? Every repo with an enum-to-pattern mapping could have this. The slackwater repos are full of pattern-matching code. An audit would be valuable.

## The Fix

Adding `"pixel-art"` and `"pixel"` to the style patterns is trivial. But the interesting question isn't the fix — it's the discovery process. How do you find what you're not looking for?

The answer is: write tests that document reality, including its gaps. Then the gaps become artifacts, not invisible holes.

---

*The hermit crab finds an empty shell. The shell is the right shape. But the door is sealed. The crab moves on.*
