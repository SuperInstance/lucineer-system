// ============================================================
// MIST — Save/Load System (localStorage)
// Persistent progress is the HOOK that keeps players coming back
// ============================================================

import { SaveData, Rank, LevelResult, SheepBreed, DailyChallenge, RANK_ORDER } from './types';
import { ALL_DISCOVERIES } from './collections';
import { getTodayString, generateDailyChallenge } from './daily';

const SAVE_KEY = 'mist_save_data';
const SAVE_VERSION = 1;

export function createNewSave(): SaveData {
  return {
    version: SAVE_VERSION,
    lastPlayed: new Date().toISOString(),
    totalPlayTime: 0,
    currentRank: Rank.Apprentice,
    skillPoints: 2, // Start with 2 to unlock first skills immediately
    totalSkillPoints: 2,
    levelResults: {},
    highestUnlockedLevel: 'app-1',
    unlockedSkills: [],
    stickers: { first_steps: true }, // Starting sticker
    stickerCount: 1,
    discoveries: {},
    discoveryCount: 0,
    sheepCatalog: {
      [SheepBreed.Wooly]: false,
      [SheepBreed.Merino]: false,
      [SheepBreed.Highland]: false,
      [SheepBreed.Suffolk]: false,
      [SheepBreed.Dorper]: false,
      [SheepBreed.Jacob]: false,
      [SheepBreed.Soay]: false,
      [SheepBreed.Valais]: false,
      [SheepBreed.Navajo]: false,
      [SheepBreed.Katahdin]: false,
      [SheepBreed.Cheviot]: false,
      [SheepBreed.Romanov]: false,
    },
    farmUpgrades: [],
    dailyChallenges: {},
    dailyStreak: 0,
    lastDailyDate: '',
    totalSheepHerded: 0,
    totalBarks: 0,
    totalTimePlayed: 0,
    totalLevelsCompleted: 0,
    perfectHerds: 0,
    musicVolume: 0.7,
    sfxVolume: 0.8,
    parentLayerEnabled: true,
    showTutorials: true,
  };
}

export function loadSave(): SaveData {
  if (typeof window === 'undefined') return createNewSave();
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return createNewSave();
    const data = JSON.parse(raw) as SaveData;
    // Migration support
    if (data.version < SAVE_VERSION) {
      return migrateSave(data);
    }
    return data;
  } catch {
    return createNewSave();
  }
}

export function saveSave(data: SaveData): void {
  if (typeof window === 'undefined') return;
  data.lastPlayed = new Date().toISOString();
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(data));
  } catch {
    // Storage full — try clearing old data
    console.warn('MIST: Save failed — storage may be full');
  }
}

function migrateSave(old: SaveData): SaveData {
  const newData = createNewSave();
  // Preserve known fields
  newData.levelResults = old.levelResults || {};
  newData.unlockedSkills = old.unlockedSkills || [];
  newData.stickers = old.stickers || {};
  newData.discoveries = old.discoveries || {};
  newData.sheepCatalog = old.sheepCatalog || {};
  newData.totalSheepHerded = old.totalSheepHerded || 0;
  newData.totalBarks = old.totalBarks || 0;
  newData.totalLevelsCompleted = old.totalLevelsCompleted || 0;
  newData.skillPoints = (old.totalSkillPoints ?? 2) - (old.unlockedSkills?.length ?? 0);
  newData.totalSkillPoints = old.totalSkillPoints ?? 2;
  newData.currentRank = old.currentRank || Rank.Apprentice;
  return newData;
}

