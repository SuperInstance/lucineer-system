// ============================================================
// @fleet/event-bus — Transport Abstraction & EventBus
// ============================================================

import {
  type FleetEvent,
  type EventId,
  type EventSeq,
  type Subject,
  type EpochMs,
  type SubjectPayloadMap,
} from "./types";

// -------------------------------------------------------------------
// TRANSPORT INTERFACE — pluggable backends
// -------------------------------------------------------------------

export interface Transport {
  /** Connect to the transport. Returns a client handle. */
  connect(): Promise<void>;
  /** Disconnect. */
  close(): Promise<void>;
  /** Publish an event to a subject. Returns the assigned sequence number. */
  publish<P>(subject: Subject, event: FleetEvent<P>): Promise<EventSeq>;
  /**
   * Subscribe to a subject pattern (supports wildcards: `*` for single token, `>` for rest).
   * Returns an async iterable or a subscription handle.
   */
  subscribe<P>(
    subjectPattern: Subject,
    options?: SubscriptionOptions,
  ): Promise<Subscription<P>>;
  /**
   * Request/reply pattern: publish and expect exactly one response.
   */
  request<P, R>(subject: Subject, payload: P, timeoutMs?: number): Promise<FleetEvent<R>>;
}

export interface SubscriptionOptions {
  /** Only deliver events with sequence > this. */
  startSequence?: EventSeq;
  /** Maximum in-flight unacknowledged messages. */
  maxInFlight?: number;
  /** For persistent streams: replay all historical events then go live. */
  replayAll?: boolean;
}

export interface Subscription<P = unknown> extends AsyncIterable<FleetEvent<P>> {
  /** Pull next event, optionally with a timeout. */
  next(timeoutMs?: number): Promise<IteratorResult<FleetEvent<P>>>;
  /** Acknowledge processing (needed for persistent/at-least-once transports). */
  ack(event: FleetEvent<P>): Promise<void>;
  /** Unsubscribe. */
  unsubscribe(): Promise<void>;
}

// ============================================================
// MEMORY TRANSPORT — in-process for development and testing
// ============================================================

interface MemorySubscriber<P = unknown> {
  pattern: Subject;
  callback: (event: FleetEvent<P>) => void;
  filter?: (event: FleetEvent<P>) => boolean;
}

export class MemoryTransport implements Transport {
  private subscribers: MemorySubscriber[] = [];
  private sequences: Map<Subject, EventSeq> = new Map();
  private persistentLog: FleetEvent[] = [];
  private seqCounter = 0;

  async connect(): Promise<void> {
    // no-op: always connected
  }

  async close(): Promise<void> {
    this.subscribers = [];
  }

  async publish<P>(subject: Subject, event: FleetEvent<P>): Promise<EventSeq> {
    this.seqCounter++;
    const seq = this.seqCounter;
    const fullEvent = { ...event, sequence: seq } as FleetEvent<P>;

    // Append to persistent log for replay
    this.persistentLog.push(fullEvent as FleetEvent);

    // Fan out to matching subscribers
    for (const sub of this.subscribers) {
      if (this.subjectMatches(sub.pattern, subject)) {
        if (!sub.filter || sub.filter(fullEvent as FleetEvent<P>)) {
          sub.callback(fullEvent as FleetEvent<P>);
        }
      }
    }

    this.sequences.set(subject, seq);
    return seq;
  }

  subscribe<P>(
    subjectPattern: Subject,
    options: SubscriptionOptions = {},
  ): Promise<Subscription<P>> {
    const events: FleetEvent<P>[] = [];
    let wakeup: (() => void) | null = null;
    let closed = false;

    // Replay historical events if requested
    if (options.replayAll || options.startSequence !== undefined) {
      for (const ev of this.persistentLog) {
        const seq = (ev as FleetEvent).sequence ?? 0;
        const passesStart = options.startSequence === undefined || seq > options.startSequence;
        if (passesStart && this.subjectMatches(subjectPattern, ev.subject)) {
          events.push(ev as FleetEvent<P>);
        }
      }
    }

    const callback = (event: FleetEvent<P>) => {
      events.push(event);
      if (wakeup) {
        wakeup();
        wakeup = null;
      }
    };

    const sub: MemorySubscriber<P> = {
      pattern: subjectPattern,
      callback,
    };

    this.subscribers.push(sub as MemorySubscriber);

    const subscription: Subscription<P> = {
      [Symbol.asyncIterator](): AsyncIterator<FleetEvent<P>> {
        return this as unknown as AsyncIterator<FleetEvent<P>>;
      },
      async next(): Promise<IteratorResult<FleetEvent<P>>> {
        while (true) {
          if (closed) return { value: undefined, done: true };
          const ev = events.shift();
          if (ev) return { value: ev, done: false };
          await new Promise<void>((resolve) => {
            wakeup = resolve;
          });
        }
      },
      ack: async (_event: FleetEvent<P>) => {
        // Memory transport: ack is a no-op
      },
      unsubscribe: async () => {
        closed = true;
        this.subscribers = this.subscribers.filter((s) => s !== (sub as MemorySubscriber));
        if (wakeup) {
          wakeup();
          wakeup = null;
        }
      },
    };

    return Promise.resolve(subscription);
  }

  async request<P, R>(_subject: Subject, _payload: P, _timeoutMs?: number): Promise<FleetEvent<R>> {
    throw new Error("Request/reply not implemented in MemoryTransport");
  }

