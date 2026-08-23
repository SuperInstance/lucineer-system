// ============================================================
// MIST — Procedural Terrain & Level Generation
// Procedural generation ensures every playthrough feels fresh
// ============================================================

import {
  Tile, TileType, TileVariant, Vec2, SeededRNG,
  LevelDef, SheepEntity, CollectibleEntity, ObstacleEntity,
  SheepBreed, SheepPersonality, Weather, Season,
  MAX_GRID_WIDTH, MAX_GRID_HEIGHT, FLOCK_DETECT_RADIUS,
} from './types';

// --- Terrain Generation ---

function createBaseTile(variant: TileVariant = TileVariant.A): Tile {
  return { type: TileType.Grass, variant, elevation: 0, walkable: true, swimable: false };
}

function makeTile(type: TileType, walkable: boolean, swimable = false, elevation = 0, variant?: TileVariant): Tile {
  const v = variant ?? (['a', 'b', 'c', 'd'] as TileVariant[])[Math.floor(Math.random() * 4)];
  return { type, variant: v, elevation, walkable, swimable };
}

export function generateTerrain(
  width: number,
  height: number,
  seed: number,
  weather: Weather
): Tile[][] {
  const rng = new SeededRNG(seed);
  const grid: Tile[][] = [];

  // Generate noise-like elevation map
  const elevationMap: number[][] = [];
  for (let y = 0; y < height; y++) {
    elevationMap[y] = [];
    for (let x = 0; x < width; x++) {
      // Simple value noise with 2 octaves
      const nx = x / width;
      const ny = y / height;
      const v1 = pseudoNoise(nx * 3, ny * 3, seed);
      const v2 = pseudoNoise(nx * 7, ny * 7, seed + 100) * 0.5;
      elevationMap[y][x] = (v1 + v2) / 1.5;
    }
  }

  for (let y = 0; y < height; y++) {
    grid[y] = [];
    for (let x = 0; x < width; x++) {
      const e = elevationMap[y][x];
      const isEdge = x === 0 || y === 0 || x === width - 1 || y === height - 1;
      const isCorner = (x <= 1 && y <= 1) || (x >= width - 2 && y <= 1) ||
                       (x <= 1 && y >= height - 2) || (x >= width - 2 && y >= height - 2);

      if (isCorner) {
        // Corners are dense trees/rocks — natural borders
        grid[y][x] = makeTile(
          rng.nextBool(0.6) ? TileType.Tree : TileType.Rock,
          false, false, Math.round(e * 3)
        );
      } else if (isEdge) {
        // Edges have mix of trees, bushes, and some gaps
        const roll = rng.next();
        if (roll < 0.35) {
          grid[y][x] = makeTile(TileType.Tree, false, false, Math.round(e * 3));
        } else if (roll < 0.55) {
          grid[y][x] = makeTile(TileType.Bush, false, false, Math.round(e * 3));
        } else if (roll < 0.65 && weather === Weather.Foggy) {
          grid[y][x] = makeTile(TileType.Fog, true, false, 0);
        } else {
          grid[y][x] = makeTileFromElevation(e, rng, weather);
        }
      } else {
        grid[y][x] = makeTileFromElevation(e, rng, weather);
      }
    }
  }

  // Add a winding path from top-center to the pen area
  addWindingPath(grid, width, height, rng);

  // Add water features in low elevation areas
  addWaterFeatures(grid, elevationMap, width, height, rng);

  // Ensure pen area is clear (bottom-right quadrant)
  clearPenArea(grid, width, height);

  // Ensure spawn area is clear (top-left quadrant)
  clearSpawnArea(grid, width, height);

  return grid;
}

function makeTileFromElevation(e: number, rng: SeededRNG, weather: Weather): Tile {
  if (e < 0.25) {
    // Low areas
    if (weather === Weather.Snowy && rng.nextBool(0.3)) {
      return makeTile(TileType.Ice, true, false, 0);
    }
    if (weather === Weather.Rainy && rng.nextBool(0.4)) {
      return makeTile(TileType.Mud, true, false, 0);
    }
    const roll = rng.next();
    if (roll < 0.3) return makeTile(TileType.Dirt, true, false, 0);
    if (roll < 0.5) return makeTile(TileType.Clover, true, false, 0);
    return makeTile(TileType.Grass, true, false, 0);
  } else if (e < 0.5) {
    // Mid-low
    const roll = rng.next();
    if (roll < 0.15) return makeTile(TileType.Flowers, true, false, 0);
    if (roll < 0.3) return makeTile(TileType.TallGrass, true, false, 1);
    if (roll < 0.4) return makeTile(TileType.Clover, true, false, 0);
    return makeTile(TileType.Grass, true, false, 0);
  } else if (e < 0.75) {
    // Mid-high
    const roll = rng.next();
    if (roll < 0.1) return makeTile(TileType.Path, true, false, 1);
    if (roll < 0.2) return makeTile(TileType.TallGrass, true, false, 1);
    if (roll < 0.3 && rng.nextBool(0.3)) return makeTile(TileType.Bush, false, false, 2);
    return makeTile(TileType.Grass, true, false, 1);
  } else {
    // High areas — rocky
    const roll = rng.next();
    if (roll < 0.25) return makeTile(TileType.Stone, false, false, 2);
    if (roll < 0.4) return makeTile(TileType.Rock, false, false, 3);
    if (roll < 0.5) return makeTile(TileType.Dirt, true, false, 2);
    return makeTile(TileType.Grass, true, false, 1);
  }
}

