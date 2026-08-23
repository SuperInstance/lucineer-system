import { CellType } from './types';
import type { WorldCell, WorldDef, NpcDef } from './types';
import {
  farmTeachings,
  forestTeachings,
  villageTeachings,
  mountainTeachings,
  meadowTeachings,
  lakeTeachings,
  ruinsTeachings,
  skyTeachings,
} from './teachings';
import { allDiscoveries } from './discoveries';
import { getQuestsForWorld } from './quests';

// ─── Grid builder ─────────────────────────────────────────────────────────

/** Maps a single uppercase character to a `WorldCell`. */
function cellFromChar(ch: string): WorldCell {
  switch (ch) {
    // Walkable, non-interactable
    case 'G': return { type: CellType.GRASS, walkable: true, interactable: false };
    case 'F': return { type: CellType.FIELD, walkable: true, interactable: false };
    case 'P': return { type: CellType.PATH, walkable: true, interactable: false };
    case 'L': return { type: CellType.FLOWER, walkable: true, interactable: false };
    case 'U': return { type: CellType.MUSHROOM, walkable: true, interactable: false };
    case 'I': return { type: CellType.BRIDGE, walkable: true, interactable: false };
    case 'O': return { type: CellType.GATE, walkable: true, interactable: false };
    case 'Q': return { type: CellType.PEN, walkable: true, interactable: false };
    case 'J': return { type: CellType.PUDDLE, walkable: true, interactable: false };
    case 'B2': return { type: CellType.BUSH, walkable: true, interactable: false };
    case 'G2': return { type: CellType.LOG, walkable: true, interactable: false };
    case 'W2': return { type: CellType.WELL, walkable: true, interactable: true };
    case 'H2': return { type: CellType.HAYBALE, walkable: false, interactable: false };
    case 'K2': return { type: CellType.PUMPKIN, walkable: true, interactable: false };
    case 'LP': return { type: CellType.LILYPAD, walkable: true, interactable: false };
    case 'RD': return { type: CellType.REED, walkable: false, interactable: false };
    case 'DK': return { type: CellType.DOCK, walkable: true, interactable: false };
    case 'BT': return { type: CellType.BOAT, walkable: true, interactable: true };
    case 'ST': return { type: CellType.STATUE, walkable: false, interactable: true };
    case 'PL': return { type: CellType.PILLAR, walkable: false, interactable: true };
    case 'CW': return { type: CellType.CRACKED_WALL, walkable: false, interactable: false };
    case 'MS': return { type: CellType.MOSAIC, walkable: true, interactable: true };
    case 'CL': return { type: CellType.COLUMN, walkable: false, interactable: true };
    case 'BS': return { type: CellType.BOOKSHELF, walkable: false, interactable: true };
    case 'CF': return { type: CellType.CLOUD, walkable: true, interactable: false };
    case 'RB': return { type: CellType.RAINBOW, walkable: true, interactable: true };
    case 'SF': return { type: CellType.STAR_FLOWER, walkable: true, interactable: false };
    case 'GM': return { type: CellType.GLOW_MUSHROOM, walkable: true, interactable: true };
    case 'IC': return { type: CellType.ICICLE, walkable: false, interactable: false };
    case 'HS': return { type: CellType.HOT_SPRING, walkable: true, interactable: true };
    case 'LR': return { type: CellType.LAVA_ROCK, walkable: false, interactable: false };
    case 'WP': return { type: CellType.WHIRLPOOL, walkable: false, interactable: false };
    case 'CH': return { type: CellType.CHEST, walkable: true, interactable: true };
    case 'FL': return { type: CellType.FLAG, walkable: true, interactable: true };
    case 'TT': return { type: CellType.TOTEM, walkable: false, interactable: true };
    case 'BM': return { type: CellType.BENCHMARK, walkable: true, interactable: true };
    case 'SC': return { type: CellType.SCROLL, walkable: true, interactable: true };
    case 'TP': return { type: CellType.TELEPORTER, walkable: true, interactable: true };

    // Walkable AND interactable
    case 'S': return { type: CellType.SHEEP, walkable: true, interactable: true };
    case 'D': return { type: CellType.CRYSTAL, walkable: true, interactable: true };
    case 'E': return { type: CellType.CAMPFIRE, walkable: true, interactable: true };

    // Blocking AND interactable
    case 'M': return { type: CellType.RAM, walkable: false, interactable: true };
    case 'B': return { type: CellType.BARN, walkable: false, interactable: true };
    case 'K': return { type: CellType.KENNEL, walkable: false, interactable: true };
    case 'Y': return { type: CellType.SIGN, walkable: false, interactable: true };
    case 'C': return { type: CellType.CAVE, walkable: false, interactable: true };

    // Blocking, non-interactable
    case 'W': return { type: CellType.WATER, walkable: false, interactable: false };
    case 'T': return { type: CellType.TREE, walkable: false, interactable: false };
    case 'R': return { type: CellType.ROCK, walkable: false, interactable: false };
    case 'X': return { type: CellType.FENCE, walkable: false, interactable: false };
    case 'H': return { type: CellType.HOUSE, walkable: false, interactable: false };
    case 'N': return { type: CellType.MOUNTAIN, walkable: false, interactable: false };

    // Void
    case '.': return { type: CellType.EMPTY, walkable: false, interactable: false };

    default: return { type: CellType.EMPTY, walkable: false, interactable: false };
  }
}

