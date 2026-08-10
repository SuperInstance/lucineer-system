// ============================================================
// @fleet/mud-engine — FULL SYSTEM COMPOSITION
// Wires the Event Bus, Agent Runtime, and Immortal Interface
// together into a complete MUD simulation mesh.
//
// This is the "executive" — it brings the MUD world, the agents,
// and the immortal console into a single running process.
// ============================================================

import {
  EventBus,
  createMemoryEventBus,
  Subjects,
  MemoryTransport,
} from "@fleet/event-bus";

import { AgentRuntime, type AgentConfig } from "@fleet/agent-runtime";
import { ImmortalConsole } from "@fleet/immortal-interface";

// ============================================================
// MUD ENGINE — simulated room/game world
// ============================================================

interface Room {
  id: string;
  name: string;
  description: string;
  exits: Record<string, string>; // direction -> target room id
  occupants: Set<string>;
  ambientText: string[];
  zoneId: string;
}

interface MobSpawn {
  mobId: string;
  roomId: string;
  name: string;
  hp: number;
  maxHp: number;
  attackDps: number;
  attackInterval: number; // ticks between attacks
  lastAttackTick: number;
}

class MudEngine {
  private eventBus: EventBus;
  private rooms: Map<string, Room> = new Map();
  private mobs: Map<string, MobSpawn> = new Map();
  private tickNumber = 0;
  private tickInterval: ReturnType<typeof setInterval> | null = null;

  constructor(eventBus: EventBus) {
    this.eventBus = eventBus;
  }

  registerRoom(room: Room): void {
    this.rooms.set(room.id, room);
  }

  spawnMob(mob: MobSpawn): void {
    this.mobs.set(mob.mobId, mob);
    const room = this.rooms.get(mob.roomId);
    if (room) {
      this.eventBus.publishRoomEvent(room.id, {
        roomId: room.id,
        text: `A ${mob.name} materializes from the shadows!`,
        category: "spawn",
      });
    }
  }

  start(tickMs = 250): void {
    this.tickInterval = setInterval(() => this.processTick(), tickMs);
  }

  stop(): void {
    if (this.tickInterval) clearInterval(this.tickInterval);
  }

  // ── Process incoming agent actions ──

  async processAgentAction(agentId: string, command: string, roomId: string): Promise<void> {
    const room = this.rooms.get(roomId);
    if (!room) return;

    // MOVEMENT
    const moveMatch = command.match(/^(north|south|east|west|up|down)$/i);
    if (moveMatch) {
      const dir = moveMatch[1]!.toLowerCase();
      const targetRoomId = room.exits[dir];
      if (targetRoomId) {
        const targetRoom = this.rooms.get(targetRoomId);
        if (targetRoom) {
          // Leave current room
          room.occupants.delete(agentId);
          this.eventBus.publish(Subjects.game.room(roomId, "leave"), {
            roomId,
            agentId,
            toRoomId: targetRoomId,
          });

          // Enter target room
          targetRoom.occupants.add(agentId);
          this.eventBus.publish(Subjects.game.room(targetRoomId, "enter"), {
            roomId: targetRoomId,
            agentId,
            fromRoomId: roomId,
          });
        }
      }
      return;
    }

    // SAY / OOC
    const sayMatch = command.match(/^say\s+(.+)/i);
    if (sayMatch) {
      const text = sayMatch[1]!.trim();
      this.eventBus.publishRoomEvent(roomId, {
        roomId,
        text: `${agentId} says: "${text}"`,
        category: "ambient",
      });
      return;
    }

    // CAST / COMBAT ACTION
    const castMatch = command.match(/^cast\s+(.+)/i);
    if (castMatch) {
      const spell = castMatch[1]!.trim();
      this.eventBus.publishRoomEvent(roomId, {
        roomId,
        text: `${agentId} intones arcane syllables and casts ${spell}!`,
        category: "ambient",
      });

      // Find a mob in the room to damage
      const roomMobs = Array.from(this.mobs.values()).filter((m) => m.roomId === roomId);
      if (roomMobs.length > 0) {
        const target = roomMobs[0]!;
        target.hp -= 25; // spell damage
        this.eventBus.publish(Subjects.game.combat(roomId, "log"), {
          roomId,
          text: `${agentId}'s ${spell} strikes ${target.name} for 25 damage! [${target.hp}/${target.maxHp}]`,
          dps: 25,
        });

        if (target.hp <= 0) {
          this.mobs.delete(target.mobId);
          this.eventBus.publishRoomEvent(roomId, {
            roomId,
            text: `${target.name} collapses, defeated!`,
            category: "ambient",
          });
          this.eventBus.publish(Subjects.game.combat(roomId, "end"), {
            roomId,
            participants: [agentId, target.mobId],
            victors: [agentId],
            fullLog: `Combat with ${target.name} ended.`,
            tickDuration: 10,
          });
        }
      } else {
        this.eventBus.publish(Subjects.game.combat(roomId, "log"), {
          roomId,
          text: `${agentId}'s ${spell} fizzles — no target in range!`,
          dps: 0,
        });
      }
      return;
    }

    // Default: echo unknown action
    this.eventBus.publishRoomEvent(roomId, {
      roomId,
      text: `${agentId} executes: ${command}`,
      category: "ambient",
    });
  }

