import { composeFleet } from "../packages/engine/src/index";
import type { AgentConfig } from "../packages/agent-runtime/src/index";

const config: AgentConfig = {
  agentId: "test_agent",
  name: "Test",
  startingRoom: "room_a",
  initialHp: 100,
  initialMana: 100,
  initialAlignments: {},
  defaultTriggers: [
    {
      label: "Explore",
      priority: 10,
      pattern: "sputters|echoes|torch|ambient",
      matchType: "room_text",
      actionExpression: "return 'north';",
      conditionExpression: "true",
    },
  ],
};

async function main() {
  const result = await composeFleet({
    rooms: [
      {
        id: "room_a",
        name: "Room A",
        description: "Starting room",
        exits: { north: "room_b" },
        zoneId: "test",
        ambientText: ["The torch on the wall sputters."],
      },
      {
        id: "room_b",
        name: "Room B",
        description: "Second room",
        exits: { south: "room_a" },
        zoneId: "test",
        ambientText: [],
      },
    ],
    agents: [config],
  });

  const { eventBus, immortal } = result;

  // Subscribe to game ticks
  const tickSub = await eventBus.subscribe("game.tick");
  (async () => {
    for await (const ev of tickSub) {
      const p = ev.payload as any;
      console.log("[DEMO] TICK #" + p.tickNumber + " rooms:", p.activeRoomIds);
    }
  })();

  const actionSub = await eventBus.subscribe("agent.*.action");
  (async () => {
    for await (const ev of actionSub) {
      const p = ev.payload as any;
      console.log("[DEMO] ACTION:", p.agentId, "->", p.command);
    }
  })();

  const roomSub = await eventBus.subscribe("game.room.*.event");
  (async () => {
    for await (const ev of roomSub) {
      const p = ev.payload as any;
      console.log("[DEMO] ROOM EVENT:", p.text?.slice(0, 60));
    }
  })();

  // Manually publish a room event to trigger the agent
  await new Promise(r => setTimeout(r, 1000));
  console.log("\n--- Manually publishing room event ---");
  await eventBus.publishRoomEvent("room_a", {
    roomId: "room_a",
    text: "The torch on the wall sputters loudly.",
    category: "ambient",
  });

  await new Promise(r => setTimeout(r, 1000));
  
  const cards = immortal.getAgentCards();
  console.log("\nAgent cards:", JSON.stringify(cards.map(c => ({ name: c.name, room: c.currentRoom, hp: c.hp }))));

  await result.stop();
  process.exit(0);
}
main();
