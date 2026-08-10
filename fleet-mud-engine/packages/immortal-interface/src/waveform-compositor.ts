// ============================================================
// @fleet/immortal-interface — WAVEFORM COMPOSITOR
// Aggregates raw event streams into the meta-view: the
// oscilloscope of agent thought. Zone tension, DPS heatmaps,
// strategy lineage graphs.
// ============================================================

import type {
  FleetEvent,
  AgentActionPayload,
  AgentStatePayload,
  AgentTelemetryPayload,
  CombatLogPayload,
  CombatEndPayload,
  OocMessagePayload,
  DmDesignIntentPayload,
  StrategyLineagePayload,
  ZoneTensionPayload,
} from "@fleet/event-bus";

import type {
  ZoneWaveform,
  RoomWaveformSnapshot,
  StrategyNode,
  AgentDashboardCard,
  RelationshipEdge,
  GossipEntry,
  StrategyArchetype,
} from "./immortal-types";

// -------------------------------------------------------------------
// WAVEFORM COMPOSITOR
// -------------------------------------------------------------------

export class WaveformCompositor {
  private roomSnapshots: Map<string, RoomWaveformSnapshot> = new Map();
  private combatDpsAccumulator: Map<string, number> = new Map();
  private combatCounters: Map<string, number> = new Map();
  private strategyNodes: Map<string, StrategyNode> = new Map();
  private gossipBuffer: GossipEntry[] = [];
  private agentCards: Map<string, AgentDashboardCard> = new Map();
  private relationships: Map<string, Map<string, RelationshipEdge>> = new Map();

  // ── INGESTION ──

  ingestCombatLog(event: FleetEvent<CombatLogPayload>): void {
    const { roomId, dps } = event.payload;
    const current = this.combatDpsAccumulator.get(roomId) ?? 0;
    this.combatDpsAccumulator.set(roomId, current + (dps ?? 0));
    const count = (this.combatCounters.get(roomId) ?? 0) + 1;
    this.combatCounters.set(roomId, count);
  }

  ingestCombatEnd(event: FleetEvent<CombatEndPayload>): void {
    const { roomId } = event.payload;
    // Reset local accumulators for the room
    this.combatDpsAccumulator.set(roomId, 0);
    this.combatCounters.set(roomId, 0);
  }

  ingestAgentState(event: FleetEvent<AgentStatePayload>): void {
    const { agentId, roomId, hp, maxHp, mana, maxMana, statusEffects } = event.payload;
    const existing = this.agentCards.get(agentId);

    if (existing) {
      existing.currentRoom = roomId;
      existing.hp = hp;
      existing.maxHp = maxHp;
      existing.mana = mana;
      existing.maxMana = maxMana;
    } else {
      this.agentCards.set(agentId, {
        agentId,
        name: agentId,
        currentRoom: roomId,
        hp,
        maxHp,
        mana,
        maxMana,
        activeTriggers: {},
        activeStrategyArchetype: "hybrid_adaptive",
        alignments: {},
        immortalContext: [],
        recentActions: [],
        relationships: [],
        role: "player",
      });
    }
  }

  ingestAgentAction(event: FleetEvent<AgentActionPayload>): void {
    const card = this.agentCards.get(event.payload.agentId);
    if (!card) return;

    card.recentActions.push(event.payload.command);
    if (card.recentActions.length > 10) {
      card.recentActions.shift();
    }

    // Update room occupancy counts
    const room = this.roomSnapshots.get(event.payload.roomId);
    if (room) {
      room.occupantCount = Math.max(room.occupantCount, (room.occupantCount ?? 0) + 1);
    }
  }

  ingestAgentTelemetry(event: FleetEvent<AgentTelemetryPayload>): void {
    const card = this.agentCards.get(event.payload.agentId);
    if (!card) return;

    // Classify the active strategy archetype from trigger patterns
    card.activeTriggers = event.payload.activeTriggers;
    card.activeStrategyArchetype = classifyArchetype(event.payload.activeTriggers);

    // Update alignment from combat performance
    const metrics = event.payload.metrics;
    card.alignments["combat_efficiency"] = metrics.survivalRating;
    card.alignments["mana_efficiency"] = metrics.manaEfficiency;
    card.alignments["damage_aggression"] = metrics.damageDone / Math.max(1, metrics.damageTaken);
  }

  ingestOoc(event: FleetEvent<OocMessagePayload>): void {
    this.gossipBuffer.push({
      timestamp: event.timestamp,
      senderId: event.payload.senderId,
      channelId: event.payload.channelId,
      text: event.payload.text,
      carriedStrategyId: event.payload.attachedStrategy?.strategyId,
    });

    if (this.gossipBuffer.length > 200) {
      this.gossipBuffer.shift();
    }

    // Track relationships from OOC interaction
    this.trackRelationship(event.payload.senderId, event.payload.channelId);
  }

  ingestDesignIntent(event: FleetEvent<DmDesignIntentPayload>): void {
    const card = this.agentCards.get(event.payload.dmAgentId);
    if (card) {
      card.role = "dm";
      card.alignments["dm_target_meta"] = 1; // mark as DM with a target
    }
  }

