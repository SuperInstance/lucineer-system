// MIST Game Engine — Quest System
// Challenges and objectives within each world

import type { Quest, DialogStep } from './types';

// ── Farm Quests (Pattern Recognition) ─────────────────────────

const farmQuests: Quest[] = [
  {
    id: 'farm-first-herd',
    world: 'farm',
    name: 'First Herd',
    description: 'Herd 2 sheep into the pen to prove you are learning the patterns.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 2,
    xpReward: 15,
    stickerReward: 'sticker-woolly-wonder',
    startDialog: [
      { text: 'Good pup! Your first task is to bring 2 sheep to the pen. Watch how they move together — that\'s a pattern!', speaker: 'elder' },
    ],
    completeDialog: [
      { text: 'Excellent! You spotted the pattern — sheep follow each other. In AI, we call that clustering!', speaker: 'elder' },
    ],
  },
  {
    id: 'farm-explore-all',
    world: 'farm',
    name: 'Farm Explorer',
    description: 'Visit at least 30 different cells to learn the layout.',
    emoji: '🗺️',
    type: 'explore_cells',
    target: 30,
    xpReward: 10,
  },
  {
    id: 'farm-elder-wisdom',
    world: 'farm',
    name: 'Elder\'s Wisdom',
    description: 'Find and listen to all 5 of Elder Bark\'s teachings on the farm.',
    emoji: '📖',
    type: 'find_discovery',
    target: 5,
    xpReward: 20,
    stickerReward: 'sticker-farm-hand',
    requiresDiscoveries: ['sheep-sight', 'flock-mind'],
  },
  {
    id: 'farm-bark-master',
    world: 'farm',
    name: 'Bark Master',
    description: 'Use your bark ability 5 times to herd sheep more efficiently.',
    emoji: '📢',
    type: 'bark_count',
    target: 5,
    xpReward: 12,
    hidden: true,
  },
];

// ── Forest Quests (Search & Optimization) ─────────────────────

const forestQuests: Quest[] = [
  {
    id: 'forest-dead-end-explorer',
    world: 'forest',
    name: 'Dead End Explorer',
    description: 'Find your way through 3 dead ends. Every wrong path teaches something!',
    emoji: '🌲',
    type: 'explore_cells',
    target: 40,
    xpReward: 15,
    startDialog: [
      { text: 'The forest is full of wrong turns. But in AI, finding what DOESN\'T work is just as important as finding what does!', speaker: 'elder' },
    ],
  },
  {
    id: 'forest-bridge-crosser',
    world: 'forest',
    name: 'Bridge Crosser',
    description: 'Cross the bridge to reach the other side of the stream.',
    emoji: '🌉',
    type: 'reach_position',
    target: 1,
    xpReward: 10,
    targetPos: { x: 5, y: 5 },
    stickerReward: 'sticker-bridge-builder',
  },
  {
    id: 'forest-mushroom-hunter',
    world: 'forest',
    name: 'Mushroom Hunter',
    description: 'Discover all the hidden mushroom patches in the forest.',
    emoji: '🍄',
    type: 'find_discovery',
    target: 3,
    xpReward: 15,
    stickerReward: 'sticker-mushroom-master',
    hidden: true,
  },
  {
    id: 'forest-all-sheep',
    world: 'forest',
    name: 'Forest Flock Finder',
    description: 'Find and collect all 4 sheep hiding in the forest.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 4,
    xpReward: 20,
  },
];

// ── Village Quests (Neural Networks) ───────────────────────────

