// MIST Game Engine — Core Types (Expanded v2.0)
// Voxel-world kids game teaching AI concepts through a sheepdog puppy adventure

/** Every cell type that can appear in a world grid. */
export enum CellType {
  GRASS = 'GRASS',
  FIELD = 'FIELD',
  WATER = 'WATER',
  TREE = 'TREE',
  ROCK = 'ROCK',
  FENCE = 'FENCE',
  GATE = 'GATE',
  SHEEP = 'SHEEP',
  RAM = 'RAM',
  BARN = 'BARN',
  KENNEL = 'KENNEL',
  FLOWER = 'FLOWER',
  MUSHROOM = 'MUSHROOM',
  BRIDGE = 'BRIDGE',
  PATH = 'PATH',
  HOUSE = 'HOUSE',
  MOUNTAIN = 'MOUNTAIN',
  CAVE = 'CAVE',
  CRYSTAL = 'CRYSTAL',
  CAMPFIRE = 'CAMPFIRE',
  SIGN = 'SIGN',
  PEN = 'PEN',
  DOG = 'DOG',
  EMPTY = 'EMPTY',
  // ── New cell types (v2.0) ───────────────────────────────────
  PUDDLE = 'PUDDLE',
  BUSH = 'BUSH',
  LOG = 'LOG',
  WELL = 'WELL',
  HAYBALE = 'HAYBALE',
  PUMPKIN = 'PUMPKIN',
  LILYPAD = 'LILYPAD',
  REED = 'REED',
  DOCK = 'DOCK',
  BOAT = 'BOAT',
  STATUE = 'STATUE',
  PILLAR = 'PILLAR',
  CRACKED_WALL = 'CRACKED_WALL',
  MOSAIC = 'MOSAIC',
  COLUMN = 'COLUMN',
  BOOKSHELF = 'BOOKSHELF',
  CLOUD = 'CLOUD',
  RAINBOW = 'RAINBOW',
  STAR_FLOWER = 'STAR_FLOWER',
  GLOW_MUSHROOM = 'GLOW_MUSHROOM',
  ICICLE = 'ICICLE',
  HOT_SPRING = 'HOT_SPRING',
  LAVA_ROCK = 'LAVA_ROCK',
  WHIRLPOOL = 'WHIRLPOOL',
  CHEST = 'CHEST',
  FLAG = 'FLAG',
  TOTEM = 'TOTEM',
  BENCHMARK = 'BENCHMARK',
  SCROLL = 'SCROLL',
  TELEPORTER = 'TELEPORTER',
}

/** Cardinal movement directions. */
export type Direction = 'up' | 'down' | 'left' | 'right';

/** Grid coordinate. */
export interface Position {
  x: number;
  y: number;
}

/** A single cell in the world grid. */
export interface WorldCell {
  type: CellType;
  /** Visual variant index (e.g. different tree sprites). */
  variant?: number;
  /** Can the player / sheep walk on this cell? */
  walkable: boolean;
  /** Can the player interact with this cell? */
  interactable: boolean;
  /** Arbitrary extra data attached to the cell. */
  data?: Record<string, unknown>;
}

/** A single step in a multi-step dialog. */
export interface DialogStep {
  text: string;
  speaker: 'elder' | 'narrator' | 'system';
  /** Optional action to trigger after this step. */
  action?: 'award_xp' | 'unlock_quest' | 'reveal_area' | 'spawn_sheep' | 'play_animation';
  /** Action parameter (e.g. XP amount). */
  actionParam?: number | string;
}

/** A teaching moment delivered by Elder Bark — now supports multi-step dialog. */
export interface Teaching {
  id: string;
  /** What Elder Bark says — kid-friendly and story-driven. */
  text: string;
  /** Short label shown in the UI (e.g. 'flocking', 'search'). */
  insight: string;
  /** The real AI concept name (displayed to parents). */
  aiConcept: string;
  /** Parent-layer explanation of the real concept. */
  aiExplanation: string;
  /** Multi-step dialog for deeper teachings (v2.0). */
  dialogSteps?: DialogStep[];
  /** Whether this is a major teaching (triggers cutscene). */
  major?: boolean;
  /** Required discoveries to unlock this teaching. */
  requiresDiscoveries?: string[];
  /** World-specific sub-concept tag. */
  subConcept?: string;
}