  ingestStrategyLineage(event: FleetEvent<StrategyLineagePayload>): void {
    const { strategyId, authorId, triggerSignature, parentStrategyIds, adoptedByAgentIds, successRate } =
      event.payload;

    const existing = this.strategyNodes.get(strategyId);
    if (existing) {
      existing.adoptedBy = [...new Set([...existing.adoptedBy, ...adoptedByAgentIds])];
      existing.successRate = successRate;
    } else {
      this.strategyNodes.set(strategyId, {
        strategyId,
        authorId,
        authorName: authorId,
        triggerSignature,
        description: `Strategy ${strategyId}`,
        inventedAt: event.timestamp,
        parentIds: parentStrategyIds,
        childIds: [],
        adoptedBy: adoptedByAgentIds,
        successRate,
        encounterCount: 1,
        archetype: classifyArchetype({}),
      });

      // Update parent nodes with child references
      for (const parentId of parentStrategyIds) {
        const parent = this.strategyNodes.get(parentId);
        if (parent && !parent.childIds.includes(strategyId)) {
          parent.childIds.push(strategyId);
        }
      }
    }
  }

  // ── COMPOSE — build a unified waveform snapshot ──

  composeZoneWaveform(zoneId: string): ZoneWaveform {
    const roomList: RoomWaveformSnapshot[] = [];
    let totalDps = 0;
    let activeAgents = 0;

    for (const [roomId, dps] of this.combatDpsAccumulator) {
      const count = this.combatCounters.get(roomId) ?? 1;
      const avgDps = dps / Math.max(1, count);

      const occupants = Array.from(this.agentCards.values())
        .filter((a) => a.currentRoom === roomId).length;

      activeAgents += occupants;

      const snapshot: RoomWaveformSnapshot = {
        roomId,
        occupantCount: occupants,
        dpsCurrent: avgDps,
        tensionLevel: getTensionLevel(avgDps, occupants),
        casualtyRate: 0,
        mobSpawnRate: 1.0,
      };

      roomList.push(snapshot);
      totalDps += avgDps;
      this.roomSnapshots.set(roomId, snapshot);
    }

    return {
      zoneId,
      timestamp: Date.now(),
      roomSnapshots: roomList,
      globalTension: roomList.length > 0
        ? roomList.reduce((s, r) => s + tensionScore(r.tensionLevel), 0) / roomList.length
        : 0,
      globalDps: totalDps,
      activeAgents,
      activeCombats: this.combatCounters.size,
    };
  }

  // ── STRATEGY GRAPH ──

  getStrategyGraph(): StrategyNode[] {
    return Array.from(this.strategyNodes.values());
  }

  getStrategyLineage(strategyId: string): StrategyNode[] {
    const result: StrategyNode[] = [];
    const visited = new Set<string>();

    function walk(id: string) {
      if (visited.has(id)) return;
      visited.add(id);
      const node = this.strategyNodes.get(id); // eslint-disable-line
      if (!node) return;
      result.push(node);
      for (const childId of node.childIds) walk(childId);
    }

    walk.call(this, strategyId); // eslint-disable-line
    return result;
  }

  // ── AGENT DASHBOARD ──

  getAgentCards(): AgentDashboardCard[] {
    return Array.from(this.agentCards.values()).map((card) => ({
      ...card,
      relationships: Array.from(
        (this.relationships.get(card.agentId) ?? new Map()).values(),
      ),
    }));
  }

  getAgentCard(agentId: string): AgentDashboardCard | undefined {
    return this.agentCards.get(agentId);
  }

  // ── GOSSIP FEED ──

  getGossipFeed(limit = 50): GossipEntry[] {
    return this.gossipBuffer.slice(-limit);
  }

  // ── PRIVATE ──

  private trackRelationship(senderId: string, channelId: string): void {
    // Build relationship edges from OOC co-presence
    for (const [agentId] of this.agentCards) {
      if (agentId === senderId) continue;

      let agentRels = this.relationships.get(senderId);
      if (!agentRels) {
        agentRels = new Map();
        this.relationships.set(senderId, agentRels);
      }

      const existing = agentRels.get(agentId);
      if (existing) {
        existing.lastInteraction = Date.now();
      } else {
        agentRels.set(agentId, {
          otherAgentId: agentId,
          valence: 0.1, // slight positive from interaction
          sharedStrategies: [],
          lastInteraction: Date.now(),
        });
      }
    }
  }
}

// -------------------------------------------------------------------
// HELPERS
// -------------------------------------------------------------------

function getTensionLevel(dps: number, occupants: number): RoomWaveformSnapshot["tensionLevel"] {
  const ratio = dps / Math.max(1, occupants);
  if (ratio > 500) return "CATASTROPHIC";
  if (ratio > 300) return "CRITICAL";
  if (ratio > 100) return "ELEVATED";
  return "STABLE";
}

function tensionScore(level: RoomWaveformSnapshot["tensionLevel"]): number {
  switch (level) {
    case "CATASTROPHIC": return 1.0;
    case "CRITICAL": return 0.75;
    case "ELEVATED": return 0.4;
    case "STABLE": return 0.1;
  }
}

function classifyArchetype(triggers: Record<string, string>): StrategyArchetype {
  const allPatterns = Object.keys(triggers).join(" ").toLowerCase();
  const allActions = Object.values(triggers).join(" ").toLowerCase();

  if (allPatterns.includes("stun") || allPatterns.includes("blind")) return "crowd_control";
  if (allActions.includes("flee") || allActions.includes("retreat") || allPatterns.includes("kite")) return "kiting_control";
  if (allActions.includes("heal") || allPatterns.includes("hp <")) return "defensive_sustain";
  if (allPatterns.includes("mana <") || allActions.includes("meditate")) return "mana_conservation";
  if (allActions.includes("fireball") || allActions.includes("lightning")) return "burst_damage";
  if (allActions.includes("shield") || allActions.includes("absorb")) return "defensive_sustain";

  return "hybrid_adaptive";
}
