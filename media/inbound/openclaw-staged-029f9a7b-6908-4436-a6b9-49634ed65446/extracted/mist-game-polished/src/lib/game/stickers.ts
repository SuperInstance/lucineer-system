import type { Sticker } from './types';

export const allStickers: Sticker[] = [
  // ── Farm set (4 earned + 1 world completion) ─────────────────────
  { id: 'sticker-woolly-wonder', emoji: '🐑', name: 'Woolly Wonder', category: 'farm', rarity: 'common' },
  { id: 'sticker-harvest-hero', emoji: '🌾', name: 'Harvest Hero', category: 'farm', rarity: 'common' },
  { id: 'sticker-good-pup', emoji: '🐕', name: 'Good Pup', category: 'farm', rarity: 'common' },
  { id: 'sticker-farm-hand', emoji: '🏡', name: 'Farm Hand', category: 'farm', rarity: 'common' },
  { id: 'sticker-farm-complete', emoji: '🥇', name: 'Farm Champion', category: 'farm', rarity: 'rare' },

  // ── Forest set (4 earned + 1 world completion) ───────────────────
  { id: 'sticker-tree-finder', emoji: '🌲', name: 'Tree Finder', category: 'forest', rarity: 'common' },
  { id: 'sticker-mushroom-master', emoji: '🍄', name: 'Mushroom Master', category: 'forest', rarity: 'common' },
  { id: 'sticker-bridge-builder', emoji: '🌉', name: 'Bridge Builder', category: 'forest', rarity: 'common' },
  { id: 'sticker-night-owl', emoji: '🦉', name: 'Night Owl', category: 'forest', rarity: 'common' },
  { id: 'sticker-forest-complete', emoji: '🌙', name: 'Forest Sage', category: 'forest', rarity: 'rare' },

  // ── Village set (4 earned + 1 world completion) ──────────────────
  { id: 'sticker-path-maker', emoji: '🏘️', name: 'Path Maker', category: 'village', rarity: 'common' },
  { id: 'sticker-fountain-friend', emoji: '⛲', name: 'Fountain Friend', category: 'village', rarity: 'common' },
  { id: 'sticker-bell-ringer', emoji: '🔔', name: 'Bell Ringer', category: 'village', rarity: 'common' },
  { id: 'sticker-knowledge-keeper', emoji: '📚', name: 'Knowledge Keeper', category: 'village', rarity: 'rare' },
  { id: 'sticker-village-complete', emoji: '🏛', name: 'Village Architect', category: 'village', rarity: 'rare' },

  // ── Mountain set (4 earned + 1 world completion) ─────────────────
  { id: 'sticker-crystal-collector', emoji: '💎', name: 'Crystal Collector', category: 'mountain', rarity: 'common' },
  { id: 'sticker-fire-tender', emoji: '🔥', name: 'Fire Tender', category: 'mountain', rarity: 'common' },
  { id: 'sticker-summit-star', emoji: '🏔️', name: 'Summit Star', category: 'mountain', rarity: 'rare' },
  { id: 'sticker-eagle-eye', emoji: '🦅', name: 'Eagle Eye', category: 'mountain', rarity: 'rare' },
  { id: 'sticker-mountain-complete', emoji: '🏔', name: 'Peak Conqueror', category: 'mountain', rarity: 'epic' },

  // ── Meadow set (4 earned + 1 world completion) ───────────────────
  { id: 'sticker-golden-bone', emoji: '🦴', name: 'Golden Bone', category: 'meadow', rarity: 'common' },
  { id: 'sticker-clover-luck', emoji: '🍀', name: 'Clover Luck', category: 'meadow', rarity: 'common' },
  { id: 'sticker-butterfly-dance', emoji: '🦋', name: 'Butterfly Dance', category: 'meadow', rarity: 'common' },
  { id: 'sticker-reward-hunter', emoji: '🌟', name: 'Reward Hunter', category: 'meadow', rarity: 'rare' },
  { id: 'sticker-meadow-complete', emoji: '🌈', name: 'Meadow Champion', category: 'meadow', rarity: 'epic' },

  // ── Lake set (4 earned + 1 world completion) ─────────────────────
  { id: 'sticker-pond-skimmer', emoji: '🐸', name: 'Pond Skimmer', category: 'lake', rarity: 'common' },
  { id: 'sticker-lily-pad-hop', emoji: '🪷', name: 'Lily Pad Hop', category: 'lake', rarity: 'common' },
  { id: 'sticker-crystal-clear', emoji: '💧', name: 'Crystal Clear', category: 'lake', rarity: 'common' },
  { id: 'sticker-pipe-liner', emoji: '🔧', name: 'Pipe Liner', category: 'lake', rarity: 'rare' },
  { id: 'sticker-lake-complete', emoji: '🌊', name: 'Lake Guardian', category: 'lake', rarity: 'epic' },

  // ── Ruins set (4 earned + 1 world completion) ────────────────────
  { id: 'sticker-scroll-reader', emoji: '📜', name: 'Scroll Reader', category: 'ruins', rarity: 'common' },
  { id: 'sticker-pillar-guardian', emoji: '🗿', name: 'Pillar Guardian', category: 'ruins', rarity: 'common' },
  { id: 'sticker-time-keeper', emoji: '⏳', name: 'Time Keeper', category: 'ruins', rarity: 'rare' },
  { id: 'sticker-memory-weaver', emoji: '🧵', name: 'Memory Weaver', category: 'ruins', rarity: 'rare' },
  { id: 'sticker-ruins-complete', emoji: '🏛️', name: 'Ruins Master', category: 'ruins', rarity: 'epic' },

  // ── Sky set (4 earned + 1 world completion) ──────────────────────
  { id: 'sticker-cloud-rider', emoji: '☁️', name: 'Cloud Rider', category: 'sky', rarity: 'common' },
  { id: 'sticker-star-catcher', emoji: '⭐', name: 'Star Catcher', category: 'sky', rarity: 'common' },
  { id: 'sticker-wind-chaser', emoji: '🍃', name: 'Wind Chaser', category: 'sky', rarity: 'rare' },
  { id: 'sticker-dream-weaver', emoji: '🌙', name: 'Dream Weaver', category: 'sky', rarity: 'rare' },
  { id: 'sticker-sky-complete', emoji: '🌌', name: 'Sky Sovereign', category: 'sky', rarity: 'epic' },

  // ── Special set (meta / level-up achievements) ───────────────────
  { id: 'sticker-alpha-student', emoji: '🎓', name: 'Alpha Student', category: 'special', rarity: 'rare' },
  { id: 'sticker-discovery-king', emoji: '👑', name: 'Discovery King', category: 'special', rarity: 'epic' },
  { id: 'sticker-ai-explorer', emoji: '🧠', name: 'AI Explorer', category: 'special', rarity: 'rare' },
  { id: 'sticker-mist-master', emoji: '🏆', name: 'MIST Master', category: 'special', rarity: 'legendary' },
  { id: 'sticker-first-steps', emoji: '🐾', name: 'First Steps', category: 'special', rarity: 'common' },
  { id: 'sticker-all-worlds', emoji: '🗺️', name: 'World Traveler', category: 'special', rarity: 'legendary' },
  { id: 'sticker-speed-pup', emoji: '⚡', name: 'Speed Pup', category: 'special', rarity: 'epic' },
  { id: 'sticker-collector', emoji: '🎁', name: 'Sticker Collector', category: 'special', rarity: 'rare' },
];

