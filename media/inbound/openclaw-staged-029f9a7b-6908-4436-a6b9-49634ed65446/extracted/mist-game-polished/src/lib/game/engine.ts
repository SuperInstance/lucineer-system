// MIST Game Engine — Flocking AI, Pathfinding, Day/Night, Particles
// Core simulation systems that make the world feel alive

import type { Position, SheepEntity, Direction, WorldDef, TimeOfDay, ParticleConfig, CellType } from './types';

// ═══════════════════════════════════════════════════════════════
// FLOCKING AI — Boids-inspired sheep behavior
// ═══════════════════════════════════════════════════════════════

/** Flocking parameters tuned for fun gameplay. */
const FLOCKING = {
  /** Distance at which sheep detect the player (bark radius). */
  barkRadius: 3,
  /** Distance at which sheep begin to flee. */
  fleeRadius: 2,
  /** Cohesion — sheep try to stay near flock center. */
  cohesionWeight: 0.3,
  /** Separation — sheep avoid crowding each other. */
  separationWeight: 0.5,
  /** Alignment — sheep try to match flock direction. */
  alignmentWeight: 0.2,
  /** Random wandering weight. */
  wanderWeight: 0.15,
  /** Frames between movement attempts. */
  moveInterval: 12,
  /** Max flee distance from bark. */
  maxFleeDistance: 4,
};

/** Get Chebyshev distance between two positions. */
function chebyshev(a: Position, b: Position): number {
  return Math.max(Math.abs(a.x - b.x), Math.abs(a.y - b.y));
}

/** Get Manhattan distance. */
function manhattan(a: Position, b: Position): number {
  return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}

/** Get Euclidean distance. */
function euclidean(a: Position, b: Position): number {
  return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
}

/** Check if a position is within world bounds and walkable. */
function isWalkable(world: WorldDef, pos: Position): boolean {
  if (pos.x < 0 || pos.x >= world.width || pos.y < 0 || pos.y >= world.height) return false;
  return world.grid[pos.y][pos.x].walkable;
}

/** Get all valid adjacent positions. */
function getAdjacentWalkable(world: WorldDef, pos: Position): Position[] {
  const dirs: Position[] = [
    { x: 0, y: -1 }, { x: 0, y: 1 }, { x: -1, y: 0 }, { x: 1, y: 0 },
  ];
  return dirs.filter((d) => isWalkable(world, { x: pos.x + d.x, y: pos.y + d.y }))
    .map((d) => ({ x: pos.x + d.x, y: pos.y + d.y }));
}

/** Compute flock center (average position of all uncollected sheep). */
function flockCenter(sheep: SheepEntity[]): Position {
  const active = sheep.filter((s) => !s.collected);
  if (active.length === 0) return { x: 0, y: 0 };
  const sx = active.reduce((sum, s) => sum + s.pos.x, 0) / active.length;
  const sy = active.reduce((sum, s) => sum + s.pos.y, 0) / active.length;
  return { x: Math.round(sx), y: Math.round(sy) };
}

/** Get the average direction the flock is moving. */
function flockAlignment(sheep: SheepEntity[]): Position {
  const active = sheep.filter((s) => !s.collected && s.state !== 'idle');
  if (active.length === 0) return { x: 0, y: 0 };
  const dirMap: Record<Direction, Position> = {
    up: { x: 0, y: -1 }, down: { x: 0, y: 1 }, left: { x: -1, y: 0 }, right: { x: 1, y: 0 },
  };
  const avg = active.reduce(
    (sum, s) => {
      const d = dirMap[s.facing] ?? { x: 0, y: 0 };
      return { x: sum.x + d.x, y: sum.y + d.y };
    },
    { x: 0, y: 0 },
  );
  return { x: avg.x / active.length, y: avg.y / active.length };
}

