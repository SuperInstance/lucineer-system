# Murmur — Deep Dive Analysis

## What It Does
Self-populating TensorDB wiki and bulletin board for the SuperInstance fleet. A Next.js 15 frontend that auto-organizes fleet knowledge via a module registry scanning the monorepo's packages directory.

## Architecture
- **Frontend**: Next.js 15, React 19, TypeScript 5, Tailwind CSS 4
- **Module Registry** (`src/lib/module-registry.ts`): Singleton pattern using Node.js global scope to persist across serverless hot-reloads. Scans `../packages` (or `PACKAGES_PATH` env) for package.json files, classifies as "foundation" vs "feature" modules.
- **Module Classification**: Foundation primitives = async, validate, cache, events, config, storage, provider-base, logger. Everything else = feature.
- **API Layer**: `/api/modules` (list), `/api/modules/load` (activate), `/api/modules/unload` (deactivate)
- **State Tracking**: idle → loading → loaded/error, with resource monitoring (CPU, memory, disk)

## Key Innovations
1. **Self-Populating**: Discovers modules automatically by scanning package.json files — zero manual registration
2. **Foundation vs Feature Taxonomy**: Built-in classification of core infrastructure vs user-facing modules
3. **Serverless-Safe Singletons**: Uses `global._superInstanceRegistry` pattern to survive Next.js dev hot-reloads
4. **Resource Monitoring**: Each module tracks CPU/memory/disk usage with timestamps

## DCA / Slackwater Integration Points
- **Module Registry Pattern → DCA**: The discovery + classification of capabilities maps directly to DCA's agent skill registry. Foundation modules = DCA core primitives; Feature modules = DCA agents.
- **TensorDB Integration**: Wiki connects to `@superinstance/knowledge-tensor` — the same knowledge graph concept DCA uses for cross-domain linking.
- **Load/Unload API**: Maps to DCA agent activation/deactivation lifecycle.

## Code Quality
- **Well-structured**: Clean separation of concerns (registry, API routes, types, UI components)
- **Typed**: Full TypeScript with proper interfaces (`ModuleMetadata`, `ModuleState`, `ModuleResources`)
- **Documented**: JSDoc on every method in module-registry.ts
- **Resilient**: Graceful error handling on package scan failures

## Patterns to Adopt
1. **Auto-discovery via package.json scanning** — works for any monorepo
2. **Global singleton for serverless persistence** — solves hot-reload state loss
3. **Foundation/Feature taxonomy** — clean separation of infrastructure from capabilities
4. **Dockside Exam checklist** — comprehensive fleet certification standard (47-point checklist)
5. **Git-Agent Standard v2.0** — CHARTER, STATE, bottle messages, tender protocol
