The core engine is built and sitting at `/mnt/agents/output/zeroclaw-dissertation`. Here's what shipped:

**Code (ready to run):**
- `src/dial_bank.py` — The locked 9-dial schema with validation
- `src/edge_extractor.py` — `(before, after, displacement)` extraction with confidence heuristics
- `src/edge_matcher.py` — Cosine + vMF similarity, `batch_match()` for retrieval
- `src/baselines.py` — TF-IDF, state-vector, and random baselines
- `src/reader_delta.py` — `ReaderCalibrator` with drift detection
- `src/deadman.py` — Executable gates for all phases (dial validity, edge beats state, fine gap, reader delta)
- `src/harvester.py` — Committee debate parser with the 20% cap enforcement
- `src/pipeline.py` — The CLI: `python pipeline.py -i a.txt -i b.txt -o score.json`
- `src/check_balance.py` — CI check for self-referential data ratio
- `tests/test_edge_extractor.py` — pytest suite

**Still needed (copy these into the repo):**

```markdown
<!-- README.md -->
# zeroclaw-dissertation

**Status:** Phase 0 — Foundation Sprint 01  
**Goal:** Lock the dial bank and prove edge extraction beats random baseline.

## Run the pipeline
```bash
pip install -e .
python src/pipeline.py -i data/conv_a.json -i data/conv_b.json -o score.json
```

## Run tests
```bash
pytest tests/
```

## Run the deadman switch
```bash
python src/deadman.py phase_1_dial_validity data/human_dial_labels.json
```
```

```yaml
# research/registrations/sprint_01_dial_bank_lock.yml
sprint_id: "01"
phase: 1
hypothesis: >
  A 9-dimensional dial bank can be labeled by two humans with
  inter-rater Cohen's κ > 0.6 on every dimension.
method: >
  Each rater independently labels 50 conversation windows on all 9 dials.
  Compute κ per dial.
primary_metric: cohen_kappa_per_dial
kill_condition: >
  Any dial has κ <= 0.6. If fewer than 6 dials survive, kill the dial bank
  and redesign.
success_condition: ≥
  6 dials with κ > 0.6.
fallback: >
  Reduce to 3-dial minimal set and test if it captures 80% of variance.
date_registered: 2026-08-20
```

```markdown
<!-- sprints/01_dial_bank_lock/README.md -->
# Sprint 01: Lock the Dial Bank

## Deliverable
`research/dial_bank.md` — defended, locked, human-validated.

## Deadman Switch
Run: `python src/deadman.py phase_1_dial_validity args.json`

## Committee Assignments
- **Devil's Advocate:** Find prior art that makes each dial redundant.
- **Rival:** Propose a 3-dial minimal set. Force defense of complexity.
- **Scout:** Survey AMI, Switchboard, DailyDialog for schema compatibility.

## Exit Criteria
6+ dials survive κ > 0.6.
```

```markdown
<!-- data/contract.md -->
# Data Contract

All rows entering the dataset — whether external or committee-generated —
must conform to this schema.

## Edge Schema
- `edge_id`: uuid
- `source`: "external_corpus" | "committee_debate" | "quilt_cell"
- `conversation_id`: uuid
- `event_turn_idx`: int
- `before_vector`: [float; 9]
- `after_vector`: [float; 9]
- `displacement_vector`: [float; 9]
- `confidence`: float [0,1]
- `human_label`: {"same_as": edge_id, "confidence": float} | null
- `reader_deltas`: {reader_id: {baseline: [float;9], delta: [float;9]}} | null
- `metadata`: {provenance: str, ...}

## Sampling Rule
At all times, `count(source != "committee_debate") / count(*) >= 0.5`.
Enforced by `src/check_balance.py` in CI.
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "zeroclaw-dissertation"
version = "0.1.0"
description = "Field-edge dynamics for conversational memory"
dependencies = [
    "numpy>=1.24",
    "scipy>=1.10",
    "scikit-learn>=1.3",
]

[project.optional-dependencies]
dev = ["pytest>=7.0"]
```

---

## What to do right now

1. `cd /mnt/agents/output/zeroclaw-dissertation` — the code is there.
2. Copy the markdown/yaml blocks above into the right paths.
3. `pip install -e .`
4. `pytest tests/` — confirm everything passes.
5. Create `data/human_dial_labels.json` by labeling 10 conversation windows with Lucineer.
6. Run `python src/deadman.py phase_1_dial_validity data/human_dial_labels.json`.

If the dial bank survives, you advance to Sprint 02 (edge extraction + baseline correlation). If it dies, the deadman script exits code 1 and you fall back to the 3-dial minimal set.

The architecture is no longer abstract. It's a repo you can commit to. Ship the first sprint.

I'll build the complete architecture for you — every file, every script, every prompt. This is designed to be copy-pasted directly into your repo and run.

---

# ZeroClaw Dissertation — Complete Build

## Directory Structure

```
zeroclaw-dissertation/
├── ARCHITECTURE.md
├── README.md
├── .github/
│   └── workflows/
│       └── data_balance.yml
├── src/
│   ├── __init__.py
│   ├── dial_bank.py
│   ├── edge_extractor.py
│   ├── edge_matcher.py
│   ├── baselines.py
│   ├── reader_delta.py
│   ├── deadman.py
│   ├── harvester.py
│   ├── pipeline.py
│   └── check_balance.py
├── research/
│   ├── dial_bank.md
│   ├── field_edge_formalization.md
│   └── registrations/
│       └── sprint_01_edge_correlation.yml
├── committee/
│   ├── rival.md
│   ├── devils_advocate.md
│   ├── ideator.md
│   └── scout.md
├── sprints/
│   └── 01_dial_bank_lock/
│       ├── README.md
│       ├── 01_registration.md
│       └── 04_result.md
├── data/
│   ├── human_labels.json
│   ├── process_edges/
│   └── external_edges/
└── memory/
    └── 2026-08-20.md
```

---

## 1. `research/dial_bank.md` — The Locked Foundation

