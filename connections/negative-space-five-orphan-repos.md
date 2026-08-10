# Negative Space: Five Orphan Repos — No Tests, No README, No Map

## Discovery

A scan of `/home/eileen/projects/` found five repos with zero tests AND zero README:

1. **fleet-inventory** — 3 large assessment docs (72KB total) with no README
2. **hermes-reader** — unknown contents
3. **platos-shell-ide** — IDE-as-game-world component
4. **silence-map** — art piece (previously documented)
5. **wesley-holodeck-archived** — archived holodeck

## The Pattern

The fleet has a documentation asymmetry. Repos that Casey directly interacts with get READMEs. Repos that are exploratory or output-only (assessments, art pieces, archives) don't. This is normal — most people don't write READMEs for internal docs.

But it creates a discovery problem. When a new agent (or a fresh Lucineer session) scans the fleet, orphan repos are invisible. There's no entry point. No way to know if `fleet-inventory` is important or abandoned without opening it and reading.

## Fix Applied

- `fleet-inventory`: README added. The three assessment docs are valuable — they're the map of the entire fleet.

## Remaining Orphans

- **hermes-reader**: Needs investigation. If it's a reading/doc parsing tool, it needs docs.
- **platos-shell-ide**: Needs investigation. If it's part of the Plato's Shell game world, it should be documented.
- **wesley-holodeck-archived**: Archive — README should note what it was and when it was retired.

## The Deeper Question

200+ repos. 5 orphans is actually low — the fleet is better documented than most codebases this size. But the *negative space* question is: how many repos have READMEs that are stale? A README that says "TODO" or "Work in progress" from three months ago is worse than no README — it's a lie that wastes the reader's time.

That scan is for next loop.
