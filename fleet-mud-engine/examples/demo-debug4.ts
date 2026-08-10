// Direct test of the async iterator pattern
import { MemoryTransport } from "../packages/event-bus/src/event-bus";

async function main() {
  const mt = new MemoryTransport();
  await mt.connect();

  // Check: does subscribe return a working iterator?
  const sub = await mt.subscribe("game.tick");
  
  // Start consuming
  const loop = (async () => {
    console.log("[LOOP] entering for-await");
    for await (const ev of sub) {
      console.log("[LOOP] got event:", ev.subject);
    }
    console.log("[LOOP] exited");
  })();

  await new Promise(r => setTimeout(r, 200));
  
  console.log("[MAIN] publishing...");
  const seq = await mt.publish("game.tick", {
    id: "test:1",
    subject: "game.tick",
    timestamp: Date.now(),
    publisher: "test",
    sequence: 1,
    payload: { tick: 1 },
    causation: [],
  });
  console.log("[MAIN] published, seq:", seq);
  
  await new Promise(r => setTimeout(r, 500));
  
  await sub.unsubscribe();
  process.exit(0);
}
main();
