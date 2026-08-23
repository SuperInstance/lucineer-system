// MIST Game Engine — Zustand Store (Expanded v2.0)
// Central game state with flocking, quests, day/night, bark, fog of war

import { create } from 'zustand';
import { CellType, LevelNames } from './types';
import type { Position, Teaching, WorldCell, WorldDef, SheepEntity, Direction, SeasonConfig, Quest } from './types';
import { allWorlds, getWorldById } from './worlds';
import { getTeachingById } from './teachings';
import { getDiscoveryById, allDiscoveries } from './discoveries';
import { allStickers } from './stickers';
import { getQuestById, getQuestsForWorld } from './quests';
import { initSheepEntities, updateFlocking, computeBark, revealFog, dirToDelta, getTimeOfDay } from './engine';

// ─── Trigger mappings ──────────────────────────────────────────────────

const DISCOVERY_TRIGGERS: Record<string, CellType> = {
  // Farm
  'sheep-sight': CellType.SHEEP, 'flock-mind': CellType.SHEEP, 'pen-purpose': CellType.PEN,
  'elder-home': CellType.KENNEL, 'grass-pattern': CellType.FIELD,
  'haybale-haystack': CellType.HAYBALE, 'well-water': CellType.WELL,
  'flower-pattern': CellType.FLOWER, 'puddle-reflect': CellType.PUDDLE,
  // Forest
  'forest-path': CellType.PATH, 'stream-cross': CellType.BRIDGE, 'mushroom-ring': CellType.MUSHROOM,
  'cave-dark': CellType.CAVE, 'firefly-glow': CellType.GRASS,
  'dead-end-lesson': CellType.TREE, 'bridge-optimization': CellType.BRIDGE,
  'mushroom-features': CellType.MUSHROOM, 'stream-pipeline': CellType.WATER,
  // Village
  'house-link': CellType.HOUSE, 'fountain-center': CellType.CAMPFIRE, 'crossroads': CellType.PATH,
  'market-square': CellType.PATH, 'bell-tower': CellType.HOUSE,
  'sign-weights': CellType.SIGN, 'garden-node': CellType.FLOWER, 'intersection-aggregation': CellType.PATH,
  'well-normalization': CellType.WELL,
  // Mountain
  'crystal-glow': CellType.CRYSTAL, 'campfire-warm': CellType.CAMPFIRE, 'summit-view': CellType.MOUNTAIN,
  'eagle-perspective': CellType.MOUNTAIN, 'snow-flake': CellType.ROCK,
  'crystal-weights': CellType.CRYSTAL, 'training-fire': CellType.CAMPFIRE,
  'overfitting-cliff': CellType.MOUNTAIN, 'generalization-valley': CellType.GRASS,
  // Meadow
  'reward-signal': CellType.SHEEP, 'explore-exploit': CellType.FIELD,
  'policy-path': CellType.PATH, 'q-value-crystal': CellType.CRYSTAL,
  'reward-shape': CellType.FLOWER, 'optimal-route': CellType.PATH,
  'delayed-reward': CellType.SHEEP,
  // Lake
  'stream-source': CellType.WATER, 'filter-net': CellType.BRIDGE,
  'batch-stone': CellType.ROCK, 'augment-flower': CellType.FLOWER,
  'normalize-pool': CellType.WATER, 'clean-water': CellType.LILYPAD,
  'pipeline-end': CellType.WATER,
  // Ruins
  'memory-hall': CellType.CAVE, 'scroll-archive': CellType.BOOKSHELF,
  'attention-pillar': CellType.PILLAR, 'gate-mechanism': CellType.STATUE,
  'context-window': CellType.COLUMN, 'forgetting-stone': CellType.ROCK,
  'recall-statue': CellType.STATUE,
  // Sky
  'pattern-weave': CellType.STAR_FLOWER, 'sampling-cloud': CellType.CLOUD,
  'temperature-breeze': CellType.FLOWER, 'diffusion-mist': CellType.CLOUD,
  'prompt-crystal': CellType.CRYSTAL, 'latent-space': CellType.CLOUD,
  'creative-peak': CellType.RAINBOW,
};