const villageQuests: Quest[] = [
  {
    id: 'village-connected',
    world: 'village',
    name: 'Well Connected',
    description: 'Visit every house in the village to understand the network of paths.',
    emoji: '🏘️',
    type: 'explore_cells',
    target: 45,
    xpReward: 15,
    startDialog: [
      { text: 'Every house is connected by paths, like neurons connected by synapses. Visit them all to see the pattern!', speaker: 'elder' },
    ],
  },
  {
    id: 'village-fountain-center',
    world: 'village',
    name: 'Heart of the Village',
    description: 'Reach the central fountain where all paths converge.',
    emoji: '⛲',
    type: 'reach_position',
    target: 1,
    xpReward: 10,
    targetPos: { x: 6, y: 4 },
    stickerReward: 'sticker-fountain-friend',
  },
  {
    id: 'village-path-walker',
    world: 'village',
    name: 'Path Walker',
    description: 'Walk along 50 path cells to trace the connections.',
    emoji: '🛤️',
    type: 'explore_cells',
    target: 50,
    xpReward: 12,
  },
  {
    id: 'village-all-sheep',
    world: 'village',
    name: 'Village Herder',
    description: 'Collect all 5 sheep scattered around the village paths.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 5,
    xpReward: 25,
  },
];

// ── Mountain Quests (Training & Generalization) ────────────────

const mountainQuests: Quest[] = [
  {
    id: 'mountain-crystal-collector',
    world: 'mountain',
    name: 'Crystal Collector',
    description: 'Find all the glowing crystals on the mountain.',
    emoji: '💎',
    type: 'find_discovery',
    target: 3,
    xpReward: 20,
    stickerReward: 'sticker-crystal-collector',
    startDialog: [
      { text: 'Crystals store memories, like model weights store learned patterns. Collect them all!', speaker: 'elder' },
    ],
  },
  {
    id: 'mountain-summit-reach',
    world: 'mountain',
    name: 'Summit Reach',
    description: 'Reach the summit of the mountain to see the whole picture.',
    emoji: '🏔️',
    type: 'reach_position',
    target: 1,
    xpReward: 30,
    targetPos: { x: 4, y: 0 },
    stickerReward: 'sticker-summit-star',
    completeDialog: [
      { text: 'From up here, you can see everything! A trained AI model sees the whole picture too — not just pieces.', speaker: 'elder' },
    ],
  },
  {
    id: 'mountain-all-sheep',
    world: 'mountain',
    name: 'Mountain Climber',
    description: 'Find all 3 sheep on the mountain slopes.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 3,
    xpReward: 20,
  },
  {
    id: 'mountain-campfire-rest',
    world: 'mountain',
    name: 'Rest by the Fire',
    description: 'Visit both campfires to understand how training warms up a model.',
    emoji: '🔥',
    type: 'find_discovery',
    target: 2,
    xpReward: 15,
    stickerReward: 'sticker-fire-tender',
  },
];

// ── Meadow Quests (Reinforcement Learning) ─────────────────────

const meadowQuests: Quest[] = [
  {
    id: 'meadow-grass-trial',
    world: 'meadow',
    name: 'Grass Trial',
    description: 'Find the best path through the tall grass by trying different routes.',
    emoji: '🌿',
    type: 'explore_cells',
    target: 50,
    xpReward: 15,
    startDialog: [
      { text: 'In the meadow, the best grass is hidden. You have to try, learn, and try again — that\'s reinforcement learning!', speaker: 'elder' },
    ],
  },
  {
    id: 'meadow-sheep-reward',
    world: 'meadow',
    name: 'Reward Seeker',
    description: 'Collect 4 sheep to earn your reward.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 4,
    xpReward: 20,
    stickerReward: 'sticker-reward-hunter',
  },
  {
    id: 'meadow-bark-trial',
    world: 'meadow',
    name: 'Bark Trial',
    description: 'Use your bark 10 times to master herding through trial and error.',
    emoji: '📢',
    type: 'bark_count',
    target: 10,
    xpReward: 18,
  },
];

// ── Lake Quests (Data Processing) ──────────────────────────────