function addWindingPath(grid: Tile[][], width: number, height: number, rng: SeededRNG) {
  let x = Math.floor(width * 0.3);
  let y = 1;

  while (y < height - 3) {
    if (y >= 0 && y < height && x >= 0 && x < width) {
      grid[y][x] = makeTile(TileType.Path, true, false, 0, TileVariant.A);
      // Widen path occasionally
      if (rng.nextBool(0.4) && x + 1 < width) {
        grid[y][x + 1] = makeTile(TileType.Path, true, false, 0, TileVariant.B);
      }
    }
    y += 1;
    x += rng.nextInt(-1, 1);
    x = Math.max(2, Math.min(width - 3, x));
  }
}

function addWaterFeatures(grid: Tile[][], elevationMap: number[][], width: number, height: number, rng: SeededRNG) {
  // Find a low point and create a small pond
  let lowestX = Math.floor(width / 2);
  let lowestY = Math.floor(height / 2);
  let lowestE = 1;

  for (let y = 3; y < height - 3; y++) {
    for (let x = 3; x < width - 3; x++) {
      if (elevationMap[y][x] < lowestE) {
        lowestE = elevationMap[y][x];
        lowestX = x;
        lowestY = y;
      }
    }
  }

  // Create a small pond (3-5 tiles)
  const pondSize = rng.nextInt(2, 3);
  for (let dy = -pondSize; dy <= pondSize; dy++) {
    for (let dx = -pondSize; dx <= pondSize; dx++) {
      const px = lowestX + dx;
      const py = lowestY + dy;
      if (px > 2 && px < width - 2 && py > 2 && py < height - 2) {
        if (Math.abs(dx) + Math.abs(dy) <= pondSize) {
          grid[py][px] = makeTile(TileType.Water, false, true, 0);
        } else if (Math.abs(dx) + Math.abs(dy) === pondSize + 1) {
          // Banks around pond
          grid[py][px] = makeTile(TileType.Dirt, true, false, 0);
        }
      }
    }
  }
}

function clearPenArea(grid: Tile[][], width: number, height: number) {
  const penX = width - 6;
  const penY = height - 5;
  for (let dy = 0; dy < 4; dy++) {
    for (let dx = 0; dx < 5; dx++) {
      const x = penX + dx;
      const y = penY + dy;
      if (y < height && x < width) {
        if (dy === 0 || dy === 3 || dx === 0 || dx === 4) {
          grid[y][x] = makeTile(TileType.Fence, false, false, 0);
        } else {
          grid[y][x] = makeTile(TileType.PenFloor, true, false, 0);
        }
      }
    }
  }
  // Gate opening
  if (penY + 1 < height) {
    grid[penY][penX + 2] = makeTile(TileType.Gate, true, false, 0);
  }
}

function clearSpawnArea(grid: Tile[][], width: number, height: number) {
  for (let y = 1; y < 4; y++) {
    for (let x = 1; x < 5; x++) {
      if (y < height && x < width) {
        grid[y][x] = makeTile(TileType.Grass, true, false, 0);
      }
    }
  }
}

function pseudoNoise(x: number, y: number, seed: number): number {
  const n = Math.sin(x * 127.1 + y * 311.7 + seed * 13.37) * 43758.5453123;
  return n - Math.floor(n);
}

// --- Entity Spawning ---

const SHEEP_NAMES = [
  'Cotton', 'Cloud', 'Pebble', 'Daisy', 'Fern', 'Maple', 'Breeze',
  'Puddles', 'Clover', 'Bramble', 'Sage', 'Willow', 'Hazel', 'Frost',
  'Dusty', 'Luna', 'Biscuit', 'Mossy', 'Patches', 'Woolly', 'Snowball',
  'Thistle', 'Poppy', 'Ember', 'Foggy', 'Storm', 'Cricket', 'Honey',
];

const BREED_COLORS: Record<SheepBreed, string> = {
  [SheepBreed.Wooly]: '#F5F5F0',
  [SheepBreed.Merino]: '#FFF8E7',
  [SheepBreed.Highland]: '#A0522D',
  [SheepBreed.Suffolk]: '#2D2D2D',
  [SheepBreed.Dorper]: '#D2B48C',
  [SheepBreed.Jacob]: '#F5F5F0',
  [SheepBreed.Soay]: '#8B7355',
  [SheepBreed.Valais]: '#2D2D2D',
  [SheepBreed.Navajo]: '#DEB887',
  [SheepBreed.Katahdin]: '#FAEBD7',
  [SheepBreed.Cheviot]: '#FFF5EE',
  [SheepBreed.Romanov]: '#696969',
};