const TEACHING_TRIGGERS: Record<string, CellType> = {
  'farm-sheep-first': CellType.SHEEP, 'farm-flock': CellType.SHEEP, 'farm-pen': CellType.PEN,
  'farm-elder': CellType.KENNEL, 'farm-grass': CellType.FIELD, 'farm-first-sort': CellType.PEN,
  'forest-path': CellType.PATH, 'forest-bridge': CellType.BRIDGE, 'forest-mushroom': CellType.MUSHROOM,
  'forest-deadend': CellType.TREE, 'forest-cave': CellType.CAVE, 'forest-water-crossing': CellType.WATER,
  'village-connections': CellType.HOUSE, 'village-center': CellType.CAMPFIRE, 'village-intersection': CellType.PATH,
  'village-weights': CellType.PATH, 'village-layers': CellType.HOUSE, 'village-fountain-hub': CellType.CAMPFIRE,
  'mountain-crystal': CellType.CRYSTAL, 'mountain-campfire': CellType.CAMPFIRE, 'mountain-summit': CellType.MOUNTAIN,
  'mountain-eagle': CellType.MOUNTAIN, 'mountain-practice': CellType.PATH, 'mountain-overfitting': CellType.MOUNTAIN,
  'meadow-reward': CellType.SHEEP, 'meadow-explore': CellType.FIELD, 'meadow-policy': CellType.PATH,
  'meadow-qvalue': CellType.CRYSTAL, 'meadow-reward-shape': CellType.FLOWER, 'meadow-delayed': CellType.SHEEP,
  'lake-stream': CellType.WATER, 'lake-filter': CellType.BRIDGE, 'lake-batch': CellType.ROCK,
  'lake-augment': CellType.FLOWER, 'lake-normalize': CellType.WATER, 'lake-pipeline': CellType.WATER,
  'ruins-memory': CellType.CAVE, 'ruins-scroll': CellType.BOOKSHELF, 'ruins-attention': CellType.PILLAR,
  'ruins-gate': CellType.STATUE, 'ruins-context': CellType.COLUMN, 'ruins-forgetting': CellType.ROCK,
  'sky-pattern': CellType.STAR_FLOWER, 'sky-sampling': CellType.CLOUD, 'sky-temperature': CellType.FLOWER,
  'sky-diffusion': CellType.CLOUD, 'sky-prompt': CellType.CRYSTAL, 'sky-creative': CellType.RAINBOW,
};

const LEVEL_STICKERS: Record<number, string> = {
  1: 'sticker-harvest-hero', 2: 'sticker-tree-finder', 3: 'sticker-path-maker',
  4: 'sticker-crystal-collector', 5: 'sticker-reward-hunter',
  6: 'sticker-island-hopper', 7: 'sticker-attention-master',
};

const WORLD_COMPLETION_STICKERS: Record<string, string> = {
  farm: 'sticker-good-pup', forest: 'sticker-bridge-builder',
  village: 'sticker-fountain-friend', mountain: 'sticker-crystal-collector',
  meadow: 'sticker-meadow-explorer', lake: 'sticker-lake-keeper',
  ruins: 'sticker-ruins-scholar', sky: 'sticker-sky-walker',
};

// ─── XP / Level helpers ────────────────────────────────────────────────

const XP_THRESHOLDS = [0, 50, 125, 250, 400, 600, 850];

export function computeLevel(xp: number): number {
  for (let i = XP_THRESHOLDS.length - 1; i >= 0; i--) {
    if (xp >= XP_THRESHOLDS[i]!) return i;
  }
  return 0;
}

// ─── Notification type ──────────────────────────────────────────────────

export interface GameNotification {
  id: string;
  text: string;
  emoji: string;
  type: 'discovery' | 'sticker' | 'xp' | 'levelup' | 'quest' | 'bark';
}

