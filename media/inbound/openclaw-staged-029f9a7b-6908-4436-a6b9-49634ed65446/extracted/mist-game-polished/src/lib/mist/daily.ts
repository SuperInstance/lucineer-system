// ============================================================
// MIST — Daily Challenge System
// A new unique challenge every day = reason to come back daily
// ============================================================

import { DailyChallenge, DailyRule, Weather, SheepBreed, SeededRNG } from './types';

export function getTodayString(): string {
  return new Date().toISOString().split('T')[0];
}

function dateSeed(dateStr: string): number {
  let hash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    const char = dateStr.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}

const DAILY_NAMES = [
  'Morning Mist', 'Golden Hour', 'Storm Chase', 'Frost Dawn',
  'Windy Ridge', 'Clover Field', 'Twilight Herd', 'Dewdrop Meadow',
  'Thunder Pasture', 'Calm Before Storm', 'Midnight Run', 'First Light',
  'Fog Valley', 'Autumn Drift', 'Spring Bloom', 'Summer Haze',
];

const DAILY_DESCRIPTIONS = [
  'A fresh start! The meadow awaits.',
  'The golden light makes everything beautiful — and tricky.',
  'Storm clouds gather. Can you herd before the rain?',
  'Frost covers the ground. Sheep slide and slip!',
  'Strong winds push the flock off course.',
  'Lucky clovers dot the field — and so do challenges.',
  'The fading light limits your time. Hurry!',
  'Morning dew makes the grass slippery.',
  'Thunder scares the sheep. They panic easily!',
  'Everything seems calm... but surprises lurk.',
  'A mysterious night challenge. Visibility is limited.',
  'The earliest herder gets the best pasture!',
  'Thick fog. Trust your instincts!',
  'Falling leaves obscure the path.',
  'New life springs up everywhere — including obstacles!',
  'Heat shimmers make distances hard to judge.',
];

const ALL_RULES: DailyRule[] = [
  { type: 'low_stamina', value: 0.6, description: 'Stamina drains 40% faster — manage your energy!' },
  { type: 'fast_sheep', value: 1.4, description: 'Sheep move 40% faster — harder to control!' },
  { type: 'fog_always', description: 'Permanent fog — limited visibility!' },
  { type: 'tiny_pen', description: 'The pen is smaller — precision herding required!' },
  { type: 'many_sheep', value: 15, description: '15 sheep to herd — a bigger flock!' },
  { type: 'mirrored', description: 'Controls are mirrored — everything feels backwards!' },
  { type: 'no_bark_limit', description: 'Unlimited barks but sheep are stubborn!' },
];

export function generateDailyChallenge(): DailyChallenge {
  const today = getTodayString();
  const seed = dateSeed(today);
  const rng = new SeededRNG(seed);

  const name = DAILY_NAMES[rng.nextInt(0, DAILY_NAMES.length - 1)];
  const description = DAILY_DESCRIPTIONS[rng.nextInt(0, DAILY_DESCRIPTIONS.length - 1)];

  // Pick 1-2 special rules
  const ruleCount = rng.nextBool(0.3) ? 2 : 1;
  const shuffledRules = rng.shuffle([...ALL_RULES]);
  const specialRules = shuffledRules.slice(0, ruleCount) as DailyRule[];

  // Calculate reward based on difficulty
  const difficulty = specialRules.reduce((sum, r) => {
    if (r.type === 'many_sheep') return sum + 2;
    if (r.type === 'fog_always' || r.type === 'mirrored') return sum + 2;
    return sum + 1;
  }, 0);

  const reward = {
    stickers: 1 + Math.floor(difficulty / 2),
    skillPoints: difficulty + 1,
    bonusDescription: difficulty >= 3 ? 'Bonus: Legendary sticker chance!' : 'Complete for rewards!',
  };

  return {
    date: today,
    seed,
    levelName: name,
    description,
    specialRules,
    reward,
    completed: false,
    stars: 0,
    bestTime: 0,
  };
}

export function getDailyChallengeForDate(dateStr: string): DailyChallenge {
  const seed = dateSeed(dateStr);
  const rng = new SeededRNG(seed);
  const name = DAILY_NAMES[rng.nextInt(0, DAILY_NAMES.length - 1)];
  const description = DAILY_DESCRIPTIONS[rng.nextInt(0, DAILY_DESCRIPTIONS.length - 1)];
  const ruleCount = rng.nextBool(0.3) ? 2 : 1;
  const shuffledRules = rng.shuffle([...ALL_RULES]);
  const specialRules = shuffledRules.slice(0, ruleCount) as DailyRule[];
  const difficulty = specialRules.reduce((sum, r) => r.type === 'many_sheep' ? sum + 2 : sum + 1, 0);

  return {
    date: dateStr,
    seed,
    levelName: name,
    description,
    specialRules,
    reward: {
      stickers: 1 + Math.floor(difficulty / 2),
      skillPoints: difficulty + 1,
      bonusDescription: 'Complete for rewards!',
    },
    completed: false,
    stars: 0,
    bestTime: 0,
  };
}

// Get daily weather based on seed
export function getDailyWeather(seed: number): Weather {
  const weathers = [Weather.Clear, Weather.Cloudy, Weather.Rainy, Weather.Foggy, Weather.Windy, Weather.Golden];
  return weathers[seed % weathers.length];
}

// Get sheep breeds for daily
export function getDailyBreeds(seed: number, count: number): SheepBreed[] {
  const allBreeds = Object.values(SheepBreed);
  const rng = new SeededRNG(seed + 42);
  const shuffled = rng.shuffle(allBreeds);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}
