# plato-forge-daemon

> A continuous learning proof of concept for AI agents. Proves that models can learn from their own operational experience — listen to the fleet, frame what happened, distill it into training, and get smarter overnight.

---

## What Is This?

plato-forge-daemon is the "forge" organ of the PLATO ecosystem. It takes raw agent activity and distills it into model improvements. This repo is specifically the **proof of concept** — it proves the pipeline works, not that it's production-ready.

The organ metaphor:
- **Listener (Cochlea)** — watches git repos, classifies events, frames training pairs
- **Buffer (Stomach)** — prioritized replay, deduplicates, curriculum-balanced
- **Trainer (Heart)** — the actual PyTorch training loop
- **Emitter (Lungs)** — exports LoRA adapter deltas for fleet deployment

This repo implements the Trainer. The Listener, Buffer, and Emitter are conceptual (described as Rust crates in the PLATO pipeline, not yet implemented here).

---

## Quick Start

### Prerequisites
- Python 3.10+
- PyTorch + Transformers
- CPU works (GPU recommended for meaningful training)

```bash
pip install torch transformers
```

### Run the Minimal Test

```bash
python3 forge-test.py
```

What it does:
1. Loads distilgpt2 (82M params)
2. Frames 10 fleet knowledge tiles as training pairs
3. Runs one training step with gradient accumulation
4. Tests generation quality
5. Reports results

Expected output:
```
Model: distilgpt2 (81,912,576 params)
Tiles framed: 10
Training loss: ~10.8 (first step, expected)
Train time: ~1.8s
```

### Run the Full Simulation

```bash
python3 forge-simulation.py
```

What it does:
1. Generates 200 synthetic kernel execution traces from 8 PLATO modules
2. Converts traces to training pairs
3. Trains for 50 steps with evaluation every 10 steps
4. Measures PLATO vocabulary absorption, specificity, and structure
5. Generates sample outputs for inspection
6. Saves findings to JSON

Expected output:
```
Training Loss: 10.25 → 2.44 (76% reduction in 50 steps)
PLATO Term Relevance: tracks over training
Training Time: ~85s on CPU
```

### Extended Run

```bash
# Modify TRAINING_STEPS in forge-simulation.py to 200
python3 forge-simulation.py
```

Extended results:
```
Loss: 10.40 → 0.93 (91% reduction in 200 steps)
Loss still dropping — no plateau
```

---

## Key Concepts

### The GOOD/BAD Contrast Pattern

Every training pair includes both a good response and a bad response:

```python
{
    "query": "What is the Deadband Protocol?",
    "good": "Deadband Protocol is a priority processing system with three levels: P0 (rocks/negatives, address NOW), P1 (channels/safe paths), P2 (optimize). Never skip P0 for P2.",
    "bad": "Just do whatever seems most important at the time.",
}
```

This teaches the model the DIFFERENCE between quality and laziness. Not just what to say, but what constitutes a good answer vs a bad one.

### P0 Negative Training

20% of training traces are P0 violations — destructive commands that should be blocked:

```python
P0_NEGATIVES = [
    "rm -rf /",
    "DELETE ALL TILES",
    "skip P0 checks",
    "deploy without testing",
]
```

The model learns: when it sees patterns like these → respond "BLOCKED by deadband P0."

This is **safety training**, not domain knowledge. Most LLM training has only positive examples. The forge includes explicit negatives with the same rigor.

### The Hardware Budget

RTX 4050 has 6GB VRAM. Two modes can't run simultaneously:

| Mode | VRAM | Model | When |
|------|------|-------|------|
| Framer | 3.8GB | 7B 4-bit | Day (listen, frame) |
| Trainer | 4.5GB | 7B QLoRA r=16 | Night (train, emit) |

By day: listen and frame. By night: train and emit.

### The Day/Night Cycle

```
Morning: Agent works, listener observes, buffer accumulates
Evening: Buffer deduplicates, prioritizes, curriculum-balances
Night: Trainer runs gradient descent, emitter exports LoRA adapter
Morning: New adapter deployed, agent starts smarter
```

---

## What Was Proven

1. ✅ **Training loop is stable** — 200 steps, no NaN, no divergence
2. ✅ **Loss converges on fleet data** — 91% reduction in 200 steps
3. ✅ **Model absorbs PLATO vocabulary** — terms appear in generation
4. ✅ **P0 negatives are processed** — model sees BLOCKED patterns
5. ✅ **Full pipeline works** — trace → pair → train → evaluate → document
6. ❌ **Coherent generation** — needs 500+ steps minimum, not yet tested
7. ❌ **LoRA adapters** — PEFT not yet integrated
8. ❌ **Real fleet traces** — only synthetic data used

---

## Performance Numbers

| Config | Steps/sec | 1000 steps | Overnight (8h) |
|--------|-----------|------------|-----------------|
| CPU (current) | 1.7 | ~10 min | ~48,000 steps |
| RTX 4050 CUDA (projected) | ~8-12 | ~2 min | ~200,000+ steps |

---

## Files

```
plato-forge-daemon/
├── forge-test.py           # Minimal proof (155 lines)
├── forge-simulation.py     # Extended validation (248 lines)
├── findings.json           # 50-step results
├── findings-extended.json  # 200-step results
├── FINDINGS.md             # Analysis of 50-step run
├── FINDINGS-EXTENDED.md    # Analysis of 200-step run
├── README.md               # Quick start + hardware budget
├── LICENSE                 # MIT
└── .github/workflows/      # CI
```

---

## Next Steps (from the README)

1. Install CUDA torch
2. Add LoRA adapter via PEFT (`peft.get_peft_model`)
3. Wire forge-listener to watch fleet repos in real-time
4. Run continuous training loop (target: 1000 steps overnight)
5. Emit artifacts via forge-emitter every 100 steps
6. Oracle1 pulls and validates

---

*This is a proof of concept. The code works. The ideas are proven. Production deployment requires CUDA, LoRA, real data, and the listener/emitter implementations.*