/** A discovery the player can unlock. */
export interface Discovery {
  id: string;
  name: string;
  emoji: string;
  aiConcept: string;
  xp: number;
  world: string;
  /** Optional hint text shown before discovery. */
  hint?: string;
  /** Whether this is a hidden discovery (not shown in journal until found). */
  hidden?: boolean;
}

/** A collectible sticker reward. */
export interface Sticker {
  id: string;
  emoji: string;
  name: string;
  category: string;
  /** Optional rarity for display. */
  rarity?: 'common' | 'rare' | 'epic' | 'legendary';
}

/** A quest/challenge within a world. */
export interface Quest {
  id: string;
  world: string;
  name: string;
  description: string;
  emoji: string;
  /** Quest type determines completion logic. */
  type: 'collect_sheep' | 'find_discovery' | 'reach_position' | 'bark_count' | 'explore_cells' | 'time_limit';
  /** Target value (e.g. 3 sheep, 5 cells explored). */
  target: number;
  /** XP reward. */
  xpReward: number;
  /** Sticker reward ID. */
  stickerReward?: string;
  /** Whether the quest is a bonus/hidden quest. */
  hidden?: boolean;
  /** Target position for 'reach_position' type. */
  targetPos?: Position;
  /** Required discoveries to unlock. */
  requiresDiscoveries?: string[];
  /** Dialog shown when quest is given. */
  startDialog?: DialogStep[];
  /** Dialog shown when quest is completed. */
  completeDialog?: DialogStep[];
}

/** A moving sheep entity with flocking behavior. */
export interface SheepEntity {
  id: string;
  pos: Position;
  /** Is this sheep collected/herded? */
  collected: boolean;
  /** Unique visual variant. */
  variant: number;
  /** Flocking state: idle, wandering, fleeing, herding. */
  state: 'idle' | 'wandering' | 'fleeing' | 'herding';
  /** Direction the sheep is facing. */
  facing: Direction;
  /** Timer for state transitions. */
  stateTimer: number;
  /** Movement cooldown (frames). */
  moveCooldown: number;
}

/** Particle configuration for visual effects. */
export interface ParticleConfig {
  type: 'firefly' | 'snow' | 'leaf' | 'dust' | 'sparkle' | 'bubble' | 'ember' | 'pollen' | 'butterfly' | 'cloud_particle';
  color: string;
  count: number;
  /** Spawn area relative to grid. */
  area: { x: number; y: number; w: number; h: number };
  speed: number;
  size: number;
}

/** Season configuration for visual themes. */
export interface SeasonConfig {
  id: 'spring' | 'summer' | 'autumn' | 'winter';
  name: string;
  emoji: string;
  /** Grid tint overlay color. */
  tintColor: string;
  /** Background gradient. */
  bgGradient: string;
  /** Particle effects active in this season. */
  particles: ParticleConfig[];
  /** Which cell types change appearance. */
  cellOverrides?: Partial<Record<CellType, { emoji: string; color: string }>>;
}

/** Time of day for the day/night cycle. */
export interface TimeOfDay {
  hour: number; // 0-23
  period: 'dawn' | 'morning' | 'noon' | 'afternoon' | 'dusk' | 'evening' | 'night' | 'midnight';
  /** Overlay opacity (0 = none, 0.5 = dark). */
  darkness: number;
  /** Tint color for the overlay. */
  tintColor: string;
  /** Whether creatures are more active. */
  creatureActivity: number; // 0-1
}

/** Bark action result. */
export interface BarkResult {
  /** Number of sheep influenced by the bark. */
  sheepInfluenced: number;
  /** Direction the bark pushed sheep. */
  direction: Direction;
}