const lakeQuests: Quest[] = [
  {
    id: 'lake-stream-follower',
    world: 'lake',
    name: 'Stream Follower',
    description: 'Follow the stream from source to lake, tracing the data pipeline.',
    emoji: '🌊',
    type: 'explore_cells',
    target: 45,
    xpReward: 15,
    startDialog: [
      { text: 'Water flows from streams to the lake, like data flows through a pipeline. Follow it!', speaker: 'elder' },
    ],
  },
  {
    id: 'lake-island-hop',
    world: 'lake',
    name: 'Island Hopper',
    description: 'Visit all the islands in the lake.',
    emoji: '🏝️',
    type: 'explore_cells',
    target: 55,
    xpReward: 18,
    stickerReward: 'sticker-island-hopper',
  },
  {
    id: 'lake-all-sheep',
    world: 'lake',
    name: 'Lake Herder',
    description: 'Find and collect all 5 sheep near the water.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 5,
    xpReward: 22,
  },
];

// ── Ruins Quests (Memory & Attention) ──────────────────────────

const ruinsQuests: Quest[] = [
  {
    id: 'ruins-memory-hall',
    world: 'ruins',
    name: 'Memory Hall',
    description: 'Explore the memory hall and find the ancient scrolls.',
    emoji: '📜',
    type: 'find_discovery',
    target: 3,
    xpReward: 20,
    startDialog: [
      { text: 'These ruins hold memories of an ancient civilization. AI models have memory too — they remember what matters and forget what doesn\'t.', speaker: 'elder' },
    ],
  },
  {
    id: 'ruins-attention-focus',
    world: 'ruins',
    name: 'Attention Focus',
    description: 'Visit the three pillars of attention to understand how AI focuses.',
    emoji: '🏛️',
    type: 'find_discovery',
    target: 3,
    xpReward: 25,
    stickerReward: 'sticker-attention-master',
  },
  {
    id: 'ruins-all-sheep',
    world: 'ruins',
    name: 'Ruins Explorer',
    description: 'Find all 4 sheep hiding among the ancient stones.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 4,
    xpReward: 20,
  },
];

// ── Sky Quests (Generative AI) ─────────────────────────────────

const skyQuests: Quest[] = [
  {
    id: 'sky-creation',
    world: 'sky',
    name: 'Cloud Creator',
    description: 'Explore the sky islands and discover how new ideas are born.',
    emoji: '☁️',
    type: 'explore_cells',
    target: 50,
    xpReward: 20,
    startDialog: [
      { text: 'Up here in the sky, new ideas form from old ones — just like generative AI creates new things from patterns it has learned!', speaker: 'elder' },
    ],
  },
  {
    id: 'sky-rainbow-chase',
    world: 'sky',
    name: 'Rainbow Chaser',
    description: 'Find the legendary rainbow bridge.',
    emoji: '🌈',
    type: 'reach_position',
    target: 1,
    xpReward: 30,
    targetPos: { x: 8, y: 1 },
    stickerReward: 'sticker-dream-weaver',
    completeDialog: [
      { text: 'You found the rainbow! Generative AI creates beautiful new things by combining patterns in unexpected ways — just like a rainbow combines light and water.', speaker: 'elder' },
    ],
  },
  {
    id: 'sky-all-sheep',
    world: 'sky',
    name: 'Sky Shepherd',
    description: 'Collect all 4 sheep floating among the clouds.',
    emoji: '🐑',
    type: 'collect_sheep',
    target: 4,
    xpReward: 25,
  },
];

// ─── All quests ─────────────────────────────────────────────────

export const allQuests: Quest[] = [
  ...farmQuests,
  ...forestQuests,
  ...villageQuests,
  ...mountainQuests,
  ...meadowQuests,
  ...lakeQuests,
  ...ruinsQuests,
  ...skyQuests,
];

/** Get quests for a specific world. */
export function getQuestsForWorld(worldId: string): Quest[] {
  return allQuests.filter((q) => q.world === worldId);
}

/** Look up a quest by its id. */
export function getQuestById(id: string): Quest | undefined {
  return allQuests.find((q) => q.id === id);
}
