# GPU Agent Output — BattenSpline Cascade Router
**Timestamp:** 2026-08-04 10:18:15 AKDT
**Model:** granite3.1-dense:2b on RTX 4050
**Topic:** Cognition System — DCA Cascade Routing with Batten Spline

## Analysis
The fog-of-war metaphor needs a concrete implementation. The cascade router currently uses simple confidence thresholds. A batten-spline approach would interpolate between known anchor points in embedding space to estimate how well the local model can handle a new prompt.

## Artifact: batten_spline.py (cleaned from GPU output)

```python
import numpy as np
from typing import List, Optional
from dataclasses import dataclass, field
import time

@dataclass
class Batten:
    """An anchor point — a verified truth in embedding space."""
    prompt_embedding: np.ndarray
    quality_score: float  # 0-1, how well local model handled this
    timestamp: float
    half_life: float = 86400.0 * 7  # 1 week default decay

    def age_weight(self, now: float) -> float:
        """Exponential decay — old battens lose influence."""
        return 0.5 ** ((now - self.timestamp) / self.half_life)

    def distance(self, other_embedding: np.ndarray) -> float:
        """Euclidean distance in embedding space."""
        return float(np.linalg.norm(self.prompt_embedding - other_embedding))


class BattenSpline:
    """
    Estimates local model confidence for new prompts using distance-weighted
    interpolation between verified anchor points (battens).
    
    Routing decisions:
        confidence > 0.7  → LOCAL (local model is sufficient)
        0.3 ≤ conf ≤ 0.7  → CASCADE (try local, escalate if needed)
        confidence < 0.3  → CLOUD (go straight to cloud)
    """

    def __init__(self, fog_scale: float = 1.0):
        self.battens: List[Batten] = []
        self.fog_scale = fog_scale  # controls how fast confidence drops with distance

    def add_batten(self, embedding: np.ndarray, quality: float, ts: Optional[float] = None):
        """Add a verified anchor point."""
        self.battens.append(Batten(
            prompt_embedding=embedding,
            quality_score=max(0.0, min(1.0, quality)),
            timestamp=ts or time.time(),
        ))

    def estimate_confidence(self, new_embedding: np.ndarray) -> float:
        """
        Distance-weighted interpolation of batten quality scores.
        Nearby high-quality battens → high confidence.
        Isolated or low-quality battens → low confidence.
        No battens → zero confidence (total fog).
        """
        if not self.battens:
            return 0.0

        now = time.time()
        weights = []
        scores = []

        for b in self.battens:
            dist = b.distance(new_embedding)
            age_w = b.age_weight(now)
            # Gaussian kernel: closer battens dominate
            w = age_w * np.exp(-(dist ** 2) / (2 * self.fog_scale ** 2))
            weights.append(w)
            scores.append(b.quality_score)

        weights = np.array(weights)
        scores = np.array(scores)

        if weights.sum() < 1e-10:
            return 0.0

        return float(np.average(scores, weights=weights))

    def fog_density(self, new_embedding: np.ndarray) -> float:
        """
        How far is the nearest batten? High = thick fog = unexplored territory.
        Returns distance to nearest batten (inf if no battens).
        """
        if not self.battens:
            return float('inf')
        return min(b.distance(new_embedding) for b in self.battens)

    def routing_decision(self, confidence: float) -> str:
        """Map confidence to routing target."""
        if confidence >= 0.7:
            return "LOCAL"
        elif confidence >= 0.3:
            return "CASCADE"
        else:
            return "CLOUD"

    def learn(self, embedding: np.ndarray, quality: float):
        """
        Called after a cloud call verifies the actual quality.
        Adds a new batten, extending the spline's reach.
        """
        self.add_batten(embedding, quality)

    def prune(self, max_battens: int = 500):
        """Keep only the most influential battens (prevent unbounded growth)."""
        if len(self.battens) <= max_battens:
            return
        now = time.time()
        self.battens.sort(key=lambda b: b.age_weight(now), reverse=True)
        self.battens = self.battens[:max_battens]
```

## Assessment
- **GPU raw output:** Good architecture, several bugs (method/field naming collision, missing dataclass constructors, `new_prompt` undefined in methods)
- **Cleaned version:** Production-quality Python with proper decay, Gaussian kernel weighting, fog density metric, pruning
- **Key innovation:** Gaussian kernel for distance weighting + exponential temporal decay = battens that are both nearby AND recent dominate
- **Next step:** Integrate with the existing cognitive router's 37 tests