/** Parse a grid template string, supporting 2-char cell codes. */
export function createGrid(template: string[]): WorldCell[][] {
  return template.map((row) => {
    const cells: WorldCell[] = [];
    let i = 0;
    while (i < row.length) {
      // Try 2-char code first
      if (i + 1 < row.length) {
        const two = row.substring(i, i + 2);
        if (two[1] && two[1] >= 'A' && two[1] <= 'Z' && two[0] >= 'A' && two[0] <= 'Z' && cellFromChar(two).type !== CellType.EMPTY) {
          cells.push(cellFromChar(two));
          i += 2;
          continue;
        }
      }
      cells.push(cellFromChar(row[i]!));
      i++;
    }
    return cells;
  });
}

// ─── Helpers ───────────────────────────────────────────────────────────────

function discoveriesForWorld(worldId: string) {
  return allDiscoveries.filter((d) => d.world === worldId);
}

// ═══════════════════════════════════════════════════════════════════════════
// WORLD 1 — FARM  "Learning to See"  (16x16)
// AI concept: Pattern Recognition & Classification
// ═══════════════════════════════════════════════════════════════════════════

const farmTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TGGGTSGXXXXQQXT',
  /* 2  */ 'TGLGGFGGXXQQGXT',
  /* 3  */ 'TGGGGGSXXXQOGXT',
  /* 4  */ 'TTGGBBBGGGGGSGT',
  /* 5  */ 'TGGGBBBGGSGGLGT',
  /* 6  */ 'TGH2GGGGLGGGSGT',
  /* 7  */ 'TGH2GGGGGGGSGGT',
  /* 8  */ 'TGGGGPPPGGGGSGT',
  /* 9  */ 'TGSGGPPPGSGGJGT',
  /* 10 */ 'TGGGGPPPGGGGSGT',
  /* 11 */ 'TGLGGPPPK2GGGGT',
  /* 12 */ 'TGGGGPPPGGGGJGT',
  /* 13 */ 'TGGGSGGPGGSGGGT',
  /* 14 */ 'TGGGGGGPGGGGGGT',
  /* 15 */ 'TTTTTGTTTGTTTTTT',
];

const farmNpcs: NpcDef[] = [
  {
    id: 'elder-bark-farm',
    name: 'Elder Bark',
    emoji: '\u{1F415}',
    pos: { x: 6, y: 6 },
    dialog: [
      'Welcome to the farm, young one. Every good sheepdog starts by learning to see.',
      'Look at the sheep. What makes them the same? What makes them different?',
      'That is what machines do too — they find patterns in what they see.',
    ],
    moves: false,
  },
];

