# Murmur → DCA Integration Plan

## Phase 1: Module Discovery Bridge
- Port the `ModuleRegistry` pattern to DCA as a capability scanner
- Scan Lucineer workspace for available skills/tools
- Classify as foundation (core DCA primitives) vs feature (agent capabilities)
- Expose via API for the orchestrator to consume

## Phase 2: Knowledge Tensor
- Integrate `@superinstance/knowledge-tensor` for cross-domain linking
- Build tensor operations into DCA's memory system
- Use semantic connections for agent skill recommendations

## Phase 3: Fleet Standards
- Adopt the Dockside Exam checklist as a DCA health check
- Implement bottle messages (for-fleet/from-fleet directories) for inter-agent communication
- Port the Tender Protocol for offline/edge agent servicing
- CHARTER.md / STATE.md pattern for each DCA agent

## Phase 4: Wiki Surface
- Deploy a Next.js dashboard similar to Murmur for DCA fleet visualization
- Module cards with load/unload capability
- Resource monitoring display
- Sitemap and catalog pages

## Key Files to Reference
- `src/lib/module-registry.ts` — module discovery pattern
- `src/types/modules.ts` — type definitions
- `DOCKSIDE-EXAM.md` — fleet certification standard
- `CHARTER.md` — agent identity format
