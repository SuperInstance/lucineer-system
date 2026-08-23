// ============================================================// MIST — Level Definitions with Spiral Curriculum// Each AI concept revisited deeper across ranks// ============================================================

import { LevelDef, Rank, SheepBreed, Weather, ObstacleType, CollectibleType } from './types';

export const LEVELS: LevelDef[] = [
  // ========================================
  // APPRENTICE RANK — "Learning the Basics"
  // AI Concept Depth 1: Intuition
  // ========================================
  {
    id: 'app-1',
    rank: Rank.Apprentice,
    index: 1,
    name: 'First Morning',
    subtitle: 'The sheep need to find the pen',
    description: 'Elder Bark shows you the basics of herding. Just get the sheep into the pen!',
    gridSize: { x: 14, y: 10 },
    aiConcept: {
      key: 'input_output',
      name: 'Input → Output',
      shortName: 'Input/Output',
      rank: Rank.Apprentice,
      depth: 1,
      metaphor: 'You give directions (input), sheep move (output). Simple!',
      realExplanation: 'Every AI system takes inputs and produces outputs. Your bark is like data going into a model, and the sheep movement is the prediction coming out.',
      parentExplanation: 'Your child is learning the most fundamental AI concept: inputs and outputs. By barking (inputting a signal), they see the sheep react (output). This mirrors how any AI model receives data and produces a response.',
      keywords: ['input', 'output', 'signal', 'response'],
      relatedConcepts: ['data', 'prediction', 'model'],
    },
    objective: { type: 'herd_all', description: 'Guide all 4 sheep into the pen' },
    constraints: {},
    terrainSeed: 1001,
    sheepCount: 4,
    sheepBreeds: [SheepBreed.Wooly],
    obstacles: [],
    weather: Weather.Clear,
    dialogIntro: {
      id: 'app-1-intro',
      speaker: 'elder_bark',
      text: 'Welcome, little one! I am Elder Bark. Today you\'ll learn the first secret of shepherding: your bark is a signal. When you bark near the sheep, they move! Try guiding them into the pen — that fenced area down there.',
      emotion: 'wise',
      choices: [
        { text: 'I\'ll try my best!', nextId: 'app-1-intro-2' },
        { text: 'What if they don\'t listen?', nextId: 'app-1-intro-alt' },
      ],
    },
    dialogOutro: {
      id: 'app-1-outro',
      speaker: 'elder_bark',
      text: 'Wonderful! You see? Your bark (input) made the sheep move (output). This is the heart of how all thinking machines work — they take in signals and produce responses. Every AI, from voice assistants to self-driving cars, follows this same pattern!',
      emotion: 'proud',
      unlockConcept: 'input_output',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'what_is_ai', posHint: 'corner' },
      { type: CollectibleType.Sticker, conceptKey: 'first_bark', posHint: 'near_sheep' },
    ],
    parentLayerContent: {
      title: 'Input → Output',
      conceptName: 'Fundamentals of AI',
      whatHappened: 'Your child used barks (inputs) to guide sheep (outputs) into the pen.',
      aiConnection: 'This is the basic model of every AI system: data goes in, predictions come out. Think of it like asking a question and getting an answer.',
      tryAtHome: 'Play "robot chef" — give your child simple instructions (inputs) and have them perform actions (outputs). Then swap roles!',
      ageAppropriate: 'Ages 5-8: Focus on the idea of cause and effect. Ages 9-12: Discuss how voice assistants work using this same principle.',
    },
    tutorialSteps: [
      { id: 't1', text: 'Use arrow keys or WASD to move your puppy!', highlight: 'move', waitFor: 'move' },
      { id: 't2', text: 'Get close to the sheep and press SPACE to bark!', highlight: 'bark', waitFor: 'bark' },
      { id: 't3', text: 'Guide the sheep toward the pen (the fenced area)', highlight: 'pen', waitFor: 'pen_reached' },
    ],
  },
  {
    id: 'app-2',
    rank: Rank.Apprentice,
    index: 2,
    name: 'Flock Together',
    subtitle: 'Sheep prefer to stay together',
    description: 'The sheep follow each other! Use their natural tendency to stay close to move them as a group.',
    gridSize: { x: 16, y: 11 },
    aiConcept: {
      key: 'patterns',
      name: 'Patterns in Data',
      shortName: 'Patterns',
      rank: Rank.Apprentice,
      depth: 1,
      metaphor: 'Sheep naturally group together — they follow patterns! AI finds patterns in data the same way.',
      realExplanation: 'Machine learning is really about finding patterns. Just as sheep naturally cluster together, AI looks for groupings and trends in data that humans might miss.',
      parentExplanation: 'Your child discovered that sheep stick together in groups — this is a pattern! AI systems do the same thing: they look for patterns in data to make predictions.',
      keywords: ['pattern', 'grouping', 'clustering', 'trend'],
      relatedConcepts: ['input_output', 'training'],
    },
    objective: { type: 'herd_all', description: 'Herd 6 sheep as a group — keep them close together!' },
    constraints: { maxBarks: 20 },
    terrainSeed: 1002,
    sheepCount: 6,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino],
    obstacles: [
      { type: ObstacleType.Haybale, pos: { x: 8, y: 5 } },
    ],
    weather: Weather.Clear,
    dialogIntro: {
      id: 'app-2-intro',
      speaker: 'elder_bark',
      text: 'Notice how the sheep stick together? They follow simple rules: stay close to your neighbors, don\'t bump into each other, and go where the group goes. This is called FLOCKING — and it\'s a lot like how AI finds patterns!',
      emotion: 'wise',
      choices: [
        { text: 'Tell me more about flocking!', nextId: 'app-2-intro-flock' },
        { text: 'Let me try herding them!', nextId: 'app-2-intro-go' },
      ],
    },
    dialogOutro: {
      id: 'app-2-outro',
      speaker: 'elder_bark',
      text: 'You kept the flock together beautifully! That\'s exactly what AI does with data — it finds the natural groupings and patterns. When you see sheep clustering, think of AI clustering similar pictures or words together!',
      emotion: 'proud',
      unlockConcept: 'patterns',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'flocking_rules', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_merino', posHint: 'behind_obstacle' },
    ],
    parentLayerContent: {
      title: 'Finding Patterns',
      conceptName: 'Pattern Recognition',
      whatHappened: 'Your child herded sheep by using their natural tendency to flock together — a pattern of behavior.',
      aiConnection: 'AI excels at finding patterns in data. Just as sheep naturally group together, AI groups similar images, words, or behaviors to make predictions.',
      tryAtHome: 'Sort a mixed bowl of fruit with your child. Ask: "What patterns do you see?" This is exactly what AI does with data!',
      ageAppropriate: 'Ages 5-8: Focus on grouping and sorting. Ages 9-12: Discuss how Netflix recommends shows by finding viewing patterns.',
    },
  },
  {
    id: 'app-3',
    rank: Rank.Apprentice,
    index: 3,
    name: 'Rainy Day Herding',
    subtitle: 'Weather changes everything',
    description: 'A storm is coming! The sheep are nervous in the rain. Keep them calm and herd them quickly!',
    gridSize: { x: 16, y: 11 },
    aiConcept: {
      key: 'noise',
      name: 'Noise in Data',
      shortName: 'Noise',
      rank: Rank.Apprentice,
      depth: 1,
      metaphor: 'Rain makes sheep behave unpredictably — just like noise in data makes AI less accurate!',
      realExplanation: 'Real-world data is messy, like rain. "Noise" means errors, confusion, or randomness in data that makes AI predictions less reliable. Good AI learns to handle noise.',
      parentExplanation: 'The rain represents "noise" in AI — messy, unpredictable data. Your child experienced how harder conditions make tasks more difficult, just like noisy data makes AI less accurate.',
      keywords: ['noise', 'accuracy', 'robustness', 'cleaning'],
      relatedConcepts: ['patterns', 'training'],
    },
    objective: { type: 'timed_herd', description: 'Herd all sheep before the storm gets worse!', timeLimit: 90 },
    constraints: { maxBarks: 15 },
    terrainSeed: 1003,
    sheepCount: 5,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Highland],
    obstacles: [
      { type: ObstacleType.Log, pos: { x: 7, y: 4 } },
      { type: ObstacleType.Log, pos: { x: 9, y: 7 } },
    ],
    weather: Weather.Rainy,
    dialogIntro: {
      id: 'app-3-intro',
      speaker: 'elder_bark',
      text: 'Oh dear, a storm is rolling in! The rain makes the ground slippery and the sheep nervous. In AI, we call this NOISE — unexpected things that make predictions harder. You\'ll need to work fast!',
      emotion: 'concerned',
    },
    dialogOutro: {
      id: 'app-3-outro',
      speaker: 'elder_bark',
      text: 'You did great despite the rain! In AI, noise is anything that messes up the data — like a smudged photo or a fuzzy voice recording. The best AI systems, like the best shepherds, learn to work through the noise!',
      emotion: 'proud',
      unlockConcept: 'noise',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'noise_in_data', posHint: 'corner' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_highland', posHint: 'behind_obstacle' },
      { type: CollectibleType.Sticker, conceptKey: 'rain_herder', posHint: 'center' },
    ],
    parentLayerContent: {
      title: 'Handling Noise',
      conceptName: 'Data Quality',
      whatHappened: 'Rain made herding harder — the sheep moved unpredictably, just like noisy data confuses AI.',
      aiConnection: 'Noise in data (errors, missing values, fuzzy inputs) is a major challenge in AI. Robust AI systems are trained to handle imperfect data.',
      tryAtHome: 'Try giving instructions to your child while music is playing loudly. Discuss how "noise" makes communication harder — just like it makes AI harder!',
      ageAppropriate: 'Ages 5-8: Focus on how hard things are when conditions aren\'t perfect. Ages 9-12: Discuss data cleaning and why AI needs good data.',
    },
  },

  // ========================================
  // JOURNEYMAN RANK — "Understanding Rules"
  // AI Concept Depth 2: Mechanisms
  // ========================================
  {
    id: 'jrn-1',
    rank: Rank.Journeyman,
    index: 1,
    name: 'Three Simple Rules',
    subtitle: 'The secret behind flocking',
    description: 'Elder Bark reveals the three rules that make flocks work: Separation, Alignment, and Cohesion.',
    gridSize: { x: 18, y: 12 },
    aiConcept: {
      key: 'rules',
      name: 'Simple Rules → Complex Behavior',
      shortName: 'Emergence',
      rank: Rank.Journeyman,
      depth: 2,
      metaphor: 'Each sheep follows just 3 rules, but together they create beautiful flocking patterns. This is called EMERGENCE!',
      realExplanation: 'Emergence is when simple rules create complex behavior. The Boids algorithm uses just 3 rules (separation, alignment, cohesion) to create realistic flocking. Neural networks work similarly — simple neurons create complex intelligence.',
      parentExplanation: 'Your child learned about EMERGENCE: complex patterns arising from simple rules. This is a profound concept in AI and nature. Each sheep follows 3 simple rules, but the flock as a whole appears to have intelligence!',
      keywords: ['emergence', 'boids', 'rules', 'complexity', 'simple'],
      relatedConcepts: ['patterns', 'neural_networks', 'training'],
    },
    objective: { type: 'herd_all', description: 'Herd 8 sheep using their flocking rules to your advantage' },
    constraints: { maxBarks: 18 },
    terrainSeed: 2001,
    sheepCount: 8,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Suffolk, SheepBreed.Dorper],
    obstacles: [
      { type: ObstacleType.Haybale, pos: { x: 8, y: 4 } },
      { type: ObstacleType.Haybale, pos: { x: 10, y: 8 } },
      { type: ObstacleType.Boulder, pos: { x: 5, y: 6 } },
    ],
    weather: Weather.Clear,
    dialogIntro: {
      id: 'jrn-1-intro',
      speaker: 'elder_bark',
      text: 'Ready for a big secret? Each sheep only follows THREE rules: 1) Don\'t crowd your neighbors (Separation), 2) Go the same direction as nearby sheep (Alignment), and 3) Move toward the center of your group (Cohesion). That\'s it! Yet look at the beautiful patterns they create together. This magic is called EMERGENCE!',
      emotion: 'wise',
      choices: [
        { text: 'That\'s amazing! Three rules?', nextId: 'jrn-1-intro-explain' },
        { text: 'Can I change these rules?', nextId: 'jrn-1-intro-sandbox' },
      ],
    },
    dialogOutro: {
      id: 'jrn-1-outro',
      speaker: 'elder_bark',
      text: 'You worked WITH the flock\'s rules instead of against them! In AI, emergence means simple building blocks (like neurons) create complex intelligence. A single neuron is simple — billions of them create minds!',
      emotion: 'proud',
      unlockConcept: 'rules',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'emergence_explained', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_suffolk', posHint: 'corner' },
      { type: CollectibleType.LorePage, conceptKey: 'elder_bark_origin', posHint: 'behind_obstacle' },
    ],
    parentLayerContent: {
      title: 'Emergence',
      conceptName: 'Simple Rules, Complex Behavior',
      whatHappened: 'Your child learned the three flocking rules and used them to herd sheep more effectively.',
      aiConnection: 'Emergence is a cornerstone of AI. Neural networks use billions of simple neurons following basic rules to create complex intelligence. Each neuron alone is trivial — together, they\'re remarkable.',
      tryAtHome: 'Try the "boids game" — have 3+ family members each follow one rule (stay apart, match direction, move to center) and walk around. Watch the flocking emerge!',
      ageAppropriate: 'Ages 5-8: Focus on the three rules and how they work together. Ages 9-12: Discuss neurons and how brains use emergence. Ages 13+: Explore cellular automata and Conway\'s Game of Life.',
    },
  },
  {
    id: 'jrn-2',
    rank: Rank.Journeyman,
    index: 2,
    name: 'Through the Fog',
    subtitle: 'Herding blind',
    description: 'Thick fog limits your vision! You can\'t see far, but the sheep can still sense each other. Trust the flock.',
    gridSize: { x: 18, y: 12 },
    aiConcept: {
      key: 'local_information',
      name: 'Local Information',
      shortName: 'Local Info',
      rank: Rank.Journeyman,
      depth: 2,
      metaphor: 'In fog, each sheep can only see nearby friends. They use LOCAL information — no sheep sees the whole picture!',
      realExplanation: 'Many AI systems (especially neural networks) only have local information — each neuron only connects to nearby neurons. Yet the whole network can solve complex problems. This is distributed intelligence.',
      parentExplanation: 'Your child experienced LOCAL INFORMATION — making decisions with limited visibility. This is how most AI works: no single part sees the whole picture, but together they figure it out.',
      keywords: ['local', 'distributed', 'neighbors', 'limited_view', 'swarm'],
      relatedConcepts: ['rules', 'neural_networks', 'training'],
    },
    objective: { type: 'herd_all', description: 'Herd all sheep through the fog!' },
    constraints: { fogRadius: 3, maxBarks: 25 },
    terrainSeed: 2002,
    sheepCount: 7,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob],
    obstacles: [
      { type: ObstacleType.Thornbush, pos: { x: 6, y: 5 } },
      { type: ObstacleType.Thornbush, pos: { x: 12, y: 7 } },
      { type: ObstacleType.Log, pos: { x: 9, y: 3 } },
    ],
    weather: Weather.Foggy,
    unlockRequirement: { rank: Rank.Apprentice, index: 3, stars: 2 },
    dialogIntro: {
      id: 'jrn-2-intro',
      speaker: 'elder_bark',
      text: 'The fog is thick today. You can barely see! But here\'s the thing — sheep don\'t need to see the whole field. Each sheep only looks at its nearest neighbors and follows the three rules. They use LOCAL INFORMATION. Amazing, isn\'t it?',
      emotion: 'mysterious',
    },
    dialogOutro: {
      id: 'jrn-2-outro',
      speaker: 'elder_bark',
      text: 'You trusted the flock even when you couldn\'t see! In AI, each neuron only "sees" its neighbors — no single neuron knows the answer. But together, they solve problems no individual could. That\'s the power of local information!',
      emotion: 'proud',
      unlockConcept: 'local_information',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'distributed_intelligence', posHint: 'hidden_path' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_jacob', posHint: 'corner' },
      { type: CollectibleType.Sticker, conceptKey: 'fog_navigator', posHint: 'behind_obstacle' },
    ],
    parentLayerContent: {
      title: 'Local Information',
      conceptName: 'Distributed Intelligence',
      whatHappened: 'Your child herded sheep in fog, experiencing how local information (seeing only neighbors) can still produce good group decisions.',
      aiConnection: 'Most AI systems use local information. Each neuron in a neural network only connects to its neighbors, yet the network can recognize faces, translate languages, and play chess.',
      tryAtHome: 'Play "telephone" — each person only hears from their neighbor. The final message shows how local information transforms as it travels through a network!',
      ageAppropriate: 'Ages 5-8: Focus on "each sheep only sees nearby friends." Ages 9-12: Discuss how neurons connect locally. Ages 13+: Explore convolutional neural networks and receptive fields.',
    },
  },
  {
    id: 'jrn-3',
    rank: Rank.Journeyman,
    index: 3,
    name: 'All Different, All Together',
    subtitle: 'Every sheep is unique',
    description: 'Different breeds and personalities! Some follow, some wander, some lead. Learn to work with diversity.',
    gridSize: { x: 18, y: 13 },
    aiConcept: {
      key: 'diversity',
      name: 'Diversity in Models',
      shortName: 'Diversity',
      rank: Rank.Journeyman,
      depth: 2,
      metaphor: 'Different sheep personalities are like different AI models — each has strengths and weaknesses. Together, they\'re stronger!',
      realExplanation: 'Ensemble methods in AI combine multiple different models to get better predictions than any single model. Each model has different strengths, just like different sheep breeds have different traits.',
      parentExplanation: 'Your child discovered that diverse sheep (different breeds/personalities) create a more interesting challenge. In AI, combining different models ("ensembles") often outperforms any single model!',
      keywords: ['ensemble', 'diversity', 'models', 'combination', 'voting'],
      relatedConcepts: ['local_information', 'training', 'generations'],
    },
    objective: { type: 'herd_all', description: 'Herd all 10 different sheep — each type needs a different approach!' },
    constraints: { maxBarks: 22 },
    terrainSeed: 2003,
    sheepCount: 10,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Highland, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob, SheepBreed.Soay],
    obstacles: [
      { type: ObstacleType.Haybale, pos: { x: 7, y: 5 } },
      { type: ObstacleType.Boulder, pos: { x: 13, y: 4 } },
      { type: ObstacleType.CrumblingWall, pos: { x: 10, y: 8 } },
    ],
    weather: Weather.Cloudy,
    unlockRequirement: { rank: Rank.Journeyman, index: 1, stars: 2 },
    dialogIntro: {
      id: 'jrn-3-intro',
      speaker: 'elder_bark',
      text: 'Today\'s flock is special — look at all the different breeds! Wooly sheep are docile, Suffolk sheep are stubborn, Jacob sheep are curious... In AI, we call this DIVERSITY. Different models have different strengths. Together, they\'re much stronger than alone!',
      emotion: 'playful',
    },
    dialogOutro: {
      id: 'jrn-3-outro',
      speaker: 'elder_bark',
      text: 'You adapted to every sheep\'s personality! In AI, ENSEMBLE methods work the same way — they combine many different models. It\'s like asking 10 experts instead of 1. The group is smarter than any individual!',
      emotion: 'proud',
      unlockConcept: 'diversity',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'ensemble_methods', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_soay', posHint: 'behind_obstacle' },
      { type: CollectibleType.FarmUpgrade, conceptKey: 'upgrade_barn', posHint: 'corner' },
      { type: CollectibleType.Sticker, conceptKey: 'diversity_master', posHint: 'near_sheep' },
    ],
    parentLayerContent: {
      title: 'Diversity & Ensembles',
      conceptName: 'Combining Multiple Models',
      whatHappened: 'Your child herded sheep with different personalities, learning that each type needs a different approach.',
      aiConnection: 'Ensemble AI methods combine multiple models (like Random Forests) to make better predictions. Each model has blind spots, but together they cover each other\'s weaknesses.',
      tryAtHome: 'Have each family member guess how many jellybeans are in a jar. Average all guesses — the group answer is usually more accurate than any individual! This is the "wisdom of crowds" principle behind ensembles.',
      ageAppropriate: 'Ages 5-8: Focus on different sheep needing different approaches. Ages 9-12: Discuss how asking multiple people gives better answers. Ages 13+: Explore Random Forests and model ensembles.',
    },
  },

  // ========================================
  // MASTER RANK — "Training & Optimization"
  // AI Concept Depth 3: Theory
  // ========================================
  {
    id: 'mst-1',
    rank: Rank.Master,
    index: 1,
    name: 'The Training Ground',
    subtitle: 'Practice makes perfect',
    description: 'A complex course with many obstacles. Your skills improve each time you try — just like AI training!',
    gridSize: { x: 20, y: 14 },
    aiConcept: {
      key: 'training',
      name: 'Training a Model',
      shortName: 'Training',
      rank: Rank.Master,
      depth: 3,
      metaphor: 'Each time you herd, you get a little better. AI "trains" the same way — trying, seeing what went wrong, and adjusting!',
      realExplanation: 'AI training is an optimization loop: make a prediction, compare to the correct answer (loss), calculate the gradient (direction of improvement), and adjust weights. Repeat thousands of times. Just like practice makes perfect for shepherding!',
      parentExplanation: 'Your child experienced the training loop firsthand: try, observe results, adjust strategy, try again. This is EXACTLY how AI models learn — through iterative practice with feedback.',
      keywords: ['training', 'optimization', 'loss', 'gradient', 'iteration', 'practice'],
      relatedConcepts: ['rules', 'generations', 'feedback'],
    },
    objective: { type: 'timed_herd', description: 'Herd all sheep fast — try to beat your best time!', timeLimit: 120 },
    constraints: { maxBarks: 20 },
    terrainSeed: 3001,
    sheepCount: 10,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Highland, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob, SheepBreed.Soay, SheepBreed.Valais],
    obstacles: [
      { type: ObstacleType.Boulder, pos: { x: 6, y: 4 } },
      { type: ObstacleType.Log, pos: { x: 10, y: 6 } },
      { type: ObstacleType.Thornbush, pos: { x: 14, y: 5 } },
      { type: ObstacleType.CrumblingWall, pos: { x: 8, y: 9 } },
    ],
    weather: Weather.Windy,
    unlockRequirement: { rank: Rank.Journeyman, index: 3, stars: 2 },
    dialogIntro: {
      id: 'mst-1-intro',
      speaker: 'elder_bark',
      text: 'Welcome to the Training Ground! Here, repetition is key. Each time you try this course, you\'ll get a little faster and smarter. That\'s exactly how AI TRAINING works — the model tries many times, learns from mistakes, and gradually improves. Your stars are like the AI\'s loss function — getting closer to perfect!',
      emotion: 'encouraging',
    },
    dialogOutro: {
      id: 'mst-1-outro',
      speaker: 'elder_bark',
      text: 'Did you notice yourself getting better? In AI, training means running the same task thousands of times. Each time, the model adjusts its internal "weights" (like your strategy) to reduce "loss" (like your mistakes). Your improvement IS machine learning in action!',
      emotion: 'proud',
      unlockConcept: 'training',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'loss_function', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_valais', posHint: 'corner' },
      { type: CollectibleType.LorePage, conceptKey: 'the_mist_secret', posHint: 'behind_obstacle' },
      { type: CollectibleType.Sticker, conceptKey: 'training_grounds', posHint: 'near_sheep' },
    ],
    parentLayerContent: {
      title: 'AI Training',
      conceptName: 'The Training Loop',
      whatHappened: 'Your child practiced herding multiple times, improving with each attempt — experiencing the training loop.',
      aiConnection: 'AI training works exactly like this: predict → measure error (loss) → adjust → repeat. The model gets better over time, just like your child got better at herding.',
      tryAtHome: 'Have your child practice throwing bean bags into a bucket. Track attempts and improvement. Explain: "An AI does this millions of times to learn!"',
      ageAppropriate: 'Ages 5-8: Focus on practice and improvement. Ages 9-12: Introduce the concept of "loss" as a score of how wrong the AI is. Ages 13+: Discuss gradient descent and learning rates.',
    },
  },
  {
    id: 'mst-2',
    rank: Rank.Master,
    index: 2,
    name: 'Generation Gap',
    subtitle: 'Knowledge passed down',
    description: 'Elder Bark teaches you a technique, and now you must teach a younger pup. Knowledge flows through generations!',
    gridSize: { x: 20, y: 14 },
    aiConcept: {
      key: 'knowledge_distillation',
      name: 'Knowledge Distillation',
      shortName: 'Distillation',
      rank: Rank.Master,
      depth: 3,
      metaphor: 'Elder Bark (big model) teaches you, and you (smaller model) teach a younger pup. Each generation keeps the important knowledge!',
      realExplanation: 'Knowledge distillation is when a large, complex AI model (teacher) trains a smaller, simpler model (student) to reproduce its behavior. The student is faster and uses less memory but keeps most of the teacher\'s intelligence.',
      parentExplanation: 'Your child experienced KNOWLEDGE DISTILLATION: Elder Bark (the expert/teacher model) passed knowledge to your pup (the student model), who can now teach an even younger pup. This is how AI companies make small, fast models that are still smart!',
      keywords: ['distillation', 'teacher', 'student', 'compression', 'transfer', 'generations'],
      relatedConcepts: ['training', 'diversity', 'generations'],
    },
    objective: { type: 'herd_all', description: 'First herd perfectly, then guide the younger pup to repeat your path!' },
    constraints: { maxBarks: 25 },
    terrainSeed: 3002,
    sheepCount: 8,
    sheepBreeds: [SheepBreed.Merino, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob, SheepBreed.Valais, SheepBreed.Navajo],
    obstacles: [
      { type: ObstacleType.IceBlock, pos: { x: 8, y: 4 } },
      { type: ObstacleType.Boulder, pos: { x: 13, y: 7 } },
      { type: ObstacleType.CrumblingWall, pos: { x: 5, y: 9 } },
    ],
    weather: Weather.Golden,
    unlockRequirement: { rank: Rank.Master, index: 1, stars: 2 },
    dialogIntro: {
      id: 'mst-2-intro',
      speaker: 'elder_bark',
      text: 'Today I\'ll teach you something special: how to pass knowledge to the next generation. I\'m the ELDER model — big and wise but slow. You\'re the STUDENT model — smaller but faster. In AI, this is called KNOWLEDGE DISTILLATION. Watch my technique, then teach a younger pup!',
      emotion: 'wise',
    },
    dialogOutro: {
      id: 'mst-2-outro',
      speaker: 'elder_bark',
      text: 'You passed on what you learned! In AI, distillation lets us take a huge, slow model and teach a tiny, fast model to be almost as smart. Your phone\'s voice assistant? Probably a distilled model — small enough to run on your phone, smart enough to understand you!',
      emotion: 'proud',
      unlockConcept: 'knowledge_distillation',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'teacher_student', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_navajo', posHint: 'corner' },
      { type: CollectibleType.LorePage, conceptKey: 'bark_apprentice_story', posHint: 'behind_obstacle' },
    ],
    parentLayerContent: {
      title: 'Knowledge Distillation',
      conceptName: 'Teacher-Student Learning',
      whatHappened: 'Your child experienced knowledge being passed from Elder Bark (teacher) to pup (student) to a younger pup — a chain of learning.',
      aiConnection: 'Knowledge distillation is how we make AI small enough for phones. A huge model (like GPT) teaches a small model its patterns. The small model is 10x faster but keeps 90% of the intelligence!',
      tryAtHome: 'Play "telephone with teaching" — teach your child a skill (like a magic trick), then have them teach it to a friend. Discuss how knowledge can be compressed and transferred.',
      ageAppropriate: 'Ages 5-8: Focus on the teacher-student relationship. Ages 9-12: Discuss why smaller is sometimes better (speed, cost). Ages 13+: Explore model compression and quantization.',
    },
  },
  {
    id: 'mst-3',
    rank: Rank.Master,
    index: 3,
    name: 'Winter\'s Challenge',
    subtitle: 'Adapt or fail',
    description: 'Snow and ice change the rules. Sheep slide on ice, get tired in snow. Adapt your strategy to the environment!',
    gridSize: { x: 20, y: 14 },
    aiConcept: {
      key: 'adaptation',
      name: 'Model Adaptation',
      shortName: 'Adaptation',
      rank: Rank.Master,
      depth: 3,
      metaphor: 'When the environment changes (snow), your old strategies don\'t work. You must ADAPT. AI models face the same challenge when conditions change!',
      realExplanation: 'AI models trained on one environment often struggle in new conditions. "Domain adaptation" and "transfer learning" help models adapt to new situations without retraining from scratch.',
      parentExplanation: 'Your child had to change strategy when snow and ice appeared. In AI, this is called DOMAIN ADAPTATION — when the real world differs from training data, AI must adapt!',
      keywords: ['adaptation', 'transfer_learning', 'domain', 'generalization', 'robustness'],
      relatedConcepts: ['noise', 'training', 'generations'],
    },
    objective: { type: 'herd_all', description: 'Adapt your herding to the winter conditions!' },
    constraints: { maxBarks: 20, staminaDrain: 15 },
    terrainSeed: 3003,
    sheepCount: 9,
    sheepBreeds: [SheepBreed.Highland, SheepBreed.Soay, SheepBreed.Cheviot, SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Romanov],
    obstacles: [
      { type: ObstacleType.IceBlock, pos: { x: 7, y: 4 } },
      { type: ObstacleType.IceBlock, pos: { x: 12, y: 7 } },
      { type: ObstacleType.IceBlock, pos: { x: 9, y: 10 } },
      { type: ObstacleType.Boulder, pos: { x: 15, y: 5 } },
    ],
    weather: Weather.Snowy,
    unlockRequirement: { rank: Rank.Master, index: 2, stars: 2 },
    dialogIntro: {
      id: 'mst-3-intro',
      speaker: 'elder_bark',
      text: 'Brrr! Winter has come to the valley. The snow slows everyone down, and ice makes the sheep slide! Your usual strategies won\'t work here. In AI, we call this needing ADAPTATION — when the world changes, models must change too. Can you adapt?',
      emotion: 'concerned',
    },
    dialogOutro: {
      id: 'mst-3-outro',
      speaker: 'elder_bark',
      text: 'You adapted beautifully! AI models face the same challenge: they\'re trained in one environment but must work in many. TRANSFER LEARNING helps — using knowledge from one task to help with a new one. Just like you used your herding skills but adjusted for snow!',
      emotion: 'proud',
      unlockConcept: 'adaptation',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'transfer_learning', posHint: 'center' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_cheviot', posHint: 'corner' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_romanov', posHint: 'behind_obstacle' },
      { type: CollectibleType.Sticker, conceptKey: 'winter_herding', posHint: 'near_sheep' },
      { type: CollectibleType.FarmUpgrade, conceptKey: 'upgrade_hot_spring', posHint: 'hidden_path' },
    ],
    parentLayerContent: {
      title: 'Adaptation & Transfer Learning',
      conceptName: 'When Conditions Change',
      whatHappened: 'Your child\'s herding strategies had to change when snow and ice appeared — the same approach didn\'t work in new conditions.',
      aiConnection: 'AI models trained on summer data may fail in winter. Transfer learning and domain adaptation help AI adjust to new conditions, just like your child adapted their herding strategy.',
      tryAtHome: 'Have your child try a familiar game with new rules (e.g., soccer with a smaller ball). Discuss how the skills transfer but need adjustment.',
      ageAppropriate: 'Ages 5-8: Focus on changing strategies. Ages 9-12: Discuss why self-driving cars need to handle snow. Ages 13+: Explore fine-tuning and domain adaptation.',
    },
  },

  // ========================================
  // ELDER RANK — "Deep Understanding"
  // AI Concept Depth 4: Meta-Cognition
  // ========================================
  {
    id: 'eld-1',
    rank: Rank.Elder,
    index: 1,
    name: 'The Neural Meadow',
    subtitle: 'See the invisible network',
    description: 'The meadow itself is a neural network! Each tile is a neuron, connected to its neighbors. Watch signals propagate.',
    gridSize: { x: 22, y: 15 },
    aiConcept: {
      key: 'neural_networks',
      name: 'Neural Networks',
      shortName: 'Neural Nets',
      rank: Rank.Elder,
      depth: 4,
      metaphor: 'The meadow is like a neural network: each patch of grass is a neuron, paths are connections, and your bark sends signals through the network!',
      realExplanation: 'Neural networks are layers of interconnected nodes (neurons). Each neuron takes inputs, applies weights, and produces an output. Deep learning stacks many layers to extract increasingly abstract features — from edges to shapes to objects to scenes.',
      parentExplanation: 'Your child explored the ultimate AI concept: NEURAL NETWORKS. The meadow metaphor shows how individual simple units (neurons/tiles) connected together can process information and make decisions.',
      keywords: ['neural_network', 'layers', 'weights', 'activation', 'deep_learning', 'features'],
      relatedConcepts: ['rules', 'local_information', 'training', 'knowledge_distillation'],
    },
    objective: { type: 'herd_all', description: 'Herd sheep through the neural meadow — watch signals flow!' },
    constraints: { maxBarks: 30 },
    terrainSeed: 4001,
    sheepCount: 12,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Highland, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob, SheepBreed.Soay, SheepBreed.Valais, SheepBreed.Navajo, SheepBreed.Katahdin, SheepBreed.Cheviot, SheepBreed.Romanov],
    obstacles: [
      { type: ObstacleType.Boulder, pos: { x: 6, y: 4 } },
      { type: ObstacleType.Log, pos: { x: 11, y: 6 } },
      { type: ObstacleType.Thornbush, pos: { x: 16, y: 4 } },
      { type: ObstacleType.CrumblingWall, pos: { x: 8, y: 9 } },
      { type: ObstacleType.Haybale, pos: { x: 14, y: 10 } },
    ],
    weather: Weather.Clear,
    unlockRequirement: { rank: Rank.Master, index: 3, stars: 3 },
    dialogIntro: {
      id: 'eld-1-intro',
      speaker: 'elder_bark',
      text: 'You\'ve come so far, young elder. Now I\'ll show you the deepest secret. Look at this meadow — each patch of grass is like a NEURON. The paths between them are CONNECTIONS. When you bark, a signal ripples through the network, just like data flows through a neural network. This is DEEP LEARNING made visible!',
      emotion: 'mysterious',
    },
    dialogOutro: {
      id: 'eld-1-outro',
      speaker: 'elder_bark',
      text: 'You\'ve seen it with your own eyes — simple units connected together creating intelligence. That\'s all a neural network is! Billions of simple neurons, following simple rules, creating the most powerful AI systems in the world. From this meadow to GPT — it\'s the same principle!',
      emotion: 'proud',
      unlockConcept: 'neural_networks',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'deep_learning', posHint: 'center' },
      { type: CollectibleType.ConceptPage, conceptKey: 'backpropagation', posHint: 'hidden_path' },
      { type: CollectibleType.SheepCatalog, conceptKey: 'breed_katahdin', posHint: 'corner' },
      { type: CollectibleType.LorePage, conceptKey: 'bark_final_teaching', posHint: 'behind_obstacle' },
      { type: CollectibleType.Secret, conceptKey: 'hidden_neural_pattern', posHint: 'center' },
    ],
    parentLayerContent: {
      title: 'Neural Networks & Deep Learning',
      conceptName: 'The Architecture of AI',
      whatHappened: 'Your child experienced how a network of simple, connected units (like tiles in a meadow) can process signals and create intelligent behavior.',
      aiConnection: 'Neural networks power everything from image recognition to language models. Each "neuron" is a simple math function, but billions of them connected together create intelligence that rivals human experts in many domains.',
      tryAtHome: 'Build a simple "neural network" with family members: each person is a neuron, passing messages (weighted signals) to neighbors. See how a simple input ("what\'s for dinner?") propagates through the network!',
      ageAppropriate: 'Ages 5-8: Focus on the network metaphor. Ages 9-12: Discuss layers and how deeper networks learn more complex things. Ages 13+: Explore real neural network architectures and training.',
    },
  },
  {
    id: 'eld-2',
    rank: Rank.Elder,
    index: 2,
    name: 'Beyond the Mist',
    subtitle: 'What lies in the unknown?',
    description: 'Thick mist surrounds the valley. Beyond it... new discoveries. But you must herd perfectly to earn the right to explore.',
    gridSize: { x: 22, y: 15 },
    aiConcept: {
      key: 'frontier',
      name: 'The AI Frontier',
      shortName: 'Frontier',
      rank: Rank.Elder,
      depth: 4,
      metaphor: 'The Mist is like the unknown in AI — there\'s so much we haven\'t discovered yet. Every answer leads to new questions!',
      realExplanation: 'AI research constantly pushes into unknown territory. AGI (Artificial General Intelligence), consciousness, creativity, ethics — these are frontier questions. The best AI researchers, like the best shepherds, are humble about what they don\'t know.',
      parentExplanation: 'Your child reached the frontier of our game\'s AI curriculum — a metaphor for the real AI frontier. Researchers are still exploring questions like: Can AI be creative? Can it understand emotions? Should it make decisions for us?',
      keywords: ['frontier', 'AGI', 'ethics', 'consciousness', 'creativity', 'future'],
      relatedConcepts: ['neural_networks', 'knowledge_distillation', 'training'],
    },
    objective: { type: 'herd_all', description: 'Achieve a PERFECT herd — no lost sheep, all discoveries found!' },
    constraints: { fogRadius: 4, maxBarks: 20 },
    terrainSeed: 4002,
    sheepCount: 10,
    sheepBreeds: [SheepBreed.Merino, SheepBreed.Suffolk, SheepBreed.Valais, SheepBreed.Soay, SheepBreed.Jacob, SheepBreed.Dorper, SheepBreed.Romanov, SheepBreed.Highland, SheepBreed.Navajo, SheepBreed.Cheviot],
    obstacles: [
      { type: ObstacleType.Boulder, pos: { x: 7, y: 5 } },
      { type: ObstacleType.Thornbush, pos: { x: 12, y: 4 } },
      { type: ObstacleType.CrumblingWall, pos: { x: 9, y: 8 } },
      { type: ObstacleType.IceBlock, pos: { x: 15, y: 10 } },
    ],
    weather: Weather.Foggy,
    unlockRequirement: { rank: Rank.Elder, index: 1, stars: 2 },
    dialogIntro: {
      id: 'eld-2-intro',
      speaker: 'elder_bark',
      text: 'Beyond the mist lies... well, we don\'t entirely know. In AI research, this is called the FRONTIER — the edge of what we understand. Some questions are still mysteries even to the wisest elders. Today, you\'ll herd at the edge of knowledge itself.',
      emotion: 'mysterious',
    },
    dialogOutro: {
      id: 'eld-2-outro',
      speaker: 'elder_bark',
      text: 'You\'ve reached the frontier, young elder. But remember — the most important thing in AI isn\'t having all the answers. It\'s asking the RIGHT questions. The mist will always be there, and that\'s what makes exploration beautiful. Keep asking "what if?" — that\'s what the best AI researchers do.',
      emotion: 'wise',
      unlockConcept: 'frontier',
    },
    discoveries: [
      { type: CollectibleType.ConceptPage, conceptKey: 'ai_ethics', posHint: 'hidden_path' },
      { type: CollectibleType.ConceptPage, conceptKey: 'agi_definition', posHint: 'center' },
      { type: CollectibleType.LorePage, conceptKey: 'bark_final_secret', posHint: 'behind_obstacle' },
      { type: CollectibleType.Secret, conceptKey: 'mist_origin', posHint: 'corner' },
      { type: CollectibleType.Sticker, conceptKey: 'frontier_explorer', posHint: 'near_sheep' },
    ],
    parentLayerContent: {
      title: 'The AI Frontier',
      conceptName: 'Open Questions in AI',
      whatHappened: 'Your child reached the edge of known knowledge in the game — a metaphor for the real frontiers of AI research.',
      aiConnection: 'AI research is full of open questions: Can machines be truly creative? How do we ensure AI is fair and safe? Will we achieve Artificial General Intelligence? These are questions YOUR child\'s generation may help answer.',
      tryAtHome: 'Ask your child: "If you could ask an AI any question, what would it be?" Their answers reveal deep thinking about the nature of intelligence.',
      ageAppropriate: 'All ages: Discuss what questions are still unanswered in AI. Encourage curiosity and critical thinking about technology\'s future.',
    },
  },
  {
    id: 'eld-3',
    rank: Rank.Elder,
    index: 3,
    name: 'The Grand Gathering',
    subtitle: 'Every sheep, every breed, one perfect herd',
    description: 'The ultimate challenge: herd all 18 sheep from every breed into the pen. Limited barks — make each one count!',
    terrainSeed: 90073,
    gridSize: { x: 22, y: 14 },
    weather: Weather.Golden,
    sheepCount: 18,
    sheepBreeds: [SheepBreed.Wooly, SheepBreed.Merino, SheepBreed.Highland, SheepBreed.Suffolk, SheepBreed.Dorper, SheepBreed.Jacob, SheepBreed.Soay, SheepBreed.Valais, SheepBreed.Navajo, SheepBreed.Katahdin, SheepBreed.Cheviot, SheepBreed.Romanov],
    constraints: { maxBarks: 25, fogRadius: 0 },
    obstacles: [],
    objective: { type: 'herd_all', timeLimit: 180, description: 'Herd all 18 sheep representing all 12 breeds into the pen within 3 minutes. Limited barks — make each one count!' },
    discoveries: [
      { type: 'concept_page' as any, conceptKey: 'ensemble_methods', posHint: 'center' },
      { type: 'sheep_catalog' as any, conceptKey: 'breed_romanov', posHint: 'corner' },
    ],
    dialogIntro: { id: 'eld-3-intro', speaker: 'elder_bark', text: 'This is it, pup. The Grand Gathering! Every breed, every personality, one perfect herd. This is what ensemble methods are all about — many different voices creating one beautiful harmony. Show me everything you have learned!', emotion: 'proud' },
    dialogOutro: { id: 'eld-3-outro', speaker: 'elder_bark', text: 'Magnificent! You have mastered the art of herding — and along the way, you have learned the fundamental patterns that power all of artificial intelligence. From data points to neural networks, from search to generative AI... you now understand them all. You are a true Elder Shepherd!', emotion: 'proud' },
    aiConcept: { key: 'ensemble_methods', name: 'Ensemble Methods', shortName: 'Ensemble', rank: Rank.Elder, depth: 4, metaphor: 'Different sheep breeds have different strengths — fluffy Merinos for warmth, sturdy Highlands for toughness. When you combine all breeds, the flock is stronger than any single type. AI models work the same way!', realExplanation: 'Ensemble methods combine multiple AI models to produce better predictions than any single model alone.', parentExplanation: 'Your child is learning that combining different AI approaches creates more robust systems.', keywords: ['ensemble', 'voting', 'bagging', 'boosting'], relatedConcepts: ['neural_networks', 'model_selection'] },
    parentLayerContent: { title: 'Ensemble Methods', conceptName: 'Combining AI Models', whatHappened: 'Your pup herded sheep of all 12 breeds together', aiConnection: 'Data scientists often combine multiple AI models (an "ensemble") to get better results than any single model alone. This is how most real-world AI systems work — from Netflix recommendations to medical diagnosis.', tryAtHome: 'Ask your child: "If you had a team with different skills, how would you combine them to solve a big problem?"', ageAppropriate: '7+' },
  },
];