/** Full definition of a playable world (expanded v2.0). */
export interface WorldDef {
  id: string;
  name: string;
  subtitle: string;
  description: string;
  grid: WorldCell[][];
  playerStart: Position;
  sheepPositions: Position[];
  penPositions: Position[];
  teachings: Teaching[];
  discoveries: Discovery[];
  quests: Quest[];
  width: number;
  height: number;
  /** Season theme for this world. */
  season: SeasonConfig['id'];
  /** NPC positions and dialog. */
  npcs?: NpcDef[];
  /** Particle effects for this world. */
  particles?: ParticleConfig[];
  /** Ambient sound identifier. */
  ambientSound?: 'farm' | 'forest' | 'village' | 'mountain' | 'meadow' | 'lake' | 'ruins' | 'sky';
  /** Whether sheep use flocking AI in this world. */
  enableFlocking?: boolean;
  /** Whether bark mechanic is enabled. */
  enableBark?: boolean;
  /** Fog of war — cells beyond this radius from player are hidden. */
  fogOfWar?: number;
  /** World-specific AI theme for Parent Layer. */
  aiTheme: { concept: string; explanation: string };
  /** Difficulty level (affects flocking behavior, quest count). */
  difficulty: 1 | 2 | 3 | 4;
}

/** NPC definition. */
export interface NpcDef {
  id: string;
  name: string;
  emoji: string;
  pos: Position;
  /** Dialog lines the NPC says when interacted with. */
 dialog: string[];
  /** Whether the NPC moves around. */
  moves: boolean;
  /** Cell types this NPC walks on. */
  walkableCells?: CellType[];
  /** Quest this NPC gives. */
  givesQuest?: string;
}

/** Top-level game state stored in Zustand. */
export interface GameState {
  currentWorld: string;
  playerPos: Position;
  discoveries: string[];
  stickers: string[];
  xp: number;
  level: number;
  teachingsSeen: string[];
  sheepInPen: number;
  totalSheep: number;
  gamePhase:
    | 'menu'
    | 'playing'
    | 'teaching'
    | 'levelComplete'
    | 'worldSelect'
    | 'journal'
    | 'stickerBook'
    | 'questComplete'
    | 'cutscene'
    | 'dialog';
  // ── New state (v2.0) ──────────────────────────────────────
  /** Current active quests. */
  activeQuests: string[];
  /** Completed quest IDs. */
  completedQuests: string[];
  /** Quest progress map (questId → current value). */
  questProgress: Record<string, number>;
  /** Cells the player has visited (for explore quests). */
  visitedCells: Set<string>;
  /** Total bark count in current world. */
  barkCount: number;
  /** Current time of day (hour 0-23). */
  timeHour: number;
  /** Current season. */
  currentSeason: SeasonConfig['id'];
  /** Moving sheep entities. */
  sheepEntities: SheepEntity[];
  /** Current dialog steps for multi-step conversations. */
  dialogSteps: DialogStep[];
  /** Current dialog step index. */
  dialogStepIndex: number;
  /** Step counter for the player. */
  stepsTaken: number;
  /** Whether fog of war is active. */
  fogRevealed: Set<string>;
}

/** Player level names ordered by index. */
export const LevelNames: string[] = [
  'Apprentice',
  'Journeyman',
  'Master',
  'Elder',
  'Sage',
  'Scholar',
  'Legend',
];

/** AI concept categories organized by world. */
export const WORLD_AI_CONCEPTS: Record<string, string> = {
  farm: 'Pattern Recognition & Classification',
  forest: 'Search Algorithms & Optimization',
  village: 'Neural Networks & Weights',
  mountain: 'Model Training & Generalization',
  meadow: 'Reinforcement Learning',
  lake: 'Data Processing & Pipelines',
  ruins: 'Memory & Attention Mechanisms',
  sky: 'Generative AI & Creativity',
};
