# ZeroClaw Arena — Quick Reference

> **Repo:** `github.com/SuperInstance/zeroclaw-arena`  
> **Clone:** `/home/eileen/projects/study-zeroclaw-arena`  
> **License:** MIT  
> **Language:** Python 3.10+  
> **Dependencies:** Zero (core), pytest (dev), numpy (experiments), torch (GPU experiments, optional)

## What It Is

A framework for learning game policies **without neural networks** — uses tile-based Monte Carlo self-play, hash-based vector embeddings, and evolutionary score updates.

## Core API

```python
from zeroclaw import TicTacToe, TileField, CompiledPolicy, run_arena

# Train
game = TicTacToe()
field = TileField(n_simulations=20, temperature=0.3)
field.train(game, num_games=500)

# Compile to zero-dependency lookup
policy = CompiledPolicy.from_tile_field(field)
action = policy("X O  X   ")  # O(1) lookup

# Evaluate
results = policy.evaluate(num_games=1000)

# Full pipeline
results = run_arena(games=["tictactoe"], mode="tile", num_train=500, num_eval=1000)
```

## Key Results

| Game | Win Rate vs Random | Training Time | Tiles |
|------|-------------------|---------------|-------|
| Tic-Tac-Toe | 66-71% | 0.57s | 1,238 |
| Connect 4 | 48% | ~5s | ~3,000 |
| Go 9×9 | 67% | ~30s | ~5,000 |
| Blackjack | 39% (near-optimal) | <1s | ~100 |

## Architecture

- **TileField** — training algorithm (Monte Carlo + softmax + evolution)
- **CompiledPolicy** — deployment artifact (O(1) dict lookup, zero deps)
- **Arena** — experiment runner (explore/evolve/exploit/tile/random modes)
- **VectorDB** — SQLite + BLAKE2b embeddings for pattern matching
- **Game Protocol** — `state() / legal_actions() / step() / reset() / copy()`

## Why It Matters

- **No neural nets** — pure statistics + vectors + evolution
- **O(1) deployment** — compiled policy is a dict lookup
- **Fully interpretable** — every decision traces to a tile entry
- **Zero dependencies** — compiled policy runs anywhere
- **Self-evolving** — policy weights tune automatically from outcomes

## Files

```
zeroclaw/
├── __init__.py          # Public API
├── games.py             # TicTacToe, Connect4, Go9x9, HoldemHand
├── tile_field.py        # TileField (training algorithm)
├── compiled_policy.py   # CompiledPolicy (deployment artifact)
├── arena.py             # run_arena() experiment runner
└── experiments.py       # Quick experiment functions

experiments/
├── zeroclaw.py          # Full standalone ZeroClaw agent (428 lines)
├── evolutionary_strategy.py  # GPU evolutionary hyperparameter optimization
├── tile_compiler.py     # Original tile → lookup compiler
├── hierarchical_tiles.py # Multi-resolution tile hierarchies
├── transfer_learning.py # Cross-game pattern transfer
├── gpu_vector_engine.py # CUDA vector operations
├── vector_store.py      # torch-vector-search wrapper
└── *.py                 # 15+ more experiments
```
