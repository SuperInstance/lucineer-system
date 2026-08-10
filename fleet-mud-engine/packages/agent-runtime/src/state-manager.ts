// ============================================================
// @fleet/agent-runtime — STATE MANAGER
// Parses the MUD text stream into structured state, handles
// prompt parsing (like old-school zMud/TinTin++ prompt parsers),
// and maintains the agent's local snapshot of the world.
// ============================================================

import type { AgentState, AgentConfig } from "./agent-types";
import type { FleetEvent, AgentStatePayload, AgentTriggerCompilePayload, ImmortalNudgePayload } from "@fleet/event-bus";

// -------------------------------------------------------------------
// PROMPT PARSER — regex extracts hp/mana/status from MUD prompt lines
// e.g. "<150hp 80m 45mv Standing>" or "<H:150 M:80 V:45>"
// -------------------------------------------------------------------

const ZMUD_PROMPT_PATTERN = /<(\d+)hp\s+(\d+)m(?:\s+(\d+)mv)?(?:\s+(\w+))?>/i;
const TINTIN_PROMPT_PATTERN = /H:(\d+)\s+M:(\d+)\s+V:(\d+)/i;
const EXTENDED_PROMPT_PATTERN = /(?:HP|hp):\s*(\d+)\/(\d+)\s+(?:Mana|MN|mana):\s*(\d+)\/(\d+)/i;

export interface ParsedPrompt {
  hp: number;
  maxHp?: number;
  mana: number;
  maxMana?: number;
  movePts?: number;
  status?: string;
}

export function parsePrompt(line: string): ParsedPrompt | null {
  // Try zMud style: <150hp 80m 45mv Standing>
  let match = line.match(ZMUD_PROMPT_PATTERN);
  if (match) {
    return {
      hp: parseInt(match[1]!, 10),
      mana: parseInt(match[2]!, 10),
      movePts: match[3] ? parseInt(match[3], 10) : undefined,
      status: match[4] || undefined,
    };
  }

  // Try TinTin++ style: H:150 M:80 V:45
  match = line.match(TINTIN_PROMPT_PATTERN);
  if (match) {
    return {
      hp: parseInt(match[1]!, 10),
      mana: parseInt(match[2]!, 10),
      movePts: parseInt(match[3]!, 10),
    };
  }

  // Try extended: HP: 120/150 Mana: 60/100
  match = line.match(EXTENDED_PROMPT_PATTERN);
  if (match) {
    return {
      hp: parseInt(match[1]!, 10),
      maxHp: parseInt(match[2]!, 10),
      mana: parseInt(match[3]!, 10),
      maxMana: parseInt(match[4]!, 10),
    };
  }

  return null;
}

// -------------------------------------------------------------------
// STATE MANAGER
// -------------------------------------------------------------------

export class StateManager {
  state: AgentState;

  constructor(config: AgentConfig) {
    this.state = {
      agentId: config.agentId,
      name: config.name,
      roomId: config.startingRoom,
      hp: config.initialHp,
      maxHp: config.initialHp,
      mana: config.initialMana,
      maxMana: config.initialMana,
      statusEffects: [],
      promptVars: {},
      recentLogBuffer: [],
      alignments: { ...config.initialAlignments },
      immortalContext: [],
      lastUpdated: Date.now(),
    };
  }

  // ── STATE MUTATORS ──