// ─── Store interface ────────────────────────────────────────────────────

export interface GameStore {
  // State
  gamePhase: 'menu' | 'playing' | 'teaching' | 'levelComplete' | 'worldSelect' | 'journal' | 'stickerBook' | 'questComplete' | 'cutscene' | 'dialog';
  currentWorld: string;
  playerPos: Position;
  playerFacing: Direction;
  discoveries: string[];
  stickers: string[];
  xp: number;
  level: number;
  teachingsSeen: string[];
  sheepInPen: number;
  totalSheep: number;
  currentTeaching: Teaching | null;
  showParentLayer: boolean;
  notifications: GameNotification[];
  sheepCollected: Set<string>;
  worldCompleted: string[];
  // v2.0 state
  activeQuests: string[];
  completedQuests: string[];
  questProgress: Record<string, number>;
  visitedCells: Set<string>;
  barkCount: number;
  timeHour: number;
  currentSeason: SeasonConfig['id'];
  sheepEntities: SheepEntity[];
  dialogSteps: { text: string; speaker: string }[];
  dialogStepIndex: number;
  stepsTaken: number;
  fogRevealed: Set<string>;
  lastBarkDir: Direction | null;
  lastBarkTime: number;
  tickCount: number;

  // Actions
  setPhase: (phase: GameStore['gamePhase']) => void;
  movePlayer: (dx: number, dy: number) => void;
  startWorld: (worldId: string) => void;
  collectSheep: (pos: Position) => void;
  triggerTeaching: (teachingId: string) => void;
  dismissTeaching: () => void;
  toggleParentLayer: () => void;
  addDiscovery: (discoveryId: string) => void;
  checkDiscoveries: (worldId: string, playerPos: Position, cellType: CellType) => void;
  checkTeachings: (worldId: string, playerPos: Position, cellType: CellType) => void;
  addNotification: (text: string, emoji: string, type: GameNotification['type']) => void;
  removeNotification: (id: string) => void;
  getWorld: () => WorldDef | undefined;
  // v2.0 actions
  bark: () => void;
  advanceDialog: () => void;
  dismissDialog: () => void;
  tick: () => void;
  checkQuests: () => void;
  getPlayerFacing: () => Direction;
}

// ─── The store ──────────────────────────────────────────────────────────

let notificationCounter = 0;
function nextNotifId(): string {
  notificationCounter += 1;
  return `notif-${Date.now()}-${notificationCounter}`;
}

