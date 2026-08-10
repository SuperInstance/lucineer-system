// ============================================================
// @fleet/immortal-interface — IMMORTAL CONSOLE
// The god console. Subscribes to everything, views the waveform
// of emergent behavior, and nudges without micromanaging.
// ============================================================

import { EventBus, type FleetEvent, Subjects } from "@fleet/event-bus";
import { Subscription } from "@fleet/event-bus";
import {
  type AgentActionPayload,
  type AgentStatePayload,
  type AgentTelemetryPayload,
  type CombatLogPayload,
  type CombatEndPayload,
  type OocMessagePayload,
  type DmDesignIntentPayload,
  type DmZoneManipulationPayload,
  type StrategyLineagePayload,
  type ImmortalNudgePayload,
  type ImmortalConceptPayload,
} from "@fleet/event-bus";

import { WaveformCompositor } from "./waveform-compositor";
import type {
  ImmortalState,
  AgentDashboardCard,
  ZoneWaveform,
  StrategyNode,
  GossipEntry,
  NudgeRecord,
} from "./immortal-types";

// -------------------------------------------------------------------
// IMMORTAL CONSOLE
// -------------------------------------------------------------------

export class ImmortalConsole {
  readonly immortalId: string;
  readonly eventBus: EventBus;
  readonly compositor: WaveformCompositor;

  private subscriptions: Subscription[] = [];
  private running = false;
  private nudgeHistory: NudgeRecord[] = [];
  private onNudgeCallbacks: Array<(nudge: NudgeRecord) => void> = [];
  private onGossipCallbacks: Array<(entry: GossipEntry) => void> = [];
  private onWaveformUpdateCallbacks: Array<(waveform: ZoneWaveform) => void> = [];
  private onStrategyCallbacks: Array<(node: StrategyNode) => void> = [];
  private dashboardUpdateCallbacks: Array<(cards: AgentDashboardCard[]) => void> = [];

  /** Polling interval for waveform composition (ms). */
  private waveformInterval: ReturnType<typeof setInterval> | null = null;

  constructor(immortalId: string, eventBus: EventBus) {
    this.immortalId = immortalId;
    this.eventBus = eventBus;
    this.compositor = new WaveformCompositor();
  }

  // ── LIFECYCLE ──

  async start(waveformIntervalMs = 1000): Promise<void> {
    if (this.running) return;
    this.running = true;

    // Subscribe to everything — the immortal sees all

    // All agent actions
    const actionSub = await this.eventBus.subscribe("agent.*.action");
    this.subscriptions.push(actionSub);
    this.runSubscriberLoop(actionSub, this.handleAgentAction);

    // All agent state updates
    const stateSub = await this.eventBus.subscribe("agent.*.state");
    this.subscriptions.push(stateSub);
    this.runSubscriberLoop(stateSub, this.handleAgentState);

    // All agent telemetry
    const telemetrySub = await this.eventBus.subscribe("agent.*.telemetry");
    this.subscriptions.push(telemetrySub);
    this.runSubscriberLoop(telemetrySub, this.handleAgentTelemetry);

    // All combat logs
    const combatSub = await this.eventBus.subscribe("game.combat.*.log");
    this.subscriptions.push(combatSub);
    this.runSubscriberLoop(combatSub, this.handleCombatLog);

    // All combat ends
    const combatEndSub = await this.eventBus.subscribe("game.combat.*.end");
    this.subscriptions.push(combatEndSub);
    this.runSubscriberLoop(combatEndSub, this.handleCombatEnd);

    // All OOC
    const oocSub = await this.eventBus.subscribe("ooc.>");
    this.subscriptions.push(oocSub);
    this.runSubscriberLoop(oocSub, this.handleOoc);

    // DM design intentions (visible on the immortal dashboard)
    const dmDesignSub = await this.eventBus.subscribe("dm.*.design_intent");
    this.subscriptions.push(dmDesignSub);
    this.runSubscriberLoop(dmDesignSub, this.handleDesignIntent);

    // DM zone manipulations (the immortal sees what traps the DM is laying)
    const dmZoneSub = await this.eventBus.subscribe("dm.*.zone_manipulation");
    this.subscriptions.push(dmZoneSub);
    this.runSubscriberLoop(dmZoneSub, this.handleDmZone);

    // Strategy lineage
    const lineageSub = await this.eventBus.subscribe("meta.lineage.*");
    this.subscriptions.push(lineageSub);
    this.runSubscriberLoop(lineageSub, this.handleStrategyLineage);

    // Waveform composition poll
    this.waveformInterval = setInterval(() => {
      const waveform = this.compositor.composeZoneWaveform("world");
      for (const cb of this.onWaveformUpdateCallbacks) {
        cb(waveform);
      }
    }, waveformIntervalMs);
  }

