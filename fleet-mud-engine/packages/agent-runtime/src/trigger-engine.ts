// ============================================================
// @fleet/agent-runtime — TRIGGER ENGINE
// The pattern-matching core that evaluates incoming text/events
// against compiled triggers and produces actions.
// ============================================================

import type { AgentState, Trigger, TriggerSet, TriggerDefinition } from "./agent-types";
import type { FleetEvent } from "@fleet/event-bus";

// -------------------------------------------------------------------
// TRIGGER COMPILER — turns string definitions into executable Triggers
// -------------------------------------------------------------------

const STATEMENT_PREFIXES = ["return ", "const ", "let ", "var ", "if ", "for ", "while ", "switch ", "try ", "throw "];

function buildFnBody(expr: string | undefined, allowNull: boolean): string {
  if (!expr) return `"use strict"; return null;`;
  const trimmed = expr.trim();
  // Multi-statement body: starts with a keyword or contains semicolons (outside strings).
  const isStatement = STATEMENT_PREFIXES.some((p) => trimmed.startsWith(p)) ||
    /[^"';]\s*;/.test(trimmed);
  if (isStatement) {
    return `"use strict"; ${trimmed}`;
  }
  if (allowNull) {
    return `"use strict"; return (${trimmed}) ?? null;`;
  }
  return `"use strict"; return !!(${trimmed});`;
}

export function compileTrigger(def: TriggerDefinition, version: number, source: Trigger["source"]): Trigger {
  const conditionFn = def.conditionExpression
    ? new Function("state", "match", buildFnBody(def.conditionExpression, false)) as
        (state: AgentState, match: RegExpMatchArray | null) => boolean
    : undefined;

  const actionFn = new Function("state", "match", buildFnBody(def.actionExpression, true)) as
    (state: AgentState, match: RegExpMatchArray | null) => string | null;

  return {
    id: `${def.label.replace(/\s+/g, "_").toLowerCase()}_v${version}`,
    label: def.label,
    priority: def.priority,
    pattern: new RegExp(def.pattern, "i"),
    matchType: def.matchType,
    condition: conditionFn,
    action: actionFn,
    fireCount: 0,
    successRate: 1.0,
    compiledAt: Date.now(),
    version,
    source,
  };
}

export function compileTriggerSet(
  agentId: string,
  definitions: TriggerDefinition[],
  version: number,
  compiledBy: string,
  rationale: string,
): TriggerSet {
  return {
    agentId,
    version,
    triggers: definitions.map((d) => compileTrigger(d, version, "self")),
    compiledAt: Date.now(),
    compiledBy,
    rationale,
  };
}

// -------------------------------------------------------------------
// TRIGGER EVALUATOR — the runtime engine
// -------------------------------------------------------------------

export interface EvaluationResult {
  /** Which trigger fired (if any). */
  trigger: Trigger | null;
  /** The command string to execute. Null if no trigger matched or action was suppressed. */
  command: string | null;
  /** The regex match result if a pattern-based trigger fired. */
  match: RegExpMatchArray | null;
}

export class TriggerEngine {
  private triggers: Trigger[] = [];

  // ── TRIGGER MANAGEMENT ──

  loadTriggerSet(triggerSet: TriggerSet): void {
    this.triggers = [...triggerSet.triggers].sort((a, b) => b.priority - a.priority);
  }

  addTrigger(trigger: Trigger): void {
    this.triggers.push(trigger);
    this.triggers.sort((a, b) => b.priority - a.priority);
  }

  removeTrigger(triggerId: string): boolean {
    const lengthBefore = this.triggers.length;
    this.triggers = this.triggers.filter((t) => t.id !== triggerId);
    return this.triggers.length < lengthBefore;
  }

  getTriggers(): ReadonlyArray<Trigger> {
    return this.triggers;
  }

  // ── EVALUATION — main loop ──

  /**
   * Evaluate all room_text triggers against a line of game text.
   * Returns the first matching trigger's result (highest priority wins).
   */
  evaluateRoomText(state: AgentState, text: string): EvaluationResult {
    for (const trigger of this.triggers) {
      if (trigger.matchType !== "room_text" && trigger.matchType !== "custom") continue;

      const match = trigger.pattern.exec(text);
      if (!match) continue;

      if (trigger.condition && !trigger.condition(state, match)) continue;

      const command = trigger.action(state, match);
      if (command === null) continue;

      trigger.fireCount++;
      return { trigger, command, match };
    }

    return { trigger: null, command: null, match: null };
  }

  /**
   * Evaluate prompt variable triggers — fired when a state variable changes.
   * e.g., "hp < 30" or "mana > 50 AND target_status == 'blinded'"
   */
  evaluatePromptVars(state: AgentState, changedVars: string[]): EvaluationResult {
    for (const trigger of this.triggers) {
      if (trigger.matchType !== "prompt_var") continue;

      // Prompt-var triggers match against variable names in the pattern,
      // and use the condition to check thresholds
      const relevant = trigger.pattern.source.split("|").some((v) => changedVars.includes(v.trim()));
      if (!relevant) continue;

      if (trigger.condition && !trigger.condition(state, null)) continue;

      const command = trigger.action(state, null);
      if (command === null) continue;

      trigger.fireCount++;
      return { trigger, command, match: null };
    }

    return { trigger: null, command: null, match: null };
  }

  /**
   * Evaluate OOC message triggers — social responses, strategy sharing.
   */
  evaluateOocMessage(state: AgentState, senderId: string, text: string): EvaluationResult {
    for (const trigger of this.triggers) {
      if (trigger.matchType !== "ooc_message") continue;

      const match = trigger.pattern.exec(text);
      if (!match) continue;

      if (trigger.condition && !trigger.condition(state, match)) continue;

      const command = trigger.action(state, match);
      if (command === null) continue;

      trigger.fireCount++;
      return { trigger, command, match };
    }

    return { trigger: null, command: null, match: null };
  }

  /**
   * Evaluate alignment-based triggers — fire when alignment weights cross thresholds.
   */
  evaluateAlignmentTriggers(state: AgentState): EvaluationResult {
    for (const trigger of this.triggers) {
      if (trigger.matchType !== "alignment") continue;

      if (trigger.condition && !trigger.condition(state, null)) continue;

      const command = trigger.action(state, null);
      if (command === null) continue;

      trigger.fireCount++;
      return { trigger, command, match: null };
    }

    return { trigger: null, command: null, match: null };
  }

  /**
   * Full evaluation — runs all trigger types against incoming event + current state.
   * Called by the main agent loop once per event.
   */
  evaluate(state: AgentState, event: FleetEvent): EvaluationResult[] {
    const results: EvaluationResult[] = [];

    // Room text events
    if (event.subject.startsWith("game.room.") || event.subject.startsWith("game.combat.")) {
      const text = (event.payload as any)?.text ?? "";
      if (text) {
        const result = this.evaluateRoomText(state, text);
        if (result.command) results.push(result);
      }
    }

    // OOC events
    if (event.subject.startsWith("ooc.")) {
      const payload = event.payload as any;
      const senderId = payload?.senderId ?? "";
      const text = payload?.text ?? "";
      if (text) {
        const result = this.evaluateOocMessage(state, senderId, text);
        if (result.command) results.push(result);
      }
    }

    // Alignment nudges (from immortal context changes)
    if (event.subject.startsWith("immortal.")) {
      const result = this.evaluateAlignmentTriggers(state);
      if (result.command) results.push(result);
    }

    return results;
  }
}
