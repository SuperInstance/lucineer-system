// ============================================================// MIST — Core Type Definitions// ============================================================

// --- Primitives ---
export interface Vec2 {
  x: number;
  y: number;
}

export interface Vec3 {
  x: number;
  y: number;
  z: number;
}

// --- Tile & Terrain ---
export enum TileType {
  Grass = 'grass',
  TallGrass = 'tall_grass',
  Dirt = 'dirt',
  Stone = 'stone',
  Water = 'water',
  Flowers = 'flowers',
  Mud = 'mud',
  Bridge = 'bridge',
  Fence = 'fence',
  Gate = 'gate',
  PenFloor = 'pen_floor',
  Bush = 'bush',
  Tree = 'tree',
  Rock = 'rock',
  Fog = 'fog',
  Ice = 'ice',
  Sand = 'sand',
  Clover = 'clover',
  Path = 'path',
}

export enum TileVariant {
  A = 'a',
  B = 'b',
  C = 'c',
  D = 'd',
}

export interface Tile {
  type: TileType;
  variant: TileVariant;
  elevation: number; // 0-3 for isometric feel
  walkable: boolean;
  swimable: boolean;
}

// --- Entities ---
export enum EntityType {
  Dog = 'dog',
  Sheep = 'sheep',
  ElderBark = 'elder_bark',
  Collectible = 'collectible',
  Obstacle = 'obstacle',
  NPC = 'npc',
  Particle = 'particle',
}

export enum SheepBreed {
  Wooly = 'wooly',        // Basic white sheep - teaches "data points"
  Merino = 'merino',      // Premium wool - teaches "weights"
  Highland = 'highland',  // Scottish - teaches "biases"
  Suffolk = 'suffolk',    // Black face - teaches "activation functions"
  Dorper = 'dorper',      // Hair sheep - teaches "regularization"
  Jacob = 'jacob',        // Multi-colored - teaches "multi-class classification"
  Soay = 'soay',          // Ancient - teaches "evolutionary algorithms"
  Valais = 'valais',      // Blacknose - teaches "face recognition / CNNs"
  Navajo = 'navajo',      // Churro - teaches "cultural knowledge / transfer learning"
  Katahdin = 'katahdin',  // Hair - teaches "lossless compression"
  Cheviot = 'cheviot',    // Hill breed - teaches "gradient ascent"
  Romanov = 'romanov',    // Russian - teaches "cold start problems"
}

export enum SheepPersonality {
  Follower = 'follower',
  Wanderer = 'wanderer',
  Leader = 'leader',
  Stubborn = 'stubborn',
  Curious = 'curious',
  Nervous = 'nervous',
  Brave = 'brave',
  Lazy = 'lazy',
}

export interface SheepEntity {
  id: string;
  type: EntityType.Sheep;
  pos: Vec2;
  vel: Vec2;
  targetPos: Vec2 | null;
  breed: SheepBreed;
  personality: SheepPersonality;
  happiness: number; // 0-100
  energy: number; // 0-100
  isInPen: boolean;
  isLost: boolean;
  name: string;
  color: string;
  // Flocking state
  neighbors: string[]; // IDs of nearby sheep
  flockId: string;
  // Animation
  facing: 'up' | 'down' | 'left' | 'right';
  animFrame: number;
  isMoving: boolean;
}

export interface DogEntity {
  id: string;
  type: EntityType.Dog;
  pos: Vec2;
  vel: Vec2;
  facing: 'up' | 'down' | 'left' | 'right';
  stamina: number; // 0-100
  barkRadius: number;
  barkCooldown: number;
  isBarking: boolean;
  isMoving: boolean;
  animFrame: number;
  // Unlocked abilities
  abilities: DogAbility[];
  activeAbility: DogAbility | null;
  dashTimer: number;
  tunnelTarget: Vec2 | null;
}

export enum DogAbility {
  GuideBark = 'guide_bark',       // Direct sheep in facing direction
  ScatterBark = 'scatter_bark',   // Scatter sheep away
  CalmBark = 'calm_bark',         // Calm nervous sheep
  Dash = 'dash',                   // Quick burst of speed
  Howl = 'howl',                   // Attract all sheep toward dog
  Tunnel = 'tunnel',               // Phase through one obstacle
  SuperSense = 'super_sense',     // See sheep through fog
  Rally = 'rally',                 // Temporarily boost all sheep speed
}