  // ── Wildcard matching ──
  private subjectMatches(pattern: Subject, subject: Subject): boolean {
    const patTokens = pattern.split(".");
    const subTokens = subject.split(".");

    for (let i = 0; i < patTokens.length; i++) {
      const p = patTokens[i]!;
      if (p === ">") return true; // matches rest
      if (p === "*") {
        if (i >= subTokens.length) return false;
        continue; // wildcard matches exactly one token
      }
      if (i >= subTokens.length) return false;
      if (p !== subTokens[i]) return false;
    }

    return patTokens.length === subTokens.length;
  }
}

// ============================================================
// EVENT BUS — the main API
// ============================================================

export interface EventBusConfig {
  transport: Transport;
  publisherId: string;
}

export class EventBus {
  private transport: Transport;
  private publisherId: string;
  private localSeq = 0;
  private streams: Set<Subject> = new Set();

  constructor(config: EventBusConfig) {
    this.transport = config.transport;
    this.publisherId = config.publisherId;
  }

  // ── PUBLISH ──

  async publish<P>(
    subject: Subject,
    payload: P,
    causation: EventId[] = [],
    correlationId?: string,
  ): Promise<EventSeq> {
    this.localSeq++;

    const event: FleetEvent<P> = {
      id: `${this.publisherId}:${this.localSeq}`,
      subject,
      timestamp: Date.now() as EpochMs,
      publisher: this.publisherId,
      sequence: this.localSeq,
      payload,
      causation,
      correlationId,
    };

    return this.transport.publish(subject, event);
  }

  // ── SUBSCRIBE (typed by subject pattern) ──

  async subscribe<S extends Subject>(
    subjectPattern: S,
    options?: SubscriptionOptions,
  ): Promise<Subscription> {
    return this.transport.subscribe(subjectPattern, options);
  }

  /**
   * Subscribe to all events matching a prefix (e.g. `agent.*.>` for everything from all agents).
   * Returns an async iterable that yields every FleetEvent on the pattern.
   */
  async subscribeAll(
    subjectPattern: Subject,
    options?: SubscriptionOptions,
  ): Promise<Subscription> {
    return this.transport.subscribe(subjectPattern, options);
  }

  // ── STREAM MANAGEMENT (persistent log) ──

  /**
   * Declare a persistent stream. Events published to matching subjects
   * are retained on the transport for replay by late-joining subscribers.
   * On MemoryTransport this is always active; on NATS this creates a JetStream stream.
   */
  declareStream(subjectPattern: Subject): void {
    this.streams.add(subjectPattern);
  }

  // ── CONVENIENCE PUBLISHERS (domain-specific) ──

  async publishGameTick(payload: import("./types").GameTickPayload): Promise<EventSeq> {
    return this.publish("game.tick", payload);
  }

  async publishRoomEvent(roomId: string, payload: import("./types").RoomEventPayload): Promise<EventSeq> {
    return this.publish(`game.room.${roomId}.event`, payload);
  }

  async publishCombatLog(roomId: string, payload: import("./types").CombatLogPayload): Promise<EventSeq> {
    return this.publish(`game.combat.${roomId}.log`, payload);
  }

  async publishCombatEnd(roomId: string, payload: import("./types").CombatEndPayload): Promise<EventSeq> {
    return this.publish(`game.combat.${roomId}.end`, payload);
  }

  async publishAgentAction(agentId: string, payload: import("./types").AgentActionPayload): Promise<EventSeq> {
    return this.publish(`agent.${agentId}.action`, payload);
  }

  async publishAgentState(agentId: string, payload: import("./types").AgentStatePayload): Promise<EventSeq> {
    return this.publish(`agent.${agentId}.state`, payload);
  }

  async publishAgentTelemetry(agentId: string, payload: import("./types").AgentTelemetryPayload): Promise<EventSeq> {
    return this.publish(`agent.${agentId}.telemetry`, payload);
  }

  async publishAgentTriggerCompile(agentId: string, payload: import("./types").AgentTriggerCompilePayload): Promise<EventSeq> {
    return this.publish(`agent.${agentId}.trigger.compile`, payload);
  }

  async publishOoc(channelId: string, payload: import("./types").OocMessagePayload): Promise<EventSeq> {
    return this.publish(`ooc.channel.${channelId}`, payload);
  }

  async publishDmZoneManipulation(dmId: string, payload: import("./types").DmZoneManipulationPayload): Promise<EventSeq> {
    return this.publish(`dm.${dmId}.zone_manipulation`, payload);
  }

  async publishDmDesignIntent(dmId: string, payload: import("./types").DmDesignIntentPayload): Promise<EventSeq> {
    return this.publish(`dm.${dmId}.design_intent`, payload);
  }

  async publishImmortalNudge(agentId: string, payload: import("./types").ImmortalNudgePayload): Promise<EventSeq> {
    return this.publish(`immortal.nudge.${agentId}`, payload);
  }

  async publishImmortalConcept(payload: import("./types").ImmortalConceptPayload): Promise<EventSeq> {
    return this.publish("immortal.concept", payload);
  }

  async publishStrategyLineage(strategyId: string, payload: import("./types").StrategyLineagePayload): Promise<EventSeq> {
    return this.publish(`meta.lineage.${strategyId}`, payload);
  }

  // ── ACCESSORS ──

  get id(): string {
    return this.publisherId;
  }

  get transport(): Transport {
    return this.transport;
  }
}

// ============================================================
// FACTORY
// ============================================================

export function createMemoryEventBus(publisherId: string): EventBus {
  return new EventBus({
    transport: new MemoryTransport(),
    publisherId,
  });
}