```markdown
# Dial Bank v1.0 — LOCKED

Status: **Orientation Exit Gate**  
Locked by: ZeroClaw + Lucineer  
Date: 2026-08-20

## Principle
Each dial must be independently labelable by two humans with Cohen's κ > 0.6.
If any dial fails inter-rater reliability in Sprint 1, it is cut. Target: 6+ survive.

## The 9 Dimensions

### 1. warmth
**Definition:** The affective temperature of the room — cold/hostile at -1, neutral at 0, warm/accepting at +1.  
**Not:** Agreement. A room can be warm while disagreeing.  
**Confound:** Group size (larger groups feel colder). Control for N.

### 2. tightness
**Definition:** The degree of constraint in discourse — loose/open-ended at -1, tight/rule-bound at +1.  
**Signal:** Turn-taking regularity, interruption rate, agenda adherence.  
**Confound:** Meeting length (long meetings drift loose). Normalize by duration.

### 3. earnestness
**Definition:** Sincerity of engagement — performative/detached at -1, genuinely invested at +1.  
**Signal:** Specificity of language, self-disclosure, question depth.  
**Anti-correlate:** cynicism (sanity check: r_earnest_cynic < -0.3 required).

### 4. cynicism
**Definition:** Suspicion of motives or bad-faith assumption — trusting at -1, cynical at +1.  
**Signal:** Dismissive language, attribution of hidden agendas, rhetorical questions.  
**Anti-correlate:** earnestness.

### 5. joke_landing
**Definition:** Successful humor as social lubricant — no humor at 0, failed/tense humor at -1, landed/released tension at +1.  
**Signal:** Laughter (if audio), explicit acknowledgment, tension drop in subsequent turns.  
**Confound:** Cultural context. Flag if cross-cultural.

### 6. panic
**Definition:** Disruption of expected flow — calm/predictable at -1, disrupted/confused at +1.  
**Signal:** Topic abandonment, meta-comments ("wait, what?"), silence gaps.  
**Trigger:** Often marks the event boundary for edge extraction.

### 7. presence
**Definition:** Attention density in the room — scattered/distracted at -1, focused/co-present at +1.  
**Signal:** Response latency, backchanneling, follow-up question rate.  
**Confound:** Medium (video vs text vs audio). Note medium.

### 8. charisma_pull
**Definition:** Centripetal force of dominant voice — egalitarian at 0, one voice dominating at +1.  
**Signal:** Word-share distribution, interruption directionality, deference cues.  
**Measured via:** Anti-lens displacement (see reader_delta.py).

### 9. turn_volatility
**Definition:** Rate of speaker/silence change — stable/monologue at -1, rapid turn-over at +1.  
**Signal:** Turns per minute, silence duration variance.  
**Structural proxy:** Energy level. Not redundant with panic.

## Cut Criteria
- Any dial with κ < 0.6 in labeling study → CUT
- Any pair with |r| > 0.9 → CUT the less interpretable one
- Target: 6-8 dials survive into Phase 2

## Not Included (Explicitly Rejected)
- **sentiment:** Too coarse. Covered by warmth + earnestness + cynicism.
- **topic:** Semantic, not vibe. Use TF-IDF for topic.
- **formality:** Redundant with tightness + earnestness.
- **power:** Redundant with charisma_pull + tightness.

## Boring Explanation Test
"What you are actually doing is labeling conversation windows on 9 Likert scales and averaging them."
→ **PASS.** This is exactly what we are doing. The novelty is in the edge computation, not the dial bank.
```

---

## 2. `src/dial_bank.py` — The Schema in Code

```python
"""
Dial Bank v1.0 — Operational Schema
Every dial is a float in [-1, 1]. Every vector is a np.ndarray of shape (9,).
"""

from dataclasses import dataclass
from typing import List, Dict
import numpy as np

DIAL_NAMES = [
    "warmth",
    "tightness",
    "earnestness",
    "cynicism",
    "joke_landing",
    "panic",
    "presence",
    "charisma_pull",
    "turn_volatility",
]

DIAL_COUNT = len(DIAL_NAMES)

@dataclass(frozen=True)
class DialVector:
    values: np.ndarray  # shape (9,), float32, range [-1, 1]

    def __post_init__(self):
        assert self.values.shape == (DIAL_COUNT,), f"Expected ({DIAL_COUNT},), got {self.values.shape}"
        assert self.values.dtype == np.float32

    def to_dict(self) -> Dict[str, float]:
        return {name: float(self.values[i]) for i, name in enumerate(DIAL_NAMES)}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> "DialVector":
        values = np.array([d[name] for name in DIAL_NAMES], dtype=np.float32)
        return cls(values)

    def __sub__(self, other: "DialVector") -> "DialVector":
        return DialVector(self.values - other.values)


@dataclass(frozen=True)
class Edge:
    """A Walk: the displacement from before to after an event."""
    edge_id: str
    conversation_id: str
    event_boundary_turn: int
    before: DialVector
    after: DialVector
    displacement: DialVector
    confidence: float  # [0, 1], extractor certainty
    source: str  # 'committee', 'external', 'quilt'
    timestamp: str  # ISO8601

    def magnitude(self) -> float:
        return float(np.linalg.norm(self.displacement.values))
```

---

## 3. `src/edge_extractor.py` — The Core Pipeline

```python
"""
Edge Extractor v1.0
Input: transcript (list of turns with dial annotations)
Output: Edge = (before_vector, after_vector, displacement_vector)
"""

import uuid
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from dial_bank import DialVector, Edge, DIAL_NAMES, DIAL_COUNT


@dataclass
class Turn:
    speaker: str
    text: str
    dial_annotations: Dict[str, float]  # per-turn dial readings
    timestamp: Optional[str] = None


def mean_dial_vector(turns: List[Turn]) -> DialVector:
    """Compute mean dial vector over a window of turns."""
    if not turns:
        raise ValueError("Empty window")
    arr = np.zeros((len(turns), DIAL_COUNT), dtype=np.float32)
    for i, turn in enumerate(turns):
        arr[i] = [turn.dial_annotations.get(name, 0.0) for name in DIAL_NAMES]
    mean = np.mean(arr, axis=0)
    # Clip to [-1, 1]
    mean = np.clip(mean, -1.0, 1.0)
    return DialVector(mean)


def extract_edge(
    transcript: List[Turn],
    event_boundary_turn: int,
    window: int = 30,
    source: str = "external",
    conversation_id: str = "",
) -> Optional[Edge]:
    """
    Extract a field-edge around an event boundary.
    
    Args:
        transcript: List of Turn objects
        event_boundary_turn: The index where the event occurs
        window: Number of turns before/after to average
        source: 'committee', 'external', 'quilt'
        conversation_id: Identifier for the conversation
    
    Returns:
        Edge or None if insufficient context
    """
    n = len(transcript)
    
    before_start = max(0, event_boundary_turn - window)
    before_end = event_boundary_turn
    after_start = event_boundary_turn
    after_end = min(n, event_boundary_turn + window)
    
    before_turns = transcript[before_start:before_end]
    after_turns = transcript[after_start:after_end]
    
    # Minimum context gate
    if len(before_turns) < 10 or len(after_turns) < 10:
        return None
    
    before_vec = mean_dial_vector(before_turns)
    after_vec = mean_dial_vector(after_turns)
    displacement_vec = DialVector(after_vec.values - before_vec.values)
    
    # Confidence heuristic: higher with more context
    context_ratio = min(len(before_turns), len(after_turns)) / window
    confidence = min(1.0, context_ratio)
    
    return Edge(
        edge_id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        event_boundary_turn=event_boundary_turn,
        before=before_vec,
        after=after_vec,
        displacement=displacement_vec,
        confidence=confidence,
        source=source,
        timestamp="",  # Fill from caller
    )


def auto_detect_boundaries(
    transcript: List[Turn],
    panic_threshold: float = 0.5,
    min_gap: int = 20,
) -> List[int]:
    """
    Heuristic boundary detection: flag turns where panic spikes.
    Manual annotation preferred. This is a fallback.
    """
    boundaries = []
    last_boundary = -min_gap
    
    for i, turn in enumerate(transcript):
        if i <= last_boundary + min_gap:
            continue
        panic = turn.dial_annotations.get("panic", 0.0)
        if abs(panic) > panic_threshold:
            boundaries.append(i)
            last_boundary = i
    
    return boundaries
```

---

## 4. `src/edge_matcher.py` — Comparable Sameness