/** Compute separation vector — steer away from nearby sheep. */
function separationVector(sheep: SheepEntity[], index: number): Position {
  const me = sheep[index]!;
  let vx = 0;
  let vy = 0;
  for (let i = 0; i < sheep.length; i++) {
    if (i === index || sheep[i]!.collected) continue;
    const dist = euclidean(me.pos, sheep[i]!.pos);
    if (dist < 2 && dist > 0) {
      vx += (me.pos.x - sheep[i]!.pos.x) / dist;
      vy += (me.pos.y - sheep[i]!.pos.y) / dist;
    }
  }
  return { x: vx, y: vy };
}

/** Direction from position a to position b. */
export function directionTo(a: Position, b: Position): Direction {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  if (Math.abs(dx) >= Math.abs(dy)) return dx > 0 ? 'right' : 'left';
  return dy > 0 ? 'down' : 'up';
}

/** Convert a direction to a position delta. */
export function dirToDelta(dir: Direction): Position {
  const map: Record<Direction, Position> = {
    up: { x: 0, y: -1 }, down: { x: 0, y: 1 }, left: { x: -1, y: 0 }, right: { x: 1, y: 0 },
  };
  return map[dir];
}

/** Pick the best adjacent cell toward a target, avoiding obstacles. */
function steerToward(world: WorldDef, from: Position, target: Position): Position | null {
  const adj = getAdjacentWalkable(world, from);
  if (adj.length === 0) return null;
  let best = adj[0]!;
  let bestDist = euclidean(adj[0]!, target);
  for (let i = 1; i < adj.length; i++) {
    const d = euclidean(adj[i]!, target);
    if (d < bestDist) {
      bestDist = d;
      best = adj[i]!;
    }
  }
  return best;
}

/** Pick the best adjacent cell away from a threat. */
function fleeFrom(world: WorldDef, from: Position, threat: Position, maxDist: number): Position | null {
  const adj = getAdjacentWalkable(world, from);
  if (adj.length === 0) return null;
  let best = adj[0]!;
  let bestDist = euclidean(adj[0]!, threat);
  for (let i = 1; i < adj.length; i++) {
    const d = euclidean(adj[i]!, threat);
    if (d > bestDist && euclidean(adj[i]!, from) <= maxDist) {
      bestDist = d;
      best = adj[i]!;
    }
  }
  return best;
}

/** Update all sheep entities for one simulation tick.
 *  Returns the updated array (does not mutate in place).
 */
