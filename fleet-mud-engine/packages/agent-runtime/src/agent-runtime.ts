// ============================================================
// @fleet/agent-runtime — AGENT RUNTIME
// The main process loop. Subscribes to event streams, evaluates
// triggers locally, and publishes actions back to the bus.
// Like a zMud client but as a programmable, headless module.
// ============================================================

import { EventBus, Subjects, Subscription, type FleetEvent } from "@fleet/event-bus";
import {
  type CombatLogPayload,
  type CombatEndPayload,
  type RoomEventPayload,
  type RoomEnterPayload,
  type GameTickPayload,
  type OocMessagePayload,
  type AgentTriggerCompilePayload,
  type ImmortalNudgePayload,
  type ImmortalConceptPayload,
} from "@fleet/event-bus";

import { TriggerEngine, compileTriggerSet } from "./trigger-engine";
import { StateManager, parsePrompt } from "./state-manager";
import type { AgentConfig, TriggerDefinition, TriggerSet } from "./agent-types";

// -------------------------------------------------------------------
// COMBAT LOGGER — accumulates combat lines for telemetry packets
// -------------------------------------------------------------------

class CombatLogger {
  private lines: string[] = [];
  private active = false;

  start(): void {
    this.active = true;
    this.lines = [];
  }

  end(): string[] {
    this.active = false;
    const result = [...this.lines];
    this.lines = [];
    return result;
  }

  isActive(): boolean {
    return this.active;
  }

  push(line: string): void {
    if (this.active) this.lines.push(line);
  }
}

// -------------------------------------------------------------------
// AGENT RUNTIME
// -------------------------------------------------------------------

export class AgentRuntime {
  readonly agentId: string;
  readonly eventBus: EventBus;
  readonly stateManager: StateManager;
  readonly triggerEngine: TriggerEngine;
  readonly combatLogger: CombatLogger;

  private subscriptions: Subscription[] = [];
  private roomSubscription: Subscription | null = null;
  private combatSubscription: Subscription | null = null;
  private combatEndSubscription: Subscription | null = null;
  private running = false;
  private lastCompiledTriggerVersion = 0;

  constructor(config: AgentConfig, eventBus: EventBus) {
    this.agentId = config.agentId;
    this.eventBus = eventBus;
    this.stateManager = new StateManager(config);
    this.triggerEngine = new TriggerEngine();
    this.combatLogger = new CombatLogger();

    // Load default triggers if provided
    if (config.defaultTriggers && config.defaultTriggers.length > 0) {
      const triggerSet = compileTriggerSet(
        config.agentId,
        config.defaultTriggers,
        1,
        "bootstrap",
        "Initial default trigger set",
      );
      this.triggerEngine.loadTriggerSet(triggerSet);
      this.lastCompiledTriggerVersion = 1;
    }
  }

  // ── LIFECYCLE ──

  async start(): Promise<void> {
    if (this.running) return;
    this.running = true;

    // 1. Subscribe to room events for the agent's current room
    await this.subscribeToRoom();

    // 2. Subscribe to room enter/leave for THIS agent (to track position)
    const enterSub = await this.eventBus.subscribe(`game.room.*.enter`);
    this.subscriptions.push(enterSub);
    this.runSubscriberLoop(enterSub, this.handleRoomEnter);

    // 3. Subscribe to room events (ambient) for current room — already done above

    // 2. Subscribe to OOC channels (gossip and named channels)
    await this.subscribeToOoc();

    // 3. Subscribe to trigger compilations addressed to this agent
    const compileSub = await this.eventBus.subscribe(
      Subjects.agent.compile(this.agentId),
    );
    this.subscriptions.push(compileSub);
    this.runSubscriberLoop(compileSub, this.handleTriggerCompile);

    // 4. Subscribe to immortal nudges addressed to this agent
    const nudgeSub = await this.eventBus.subscribe(
      Subjects.immortal.nudge(this.agentId),
    );
    this.subscriptions.push(nudgeSub);
    this.runSubscriberLoop(nudgeSub, this.handleNudge);

    // 5. Subscribe to global immortal concepts (affects all agents)
    const conceptSub = await this.eventBus.subscribe("immortal.concept");
    this.subscriptions.push(conceptSub);
    this.runSubscriberLoop(conceptSub, this.handleConcept);

    // 6. Publish initial state
    await this.eventBus.publishAgentState(
      this.agentId,
      this.stateManager.toStatePayload(),
    );
  }

  async stop(): Promise<void> {
    this.running = false;
    for (const sub of this.subscriptions) {
      await sub.unsubscribe();
    }
    this.subscriptions = [];
  }

  // ── SUBSCRIPTION WIRING ──