// Dialog tree extensions
export const DIALOG_TREE: Record<string, { text: string; emotion?: string; unlockConcept?: string; nextId?: string; choices?: { text: string; nextId: string }[] }> = {
  'app-1-intro-2': {
    text: 'That\'s the spirit! Remember: get near the sheep, face the pen, and bark. They\'ll move away from you — use that to guide them! The pen is the fenced area to the southeast.',
    emotion: 'encouraging',
  },
  'app-1-intro-alt': {
    text: 'A fair question! Sheep always move AWAY from your bark. So stand on the opposite side of the sheep from where you want them to go, then bark! It\'s like pushing them gently with sound.',
    emotion: 'wise',
  },
  'app-2-intro-flock': {
    text: 'Flocking has three rules each sheep follows: 1) SEPARATION — don\'t crowd neighbors, 2) ALIGNMENT — go the same direction as nearby sheep, and 3) COHESION — move toward the group\'s center. No sheep knows the whole plan — they just follow their neighbors!',
    emotion: 'wise',
  },
  'app-2-intro-go': {
    text: 'Go for it! Remember, the sheep want to stay together. Use that! Get behind the group and bark to push them toward the pen as a unit.',
    emotion: 'encouraging',
  },
  'jrn-1-intro-explain': {
    text: 'Exactly! Separation means "don\'t bump into friends." Alignment means "go the same way as nearby sheep." Cohesion means "move toward the center of your group." Three tiny rules, and look — beautiful flocking patterns emerge!',
    emotion: 'wise',
  },
  'jrn-1-intro-sandbox': {
    text: 'Oh, you\'re thinking like an AI researcher! Yes, changing the rules changes the behavior. In the Sandbox mode (unlocked later!), you\'ll be able to adjust these parameters yourself and see what happens. For now, let\'s master the basics!',
    emotion: 'playful',
  },
};

