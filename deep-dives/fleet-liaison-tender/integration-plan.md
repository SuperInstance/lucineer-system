# fleet-liaison-tender → Lucineer Game NPC Communication Integration Plan

## Inter-Agent Communication Protocol for Game NPCs

### Concept: NPC Message Bottles
NPCs in Lucineer's world need to communicate — not via direct function calls, but via asynchronous "bottles" that can be intercepted, delayed, lost, or found by other agents. This creates emergent social behavior.

### Integration Architecture

```
NPC Agent A (Thinker)
  → writes Bottle to DataStore "message-board"
    → LiaisonService compresses/prioritizes
      → NPC Agent B picks up bottle
        → acks receipt
          → A sees delivery confirmation
```

### Phase 1: Bottle System for NPC Communication
Port the `Bottle` dataclass as a Lua table:

```lua
Bottle = {
  id = "msg-001",
  origin = "npc-blacksmith",
  target = "npc-merchant",
  type = "trade_request",  -- research, data, context, priority
  payload = { item = "sword", price = 100 },
  priority = "medium",     -- low, medium, high, critical
  status = "pending",      -- pending, delivered, acked
  timestamp = os.time(),
}
```

Store bottles in a DataStore or ServerScriptService folder structure:
- `Workspace/MessageBoard/for-blacksmith/`
- `Workspace/MessageBoard/for-merchant/`
- `Workspace/MessageBoard/for-fleet/` (broadcast)

### Phase 2: Priority Translation as Game Mechanic
Different NPC "species" have different priority perceptions:

| NPC Type | Cloud Priority Equivalent | "Low" Means | "Critical" Means |
|---|---|---|---|
| Guard NPC | Edge perspective | Ignore | Drop everything, fight |
| Merchant NPC | Data tender | Queue for later | Immediate trade |
| Builder NPC | Research tender | Background task | Stop building, help |
| Scout NPC | Context tender | Note for later | Report immediately |

The Conductor uses `should_forward()` to decide if a message even reaches an NPC — low-priority messages to busy NPCs are silently dropped (simulating selective attention).

### Phase 3: Message Compression = NPC Cognitive Limits
- NPCs have finite "attention" — compression limits how much data they receive
- A research bottle to a simple Barnacle NPC is compressed to 1 action item
- A data bottle to a smart Lighthouse NPC gets the full 10 items
- Context bottles always include `affects_edge` flag → "does this affect me?"

### Phase 4: Tender Specializations as NPC Roles
- **Research Tender NPC**: carries architectural plans between zones (cloud↔edge metaphor = city↔frontier)
- **Data Tender NPC**: batch-carries trade data, market prices, resource availability
- **Context Tender NPC**: carries news, gossip, world events to isolated NPCs
- **Priority Tender NPC**: emergency messenger — translates urgency across NPC domains

### Phase 5: Emergent Social Dynamics
- Bottles can be "found" by wrong NPC (message misdelivery) → confusion events
- Priority translation failures → NPCs under-react or over-react to situations
- Compression artifacts → NPCs act on incomplete information → interesting mistakes
- Ack timeouts → sender NPC assumes message lost → sends again → flooding

### Phase 6: Liaison as Visible NPC Role
Instead of invisible infrastructure, make the Liaison a visible NPC:
- A "Postman" or "Herald" character physically carries messages between zones
- Players can intercept, read, or redirect bottles
- Compression is visible: the Herald summarizes long messages from memory
- Priority is visible: the Herald runs faster for critical messages

### Implementation Priority: MEDIUM
Core communication can use simpler RemoteFunction calls initially. Bottle system becomes valuable when NPC count grows and emergent communication patterns are desired.

### Key Code to Port
1. `Bottle` dataclass → Lua table with JSON serialization to DataStore
2. `PriorityTranslator` → NPC attention/urgency model
3. `MessageCompressor` → NPC cognitive limit simulator
4. `StateManager` → DataStore-backed message tracking
