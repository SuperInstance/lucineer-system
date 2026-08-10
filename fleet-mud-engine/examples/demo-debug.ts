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

  const actionSub = await eventBus.subscribe("agent.*.action");
  (async () => {
    console.log("[DEMO] action subscriber ready");
    for await (const ev of actionSub) {
      const p = ev.payload as any;
      console.log("[DEMO] ACTION:", p.agentId, "->", p.command, "in room", p.roomId);
    }
  })();

  // Log all room events too
  const roomSub = await eventBus.subscribe("game.room.*.event");
  (async () => {
    console.log("[DEMO] room subscriber ready");
    for await (const ev of roomSub) {
      const p = ev.payload as any;
      console.log("[DEMO] ROOM EVENT:", ev.subject, p.text);
    }
  })();

  await new Promise(r => setTimeout(r, 2000));
  
  const cards = immortal.getAgentCards();
  console.log("\nAgent cards:", JSON.stringify(cards.map(c => ({ name: c.name, room: c.currentRoom, hp: c.hp }))));
  
  const waveform = immortal.getWaveform("test");
  console.log("Waveform:", JSON.stringify({ tension: waveform.globalTension, dps: waveform.globalDps, combats: waveform.activeCombats }));

  await result.stop();
  process.exit(0);
}
main();