export interface CollectibleEntity {
  id: string;
  type: EntityType.Collectible;
  pos: Vec2;
  collectibleType: CollectibleType;
  discovered: boolean;
  conceptKey: string;
  sparkle: boolean;
}

export enum CollectibleType {
  ConceptPage = 'concept_page',       // Elder Bark's teaching
  SheepCatalog = 'sheep_catalog',     // New breed info
  Sticker = 'sticker',               // Collectible sticker
  FarmUpgrade = 'farm_upgrade',       // Decoration/upgrade for farm
  LorePage = 'lore_page',            // Story fragment
  Secret = 'secret',                 // Hidden discovery
}

export interface ObstacleEntity {
  id: string;
  type: EntityType.Obstacle;
  pos: Vec2;
  obstacleType: ObstacleType;
  destructible: boolean;
  health: number;
}

export enum ObstacleType {
  Boulder = 'boulder',
  Log = 'log',
  Haybale = 'haybale',
  Thornbush = 'thornbush',
  IceBlock = 'ice_block',
  CrumblingWall = 'crumbling_wall',
}

export interface Particle {
  id: string;
  pos: Vec2;
  vel: Vec2;
  life: number;
  maxLife: number;
 color: string;
  size: number;
  particleType: ParticleType;
}

export enum ParticleType {
  Bark = 'bark',
  Dust = 'dust',
  Sparkle = 'sparkle',
  Confetti = 'confetti',
  Footprint = 'footprint',
  Mist = 'mist',
  Rain = 'rain',
  Snow = 'snow',
  Leaf = 'leaf',
  Heart = 'heart',
}

export type Entity = DogEntity | SheepEntity | CollectibleEntity | ObstacleEntity;

// --- Weather & Environment ---
export enum Weather {
  Clear = 'clear',
  Cloudy = 'cloudy',
  Rainy = 'rainy',
  Foggy = 'foggy',
  Snowy = 'snowy',
  Windy = 'windy',
  Golden = 'golden', // Golden hour lighting
  Starry = 'starry', // Night level
}

export enum Season {
  Spring = 'spring',
  Summer = 'summer',
  Autumn = 'autumn',
  Winter = 'winter',
}

export interface WeatherState {
  current: Weather;
  intensity: number; // 0-1
  windDir: Vec2;
  particles: Particle[];
  transitionTimer: number;
}

// --- Ranks & Progression ---
export enum Rank {
  Apprentice = 'apprentice',
  Journeyman = 'journeyman',
  Master = 'master',
  Elder = 'elder',
}

export const RANK_ORDER: Rank[] = [Rank.Apprentice, Rank.Journeyman, Rank.Master, Rank.Elder];

export const RANK_COLORS: Record<Rank, string> = {
  [Rank.Apprentice]: '#8B9467',  // Muted green
  [Rank.Journeyman]: '#C4956A', // Warm bronze
  [Rank.Master]: '#7B8FA8',     // Steel blue
  [Rank.Elder]: '#D4A843',      // Gold
};

export const RANK_LABELS: Record<Rank, string> = {
  [Rank.Apprentice]: 'Apprentice Pup',
  [Rank.Journeyman]: 'Journeyman Dog',
  [Rank.Master]: 'Master Shepherd',
  [Rank.Elder]: 'Elder Guardian',
};

// --- Level Definitions ---
export interface LevelDef {
  id: string;
  rank: Rank;
  index: number; // 1-based within rank
  name: string;
  subtitle: string;
  description: string;
  gridSize: Vec2;
  aiConcept: AIConcept;
  objective: LevelObjective;
  constraints: LevelConstraints;
  terrainSeed: number;
  sheepCount: number;
  sheepBreeds: SheepBreed[];
  obstacles: ObstaclePlacement[];
  weather: Weather;
  dialogIntro: DialogNode;
  dialogOutro: DialogNode;
  discoveries: DiscoveryPlacement[];
  parentLayerContent: ParentLayerContent;
  unlockRequirement?: { rank: Rank; index: number; stars: number };
  tutorialSteps?: TutorialStep[];
}

export interface Vec2 {
  x: number;
  y: number;
}

export interface ObstaclePlacement {
  type: ObstacleType;
  pos: Vec2;
}

export interface DiscoveryPlacement {
  type: CollectibleType;
  conceptKey: string;
  posHint: 'near_sheep' | 'corner' | 'center' | 'behind_obstacle' | 'hidden_path';
}