export function updateFlocking(
  sheep: SheepEntity[],
  world: WorldDef,
  playerPos: Position,
  lastBarkDir: Direction | null,
  lastBarkTime: number,
  now: number,
): SheepEntity[] {
  return sheep.map((s, idx) => {
    if (s.collected) return s;

    const copy = { ...s };
    copy.stateTimer -= 1;
    copy.moveCooldown -= 1;

    // ── State transitions ──────────────────────────────────
    const distToPlayer = chebyshev(s.pos, playerPos);
    const recentBark = lastBarkDir && (now - lastBarkTime) < 30;

    if (recentBark && distToPlayer <= FLOCKING.barkRadius && !s.collected) {
      // Bark triggered — flee from player
      copy.state = 'fleeing';
      copy.stateTimer = FLOCKING.maxFleeDistance * 2;
    } else if (distToPlayer <= FLOCKING.fleeRadius && copy.state !== 'herding') {
      // Player too close — flee
      copy.state = 'fleeing';
      copy.stateTimer = 8;
    } else if (copy.stateTimer <= 0) {
      // Return to wandering
      copy.state = 'wandering';
      copy.stateTimer = 20 + Math.floor(Math.random() * 40);
    }

    // ── Movement ───────────────────────────────────────────
    if (copy.moveCooldown <= 0) {
      let newPos: Position | null = null;

      switch (copy.state) {
        case 'fleeing': {
          const fleeTarget = lastBarkDir
            ? { x: playerPos.x + dirToDelta(lastBarkDir).x * FLOCKING.maxFleeDistance,
                y: playerPos.y + dirToDelta(lastBarkDir).y * FLOCKING.maxFleeDistance }
            : playerPos;
          newPos = fleeFrom(world, copy.pos, fleeTarget, FLOCKING.maxFleeDistance);
          if (newPos) copy.facing = directionTo(copy.pos, newPos);
          break;
        }
        case 'wandering': {
          // Mix flocking forces
          const center = flockCenter(sheep);
          const alignment = flockAlignment(sheep);
          const sep = separationVector(sheep, idx);
          
          // Random wander component
          const randX = (Math.random() - 0.5) * 2;
          const randY = (Math.random() - 0.5) * 2;
          
          // Weighted sum of forces
          let targetX = copy.pos.x + Math.round(
            (center.x - copy.pos.x) * FLOCKING.cohesionWeight +
            alignment.x * FLOCKING.alignmentWeight +
            sep.x * FLOCKING.separationWeight +
            randX * FLOCKING.wanderWeight
          );
          let targetY = copy.pos.y + Math.round(
            (center.y - copy.pos.y) * FLOCKING.cohesionWeight +
            alignment.y * FLOCKING.alignmentWeight +
            sep.y * FLOCKING.separationWeight +
            randY * FLOCKING.wanderWeight
          );
          
          targetX = Math.max(0, Math.min(world.width - 1, targetX));
          targetY = Math.max(0, Math.min(world.height - 1, targetY));
          
          newPos = steerToward(world, copy.pos, { x: targetX, y: targetY });
          if (newPos && Math.random() > 0.4) {
            copy.facing = directionTo(copy.pos, newPos);
          }
          break;
        }
        case 'herding': {
          // Move toward nearest pen position
          const pen = world.penPositions[0];
          if (pen) {
            newPos = steerToward(world, copy.pos, pen);
            if (newPos) copy.facing = directionTo(copy.pos, newPos);
            if (newPos && chebyshev(newPos, pen) <= 1) {
              copy.state = 'idle';
              copy.stateTimer = 999;
            }
          }
          break;
        }
        default:
          break;
      }

      if (newPos) {
        copy.pos = newPos;
        copy.moveCooldown = FLOCKING.moveInterval + Math.floor(Math.random() * 6);
      } else {
        copy.moveCooldown = 4; // try again soon
      }
    }

    return copy;
  });
}

/** Initialize sheep entities from world definition. */
export function initSheepEntities(world: WorldDef): SheepEntity[] {
  return world.sheepPositions.map((pos, i) => ({
    id: `sheep-${i}`,
    pos: { ...pos },
    collected: false,
    variant: i % 4,
    state: 'idle' as const,
    facing: (['right', 'down', 'left', 'up'] as Direction[])[i % 4],
    stateTimer: 30 + Math.floor(Math.random() * 60),
    moveCooldown: FLOCKING.moveInterval + Math.floor(Math.random() * 10),
  }));
}

// ═══════════════════════════════════════════════════════════════
// BARK MECHANIC — Player herding action
// ═══════════════════════════════════════════════════════════════

export interface BarkResult {
  sheepInfluenced: number;
  direction: Direction;
}

/** Compute the result of a bark action. */
export function computeBark(
  playerPos: Position,
  playerFacing: Direction,
  sheep: SheepEntity[],
): BarkResult {
  const influenced = sheep.filter(
    (s) => !s.collected && chebyshev(s.pos, playerPos) <= FLOCKING.barkRadius,
  );
  return {
    sheepInfluenced: influenced.length,
    direction: playerFacing,
  };
}

// ═══════════════════════════════════════════════════════════════
// PATHFINDING — A* for NPCs and optional player guidance
// ═══════════════════════════════════════════════════════════════

interface PathNode {
  pos: Position;
  g: number;
  h: number;
  f: number;
  parent: PathNode | null;
}

