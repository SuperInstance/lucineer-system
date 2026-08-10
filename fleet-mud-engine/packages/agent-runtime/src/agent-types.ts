// ============================================================
// @fleet/agent-runtime — Agent State & Trigger Definitions
// ============================================================

import type { EpochMs, EventSeq, Subject } from "@fleet/event-bus";

// -------------------------------------------------------------------
// AGENT STATE — mutable local snapshot of the agent's world
// -------------------------------------------------------------------

export interface AgentState {
  agentId: string;
  name: string;
  roomId: string;
  hp: number;
  maxHp: number;
  mana: number;
  maxMana: number;
  statusEffects: string[];
  /** Parsed prompt variables from the MUD text stream. */
  promptVars: Record<string, number | string>;
  /** Last 50 lines of room/combat log, FIFO. */
  recentLogBuffer: string[];
  /** Alignment/personality weights (0-1 scale, or -1 to +1 for bipolar). */
  alignments: Record<string, number>;
  /** Context injected by immortals — concept blurbs affecting decision weights. */
  immortalContext: string[];
  /** When the state was last updated. */
  lastUpdated: EpochMs;
}

// -------------------------------------------------------------------
// TRIGGER — the atomic unit of agent behavior
// -------------------------------------------------------------------

export interface Trigger {
  /** Unique ID within this agent's trigger set. */
  id: string;
  /** Human-readable label: "Cast fireball on blinded target" */
  label: string;
  /** Priority: higher fires first if multiple triggers match. */
  priority: number;
  /** Compiled regex pattern. */
  pattern: RegExp;
  /** Match against: "room_text", "prompt_hp", "ooc_message", "alignment". */
  matchType: "room_text" | "prompt_var" | "ooc_message" | "alignment" | "custom";
  /** Optional condition: must ALSO pass this predicate for the trigger to fire. */
  condition?: (state: AgentState, match: RegExpMatchArray | null) => boolean;
  /** The action to execute. Returns the command string or null if suppressed. */
  action: (state: AgentState, match: RegExpMatchArray | null) => string | null;
  /** How many times this trigger has fired. */
  fireCount: number;
  /** Success rate of this trigger's actions (updated by telemetry feedback). */
  successRate: number;
  /** When this trigger was compiled. */
  compiledAt: EpochMs;
  /** Version of this trigger. */
  version: number;
  /** Source of compilation. */
  source: "self" | "dm" | "immortal" | "guild";
}

// -------------------------------------------------------------------
// TRIGGER SET — a deployed collection of triggers (versioned)
// -------------------------------------------------------------------

export interface TriggerSet {
  agentId: string;
  version: number;
  triggers: Trigger[];
  compiledAt: EpochMs;
  compiledBy: string;
  rationale: string;
}

// -------------------------------------------------------------------
// AGENT CONFIG — initialization parameters
// -------------------------------------------------------------------

export interface AgentConfig {
  agentId: string;
  name: string;
  startingRoom: string;
  initialHp: number;
  initialMana: number;
  initialAlignments: Record<string, number>;
  /** Default triggers loaded at startup. */
  defaultTriggers?: TriggerDefinition[];
}

export interface TriggerDefinition {
  label: string;
  priority: number;
  pattern: string;  // string form, compiled to RegExp at load time
  matchType: Trigger["matchType"];
  conditionExpression?: string;  // function body string, evaled in sandbox
  actionExpression: string;      // function body string, evaled in sandbox
}