  // ── TICK PROCESSING ──

  private processTick(): void {
    this.tickNumber++;

    // Publish global tick
    this.eventBus.publishGameTick({
      tickNumber: this.tickNumber,
      tickDurationMs: 250,
      activeRoomIds: Array.from(this.rooms.keys()),
      activeAgentIds: Array.from(
        new Set(
          Array.from(this.rooms.values()).flatMap((r) => Array.from(r.occupants)),
        ),
      ),
    });

    // Process mob attacks
    for (const [, mob] of this.mobs) {
      if (this.tickNumber - mob.lastAttackTick >= mob.attackInterval) {
        mob.lastAttackTick = this.tickNumber;
        const room = this.rooms.get(mob.roomId);
        if (room && room.occupants.size > 0) {
          // Attack a random occupant
          const occupants = Array.from(room.occupants);
          const target = occupants[Math.floor(Math.random() * occupants.length)]!;

          const damage = Math.floor(mob.attackDps * (0.75 + Math.random() * 0.5));
          this.eventBus.publish(Subjects.game.combat(mob.roomId, "log"), {
            roomId: mob.roomId,
            text: `${mob.name} attacks ${target} for ${damage} damage!`,
            dps: damage,
          });
        }
      }
    }

    // Emit ambient room text occasionally
    for (const [, room] of this.rooms) {
      if (room.ambientText.length > 0 && this.tickNumber % 4 === 0) {
        const ambient = room.ambientText[this.tickNumber % room.ambientText.length]!;
        this.eventBus.publishRoomEvent(room.id, {
          roomId: room.id,
          text: ambient,
          category: "ambient",
        });
      }
    }
  }
}

// ============================================================
// COMPOSE — bring everything together
// ============================================================

export interface ComposeConfig {
  rooms: Array<{
    id: string;
    name: string;
    description: string;
    exits: Record<string, string>;
    zoneId: string;
    ambientText?: string[];
  }>;
  agents: Array<AgentConfig>;
  mobs?: Array<{
    mobId: string;
    roomId: string;
    name: string;
    hp: number;
    attackDps: number;
    attackInterval?: number;
  }>;
  immortalId?: string;
}

export interface ComposeResult {
  eventBus: EventBus;
  engine: MudEngine;
  agents: AgentRuntime[];
  immortal: ImmortalConsole;
  stop: () => Promise<void>;
}