  async stop(): Promise<void> {
    this.running = false;
    if (this.waveformInterval) {
      clearInterval(this.waveformInterval);
      this.waveformInterval = null;
    }
    for (const sub of this.subscriptions) {
      await sub.unsubscribe();
    }
    this.subscriptions = [];
  }

  // ── NUKE BUTTONS (Immortal Actions) ──

  /**
   * Inject a concept into a single agent's context.
   * "A strange premonition tells you the dragon is immune to fire."
   * This alters the agent's prompt weighting / trigger evaluation.
   */
  async nudgeAgent(
    targetAgentId: string,
    concept: string,
    weight: number = 0.5,
  ): Promise<void> {
    const payload: ImmortalNudgePayload = {
      immortalId: this.immortalId,
      targetAgentId,
      concept,
      weight: Math.min(1, Math.max(0, weight)),
      scope: "single",
    };

    await this.eventBus.publishImmortalNudge(targetAgentId, payload);

    this.nudgeHistory.push({
      timestamp: Date.now(),
      immortalId: this.immortalId,
      targetAgentId,
      concept,
      weight,
    });

    for (const cb of this.onNudgeCallbacks) {
      cb(this.nudgeHistory[this.nudgeHistory.length - 1]!);
    }
  }

  /**
   * Broadcast a concept to all agents simultaneously.
   * "The gods whisper that efficiency is a trap; true honor belongs to
   *  those who survive on the edge of death."
   * This shifts reward weights across all agent architectures at once.
   */
  async broadcastConcept(
    concept: string,
    rewardWeightOverride?: Record<string, number>,
  ): Promise<void> {
    const payload: ImmortalConceptPayload = {
      immortalId: this.immortalId,
      concept,
      rewardWeightOverride,
    };

    await this.eventBus.publishImmortalConcept(payload);
  }

  /**
   * Nudge the current DM. Inject design constraints.
   * "Remember that a good story requires hope; insert a hidden room
   *  with a hint about the slime's weakness."
   */
  async nudgeDM(concept: string): Promise<void> {
    // Get current DM
    const cards = this.compositor.getAgentCards();
    const dm = cards.find((c) => c.role === "dm");
    if (dm) {
      await this.nudgeAgent(dm.agentId, `[DM NUDGE] ${concept}`, 1.0);
    }
  }

  /**
   * Inject a trigger compilation directly into an agent.
   * Force an agent to adopt a specific trigger pattern.
   */
  async injectTriggerCompile(
    agentId: string,
    triggers: Record<string, string>,
    rationale: string,
  ): Promise<void> {
    await this.eventBus.publishAgentTriggerCompile(agentId, {
      agentId,
      source: "immortal",
      triggers,
      rationale,
      triggerVersion: Date.now(),
    });
  }

  // ── QUERIES ──

  getAgentCards(): AgentDashboardCard[] {
    return this.compositor.getAgentCards();
  }

  getAgentCard(agentId: string): AgentDashboardCard | undefined {
    return this.compositor.getAgentCard(agentId);
  }

  getWaveform(zoneId = "world"): ZoneWaveform {
    return this.compositor.composeZoneWaveform(zoneId);
  }

