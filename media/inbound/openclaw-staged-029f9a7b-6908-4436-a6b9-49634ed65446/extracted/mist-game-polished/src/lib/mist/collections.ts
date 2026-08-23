// ============================================================
// MIST — Collections, Stickers, and Discoveries
// Completionism drives replay: 100+ things to find
// ============================================================

import { Sticker, StickerCategory, StickerRarity, FarmUpgrade, SheepBreed, CollectibleType } from './types';

export const ALL_STICKERS: Sticker[] = [
  // --- Achievement Stickers (Common) ---
  { id: 'first_steps', name: 'First Steps', description: 'Started your journey as a puppy!', icon: '🐾', category: StickerCategory.Achievement, rarity: StickerRarity.Common, unlocked: false },
  { id: 'first_herd', name: 'First Herd', description: 'Completed your first herding level!', icon: '🐑', category: StickerCategory.Achievement, rarity: StickerRarity.Common, unlocked: false },
  { id: 'rain_herder', name: 'Rain Herder', description: 'Herded sheep in the rain!', icon: '🌧', category: StickerCategory.Achievement, rarity: StickerRarity.Common, unlocked: false },
  { id: 'fog_navigator', name: 'Fog Navigator', description: 'Found your way through thick fog!', icon: '🌫', category: StickerCategory.Achievement, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'winter_herding', name: 'Winter Warrior', description: 'Herded in the snow!', icon: '❄', category: StickerCategory.Achievement, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'training_grounds', name: 'Training Master', description: 'Completed the training ground!', icon: '🏋', category: StickerCategory.Achievement, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'fifty_club', name: 'Fifty Club', description: 'Herded 50 sheep total!', icon: '💯', category: StickerCategory.Achievement, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'perfect_five', name: 'Perfect Five', description: '5 perfect herds (no sheep lost)!', icon: '⭐', category: StickerCategory.Achievement, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'speed_demon', name: 'Speed Demon', description: 'Completed a level in under 30 seconds!', icon: '⚡', category: StickerCategory.Achievement, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'frontier_explorer', name: 'Frontier Explorer', description: 'Reached the AI frontier!', icon: '🌌', category: StickerCategory.Achievement, rarity: StickerRarity.Rare, unlocked: false },

  // --- Concept Stickers ---
  { id: 'sticker_io', name: 'Input/Output', description: 'Learned about inputs and outputs!', icon: '⇄', category: StickerCategory.Concept, rarity: StickerRarity.Common, unlocked: false },
  { id: 'sticker_patterns', name: 'Pattern Finder', description: 'Discovered how AI finds patterns!', icon: '🔍', category: StickerCategory.Concept, rarity: StickerRarity.Common, unlocked: false },
  { id: 'sticker_noise', name: 'Noise Handler', description: 'Learned about noisy data!', icon: '📡', category: StickerCategory.Concept, rarity: StickerRarity.Common, unlocked: false },
  { id: 'sticker_emergence', name: 'Emergence!', description: 'Witnessed emergence in action!', icon: '🌀', category: StickerCategory.Concept, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_local', name: 'Local Thinker', description: 'Experienced local information processing!', icon: '👥', category: StickerCategory.Concept, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_ensemble', name: 'Team Player', description: 'Learned about ensemble methods!', icon: '🤝', category: StickerCategory.Concept, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_training', name: 'Trainer!', description: 'Experienced the training loop!', icon: '🔄', category: StickerCategory.Concept, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_distill', name: 'Knowledge Keeper', description: 'Learned knowledge distillation!', icon: '📚', category: StickerCategory.Concept, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_adapt', name: 'Adapt-A-Pup', description: 'Mastered adaptation!', icon: '🦎', category: StickerCategory.Concept, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_neural', name: 'Neural Navigator', description: 'Explored the neural meadow!', icon: '🧠', category: StickerCategory.Concept, rarity: StickerRarity.Legendary, unlocked: false },

  // --- Weather Stickers ---
  { id: 'sticker_clear_day', name: 'Clear Day', description: 'Herded on a perfect clear day!', icon: '☀', category: StickerCategory.Weather, rarity: StickerRarity.Common, unlocked: false },
  { id: 'sticker_rain_storm', name: 'Storm Rider', description: 'Herded through a rainstorm!', icon: '⛈', category: StickerCategory.Weather, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_snow_day', name: 'Snow Day', description: 'Herded in falling snow!', icon: '🌨', category: StickerCategory.Weather, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_golden_hour', name: 'Golden Hour', description: 'Herded in beautiful golden light!', icon: '🌅', category: StickerCategory.Weather, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_starry_night', name: 'Night Shepherd', description: 'Herded under the stars!', icon: '🌙', category: StickerCategory.Weather, rarity: StickerRarity.Legendary, unlocked: false },

  // --- Secret Stickers ---
  { id: 'sticker_hidden_pattern', name: 'Hidden Pattern', description: 'Found a secret pattern in the meadow...', icon: '🔮', category: StickerCategory.Secret, rarity: StickerRarity.Legendary, unlocked: false },
  { id: 'sticker_barks_secret', name: 'Bark\'s Secret', description: 'Discovered Elder Bark\'s hidden story!', icon: '📖', category: StickerCategory.Secret, rarity: StickerRarity.Legendary, unlocked: false },
  { id: 'sticker_all_breeds', name: 'Master Breeder', description: 'Cataloged all 12 sheep breeds!', icon: '🏆', category: StickerCategory.Secret, rarity: StickerRarity.Legendary, unlocked: false },
  { id: 'sticker_all_concepts', name: 'AI Scholar', description: 'Discovered every AI concept!', icon: '🎓', category: StickerCategory.Secret, rarity: StickerRarity.Legendary, unlocked: false },

  // --- Milestone Stickers ---
  { id: 'sticker_level_3', name: 'Triple Star', description: 'Got 3 stars on any level!', icon: '🌟', category: StickerCategory.Milestone, rarity: StickerRarity.Uncommon, unlocked: false },
  { id: 'sticker_all_apprentice', name: 'Graduate Puppy', description: '3-starred all Apprentice levels!', icon: '📜', category: StickerCategory.Milestone, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_all_journeyman', name: 'Journey\'s End', description: '3-starred all Journeyman levels!', icon: '🗺', category: StickerCategory.Milestone, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_daily_7', name: 'Week Warrior', description: '7-day daily challenge streak!', icon: '📅', category: StickerCategory.Milestone, rarity: StickerRarity.Rare, unlocked: false },
  { id: 'sticker_daily_30', name: 'Monthly Master', description: '30-day daily challenge streak!', icon: '🏅', category: StickerCategory.Milestone, rarity: StickerRarity.Legendary, unlocked: false },
  { id: 'sticker_diversity_master', name: 'Diversity Master', description: 'Herded all 12 breeds in one level!', icon: '🌈', category: StickerCategory.Milestone, rarity: StickerRarity.Rare, unlocked: false },
];

export const ALL_DISCOVERIES: Record<string, { name: string; description: string; type: CollectibleType; icon: string }> = {
  // AI Concepts discovered in levels
  what_is_ai: { name: 'What is AI?', description: 'A gentle introduction to artificial intelligence.', type: CollectibleType.ConceptPage, icon: '💡' },
  first_bark: { name: 'First Bark!', description: 'A sticker commemorating your very first bark.', type: CollectibleType.Sticker, icon: '📢' },
  flocking_rules: { name: 'Flocking Rules', description: 'The three rules: Separation, Alignment, Cohesion.', type: CollectibleType.ConceptPage, icon: '📋' },
  breed_merino: { name: 'Merino Sheep', description: 'Known for the finest, softest wool. Represents AI weights — the parameters that give each model its unique properties.', type: CollectibleType.SheepCatalog, icon: '🐑' },
  noise_in_data: { name: 'Noisy Data', description: 'When data is messy or corrupted, AI struggles — just like herding in rain!', type: CollectibleType.ConceptPage, icon: '📡' },
  breed_highland: { name: 'Highland Sheep', description: 'Tough and resilient, with impressive horns. Represents AI biases — the pre-existing tendencies that affect all decisions.', type: CollectibleType.SheepCatalog, icon: '🐑' },
  emergence_explained: { name: 'Emergence Explained', description: 'Complex behavior from simple rules. The magic of flocking AND neural networks!', type: CollectibleType.ConceptPage, icon: '🌀' },
  breed_suffolk: { name: 'Suffolk Sheep', description: 'Distinctive black face and legs. Represents activation functions — the on/off switches that let neural networks make decisions.', type: CollectibleType.SheepCatalog, icon: '🐑' },
  elder_bark_origin: { name: 'Elder Bark\'s Origin', description: 'A torn journal page: "...when I was a pup, the meadow stretched forever. But the Mist came, and with it, change..."', type: CollectibleType.LorePage, icon: '📖' },
  distributed_intelligence: { name: 'Distributed Intelligence', description: 'When no single unit has the full picture, but the group is smart anyway.', type: CollectibleType.ConceptPage, icon: '🕸' },
  breed_jacob: { name: 'Jacob Sheep', description: 'Multi-colored with distinctive spots. Represents multi-class classification — sorting things into many categories!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  ensemble_methods: { name: 'Ensemble Methods', description: 'Combining multiple AI models for better results. Like having a council of advisors!', type: CollectibleType.ConceptPage, icon: '🤝' },
  breed_soay: { name: 'Soay Sheep', description: 'One of the oldest breeds — survivors from ancient times. Represents evolutionary algorithms — AI that improves through selection!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  upgrade_barn: { name: 'Barn Upgrade', description: 'A blueprint for upgrading the farm barn. Unlocks the barn decoration!', type: CollectibleType.FarmUpgrade, icon: '🏠' },
  loss_function: { name: 'Loss Functions', description: 'How AI measures "how wrong" it is — and uses that to get better!', type: CollectibleType.ConceptPage, icon: '📉' },
  breed_valais: { name: 'Valais Blacknose', description: 'The cutest sheep — fluffy with a black face. Represents face recognition and CNNs!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  the_mist_secret: { name: 'The Mist\'s Secret', description: 'A faded page: "...the Mist isn\'t hiding the world. It\'s hiding what the world COULD be..."', type: CollectibleType.LorePage, icon: '📖' },
  teacher_student: { name: 'Teacher-Student Learning', description: 'How big AI models teach small ones to be almost as smart!', type: CollectibleType.ConceptPage, icon: '🎓' },
  breed_navajo: { name: 'Navajo Churro', description: 'Sacred to the Navajo people. Represents cultural knowledge and transfer learning — using what you know to learn faster!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  bark_apprentice_story: { name: 'Bark\'s Apprenticeship', description: '"My teacher was called Willow. She could herd a hundred sheep with three barks. I was not so talented... but I was persistent."', type: CollectibleType.LorePage, icon: '📖' },
  transfer_learning: { name: 'Transfer Learning', description: 'Using knowledge from one task to help with another. Like using herding skills in snow!', type: CollectibleType.ConceptPage, icon: '🔄' },
  breed_cheviot: { name: 'Cheviot Sheep', description: 'Hill breed — sure-footed on steep terrain. Represents gradient ascent — finding the path uphill to better solutions!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  breed_romanov: { name: 'Romanov Sheep', description: 'Russian breed that thrives in cold. Represents the "cold start" problem — when AI has no prior data!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  upgrade_hot_spring: { name: 'Hot Spring', description: 'A natural hot spring blueprint. Sheep (and puppies) can warm up here!', type: CollectibleType.FarmUpgrade, icon: '♨' },
  deep_learning: { name: 'Deep Learning', description: 'Stacking many layers of neurons to learn increasingly complex patterns!', type: CollectibleType.ConceptPage, icon: '🧠' },
  backpropagation: { name: 'Backpropagation', description: 'How neural networks learn: send a signal forward, measure the error, then propagate corrections backward!', type: CollectibleType.ConceptPage, icon: '↩' },
  breed_katahdin: { name: 'Katahdin Sheep', description: 'Hair sheep that don\'t need shearing. Represents lossless compression — keeping what matters, discarding what doesn\'t!', type: CollectibleType.SheepCatalog, icon: '🐑' },
  bark_final_teaching: { name: 'Bark\'s Final Teaching', description: '"The secret isn\'t in the barking, young one. It\'s in the listening. Watch the flock, and they\'ll tell you what they need."', type: CollectibleType.LorePage, icon: '📖' },
  hidden_neural_pattern: { name: 'Hidden Neural Pattern', description: 'A strange pattern in the meadow that looks like... a neural network? SECRET discovery!', type: CollectibleType.Secret, icon: '🔮' },
  ai_ethics: { name: 'AI Ethics', description: 'With great power comes great responsibility. Who decides what AI should and shouldn\'t do?', type: CollectibleType.ConceptPage, icon: '⚖' },
  agi_definition: { name: 'What is AGI?', description: 'Artificial General Intelligence — AI that can do ANY intellectual task a human can. We\'re not there... yet.', type: CollectibleType.ConceptPage, icon: '🌟' },
  bark_final_secret: { name: 'Bark\'s True Secret', description: '"I wasn\'t always an elder. Once, I was a lost puppy in the Mist. But I found my way by watching the sheep. They taught me everything."', type: CollectibleType.LorePage, icon: '📖' },
  mist_origin: { name: 'Origin of the Mist', description: 'The deepest secret: "The Mist is the space between what we know and what we could discover. It\'s not an obstacle — it\'s an invitation."', type: CollectibleType.Secret, icon: '🌫' },
};

export const ALL_FARM_UPGRADES: FarmUpgrade[] = [
  { id: 'upgrade_barn', name: 'Cozy Barn', description: 'A warm barn for the sheep to rest.', icon: '🏠', cost: 3, unlocked: false, position: { x: 3, y: 5 } },
  { id: 'upgrade_hot_spring', name: 'Hot Spring', description: 'A natural hot spring on the farm!', icon: '♨', cost: 5, unlocked: false, position: { x: 7, y: 3 } },
  { id: 'upgrade_garden', name: 'Flower Garden', description: 'Beautiful flowers that attract butterflies.', icon: '🌸', cost: 2, unlocked: false, position: { x: 5, y: 7 } },
  { id: 'upgrade_windmill', name: 'Windmill', description: 'An old windmill that creaks in the breeze.', icon: '🌀', cost: 4, unlocked: false, position: { x: 9, y: 2 } },
  { id: 'upgrade_pond', name: 'Duck Pond', description: 'A peaceful pond with ducks!', icon: '🦆', cost: 3, unlocked: false, position: { x: 2, y: 8 } },
  { id: 'upgrade_treehouse', name: 'Treehouse', description: 'A lookout treehouse with a great view!', icon: '🌳', cost: 6, unlocked: false, position: { x: 10, y: 6 } },
  { id: 'upgrade_scarecrow', name: 'Friendly Scarecrow', description: 'Not scary at all — just friendly!', icon: '🧑‍🌾', cost: 2, unlocked: false, position: { x: 6, y: 9 } },
  { id: 'upgrade_bench', name: 'Contemplation Bench', description: 'Sit and think about AI concepts...', icon: '🪑', cost: 1, unlocked: false, position: { x: 4, y: 4 } },
];

export const BREED_INFO: Record<SheepBreed, { name: string; description: string; aiConcept: string; icon: string; color: string }> = {
  [SheepBreed.Wooly]: { name: 'Wooly', description: 'The classic fluffy white sheep. Gentle and predictable.', aiConcept: 'Data Points — the basic units of information.', icon: '🐑', color: '#F5F5F0' },
  [SheepBreed.Merino]: { name: 'Merino', description: 'Premium wool sheep. Their fleece represents model weights — the parameters that make each model unique.', aiConcept: 'Weights — the numbers that give a model its knowledge.', icon: '🐑', color: '#FFF8E7' },
  [SheepBreed.Highland]: { name: 'Highland', description: 'Tough Scottish sheep with impressive horns. They represent biases — built-in tendencies.', aiConcept: 'Biases — the starting assumptions that shape all outputs.', icon: '🐑', color: '#A0522D' },
  [SheepBreed.Suffolk]: { name: 'Suffolk', description: 'Black-faced sheep known for meat production. They represent activation functions.', aiConcept: 'Activation Functions — the on/off switches in neural networks.', icon: '🐑', color: '#2D2D2D' },
  [SheepBreed.Dorper]: { name: 'Dorper', description: 'Hair sheep that don\'t need shearing. They represent regularization — simplifying models.', aiConcept: 'Regularization — preventing models from memorizing instead of learning.', icon: '🐑', color: '#D2B48C' },
  [SheepBreed.Jacob]: { name: 'Jacob', description: 'Multi-colored spotted sheep. They represent multi-class classification!', aiConcept: 'Multi-class Classification — sorting into many categories.', icon: '🐑', color: '#F5F5F0' },
  [SheepBreed.Soay]: { name: 'Soay', description: 'Ancient breed from Scotland. Represents evolutionary algorithms.', aiConcept: 'Evolutionary Algorithms — AI that improves through selection and mutation.', icon: '🐑', color: '#8B7355' },
  [SheepBreed.Valais]: { name: 'Valais Blacknose', description: 'The world\'s cutest sheep! Represents CNNs and face recognition.', aiConcept: 'Convolutional Neural Networks — AI that sees and recognizes patterns.', icon: '🐑', color: '#2D2D2D' },
  [SheepBreed.Navajo]: { name: 'Navajo Churro', description: 'Sacred to the Navajo people. Represents transfer learning.', aiConcept: 'Transfer Learning — using knowledge from one task to help with another.', icon: '🐑', color: '#DEB887' },
  [SheepBreed.Katahdin]: { name: 'Katahdin', description: 'Smooth hair sheep. Represents lossless compression in AI.', aiConcept: 'Compression — keeping what matters, discarding what doesn\'t.', icon: '🐑', color: '#FAEBD7' },
  [SheepBreed.Cheviot]: { name: 'Cheviot', description: 'Sure-footed hill breed. Represents gradient-based optimization.', aiConcept: 'Gradient Descent — finding the path to better solutions step by step.', icon: '🐑', color: '#FFF5EE' },
  [SheepBreed.Romanov]: { name: 'Romanov', description: 'Russian cold-weather breed. Represents the cold start problem in AI.', aiConcept: 'Cold Start — when AI has no prior data to work with.', icon: '🐑', color: '#696969' },
};

export function getCollectionProgress(stickers: Record<string, boolean>, discoveries: Record<string, boolean>, sheepCatalog: Record<string, boolean>): {
  stickers: { found: number; total: number };
  discoveries: { found: number; total: number };
  breeds: { found: number; total: number };
} {
  return {
    stickers: { found: Object.values(stickers).filter(Boolean).length, total: ALL_STICKERS.length },
    discoveries: { found: Object.values(discoveries).filter(Boolean).length, total: Object.keys(ALL_DISCOVERIES).length },
    breeds: { found: Object.values(sheepCatalog).filter(Boolean).length, total: Object.keys(BREED_INFO).length },
  };
}
