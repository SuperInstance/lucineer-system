// MIST Game Engine — Utility Functions (Expanded v2.0)

import { CellType } from './types';
import type { WorldCell, SeasonConfig } from './types';

// -- XP helpers --

const XP_THRESHOLDS = [0, 50, 125, 250, 400, 600, 850] as const;

export function xpForLevel(level: number): number {
  if (level < 0) return 0;
  if (level >= XP_THRESHOLDS.length) return XP_THRESHOLDS[XP_THRESHOLDS.length - 1]!;
  return XP_THRESHOLDS[level]!;
}

export function xpProgress(xp: number, level: number): number {
  if (level >= XP_THRESHOLDS.length - 1) return 1;
  const currentMin = XP_THRESHOLDS[level]!;
  const nextMin = XP_THRESHOLDS[level + 1]!;
  const range = nextMin - currentMin;
  if (range <= 0) return 1;
  return Math.min(1, Math.max(0, (xp - currentMin) / range));
}

// -- World unlock helpers --

const WORLD_UNLOCK_LEVELS: Record<string, number> = {
  farm: 0, forest: 0, village: 1, mountain: 2,
  meadow: 1, lake: 2, ruins: 3, sky: 3,
};

export function worldUnlockLevel(worldId: string): number {
  return WORLD_UNLOCK_LEVELS[worldId] ?? 0;
}

export function isWorldUnlocked(worldId: string, playerLevel: number): boolean {
  return playerLevel >= worldUnlockLevel(worldId);
}

// -- Cell emoji map --

const CELL_EMOJI: Record<CellType, string> = {
  [CellType.GRASS]: '\u{1F7E9}',
  [CellType.FIELD]: '\u{1F33E}',
  [CellType.WATER]: '\u{1F7E6}',
  [CellType.TREE]: '\u{1F332}',
  [CellType.ROCK]: '\u{1FAA8}',
  [CellType.FENCE]: '\u{1F532}',
  [CellType.GATE]: '\u{1F6AA}',
  [CellType.SHEEP]: '\u{1F411}',
  [CellType.RAM]: '\u{1F410}',
  [CellType.BARN]: '\u{1F3DA}',
  [CellType.KENNEL]: '\u{1F3E0}',
  [CellType.FLOWER]: '\u{1F338}',
  [CellType.MUSHROOM]: '\u{1F344}',
  [CellType.BRIDGE]: '\u{1F309}',
  [CellType.PATH]: '\u{1F7EB}',
  [CellType.HOUSE]: '\u{1F3D8}',
  [CellType.MOUNTAIN]: '\u26F0',
  [CellType.CAVE]: '\u{1F573}',
  [CellType.CRYSTAL]: '\u{1F48E}',
  [CellType.CAMPFIRE]: '\u{1F525}',
  [CellType.SIGN]: '\u{1FAA7}',
  [CellType.PEN]: '\u2B1C',
  [CellType.DOG]: '\u{1F415}',
  [CellType.EMPTY]: '\u2B1B',
  [CellType.PUDDLE]: '\u{1F4A7}',
  [CellType.BUSH]: '\u{1F333}',
  [CellType.LOG]: '\u{1FAB5}',
  [CellType.WELL]: '\u{1FAA2}',
  [CellType.HAYBALE]: '\u{1F33E}',
  [CellType.PUMPKIN]: '\u{1F383}',
  [CellType.LILYPAD]: '\u{1F33A}',
  [CellType.REED]: '\u{1F33F}',
  [CellType.DOCK]: '\u{1F6A2}',
  [CellType.BOAT]: '\u{26F5}',
  [CellType.STATUE]: '\u{1F5FF}',
  [CellType.PILLAR]: '\u{1F3DB}',
  [CellType.CRACKED_WALL]: '\u{1F9F1}',
  [CellType.MOSAIC]: '\u{1F3A8}',
  [CellType.COLUMN]: '\u{1F3DB}',
  [CellType.BOOKSHELF]: '\u{1F4DA}',
  [CellType.CLOUD]: '\u2601',
  [CellType.RAINBOW]: '\u{1F308}',
  [CellType.STAR_FLOWER]: '\u{1F490}',
  [CellType.GLOW_MUSHROOM]: '\u{1F436}',
  [CellType.ICICLE]: '\u2744',
  [CellType.HOT_SPRING]: '\u{2668}',
  [CellType.LAVA_ROCK]: '\u{1F30B}',
  [CellType.WHIRLPOOL]: '\u{1F300}',
  [CellType.CHEST]: '\u{1F4E6}',
  [CellType.FLAG]: '\u{1F6A9}',
  [CellType.TOTEM]: '\u{1FA97}',
  [CellType.BENCHMARK]: '\u{1F4CA}',
  [CellType.SCROLL]: '\u{1F4DC}',
  [CellType.TELEPORTER]: '\u{1F300}',
};

export function getCellEmoji(cell: WorldCell): string {
  return CELL_EMOJI[cell.type] ?? '\u2B1B';
}