export interface LevelObjective {
  type: 'herd_all' | 'herd_count' | 'find_concept' | 'timed_herd' | 'protect_sheep' | 'pattern_herd';
  targetCount?: number; // for herd_count
  timeLimit?: number; // in seconds
  maxLostSheep?: number;
  description: string;
}

export interface LevelConstraints {
  maxBarks?: number;
  staminaDrain?: number;
  fogRadius?: number;
  movingObstacles?: boolean;
  predatorEvents?: boolean;
}

export interface TutorialStep {
  id: string;
  text: string;
  highlight: 'move' | 'bark' | 'sheep' | 'pen' | 'ability';
  waitFor: 'move' | 'bark' | 'sheep_herded' | 'pen_reached' | 'ability_used';
}

// --- AI Concepts (Spiral Curriculum) ---
export interface AIConcept {
  key: string;
  name: string;
  shortName: string;
  rank: Rank;
  depth: number; // 1-4, spirals deeper each rank
  metaphor: string; // The in-game metaphor
  realExplanation: string; // Real AI explanation
  parentExplanation: string; // For Parent Layer
  keywords: string[];
  relatedConcepts: string[];
}

export interface ParentLayerContent {
  title: string;
  conceptName: string;
  whatHappened: string;
  aiConnection: string;
  tryAtHome: string;
  ageAppropriate: string;
}

// --- Dialog System ---
export interface DialogNode {
  id: string;
  speaker: 'elder_bark' | 'narrator' | 'sheep' | 'dog';
  text: string;
  choices?: DialogChoice[];
  nextId?: string;
  emotion?: 'wise' | 'playful' | 'concerned' | 'proud' | 'mysterious' | 'encouraging';
  unlockConcept?: string;
  animation?: 'nod' | 'shake' | 'jump' | 'look_around' | 'paw_ground';
}

export interface DialogChoice {
  text: string;
  nextId: string;
  condition?: (state: GameState) => boolean;
}

// --- Skill Tree ---
export interface SkillNode {
  id: string;
  name: string;
  description: string;
  icon: string;
  ability?: DogAbility;
  cost: number; // Skill points
  requires?: string[]; // IDs of prerequisite skills
  rank: Rank;
  tier: number; // 1-3 within rank
  effect: SkillEffect;
  unlocked: boolean;
}

export interface SkillEffect {
  type: 'unlock_ability' | 'stat_boost' | 'passive';
  stat?: 'stamina' | 'speed' | 'bark_radius' | 'bark_cooldown' | 'sheep_calm_rate' | 'visibility';
  value?: number;
  ability?: DogAbility;
  description: string;
}

// --- Collection System ---
export interface Sticker {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: StickerCategory;
  rarity: StickerRarity;
  unlocked: boolean;
  unlockedDate?: string;
}

export enum StickerCategory {
  Achievement = 'achievement',
  Concept = 'concept',
  Breed = 'breed',
  Weather = 'weather',
  Secret = 'secret',
  Milestone = 'milestone',
}

export enum StickerRarity {
  Common = 'common',
  Uncommon = 'uncommon',
  Rare = 'rare',
  Legendary = 'legendary',
}

export interface FarmUpgrade {
  id: string;
  name: string;
  description: string;
  icon: string;
  cost: number;
  unlocked: boolean;
  position: Vec2;
}

// --- Daily Challenge ---
export interface DailyChallenge {
  date: string; // YYYY-MM-DD
  seed: number;
  levelName: string;
  description: string;
 specialRules: DailyRule[];
  reward: DailyReward;
  completed: boolean;
  stars: number;
  bestTime: number;
}

export interface DailyRule {
  type: 'low_stamina' | 'no_bark_limit' | 'fog_always' | 'fast_sheep' | 'mirrored' | 'tiny_pen' | 'many_sheep';
  value?: number;
  description: string;
}

export interface DailyReward {
  stickers: number;
  skillPoints: number;
  bonusDescription: string;
}

// --- Star Rating ---
export interface LevelResult {
  levelId: string;
  stars: number; // 0-3
  time: number; // seconds
  sheepHerded: number;
  sheepTotal: number;
  barksUsed: number;
  discoveriesFound: number;
  personalBest: boolean;
  newDiscoveries: string[];
}

export const STAR_CRITERIA = {
  1: { description: 'Complete the level' },
  2: { description: 'Herd all sheep + find 1 discovery' },
  3: { description: 'Complete fast + find all discoveries' },
} as const;

