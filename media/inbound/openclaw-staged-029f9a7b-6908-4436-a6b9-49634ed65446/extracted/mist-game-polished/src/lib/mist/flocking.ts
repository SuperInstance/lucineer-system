// ============================================================
// MIST — Flocking / Boids Algorithm
// This IS the AI concept made playable.
// Kids don't read about emergence — they SEE it.
// ============================================================

import { Vec2, SheepEntity, DogEntity, DogAbility, Tile, TileType, BARK_BASE_RADIUS, SEPARATION_RADIUS, ALIGNMENT_RADIUS, COHESION_RADIUS, SHEEP_BASE_SPEED, FLOCK_DETECT_RADIUS } from './types';

export interface FlockingParams {
  separation: number;  // Avoid crowding neighbors (1.5 default)
  alignment: number;   // Steer towards avg heading (1.0 default)
  cohesion: number;    // Steer towards avg position (1.0 default)
  barkInfluence: number; // How much barks affect direction (3.0 default)
  dogFear: number;     // How much sheep avoid the dog (2.0 default)
  penAttraction: number; // How much sheep are attracted to pen (0.5 default)
  speed: number;       // Base sheep speed
  personalityMod: number; // How much personality affects behavior (0.5 default)
}

export const DEFAULT_FLOCKING: FlockingParams = {
  separation: 1.5,
  alignment: 1.0,
  cohesion: 1.0,
  barkInfluence: 3.0,
  dogFear: 2.0,
  penAttraction: 0.5,
  speed: SHEEP_BASE_SPEED,
  personalityMod: 0.5,
};

// Spiral curriculum: each rank changes flocking to teach deeper concepts
export const RANK_FLOCKING_PRESETS: Record<string, FlockingParams> = {
  apprentice: {
    ...DEFAULT_FLOCKING,
    separation: 1.0,   // Sheep clump together more (easy to herd)
    alignment: 0.5,    // They don't coordinate well
    cohesion: 2.0,     // Strong pull together (easy herding)
    dogFear: 3.0,      // Very responsive to dog (forgiving)
    penAttraction: 0.2,
  },
  journeyman: {
    ...DEFAULT_FLOCKING,
    separation: 1.5,
    alignment: 1.0,    // Start forming proper flocks
    cohesion: 1.2,
    dogFear: 2.0,
    penAttraction: 0.5,
  },
  master: {
    ...DEFAULT_FLOCKING,
    separation: 2.0,   // More independent sheep (harder)
    alignment: 1.5,    // Better coordinated flocks
    cohesion: 0.8,     // Less clumping
    dogFear: 1.5,      // Less responsive to dog
    penAttraction: 0.3,
  },
  elder: {
    ...DEFAULT_FLOCKING,
    separation: 2.5,   // Very spread out
    alignment: 2.0,    // Highly coordinated — emergence visible
    cohesion: 0.5,     // Minimal clumping
    dogFear: 1.0,      // Barely responsive to dog
    penAttraction: 0.1,
    personalityMod: 1.0, // Personalities fully expressed
  },
};

// Personality modifiers — each personality tweaks the flocking weights
const PERSONALITY_MODS: Record<string, Partial<FlockingParams>> = {
  follower: { cohesion: 1.5, alignment: 1.3, separation: 0.8 },
  wanderer: { cohesion: 0.5, alignment: 0.3, separation: 1.8 },
  leader: { alignment: 1.5, dogFear: 0.7 },
  stubborn: { barkInfluence: 0.3, dogFear: 0.5, cohesion: 0.4 },
  curious: { barkInfluence: 1.5, dogFear: 0.8 },
  nervous: { dogFear: 3.0, separation: 2.0, speed: SHEEP_BASE_SPEED * 1.3 },
  brave: { dogFear: 0.5, barkInfluence: 0.8, speed: SHEEP_BASE_SPEED * 1.1 },
  lazy: { speed: SHEEP_BASE_SPEED * 0.6, cohesion: 1.5 },
};