// -- Cell color map for CSS voxel rendering --

const CELL_COLORS: Partial<Record<CellType, { bg: string; border: string; shadow: string }>> = {
  [CellType.GRASS]: { bg: '#4ade80', border: '#22c55e', shadow: '#16a34a' },
  [CellType.FIELD]: { bg: '#fbbf24', border: '#f59e0b', shadow: '#d97706' },
  [CellType.WATER]: { bg: '#38bdf8', border: '#0ea5e9', shadow: '#0284c7' },
  [CellType.TREE]: { bg: '#166534', border: '#15803d', shadow: '#14532d' },
  [CellType.ROCK]: { bg: '#a8a29e', border: '#78716c', shadow: '#57534e' },
  [CellType.FENCE]: { bg: '#a16207', border: '#854d0e', shadow: '#713f12' },
  [CellType.GATE]: { bg: '#ca8a04', border: '#a16207', shadow: '#854d0e' },
  [CellType.SHEEP]: { bg: '#f5f5f4', border: '#d6d3d1', shadow: '#a8a29e' },
  [CellType.RAM]: { bg: '#78350f', border: '#92400e', shadow: '#451a03' },
  [CellType.BARN]: { bg: '#b91c1c', border: '#991b1b', shadow: '#7f1d1d' },
  [CellType.KENNEL]: { bg: '#92400e', border: '#78350f', shadow: '#451a03' },
  [CellType.FLOWER]: { bg: '#f9a8d4', border: '#ec4899', shadow: '#db2777' },
  [CellType.MUSHROOM]: { bg: '#d946ef', border: '#c026d3', shadow: '#a21caf' },
  [CellType.BRIDGE]: { bg: '#a16207', border: '#854d0e', shadow: '#713f12' },
  [CellType.PATH]: { bg: '#d6d3d1', border: '#a8a29e', shadow: '#78716c' },
  [CellType.HOUSE]: { bg: '#f97316', border: '#ea580c', shadow: '#c2410c' },
  [CellType.MOUNTAIN]: { bg: '#64748b', border: '#475569', shadow: '#334155' },
  [CellType.CAVE]: { bg: '#1c1917', border: '#292524', shadow: '#0c0a09' },
  [CellType.CRYSTAL]: { bg: '#a78bfa', border: '#8b5cf6', shadow: '#7c3aed' },
  [CellType.CAMPFIRE]: { bg: '#f97316', border: '#ef4444', shadow: '#dc2626' },
  [CellType.SIGN]: { bg: '#a16207', border: '#854d0e', shadow: '#713f12' },
  [CellType.PEN]: { bg: '#e7e5e4', border: '#d6d3d1', shadow: '#a8a29e' },
  [CellType.PUDDLE]: { bg: '#7dd3fc', border: '#38bdf8', shadow: '#0ea5e9' },
  [CellType.BUSH]: { bg: '#22c55e', border: '#16a34a', shadow: '#15803d' },
  [CellType.LOG]: { bg: '#92400e', border: '#78350f', shadow: '#451a03' },
  [CellType.WELL]: { bg: '#6b7280', border: '#4b5563', shadow: '#374151' },
  [CellType.HAYBALE]: { bg: '#fbbf24', border: '#f59e0b', shadow: '#d97706' },
  [CellType.PUMPKIN]: { bg: '#f97316', border: '#ea580c', shadow: '#c2410c' },
  [CellType.LILYPAD]: { bg: '#4ade80', border: '#22c55e', shadow: '#16a34a' },
  [CellType.DOCK]: { bg: '#a16207', border: '#854d0e', shadow: '#713f12' },
  [CellType.STATUE]: { bg: '#d6d3d1', border: '#a8a29e', shadow: '#78716c' },
  [CellType.PILLAR]: { bg: '#e7e5e4', border: '#d6d3d1', shadow: '#a8a29e' },
  [CellType.CRACKED_WALL]: { bg: '#78716c', border: '#57534e', shadow: '#44403c' },
  [CellType.MOSAIC]: { bg: '#c084fc', border: '#a855f7', shadow: '#9333ea' },
  [CellType.COLUMN]: { bg: '#d6d3d1', border: '#a8a29e', shadow: '#78716c' },
  [CellType.BOOKSHELF]: { bg: '#92400e', border: '#78350f', shadow: '#451a03' },
  [CellType.CLOUD]: { bg: '#f0f9ff', border: '#e0f2fe', shadow: '#bae6fd' },
  [CellType.RAINBOW]: { bg: '#fbbf24', border: '#f472b6', shadow: '#8b5cf6' },
  [CellType.STAR_FLOWER]: { bg: '#fde68a', border: '#fbbf24', shadow: '#f59e0b' },
  [CellType.GLOW_MUSHROOM]: { bg: '#e879f9', border: '#d946ef', shadow: '#a21caf' },
  [CellType.HOT_SPRING]: { bg: '#67e8f9', border: '#22d3ee', shadow: '#06b6d4' },
  [CellType.LAVA_ROCK]: { bg: '#dc2626', border: '#991b1b', shadow: '#7f1d1d' },
  [CellType.WHIRLPOOL]: { bg: '#0284c7', border: '#0369a1', shadow: '#075985' },
  [CellType.CHEST]: { bg: '#a16207', border: '#854d0e', shadow: '#713f12' },
  [CellType.FLAG]: { bg: '#dc2626', border: '#991b1b', shadow: '#7f1d1d' },
  [CellType.TOTEM]: { bg: '#78350f', border: '#92400e', shadow: '#451a03' },
  [CellType.BENCHMARK]: { bg: '#6b7280', border: '#4b5563', shadow: '#374151' },
  [CellType.SCROLL]: { bg: '#fef3c7', border: '#fbbf24', shadow: '#f59e0b' },
  [CellType.TELEPORTER]: { bg: '#818cf8', border: '#6366f1', shadow: '#4f46e5' },
  [CellType.REED]: { bg: '#22c55e', border: '#16a34a', shadow: '#15803d' },
  [CellType.BOAT]: { bg: '#92400e', border: '#78350f', shadow: '#451a03' },
  [CellType.ICICLE]: { bg: '#bae6fd', border: '#7dd3fc', shadow: '#38bdf8' },
  [CellType.EMPTY]: { bg: '#18181b', border: '#18181b', shadow: '#09090b' },
};

