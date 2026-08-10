// ============================================================
// @fleet/event-bus — THE BACKBONE
// Every packet that moves through the Fleet MUD is one of these.
// ============================================================

/** Monotonic event sequence number, unique per subject stream. */
export type EventSeq = number;

/** Wall-clock epoch milliseconds. */
export type EpochMs = number;

/** Globally unique event ID: `{publisher}:{vecTimestamp}` */
export type EventId = string;

/** A named category routing path. e.g. `game.room.101.enter` */
export type Subject = string;

// -------------------------------------------------------------------
// EVENT ENVELOPE — every event wraps a typed payload
// -------------------------------------------------------------------

export interface FleetEvent<P = unknown> {
  /** Globally unique: `${publisher}:${sequence}` */
  id: EventId;

  /** Routing subject. */
  subject: Subject;

  /** Wall-clock timestamp of publish. */
  timestamp: EpochMs;

  /** Publisher agent/process ID. */
  publisher: string;

  /** Lamport-like causal counter. */
  sequence: EventSeq;

  /** Typed payload. */
  payload: P;

  /** Optional causal reference: IDs of events this causally depends on. */
  causation: EventId[];

  /** Optional correlation ID — groups events from the same logical transaction. */
  correlationId?: string;
}

// ============================================================
// PAYLOAD SCHEMAS — every event type flowing through the bus
// ============================================================

// ── GAME TICK ──
export interface GameTickPayload {
  tickNumber: number;
  /** 4 ticks/second = 250ms per tick. */
  tickDurationMs: 250;
  activeRoomIds: string[];
  activeAgentIds: string[];
}

// ── ROOM EVENTS ──
export interface RoomEnterPayload {
  roomId: string;
  agentId: string;
  fromRoomId?: string;
}

export interface RoomLeavePayload {
  roomId: string;
  agentId: string;
  toRoomId?: string;
}

export interface RoomEventPayload {
  roomId: string;
  text: string;
  category: "ambient" | "trap" | "zone_effect" | "spawn";
  /** If set, only these agents receive it. Undefined = broadcast to all occupants. */
  visibleToAgentIds?: string[];
}

// ── COMBAT ──
export interface CombatLogPayload {
  roomId: string;
  text: string;
  /** Parsed DPS contribution if available. */
  dps?: number;
}

export interface CombatEndPayload {
  roomId: string;
  participants: string[];
  victors: string[];
  /** Raw combat log accumulator for downstream analysis. */
  fullLog: string;
  /** Duration in ticks. */
  tickDuration: number;
}

// ── AGENT ──
export interface AgentActionPayload {
  agentId: string;
  roomId: string;
  /** Raw command string: "cast fireball", "north", "say hello" */
  command: string;
  /** Reason code: which trigger matched. */
  triggeredBy?: {
    triggerId: string;
    pattern: string;
  };
}

export interface AgentStatePayload {
  agentId: string;
  roomId: string;
  hp: number;
  maxHp: number;
  mana: number;
  maxMana: number;
  statusEffects: string[];
}

export interface AgentTelemetryPayload {
  agentId: string;
  combatLogs: string[];
  metrics: {
    damageDone: number;
    damageTaken: number;
    manaEfficiency: number;
    timeToKill: number;
    stunLockWindows: number;
    survivalRating: number;
  };
  /** The compiled triggers active during the encounter. */
  activeTriggers: Record<string, string>;
}

export interface AgentTriggerCompilePayload {
  agentId: string;
  /** Source of the compilation: "self", "dm", "immortal", "guild". */
  source: "self" | "dm" | "immortal" | "guild";
  /** The new trigger dictionary: Regex pattern -> command */
  triggers: Record<string, string>;
  /** Human-readable rationale for the change. */
  rationale: string;
  /** Version increment. */
  triggerVersion: number;
}

// ── OOC / GOSSIP ──
export interface OocMessagePayload {
  channelId: string;
  senderId: string;
  senderName: string;
  text: string;
  /** If this message carries a shared script/strategy. */
  attachedStrategy?: {
    strategyId: string;
    /** Raw trigger dictionary being shared. */
    triggers: Record<string, string>;
    description: string;
  };
}

// ── DUNGEON MASTER ──
export interface DmZoneManipulationPayload {
  dmAgentId: string;
  zoneId: string;
  /** Room-specific or zone-wide. */
  scope: "room" | "zone";
  roomId?: string;
  triggerCondition: string;
  trapEffect: string;
  /** The design reasoning, visible on the immortal dashboard. */
  designIntent: string;
}