  /** Apply a parsed prompt to the state snapshot. */
  applyPrompt(parsed: ParsedPrompt): string[] {
    const changed: string[] = [];

    if (parsed.hp !== this.state.hp) {
      this.state.hp = parsed.hp;
      this.state.promptVars["hp"] = parsed.hp;
      changed.push("hp");
    }
    if (parsed.maxHp !== undefined && parsed.maxHp !== this.state.maxHp) {
      this.state.maxHp = parsed.maxHp;
      this.state.promptVars["maxHp"] = parsed.maxHp;
      changed.push("maxHp");
    }
    if (parsed.mana !== this.state.mana) {
      this.state.mana = parsed.mana;
      this.state.promptVars["mana"] = parsed.mana;
      changed.push("mana");
    }
    if (parsed.maxMana !== undefined && parsed.maxMana !== this.state.maxMana) {
      this.state.maxMana = parsed.maxMana;
      this.state.promptVars["maxMana"] = parsed.maxMana;
      changed.push("maxMana");
    }
    if (parsed.status && parsed.status !== this.state.promptVars["status"]) {
      this.state.promptVars["status"] = parsed.status;
      changed.push("status");
    }

    return changed;
  }

  /** Apply an official state update from the event bus. */
  applyStatePayload(payload: AgentStatePayload): void {
    this.state.hp = payload.hp;
    this.state.maxHp = payload.maxHp;
    this.state.mana = payload.mana;
    this.state.maxMana = payload.maxMana;
    this.state.statusEffects = payload.statusEffects;
    this.state.roomId = payload.roomId;
    this.state.lastUpdated = Date.now();
  }

  /** Append a line to the log buffer, maintaining FIFO window. */
  pushLogLine(line: string): void {
    this.state.recentLogBuffer.push(line);
    if (this.state.recentLogBuffer.length > 50) {
      this.state.recentLogBuffer.shift();
    }
  }

  /** Change room. */
  moveToRoom(roomId: string): void {
    this.state.roomId = roomId;
    this.state.lastUpdated = Date.now();
  }

  /** Handle a trigger compile event — note the context change but don't apply (triggers are in TriggerEngine). */
  noteTriggerCompile(payload: AgentTriggerCompilePayload): void {
    this.state.promptVars["triggerVersion"] = payload.triggerVersion;
    this.state.promptVars["lastCompileSource"] = payload.source;
  }

  /** Absorb an immortal nudge — injects into context and may shift alignment weights. */
  absorbNudge(payload: ImmortalNudgePayload): void {
    this.state.immortalContext.push(payload.concept);
    // Keep last 10 nudges
    if (this.state.immortalContext.length > 10) {
      this.state.immortalContext.shift();
    }

    // Nudge shifts alignment weights — applied multiplicatively by weight
    // e.g., "honor belongs to the reckless" might increase riskTolerance
    if (payload.weight > 0) {
      const current = this.state.alignments["nudgeWeight"] ?? 0;
      this.state.alignments["nudgeWeight"] = current + payload.weight;
      this.state.alignments["nudgeActive"] = 1;
    }
  }

  /** Tick handler — decrement status effects, apply environmental damage. */
  processTick(damagePerTick: number = 0): void {
    if (damagePerTick > 0) {
      this.state.hp = Math.max(0, this.state.hp - damagePerTick);
    }
    this.state.lastUpdated = Date.now();
  }

  // ── QUERIES ──

  getHpRatio(): number {
    return this.state.maxHp > 0 ? this.state.hp / this.state.maxHp : 0;
  }

  getManaRatio(): number {
    return this.state.maxMana > 0 ? this.state.mana / this.state.maxMana : 0;
  }

  getAlignment(name: string): number {
    return this.state.alignments[name] ?? 0;
  }

  /** Produce a snapshot suitable for the event bus state publication. */
  toStatePayload(): AgentStatePayload {
    return {
      agentId: this.state.agentId,
      roomId: this.state.roomId,
      hp: this.state.hp,
      maxHp: this.state.maxHp,
      mana: this.state.mana,
      maxMana: this.state.maxMana,
      statusEffects: [...this.state.statusEffects],
    };
  }

  /** Produce a compact metric snapshot for telemetry. */
  toMetrics(): Record<string, number> {
    return {
      hp: this.state.hp,
      mana: this.state.mana,
      hpRatio: this.getHpRatio(),
      manaRatio: this.getManaRatio(),
    };
  }
}