export const farmWorld: WorldDef = {
  id: 'farm',
  name: 'The Farm',
  subtitle: 'Learning to See',
  description: 'A peaceful farm where patterns hide in plain sight. Learn to see what makes things the same — and different.',
  grid: createGrid(farmTemplate),
  playerStart: { x: 7, y: 14 },
  sheepPositions: [
    { x: 5, y: 1 }, { x: 7, y: 3 }, { x: 9, y: 5 }, { x: 10, y: 7 },
    { x: 2, y: 9 }, { x: 10, y: 9 }, { x: 4, y: 13 }, { x: 7, y: 13 },
  ],
  penPositions: [
    { x: 9, y: 1 }, { x: 10, y: 1 }, { x: 9, y: 2 }, { x: 10, y: 2 },
  ],
  teachings: farmTeachings,
  discoveries: discoveriesForWorld('farm'),
  quests: getQuestsForWorld('farm'),
  npcs: farmNpcs,
  season: 'summer',
  ambientSound: 'farm',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Pattern Recognition & Classification',
    explanation: 'On the farm, your puppy learns to recognize sheep by their shape, color, and sound. This is exactly how AI classifiers work — they learn patterns from features in training data to categorize inputs.',
  },
  difficulty: 1,
};

// ═══════════════════════════════════════════════════════════════════════════
// WORLD 2 — FOREST  "Finding the Path"  (16x16)
// AI concept: Search Algorithms & Optimization
// ═══════════════════════════════════════════════════════════════════════════

const forestTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TGGGTGGGTGGGTGGT',
  /* 2  */ 'TGTGTUUGTGGGTGGT',
  /* 3  */ 'TPTGGGGGGGGTTGGT',
  /* 4  */ 'TPGGWWGGGGGGTGGT',
  /* 5  */ 'TPGGIIGGGGGGTGGT',
  /* 6  */ 'TPGGWWGGGTTTTGGT',
  /* 7  */ 'TPPGGTGGGGGGGGGT',
  /* 8  */ 'TTPGTGUGTUGTGGGT',
  /* 9  */ 'TGPGGGSSGGGTGGGT',
  /* 10 */ 'TGPGTGSSGGCTGGGT',
  /* 11 */ 'TGGGGGGGGGGGUGGT',
  /* 12 */ 'TGTGGGMGGGGTGGGT',
  /* 13 */ 'TGGTGGGGGGGTUGGT',
  /* 14 */ 'TGPGGGSSGGGGGGGT',
  /* 15 */ 'TTTTTTTTTTTTTTTT',
];

const forestNpcs: NpcDef[] = [
  {
    id: 'wise-owl',
    name: 'Wise Owl',
    emoji: '\u{1F989}',
    pos: { x: 2, y: 2 },
    dialog: [
      'Hoo hoo! Lost in the forest? That\'s the point!',
      'Every dead end teaches you something. Machines search the same way — trying paths until they find the answer.',
    ],
    moves: false,
  },
];

export const forestWorld: WorldDef = {
  id: 'forest',
  name: 'The Forest',
  subtitle: 'Finding the Path',
  description: 'A mysterious forest full of winding paths and hidden clearings. Every dead end teaches you something new about searching.',
  grid: createGrid(forestTemplate),
  playerStart: { x: 2, y: 14 },
  sheepPositions: [
    { x: 7, y: 9 }, { x: 8, y: 9 }, { x: 7, y: 10 }, { x: 8, y: 10 },
    { x: 7, y: 14 }, { x: 8, y: 14 },
  ],
  penPositions: [],
  teachings: forestTeachings,
  discoveries: discoveriesForWorld('forest'),
  quests: getQuestsForWorld('forest'),
  npcs: forestNpcs,
  season: 'summer',
  ambientSound: 'forest',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Search Algorithms & Optimization',
    explanation: 'In the forest, you explore paths and find the best route. AI uses search algorithms (BFS, DFS, A*) to navigate problem spaces efficiently, just like finding your way through trees.',
  },
  difficulty: 1,
};

// ═══════════════════════════════════════════════════════════════════════════
// WORLD 3 — VILLAGE  "Connections Matter"  (16x16)
// AI concept: Neural Networks & Weights
// ═══════════════════════════════════════════════════════════════════════════

const villageTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TGGGTGTGGGTGTGGT',
  /* 2  */ 'TGHGGPGGHGGPGGGT',
  /* 3  */ 'TGGGTPTGGGGTGGGT',
  /* 4  */ 'TSPPPPEPPPSPPSGT',
  /* 5  */ 'TGGGTPTGGGHGTGGGT',
  /* 6  */ 'TGHGGPGGGGGGTGGGT',
  /* 7  */ 'TGGGTPTGGGGTGGGT',
  /* 8  */ 'TPPGPPPGPPGPPPGT',
  /* 9  */ 'TGSGGPSGGSGGPSGGT',
  /* 10 */ 'TGGGGGGPGGGGGGGGT',
  /* 11 */ 'TGGGHGGPGGGHGGGGT',
  /* 12 */ 'TGGGTPTPGGGTPTGGT',
  /* 13 */ 'TGGGGPPPGGGPPPGGT',
  /* 14 */ 'TGSGGGGGGGGGSGGGT',
  /* 15 */ 'TTTTTTTTTTTTTTTT',
];