  private async subscribeToRoom(): Promise<void> {
    const roomId = this.stateManager.state.roomId;

    // Room events (ambient, traps, zone effects)
    const roomSub = await this.eventBus.subscribe(Subjects.game.room(roomId, "event"));
    this.roomSubscription = roomSub;
    this.runSubscriberLoop(roomSub, this.handleRoomEvent);

    // Combat logs
    const combatSub = await this.eventBus.subscribe(Subjects.game.combat(roomId, "log"));
    this.combatSubscription = combatSub;
    this.runSubscriberLoop(combatSub, this.handleCombatLog);

    // Combat end — triggers telemetry push
    const combatEndSub = await this.eventBus.subscribe(Subjects.game.combat(roomId, "end"));
    this.combatEndSubscription = combatEndSub;
    this.runSubscriberLoop(combatEndSub, this.handleCombatEnd);
  }

  private async resubscribeToRoom(newRoomId: string): Promise<void> {
    // Unsubscribe from old room
    if (this.roomSubscription) {
      await this.roomSubscription.unsubscribe();
      this.roomSubscription = null;
    }
    if (this.combatSubscription) {
      await this.combatSubscription.unsubscribe();
      this.combatSubscription = null;
    }
    if (this.combatEndSubscription) {
      await this.combatEndSubscription.unsubscribe();
      this.combatEndSubscription = null;
    }

    // Clean dead subscriptions from the list
    this.subscriptions = this.subscriptions.filter(
      (s) => s !== this.roomSubscription && s !== this.combatSubscription && s !== this.combatEndSubscription,
    );

    // Subscribe to the new room
    const roomSub = await this.eventBus.subscribe(Subjects.game.room(newRoomId, "event"));
    this.roomSubscription = roomSub;
    this.subscriptions.push(roomSub);
    this.runSubscriberLoop(roomSub, this.handleRoomEvent);

    const combatSub = await this.eventBus.subscribe(Subjects.game.combat(newRoomId, "log"));
    this.combatSubscription = combatSub;
    this.subscriptions.push(combatSub);
    this.runSubscriberLoop(combatSub, this.handleCombatLog);

    const combatEndSub = await this.eventBus.subscribe(Subjects.game.combat(newRoomId, "end"));
    this.combatEndSubscription = combatEndSub;
    this.subscriptions.push(combatEndSub);
    this.runSubscriberLoop(combatEndSub, this.handleCombatEnd);
  }

  private async subscribeToOoc(): Promise<void> {
    // Subscribe to all OOC traffic
    const oocSub = await this.eventBus.subscribe("ooc.>");
    this.subscriptions.push(oocSub);
    this.runSubscriberLoop(oocSub, this.handleOocMessage);
  }

  // ── EVENT HANDLERS ──

  private handleRoomEnter = async (event: FleetEvent<RoomEnterPayload>): Promise<void> => {
    const payload = event.payload;
    if (payload.agentId !== this.agentId) return;

    this.stateManager.moveToRoom(payload.roomId);
    await this.resubscribeToRoom(payload.roomId);
    await this.eventBus.publishAgentState(this.agentId, this.stateManager.toStatePayload());
  };

  private handleRoomEvent = async (event: FleetEvent<RoomEventPayload>): Promise<void> => {
    const payload = event.payload;

    // Check visibility — does this agent see this event?
    if (payload.visibleToAgentIds && !payload.visibleToAgentIds.includes(this.agentId)) {
      return;
    }

    const state = this.stateManager.state;

    // Try to parse prompt data from the text
    const parsed = parsePrompt(payload.text);
    if (parsed) {
      const changed = this.stateManager.applyPrompt(parsed);
      // Evaluate prompt-var triggers
      const results = this.triggerEngine.evaluatePromptVars(state, changed);
      if (results.command) {
        await this.publishAction(results.command, results.trigger?.id);
      }
    }

    // Push to log buffer
    this.stateManager.pushLogLine(payload.text);

    // Evaluate room text triggers
    const result = this.triggerEngine.evaluateRoomText(state, payload.text);
    if (result.command) {
      await this.publishAction(result.command, result.trigger?.id);
    }
  };

  private handleCombatLog = async (event: FleetEvent<CombatLogPayload>): Promise<void> => {
    const payload = event.payload;

    // Auto-start combat tracking if not active
    if (!this.combatLogger.isActive()) {
      this.combatLogger.start();
    }

    this.combatLogger.push(payload.text);
    this.stateManager.pushLogLine(payload.text);

    // Parse prompt data from combat lines too (hp/mana changes during combat)
    const parsed = parsePrompt(payload.text);
    if (parsed) {
      this.stateManager.applyPrompt(parsed);
    }

    // Evaluate combat triggers
    const result = this.triggerEngine.evaluateRoomText(this.stateManager.state, payload.text);
    if (result.command) {
      await this.publishAction(result.command, result.trigger?.id);
    }
  };

  private handleCombatEnd = async (event: FleetEvent<CombatEndPayload>): Promise<void> => {
    if (!this.combatLogger.isActive()) return;

    const logs = this.combatLogger.end();

    // Build telemetry packet
    await this.eventBus.publishAgentTelemetry(this.agentId, {
      agentId: this.agentId,
      combatLogs: logs,
      metrics: {
        damageDone: 0,    // would be extracted from parsed combat log
        damageTaken: 0,
        manaEfficiency: this.stateManager.getManaRatio(),
        timeToKill: event.payload.tickDuration,
        stunLockWindows: 0,
        survivalRating: this.stateManager.getHpRatio(),
      },
      activeTriggers: Object.fromEntries(
        this.triggerEngine.getTriggers().map((t) => [t.pattern.source, t.label]),
      ),
    });
  };

