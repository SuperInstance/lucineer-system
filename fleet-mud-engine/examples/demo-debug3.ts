// Direct test of MemoryTransport pub/sub within the compose flow
import { EventBus, MemoryTransport, Subjects } from "../packages/event-bus/src/index";

async function main() {
  const transport = new MemoryTransport();
  await transport.connect();
  
  const bus = new EventBus({ transport, publisherId: "test" });
  
  // Subscribe first
  const tickSub = await bus.subscribe("game.tick");
  (async () => {
    console.log("[TEST] tick subscriber started");
    for await (const ev of tickSub) {
      console.log("[TEST] GOT TICK:", (ev.payload as any).tickNumber);
    }
  })();
  
  const roomSub = await bus.subscribe("game.room.*.event");
  (async () => {
    console.log("[TEST] room subscriber started");
    for await (const ev of roomSub) {
      console.log("[TEST] GOT ROOM EVENT:", ev.subject);
    }
  })();

  // Then publish
  await new Promise(r => setTimeout(r, 500));
  console.log("--- Publishing tick ---");
  await bus.publishGameTick({ tickNumber: 1, tickDurationMs: 250, activeRoomIds: ["r1"], activeAgentIds: ["a1"] });
  
  await new Promise(r => setTimeout(r, 200));
  console.log("--- Publishing room event ---");
  await bus.publishRoomEvent("r1", { roomId: "r1", text: "Hello world", category: "ambient" });
  
  await new Promise(r => setTimeout(r, 500));
  console.log("Done");
  process.exit(0);
}
main();