// --- Game State ---
export type GameScreen =
  | 'title'
  | 'level_select'
  | 'game'
  | 'dialog'
  | 'level_complete'
  | 'skill_tree'
  | 'collection_book'
  | 'sandbox'
  | 'farm'
  | 'daily_challenge'
  | 'settings';

export interface GameState {
  screen: GameScreen;
  // Current level
  currentLevel: LevelDef | null;
  grid: Tile[][];
  gridWidth: number;
  gridHeight: number;
  entities: Entity[];
  dog: DogEntity | null;
  sheep: SheepEntity[];
  collectibles: CollectibleEntity[];
  obstacles: ObstacleEntity[];
  particles: Particle[];
  // Level state
  timer: number;
  barksUsed: number;
  sheepInPen: number;
  sheepLost: number;
  totalSheep: number;
  discoveriesThisLevel: string[];
  isPaused: boolean;
  isComplete: boolean;
  // Weather
  weather: WeatherState;
  season: Season;
  // Dialog
  currentDialog: DialogNode | null;
  dialogHistory: string[];
  // Tutorial
  activeTutorial: TutorialStep | null;
  tutorialIndex: number;
  // Sandbox
  sandboxParams: SandboxParams;
}

export interface SandboxParams {
  separation: number;
  alignment: number;
  cohesion: number;
  sheepCount: number;
  showVectors: boolean;
  showFlocks: boolean;
  placeObstacles: boolean;
  weather: Weather;
  barkType: DogAbility.GuideBark | DogAbility.ScatterBark | DogAbility.CalmBark;
}

// --- Persistent Save Data ---
export interface SaveData {
  version: number;
  lastPlayed: string;
  totalPlayTime: number;
  // Progression
  currentRank: Rank;
  skillPoints: number;
  totalSkillPoints: number;
  // Level results
  levelResults: Record<string, LevelResult>;
  highestUnlockedLevel: string;
  // Skills
  unlockedSkills: string[];
  // Collection
  stickers: Record<string, boolean>;
  stickerCount: number;
  discoveries: Record<string, boolean>; // conceptKey -> found
  discoveryCount: number;
  sheepCatalog: Record<SheepBreed, boolean>; // breed -> cataloged
  farmUpgrades: string[];
  // Daily
  dailyChallenges: Record<string, DailyChallenge>;
  dailyStreak: number;
  lastDailyDate: string;
  // Stats
  totalSheepHerded: number;
  totalBarks: number;
  totalTimePlayed: number;
  totalLevelsCompleted: number;
  perfectHerds: number;
  // Settings
  musicVolume: number;
  sfxVolume: number;
  parentLayerEnabled: boolean;
  showTutorials: boolean;
}

// --- Input ---
export type Direction = 'up' | 'down' | 'left' | 'right' | 'none';

export interface InputState {
  direction: Direction;
  bark: boolean;
  ability: boolean;
  pause: boolean;
  interact: boolean;
  menu: boolean;
}

// --- Seeded RNG ---
export class SeededRNG {
  private seed: number;

  constructor(seed: number) {
    this.seed = seed;
  }

  next(): number {
    this.seed = (this.seed * 16807 + 0) % 2147483647;
    return this.seed / 2147483647;
  }

  nextInt(min: number, max: number): number {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }

  nextBool(probability: number = 0.5): boolean {
    return this.next() < probability;
  }

  shuffle<T>(array: T[]): T[] {
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
      const j = this.nextInt(0, i);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  pick<T>(array: T[]): T {
    return array[this.nextInt(0, array.length - 1)];
  }
}

// --- Constants ---
export const TILE_SIZE = 48;
export const DOG_SPEED = 3.5;
export const SHEEP_BASE_SPEED = 2.0;
export const BARK_BASE_RADIUS = 3.5;
export const BARK_COOLDOWN = 0.4; // seconds
export const STAMINA_MAX = 100;
export const STAMINA_DRAIN_RATE = 8; // per second when moving
export const STAMINA_REGEN_RATE = 15; // per second when still
export const SHEEP_HAPPINESS_DECAY = 0.5; // per second
export const MAX_GRID_WIDTH = 24;
export const MAX_GRID_HEIGHT = 18;
export const FLOCK_DETECT_RADIUS = 5;
export const SEPARATION_RADIUS = 1.2;
export const ALIGNMENT_RADIUS = 3.0;
export const COHESION_RADIUS = 4.0;