  getStrategyGraph(): StrategyNode[] {
    return this.compositor.getStrategyGraph();
  }

  getStrategyLineage(strategyId: string): StrategyNode[] {
    return this.compositor.getStrategyLineage(strategyId);
  }

  getGossipFeed(limit = 50): GossipEntry[] {
    return this.compositor.getGossipFeed(limit);
  }

  getNudgeHistory(): NudgeRecord[] {
    return [...this.nudgeHistory];
  }

  // ── SUBSCRIPTION CALLBACKS (for UI binding) ──

  onNudge(cb: (nudge: NudgeRecord) => void): () => void {
    this.onNudgeCallbacks.push(cb);
    return () => {
      this.onNudgeCallbacks = this.onNudgeCallbacks.filter((c) => c !== cb);
    };
  }

  onGossip(cb: (entry: GossipEntry) => void): () => void {
    this.onGossipCallbacks.push(cb);
    return () => {
      this.onGossipCallbacks = this.onGossipCallbacks.filter((c) => c !== cb);
    };
  }

  onWaveformUpdate(cb: (waveform: ZoneWaveform) => void): () => void {
    this.onWaveformUpdateCallbacks.push(cb);
    return () => {
      this.onWaveformUpdateCallbacks = this.onWaveformUpdateCallbacks.filter((c) => c !== cb);
    };
  }

  onStrategyEvolved(cb: (node: StrategyNode) => void): () => void {
    this.onStrategyCallbacks.push(cb);
    return () => {
      this.onStrategyCallbacks = this.onStrategyCallbacks.filter((c) => c !== cb);
    };
  }

  onDashboardUpdate(cb: (cards: AgentDashboardCard[]) => void): () => void {
    this.dashboardUpdateCallbacks.push(cb);
    return () => {
      this.dashboardUpdateCallbacks = this.dashboardUpdateCallbacks.filter((c) => c !== cb);
    };
  }

  // ── EVENT HANDLERS ──

  private handleAgentAction = async (event: FleetEvent<AgentActionPayload>): Promise<void> => {
    this.compositor.ingestAgentAction(event);
  };

  private handleAgentState = async (event: FleetEvent<AgentStatePayload>): Promise<void> => {
    this.compositor.ingestAgentState(event);
  };

  private handleAgentTelemetry = async (event: FleetEvent<AgentTelemetryPayload>): Promise<void> => {
    this.compositor.ingestAgentTelemetry(event);
  };

  private handleCombatLog = async (event: FleetEvent<CombatLogPayload>): Promise<void> => {
    this.compositor.ingestCombatLog(event);
  };

  private handleCombatEnd = async (event: FleetEvent<CombatEndPayload>): Promise<void> => {
    this.compositor.ingestCombatEnd(event);
  };

  private handleOoc = async (event: FleetEvent<OocMessagePayload>): Promise<void> => {
    this.compositor.ingestOoc(event);
    const entry: GossipEntry = {
      timestamp: event.timestamp,
      senderId: event.payload.senderId,
      channelId: event.payload.channelId,
      text: event.payload.text,
      carriedStrategyId: event.payload.attachedStrategy?.strategyId,
    };
    for (const cb of this.onGossipCallbacks) {
      cb(entry);
    }
  };

  private handleDesignIntent = async (event: FleetEvent<DmDesignIntentPayload>): Promise<void> => {
    this.compositor.ingestDesignIntent(event);
  };

  private handleDmZone = async (_event: FleetEvent<DmZoneManipulationPayload>): Promise<void> => {
    // Zone manipulations are logged for the dashboard
  };

  private handleStrategyLineage = async (event: FleetEvent<StrategyLineagePayload>): Promise<void> => {
    this.compositor.ingestStrategyLineage(event);
    const node = this.compositor.getStrategyGraph().find(
      (n) => n.strategyId === event.payload.strategyId,
    );
    if (node) {
      for (const cb of this.onStrategyCallbacks) {
        cb(node);
      }
    }
  };

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
      } catch {
        // Subscription closed
      }
    })();
  }
}