/** A* pathfinding on the world grid. Returns path (excluding start). */
export function findPath(
  world: WorldDef,
  start: Position,
  goal: Position,
  maxSteps = 200,
): Position[] {
  if (start.x === goal.x && start.y === goal.y) return [];

  const key = (p: Position) => `${p.x},${p.y}`;
  const heuristic = (a: Position, b: Position) => manhattan(a, b);

  const openSet = new Map<string, PathNode>();
  const closedSet = new Set<string>();

  const startNode: PathNode = {
    pos: start,
    g: 0,
    h: heuristic(start, goal),
    f: heuristic(start, goal),
    parent: null,
  };

  openSet.set(key(start), startNode);
  let steps = 0;

  while (openSet.size > 0 && steps < maxSteps) {
    steps++;

    // Find node with lowest f
    let current: PathNode | null = null;
    for (const node of openSet.values()) {
      if (!current || node.f < current.f) current = node;
    }
    if (!current) break;

    if (current.pos.x === goal.x && current.pos.y === goal.y) {
      // Reconstruct path
      const path: Position[] = [];
      let node: PathNode | null = current;
      while (node?.parent) {
        path.unshift(node.pos);
        node = node.parent;
      }
      return path;
    }

    openSet.delete(key(current.pos));
    closedSet.add(key(current.pos));

    // Neighbors
    const dirs: Position[] = [
      { x: 0, y: -1 }, { x: 0, y: 1 }, { x: -1, y: 0 }, { x: 1, y: 0 },
    ];
    for (const d of dirs) {
      const nx = current.pos.x + d.x;
      const ny = current.pos.y + d.y;
      const nPos = { x: nx, y: ny };
      const nKey = key(nPos);

      if (nx < 0 || nx >= world.width || ny < 0 || ny >= world.height) continue;
      if (!world.grid[ny][nx].walkable) continue;
      if (closedSet.has(nKey)) continue;

      const g = current.g + 1;
      const h = heuristic(nPos, goal);
      const existing = openSet.get(nKey);

      if (!existing || g < existing.g) {
        const node: PathNode = {
          pos: nPos,
          g,
          h,
          f: g + h,
          parent: current,
        };
        openSet.set(nKey, node);
      }
    }
  }

  return []; // No path found
}

// ═══════════════════════════════════════════════════════════════
// DAY/NIGHT CYCLE
// ═══════════════════════════════════════════════════════════════

/** Get the TimeOfDay config for a given hour. */
export function getTimeOfDay(hour: number): TimeOfDay {
  const h = ((hour % 24) + 24) % 24;

  if (h >= 5 && h < 7) return { hour: h, period: 'dawn', darkness: 0.15, tintColor: 'rgba(255,180,100,0.15)', creatureActivity: 0.3 };
  if (h >= 7 && h < 10) return { hour: h, period: 'morning', darkness: 0, tintColor: 'rgba(255,255,200,0.05)', creatureActivity: 0.7 };
  if (h >= 10 && h < 14) return { hour: h, period: 'noon', darkness: 0, tintColor: 'transparent', creatureActivity: 1.0 };
  if (h >= 14 && h < 17) return { hour: h, period: 'afternoon', darkness: 0, tintColor: 'rgba(255,200,100,0.05)', creatureActivity: 0.8 };
  if (h >= 17 && h < 19) return { hour: h, period: 'dusk', darkness: 0.2, tintColor: 'rgba(255,100,50,0.2)', creatureActivity: 0.5 };
  if (h >= 19 && h < 21) return { hour: h, period: 'evening', darkness: 0.35, tintColor: 'rgba(100,100,200,0.25)', creatureActivity: 0.2 };
  if (h >= 21 && h < 1) return { hour: h, period: 'night', darkness: 0.45, tintColor: 'rgba(20,20,80,0.45)', creatureActivity: 0.1 };
  return { hour: h, period: 'midnight', darkness: 0.5, tintColor: 'rgba(10,10,50,0.5)', creatureActivity: 0.05 };
}