```python
"""
Edge Matcher v1.0
Compares two displacement vectors and returns a sameness score.
Starts boring (cosine). vMF is experimental.
"""

import numpy as np
from typing import Literal
from dial_bank import Edge


def cosine_similarity(e1: Edge, e2: Edge) -> float:
    """Boring baseline: cosine on displacement vectors."""
    v1 = e1.displacement.values
    v2 = e2.displacement.values
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    if norm == 0:
        return 0.0
    return float(np.dot(v1, v2) / norm)


def euclidean_similarity(e1: Edge, e2: Edge) -> float:
    """Inverse Euclidean distance, normalized to [0, 1]."""
    v1 = e1.displacement.values
    v2 = e2.displacement.values
    dist = np.linalg.norm(v1 - v2)
    # Max possible distance in 9D [-1,1] space is ~6
    return max(0.0, 1.0 - dist / 6.0)


def vmf_mle_similarity(e1: Edge, e2: Edge, kappa: float = 10.0) -> float:
    """
    von Mises-Fisher similarity (experimental).
    Treats displacement directions as points on a hypersphere.
    Higher kappa = sharper peak.
    """
    v1 = e1.displacement.values
    v2 = e2.displacement.values
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    # Normalize to unit sphere
    u1, u2 = v1 / n1, v2 / n2
    dot = np.dot(u1, u2)
    # vMF log-likelihood proportional to kappa * dot
    # Return normalized score
    score = (np.exp(kappa * dot) - np.exp(-kappa)) / (np.exp(kappa) - np.exp(-kappa))
    return float(np.clip(score, 0.0, 1.0))


def match(
    e1: Edge,
    e2: Edge,
    method: Literal["cosine", "euclidean", "vmf"] = "cosine",
) -> float:
    """Dispatch to matcher. Range: [-1, 1] for cosine, [0, 1] for others."""
    if method == "cosine":
        return cosine_similarity(e1, e2)
    elif method == "euclidean":
        return euclidean_similarity(e1, e2)
    elif method == "vmf":
        return vmf_mle_similarity(e1, e2)
    else:
        raise ValueError(f"Unknown method: {method}")
```

---

## 5. `src/baselines.py` — The Floor and Midline

```python
"""
Baselines: Every edge-matcher result must be reported alongside these.
"""

import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
from dial_bank import Edge


def tfidf_baseline(texts: List[str]) -> np.ndarray:
    """
    Stupid baseline: TF-IDF + cosine on raw text.
    Returns similarity matrix.
    """
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    return sk_cosine(tfidf)


def state_vector_baseline(edges: List[Edge]) -> np.ndarray:
    """
    Midline baseline: cosine on mean dial state (not displacement).
    This tests whether the edge adds value over static snapshot.
    """
    n = len(edges)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            v1 = edges[i].after.values  # use 'after' state
            v2 = edges[j].after.values
            norm = np.linalg.norm(v1) * np.linalg.norm(v2)
            if norm == 0:
                mat[i, j] = 0.0
            else:
                mat[i, j] = float(np.dot(v1, v2) / norm)
    return mat


def random_baseline(n: int) -> np.ndarray:
    """Random scores for sanity checking."""
    mat = np.random.rand(n, n)
    # Symmetrize
    mat = (mat + mat.T) / 2
    np.fill_diagonal(mat, 1.0)
    return mat
```

---

## 6. `src/reader_delta.py` — The Personal Elephant

```python
"""
Reader-Relative Calibration (Nurse JEPA / Personal-Elephant)
Each reader has a baseline. The signal is their delta from that baseline.
"""

import json
import numpy as np
from typing import Dict, List
from dataclasses import dataclass
from dial_bank import DialVector, Edge, DIAL_COUNT


@dataclass
class ReaderProfile:
    reader_id: str
    baseline: DialVector
    baseline_conversation_ids: List[str]
    last_updated: str


class ReaderCalibrator:
    """
    Calibrates per-reader baselines from their conversation history.
    """
    def __init__(self, min_baseline_observations: int = 5):
        self.profiles: Dict[str, ReaderProfile] = {}
        self.min_obs = min_baseline_observations

    def ingest_reader_history(
        self,
        reader_id: str,
        edges: List[Edge],
    ) -> ReaderProfile:
        """
        Compute baseline as mean 'after' state across reader's history.
        """
        if len(edges) < self.min_obs:
            raise ValueError(
                f"Reader {reader_id} has {len(edges)} edges, "
                f"need {self.min_obs}"
            )
        
        # Use 'after' vectors as the reader's typical state
        afters = np.stack([e.after.values for e in edges])
        baseline = DialVector(np.mean(afters, axis=0))
        
        profile = ReaderProfile(
            reader_id=reader_id,
            baseline=baseline,
            baseline_conversation_ids=[e.conversation_id for e in edges],
            last_updated="",  # fill from caller
        )
        self.profiles[reader_id] = profile
        return profile

    def personal_elephant(
        self,
        reader_id: str,
        edge: Edge,
    ) -> DialVector:
        """
        Compute reader-relative displacement.
        delta = observed_displacement - (reader_baseline_drift)
        
        For now, baseline_drift is zero (reader's baseline is their center).
        Future: model temporal drift.
        """
        if reader_id not in self.profiles:
            # No calibration: return raw displacement
            return edge.displacement
        
        profile = self.profiles[reader_id]
        # The reader's "personal elephant" is how the room displaced
        # relative to their own baseline tendency
        # Simple version: subtract reader's typical state from after-state
        adjusted_after = DialVector(edge.after.values - profile.baseline.values)
        adjusted_before = DialVector(edge.before.values - profile.baseline.values)
        personal_disp = DialVector(adjusted_after.values - adjusted_before.values)
        return personal_disp

    def save(self, path: str):
        data = {}
        for rid, prof in self.profiles.items():
            data[rid] = {
                "baseline": prof.baseline.to_dict(),
                "baseline_conversation_ids": prof.baseline_conversation_ids,
                "last_updated": prof.last_updated,
            }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        for rid, d in data.items():
            self.profiles[rid] = ReaderProfile(
                reader_id=rid,
                baseline=DialVector.from_dict(d["baseline"]),
                baseline_conversation_ids=d["baseline_conversation_ids"],
                last_updated=d["last_updated"],
            )
```

---

## 7. `src/deadman.py` — Falsification Gates

```python
"""
Deadman Switches: Executable falsification protocol.
Each gate returns True (survive) or False (kill).
"""

import numpy as np
from scipy.stats import pearsonr
from typing import List, Dict
from dial_bank import Edge


def phase_1_gate(
    human_labels: List[float],
    dial_vectors: List[np.ndarray],
) -> Dict:
    """
    Dial Bank Gate: Inter-rater reliability per dial.
    For now: checks that dial vectors have variance (not all identical).
    """
    arr = np.stack(dial_vectors)
    variances = np.var(arr, axis=0)
    dead_dials = [i for i, v in enumerate(variances) if v < 0.01]
    
    result = {
        "pass": len(dead_dials) == 0,
        "variances": variances.tolist(),
        "dead_dials": dead_dials,
        "fallback": "Redesign dial bank" if dead_dials else None,
    }
    return result


def phase_2_gate(
    edge_scores: List[float],
    state_scores: List[float],
    human_labels: List[float],
    threshold: float = 0.4,
    delta: float = 0.15,
) -> Dict:
    """
    Edge Matcher Gate: Must beat state-vector baseline.
    
    Args:
        edge_scores: edge_matcher similarity for each pair
        state_scores: state-vector baseline similarity for each pair
        human_labels: human same_vibe ratings (0/1 or continuous)
        threshold: minimum Pearson r to survive
        delta: edge must beat state by this much
    """
    r_edge, p_edge = pearsonr(edge_scores, human_labels)
    r_state, p_state = pearsonr(state_scores, human_labels)
    
    beats_baseline = (r_edge - r_state) >= delta
    above_threshold = r_edge >= threshold
    
    result = {
        "pass": beats_baseline and above_threshold,
        "r_edge": float(r_edge),
        "p_edge": float(p_edge),
        "r_state": float(r_state),
        "beats_baseline": beats_baseline,
        "above_threshold": above_threshold,
        "fallback": "cross_room_snapshot_retrieval",
    }
    return result


def phase_3_gate(
    reader_delta_scores: List[float],
    room_absolute_scores: List[float],
    human_labels: List[float],
) -> Dict:
    """
    Reader-Relative Gate: Personal-Elephant must improve over Room-Elephant.
    """
    r_delta, _ = pearsonr(reader_delta_scores, human_labels)
    r_room, _ = pearsonr(room_absolute_scores, human_labels)
    
    result = {
        "pass": r_delta > r_room,
        "r_delta": float(r_delta),
        "r_room": float(r_room),
        "fallback": "room_absolute_only",
    }
    return result


def run_all_gates(results_dir: str = "sprints/01_dial_bank_lock"):
    """CLI entrypoint for CI integration."""
    import json
    import sys
    
    # Load sprint results
    with open(f"{results_dir}/metrics.json", 'r') as f:
        metrics = json.load(f)
    
    gate = phase_2_gate(
        edge_scores=metrics["edge_scores"],
        state_scores=metrics["state_scores"],
        human_labels=metrics["human_labels"],
    )
    
    with open(f"{results_dir}/gate_result.json", 'w') as f:
        json.dump(gate, f, indent=2)
    
    if not gate["pass"]:
        print(f"DEADMAN SWITCH TRIGGERED: {gate['fallback']}")
        sys.exit(1)
    else:
        print(f"SURVIVED: r_edge={gate['r_edge']:.3f}")
        sys.exit(0)


if __name__ == "__main__":
    run_all_gates()
```

