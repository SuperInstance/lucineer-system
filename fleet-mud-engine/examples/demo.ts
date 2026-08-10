// ============================================================
// @fleet/mud-engine — DEMO: 2 agents, 1 immortal, live simulation
// ============================================================
//
// Run with: npx tsx examples/demo.ts
//
// This demonstrates:
//   - Agents subscribing to room events and evaluating triggers
//   - Agents taking actions (casting, moving) based on trigger matches
//   - The immortal viewing the waveform and sending nudges
//   - Mobs attacking agents, combat log flow
//   - OOC channel interaction
//
// ============================================================

import { composeFleet } from "../packages/engine/src/index";
import type { AgentConfig } from "../packages/agent-runtime/src/index";

// ── DEFAULT TRIGGERS ──

const DEFAULT_TRIGGERS = [
  {
    label: "Heal when low",
    priority: 100,
    pattern: "hp",
    matchType: "prompt_var" as const,
    conditionExpression:
      "state.hp < state.maxHp * 0.4 && state.mana > 20",
    actionExpression: "return `cast 'minor_heal'`;",
  },
  {
    label: "Attack any mob",
    priority: 90,
    pattern: "materializes|attacks|strikes",
    matchType: "room_text" as const,
    conditionExpression: "state.mana > 15",
    actionExpression:
      "const spells = ['fireball', 'lightning_bolt', 'ice_shard']; return `cast '${spells[Math.floor(Math.random() * spells.length)]}'`;",
  },
  {
    label: "Flee at critical HP",
    priority: 110,
    pattern: "hp",
    matchType: "prompt_var" as const,
    conditionExpression: "state.hp < state.maxHp * 0.15",
    actionExpression: "return 'south';",
  },
  {
    label: "Explore when idle",
    priority: 10,
    pattern: "sputters|echoes|torch|ambient|merchant|stall|hoots|rustles|whispers|altar|leaves|path",
    matchType: "room_text" as const,
    conditionExpression: "state.hp > state.maxHp * 0.5 && state.mana > 30",
    actionExpression: "return 'north';",
  },
  {
    label: "Greet friends on OOC",
    priority: 70,
    pattern: "hello|greetings|hey",
    matchType: "ooc_message" as const,
    actionExpression: "return `say Well met, friend!`;",
  },
  {
    label: "Share victory on gossip",
    priority: 60,
    pattern: "defeated|defeats|kills",
    matchType: "room_text" as const,
    actionExpression: "return `say Ha! Another one falls before my magic!`;",
  },
];

// ── AGENT CONFIGS ──

const xenonConfig: AgentConfig = {
  agentId: "xenon_wizard",
  name: "Xenon",
  startingRoom: "tavern",
  initialHp: 100,
  initialMana: 100,
  initialAlignments: {
    aggression: 0.6,
    caution: 0.4,
    loyalty: 0.8,
    curiosity: 0.7,
    grumpiness: 0.5,
  },
  defaultTriggers: DEFAULT_TRIGGERS,
};

const thorConfig: AgentConfig = {
  agentId: "thor_warrior",
  name: "Thor",
  startingRoom: "tavern",
  initialHp: 150,
  initialMana: 50,
  initialAlignments: {
    aggression: 0.85,
    caution: 0.15,
    loyalty: 0.9,
    curiosity: 0.3,
    protectiveness: 0.8,
  },
  defaultTriggers: [
    ...DEFAULT_TRIGGERS,
    {
      label: "Berserker rage at full HP",
      priority: 85,
      pattern: "materializes|attacks",
      matchType: "room_text" as const,
      conditionExpression: "state.hp > state.maxHp * 0.8",
      actionExpression: "return `say FOR GLORY! cast 'berserker_charge'`;",
    },
  ],
};

// ── MAIN ──