const villageNpcs: NpcDef[] = [
  {
    id: 'mayor-cat',
    name: 'Mayor Whiskers',
    emoji: '\u{1F431}',
    pos: { x: 7, y: 4 },
    dialog: [
      'Welcome to our village, little pup!',
      'Every house is connected by paths. The wider the path, the more important the connection.',
      'Machines have connections too — they call them weights!',
    ],
    moves: false,
  },
];

export const villageWorld: WorldDef = {
  id: 'village',
  name: 'The Village',
  subtitle: 'Connections Matter',
  description: 'A charming village where every house is connected. Discover how paths between places are like connections in a thinking machine.',
  grid: createGrid(villageTemplate),
  playerStart: { x: 7, y: 14 },
  sheepPositions: [
    { x: 1, y: 4 }, { x: 11, y: 4 }, { x: 2, y: 9 }, { x: 7, y: 9 },
    { x: 12, y: 9 }, { x: 2, y: 14 }, { x: 12, y: 14 },
  ],
  penPositions: [],
  teachings: villageTeachings,
  discoveries: discoveriesForWorld('village'),
  quests: getQuestsForWorld('village'),
  npcs: villageNpcs,
  season: 'autumn',
  ambientSound: 'village',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Neural Networks & Weights',
    explanation: 'The village paths are like neural connections. Each path has a "weight" (importance), and information flows through layers to reach a decision — just like signals in a neural network.',
  },
  difficulty: 2,
};

// ═══════════════════════════════════════════════════════════════
// WORLD 4 — MOUNTAIN  "Seeing the Whole"  (16x16)
// AI concept: Model Training & Generalization
// ═══════════════════════════════════════════════════════════════

const mountainTemplate = [
  /* 0  */ 'NNNNNGNGNNNNNGNNN',
  /* 1  */ 'NNRRGRGRRRNNNGNN',
  /* 2  */ 'NRRGGGGGGRRNGGGN',
  /* 3  */ 'NRGGDGGDGGRNGGGN',
  /* 4  */ 'RRGDGGGGDGRNGGGN',
  /* 5  */ 'RGGGGRRGGGGRRGGN',
  /* 6  */ 'RGEGGGGGGEGRGGGN',
  /* 7  */ 'RGGGRGGRSGGRGGGGN',
  /* 8  */ 'NRGCGGGGGGRNGGGGN',
  /* 9  */ 'NNRGGSGGGRNNNGGGN',
  /* 10 */ 'NNNRGSGRNNNNNGGGN',
  /* 11 */ 'NNNNRGGGNNNNNGGGN',
  /* 12 */ 'NNNRRGGGGRRRNGGGN',
  /* 13 */ 'NNNRGGSGGGGRRGGGN',
  /* 14 */ 'NNNRGGGGGGRNGGGGN',
  /* 15 */ 'NNNNNGGGNNNNNGNNN',
];

const mountainNpcs: NpcDef[] = [
  {
    id: 'mountain-goat',
    name: 'Guide Horns',
    emoji: '\u{1F410}',
    pos: { x: 6, y: 12 },
    dialog: [
      'Baaaa! Climbing high, little pup?',
      'Every step up this mountain is like feeding an example to a machine.',
      'At the top, you\'ll see how all the pieces fit together!',
    ],
    moves: true,
    walkableCells: [CellType.GRASS],
  },
];

export const mountainWorld: WorldDef = {
  id: 'mountain',
  name: 'The Mountain',
  subtitle: 'Seeing the Whole',
  description: 'A towering peak where crystals glow and campfires warm. Climb high enough and you will see how every piece fits together.',
  grid: createGrid(mountainTemplate),
  playerStart: { x: 6, y: 15 },
  sheepPositions: [
    { x: 9, y: 7 }, { x: 6, y: 9 }, { x: 6, y: 10 }, { x: 6, y: 13 },
    { x: 7, y: 13 },
  ],
  penPositions: [],
  teachings: mountainTeachings,
  discoveries: discoveriesForWorld('mountain'),
  quests: getQuestsForWorld('mountain'),
  npcs: mountainNpcs,
  season: 'winter',
  ambientSound: 'mountain',
  enableFlocking: true,
  enableBark: true,
  fogOfWar: 5,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Model Training & Generalization',
    explanation: 'Climbing the mountain is like training a model — each step (example) makes you better. At the summit, you see the whole picture (generalization), not just individual training points.',
  },
  difficulty: 3,
};

