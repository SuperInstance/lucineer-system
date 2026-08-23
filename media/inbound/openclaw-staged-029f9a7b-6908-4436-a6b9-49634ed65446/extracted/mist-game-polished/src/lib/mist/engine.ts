// ============================================================
// MIST — Game Engine (Zustand Store)
// The heart: game loop, state management, all mechanics
// ============================================================

import { create } from 'zustand';
import {
  GameState, GameScreen, DogEntity, SheepEntity, Tile, TileType,
  LevelDef, InputState, DogAbility, Rank, Weather, Season,
  Particle, ParticleType, SaveData, LevelResult, Direction, SeededRNG,
  DOG_SPEED, STAMINA_MAX, STAMINA_DRAIN_RATE, STAMINA_REGEN_RATE,
  BARK_BASE_RADIUS, BARK_COOLDOWN, TILE_SIZE,
} from './types';
import { RANK_FLOCKING_PRESETS, FlockingParams, updateFlocking, checkPenEntries, checkLostSheep } from './flocking';
import { generateTerrain, spawnSheep, spawnCollectibles, spawnObstacles, isTileInPen } from './procedural';
import { LEVELS, DIALOG_TREE, calculateStars, isLevelUnlocked, getLevelById } from './levels';
import { SKILL_TREE, canUnlockSkill } from './skills';
import { ALL_DISCOVERIES, ALL_STICKERS, BREED_INFO, ALL_FARM_UPGRADES } from './collections';
import { loadSave, saveSave, saveLevelResult, saveDiscovery, saveBreedCatalog, unlockSkill, saveDailyChallenge, createNewSave, resetSave as resetSaveData } from './save';
import { generateDailyChallenge, getTodayString, getDailyWeather, getDailyBreeds } from './daily';

export interface MistStore extends GameState {
  // Save data
  saveData: SaveData;
  // Input
  input: InputState;
  // Flocking params (for sandbox)
  flockingParams: FlockingParams;
  // Camera
  cameraOffset: { x: number; y: number };
  // Animation
  frameCount: number;
  lastTime: number;
  // Actions
  init: () => void;
  setScreen: (screen: GameScreen) => void;
  startLevel: (levelId: string) => void;
  startDailyChallenge: () => void;
  updateGame: (dt: number) => void;
  handleKeyDown: (key: string) => void;
  handleKeyUp: (key: string) => void;
  bark: () => void;
  useAbility: () => void;
  advanceDialog: (choiceId?: string) => void;
  collectDiscovery: (entityId: string) => void;
  completeLevel: () => void;
  unlockSkillAction: (skillId: string) => void;
  resetSave: () => void;
  setSandboxParam: (key: string, value: number | boolean) => void;
}

const DEFAULT_INPUT: InputState = {
  direction: 'none',
  bark: false,
  ability: false,
  pause: false,
  interact: false,
  menu: false,
};

const DEFAULT_WEATHER: Weather = Weather.Clear;

function createDogEntity(pos: { x: number; y: number }, unlockedAbilities: string[]): DogEntity {
  const abilities = unlockedAbilities
    .map(id => SKILL_TREE.find(s => s.id === id)?.effect.ability)
    .filter(Boolean) as DogAbility[];

  return {
    id: 'dog_player',
    type: 'dog' as never,
    pos: { ...pos },
    vel: { x: 0, y: 0 },
    facing: 'down',
    stamina: STAMINA_MAX,
    barkRadius: BARK_BASE_RADIUS,
    barkCooldown: 0,
    isBarking: false,
    isMoving: false,
    animFrame: 0,
    abilities,
    activeAbility: abilities.includes(DogAbility.GuideBark) ? DogAbility.GuideBark : null,
    dashTimer: 0,
    tunnelTarget: null,
  };
}

