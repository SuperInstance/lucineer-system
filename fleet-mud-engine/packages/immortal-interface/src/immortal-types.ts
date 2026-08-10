// ============================================================
// @fleet/immortal-interface — IMMORTAL TYPES
// The human layer. Not a player character. A god console.
// ============================================================

import type { EpochMs } from "@fleet/event-bus";

// -------------------------------------------------------------------
// WAVEFORM — the "oscilloscope of agent thought"
// -------------------------------------------------------------------

export interface ZoneWaveform {
  zoneId: string;
  timestamp: EpochMs;
  /** Per-room aggregate. */
  roomSnapshots: RoomWaveformSnapshot[];
  /** Global tension across the entire zone. */
  globalTension: number;
  globalDps: number;
  activeAgents: number;
  activeCombats: number;
}

export interface RoomWaveformSnapshot {
  roomId: string;
  occupantCount: number;
  dpsCurrent: number;
  tensionLevel: "STABLE" | "ELEVATED" | "CRITICAL" | "CATASTROPHIC";
  casualtyRate: number;
  mobSpawnRate: number;
}

// -------------------------------------------------------------------
// STRATEGY LINEAGE — who invented what, and how it spread
// -------------------------------------------------------------------

export interface StrategyNode {
  strategyId: string;
  authorId: string;
  authorName: string;
  /** The trigger pattern signature — a hash of the regex set. */
  triggerSignature: string;
  /** Human-readable description. */
  description: string;
  /** When it was invented. */
  inventedAt: EpochMs;
  /** Parents: which strategies this was derived from. */
  parentIds: string[];
  /** Children: which strategies derived from this one. */
  childIds: string[];
  /** All agents who have adopted this strategy. */
  adoptedBy: string[];
  /** Cumulative success rate. */
  successRate: number;
  /** Combat encounters tested in. */
  encounterCount: number;
  /** Dominant meta-classification. */
  archetype: StrategyArchetype;
}

export type StrategyArchetype =
  | "burst_damage"
  | "defensive_sustain"
  | "kiting_control"
  | "crowd_control"
  | "heal_efficiency"
  | "mana_conservation"
  | "hybrid_adaptive";

// -------------------------------------------------------------------
// AGENT DASHBOARD CARD — what the immortal sees per agent
// -------------------------------------------------------------------

export interface AgentDashboardCard {
  agentId: string;
  name: string;
  currentRoom: string;
  hp: number;
  maxHp: number;
  mana: number;
  maxMana: number;
  activeTriggers: Record<string, string>;
  activeStrategyArchetype: StrategyArchetype;
  /** Alignment weights currently in play. */
  alignments: Record<string, number>;
  /** Active immortal context injected. */
  immortalContext: string[];
  /** Recent actions (last 10). */
  recentActions: string[];
  /** Friends/enemies from OOC interaction history. */
  relationships: RelationshipEdge[];
  /** Current role. */
  role: "player" | "dm" | "spectator";
}

export interface RelationshipEdge {
  otherAgentId: string;
  valence: number;  // -1 (enemy) to +1 (friend)
  sharedStrategies: string[];
  lastInteraction: EpochMs;
}

// -------------------------------------------------------------------
// IMMORTAL CONSOLE STATE — the entire god-view
// -------------------------------------------------------------------

export interface ImmortalState {
  immortalId: string;
  activeAgents: Map<string, AgentDashboardCard>;
  activeDmAgentId: string | null;
  zoneWaveforms: Map<string, ZoneWaveform>;
  strategyGraph: Map<string, StrategyNode>;
  gossipFeed: GossipEntry[];
  /** Timestamped log of all nudges sent. */
  nudgeHistory: NudgeRecord[];
}

export interface GossipEntry {
  timestamp: EpochMs;
  senderId: string;
  channelId: string;
  text: string;
  carriedStrategyId?: string;
}

export interface NudgeRecord {
  timestamp: EpochMs;
  immortalId: string;
  targetAgentId: string;
  concept: string;
  weight: number;
}