// ═══════════════════════════════════════════════════════════════
// WORLD 5 — MEADOW  "Learning by Trying"  (16x16)
// AI concept: Reinforcement Learning
// ═══════════════════════════════════════════════════════════════

const meadowTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TLLLLGGGGGGGGLLT',
  /* 2  */ 'TLLLLSGGGGGGLLGT',
  /* 3  */ 'TGGGFGGGGGGFGGGT',
  /* 4  */ 'TGGGFGGGGGGGFGGT',
  /* 5  */ 'TSSGFGGGGGGFGSGT',
  /* 6  */ 'TGGGFGGGGGGGFGGT',
  /* 7  */ 'TGGGFGGGSSGFGGGT',
  /* 8  */ 'TLLLGFGGGGGFGLLT',
  /* 9  */ 'TLLLLFGGGGGFLLGT',
  /* 10 */ 'TGGGGFGGGGGFGGGT',
  /* 11 */ 'TGGGGFGGGGGFGGGT',
  /* 12 */ 'TSSSGFGGGGGFGSGT',
  /* 13 */ 'TGGGGFGGGGGFGGGT',
  /* 14 */ 'TGGGGFGGGGGFGGGT',
  /* 15 */ 'TTTTTTTTTTTTTTTT',
];

const meadowNpcs: NpcDef[] = [
  {
    id: 'rabbit-trainer',
    name: 'Coach Hops',
    emoji: '\u{1F430}',
    pos: { x: 7, y: 7 },
    dialog: [
      'Try the tall grass! Some paths are better than others.',
      'When you find a good path, remember it! That\'s reinforcement learning — learn from rewards!',
    ],
    moves: true,
    walkableCells: [CellType.GRASS, CellType.FIELD, CellType.FLOWER],
  },
];

export const meadowWorld: WorldDef = {
  id: 'meadow',
  name: 'The Meadow',
  subtitle: 'Learning by Trying',
  description: 'An endless meadow of tall grass and wildflowers. Try different paths, learn from what works, and discover how machines learn from rewards.',
  grid: createGrid(meadowTemplate),
  playerStart: { x: 7, y: 14 },
  sheepPositions: [
    { x: 2, y: 1 }, { x: 13, y: 1 }, { x: 1, y: 5 }, { x: 14, y: 5 },
    { x: 2, y: 12 }, { x: 13, y: 12 },
  ],
  penPositions: [
    { x: 7, y: 0 }, { x: 8, y: 0 },
  ],
  teachings: meadowTeachings,
  discoveries: discoveriesForWorld('meadow'),
  quests: getQuestsForWorld('meadow'),
  npcs: meadowNpcs,
  season: 'spring',
  ambientSound: 'meadow',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Reinforcement Learning',
    explanation: 'In the meadow, the puppy tries different paths and learns which ones lead to sheep. Reinforcement learning works the same way — an agent tries actions, gets rewards, and learns a policy for what works.',
  },
  difficulty: 2,
};

// ═══════════════════════════════════════════════════════════════
// WORLD 6 — LAKE  "Flow and Transform"  (16x16)
// AI concept: Data Processing & Pipelines
// ═══════════════════════════════════════════════════════════════

const lakeTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TGGGGWWWWGGGGGWT',
  /* 2  */ 'TGGGGWWWWGGGGGWT',
  /* 3  */ 'TGGGWWWWWWGGGGWT',
  /* 4  */ 'TGWWWIIGWWWGGWT',
  /* 5  */ 'TWWWWWGWWWWWWGT',
  /* 6  */ 'TWWWWGGWWWWWLPGT',
  /* 7  */ 'TWWWGGSGWWWLLPGT',
  /* 8  */ 'TWWWWGGWWWWWLPGT',
  /* 9  */ 'TWWWWWGWWWWWWGT',
  /* 10 */ 'TGWWWGWWWWGGGGT',
  /* 11 */ 'TGGGGWWWWGGGSGT',
  /* 12 */ 'TGGSGWWWWGGGGGT',
  /* 13 */ 'TGGGGWWWWGGSGGT',
  /* 14 */ 'TGGGGGWWGGGGGSGT',
  /* 15 */ 'TTTTTTTTTTTTTTTT',
];