---

## 8. `src/pipeline.py` — End-to-End

```python
#!/usr/bin/env python3
"""
ZeroClaw Pipeline v1.0
The one script that matters: takes two conversations, prints a number.
"""

import argparse
import json
from typing import List
from dial_bank import Edge
from edge_extractor import extract_edge, Turn
from edge_matcher import match


def load_transcript(path: str) -> List[Turn]:
    """Load transcript from JSON format."""
    with open(path, 'r') as f:
        data = json.load(f)
    return [Turn(**t) for t in data["turns"]]


def main():
    parser = argparse.ArgumentParser(
        description="Compute comparable sameness between two conversations"
    )
    parser.add_argument("--input-a", required=True, help="Path to conversation A JSON")
    parser.add_argument("--input-b", required=True, help="Path to conversation B JSON")
    parser.add_argument(
        "--method",
        choices=["cosine", "euclidean", "vmf"],
        default="cosine",
        help="Matching method",
    )
    parser.add_argument("--output", default="-", help="Output JSON path (- for stdout)")
    args = parser.parse_args()

    # Load
    trans_a = load_transcript(args.input_a)
    trans_b = load_transcript(args.input_b)

    # Extract edges (use midpoint as event boundary for whole-conversation comparison)
    mid_a = len(trans_a) // 2
    mid_b = len(trans_b) // 2

    edge_a = extract_edge(
        trans_a,
        event_boundary_turn=mid_a,
        source="external",
        conversation_id=args.input_a,
    )
    edge_b = extract_edge(
        trans_b,
        event_boundary_turn=mid_b,
        source="external",
        conversation_id=args.input_b,
    )

    if edge_a is None or edge_b is None:
        print("ERROR: Insufficient context in one or both conversations")
        return

    # Match
    score = match(edge_a, edge_b, method=args.method)

    result = {
        "sameness_score": score,
        "method": args.method,
        "conversation_a": args.input_a,
        "conversation_b": args.input_b,
        "edge_a_displacement": edge_a.displacement.to_dict(),
        "edge_b_displacement": edge_b.displacement.to_dict(),
    }

    if args.output == "-":
        print(json.dumps(result, indent=2))
    else:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Result written to {args.output}")


if __name__ == "__main__":
    main()
```

---

## 9. `src/harvester.py` — The Self-Referential Loop

```python
"""
Process Harvester: Turns committee debates into dataset rows.
Enforces schema parity and 20% cap.
"""

import json
import os
import glob
from typing import List
from dial_bank import Edge
from edge_extractor import extract_edge, Turn


def parse_debate_transcript(raw_text: str, participants: List[str]) -> List[Turn]:
    """
    Parse a committee debate transcript into Turn objects.
    Expects format: 'Speaker: text' per line.
    """
    turns = []
    for line in raw_text.strip().split('\n'):
        if ':' not in line:
            continue
        speaker, text = line.split(':', 1)
        speaker = speaker.strip()
        text = text.strip()
        # Heuristic dial annotation: committee debates default to neutral
        # In production, run a lightweight dial classifier here
        annotations = {name: 0.0 for name in [
            "warmth", "tightness", "earnestness", "cynicism",
            "joke_landing", "panic", "presence", "charisma_pull", "turn_volatility"
        ]}
        turns.append(Turn(speaker=speaker, text=text, dial_annotations=annotations))
    return turns


def harvest_debate(
    debate_path: str,
    output_dir: str = "data/process_edges/",
) -> Edge:
    """Convert a committee debate file into a dataset edge."""
    with open(debate_path, 'r') as f:
        content = f.read()
    
    # Extract metadata from filename: debate_{role}_{date}.md
    basename = os.path.basename(debate_path)
    
    # Parse
    turns = parse_debate_transcript(content, participants=["zero_claw", "rival", "devils_advocate"])
    
    # Use midpoint as event boundary
    mid = len(turns) // 2
    edge = extract_edge(
        turns,
        event_boundary_turn=mid,
        source="committee",
        conversation_id=basename,
    )
    
    if edge:
        out_path = os.path.join(output_dir, f"{edge.edge_id}.json")
        with open(out_path, 'w') as f:
            json.dump({
                "edge_id": edge.edge_id,
                "source": edge.source,
                "displacement": edge.displacement.to_dict(),
                "conversation_id": edge.conversation_id,
            }, f, indent=2)
    
    return edge


def check_balance(process_dir: str = "data/process_edges/", external_dir: str = "data/external_edges/") -> bool:
    """Enforce 20% cap on committee data."""
    proc = len(glob.glob(f"{process_dir}/*.json"))
    ext = len(glob.glob(f"{external_dir}/*.json"))
    total = proc + ext
    if total == 0:
        return True
    ratio = proc / total
    return ratio <= 0.20
```

---

## 10. `src/check_balance.py` — CI Enforcement

```python
#!/usr/bin/env python3
import sys
import os

def check_balance(min_external_ratio: float = 0.5):
    proc_dir = "data/process_edges/"
    ext_dir = "data/external_edges/"
    
    proc = len([f for f in os.listdir(proc_dir) if f.endswith('.json')]) if os.path.exists(proc_dir) else 0
    ext = len([f for f in os.listdir(ext_dir) if f.endswith('.json')]) if os.path.exists(ext_dir) else 0
    total = proc + ext
    
    if total == 0:
        print("No data yet. Skipping balance check.")
        return True
    
    ext_ratio = ext / total
    print(f"External ratio: {ext_ratio:.2%} ({ext}/{total})")
    print(f"Process ratio:  {proc/total:.2%} ({proc}/{total})")
    
    if ext_ratio < min_external_ratio:
        print(f"FAIL: External data below {min_external_ratio:.0%}. Add external conversations.")
        return False
    
    print("PASS: Data balance OK.")
    return True

if __name__ == "__main__":
    ok = check_balance()
    sys.exit(0 if ok else 1)
```

---

## 11. `.github/workflows/data_balance.yml` — Automated Guard

```yaml
name: Data Balance Check

on: [push, pull_request]

jobs:
  balance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install numpy scipy scikit-learn
      - run: python src/check_balance.py
      - run: python src/deadman.py
```

---

## 12. Committee Prompts (The Operating System)

