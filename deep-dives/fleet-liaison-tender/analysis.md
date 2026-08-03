# fleet-liaison-tender — Deep Dive Analysis

## Overview
Inter-vessel communication system for the Cocapn Fleet. Manages "bottles" (message units) between cloud and edge agents, with priority translation, message compression for bandwidth-constrained nodes, and state tracking via local JSON persistence.

## Architecture

### Bottle System (`bottles.py`)
- **`Bottle`** dataclass: id, origin, target, type, payload, priority, compressed, timestamp, status
- Status lifecycle: `pending → delivered → acked`
- Serialization: `to_json()` / `from_json()` for git-native transport
- Bottles are `.md` or `.json` files in directional directories: `for-fleet/`, `for-oracle1/`

### Tender Types (4 specializations)
1. **Research Tender**: carries specs cloud→edge, benchmarks edge→cloud
2. **Data Tender**: batches big data, compresses to edge-relevant subset (max 10 items)
3. **Context Tender**: selective fleet visibility for isolated nodes (200 char summary limit)
4. **Priority Tender**: translates urgency between cloud/edge realities

### Priority Translation (`priority.py`)
- **Cloud → Edge**: low→ignore, medium→queue, high→handle_soon, critical→immediate
- **Edge → Cloud**: nominal→info, degraded→warning, failing→high, down→critical
- **`should_forward()`**: filter — "low" priority messages are NOT forwarded to edge (saves bandwidth)
- **`translate_message()`**: attaches both original and translated priority

### Message Compression (`compression.py`)
Type-aware compression strategy:
- **Research**: extracts only `changes_affecting_edge`, `isa_modifications`, `deadline`
- **Data**: limits to 10 items, marks `edge_relevant_only: true`
- **Context**: truncates summary to 200 chars, extracts `action_required` flag
- **Priority**: translates priority + truncates reason to 100 chars
- **Generic**: stringifies payload, truncates to 200 chars

### State Management (`state.py`)
- JSON file at `~/.tenderctl/state.json`
- Per-bottle tracking: vessel, status, timestamp, delivered_at, acked_at
- Per-vessel status: pending/delivered/acked counts
- All operations are file-based (no database dependency)

### GitHub Transport (`github_client.py`)
- Scans org repos for vessel pattern (name contains "vessel" or known names)
- Looks for `.md` bottle files in `for-oracle1/` and `for-fleet/` directories
- Reads file content via GitHub Contents API (base64 decode)
- Pagination support for large orgs (up to 15 pages × 100 repos)

### CLI Controller (`cli.py`)
- **`scan`**: discover new bottles across vessels, add to state
- **`deliver`**: compress + priority-filter + forward pending bottles
- **`status`**: show per-vessel message counts
- **`ack`**: mark bottle as acknowledged

## Key Patterns

1. **Information asymmetry**: cloud→edge is curated/compressed; edge→cloud is raw/detailed
2. **Git as transport**: messages are files in repos — no message broker needed
3. **Priority-gated delivery**: low-priority messages filtered before consuming edge bandwidth
4. **Type-aware compression**: different message types get different compression strategies
5. **Ack-based reliability**: bottles track pending→delivered→acked lifecycle
6. **Vessel specialization**: different tenders for different communication needs

## Technology
- **Language**: Python 3.10+
- **Dependencies**: `requests` (GitHub API only)
- **Transport**: GitHub git (bottle files in repo directories)
- **State**: local JSON file