export function getCellColors(cell: WorldCell): { bg: string; border: string; shadow: string } {
  return CELL_COLORS[cell.type] ?? { bg: '#18181b', border: '#18181b', shadow: '#09090b' };
}

// -- Season configs --

export const SEASONS: Record<SeasonConfig['id'], SeasonConfig> = {
  spring: {
    id: 'spring', name: 'Spring', emoji: '\u{1F338}',
    tintColor: 'rgba(144, 238, 144, 0.06)',
    bgGradient: 'from-green-950 to-emerald-950',
    particles: [],
  },
  summer: {
    id: 'summer', name: 'Summer', emoji: '\u2600',
    tintColor: 'rgba(255, 255, 0, 0.04)',
    bgGradient: 'from-green-950 to-stone-950',
    particles: [],
  },
  autumn: {
    id: 'autumn', name: 'Autumn', emoji: '\u{1F342}',
    tintColor: 'rgba(255, 165, 0, 0.08)',
    bgGradient: 'from-amber-950 to-stone-950',
    particles: [],
  },
  winter: {
    id: 'winter', name: 'Winter', emoji: '\u2744',
    tintColor: 'rgba(200, 220, 255, 0.1)',
    bgGradient: 'from-slate-900 to-slate-800',
    particles: [],
  },
};

// -- World visual metadata --

export const WORLD_META: Record<string, { emoji: string; color: string; bg: string; gradient: string }> = {
  farm: { emoji: '\u{1F33E}', color: 'text-amber-500', bg: 'bg-amber-950/40', gradient: 'from-green-950/80 to-amber-950/40' },
  forest: { emoji: '\u{1F332}', color: 'text-green-500', bg: 'bg-green-950/40', gradient: 'from-green-950/90 to-green-950/50' },
  village: { emoji: '\u{1F3D8}', color: 'text-orange-500', bg: 'bg-orange-950/40', gradient: 'from-amber-950/50 to-stone-950/50' },
  mountain: { emoji: '\u26F0', color: 'text-slate-400', bg: 'bg-slate-800/60', gradient: 'from-slate-900 to-slate-800' },
  meadow: { emoji: '\u{1F33F}', color: 'text-lime-500', bg: 'bg-lime-950/40', gradient: 'from-lime-950/60 to-green-950/40' },
  lake: { emoji: '\u{1F4A7}', color: 'text-cyan-500', bg: 'bg-cyan-950/40', gradient: 'from-cyan-950/50 to-blue-950/40' },
  ruins: { emoji: '\u{1F3DB}', color: 'text-purple-400', bg: 'bg-purple-950/40', gradient: 'from-purple-950/50 to-stone-950/50' },
  sky: { emoji: '\u2601', color: 'text-sky-400', bg: 'bg-sky-950/40', gradient: 'from-sky-950/40 to-amber-950/30' },
};

// -- Quest progress helpers --

export function getQuestProgressText(quest: { type: string; target: number }, progress: number): string {
  switch (quest.type) {
    case 'collect_sheep': return `${Math.min(progress, quest.target)}/${quest.target} sheep`;
    case 'find_discovery': return `${Math.min(progress, quest.target)}/${quest.target} discoveries`;
    case 'reach_position': return progress >= quest.target ? 'Reached!' : 'Not reached';
    case 'bark_count': return `${Math.min(progress, quest.target)}/${quest.target} barks`;
    case 'explore_cells': return `${progress} cells explored`;
    default: return `${progress}/${quest.target}`;
  }
}