const lakeNpcs: NpcDef[] = [
  {
    id: 'old-turtle',
    name: 'Professor Shell',
    emoji: '\u{1F422}',
    pos: { x: 1, y: 14 },
    dialog: [
      'Slow and steady... like data flowing through a pipeline.',
      'Water starts as a stream, gets filtered, pooled, and finally reaches the lake. Data does the same thing!',
    ],
    moves: true,
    walkableCells: [CellType.GRASS, CellType.BRIDGE, CellType.LILYPAD, CellType.DOCK],
  },
];

export const lakeWorld: WorldDef = {
  id: 'lake',
  name: 'The Lake',
  subtitle: 'Flow and Transform',
  description: 'A shimmering lake fed by streams. Watch how water flows, gets filtered, and pools — just like data in a processing pipeline.',
  grid: createGrid(lakeTemplate),
  playerStart: { x: 1, y: 13 },
  sheepPositions: [
    { x: 7, y: 7 }, { x: 12, y: 11 }, { x: 13, y: 12 }, { x: 13, y: 13 },
    { x: 12, y: 14 },
  ],
  penPositions: [],
  teachings: lakeTeachings,
  discoveries: discoveriesForWorld('lake'),
  quests: getQuestsForWorld('lake'),
  npcs: lakeNpcs,
  season: 'summer',
  ambientSound: 'lake',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Data Processing & Pipelines',
    explanation: 'Water flows from streams to the lake through filters and pools, just like data flows through a pipeline: collection, cleaning, transformation, and storage.',
  },
  difficulty: 2,
};

// ═══════════════════════════════════════════════════════════════
// WORLD 7 — RUINS  "Remember and Focus"  (16x16)
// AI concept: Memory & Attention Mechanisms
// ═══════════════════════════════════════════════════════════════

const ruinsTemplate = [
  /* 0  */ 'TTTTTTTTTTTTTTTT',
  /* 1  */ 'TCWCLGGGGGGLCWCT',
  /* 2  */ 'TGGGGGGGGGGGGGT',
  /* 3  */ 'TGGPLGGGMSGGGPGT',
  /* 4  */ 'TGGGGGGGGGGGGGT',
  /* 5  */ 'TGGGGSTTSGGGGGGT',
  /* 6  */ 'TGGGGGGGGGGGGGGT',
  /* 7  */ 'TGPLGGGSSGGGPGGT',
  /* 8  */ 'TGGGGGGGGGGGGGGT',
  /* 9  */ 'TGGMSGGGGGGMSGGT',
  /* 10 */ 'TGGGGGGGGGGGGGGT',
  /* 11 */ 'TGGPLGGSCGGGPLGT',
  /* 12 */ 'TGGGGGGGGGGGGGGT',
  /* 13 */ 'TGGSGGGGGGGSGGGT',
  /* 14 */ 'TGGGGGGPGGGGGGGT',
  /* 15 */ 'TTTTTTTTTTTTTTTT',
];

const ruinsNpcs: NpcDef[] = [
  {
    id: 'ghost-scholar',
    name: 'Professor Whisper',
    emoji: '\u{1F47B}',
    pos: { x: 8, y: 8 },
    dialog: [
      'These ruins remember everything...',
      'AI models have memory too. Some things they remember forever (long-term), some only for a moment (short-term).',
      'And attention? That\'s when the model decides what\'s important RIGHT NOW.',
    ],
    moves: true,
    walkableCells: [CellType.GRASS, CellType.MOSAIC, CellType.PATH],
  },
];