export async function composeFleet(config: ComposeConfig): Promise<ComposeResult> {
  // 1. Shared event bus
  const transport = new MemoryTransport();
  await transport.connect();

  const eventBus = new EventBus({
    transport,
    publisherId: "fleet-orchestrator",
  });

  // 2. MUD engine
  const engine = new MudEngine(eventBus);

  for (const roomDef of config.rooms) {
    engine.registerRoom({
      id: roomDef.id,
      name: roomDef.name,
      description: roomDef.description,
      exits: roomDef.exits,
      occupants: new Set(),
      zoneId: roomDef.zoneId,
      ambientText: roomDef.ambientText ?? [],
    });
  }

  // 3. Spawn agents
  const agents: AgentRuntime[] = [];
  for (const agentConfig of config.agents) {
    const agent = new AgentRuntime(agentConfig, eventBus);
    await agent.start();

    // Place agent in its starting room
    const room = (engine as any).rooms.get(agentConfig.startingRoom);
    if (room) {
      room.occupants.add(agentConfig.agentId);
    }

    agents.push(agent);
  }

  // 4. Spawn mobs
  if (config.mobs) {
    for (const mobDef of config.mobs) {
      engine.spawnMob({
        mobId: mobDef.mobId,
        roomId: mobDef.roomId,
        name: mobDef.name,
        hp: mobDef.hp,
        maxHp: mobDef.hp,
        attackDps: mobDef.attackDps,
        attackInterval: mobDef.attackInterval ?? 4, // attack every 4 ticks
        lastAttackTick: 0,
      });
    }
  }

  // 5. Immortal console
  const immortal = new ImmortalConsole(
    config.immortalId ?? "the-watcher",
    eventBus,
  );
  await immortal.start(500); // compose waveform every 500ms

  // 6. Wire agent actions into the MUD engine
  const actionSub = await eventBus.subscribe("agent.*.action");
  (async () => {
    try {
      for await (const event of actionSub) {
        const payload = event.payload as import("@fleet/event-bus").AgentActionPayload;
        await engine.processAgentAction(payload.agentId, payload.command, payload.roomId);
      }
    } catch {
      // subscription closed
    }
  })();

  // 7. Start the game tick
  engine.start(250);

  return {
    eventBus,
    engine,
    agents,
    immortal,
    stop: async () => {
      engine.stop();
      await immortal.stop();
      for (const agent of agents) {
        await agent.stop();
      }
      await transport.close();
    },
  };
}

// ============================================================
// WIRING DIAGRAM (for documentation)
// ============================================================

/**
 * The full data flow through the system:
 *
 *   ┌──────────────────────┐
 *   │     MUD ENGINE        │  publishes: game.tick, game.room.*.event,
 *   │   (MudEngine)         │             game.combat.*.log, game.combat.*.end
 *   └──────────┬───────────┘
 *              │
 *              ▼
 *   ┌──────────────────────────────────────────────┐
 *   │              EVENT BUS (MemoryTransport)      │
 *   │                                               │
 *   │  game.*  │  agent.*  │  ooc.*  │  dm.*  │ immortal.* │ meta.*  │
 *   └───┬──────────┬───────────┬─────────┬──────────┬──────────┬────────┘
 *       │          │           │         │          │          │
 *       ▼          ▼           ▼         ▼          ▼          ▼
 *   ┌────────┐┌────────┐┌─────────┐┌────────┐┌──────────┐┌──────────┐
 *   │ AGENT  ││ AGENT  ││ IMMORTAL││  OOC   ││STRATEGY  ││  AGENT   │
 *   │RUNTIME ││RUNTIME ││ CONSOLE ││CHANNELS││ LINEAGE  ││COMPILERS │
 *   │(Xenon) ││(Thor)  ││(The     ││        ││ TRACKER  ││ (MCP/LLM)│
 *   │        ││        ││ Watcher)││        ││          ││          │
 *   └───┬────┘└───┬────┘└────┬────┘└────────┘└──────────┘└────┬─────┘
 *       │         │          │                                │
 *       │  publish: agent.*.action, agent.*.state             │
 *       │         │          │                                │
 *       │         │  publish: immortal.nudge.*                │
 *       │         │          │  publish: agent.*.trigger.compile
 *       ▼         ▼          ▼          ▲
 *   ┌──────────────────────────────────────────────────┐
 *   │          BACK TO EVENT BUS (fan-in)               │
 *   └──────────────────────────────────────────────────┘
 *              │
 *              ▼ (MUD Engine consumes agent actions)
 *   ┌──────────────────────┐
 *   │   MUD ENGINE          │
 *   │   (processAgentAction)│
 *   └──────────────────────┘
 */