export const useGameStore = create<GameStore>()((set, get) => ({
  gamePhase: 'menu',
  currentWorld: 'farm',
  playerPos: { x: 7, y: 14 },
  playerFacing: 'up',
  discoveries: [],
  stickers: [],
  xp: 0,
  level: 0,
  teachingsSeen: [],
  sheepInPen: 0,
  totalSheep: 0,
  currentTeaching: null,
  showParentLayer: false,
  notifications: [],
  sheepCollected: new Set(),
  worldCompleted: [],
  activeQuests: [],
  completedQuests: [],
  questProgress: {},
  visitedCells: new Set(),
  barkCount: 0,
  timeHour: 8,
  currentSeason: 'summer',
  sheepEntities: [],
  dialogSteps: [],
  dialogStepIndex: 0,
  stepsTaken: 0,
  fogRevealed: new Set(),
  lastBarkDir: null,
  lastBarkTime: 0,
  tickCount: 0,

  setPhase: (phase) => set({ gamePhase: phase }),

  getWorld: () => getWorldById(get().currentWorld),

  startWorld: (worldId) => {
    const world = getWorldById(worldId);
    if (!world) return;
    const entities = world.enableFlocking ? initSheepEntities(world) : [];
    const startFog = world.fogOfWar ? revealFog(world.playerStart, world.fogOfWar, world.width, world.height, new Set()) : new Set<string>();

    // Auto-start quests for this world
    const worldQuests = getQuestsForWorld(worldId);
    const autoQuests = worldQuests.filter(q => !q.hidden && !q.requiresDiscoveries);

    set({
      currentWorld: worldId,
      playerPos: { ...world.playerStart },
      gamePhase: 'playing',
      totalSheep: world.sheepPositions.length,
      sheepInPen: 0,
      sheepCollected: new Set(),
      currentTeaching: null,
      sheepEntities: entities,
      activeQuests: autoQuests.map(q => q.id),
      questProgress: Object.fromEntries(autoQuests.map(q => [q.id, 0])),
      visitedCells: new Set([`${world.playerStart.x},${world.playerStart.y}`]),
      barkCount: 0,
      stepsTaken: 0,
      fogRevealed: startFog,
      currentSeason: world.season,
      lastBarkDir: null,
      lastBarkTime: 0,
    });
  },

  movePlayer: (dx, dy) => {
    const state = get();
    if (state.gamePhase !== 'playing') return;

    const world = getWorldById(state.currentWorld);
    if (!world) return;

    // Update facing direction
    let facing: Direction = 'right';
    if (dx === 1) facing = 'right';
    else if (dx === -1) facing = 'left';
    else if (dy === -1) facing = 'up';
    else if (dy === 1) facing = 'down';

    const newX = state.playerPos.x + dx;
    const newY = state.playerPos.y + dy;

    if (newX < 0 || newX >= world.width || newY < 0 || newY >= world.height) return;
    const cell = world.grid[newY][newX];
    if (!cell.walkable) return;

    // Handle sheep collection
    if (cell.type === CellType.SHEEP) {
      const key = `${newX},${newY}`;
      if (!state.sheepCollected.has(key)) {
        get().collectSheep({ x: newX, y: newY });
        if (get().gamePhase === 'levelComplete') return;
      }
    }

    // Update visited cells
    const newVisited = new Set(state.visitedCells);
    newVisited.add(`${newX},${newY}`);

    // Update fog of war
    let newFog = state.fogRevealed;
    if (world.fogOfWar) {
      newFog = revealFog({ x: newX, y: newY }, world.fogOfWar, world.width, world.height, state.fogRevealed);
    }

    set({
      playerPos: { x: newX, y: newY },
      playerFacing: facing,
      stepsTaken: state.stepsTaken + 1,
      visitedCells: newVisited,
      fogRevealed: newFog,
    });

    if (get().gamePhase === 'playing') {
      get().checkDiscoveries(state.currentWorld, { x: newX, y: newY }, cell.type);
      get().checkTeachings(state.currentWorld, { x: newX, y: newY }, cell.type);
      get().checkQuests();
    }
  },

  collectSheep: (pos) => {
    const state = get();
    const key = `${pos.x},${pos.y}`;
    if (state.sheepCollected.has(key)) return;

    const newCollected = new Set(state.sheepCollected);
    newCollected.add(key);

    // Also mark the sheep entity as collected
    const newEntities = state.sheepEntities.map(s =>
      s.pos.x === pos.x && s.pos.y === pos.y ? { ...s, collected: true } : s
    );

    const newSheepInPen = state.sheepInPen + 1;
    let newXP = state.xp + 5;
    const newStickers = [...state.stickers];
    const newNotifications: GameNotification[] = [...state.notifications];
    const newWorldCompleted = [...state.worldCompleted];
    let newLevel = computeLevel(newXP);
    const newProgress = { ...state.questProgress };

    // Update sheep collection quest progress
    for (const qid of state.activeQuests) {
      const q = getQuestById(qid);
      if (q && q.type === 'collect_sheep') {
        newProgress[qid] = (newProgress[qid] ?? 0) + 1;
      }
    }

    const alreadyCompleted = newWorldCompleted.includes(state.currentWorld);
    const justCompleted = newSheepInPen >= state.totalSheep && !alreadyCompleted;

    if (justCompleted) {
      newWorldCompleted.push(state.currentWorld);
      newXP += 25;
      newLevel = computeLevel(newXP);

      const worldStickerId = WORLD_COMPLETION_STICKERS[state.currentWorld];
      if (worldStickerId) {
        const sd = allStickers.find((s) => s.id === worldStickerId);
        if (sd && !newStickers.includes(worldStickerId)) {
          newStickers.push(worldStickerId);
          newNotifications.push({ id: nextNotifId(), text: `Sticker: ${sd.name}`, emoji: sd.emoji, type: 'sticker' });
        }
      }

      if (newWorldCompleted.length >= allWorlds.length) {
        const ms = 'sticker-mist-master';
        if (!newStickers.includes(ms)) newStickers.push(ms);
        newNotifications.push({ id: nextNotifId(), text: 'MIST Master! All worlds complete!', emoji: '‏\u{1F3C6}', type: 'levelup' });
      }
    }

    if (newLevel > state.level) {
      newNotifications.push({ id: nextNotifId(), text: `Level Up! Now ${LevelNames[newLevel]}!`, emoji: '‏\u{1F389}', type: 'levelup' });
      const ls = LEVEL_STICKERS[newLevel];
      if (ls && !newStickers.includes(ls)) {
        const sd = allStickers.find((s) => s.id === ls);
        if (sd) {
          newStickers.push(ls);
          newNotifications.push({ id: nextNotifId(), text: `Sticker: ${sd.name}`, emoji: sd.emoji, type: 'sticker' });
        }
      }
    }

    set({
      sheepCollected: newCollected,
      sheepEntities: newEntities,
      sheepInPen: newSheepInPen,
      xp: newXP,
      level: newLevel,
      stickers: newStickers,
      notifications: newNotifications,
      worldCompleted: newWorldCompleted,
      questProgress: newProgress,
      ...(justCompleted ? { gamePhase: 'levelComplete' as const } : {}),
    });
  },

  triggerTeaching: (teachingId) => {
    const state = get();
    if (state.teachingsSeen.includes(teachingId)) return;
    const teaching = getTeachingById(teachingId);
    if (!teaching) return;

    // Check requiresDiscoveries
    if (teaching.requiresDiscoveries) {
      const hasAll = teaching.requiresDiscoveries.every(d => state.discoveries.includes(d));
      if (!hasAll) return;
    }

    // Award XP for teaching
    const newXP = state.xp + 3;
    const newLevel = computeLevel(newXP);

    if (teaching.dialogSteps && teaching.dialogSteps.length > 0 && teaching.major) {
      set({
        dialogSteps: teaching.dialogSteps,
        dialogStepIndex: 0,
        gamePhase: 'cutscene',
        teachingsSeen: [...state.teachingsSeen, teachingId],
        xp: newXP,
        level: newLevel,
      });
    } else {
      set({
        currentTeaching: teaching,
        teachingsSeen: [...state.teachingsSeen, teachingId],
        gamePhase: 'teaching',
        xp: newXP,
        level: newLevel,
      });
    }
  },

  dismissTeaching: () => set({ currentTeaching: null, gamePhase: 'playing' }),
  toggleParentLayer: () => set((s) => ({ showParentLayer: !s.showParentLayer })),

  addDiscovery: (discoveryId) => {
    const state = get();
    if (state.discoveries.includes(discoveryId)) return;
    const discovery = getDiscoveryById(discoveryId);
    if (!discovery) return;

    const newXP = state.xp + discovery.xp;
    const newLevel = computeLevel(newXP);
    const newStickers = [...state.stickers];
    const newNotifications: GameNotification[] = [
      ...state.notifications,
      { id: nextNotifId(), text: `Discovery: ${discovery.name}`, emoji: discovery.emoji, type: 'discovery' },
    ];
    const newProgress = { ...state.questProgress };
    const newActiveQuests = [...state.activeQuests];

    // Update discovery quest progress
    for (const qid of state.activeQuests) {
      const q = getQuestById(qid);
      if (q && q.type === 'find_discovery') {
        newProgress[qid] = (newProgress[qid] ?? 0) + 1;
      }
    }

    // Check if any hidden quests should unlock
    const allWorldQuests = getQuestsForWorld(state.currentWorld);
    for (const q of allWorldQuests) {
      if (q.hidden && q.requiresDiscoveries && !newActiveQuests.includes(q.id) && !state.completedQuests.includes(q.id)) {
        const hasAll = q.requiresDiscoveries.every(d => state.discoveries.includes(d) || d === discoveryId);
        if (hasAll) {
          newActiveQuests.push(q.id);
          newProgress[q.id] = 0;
          newNotifications.push({ id: nextNotifId(), text: `New Quest: ${q.name}!`, emoji: q.emoji, type: 'quest' });
        }
      }
    }

    if (newLevel > state.level) {
      newNotifications.push({ id: nextNotifId(), text: `Level Up! Now ${LevelNames[newLevel]}!`, emoji: '‏\u{1F389}', type: 'levelup' });
      const ls = LEVEL_STICKERS[newLevel];
      if (ls && !newStickers.includes(ls)) {
        const sd = allStickers.find((s) => s.id === ls);
        if (sd) { newStickers.push(ls); newNotifications.push({ id: nextNotifId(), text: `Sticker: ${sd.name}`, emoji: sd.emoji, type: 'sticker' }); }
      }
    }

    set({
      discoveries: [...state.discoveries, discoveryId], xp: newXP, level: newLevel,
      stickers: newStickers, notifications: newNotifications, questProgress: newProgress, activeQuests: newActiveQuests,
    });
  },

  checkDiscoveries: (worldId, playerPos, cellType) => {
    const state = get();
    if (state.gamePhase !== 'playing') return;
    const world = getWorldById(worldId);
    if (!world) return;
    for (const discovery of world.discoveries) {
      if (state.discoveries.includes(discovery.id)) continue;
      const triggerType = DISCOVERY_TRIGGERS[discovery.id];
      if (triggerType && cellType === triggerType) { get().addDiscovery(discovery.id); return; }
    }
  },

  checkTeachings: (worldId, playerPos, _cellType) => {
    const state = get();
    if (state.gamePhase !== 'playing') return;
    const world = getWorldById(worldId);
    if (!world) return;
    for (const teaching of world.teachings) {
      if (state.teachingsSeen.includes(teaching.id)) continue;
      if (teaching.requiresDiscoveries) {
        const hasAll = teaching.requiresDiscoveries.every(d => state.discoveries.includes(d));
        if (!hasAll) continue;
      }
      const triggerType = TEACHING_TRIGGERS[teaching.id];
      if (!triggerType) continue;
      let found = false;
      for (let dy = -1; dy <= 1 && !found; dy++) {
        for (let dx = -1; dx <= 1 && !found; dx++) {
          const cx = playerPos.x + dx; const cy = playerPos.y + dy;
          if (cx < 0 || cx >= world.width || cy < 0 || cy >= world.height) continue;
          if (world.grid[cy][cx].type === triggerType) found = true;
        }
      }
      if (found) { get().triggerTeaching(teaching.id); return; }
    }
  },

  // v2.0: Bark action
  bark: () => {
    const state = get();
    if (state.gamePhase !== 'playing') return;
    const world = getWorldById(state.currentWorld);
    if (!world || !world.enableBark) return;

    const result = computeBark(state.playerPos, state.playerFacing, state.sheepEntities);
    const newBarkCount = state.barkCount + 1;
    const newProgress = { ...state.questProgress };

    for (const qid of state.activeQuests) {
      const q = getQuestById(qid);
      if (q && q.type === 'bark_count') {
        newProgress[qid] = newBarkCount;
      }
    }

    set({
      lastBarkDir: result.direction,
      lastBarkTime: state.tickCount,
      barkCount: newBarkCount,
      questProgress: newProgress,
    });

    if (result.sheepInfluenced > 0) {
 get().addNotification(`Woof! ${result.sheepInfluenced} sheep heard you!`, '‏\u{1F415}', 'bark');
    }
  },

  // v2.0: Dialog advancement
  advanceDialog: () => {
    const state = get();
    const nextIdx = state.dialogStepIndex + 1;
    if (nextIdx >= state.dialogSteps.length) {
 set({ dialogSteps: [], dialogStepIndex: 0, gamePhase: 'playing' });
    } else {
      set({ dialogStepIndex: nextIdx });
    }
  },

  dismissDialog: () => set({ dialogSteps: [], dialogStepIndex: 0, gamePhase: 'playing' }),

  // v2.0: Game tick (called every frame for flocking, time)
  tick: () => {
    const state = get();
    if (state.gamePhase !== 'playing') return;
    const world = getWorldById(state.currentWorld);
    if (!world) return;

    const newTick = state.tickCount + 1;
    let newEntities = state.sheepEntities;

    // Update flocking every 3 ticks
    if (world.enableFlocking && newTick % 3 === 0) {
      newEntities = updateFlocking(
        state.sheepEntities, world, state.playerPos,
        state.lastBarkDir, state.lastBarkTime, newTick,
      );
    }

    // Advance time every 600 ticks (~10 seconds at 60fps)
    let newTime = state.timeHour;
    if (newTick % 600 === 0) {
      newTime = ((state.timeHour + 1) % 24 + 24) % 24;
    }

    set({ sheepEntities: newEntities, timeHour: newTime, tickCount: newTick });
  },

  // v2.0: Check quest completion
  checkQuests: () => {
    const state = get();
    if (state.gamePhase !== 'playing') return;
    const world = getWorldById(state.currentWorld);
    if (!world) return;

    const newCompleted = [...state.completedQuests];
    const newStickers = [...state.stickers];
    const newNotifications: GameNotification[] = [...state.notifications];
    const newXP = state.xp;
    const newActiveQuests = [...state.activeQuests];
    let xpGain = 0;

    for (const qid of state.activeQuests) {
      if (newCompleted.includes(qid)) continue;
      const q = getQuestById(qid);
      if (!q) continue;

      let progress = state.questProgress[qid] ?? 0;

      switch (q.type) {
        case 'explore_cells':
          progress = state.visitedCells.size;
          break;
        case 'reach_position':
          if (q.targetPos && state.playerPos.x === q.targetPos.x && state.playerPos.y === q.targetPos.y) {
            progress = 1;
          }
          break;
      }

      if (progress >= q.target) {
        newCompleted.push(qid);
        xpGain += q.xpReward;
        newNotifications.push({ id: nextNotifId(), text: `Quest Complete: ${q.name}!`, emoji: q.emoji, type: 'quest' });

        if (q.stickerReward && !newStickers.includes(q.stickerReward)) {
          const sd = allStickers.find((s) => s.id === q.stickerReward);
          if (sd) { newStickers.push(q.stickerReward); newNotifications.push({ id: nextNotifId(), text: `Sticker: ${sd.name}`, emoji: sd.emoji, type: 'sticker' }); }
        }
      }
    }

    if (xpGain > 0) {
      const newLevel = computeLevel(newXP + xpGain);
      set({
        completedQuests: newCompleted, stickers: newStickers, notifications: newNotifications,
        xp: newXP + xpGain, level: newLevel, activeQuests: newActiveQuests,
      });
    }
  },

  getPlayerFacing: () => get().playerFacing,

  addNotification: (text, emoji, type) => {
    set((s) => ({ notifications: [...s.notifications, { id: nextNotifId(), text, emoji, type }] }));
  },

  removeNotification: (id) => {
    set((s) => ({ notifications: s.notifications.filter((n) => n.id !== id) }));
  },
}));