function vec2Add(a: Vec2, b: Vec2): Vec2 { return { x: a.x + b.x, y: a.y + b.y }; }
function vec2Sub(a: Vec2, b: Vec2): Vec2 { return { x: a.x - b.x, y: a.y - b.y }; }
function vec2Scale(v: Vec2, s: number): Vec2 { return { x: v.x * s, y: v.y * s }; }
function vec2Len(v: Vec2): number { return Math.sqrt(v.x * v.x + v.y * v.y); }
function vec2Norm(v: Vec2): Vec2 { const l = vec2Len(v) || 1; return { x: v.x / l, y: v.y / l }; }
function vec2Dist(a: Vec2, b: Vec2): number { return vec2Len(vec2Sub(a, b)); }

function clampVec(v: Vec2, maxLen: number): Vec2 {
  const l = vec2Len(v);
  if (l > maxLen) return vec2Scale(vec2Norm(v), maxLen);
  return v;
}

export function updateFlocking(
  sheep: SheepEntity[],
  dog: DogEntity,
  grid: Tile[][],
  gridWidth: number,
  gridHeight: number,
  params: FlockingParams,
  dt: number
): void {
  const penPos = { x: gridWidth - 4, y: gridHeight - 3 };

  // Update neighbor lists
  for (const s of sheep) {
    if (s.isInPen || s.isLost) continue;
    s.neighbors = sheep
      .filter(other => other.id !== s.id && !other.isInPen && !other.isLost && vec2Dist(s.pos, other.pos) < FLOCK_DETECT_RADIUS)
      .map(other => other.id);
  }

  // Calculate and apply forces for each sheep
  for (const s of sheep) {
    if (s.isInPen || s.isLost) continue;

    const neighbors = sheep.filter(n => s.neighbors.includes(n.id));

    // Get personality-modified params
    const pMod = PERSONALITY_MODS[s.personality] || {};
    const sep = (params.separation + (pMod.separation ?? 0)) * params.personalityMod + params.separation * (1 - params.personalityMod);
    const ali = (params.alignment + (pMod.alignment ?? 0)) * params.personalityMod + params.alignment * (1 - params.personalityMod);
    const coh = (params.cohesion + (pMod.cohesion ?? 0)) * params.personalityMod + params.cohesion * (1 - params.personalityMod);
    const bark = params.barkInfluence + (pMod.barkInfluence ?? 0);
    const fear = params.dogFear + (pMod.dogFear ?? 0);
    const speed = (pMod.speed ?? params.speed);

    let force: Vec2 = { x: 0, y: 0 };

    // 1. SEPARATION — avoid crowding neighbors
    if (neighbors.length > 0) {
      let sepForce: Vec2 = { x: 0, y: 0 };
      let count = 0;
      for (const n of neighbors) {
        const d = vec2Dist(s.pos, n.pos);
        if (d < SEPARATION_RADIUS && d > 0) {
          const diff = vec2Scale(vec2Norm(vec2Sub(s.pos, n.pos)), 1 / d);
          sepForce = vec2Add(sepForce, diff);
          count++;
        }
      }
      if (count > 0) {
        sepForce = vec2Scale(sepForce, sep / count);
        force = vec2Add(force, sepForce);
      }
    }

    // 2. ALIGNMENT — steer towards average heading of neighbors
    if (neighbors.length > 0) {
      let avgVel: Vec2 = { x: 0, y: 0 };
      for (const n of neighbors) {
        avgVel = vec2Add(avgVel, n.vel);
      }
      avgVel = vec2Scale(avgVel, 1 / neighbors.length);
      const aliForce = vec2Scale(avgVel, ali * 0.1);
      force = vec2Add(force, aliForce);
    }

    // 3. COHESION — steer towards average position of neighbors
    if (neighbors.length > 0) {
      let avgPos: Vec2 = { x: 0, y: 0 };
      for (const n of neighbors) {
        avgPos = vec2Add(avgPos, n.pos);
      }
      avgPos = vec2Scale(avgPos, 1 / neighbors.length);
      const toCenter = vec2Sub(avgPos, s.pos);
      const cohForce = vec2Scale(vec2Norm(toCenter), coh * 0.05);
      force = vec2Add(force, cohForce);
    }

    // 4. DOG FEAR — flee from dog
    const dogDist = vec2Dist(s.pos, dog.pos);
    if (dogDist < BARK_BASE_RADIUS * 2 && dogDist > 0) {
      const awayFromDog = vec2Norm(vec2Sub(s.pos, dog.pos));
      const fearStrength = fear * (1 - dogDist / (BARK_BASE_RADIUS * 2));
      force = vec2Add(force, vec2Scale(awayFromDog, fearStrength));
    }

    // 5. BARK INFLUENCE — directional push from bark
    if (dog.isBarking && dog.barkCooldown <= 0) {
      const barkDist = vec2Dist(s.pos, dog.pos);
      if (barkDist < BARK_BASE_RADIUS && barkDist > 0) {
        let barkDir: Vec2;
        // Guide bark pushes sheep in dog's facing direction
        if (dog.abilities.includes(DogAbility.GuideBark) || !dog.activeAbility || dog.activeAbility === DogAbility.GuideBark) {
          const facingDir: Record<string, Vec2> = {
            up: { x: 0, y: -1 }, down: { x: 0, y: 1 }, left: { x: -1, y: 0 }, right: { x: 1, y: 0 },
          };
          barkDir = facingDir[dog.facing] || { x: 0, y: -1 };
        } else {
          // Default: push away from dog
          barkDir = vec2Norm(vec2Sub(s.pos, dog.pos));
        }
        const barkForce = vec2Scale(barkDir, bark * (1 - barkDist / BARK_BASE_RADIUS));
        force = vec2Add(force, barkForce);
      }

      // Scatter bark — push in all directions
      if (dog.activeAbility === DogAbility.ScatterBark) {
        const away = vec2Norm(vec2Sub(s.pos, dog.pos));
        force = vec2Add(force, vec2Scale(away, bark * 2));
      }

      // Calm bark — reduce fear, increase happiness
      if (dog.activeAbility === DogAbility.CalmBark) {
        s.happiness = Math.min(100, s.happiness + 15);
      }

      // Howl — attract toward dog
      if (dog.activeAbility === DogAbility.Howl) {
        const toward = vec2Norm(vec2Sub(dog.pos, s.pos));
        force = vec2Add(force, vec2Scale(toward, bark * 1.5));
      }
    }

    // 6. PEN ATTRACTION — subtle pull toward pen (increases as sheep get closer)
    const distToPen = vec2Dist(s.pos, penPos);
    if (distToPen < 8 && distToPen > 0.5) {
      const towardPen = vec2Norm(vec2Sub(penPos, s.pos));
      const penForce = vec2Scale(towardPen, params.penAttraction * (1 - distToPen / 8));
      force = vec2Add(force, penForce);
    }

    // 7. TERRAIN AVOIDANCE — avoid water, fences, rocks
    const tileX = Math.round(s.pos.x);
    const tileY = Math.round(s.pos.y);
    const lookAhead: Vec2[] = [
      { x: s.pos.x + 1, y: s.pos.y },
      { x: s.pos.x - 1, y: s.pos.y },
      { x: s.pos.x, y: s.pos.y + 1 },
      { x: s.pos.x, y: s.pos.y - 1 },
    ];
    for (const look of lookAhead) {
      const lx = Math.round(look.x);
      const ly = Math.round(look.y);
      const tile = grid[ly]?.[lx];
      if (tile && !tile.walkable) {
        const awayFromWall = vec2Norm(vec2Sub(s.pos, look));
        force = vec2Add(force, vec2Scale(awayFromWall, 2.0));
      }
    }

    // 8. BOUNDARY AVOIDANCE — soft boundary at grid edges
    const margin = 1.5;
    if (s.pos.x < margin) force.x += (margin - s.pos.x) * 2;
    if (s.pos.x > gridWidth - 1 - margin) force.x -= (s.pos.x - (gridWidth - 1 - margin)) * 2;
    if (s.pos.y < margin) force.y += (margin - s.pos.y) * 2;
    if (s.pos.y > gridHeight - 1 - margin) force.y -= (s.pos.y - (gridHeight - 1 - margin)) * 2;

    // Apply force with damping
    const damping = 0.92;
    s.vel = {
      x: (s.vel.x * damping + force.x * dt) ,
      y: (s.vel.y * damping + force.y * dt) ,
    };

    // Clamp speed
    const maxSpeed = speed * dt;
    s.vel = clampVec(s.vel, maxSpeed);

    // Update position
    const newPos = vec2Add(s.pos, s.vel);
    const newTileX = Math.round(newPos.x);
    const newTileY = Math.round(newPos.y);

    // Collision check
    const targetTile = grid[newTileY]?.[newTileX];
    if (targetTile?.walkable) {
      s.pos = newPos;
    } else if (targetTile?.swimable) {
      // Can't swim — bounce back
      s.vel = vec2Scale(s.vel, -0.5);
    } else {
      // Try sliding along axis
      const slideX = { ...newPos, y: s.pos.y };
      const slideY = { ...newPos, x: s.pos.x };
      const tileXCheck = grid[Math.round(slideX.y)]?.[Math.round(slideX.x)];
      const tileYCheck = grid[Math.round(slideY.y)]?.[Math.round(slideY.x)];
      if (tileXCheck?.walkable) {
        s.pos = slideX;
      } else if (tileYCheck?.walkable) {
        s.pos = slideY;
      } else {
        s.vel = vec2Scale(s.vel, -0.3);
      }
    }

    // Clamp to grid bounds
    s.pos.x = Math.max(0.5, Math.min(gridWidth - 1.5, s.pos.x));
    s.pos.y = Math.max(0.5, Math.min(gridHeight - 1.5, s.pos.y));

    // Update facing
    if (Math.abs(s.vel.x) > 0.01 || Math.abs(s.vel.y) > 0.01) {
      s.isMoving = true;
      if (Math.abs(s.vel.x) > Math.abs(s.vel.y)) {
        s.facing = s.vel.x > 0 ? 'right' : 'left';
      } else {
        s.facing = s.vel.y > 0 ? 'down' : 'up';
      }
      s.animFrame = (s.animFrame + dt * 6) % 4;
    } else {
      s.isMoving = false;
    }

    // Energy/happiness decay
    s.energy = Math.max(0, s.energy - 0.3 * dt);
    s.happiness = Math.max(0, s.happiness - 0.2 * dt);
  }
}