export function spawnSheep(
  level: LevelDef,
  grid: Tile[][],
  rng: SeededRNG
): SheepEntity[] {
  const sheep: SheepEntity[] = [];
  const w = grid[0]?.length ?? 10;
  const h = grid.length;
  const personalities = Object.values(SheepPersonality);

  for (let i = 0; i < level.sheepCount; i++) {
    let pos: Vec2;
    let attempts = 0;
    do {
      pos = {
        x: rng.nextInt(2, Math.floor(w * 0.6)),
        y: rng.nextInt(2, h - 4),
      };
      attempts++;
    } while (attempts < 100 && !grid[pos.y]?.[pos.x]?.walkable);

    const breed = level.sheepBreeds[i % level.sheepBreeds.length];
    const personality = personalities[rng.nextInt(0, personalities.length - 1)];
    const name = SHEEP_NAMES[i % SHEEP_NAMES.length];

    sheep.push({
      id: `sheep_${i}_${Date.now()}`,
      type: 'sheep' as never,
      pos,
      vel: { x: 0, y: 0 },
      targetPos: null,
      breed,
      personality,
      happiness: 70 + rng.nextInt(0, 30),
      energy: 80 + rng.nextInt(0, 20),
      isInPen: false,
      isLost: false,
      name,
      color: BREED_COLORS[breed],
      neighbors: [],
      flockId: `flock_${Math.floor(i / 4)}`,
      facing: rng.pick(['up', 'down', 'left', 'right'] as const),
      animFrame: 0,
      isMoving: false,
    });
  }

  return sheep;
}

export function spawnCollectibles(
  level: LevelDef,
  grid: Tile[][],
  rng: SeededRNG
): CollectibleEntity[] {
  const collectibles: CollectibleEntity[] = [];
  const w = grid[0]?.length ?? 10;
  const h = grid.length;

  for (const disc of level.discoveries) {
    let pos: Vec2;
    let attempts = 0;
    do {
      switch (disc.posHint) {
        case 'corner':
          pos = rng.nextBool() ? { x: rng.nextInt(3, 6), y: rng.nextInt(3, 6) } : { x: w - rng.nextInt(3, 6), y: h - rng.nextInt(3, 6) };
          break;
        case 'center':
          pos = { x: Math.floor(w / 2) + rng.nextInt(-2, 2), y: Math.floor(h / 2) + rng.nextInt(-2, 2) };
          break;
        case 'behind_obstacle':
          pos = { x: rng.nextInt(w * 0.3, w * 0.7) | 0, y: rng.nextInt(h * 0.3, h * 0.7) | 0 };
          break;
        default:
          pos = { x: rng.nextInt(2, w - 2), y: rng.nextInt(2, h - 2) };
      }
      attempts++;
    } while (attempts < 50 && (!grid[pos.y]?.[pos.x]?.walkable || collectibles.some(c => Math.abs(c.pos.x - pos.x) < 2 && Math.abs(c.pos.y - pos.y) < 2)));

    collectibles.push({
      id: `collectible_${disc.conceptKey}_${Date.now()}`,
      type: 'collectible' as never,
      pos,
      collectibleType: disc.type,
      discovered: false,
      conceptKey: disc.conceptKey,
      sparkle: true,
    });
  }

  return collectibles;
}

export function spawnObstacles(
  level: LevelDef,
  grid: Tile[][],
  rng: SeededRNG
): ObstacleEntity[] {
  return level.obstacles.map((ob, i) => ({
    id: `obstacle_${i}`,
    type: 'obstacle' as never,
    pos: ob.pos,
    obstacleType: ob.type,
    destructible: ob.type !== 'boulder',
    health: ob.type === 'boulder' ? 999 : ob.type === 'crumbling_wall' ? 1 : 3,
  }));
}

// --- Pen Position Helper ---
export function getPenPosition(gridWidth: number, gridHeight: number): Vec2 {
  return { x: gridWidth - 4, y: gridHeight - 3 };
}

export function getPenGatePosition(gridWidth: number, gridHeight: number): Vec2 {
  return { x: gridWidth - 4, y: gridHeight - 5 };
}

export function isTileInPen(x: number, y: number, gridWidth: number, gridHeight: number): boolean {
  const penX = gridWidth - 6;
  const penY = gridHeight - 5;
  return x >= penX + 1 && x <= penX + 3 && y >= penY + 1 && y <= penY + 2;
}

// --- Weather Particles ---
export function createWeatherParticles(weather: Weather, gridWidth: number, gridHeight: number, dt: number): never[] {
  // Simplified — actual particle spawning handled in engine
  return [] as never[];
}

// --- Season from Level Index ---
export function getSeasonForLevel(rank: string, index: number): Season {
  const seasons = [Season.Spring, Season.Summer, Season.Autumn, Season.Winter];
  const rankIndex = ['apprentice', 'journeyman', 'master', 'elder'].indexOf(rank);
  return seasons[(rankIndex + index - 1) % 4];
}