/** Return stickers that belong to a given world category. */
export function getStickersForWorld(worldId: string): Sticker[] {
  return allStickers.filter((s) => s.category === worldId);
}

/**
 * Return stickers unlockable at a given player level.
 *
 * Level 0 (Apprentice)       → farm
 * Level 1 (Journeyman)       → farm, forest
 * Level 2 (Master)           → farm, forest, village
 * Level 3 (Elder)            → farm, forest, village, mountain
 * Level 4                     → + meadow, lake
 * Level 5                     → + ruins, sky
 * Level 6+                    → + special
 */
export function getStickersForLevel(level: number): Sticker[] {
  const categoryMap: Record<number, string[]> = {
    0: ['farm'],
    1: ['farm', 'forest'],
    2: ['farm', 'forest', 'village'],
    3: ['farm', 'forest', 'village', 'mountain'],
    4: ['farm', 'forest', 'village', 'mountain', 'meadow', 'lake'],
    5: ['farm', 'forest', 'village', 'mountain', 'meadow', 'lake', 'ruins', 'sky'],
    6: ['farm', 'forest', 'village', 'mountain', 'meadow', 'lake', 'ruins', 'sky', 'special'],
  };

  const categories = categoryMap[level] ?? categoryMap[6]!;
  return allStickers.filter((s) => categories.includes(s.category));
}