// Check if sheep entered pen
export function checkPenEntries(
  sheep: SheepEntity[],
  gridWidth: number,
  gridHeight: number
): { newlyPenned: SheepEntity[]; count: number } {
  const penX = gridWidth - 6;
  const penY = gridHeight - 5;
  const newlyPenned: SheepEntity[] = [];

  for (const s of sheep) {
    if (s.isInPen || s.isLost) continue;
    const inPen = s.pos.x >= penX + 1 && s.pos.x <= penX + 3 && s.pos.y >= penY + 1 && s.pos.y <= penY + 2;
    if (inPen) {
      s.isInPen = true;
      s.happiness = Math.min(100, s.happiness + 20);
      newlyPenned.push(s);
    }
  }

  return { newlyPenned, count: sheep.filter(s => s.isInPen).length };
}

// Check if sheep are lost (stuck at edge too long)
export function checkLostSheep(
  sheep: SheepEntity[],
  gridWidth: number,
  gridHeight: number,
  lostThreshold: number = 15
): SheepEntity[] {
  const newlyLost: SheepEntity[] = [];
  const margin = 1.5;

  for (const s of sheep) {
    if (s.isInPen || s.isLost) continue;
    const atEdge = s.pos.x < margin || s.pos.x > gridWidth - 1 - margin ||
                   s.pos.y < margin || s.pos.y > gridHeight - 1 - margin;
    if (atEdge) {
      s.energy = Math.max(0, s.energy - 2);
      if (s.energy <= 0) {
        s.isLost = true;
        newlyLost.push(s);
      }
    }
  }

  return newlyLost;
}