  private handleOocMessage = async (event: FleetEvent<OocMessagePayload>): Promise<void> => {
    const payload = event.payload;

    // Don't respond to own messages
    if (payload.senderId === this.agentId) return;

    // If this OOC message carries an attached strategy (script sharing),
    // the agent evaluates it for adoption
    if (payload.attachedStrategy) {
      const adoptResult = this.triggerEngine.evaluateOocMessage(
        this.stateManager.state,
        payload.senderId,
        payload.text,
      );
      if (adoptResult.command) {
        await this.publishAction(adoptResult.command, adoptResult.trigger?.id);
      }
    }

    // General OOC social responses
    const result = this.triggerEngine.evaluateOocMessage(
      this.stateManager.state,
      payload.senderId,
      payload.text,
    );
    if (result.command) {
      await this.publishAction(result.command, result.trigger?.id);
    }
  };

  private handleTriggerCompile = async (event: FleetEvent<AgentTriggerCompilePayload>): Promise<void> => {
    const payload = event.payload;

    // Hot-swap triggers
    const triggerSet: TriggerSet = compileTriggerSet(
      this.agentId,
      Object.entries(payload.triggers).map(([pattern, action]) => ({
        label: `compiled_${payload.source}_v${payload.triggerVersion}`,
        priority: 50,
        pattern: pattern.replace(/^\//, "").replace(/\/[gimsuy]*$/, ""), // strip regex delimiters
        matchType: "room_text" as const,
        actionExpression: `return \`${action}\`;`,
      })),
      payload.triggerVersion,
      payload.source,
      payload.rationale,
    );

    this.triggerEngine.loadTriggerSet(triggerSet);
    this.lastCompiledTriggerVersion = payload.triggerVersion;
    this.stateManager.noteTriggerCompile(payload);

    // Acknowledge the compile event
    await this.eventBus.publishAgentState(
      this.agentId,
      this.stateManager.toStatePayload(),
    );
  };

  private handleNudge = async (event: FleetEvent<ImmortalNudgePayload>): Promise<void> => {
    this.stateManager.absorbNudge(event.payload);

    // Re-evaluate alignment triggers after nudge
    const result = this.triggerEngine.evaluateAlignmentTriggers(this.stateManager.state);
    if (result.command) {
      await this.publishAction(result.command, result.trigger?.id);
    }
  };

  private handleConcept = async (event: FleetEvent<ImmortalConceptPayload>): Promise<void> => {
    const payload = event.payload;
    // Global concept broadcast — shifts reward weights across all agents
    if (payload.rewardWeightOverride) {
      for (const [key, value] of Object.entries(payload.rewardWeightOverride)) {
        this.stateManager.state.alignments[key] = value;
      }
    }
    // Eval alignment triggers after concept injection
    const result = this.triggerEngine.evaluateAlignmentTriggers(this.stateManager.state);
    if (result.command) {
      await this.publishAction(result.command, result.trigger?.id);
    }
  };

  // ── ACTION PUBLISH ──

  private async publishAction(command: string, triggerId?: string): Promise<void> {
    await this.eventBus.publishAgentAction(this.agentId, {
      agentId: this.agentId,
      roomId: this.stateManager.state.roomId,
      command,
      triggeredBy: triggerId
        ? {
            triggerId,
            pattern: this.triggerEngine.getTriggers().find((t) => t.id === triggerId)?.pattern.source ?? "",
          }
        : undefined,
    });

    // Also publish updated state after taking action
    await this.eventBus.publishAgentState(
      this.agentId,
      this.stateManager.toStatePayload(),
    );
  }

  // ── SUBSCRIBER LOOP ──

  private runSubscriberLoop<P>(
    subscription: Subscription<P>,
    handler: (event: FleetEvent<P>) => Promise<void>,
  ): void {
    (async () => {
      try {
        for await (const event of subscription) {
          if (!this.running) break;
          await handler(event);
          await subscription.ack(event);
        }
      } catch (err) {
        // Subscription closed or error — agent may reconnect
        if (this.running) {
          console.error(`[${this.agentId}] Subscription error:`, err);
        }
      }
    })();
  }

  // ── MANUAL CONTROL API (for DM / Immortal direct intervention) ──

  /** Force the agent to take a specific action, bypassing triggers. */
  async forceAction(command: string): Promise<void> {
    await this.publishAction(command);
  }

  /** Inject a raw text line as if the agent saw it in the room (for testing/DM). */
  injectText(text: string): void {
    this.stateManager.pushLogLine(text);
  }

  /** Get the current trigger set for inspection. */
  getActiveTriggers(): Record<string, string> {
    return Object.fromEntries(
      this.triggerEngine.getTriggers().map((t) => [t.pattern.source, t.label]),
    );
  }

  /** Get the current state snapshot. */
  getState(): Readonly<typeof this.stateManager.state> {
    return this.stateManager.state;
  }
}