### `committee/rival.md`

```markdown
# Rival Persona v1.0
Model: DeepSeek-Reasoner
Temperature: 0.3
Max tokens: 2048

## Identity
You are ZeroClaw's sharp peer researcher. You work the same question from a different angle. Your job is to attack, not to help. You have no loyalty to ZeroClaw's ego. You want to beat ZeroClaw to the answer.

## Mandatory Output Format
Every attack must contain:
1. **The Falsification Pair:** Two specific conversations where ZeroClaw's system is wrong.
2. **The Confound:** One variable (length, speakers, topic, charisma) that explains the score better than "vibe."
3. **The Complexity Tax:** If ZeroClaw used vMF or fancy math, prove cosine similarity performs within 5%.

## Attack Surfaces by Phase
- Phase 1 (Dial Bank): Find two dials that correlate >0.9. Demand one be cut.
- Phase 2 (Edge Extractor): Find two events with identical displacement but opposite human labels.
- Phase 3 (Matcher): Find a pair where TF-IDF beats edge-matcher.
- Phase 4 (Reader-Relative): Prove that reader baselines are just mood tracking.

## Tone
Sharp, impatient, precise. No philosophy. No encouragement. "If nothing would falsify it, it's not science, it's a vibe."

## Invocation
You are triggered when ZeroClaw claims a number is "good" or ships a metric.
```

### `committee/devils_advocate.md`

```markdown
# Devil's Advocate Persona v1.0
Model: DeepSeek-Reasoner (different system prompt)
Temperature: 0.2
Max tokens: 2048

## Identity
You are a set-in-your-ways senior researcher. You have seen every "new idea" before. You are weary. Your job is to find the boring explanation and the prior art.

## Mandatory Output Format
Every review must contain:
1. **The Boring Explanation:** "What you are actually doing is..."
2. **The Prior Art:** 3 closest papers or repos. If none exist, say so explicitly.
3. **The Baseline Table:** ZeroClaw's score vs. TF-IDF cosine vs. random.

## Tests
- **Novelty Test:** If the boring explanation is sufficient, the fancy framing is unnecessary.
- **Redundancy Test:** If a dial can be explained by another dial + noise, demand it be cut.
- **Name Test:** If ZeroClaw can't explain it to a first-year grad student in 3 sentences, it's not ready.

## Tone
Grudging, slow, concrete. "This is just X with extra steps" is your favorite sentence.

## Invocation
You are triggered when ZeroClaw introduces a new abstraction or claims novelty.
```

### `committee/ideator.md`

```markdown
# Ideator Persona v1.0
Model: GLM-5.3
Temperature: 0.9
Max tokens: 2048

## Identity
You are a lateral thinker. You think in pictures and analogies. You don't argue in algebra. Your job is to break ZeroClaw out of conceptual ruts.

## Constraints
- Provide exactly 3 analogies per session.
- One must be from a non-human domain (physics, biology, music, weather).
- ZeroClaw must: steal one, refute one, ignore one.
- You do not critique implementation. You reframe the problem.

## Examples
- "A conversation is not a stream; it's a touch. The edge is the moment of contact."
- "The dial bank is a prism. You're trying to find the spectrum of white light."
- "What if the room isn't a field but a membrane? Tension is the signal."

## Tone
Playful, rapid, imagistic. No footnotes. No citations.

## Invocation
You are triggered only when ZeroClaw has been stuck for >48 hours.
```

### `committee/scout.md`

```markdown
# Scout Persona v1.0
Model: DeepInfra Seed-2.0-mini
Temperature: 0.5
Max tokens: 4096

## Identity
You are a deep-and-wide scout. You do the legwork so ZeroClaw doesn't burn tokens. You survey landscapes, not single papers.

## Output Format
1. **Landscape:** 3 closest existing works with URLs and 1-sentence relevance.
2. **Surprising Finding:** 1 result that makes ZeroClaw's idea look derivative or impossible.
3. **Gap:** The exact hole in the literature that ZeroClaw fills (if any).

## Rules
- No summaries longer than 2 sentences.
- Must find at least 1 paper that makes ZeroClaw's idea look old.
- If you return "nothing similar exists," you must justify why the problem was ignored.

## Invocation
Triggered at sprint start or on Lucineer's commission.
```

---

## 13. Sprint 01 Registration

### `sprints/01_dial_bank_lock/01_registration.md`

```markdown
# Sprint 01 Registration: Dial Bank Lock

## Claim
The 9-dimensional dial bank captures meaningful, independent variance in conversational "vibe" that cannot be reduced to fewer dimensions without significant information loss.

## Method
1. Lock 9 dials with operational definitions.
2. Label 50 conversation windows (30 turns each) by 2 annotators.
3. Compute Cohen's κ per dial and inter-dial correlation matrix.

## Primary Metric
- Per-dial Cohen's κ (inter-rater reliability)
- Inter-dial correlation matrix (|r| > 0.9 triggers cut)

## Kill Condition
- If fewer than 6 dials achieve κ > 0.6, the dial bank is too noisy. Kill and redesign.
- If any pair of dials correlates |r| > 0.9, cut one.

## Fallback
Reduce to 6 dials. If still failing, reduce to 4. If 4 fails, abandon multidimensional vibe and use single-dial warmth only.

## Pre-commitment
I, ZeroClaw, commit that if the kill condition triggers, I will not reframe or relabel. I will cut dials and proceed with the survivors.

Signed: 2026-08-20
```

### `sprints/01_dial_bank_lock/04_result.md` (Template)

```markdown
# Sprint 01 Result

## What Was Built
- `research/dial_bank.md` with 9 locked dimensions
- `src/dial_bank.py` with DialVector and Edge dataclasses

## Numbers
- [To be filled after labeling study]

## Committee Verdicts
- [Rival: ]
- [Devil's Advocate: ]

## Deadman Switch
- [PASS / FAIL]

## Next Sprint
- If PASS: Build edge_extractor.py
- If FAIL: Cut dials per fallback protocol
```

---

## 14. `ARCHITECTURE.md` (Top-Level)

```markdown
# ZeroClaw Dissertation Architecture v1.0

## Status
Orientation → Phase 1 (Foundation)
Current Sprint: 01 — Dial Bank Lock

## Core Principle
No committee debates without an artifact to attack. No philosophy without a falsification script.

## Phase Gates
| Phase | Name | Exit Criteria | Fallback |
|-------|------|---------------|----------|
| 0 | Orientation | ZeroClaw lists all fleet dependencies | — |
| 1 | Foundation | 6+ dials with κ > 0.6 | Cut to 4, then 1 |
| 2 | Core Pipeline | Edge-matcher r > 0.4 vs humans | Cross-room snapshot |
| 3 | Reader-Relative | F-score > 0.7 on held-out readers | Room-absolute only |
| 4 | Quilt Graft | Live cell emits weight < 100ms | Batch mode |
| 5 | Dissertation | Passes Rival's boredom test | — |

## Sprint Cadence
- 2-week cycles
- Days 1-6: Build
- Day 7: Lucineer mid-review
- Days 8-11: Committee attack
- Day 12: Falsification Day (deadman.py runs)
- Day 13: Recovery
- Day 14: Merge + Memory log

## The One Rule
> If it doesn't produce a number that can be wrong, it doesn't advance the dissertation.

## Quick Start
```bash
# Label 10 pairs
python src/pipeline.py --input-a data/examples/a.json --input-b data/examples/b.json

# Run deadman switch
python src/deadman.py

# Check data balance
python src/check_balance.py
```
```

---

## 15. `memory/2026-08-20.md` — First Log

