// ============================================================
// MIST — Skill Tree
// Unlockable abilities that change gameplay and create
// a persistent sense of growth and power
// ============================================================

import { SkillNode, Rank, DogAbility } from './types';

export const SKILL_TREE: SkillNode[] = [
  // ========================================
  // APPRENTICE SKILLS (Tier 1-2)
  // ========================================
  {
    id: 'app_stamina_1',
    name: 'Puppy Energy',
    description: 'Increase max stamina by 20%. Running around is tiring work!',
    icon: '⚡',
    cost: 1,
    rank: Rank.Apprentice,
    tier: 1,
    effect: { type: 'stat_boost', stat: 'stamina', value: 20, description: '+20% stamina' },
    unlocked: false,
  },
  {
    id: 'app_speed_1',
    name: 'Quick Paws',
    description: 'Move 15% faster. Every shepherd needs speed!',
    icon: '🐾',
    cost: 1,
    rank: Rank.Apprentice,
    tier: 1,
    effect: { type: 'stat_boost', stat: 'speed', value: 15, description: '+15% speed' },
    unlocked: false,
  },
  {
    id: 'app_bark_radius',
    name: 'Louder Bark',
    description: 'Your bark reaches 25% further. More sheep hear you!',
    icon: '📢',
    cost: 2,
    rank: Rank.Apprentice,
    tier: 2,
    requires: ['app_stamina_1'],
    effect: { type: 'stat_boost', stat: 'bark_radius', value: 25, description: '+25% bark radius' },
    unlocked: false,
  },
  {
    id: 'app_guide_bark',
    name: 'Guide Bark',
    description: 'Bark in a direction to PUSH sheep that way! The first real herding technique.',
    icon: '🧭',
    cost: 2,
    rank: Rank.Apprentice,
    tier: 2,
    requires: ['app_bark_radius'],
    effect: { type: 'unlock_ability', ability: DogAbility.GuideBark, description: 'Unlock: Guide Bark' },
    unlocked: false,
  },

  // ========================================
  // JOURNEYMAN SKILLS (Tier 1-2)
  // ========================================
  {
    id: 'jrn_scatter_bark',
    name: 'Scatter Bark',
    description: 'A sharp bark that scatters sheep in all directions. Useful when they clump up!',
    icon: '💥',
    cost: 3,
    rank: Rank.Journeyman,
    tier: 1,
    requires: ['app_guide_bark'],
    effect: { type: 'unlock_ability', ability: DogAbility.ScatterBark, description: 'Unlock: Scatter Bark' },
    unlocked: false,
  },
  {
    id: 'jrn_calm_bark',
    name: 'Soothing Bark',
    description: 'A gentle, low bark that calms nervous sheep and restores their happiness.',
    icon: '💙',
    cost: 3,
    rank: Rank.Journeyman,
    tier: 1,
    requires: ['app_guide_bark'],
    effect: { type: 'unlock_ability', ability: DogAbility.CalmBark, description: 'Unlock: Calm Bark' },
    unlocked: false,
  },
  {
    id: 'jrn_stamina_2',
    name: 'Endurance Training',
    description: 'Stamina regenerates 30% faster. Keep herding longer!',
    icon: '💪',
    cost: 2,
    rank: Rank.Journeyman,
    tier: 1,
    requires: ['app_stamina_1'],
    effect: { type: 'stat_boost', stat: 'stamina', value: 30, description: '+30% stamina regen' },
    unlocked: false,
  },
  {
    id: 'jrn_bark_cooldown',
    name: 'Rapid Bark',
    description: 'Bark cooldown reduced by 25%. Bark more often!',
    icon: '🔄',
    cost: 3,
    rank: Rank.Journeyman,
    tier: 2,
    requires: ['jrn_scatter_bark', 'jrn_calm_bark'],
    effect: { type: 'stat_boost', stat: 'bark_cooldown', value: 25, description: '-25% bark cooldown' },
    unlocked: false,
  },

  // ========================================
  // MASTER SKILLS (Tier 1-3)
  // ========================================
  {
    id: 'mst_howl',
    name: 'Elder Howl',
    description: 'Howl to ATTRACT all sheep toward you. The reverse of barking!',
    icon: '🐺',
    cost: 4,
    rank: Rank.Master,
    tier: 1,
    requires: ['jrn_calm_bark'],
    effect: { type: 'unlock_ability', ability: DogAbility.Howl, description: 'Unlock: Howl' },
    unlocked: false,
  },
  {
    id: 'mst_dash',
    name: 'Puppy Dash',
    description: 'Quick dash in your facing direction. Great for getting to sheep fast!',
    icon: '💨',
    cost: 3,
    rank: Rank.Master,
    tier: 1,
    requires: ['jrn_stamina_2'],
    effect: { type: 'unlock_ability', ability: DogAbility.Dash, description: 'Unlock: Dash' },
    unlocked: false,
  },
  {
    id: 'mst_super_sense',
    name: 'Super Sense',
    description: 'See through fog and find hidden discoveries. Nothing escapes your nose!',
    icon: '👁',
    cost: 4,
    rank: Rank.Master,
    tier: 2,
    requires: ['mst_howl', 'mst_dash'],
    effect: { type: 'unlock_ability', ability: DogAbility.SuperSense, description: 'Unlock: Super Sense' },
    unlocked: false,
  },
  {
    id: 'mst_rally',
    name: 'Rally Cry',
    description: 'Temporarily boost all sheep speed and happiness. Get them moving!',
    icon: '📯',
    cost: 4,
    rank: Rank.Master,
    tier: 2,
    requires: ['mst_howl'],
    effect: { type: 'unlock_ability', ability: DogAbility.Rally, description: 'Unlock: Rally Cry' },
    unlocked: false,
  },
  {
    id: 'mst_sheep_calm',
    name: 'Gentle Presence',
    description: 'Sheep near you calm down 50% faster. Your calm energy soothes the flock.',
    icon: '🌿',
    cost: 3,
    rank: Rank.Master,
    tier: 2,
    requires: ['jrn_calm_bark'],
    effect: { type: 'stat_boost', stat: 'sheep_calm_rate', value: 50, description: '+50% sheep calm rate' },
    unlocked: false,
  },

  // ========================================
  // ELDER SKILLS (Tier 1-3)
  // ========================================
  {
    id: 'eld_tunnel',
    name: 'Phase Dash',
    description: 'Dash THROUGH one obstacle. Like a ghost pup!',
    icon: '👻',
    cost: 5,
    rank: Rank.Elder,
    tier: 1,
    requires: ['mst_dash'],
    effect: { type: 'unlock_ability', ability: DogAbility.Tunnel, description: 'Unlock: Phase Dash' },
    unlocked: false,
  },
  {
    id: 'eld_visibility',
    name: 'Eagle Eye',
    description: 'See the entire field regardless of fog. True elder vision.',
    icon: '🦅',
    cost: 5,
    rank: Rank.Elder,
    tier: 1,
    requires: ['mst_super_sense'],
    effect: { type: 'stat_boost', stat: 'visibility', value: 100, description: 'Full visibility' },
    unlocked: false,
  },
  {
    id: 'eld_master_bark',
    name: 'Elder Bark',
    description: 'All barks are 50% more powerful and affect more sheep. The legendary technique!',
    icon: '✨',
    cost: 5,
    rank: Rank.Elder,
    tier: 2,
    requires: ['eld_tunnel', 'eld_visibility'],
    effect: { type: 'stat_boost', stat: 'bark_radius', value: 50, description: '+50% bark power' },
    unlocked: false,
  },
];

export function getSkillsForRank(rank: Rank): SkillNode[] {
  return SKILL_TREE.filter(s => s.rank === rank);
}

export function getAvailableSkills(unlockedIds: string[], skillPoints: number): SkillNode[] {
  return SKILL_TREE.filter(s => {
    if (s.unlocked) return false;
    if (s.cost > skillPoints) return false;
    if (s.requires) {
      if (!s.requires.every(req => unlockedIds.includes(req))) return false;
    }
    // Check rank is accessible (simplified — all ranks available)
    return true;
  });
}

export function canUnlockSkill(skillId: string, unlockedIds: string[], skillPoints: number): boolean {
  const skill = SKILL_TREE.find(s => s.id === skillId);
  if (!skill) return false;
  if (skill.unlocked) return false;
  if (skill.cost > skillPoints) return false;
  if (skill.requires) {
    if (!skill.requires.every(req => unlockedIds.includes(req))) return false;
  }
  return true;
}

export function getTotalSkillCost(): number {
  return SKILL_TREE.reduce((sum, s) => sum + s.cost, 0);
}