export const useMistStore = create<MistStore>((set, get) => ({
  // Initial state
  screen: 'title' as GameScreen,
  currentLevel: null,
  grid: [],
  gridWidth: 0,
  gridHeight: 0,
  entities: [],
  dog: null,
  sheep: [],
  collectibles: [],
  obstacles: [],
  particles: [],
  timer: 0,
  barksUsed: 0,
  sheepInPen: 0,
  sheepLost: 0,
  totalSheep: 0,
  discoveriesThisLevel: [],
  isPaused: false,
  isComplete: false,
  weather: {
    current: DEFAULT_WEATHER,
    intensity: 0,
    windDir: { x: 0, y: 0 },
    particles: [],
    transitionTimer: 0,
  },
  season: Season.Spring,
  currentDialog: null,
  dialogHistory: [],
  activeTutorial: null,
  tutorialIndex: 0,
  sandboxParams: {
    separation: 1.5,
    alignment: 1.0,
    cohesion: 1.0,
    sheepCount: 10,
    showVectors: false,
    showFlocks: true,
    placeObstacles: false,
    weather: Weather.Clear,
    barkType: DogAbility.GuideBark,
  },
  saveData: createNewSave(),
  input: DEFAULT_INPUT,
  flockingParams: RANK_FLOCKING_PRESETS.apprentice,
  cameraOffset: { x: 0, y: 0 },
  frameCount: 0,
  lastTime: 0,

  init: () => {
    const save = loadSave();
    set({ saveData: save });
  },

  setScreen: (screen) => set({ screen }),

  startLevel: (levelId) => {
    const level = getLevelById(levelId);
    if (!level) return;

    const save = get().saveData;
    const isDaily = false;
    // Use level seed + current day for variation on replay
    const dayVariation = Date.now() % 10000;
    const seed = level.terrainSeed + (save.levelResults[levelId] ? dayVariation : 0);

    const grid = generateTerrain(level.gridSize.x, level.gridSize.y, seed, level.weather);
    const rng = new SeededRNG(seed);
    const sheep = spawnSheep(level, grid, rng);
    const collectibles = spawnCollectibles(level, grid, rng);
    const obstacles = spawnObstacles(level, grid, rng);
    const dog = createDogEntity({ x: 2, y: 2 }, save.unlockedSkills);

    const flockingParams = RANK_FLOCKING_PRESETS[level.rank] || RANK_FLOCKING_PRESETS.apprentice;

    // Apply skill bonuses to dog
    const speedSkill = save.unlockedSkills.find(id => SKILL_TREE.find(s => s.id === id)?.effect.stat === 'speed');
    const barkRadSkill = save.unlockedSkills.find(id => SKILL_TREE.find(s => s.id === id)?.effect.stat === 'bark_radius');
    if (barkRadSkill) dog.barkRadius *= 1.25;

    set({
      screen: 'game',
      currentLevel: level,
      grid,
      gridWidth: level.gridSize.x,
      gridHeight: level.gridSize.y,
      dog,
      sheep,
      collectibles,
      obstacles,
      particles: [],
      timer: 0,
      barksUsed: 0,
      sheepInPen: 0,
      sheepLost: 0,
      totalSheep: sheep.length,
      discoveriesThisLevel: [],
      isPaused: false,
      isComplete: false,
      weather: { current: level.weather, intensity: 0.5, windDir: { x: 0, y: 0 }, particles: [], transitionTimer: 0 },
      currentDialog: level.dialogIntro,
      dialogHistory: [],
      activeTutorial: level.tutorialSteps?.[0] ?? null,
      tutorialIndex: 0,
      flockingParams,
      entities: [dog, ...sheep, ...collectibles, ...obstacles],
    });
  },

  startDailyChallenge: () => {
    const challenge = generateDailyChallenge();
    const save = get().saveData;
    const existing = save.dailyChallenges[getTodayString()];
    if (existing?.completed) {
      set({ screen: 'daily_challenge' });
      return;
    }

    let dailyWeather = getDailyWeather(challenge.seed);
    const gridSize = { x: 18, y: 12 };
    const sheepCount = challenge.specialRules.find(r => r.type === 'many_sheep')?.value ?? 8;
    const breeds = getDailyBreeds(challenge.seed, sheepCount);
    const grid = generateTerrain(gridSize.x, gridSize.y, challenge.seed, dailyWeather);

    const rng = new SeededRNG(challenge.seed);
    const sheep = spawnSheep({
      ...LEVELS[0],
      sheepCount,
      sheepBreeds: breeds,
      terrainSeed: challenge.seed,
      weather: dailyWeather,
      gridSize,
      obstacles: [],
      discoveries: [],
      objective: { type: 'herd_all', description: challenge.description },
      dialogIntro: { id: 'daily-intro', speaker: 'elder_bark', text: challenge.description, emotion: 'playful' as const },
      dialogOutro: { id: 'daily-outro', speaker: 'elder_bark', text: 'Daily challenge complete! Come back tomorrow for a new one!', emotion: 'proud' as const },
      parentLayerContent: { title: 'Daily Challenge', conceptName: 'Practice', whatHappened: '', aiConnection: '', tryAtHome: '', ageAppropriate: '' },
    }, grid, rng);

    const dog = createDogEntity({ x: 2, y: 2 }, save.unlockedSkills);
    const flockingParams = { ...RANK_FLOCKING_PRESETS.journeyman };
    const constraints: Record<string, any> = {};
    challenge.specialRules.forEach(rule => {
      if (rule.type === 'fast_sheep') flockingParams.speed *= (rule.value ?? 1.4);
      if (rule.type === 'low_stamina') constraints.staminaDrain = (rule.value ?? 0.6) * 16;
      if (rule.type === 'fog_always') dailyWeather = Weather.Foggy;
      if (rule.type === 'mirrored') (dog as any)._mirrored = true;
      if (rule.type === 'no_bark_limit') constraints.maxBarks = 0;
    });

    set({
      screen: 'game',
      currentLevel: {
        ...LEVELS[0],
        id: 'daily',
        name: challenge.levelName,
        description: challenge.description,
        sheepCount,
        weather: dailyWeather,
        gridSize,
        objective: { type: 'herd_all', description: challenge.description },
        constraints,
      },
      grid,
      gridWidth: gridSize.x,
      gridHeight: gridSize.y,
      dog,
      sheep,
      collectibles: [],
      obstacles: [],
      particles: [],
      timer: 0,
      barksUsed: 0,
      sheepInPen: 0,
      sheepLost: 0,
      totalSheep: sheep.length,
      discoveriesThisLevel: [],
      isPaused: false,
      isComplete: false,
      weather: { current: dailyWeather, intensity: 0.5, windDir: { x: 0, y: 0 }, particles: [], transitionTimer: 0 },
      currentDialog: { id: 'daily-intro', speaker: 'elder_bark', text: `Daily Challenge: ${challenge.levelName}! ${challenge.description}`, emotion: 'playful' },
      dialogHistory: [],
      activeTutorial: null,
      tutorialIndex: 0,
      flockingParams,
      entities: [dog, ...sheep],
    });
  },

  updateGame: (dt) => {
    const state = get();
    if (state.isPaused || state.isComplete || !state.dog || !state.currentLevel || state.currentDialog) return;

    const dog = { ...state.dog };
    const input = state.input;
    const grid = state.grid;
    const gw = state.gridWidth;
    const gh = state.gridHeight;

    // Update timer
    const newTimer = state.timer + dt;

    // --- Dog Movement ---
    let speed = DOG_SPEED * dt;
    if (dog.abilities.includes(DogAbility.Dash) && dog.dashTimer > 0) {
      speed *= 2.5;
      dog.dashTimer -= dt;
    }

    const save = state.saveData;
    const speedSkill = save.unlockedSkills.find(id => SKILL_TREE.find(s => s.id === id)?.effect.stat === 'speed');
    if (speedSkill) speed *= 1.15;
    // Stamina skill bonus (regen)
    const regenSkill = get().saveData.unlockedSkills.find(id => SKILL_TREE.find(s => s.id === id)?.effect.stat === 'stamina');
    if (regenSkill) dog.stamina = Math.min(STAMINA_MAX, dog.stamina + STAMINA_REGEN_RATE * 1.5 * dt);

    let dx = 0, dy = 0;
    // Support mirrored controls (daily challenge rule)
    const isMirrored = (dog as any)._mirrored === true;
    switch (input.direction) {
      case 'up': dy = -speed; dog.facing = 'up'; break;
      case 'down': dy = speed; dog.facing = 'down'; break;
      case 'left': dx = isMirrored ? speed : -speed; dog.facing = isMirrored ? 'right' : 'left'; break;
      case 'right': dx = isMirrored ? -speed : speed; dog.facing = isMirrored ? 'left' : 'right'; break;
    }

    dog.isMoving = dx !== 0 || dy !== 0;
    if (dog.isMoving) {
      dog.animFrame = (dog.animFrame + dt * 8) % 4;
      // Stamina drain
      const drainMult = state.currentLevel.constraints.staminaDrain ? state.currentLevel.constraints.staminaDrain / 8 : 1;
      dog.stamina = Math.max(0, dog.stamina - STAMINA_DRAIN_RATE * drainMult * dt);
    } else {
      dog.animFrame = 0;
      dog.stamina = Math.min(STAMINA_MAX, dog.stamina + STAMINA_REGEN_RATE * dt);
    }

    // Apply movement with collision
    if (dog.stamina > 0) {
      const newPosX = dog.pos.x + dx;
      const newPosY = dog.pos.y + dy;
      const tileX = Math.round(newPosX);
      const tileY = Math.round(newPosY);
      const targetTile = grid[tileY]?.[tileX];

      if (targetTile?.walkable) {
        dog.pos.x = Math.max(0.5, Math.min(gw - 1.5, newPosX));
        dog.pos.y = Math.max(0.5, Math.min(gh - 1.5, newPosY));
      } else {
        // Try sliding
        const slideX = grid[Math.round(dog.pos.y)]?.[Math.round(newPosX)];
        const slideY = grid[Math.round(newPosY)]?.[Math.round(dog.pos.x)];
        if (dx !== 0 && slideX?.walkable) dog.pos.x = Math.max(0.5, Math.min(gw - 1.5, newPosX));
        else if (dy !== 0 && slideY?.walkable) dog.pos.y = Math.max(0.5, Math.min(gh - 1.5, newPosY));
      }
    }

    // Bark cooldown
    if (dog.barkCooldown > 0) dog.barkCooldown -= dt;
    if (dog.barkCooldown <= -0.1) dog.isBarking = false;

    // --- Flocking Update ---
    const sheep = [...state.sheep];
    updateFlocking(sheep, dog, grid, gw, gh, state.flockingParams, dt);

    // --- Check Pen Entries ---
    const { newlyPenned, count: newSheepInPen } = checkPenEntries(sheep, gw, gh);

    // --- Check Lost Sheep ---
    const newlyLost = checkLostSheep(sheep, gw, gh);

    // --- Check Discoveries ---
    const collectibles = [...state.collectibles];
    const newDiscoveries: string[] = [...state.discoveriesThisLevel];
    for (const c of collectibles) {
      if (c.discovered) continue;
      const dist = Math.sqrt((dog.pos.x - c.pos.x) ** 2 + (dog.pos.y - c.pos.y) ** 2);
      if (dist < 1.2) {
        c.discovered = true;
        newDiscoveries.push(c.conceptKey);
        // Persist discovery immediately (not just on level complete)
        let save = get().saveData;
        save = saveDiscovery(save, c.conceptKey);
        if (c.conceptKey.startsWith('breed_')) {
          save = saveBreedCatalog(save, c.conceptKey.replace('breed_', '') as any);
        }
        saveSave(save);
        // Add sparkle particles
        const particles: Particle[] = [];
        for (let i = 0; i < 8; i++) {
          const angle = (i / 8) * Math.PI * 2;
          particles.push({
            id: `p_${Date.now()}_${i}`,
            pos: { ...c.pos },
            vel: { x: Math.cos(angle) * 2, y: Math.sin(angle) * 2 },
            life: 1.0,
            maxLife: 1.0,
            color: '#FFD700',
            size: 4,
            particleType: ParticleType.Sparkle,
          });
        }
        set(s => ({ particles: [...s.particles, ...particles] }));
      }
    }

    // --- Update Particles ---
    const particles = state.particles
      .map(p => ({
        ...p,
        pos: { x: p.pos.x + p.vel.x * dt, y: p.pos.y + p.vel.y * dt },
        life: p.life - dt,
        vel: { x: p.vel.x * 0.95, y: p.vel.y * 0.95 },
      }))
      .filter(p => p.life > 0);

    // --- Weather Particles ---
    if (state.weather.current === Weather.Rainy || state.weather.current === Weather.Snowy) {
      const isRain = state.weather.current === Weather.Rainy;
      if (Math.random() < 0.3) {
        particles.push({
          id: `wp_${Date.now()}`,
          pos: { x: Math.random() * gw, y: 0 },
          vel: { x: state.weather.windDir.x * 0.5, y: isRain ? 8 : 1.5 },
          life: 2,
          maxLife: 2,
          color: isRain ? '#7BA7CC' : '#FFFFFF',
          size: isRain ? 2 : 3,
          particleType: isRain ? ParticleType.Rain : ParticleType.Snow,
        });
      }
    }

    // --- Check Level Complete ---
    const level = state.currentLevel;
    const allPenned = newSheepInPen >= state.totalSheep;
    const timeUp = level.objective.timeLimit ? newTimer >= level.objective.timeLimit : false;
    const tooManyLost = level.objective.maxLostSheep ? newlyLost.length > level.objective.maxLostSheep : false;
    const isComplete = allPenned || timeUp || tooManyLost;

    set({
      dog,
      sheep,
      collectibles,
      particles,
      timer: newTimer,
      sheepInPen: newSheepInPen,
      sheepLost: sheep.filter(s => s.isLost).length,
      discoveriesThisLevel: newDiscoveries,
      isComplete,
      frameCount: state.frameCount + 1,
    });

    if (isComplete) {
      // Use a frame-count delay instead of setTimeout to avoid stale state
      get().completeLevel();
    }
  },

  handleKeyDown: (key) => {
    const state = get();
    if (state.screen !== 'game' || state.isComplete) return;

    let direction: Direction = 'none';
    switch (key) {
      case 'ArrowUp': case 'w': case 'W': direction = 'up'; break;
      case 'ArrowDown': case 's': case 'S': direction = 'down'; break;
      case 'ArrowLeft': case 'a': case 'A': direction = 'left'; break;
      case 'ArrowRight': case 'd': case 'D': direction = 'right'; break;
      case ' ': case 'Space':
        if (!state.currentDialog) get().bark();
        return;
      case 'Escape':
        if (state.currentDialog) get().advanceDialog();
        else set({ isPaused: !state.isPaused });
        return;
      case 'e': case 'E':
        if (state.currentDialog) get().advanceDialog();
        return;
      case 'q': case 'Q':
        if (!state.currentDialog) get().useAbility();
        return;
    }
    set({ input: { ...state.input, direction } });
  },

  handleKeyUp: (key) => {
    const state = get();
    const currentDir = state.input.direction;
    let stillHeld = false;
    switch (key) {
      case 'ArrowUp': case 'w': case 'W': stillHeld = currentDir !== 'up'; break;
      case 'ArrowDown': case 's': case 'S': stillHeld = currentDir !== 'down'; break;
      case 'ArrowLeft': case 'a': case 'A': stillHeld = currentDir !== 'left'; break;
      case 'ArrowRight': case 'd': case 'D': stillHeld = currentDir !== 'right'; break;
    }
    if (stillHeld) return; // Another direction key still held
    set({ input: { ...state.input, direction: 'none' } });
  },

  bark: () => {
    const state = get();
    if (!state.dog || state.dog.barkCooldown > 0) return;

    const maxBarks = state.currentLevel?.constraints.maxBarks;
    if (maxBarks && state.barksUsed >= maxBarks) return;

    const dog = { ...state.dog };
    dog.isBarking = true;
    dog.barkCooldown = BARK_COOLDOWN;

    // Bark cooldown skill reduction
    const save = state.saveData;
    const cdSkill = save.unlockedSkills.find(id => SKILL_TREE.find(s => s.id === id)?.effect.stat === 'bark_cooldown');
    if (cdSkill) dog.barkCooldown *= 0.75;

    // Add bark particles
    const particles: Particle[] = [];
    const facingDirs: Record<string, { x: number; y: number }> = {
      up: { x: 0, y: -1 }, down: { x: 0, y: 1 }, left: { x: -1, y: 0 }, right: { x: 1, y: 0 },
    };
    const dir = facingDirs[dog.facing];
    for (let i = 0; i < 6; i++) {
      const spread = (Math.random() - 0.5) * 0.8;
      particles.push({
        id: `bark_${Date.now()}_${i}`,
        pos: { ...dog.pos },
        vel: { x: dir.x * 3 + spread, y: dir.y * 3 + spread },
        life: 0.5,
        maxLife: 0.5,
        color: '#FFFFFF',
        size: 6,
        particleType: ParticleType.Bark,
      });
    }

    set({
      dog,
      barksUsed: state.barksUsed + 1,
      particles: [...state.particles, ...particles],
    });
  },

  useAbility: () => {
    const state = get();
    if (!state.dog || state.dog.abilities.length === 0) return;

    const dog = { ...state.dog };
    const currentIndex = dog.abilities.indexOf(dog.activeAbility ?? DogAbility.Dash);
    const nextIndex = (currentIndex + 1) % dog.abilities.length;
    dog.activeAbility = dog.abilities[nextIndex];

    // Dash
    if (dog.activeAbility === DogAbility.Dash) {
      dog.dashTimer = 0.3;
    }

    set({ dog });
  },

  advanceDialog: (choiceId) => {
    const state = get();
    if (!state.currentDialog) return;

    // Check dialog tree for next node
    const nextId = choiceId ?? state.currentDialog.nextId;
    if (!nextId) {
      // Dialog ended — return to game or show outro
      if (state.isComplete && state.currentLevel?.dialogOutro) {
        // Level just completed, show outro
        // Already handled in completeLevel
      }
      set({ currentDialog: null });
      return;
    }

    const nextDialog = DIALOG_TREE[nextId];
    if (nextDialog) {
      set({
        currentDialog: {
          id: nextId,
          speaker: (nextDialog as any).speaker ?? 'elder_bark',
          text: nextDialog.text,
          emotion: nextDialog.emotion as any,
          choices: nextDialog.choices,
          unlockConcept: nextDialog.unlockConcept,
        },
        dialogHistory: [...state.dialogHistory, state.currentDialog.id],
      });
    } else {
      set({ currentDialog: null });
    }
  },

  collectDiscovery: (entityId) => {
    const state = get();
    const collectible = state.collectibles.find(c => c.id === entityId);
    if (!collectible || collectible.discovered) return;

    const updatedCollectibles = state.collectibles.map(c =>
      c.id === entityId ? { ...c, discovered: true } : c
    );
    const newDiscoveries = [...state.discoveriesThisLevel, collectible.conceptKey];

    // Update save
    let save = state.saveData;
    save = saveDiscovery(save, collectible.conceptKey);
    if (collectible.conceptKey.startsWith('breed_')) {
      save = saveBreedCatalog(save, collectible.conceptKey.replace('breed_', '') as any);
    }
    saveSave(save);

    set({
      collectibles: updatedCollectibles,
      discoveriesThisLevel: newDiscoveries,
      saveData: save,
    });
  },

  completeLevel: () => {
    const state = get();
    if (!state.currentLevel) return;

    const level = state.currentLevel;
    const stars = calculateStars(
      level,
      state.timer,
      state.sheepInPen,
      state.totalSheep,
      state.barksUsed,
      state.discoveriesThisLevel.length,
      level.discoveries.length,
    );

    const result: LevelResult = {
      levelId: level.id,
      stars,
      time: state.timer,
      sheepHerded: state.sheepInPen,
      sheepTotal: state.totalSheep,
      barksUsed: state.barksUsed,
      discoveriesFound: state.discoveriesThisLevel.length,
      personalBest: false,
      newDiscoveries: state.discoveriesThisLevel,
    };

    // Save result
    let save = state.saveData;
    save = saveLevelResult(save, result);
    for (const d of state.discoveriesThisLevel) {
      save = saveDiscovery(save, d);
    }
    saveSave(save);

    // Show outro dialog if all sheep herded
    if (stars >= 1 && level.dialogOutro) {
      set({
        screen: 'level_complete',
        isComplete: true,
        saveData: save,
        currentDialog: level.dialogOutro,
      });
    } else {
      set({
        screen: 'level_complete',
        isComplete: true,
        saveData: save,
      });
    }
  },

  unlockSkillAction: (skillId) => {
    const state = get();
    const skill = SKILL_TREE.find(s => s.id === skillId);
    if (!skill || !canUnlockSkill(skillId, state.saveData.unlockedSkills, state.saveData.skillPoints)) return;

    let save = unlockSkill(state.saveData, skillId, skill.cost);
    saveSave(save);
    set({ saveData: save });
  },

  resetSave: () => {
    const save = resetSaveData();
    saveSave(save);
    set({ saveData: save, screen: 'title' });
  },

  setSandboxParam: (key, value) => {
    set(s => ({
      sandboxParams: { ...s.sandboxParams, [key]: value },
    }));
  },
}));