export const ruinsWorld: WorldDef = {
  id: 'ruins',
  name: 'The Ancient Ruins',
  subtitle: 'Remember and Focus',
  description: 'Mysterious ruins that hold the memories of an ancient civilization. Discover how AI remembers what matters and focuses on what\'s important.',
  grid: createGrid(ruinsTemplate),
  playerStart: { x: 7, y: 14 },
  sheepPositions: [
    { x: 2, y: 5 }, { x: 12, y: 5 }, { x: 3, y: 9 }, { x: 12, y: 9 },
  ],
  penPositions: [],
  teachings: ruinsTeachings,
  discoveries: discoveriesForWorld('ruins'),
  quests: getQuestsForWorld('ruins'),
  npcs: ruinsNpcs,
  season: 'autumn',
  ambientSound: 'ruins',
  enableFlocking: true,
  enableBark: true,
  fogOfWar: 6,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Memory & Attention Mechanisms',
    explanation: 'The ruins hold memories, like how neural networks use memory cells (LSTM/GRU) and attention mechanisms to remember important information and focus on relevant parts of their input.',
  },
  difficulty: 3,
};

// ═══════════════════════════════════════════════════════════════
// WORLD 8 — SKY  "Creating New Worlds"  (16x16)
// AI concept: Generative AI & Creativity
// ═══════════════════════════════════════════════════════════════

const skyTemplate = [
  /* 0  */ 'CCCCCCCCCCCCCCCC',
  /* 1  */ 'CCGGGGGGGGGGGGCC',
  /* 2  */ 'CGGGSSFGGGSSFGGCC',
  /* 3  */ 'CGGGFGGGGFGGGGCC',
  /* 4  */ 'CGGGFGGGGFGGGGCC',
  /* 5  */ 'CGSSFGGGSFGGSSGCC',
  /* 6  */ 'CGGGFGGGGFGGGGCC',
  /* 7  */ 'CGGGFGGGGFGGGGCC',
  /* 8  */ 'CGSSFGGGSFGGSSGCC',
  /* 9  */ 'CGGGFGGGGFGGGGCC',
  /* 10 */ 'CGGGFGGGGFGGGGCC',
  /* 11 */ 'CGSSFGGGGGFGGSSCC',
  /* 12 */ 'CGGGSSFGGSSFGGGCC',
  /* 13 */ 'CGGGFGGGGFGGGGCC',
  /* 14 */ 'CGGGFGGGGFGGGGCC',
  /* 15 */ 'CCCCCCCCCCCCCCCC',
];

const skyNpcs: NpcDef[] = [
  {
    id: 'dream-bird',
    name: 'Dreamweaver',
    emoji: '\u{1F985}',
    pos: { x: 7, y: 7 },
    dialog: [
      'Up here, we create new things from old patterns!',
      'Take a little of this, a little of that, mix them together... that\'s what generative AI does!',
      'It\'s like cooking — you learn recipes, then create your own dishes!',
    ],
    moves: true,
    walkableCells: [CellType.GRASS, CellType.CLOUD, CellType.STAR_FLOWER, CellType.FLOWER],
  },
];

export const skyWorld: WorldDef = {
  id: 'sky',
  name: 'The Sky Islands',
  subtitle: 'Creating New Worlds',
  description: 'Floating islands among the clouds. Discover how AI creates new things by combining old patterns in surprising ways.',
  grid: createGrid(skyTemplate),
  playerStart: { x: 7, y: 14 },
  sheepPositions: [
    { x: 3, y: 2 }, { x: 12, y: 2 }, { x: 3, y: 8 }, { x: 12, y: 8 },
  ],
  penPositions: [],
  teachings: skyTeachings,
  discoveries: discoveriesForWorld('sky'),
  quests: getQuestsForWorld('sky'),
  npcs: skyNpcs,
  season: 'spring',
  ambientSound: 'sky',
  enableFlocking: true,
  enableBark: true,
  width: 16,
  height: 16,
  aiTheme: {
    concept: 'Generative AI & Creativity',
    explanation: 'Sky islands combine elements from all worlds into something new, just like generative AI (GANs, diffusion models, LLMs) creates new content by learning and combining patterns from training data.',
  },
  difficulty: 4,
};

// ─── World registry ────────────────────────────────────────────────────────

/** All worlds in level order. */
export const allWorlds: WorldDef[] = [
  farmWorld,
  forestWorld,
  villageWorld,
  mountainWorld,
  meadowWorld,
  lakeWorld,
  ruinsWorld,
  skyWorld,
];

/** Look up a world by its id. */
export function getWorldById(id: string): WorldDef | undefined {
  return allWorlds.find((w) => w.id === id);
}