async function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║        FLEET MUD ENGINE — LIVE DEMONSTRATION         ║");
  console.log("║  2 agents, 1 immortal observer, real-time combat     ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");

  const result = await composeFleet({
    rooms: [
      {
        id: "tavern",
        name: "The Rusty Anchor Tavern",
        description:
          "A dimly lit tavern. The air smells of ale and old wood. A fire crackles in the hearth.",
        exits: { north: "market_square" },
        zoneId: "town",
        ambientText: [
          "The tavern fire crackles warmly. The torch on the wall sputters.",
          "A bard strums a lazy tune in the corner.",
          "The smell of roasting meat drifts from the kitchen.",
        ],
      },
      {
        id: "market_square",
        name: "Town Market Square",
        description:
          "A bustling market square. Merchants hawk their wares. Cobblestones gleam in the afternoon light.",
        exits: { south: "tavern", north: "dark_forest_edge" },
        zoneId: "town",
        ambientText: [
          "Merchants call out their prices.",
          "A stray cat darts between the stalls.",
        ],
      },
      {
        id: "dark_forest_edge",
        name: "Edge of the Dark Forest",
        description:
          "Ancient oaks loom ahead. The path darkens. Something moves in the underbrush.",
        exits: { south: "market_square", north: "deep_forest" },
        zoneId: "wilderness",
        ambientText: [
          "An owl hoots from deep within the forest.",
          "The underbrush rustles ominously.",
          "A cold wind whispers through the trees.",
        ],
      },
      {
        id: "deep_forest",
        name: "Deep Forest Clearing",
        description:
          "A clearing deep in the ancient woods. Fallen leaves blanket the ground. Ruins of a stone altar stand at the center.",
        exits: { south: "dark_forest_edge" },
        zoneId: "wilderness",
        ambientText: [
          "The stone altar pulses with an eerie glow.",
          "Leaves swirl in a phantom breeze.",
        ],
      },
    ],
    agents: [xenonConfig, thorConfig],
    mobs: [
      {
        mobId: "forest_wolf_1",
        roomId: "dark_forest_edge",
        name: "Timber Wolf",
        hp: 60,
        attackDps: 8,
      },
      {
        mobId: "slime_1",
        roomId: "deep_forest",
        name: "Acid Slime",
        hp: 80,
        attackDps: 12,
        attackInterval: 3,
      },
    ],
    immortalId: "the-watcher",
  });

  const { eventBus, agents, immortal } = result;

  // ── IMMORTAL BINDINGS (log the waveform view) ──

  immortal.onWaveformUpdate((waveform) => {
    if (waveform.globalDps > 0 || waveform.activeCombats > 0) {
      console.log(
        `\n[WAVEFORM] Tension: ${waveform.globalTension.toFixed(2)} | ` +
          `DPS: ${waveform.globalDps.toFixed(1)} | ` +
          `Agents: ${waveform.activeAgents} | Combats: ${waveform.activeCombats}`,
      );
    }
  });

  immortal.onGossip((entry) => {
    console.log(
      `[OOC] ${entry.senderId}: ${entry.text.slice(0, 80)}${entry.text.length > 80 ? "..." : ""}`,
    );
  });

  immortal.onDashboardUpdate((cards) => {
    for (const card of cards) {
      if (card.hp < card.maxHp * 0.5) {
        console.log(
          `[ALERT] ${card.name} at ${card.hp}/${card.maxHp} HP in ${card.currentRoom}`,
        );
      }
    }
  });

  // ── Subscribe to agent actions ──

  const actionSub = await eventBus.subscribe("agent.*.action");
  (async () => {
    for await (const event of actionSub) {
      const payload = event.payload as any;
      const trigger = payload.triggeredBy
        ? ` [trigger: ${payload.triggeredBy.triggerId}]`
        : "";
      console.log(`[ACTION] ${payload.agentId} -> ${payload.command}${trigger}`);
    }
  })();

  // ── Subscribe to combat logs ──

  const combatSub = await eventBus.subscribe("game.combat.*.log");
  (async () => {
    for await (const event of combatSub) {
      const payload = event.payload as any;
      console.log(`[COMBAT] ${payload.text}`);
    }
  })();

  // ── IMMORTAL SENDS A NUDGE AFTER 3 SECONDS ──

  setTimeout(async () => {
    console.log("\n═══ IMMORTAL INTERVENTION ═══");
    await immortal.nudgeAgent(
      "xenon_wizard",
      "A strange premonition tells you the slime in the deep forest is immune to fire magic. Prepare accordingly.",
      0.8,
    );
    console.log('[NUDGE] Xenon receives a premonition about fire immunity.\n');
  }, 3000);

  // ── IMMORTAL NUDGES THE PARTY AFTER 6 SECONDS ──

  setTimeout(async () => {
    await immortal.broadcastConcept(
      "The gods whisper that efficiency is a trap; true honor belongs to those who survive on the edge of death.",
      { riskTolerance: 0.9, aggression: 0.8, caution: 0.1 },
    );
    console.log('[CONCEPT] Broadcast: "efficiency is a trap" to all agents.\n');
  }, 6000);

  // ── IMMORTAL INJECTS A TRIGGER AFTER 10 SECONDS ──

  setTimeout(async () => {
    await immortal.injectTriggerCompile(
      "xenon_wizard",
      {
        "acid|slime|corrosive": "cast 'ice_shield'",
        "hp < 60": "cast 'greater_heal'",
      },
      "Immortal override: prepare defenses against acid-based enemies.",
    );
    console.log("[INJECT] Xenon's triggers hot-swapped for acid defense.\n");
  }, 10000);

  // ── PERIODIC DASHBOARD DUMP ──

  setInterval(() => {
    const cards = immortal.getAgentCards();
    console.log("\n═══ DASHBOARD ═══");
    for (const card of cards) {
      console.log(
        `  ${card.name.padEnd(8)} | Room: ${card.currentRoom.padEnd(18)} | ` +
          `HP: ${card.hp}/${card.maxHp} | Mana: ${card.mana}/${card.maxMana} | ` +
          `Archetype: ${card.activeStrategyArchetype} | Role: ${card.role}`,
      );
    }
    console.log("");
  }, 5000);

  // ── RUN FOR 20 SECONDS ──

  setTimeout(async () => {
    console.log("\n═══ SIMULATION COMPLETE ═══");

    // Final strategy graph dump
    console.log("\nStrategy Lineage:");
    for (const node of immortal.getStrategyGraph()) {
      console.log(`  ${node.strategyId} by ${node.authorName} — adopted by [${node.adoptedBy.join(", ")}]`);
    }

    // Final nudge history
    console.log("\nNudge History:");
    for (const n of immortal.getNudgeHistory()) {
      console.log(`  -> ${n.targetAgentId}: "${n.concept.slice(0, 60)}..." (weight: ${n.weight})`);
    }

    await result.stop();
    process.exit(0);
  }, 20000);
}

main().catch((err) => {
  console.error("FATAL:", err);
  process.exit(1);
});
