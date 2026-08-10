import { MemoryTransport } from "../packages/event-bus/src/event-bus";

async function main() {
  const mt = new MemoryTransport();
  await mt.connect();
  const sub = await mt.subscribe("game.tick");

  // Manually iterate with .next() instead of for-await
  (async () => {
    console.log("[LOOP] calling next()...");
    try {
      const ev = await sub.next(5000);
      console.log("[LOOP] got event via next():", ev.subject);
    } catch (e) {
      console.log("[LOOP] next() error:", e);
    }
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
  process.exit(0);
}
main();