export function getLevelById(id: string): LevelDef | undefined {
  return LEVELS.find(l => l.id === id);
}

export function getLevelsForRank(rank: Rank): LevelDef[] {
  return LEVELS.filter(l => l.rank === rank);
}

export function getNextLevel(currentId: string): LevelDef | undefined {
  const idx = LEVELS.findIndex(l => l.id === currentId);
  if (idx >= 0 && idx < LEVELS.length - 1) return LEVELS[idx + 1];
  return undefined;
}

export function isLevelUnlocked(levelId: string, levelResults: Record<string, { stars: number }>): boolean {
  const level = getLevelById(levelId);
  if (!level) return false;
  if (level.rank === 'apprentice' && level.index === 1) return true;
  // Handle starsRequired field
  if ((level as any).starsRequired) {
    const sr = (level as any).starsRequired as { level: string; stars: number };
    return (levelResults[sr.level]?.stars ?? 0) >= sr.stars;
  }
  if (!level.unlockRequirement) {
    // If no specific requirement, just check if previous level exists and has been attempted
    const idx = LEVELS.findIndex(l => l.id === levelId);
    if (idx > 0) {
      const prev = LEVELS[idx - 1];
      return (levelResults[prev.id]?.stars ?? 0) >= 1;
    }
    return true;
  }
  const req = level.unlockRequirement;
  const reqLevel = LEVELS.find(l => l.rank === req.rank && l.index === req.index);
  if (!reqLevel) return false;
  return (levelResults[reqLevel.id]?.stars ?? 0) >= req.stars;
}

export function calculateStars(
  level: LevelDef,
  time: number,
  sheepHerded: number,
  sheepTotal: number,
  barksUsed: number,
  discoveriesFound: number,
  totalDiscoveries: number
): number {
  // Star 1: Complete the level
  if (sheepHerded < sheepTotal) return 0;

  let stars = 1;

  // Star 2: Find at least 1 discovery
  if (discoveriesFound >= 1) stars = 2;

  // Star 3: Fast time + all discoveries + efficient barks
  const timeLimit = level.objective.timeLimit ?? 120;
 const isFast = time < timeLimit * 0.6;
  const allDiscoveries = discoveriesFound >= totalDiscoveries;
  const efficientBarks = !level.constraints.maxBarks || barksUsed <= (level.constraints.maxBarks * 0.7);

  if (isFast && allDiscoveries && efficientBarks) stars = 3;
  else if ((isFast && allDiscoveries) || (allDiscoveries && efficientBarks)) stars = Math.max(stars, 2);

  return stars;
}