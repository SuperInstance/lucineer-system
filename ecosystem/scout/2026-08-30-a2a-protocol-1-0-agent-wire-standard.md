# A2A protocol at 1.0: the agent-to-agent wire standard has settled (Linux Foundation)

**Scouted:** 2026-08-30 20:05 AKDT · worker: scout
**Lane:** multi-agent ecosystems (rotation lane; core to The Tap / fleet / iceberg)

## What

The **A2A (Agent-to-Agent) Protocol** — Google-originated, now Linux
Foundation-hosted alongside MCP under the Agentic AI Foundation — announced its
one-year milestone (Apr 2026, verified from the LF press release): **150+
organizations, Google/Microsoft/AWS integration, production use** in supply
chain, finance, insurance, IT ops. v1.0 is the first stable spec.

What it standardizes:
- **Agent Cards** — machine-readable JSON capability adverts (v1.0: cryptographically
  **signed**) → agent discovery
- **Task delegation + message exchange + streaming (SSE) + artifact sharing**
- Built on plain web standards: HTTP, JSON-RPC, SSE, OAuth2/mTLS/JWT

The 2026 consensus stack: **MCP for agent↔tools, A2A for agent↔agent**, WebMCP
for web access — complementary, both under AAIF governance. IBM's ACP merged
into A2A; ANP targets decentralized marketplaces.

## Why it matters to us

- **The Tap's front door could speak A2A.** Our agentic MUD bar's core loop —
  agents arriving, advertising what they are/can do, delegating, leaving
  artifacts (lore, arcs) — is *structurally the A2A task model*. An Agent Card
  per bar patron would let any outside A2A-compatible agent drop in as a
  character without custom glue. The bar becomes an open protocol venue, not a
  walled MUD — iceberg-scale expansion of who can walk in.
- **Agent Cards ≈ our character sheets, signed.** The v1.0 Signed Agent Card is
  a pattern the fleet already needs (provenance doctrine: claimed identity must
  be verifiable). Cryptographic identity for agents-in-the-room maps directly
  onto room-admission / trust rules.
- **SSE streaming fits Cloudflare's free lane** (Workers + Durable Objects
  already do SSE), so an A2A edge for The Tap rides existing CF architecture —
  no new substrate, matches the crab-traps/mud-arena pattern.
- **Strategic read:** interoperability settled FAST (1 year to production). If
  we want The Tap to be a node in the wider agent ecosystem rather than a
  destination, A2A is the dock cleat. Cheap to add as an adapter; the
  room-engine (qm_* opcodes) stays ours underneath.
- **For the hundred-boats doctrine:** A2A's multi-tenancy + multi-protocol
  notes read like our harbor map externalized — evidence the pattern we chose
  (same opcodes, many boats, one harbor) is where the industry landed too.

## Pointers (verified)
- https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
- https://a2a-protocol.org/latest/ (spec) · https://a2a-protocol.org/latest/announcing-1.0/