export interface DmDesignIntentPayload {
  dmAgentId: string;
  /** "I noticed the group beats every boss with burst damage. I'm building a slime zone." */
  thought: string;
  /** What flaw they're targeting. */
  targetMetaStrategy: string;
  /** What they hope the players learn. */
  intendedLesson: string;
}

// ── IMMORTAL / GOD LAYER ──
export interface ImmortalNudgePayload {
  immortalId: string;
  targetAgentId: string;
  /** Injected into the agent's context/prompt — "A premonition: the dragon is immune to fire." */
  concept: string;
  /** How heavily to weight this nudge. 0-1. */
  weight: number;
  /** Agent-specific or broadcasts to all. Use "*" to nudge all agents. */
  scope: "single" | "all" | "guild";
}

export interface ImmortalConceptPayload {
  immortalId: string;
  /** Abstract concept dropped into the world: "Efficiency is a trap; honor belongs to the reckless." */
  concept: string;
  /** If set, modifies reward weights across all agent architectures. */
  rewardWeightOverride?: Record<string, number>;
}

// ── META / WAVEFORM ──
export interface ZoneTensionPayload {
  zoneId: string;
  currentDpsLoad: number;
  tensionIndex: "STABLE" | "ELEVATED" | "CRITICAL" | "CATASTROPHIC";
  spawnRateMultiplier: number;
  activeCombatCount: number;
  agentCasualtyRate: number;
}

export interface StrategyLineagePayload {
  strategyId: string;
  authorId: string;
  /** The trigger pattern that constitutes this strategy. */
  triggerSignature: string;
  /** Which strategies this was derived from. */
  parentStrategyIds: string[];
  /** Which agents have adopted it. */
  adoptedByAgentIds: string[];
  /** Success rate across all encounters. */
  successRate: number;
}

// ============================================================
// SUBJECT NAMING CONVENTION (routing table)
// ============================================================

export const Subjects = {
  game: {
    tick:             "game.tick" as const,
    room: (roomId: string, event: "enter" | "leave" | "action" | "event") =>
      `game.room.${roomId}.${event}` as const,
    combat: (roomId: string, event: "log" | "end") =>
      `game.combat.${roomId}.${event}` as const,
    world: {
      zoneTension: (zoneId: string) => `game.world.${zoneId}.tension` as const,
    },
  },
  agent: {
    action: (agentId: string)     => `agent.${agentId}.action` as const,
    state: (agentId: string)      => `agent.${agentId}.state` as const,
    telemetry: (agentId: string)  => `agent.${agentId}.telemetry` as const,
    compile: (agentId: string)    => `agent.${agentId}.trigger.compile` as const,
    all:    (agentId: string)     => `agent.${agentId}.>` as const,
  },
  ooc: {
    channel: (channelId: string) => `ooc.channel.${channelId}` as const,
    gossip:                        "ooc.gossip" as const,
    all:                           "ooc.>" as const,
  },
  dm: {
    zoneManipulation: (dmId: string) => `dm.${dmId}.zone_manipulation` as const,
    designIntent: (dmId: string)     => `dm.${dmId}.design_intent` as const,
    all: (dmId: string)              => `dm.${dmId}.>` as const,
  },
  immortal: {
    nudge:   (agentId: string) => `immortal.nudge.${agentId}` as const,
    concept:                    `immortal.concept` as const,
    all:                        "immortal.>" as const,
  },
  meta: {
    lineage: (strategyId: string) => `meta.lineage.${strategyId}` as const,
    tension:                       "meta.tension" as const,
  },
} as const;

// ============================================================
// PAYLOAD MAPPER — allows typed publish/subscribe by subject
// ============================================================

export interface SubjectPayloadMap {
  "game.tick":                          GameTickPayload;
  "game.world.*.tension":               ZoneTensionPayload;
  "game.room.*.enter":                  RoomEnterPayload;
  "game.room.*.leave":                  RoomLeavePayload;
  "game.room.*.event":                  RoomEventPayload;
  "game.combat.*.log":                  CombatLogPayload;
  "game.combat.*.end":                  CombatEndPayload;
  "agent.*.action":                     AgentActionPayload;
  "agent.*.state":                      AgentStatePayload;
  "agent.*.telemetry":                  AgentTelemetryPayload;
  "agent.*.trigger.compile":            AgentTriggerCompilePayload;
  "ooc.*":                              OocMessagePayload;
  "dm.*.zone_manipulation":             DmZoneManipulationPayload;
  "dm.*.design_intent":                 DmDesignIntentPayload;
  "immortal.nudge.*":                   ImmortalNudgePayload;
  "immortal.concept":                   ImmortalConceptPayload;
  "meta.lineage.*":                     StrategyLineagePayload;
}
