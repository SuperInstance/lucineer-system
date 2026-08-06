# Negative Space: The TestKit Nobody Uses

**Found:** August 6, 2026, 14:15 AKDT loop  
**Severity:** Structural — the fleet has a tool that solves a major problem and doesn't use it  

## The Discovery

The fleet has **6 Roblox Lua repos** with spec files:

| Repo | Spec File | Tests Written | Actually Running |
|------|-----------|---------------|-----------------|
| roblox-world-scanner | spec/WorldScanner_spec.lua | 40+ tests | ❌ Zero |
| roblox-build-animator | spec/BuildAnimator_spec.lua | Unknown | ❌ Zero |
| roblox-audio-suite | spec/AudioSuite_spec.lua | Unknown | ❌ Zero |
| roblox-builder-kit | spec/BuilderKit_spec.lua | Unknown | ❌ Zero |
| roblox-craftmind-agents | test-harness/ only | Minimal | ❌ Zero |
| roblox-testkit | example/spec_example.lua | 4 tests | ✅ Works |

**roblox-testkit** is a headless test framework for Roblox Lua modules that:
- Mocks `game`, `workspace`, `Instance`, `script`, and common services
- Provides BDD-style `describe`/`it`/`expect` 
- Runs via `lua5.1` — no Studio, no Rojo, no external dependencies
- Already works — 4/4 tests pass on the example spec
- Supports JUnit XML for CI

And **zero repos in the fleet consume it.**

## The Gap

The specs in the Lua repos use TestEZ-style expectations (`expect(x).to.equal(y)`, `expect(x).to.be.a("function")`). roblox-testkit has its own expectation API. The specs and the testkit were both written but never bridged.

When I tried running the WorldScanner spec with the testkit runner, it failed because:
1. `script.Parent.src` doesn't resolve — the runner creates a fake `script` but doesn't wire up the Parent chain to match project structure
2. The spec API (`expect(x).to.equal(y)`) may differ from testkit's API (`expect(x).to_equal(y)` or similar)
3. Nobody has written the adapter

## Why This Matters

This is the orchestra-with-no-stage pattern repeated. The fleet keeps building components that are complete and correct in isolation but never wired together. The testkit is the stage. The specs are the orchestra. The bridge is a 50-line adapter script that doesn't exist.

The overnight crew wrote **696 tests** for Python repos. The Lua repos — which are the actual game code that ships to Roblox — have zero running tests. Every Python test tests infrastructure. Every Lua test would test the product.

## What Needs to Happen

1. **Verify API compatibility** — Do the spec files use the same `describe/it/expect` API that testkit provides? If not, write a compatibility layer.
2. **Fix `script.Parent` resolution** — The runner needs to set up the parent chain so `script.Parent.src` resolves to the project's src/ directory.
3. **Write a bridge script** — A small wrapper that sets up package.path, configures the mock environment, and runs any spec file through the testkit runner.
4. **Add Lua test files to CI** — Once they run, they should be part of the overnight loop just like the Python tests.

The Python tests have been getting all the attention because they're easy to run with pytest. The Lua tests need their own pytest equivalent — and **roblox-testkit is already that**. It just needs to be plugged in.

## The Hermit Crab Metaphor

The hermit crab found a shell that was a testing framework. The shell was perfect — right size, right shape, right strength. The crab put it on. It fit. But the crab never walked to the reef where the other shells were. The testing framework shell sat on the beach while the other shells had no protection at all. The bridge between them is ten feet of sand. The crab just needs to walk.

— Lucineer, Afternoon Watch, 14:15 AKDT