export function saveLevelResult(save: SaveData, result: LevelResult): SaveData {
  const existing = save.levelResults[result.levelId];
  const isNew = !existing || result.stars > existing.stars;
  const isPersonalBest = !existing || result.time < existing.time;
  
  const updated = {
    ...save,
    levelResults: {
      ...save.levelResults,
      [result.levelId]: {
        ...result,
        personalBest: isPersonalBest,
        stars: Math.max(existing?.stars ?? 0, result.stars),
        time: Math.min(existing?.time ?? Infinity, result.time),
      },
    },
    // Only count stats delta on improvement (no inflation on replay)
    totalSheepHerded: save.totalSheepHerded + (isNew ? Math.max(0, result.sheepHerded - (existing?.sheepHerded ?? 0)) : 0),
    totalBarks: save.totalBarks + (isNew ? Math.max(0, result.barksUsed - (existing?.barksUsed ?? 0)) : 0),
    totalTimePlayed: save.totalTimePlayed + result.time,
    totalLevelsCompleted: save.totalLevelsCompleted + (isNew ? 1 : 0),
  };

  // Award skill points for new stars
  if (isNew) {
    const newStars = result.stars - (existing?.stars ?? 0);
    const pointsEarned = newStars * 2;
    updated.skillPoints += pointsEarned;
    updated.totalSkillPoints += pointsEarned;
  }

  // Check for rank advancement
  updated.currentRank = calculateRank(updated);

  // Check for new highest unlocked level
  const completedLevelIds = Object.keys(updated.levelResults).filter(id => (updated.levelResults[id].stars ?? 0) >= 1);
  if (completedLevelIds.length > 0) {
    updated.highestUnlockedLevel = completedLevelIds[completedLevelIds.length - 1];
  }

  // Perfect herd check
  if (result.sheepHerded === result.sheepTotal) {
    updated.perfectHerds = (updated.perfectHerds || 0) + 1;
  }

  // Award stickers for milestones
  if (updated.totalLevelsCompleted >= 1 && !updated.stickers['first_herd']) {
    updated.stickers['first_herd'] = true;
    updated.stickerCount++;
  }
  if (updated.totalSheepHerded >= 50 && !updated.stickers['fifty_club']) {
    updated.stickers['fifty_club'] = true;
    updated.stickerCount++;
  }
  if (updated.perfectHerds >= 5 && !updated.stickers['perfect_five']) {
    updated.stickers['perfect_five'] = true;
    updated.stickerCount++;
  }

  return updated;
}

export function saveDiscovery(save: SaveData, conceptKey: string): SaveData {
  if (save.discoveries[conceptKey]) return save;
  return {
    ...save,
    discoveries: { ...save.discoveries, [conceptKey]: true },
    discoveryCount: save.discoveryCount + 1,
  };
}

export function saveBreedCatalog(save: SaveData, breed: SheepBreed): SaveData {
  if (save.sheepCatalog[breed]) return save;
  return {
    ...save,
    sheepCatalog: { ...save.sheepCatalog, [breed]: true },
  };
}

export function unlockSkill(save: SaveData, skillId: string, cost: number): SaveData {
  if (save.unlockedSkills.includes(skillId)) return save;
  if (save.skillPoints < cost) return save;
  return {
    ...save,
    unlockedSkills: [...save.unlockedSkills, skillId],
    skillPoints: save.skillPoints - cost,
  };
}

export function saveDailyChallenge(save: SaveData, challenge: DailyChallenge): SaveData {
  const today = getTodayString();
  // Update streak
  let newStreak = save.dailyStreak;
  if (save.lastDailyDate !== today) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toISOString().split('T')[0];
    newStreak = save.lastDailyDate === yesterdayStr ? save.dailyStreak + 1 : 1;
  }
  return {
    ...save,
    dailyChallenges: { ...save.dailyChallenges, [today]: challenge },
    dailyStreak: newStreak,
    lastDailyDate: today,
    skillPoints: save.skillPoints + (challenge.completed ? challenge.reward.skillPoints : 0),
    totalSkillPoints: save.totalSkillPoints + (challenge.completed ? challenge.reward.skillPoints : 0),
  };
}

export function calculateRank(save: SaveData): Rank {
  const totalStars = Object.values(save.levelResults).reduce((sum, r) => sum + (r.stars ?? 0), 0);
  const completedLevels = Object.values(save.levelResults).filter(r => (r.stars ?? 0) >= 1).length;

  if (totalStars >= 20 && completedLevels >= 8) return Rank.Elder;
  if (totalStars >= 12 && completedLevels >= 5) return Rank.Master;
  if (totalStars >= 5 && completedLevels >= 3) return Rank.Journeyman;
  return Rank.Apprentice;
}

export function getCompletionPercentage(save: SaveData): number {
  // Stars are 60% weight, discoveries are 40%
  const totalPossibleStars = 10 * 3; // Updated for 10 levels
  const earnedStars = Object.values(save.levelResults).reduce((sum, r) => sum + (r.stars ?? 0), 0);
  const totalDiscoveries = Object.keys(ALL_DISCOVERIES).length || 1;
  const foundDiscoveries = Object.keys(save.discoveries).length;
  const starPct = earnedStars / totalPossibleStars;
  const discPct = foundDiscoveries / totalDiscoveries;
  return Math.min(100, Math.round((starPct * 0.6 + discPct * 0.4) * 100));
}

export function resetSave(): SaveData {
  if (typeof window === 'undefined') return createNewSave();
  localStorage.removeItem(SAVE_KEY);
  return createNewSave();
}

// Auto-save hook support
export function autoSave(save: SaveData): void {
  saveSave(save);
}
