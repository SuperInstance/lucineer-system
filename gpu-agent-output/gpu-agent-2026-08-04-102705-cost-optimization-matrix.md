# GPU Agent Output — Cost Optimization Matrix
**Timestamp:** 2026-08-04 10:27:05 AKDT
**Model:** granite3.1-dense:2b on RTX 4050
**Topic:** Cost Optimization — Local vs Cloud Task Routing

## Analysis
The GPU attempted a cost-routing matrix but confused artifact names with model names (e.g., "VesselFishingBridge" as an embeddings model). The raw output is hallucinated in places but the structure is useful. Here's the corrected version:

## Corrected Cost-Optimization Matrix

| Task Type | Target | Model | Est. Cost/Call | Quality (1-5) | Speed (1-5) |
|-----------|--------|-------|----------------|---------------|-------------|
| Code Review (Lua/TS) | LOCAL (GPU) | Granite 3.1 2B | $0.00 | 3 | 3 |
| Creative Writing | CLOUD | GLM-5.2 (Z.ai Max) | $0.00 (unlimited) | 5 | 4 |
| Bug Detection | CLOUD | GLM-5.2 or DeepSeek V3 | $0.001-0.01 | 4 | 4 |
| Architecture Design | CLOUD | Claude Opus 5 (Pro) | $0.00 (plan) | 5 | 3 |
| Embeddings/Vectorization | LOCAL (GPU) | nomic-embed-text | $0.00 | 4 | 5 |
| Text Classification | LOCAL (GPU) | Qwen 0.5B | $0.00 | 3 | 5 |
| Long-form Documentation | CLOUD | GLM-5.2 (Z.ai Max) | $0.00 (unlimited) | 4 | 4 |
| Quick Q&A | LOCAL (GPU) | Qwen 0.5B | $0.00 | 3 | 5 |
| Build Command Generation | CLOUD | DeepSeek V3/Flash | $0.001-0.005 | 4 | 4 |
| Player Chat (Lucineier) | CLOUD | GLM-5.2 fast path | $0.00 (unlimited) | 4 | 4 |

## Key Insight
With Z.ai Max (unlimited GLM-5.2), most cloud tasks cost $0. The real routing decision is:
- **Real-time (player waiting):** Fast path Worker endpoint (200ms templates) or LOCAL
- **Background (overnight/agents):** GLM-5.2 unlimited cloud
- **Deep reasoning (architecture):** Claude Opus (limited, use sparingly)
- **Embeddings (always):** LOCAL nomic-embed-text (free, fast)

## Corrected Python Decision Function

```python
from enum import Enum
from dataclasses import dataclass

class Target(Enum):
    LOCAL_GPU = "local_gpu"
    CLOUD_GLM = "cloud_glm"      # Z.ai Max — unlimited
    CLOUD_CLAUDE = "cloud_claude" # Pro plan — limited
    CLOUD_DEEPSEEK = "cloud_deepseek" # Pay-per-token — cheapest
    CLOUD_DEEPINFRA = "cloud_deepinfra" # 179 models

@dataclass
class RoutingResult:
    target: Target
    model: str
    est_cost_usd: float
    est_latency_ms: int
    quality_score: int  # 1-5

def route_task(task_type: str, urgency: str, complexity: int) -> RoutingResult:
    """
    Route a task to the optimal model based on type, urgency, and complexity.
    
    Args:
        task_type: one of the 10 task categories
        urgency: 'realtime' (player waiting), 'background', 'overnight'
        complexity: 1-5, how hard the task is
    """
    # Real-time tasks: minimize latency
    if urgency == 'realtime':
        if task_type == 'player_chat':
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 200, 4)
        elif task_type == 'build_commands':
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 200, 4)
        elif task_type == 'quick_qa':
            return RoutingResult(Target.LOCAL_GPU, "Qwen-0.5B", 0.0, 500, 3)
        elif task_type == 'classification':
            return RoutingResult(Target.LOCAL_GPU, "Qwen-0.5B", 0.0, 500, 3)
    
    # Background tasks: maximize quality, cost doesn't matter (GLM unlimited)
    if urgency in ('background', 'overnight'):
        if task_type == 'architecture':
            return RoutingResult(Target.CLOUD_CLAUDE, "Opus-5", 0.0, 30000, 5)
        elif task_type == 'creative_writing':
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 10000, 5)
        elif task_type == 'code_review':
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 10000, 4)
        elif task_type == 'documentation':
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 15000, 4)
        elif task_type == 'bug_detection':
            if complexity >= 4:
                return RoutingResult(Target.CLOUD_CLAUDE, "Opus-5", 0.0, 30000, 5)
            return RoutingResult(Target.CLOUD_GLM, "GLM-5.2", 0.0, 10000, 4)
    
    # Embeddings always local
    if task_type == 'embeddings':
        return RoutingResult(Target.LOCAL_GPU, "nomic-embed-text", 0.0, 50, 4)
    
    # Default: cheapest cloud
    return RoutingResult(Target.CLOUD_DEEPSEEK, "DeepSeek-V3", 0.001, 5000, 4)
```

## Assessment
- **GPU raw output:** Confused artifact names with model names, cost estimates hallucinated
- **Corrected version:** Uses actual Z.ai Max plan economics — most tasks are $0
- **Key takeaway:** The routing decision is really about latency, not cost, since GLM-5.2 is unlimited