/** Advance time by a given number of in-game hours. */
export function advanceTime(currentHour: number, delta: number): number {
  return ((currentHour + delta) % 24 + 24) % 24;
}

// ═══════════════════════════════════════════════════════════════
// PARTICLE SYSTEM CONFIGS
// ═══════════════════════════════════════════════════════════════

export const WORLD_PARTICLES: Record<string, ParticleConfig[]> = {
  farm: [
    { type: 'pollen', color: 'bg-yellow-300/40', count: 15, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.3, size: 3 },
  ],
  forest: [
    { type: 'firefly', color: 'bg-green-300/60', count: 12, area: { x: 2, y: 6, w: 8, h: 5 }, speed: 0.2, size: 4 },
    { type: 'leaf', color: 'bg-green-500/30', count: 8, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.4, size: 5 },
  ],
  village: [
    { type: 'sparkle', color: 'bg-amber-200/40', count: 8, area: { x: 4, y: 3, w: 8, h: 6 }, speed: 0.15, size: 3 },
  ],
  mountain: [
    { type: 'snow', color: 'bg-white/50', count: 20, area: { x: 0, y: 0, w: 16, h: 8 }, speed: 0.5, size: 3 },
    { type: 'ember', color: 'bg-orange-400/60', count: 6, area: { x: 1, y: 6, w: 3, h: 2 }, speed: 0.3, size: 3 },
    { type: 'ember', color: 'bg-orange-400/60', count: 6, area: { x: 8, y: 6, w: 3, h: 2 }, speed: 0.3, size: 3 },
  ],
  meadow: [
    { type: 'pollen', color: 'bg-yellow-200/50', count: 20, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.25, size: 3 },
    { type: 'butterfly', color: 'bg-pink-300/40', count: 6, area: { x: 2, y: 2, w: 12, h: 12 }, speed: 0.2, size: 5 },
  ],
  lake: [
    { type: 'bubble', color: 'bg-cyan-300/40', count: 10, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.2, size: 4 },
    { type: 'sparkle', color: 'bg-blue-200/30', count: 8, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.15, size: 3 },
  ],
  ruins: [
    { type: 'dust', color: 'bg-stone-400/30', count: 12, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.1, size: 4 },
    { type: 'sparkle', color: 'bg-purple-300/40', count: 8, area: { x: 4, y: 4, w: 8, h: 8 }, speed: 0.15, size: 3 },
  ],
  sky: [
    { type: 'sparkle', color: 'bg-amber-200/50', count: 15, area: { x: 0, y: 0, w: 16, h: 16 }, speed: 0.2, size: 4 },
    { type: 'cloud_particle', color: 'bg-white/20', count: 8, area: { x: 0, y: 0, w: 16, h: 6 }, speed: 0.15, size: 8 },
  ],
};

// ═══════════════════════════════════════════════════════════════
// FOG OF WAR
// ═══════════════════════════════════════════════════════════════

/** Reveal cells within a radius of the player position.
 *  Returns a new Set of revealed cell keys.
 */
export function revealFog(
  playerPos: Position,
  radius: number,
  worldWidth: number,
  worldHeight: number,
  existing: Set<string>,
): Set<string> {
  const newRevealed = new Set(existing);
  for (let dy = -radius; dy <= radius; dy++) {
    for (let dx = -radius; dx <= radius; dx++) {
      if (dx * dx + dy * dy > radius * radius) continue;
      const x = playerPos.x + dx;
      const y = playerPos.y + dy;
      if (x < 0 || x >= worldWidth || y < 0 || y >= worldHeight) continue;
      newRevealed.add(`${x},${y}`);
    }
  }
  return newRevealed;
}

/** Check if a cell is revealed (visible to the player). */
export function isCellRevealed(
  x: number, y: number,
  playerPos: Position,
  radius: number,
): boolean {
  const dx = x - playerPos.x;
  const dy = y - playerPos.y;
  return dx * dx + dy * dy <= radius * radius;
}