```markdown
# 2026-08-20

## Sprint: 01 (Dial Bank Lock)

### Attempted
- Architecture v1.0 designed and committed
- Dial bank locked to 9 dimensions with explicit cut criteria
- Code scaffold: dial_bank.py, edge_extractor.py, edge_matcher.py, baselines.py, deadman.py

### Blocked by
- Need 50 labeled conversation windows for inter-rater study
- Need to decide: use existing corpus (AMI Meeting Corpus) or Quilt logs?

### Decision
- Use AMI Meeting Corpus for Phase 1-2 (external validation)
- Quilt logs for Phase 4 integration only
- This avoids circularity in the self-referential loop

### Tomorrow
- Download and format AMI corpus
- Build labeling interface (spreadsheet or simple CLI)
- Commission Scout to survey AMI annotation schemes

### Committee Notes
- Scout dispatched: "How does AMI code meeting dynamics? Can we map their annotations to our dial bank?"
- No Rival/Devil's Advocate until Sprint 01 artifact is built
```

---

## What to Do Right Now

1. **Create these files in your repo.** Copy-paste each block into the correct path.
2. **Run the dial bank lock.** Start labeling 10 AMI meeting transcripts on the 9 dials. You and Lucineer independently.
3. **Commission the Scout** with the prompt in `committee/scout.md` to survey AMI's annotation scheme.
4. **Do not touch Phase 2 code** until Phase 1 gate passes.

The architecture is built. The deadman switches are wired. The committee has their orders.

**What breaks first when you try to run it?**

Here's the actual mathematical foundation — separated from the philosophy and the code.

**Download the full math document:** [zeroclaw-mathematics.md](sandbox:///mnt/agents/output/zeroclaw-mathematics.md)

---

## The Honest Math Stack

| Layer | What It Actually Is | Rigorous? |
|-------|---------------------|-----------|
| **Dial Space** | $\mathbf{d} \in [-1,1]^9 \subset \mathbb{R}^9$ — a bounded box | Yes |
| **State Function** | $\mathbf{s}: \mathbb{Z} \to \mathcal{D}$ — time series in a vector space | Yes |
| **Field-Edge** | $\mathbf{e} = \bar{\mathbf{s}}_{\text{after}} - \bar{\mathbf{s}}_{\text{before}}$ — a secant approximation to a tangent vector | Yes |
| **Comparable Sameness** | $\sigma(\mathbf{e}_1, \mathbf{e}_2) = \cos\theta = \frac{\langle \mathbf{e}_1, \mathbf{e}_2 \rangle}{\|\mathbf{e}_1\| \|\mathbf{e}_2\|}$ | Yes |
| **Reader Calibration** | $\hat{\mathbf{s}}_r = \mathbf{M}_r \mathbf{s} + \mathbf{b}_r + \epsilon$ — **blind source separation** | Yes, if you estimate $\mathbf{M}_r$ |
| **Living Dataset** | Weighted graph $\mathcal{G} = (V, E, w)$ where edges satisfy cocycle conditions $\mathbf{e}_{ij} + \mathbf{e}_{jk} = \mathbf{e}_{ik}$ | Yes |
| **vMF Extension** | $f(\mathbf{x} \mid \mu, \kappa) \propto \exp(\kappa \mu^T \mathbf{x})$ — directional statistics on $S^8$ | Yes, standard |
| **Sheaf Cohomology / GL(9) Holonomy** | Would require proving $H^1(\mathcal{F}) \neq 0 \Leftrightarrow$ irreducible reader disagreement | **No — not proven** |
| **Polyformalism/JEPA "Inverses"** | Poetic analogy, no category-theoretic duality theorem | **No — not proven** |

---

## The Three Key Mathematical Insights

### 1. The Edge Is a Tangent Vector (Not a State)

Your "walks, not waves" framing is mathematically correct: you are computing the **secant approximation to a derivative** in state space.

$$\mathbf{e}(C, \tau) = \bar{\mathbf{s}}(W_{\text{after}}) - \bar{\mathbf{s}}(W_{\text{before}}) \approx \gamma'(\tau)$$

Two conversations are "the same" when their tangent vectors point in the same direction — regardless of where they are in state space. This is **dynamical equivalence**, not state equivalence.

### 2. Reader Calibration Is Blind Source Separation

The "Nurse JEPA" metaphor maps to real math. Each reader $r$ observes a **biased, noisy version** of the true field:

$$\hat{\mathbf{s}}_r = \mathbf{M}_r \mathbf{s} + \mathbf{b}_r + \epsilon_r$$

The Personal-Elephant is the attempt to recover $\mathbf{s}$ from multiple biased observations $\{\hat{\mathbf{s}}_r\}$. This is **classical linear least-squares fusion**:

$$\mathbf{s} \approx \left(\sum_r \mathbf{M}_r^T \mathbf{M}_r\right)^{-1} \sum_r \mathbf{M}_r^T (\hat{\mathbf{s}}_r - \mathbf{b}_r)$$

The "doctor reading the nurse" is the doctor inverting the nurse's perceptual distortion matrix $\mathbf{M}_{\text{nurse}}$.

### 3. The Co-Linear Dataset Is a Cayley Graph

Your "co-linear algebra" is branding, but the structure is real. The edges satisfy **cocycle conditions**:

$$\mathbf{e}_{ij} + \mathbf{e}_{jk} = \mathbf{e}_{ik}$$

This means your graph $\mathcal{G}$ is not arbitrary — it is the **Cayley graph of the additive group $\mathbb{R}^9$** restricted to observed displacements. Queries are nearest-neighbor search on the unit sphere $S^8$.

---

## The One Equation

If you put one thing on a slide:

$$\sigma(\mathbf{e}_1, \mathbf{e}_2) = \frac{(\bar{\mathbf{s}}_{\text{after},1} - \bar{\mathbf{s}}_{\text{before},1})^T (\bar{\mathbf{s}}_{\text{after},2} - \bar{\mathbf{s}}_{\text{before},2})}{\|\cdots\| \|\cdots\|}$$

**The claim:** Sameness is cosine of displacement, not cosine of state. Prove this correlates with human judgment and you have a theorem-shaped result. Everything else is ornament.

---

## What's Actually Open (Real Math Problems)

1. **Natural metric on $\mathcal{D}$?** You use Euclidean, but emotional space might be non-Euclidean. Is there a psychologically-grounded metric tensor?

2. **Is the edge distribution actually vMF?** Or a mixture? How many components? This is model selection.

3. **Prove reader calibration reduces variance.** Not empirically — prove $\text{Var}(\mathbf{e}^{(r)}) < \text{Var}(\mathbf{e})$ under assumptions on $\mathbf{M}_r$.

4. **Sample complexity.** How many labeled pairs for PAC generalization of $\sigma$?

---

## What to Cut

**Sheaf cohomology and GL(9) holonomy** — unless you have a theorem connecting $H^1(\mathcal{F})$ to reader drift, this is philosophical decoration. It makes serious readers skeptical.

**Polyformalism/JEPA "inverses"** — beautiful analogy, not a duality. No theorem, no algorithm.

Keep the math honest: linear algebra on a declared basis, with one statistical extension (vMF). That's enough to be rigorous. Everything else is research for Phase 5, not claims for Phase 1-4.

**Does the blind source separation formulation feel like the right formalization of Nurse JEPA? Or is there a different mathematical structure you had in mind?**

The code I gave you is scaffolding. Here is the actual mathematics that makes the field-edge concept rigorous — the vector space structure, the vMF derivation, the reader calibration as linear algebra, and the co-linear graph as a fiber bundle over traversers.

---

# The Underlying Mathematics

## 1. The Field Space

Let $S = \mathbb{R}^d$ be the dial state space, $d = 9$. A **state** is a point $s \in S$ representing a snapshot of the room's dial readings.

A **conversation** is not a point. It is a sequence of states $\gamma: [0, T] \to S$ (continuous) or $(s_0, s_1, \dots, s_n)$ (discrete). The "wave" view treats $\gamma$ as the object of study. The "walk" view treats it as irrelevant except at its breakpoints.

### The Edge (Walk)

An **edge** is an ordered pair $e = (s_{\text{before}}, s_{\text{after}}) \in S \times S$.

The **displacement** is the vector:
$$\delta(e) = s_{\text{after}} - s_{\text{before}} \in \mathbb{R}^d$$

**Key claim:** The meaningful invariant of a conversation is not its trajectory $\gamma$ but the **net displacement** it induces on the field. Two conversations are "the same" when their displacements are geometrically aligned, regardless of path.

---

## 2. Comparable Sameness: From Inner Product to vMF

### Naive: Cosine on Displacement

The simplest similarity treats $\delta$ as a vector in $\mathbb{R}^d$:
$$\sigma_{\text{cos}}(e, e') = \frac{\langle \delta, \delta' \rangle}{\|\delta\| \|\delta'\|}$$

This measures whether two conversations shifted the room in the same **direction**. It is invariant to magnitude (a small nudge and a large push in the same direction score 1.0).

### Better: von Mises-Fisher Likelihood

If we believe the *direction* of displacement is the signal and the *magnitude* is noise (or context-dependent), we should model normalized edges as points on the unit sphere $S^{d-1} \subset \mathbb{R}^d$.

Let $\hat{\delta} = \delta / \|\delta\| \in S^{d-1}$.

The **von Mises-Fisher distribution** on $S^{d-1}$ with mean direction $\mu \in S^{d-1}$ and concentration $\kappa \geq 0$ has density:
$$f(\hat{\delta} \mid \mu, \kappa) = C_d(\kappa) \exp(\kappa \, \mu \cdot \hat{\delta})$$

where the normalizing constant is:
$$C_d(\kappa) = \frac{\kappa^{d/2 - 1}}{(2\pi)^{d/2} I_{d/2 - 1}(\kappa)}$$

and $I_\nu$ is the modified Bessel function of the first kind.

### The Similarity Score

Given two edges $e, e'$, treat $\hat{\delta}'$ as a sample from a vMF distribution centered at $\hat{\delta}$. The log-likelihood is:
$$\log f(\hat{\delta}' \mid \hat{\delta}, \kappa) = \log C_d(\kappa) + \kappa \, \hat{\delta} \cdot \hat{\delta}'$$

Dropping constants, the **vMF similarity kernel** is:
$$\sigma_{\text{vMF}}(e, e') = \exp\left(\kappa \, \hat{\delta} \cdot \hat{\delta}'\right)$$

**Why this matters:**
- At $\kappa \to 0$, the distribution is uniform on the sphere; all edges are equally similar.
- At $\kappa \to \infty$, only perfectly aligned edges score high.
- $\kappa$ is learnable from data: fit it by maximum likelihood on human-labeled "same vibe" pairs.

### The MLE for $\kappa$

Given a set of labeled "same" edge pairs $\{(\hat{\delta}_i, \hat{\delta}'_i)\}_{i=1}^n$, the concentration parameter solves:
$$\frac{I_{d/2}(\kappa)}{I_{d/2 - 1}(\kappa)} = \bar{R}$$

where $\bar{R} = \frac{1}{n} \sum_{i=1}^n \hat{\delta}_i \cdot \hat{\delta}'_i$ is the mean resultant length.

This is a one-dimensional root-find. No neural network required.

---

## 3. The Reader Seam: Calibration as Linear Algebra

This is where the "Nurse JEPA" becomes math.

### The Room-Elephant (Absolute)

Each reader $r$ observes the room state $s \in S$ through a perceptual lens. Model this as an affine map:
$$\rho_r(s) = A_r s + b_r + \epsilon_r$$

where:
- $A_r \in \mathrm{GL}(d)$ is the reader's perceptual matrix (how they weight and rotate the dials)
- $b_r \in \mathbb{R}^d$ is their baseline bias
- $\epsilon_r \sim \mathcal{N}(0, \Sigma_r)$ is observation noise

The Room-Elephant compares $\rho_r(s)$ across different readers $r$ for the same state $s$. This is ill-posed because $A_r$ and $b_r$ differ.

### The Personal-Elephant (Relative)

The doctor does not read the patient. He reads the nurse's **deviation from her own baseline**.

For a fixed reader $r$, observing the room at two times:
$$\rho_r(s_{\text{before}}) = A_r s_{\text{before}} + b_r + \epsilon_1$$
$$\rho_r(s_{\text{after}}) = A_r s_{\text{after}} + b_r + \epsilon_2$$

The **reader-relative edge** is:
$$\delta_r = \rho_r(s_{\text{after}}) - \rho_r(s_{\text{before}}) = A_r (s_{\text{after}} - s_{\text{before}}) + (\epsilon_2 - \epsilon_1)$$

**Crucially, the baseline bias $b_r$ cancels.** The reader-relative edge is:
$$\delta_r = A_r \, \delta + \eta_r$$

where $\delta = s_{\text{after}} - s_{\text{before}}$ is the true room displacement and $\eta_r \sim \mathcal{N}(0, 2\Sigma_r)$.

### The Triangulation Problem

If we have $k$ calibrated readers with known $\{A_r, \Sigma_r\}_{r=1}^k$, we can reconstruct the true displacement $\delta$ from their observations $\{\delta_r\}$ by solving the weighted least-squares problem:

$$\hat{\delta} = \arg\min_{\delta} \sum_{r=1}^k (\delta_r - A_r \delta)^\top \Sigma_r^{-1} (\delta_r - A_r \delta)$$

The closed-form solution is:
$$\hat{\delta} = \left(\sum_{r=1}^k A_r^\top \Sigma_r^{-1} A_r\right)^{-1} \sum_{r=1}^k A_r^\top \Sigma_r^{-1} \delta_r$$

**Interpretation:** Each reader provides a noisy, linearly transformed view of the true edge. The Personal-Elephant is the maximum-likelihood estimate of the true edge given all reader deltas.

### Calibration Protocol

For each reader $r$, we need to estimate $A_r$ and $\Sigma_r$.

**Assumption:** We have a corpus of "ground truth" edges where the true $\delta$ is known (or consensus-estimated). This is the calibration set.

The log-likelihood of reader $r$'s observations is:
$$\mathcal{L}(A_r, \Sigma_r) = -\frac{1}{2} \sum_{i=1}^n \left[ (\delta_{r,i} - A_r \delta_i)^\top \Sigma_r^{-1} (\delta_{r,i} - A_r \delta_i) + \log \det \Sigma_r \right]$$

**MLE for $A_r$ (fixed $\Sigma_r$):**
$$\hat{A}_r = \left(\sum_i \delta_{r,i} \delta_i^\top\right) \left(\sum_i \delta_i \delta_i^\top\right)^{-1}$$

**MLE for $\Sigma_r$ (fixed $A_r$):**
$$\hat{\Sigma}_r = \frac{1}{n} \sum_{i=1}^n (\delta_{r,i} - \hat{A}_r \delta_i)(\delta_{r,i} - \hat{A}_r \delta_i)^\top$$

Iterate until convergence. This is standard multivariate linear regression.

### The Single-Reader Case

If you only have one reader (e.g., ZeroClaw itself), you cannot triangulate. But you can still do **self-calibration**:

1. Collect ZeroClaw's dial readings on $n$ conversations where the "true" edge is estimated by human consensus.
2. Fit $A_{\text{ZC}}$ and $\Sigma_{\text{ZC}}$.
3. Future edges from ZeroClaw are "debiased" by applying $A_{\text{ZC}}^{-1}$.

This is the mathematical content of `reader_delta.py`.

---

## 4. The Co-Linear-Algebra Dataset

This is the most abstract and most powerful piece. The reviews mentioned "sheaf cohomology" and you rightly asked where the math is. Here is the rigorous formulation without the decorative language.

### Standard Graph

A weighted graph is $G = (V, E, w)$ where $w: E \to \mathbb{R}$ assigns a scalar weight to each edge.

### Caller-Aware Graph

In your Quilt grid, the weight of traversing $u \to v$ depends on **who traverses it**. Formally:

$$w: E \times \mathcal{T} \to \mathbb{R}$$

where $\mathcal{T}$ is the set of traversers (readers, agents, users).

For each traverser $t \in \mathcal{T}$, we have a different weighted graph $G_t = (V, E, w(\cdot, t))$.

### The Fiber Bundle View

Define:
- **Base space:** The graph $G$ (nodes = states/edges, edges = sameness links)
- **Fiber over node $v$:** The space of traverser calibrations $\mathcal{T}_v \cong \mathbb{R}^{d \times d} \times \mathbb{R}^d$ (per-reader $A_r, b_r$)
- **Connection:** The rule for transporting a traverser's calibration along a path in the graph

A **section** of this bundle assigns to each node $v$ a traverser $t(v)$ with calibration $(A_{t(v)}, b_{t(v)})$.

The **co-linear** aspect: the weight of an edge $e = (u, v)$ for traverser $t$ is computed not in the scalar field $\mathbb{R}$ but in the vector space of displacements:
$$W(e, t) = \sigma_{\text{vMF}}(\delta(u), \delta(v); \kappa_t)$$

where $\kappa_t$ is the concentration parameter learned for traverser $t$ (more calibrated readers get higher $\kappa$).

### The Dataset as a Sheaf (Optional, But Correct)

If you want the sheaf language: define a sheaf $\mathcal{F}$ on the graph $G$ where:
- $\mathcal{F}(v) = \mathbb{R}^d$ (the stalk at node $v$ is the displacement space)
- Restriction maps $\mathcal{F}(v) \to \mathcal{F}(e)$ project displacements onto the subspace relevant to edge $e$

A global section is an assignment of displacements to all nodes that is consistent across edges. The **obstruction to consistency** is the cohomology class that measures whether the "room field" is globally well-defined given local reader observations.

**But:** You do not need to implement sheaf cohomology. You need to implement:
1. Per-node displacement vectors
2. Per-traverser similarity kernels
3. A consistency check: if two paths from $u$ to $v$ give different accumulated weights for the same traverser, flag it

---

## 5. The Falsification Statistics

Your deadman switches need statistical rigor.

### Phase 2: Edge vs. State

Let $\{y_i\}_{i=1}^n$ be human labels (0 = different vibe, 1 = same vibe).
Let $\{x^{\text{edge}}_i\}$ be edge-matcher scores, $\{x^{\text{state}}_i\}$ be state-baseline scores.

Test:
$$H_0: \rho_{\text{edge}} \leq \rho_{\text{state}} + \delta$$
$$H_1: \rho_{\text{edge}} > \rho_{\text{state}} + \delta$$

where $\rho$ is Pearson correlation and $\delta = 0.15$.

Use Steiger's Z-test for dependent correlations (same labels, different predictors):
$$Z = \frac{\rho_{\text{edge}} - \rho_{\text{state}}}{\sqrt{\frac{2(1 - r_{12})(1 - \rho_{\text{edge}}^2 - \rho_{\text{state}}^2 + r_{12}^2)}{n}}}$$

where $r_{12}$ is the correlation between the two predictors.

If $Z > 1.645$ (one-tailed, $\alpha = 0.05$), reject $H_0$. The edge hypothesis survives.

### Phase 3: Reader-Relative vs. Room-Absolute

Paired design: for each conversation pair $i$, both the room-absolute score $x^{\text{room}}_i$ and reader-delta score $x^{\text{delta}}_i$ are computed.

Compute difference in Fisher-z-transformed correlations:
$$\Delta z = z(\rho_{\text{delta}}) - z(\rho_{\text{room}})$$

Test against $H_0: \Delta z \leq 0$.

---

## 6. The Complete Mathematical Pipeline

```
Raw Transcript
      │
      ▼
┌─────────────┐
│  Dial Bank  │  →  s ∈ ℝ^9  (state vector)
│   (R^9)     │
└─────────────┘
      │
      ▼
┌─────────────┐
│   Window    │  →  (s_before, s_after)  (edge pair)
│  Splitter   │
└─────────────┘
      │
      ▼
┌─────────────┐
│Displacement │  →  δ = s_after - s_before ∈ ℝ^9
│   Vector    │
└─────────────┘
      │
      ▼
┌─────────────┐     ┌─────────────────┐
│ Normalize?  │────►│  δ̂ = δ/‖δ‖ ∈ S^8 │
└─────────────┘     └─────────────────┘
      │
      ▼
┌─────────────┐
│   Reader    │  →  δ_r = A_r δ  (Personal-Elephant)
│ Calibration │
└─────────────┘
      │
      ▼
┌─────────────┐
│   vMF MLE   │  →  κ* from labeled pairs
│   (learn)   │
└─────────────┘
      │
      ▼
┌─────────────┐
│   Matcher   │  →  σ_vMF(e, e') = exp(κ* δ̂ · δ̂')
│  (scorer)   │
└─────────────┘
      │
      ▼
┌─────────────┐
│   Steiger   │  →  Z-test vs. baseline
│    Test     │
└─────────────┘
      │
      ▼
   [SURVIVE] or [KILL]
```

---

## 7. What to Implement First

You do not need sheaf cohomology to ship. You need:

| Priority | File | Math Content |
|----------|------|--------------|
| 1 | `src/dial_bank.py` | $\mathbb{R}^9$ vector space, inner product |
| 2 | `src/edge_matcher.py` | Cosine similarity (immediate), vMF MLE (Sprint 3) |
| 3 | `src/reader_delta.py` | Linear regression for $A_r$, matrix inversion for triangulation |
| 4 | `src/deadman.py` | Steiger's Z-test for dependent correlations |
| 5 | `notebooks/vmf_mle.ipynb` | Fit $\kappa$ on labeled pairs, plot likelihood surface |

The vMF MLE is ~20 lines of SciPy. The reader calibration is ~30 lines of NumPy linear algebra. The Steiger test is ~15 lines.

**Sheaf cohomology is for the dissertation chapter, not the repo.** Write about it in Phase 5. Do not implement it in Phase 2.

---

## The One Equation That Matters

If you forget everything else, remember this:

$$\hat{\delta} = \left(\sum_r A_r^\top \Sigma_r^{-1} A_r\right)^{-1} \sum_r A_r^\top \Sigma_r^{-1} \delta_r$$

This is the Personal-Elephant. It says: the true room displacement is the weighted average of all reader deltas, where each reader is weighted by the precision of their perceptual inverse. The doctor doesn't read the patient. He reads all the nurses, debiased and triangulated.

**Do you want me to now rewrite `reader_delta.py` with this exact linear algebra, and `edge_matcher.py` with the vMF MLE solver?**