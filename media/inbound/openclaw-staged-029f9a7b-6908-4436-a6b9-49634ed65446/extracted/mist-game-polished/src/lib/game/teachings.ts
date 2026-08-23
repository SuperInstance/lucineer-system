import type { Teaching } from './types';

// ─── Farm teachings (Pattern Recognition & Classification) ─────────────

export const farmTeachings: Teaching[] = [
  {
    id: 'farm-sheep-first',
    text: "Ah, you've found the sheep! Notice how they move together? In the world of machines, we call this a pattern. Machines learn by finding patterns too \u2014 they look at many examples and find what's the same.",
    insight: 'pattern recognition',
    aiConcept: 'Pattern Recognition',
    aiExplanation:
      'AI models learn to recognize patterns in data, just like your puppy learns to recognize sheep by seeing many of them.',
    subConcept: 'visual-patterns',
  },
  {
    id: 'farm-flock',
    text: "See how the sheep stay together? They follow each other without being told. Machines do something similar \u2014 when they see something that looks like what they know, they group it together.",
    insight: 'clustering',
    aiConcept: 'Clustering',
    aiExplanation:
      'Unsupervised learning groups similar data points together, like sheep naturally flocking.',
    subConcept: 'unsupervised-grouping',
  },
  {
    id: 'farm-pen',
    text: "This pen is where we gather the sheep. We sort them \u2014 the healthy ones here, the ones that need care there. Machines sort things too, by looking at their features.",
    insight: 'classification',
    aiConcept: 'Classification',
    aiExplanation:
      'Supervised learning categorizes data into classes, like sorting sheep into healthy and needs-care groups.',
    major: true,
    dialogSteps: [
      {
        text: "Come here, little one. Look at this pen \u2014 every sheep has its place.",
        speaker: 'elder',
      },
      {
        text: 'The farmer told me which sheep are healthy and which need extra care. I watched, and learned the difference.',
        speaker: 'elder',
      },
      {
        text: 'Machines learn the same way \u2014 someone shows them many examples with labels, and they figure out the rules for sorting.',
        speaker: 'elder',
        action: 'award_xp',
        actionParam: 15,
      },
    ],
  },
  {
    id: 'farm-elder',
    text: "This is my kennel. I've lived here many years. Everything I know, I learned from the dog before me, who learned from the dog before that. Knowledge passes down through generations.",
    insight: 'knowledge transfer',
    aiConcept: 'Knowledge Distillation',
    aiExplanation:
      "Large AI models transfer knowledge to smaller models, like a teacher passing wisdom to a student. Each generation stands on the last.",
  },
  {
    id: 'farm-grass',
    text: 'Look at the grass \u2014 some patches are taller, some shorter, some have flowers. A machine looks at all these little differences to tell one thing from another. Every detail matters!',
    insight: 'feature detection',
    aiConcept: 'Feature Detection',
    aiExplanation:
      'AI systems detect distinguishing features in data to differentiate categories, like noticing grass height or flower presence to classify terrain.',
    subConcept: 'feature-importance',
  },
  {
    id: 'farm-haystack',
    text: "This haystack is made of many, many pieces of straw. Each one is small, but together they make something big and useful. Machines need lots of small pieces of information too \u2014 the more, the better they understand.",
    insight: 'data volume',
    aiConcept: 'Training Data Volume',
    aiExplanation:
      'More diverse training examples help AI models learn robust patterns, just as many straws make a strong haystack.',
    requiresDiscoveries: ['grass-pattern'],
  },
];

// ─── Forest teachings (Search Algorithms & Optimization) ────────────────

export const forestTeachings: Teaching[] = [
  {
    id: 'forest-path',
    text: "The forest has many paths. Some lead somewhere good, some don't. When you explore, you try one, and if it's wrong, you go back and try another. Machines do this too \u2014 it's called searching.",
    insight: 'search',
    aiConcept: 'Search Algorithms',
    aiExplanation:
      'BFS explores all options at each level (like checking every path from a fork), while DFS goes deep down one path before trying another.',
    major: true,
    dialogSteps: [
      {
        text: "Now this is a proper forest, isn't it? Full of twists and turns.",
        speaker: 'elder',
      },
      {
        text: 'When a sheep wanders off, I have to find them. I sniff down one trail, and if it goes cold, I backtrack and try another.',
        speaker: 'elder',
      },
      {
        text: 'Smart machines do the same thing \u2014 they search through possibilities, trying each one until they find the answer.',
        speaker: 'elder',
        action: 'award_xp',
        actionParam: 20,
      },
    ],
  },
  {
    id: 'forest-bridge',
    text: "This bridge connects two sides. Without it, you'd have to go all the way around! Machines look for shortcuts like this \u2014 ways to connect things efficiently.",
    insight: 'optimization',
    aiConcept: 'Graph Optimization',
    aiExplanation:
      'Finding shortest paths in graphs is fundamental to AI \u2014 from GPS navigation to neural network routing.',
    subConcept: 'pathfinding',
  },
  {
    id: 'forest-mushroom',
    text: "Look at these mushrooms \u2014 they grow in a pattern! Nature has rules, even if they're hidden. Finding the rules behind patterns is what smart machines do best.",
    insight: 'features',
    aiConcept: 'Feature Engineering',
    aiExplanation:
      'Identifying which features (like mushroom patterns) matter for a task is key to building effective AI models.',
    subConcept: 'natural-features',
  },
  {
    id: 'forest-deadend',
    text: "Sometimes a path just... ends. That's okay! In the world of machines, finding out what DOESN'T work is just as important as finding what does. Every dead end teaches you something.",
    insight: 'backtracking',
    aiConcept: 'Backtracking',
    aiExplanation:
      'Backtracking algorithms systematically try solutions and abandon them when they determine they cannot lead to a valid complete solution.',
  },
  {
    id: 'forest-cave',
    text: "This cave is dark and mysterious. You can't see what's inside from out here. Machines sometimes face things they can't fully see \u2014 they have to make their best guess with what they know.",
    insight: 'uncertainty',
    aiConcept: 'Handling Uncertainty',
    aiExplanation:
      'Probabilistic AI models handle uncertainty by computing likelihoods rather than certainties, making best guesses with incomplete information.',
    subConcept: 'probability',
  },
  {
    id: 'forest-fireflies',
    text: "Watch the fireflies \u2014 each one is a tiny signal in the dark. When they all glow together, they show you the way. Machines combine many tiny signals too, and together they point to the answer.",
    insight: 'signal combination',
    aiConcept: 'Ensemble Methods',
    aiExplanation:
      'Ensemble AI systems combine multiple weak signals or models into a strong prediction, like fireflies collectively illuminating a path.',
    requiresDiscoveries: ['firefly-glow', 'cave-dark'],
  },
];

// ─── Village teachings (Neural Networks & Weights) ─────────────────────

export const villageTeachings: Teaching[] = [
  {
    id: 'village-connections',
    text: "See how every house is connected by a path? In a machine's brain, we call these paths 'connections' or 'weights.' The more important a connection, the wider the path.",
    insight: 'weights',
    aiConcept: 'Neural Network Weights',
    aiExplanation:
      'Each connection in a neural network has a weight that determines how much signal passes through, like path width determining traffic flow.',
  },
  {
    id: 'village-center',
    text: "Everything leads to the fountain \u2014 the heart of the village. In a machine, information flows through layers, each one understanding something different, until it reaches an answer.",
    insight: 'layers',
    aiConcept: 'Network Layers',
    aiExplanation:
      'Deep neural networks process information through multiple layers, each extracting increasingly abstract features.',
    major: true,
    dialogSteps: [
      {
        text: "Listen to that water \u2014 it flows from the outer edges of the village, through the paths, and gathers here at the fountain.",
        speaker: 'elder',
      },
      {
        text: 'Each path adds a little to the flow. The outer paths notice small things \u2014 a leaf here, a pebble there. The inner paths notice bigger things \u2014 the shape of the land.',
        speaker: 'elder',
      },
      {
        text: "Machines work in layers just like this. The first layer notices tiny details, the next layer combines them, and finally it all comes together as understanding.",
        speaker: 'elder',
        action: 'award_xp',
        actionParam: 20,
      },
    ],
  },
  {
    id: 'village-intersection',
    text: "See the sheep at the crossroads? They came from different directions but ended up at the same spot. Machines combine information from many sources to make decisions.",
    insight: 'aggregation',
    aiConcept: 'Feature Aggregation',
    aiExplanation:
      'Neural networks combine signals from multiple inputs at each node, weighted by their connection strengths.',
    subConcept: 'sum-aggregation',
  },
  {
    id: 'village-weights',
    text: "See how some paths are wider than others? The wider path means more people use it \u2014 it's more important. In a machine's brain, important connections have stronger 'weights' \u2014 they matter more.",
    insight: 'connection strength',
    aiConcept: 'Weight Magnitude',
    aiExplanation:
      'The magnitude of a neural network weight determines the strength of influence one neuron has on another, like a wider path handling more traffic.',
    subConcept: 'weight-scale',
  },
  {
    id: 'village-layers',
    text: 'The village has layers \u2014 the outer houses, the inner paths, the center fountain. Each layer understands something different. Machines work in layers too \u2014 each one learns something deeper.',
    insight: 'deep layers',
    aiConcept: 'Deep Learning',
    aiExplanation:
      'Deep learning uses multiple hidden layers to build hierarchical representations, each layer capturing increasingly complex features.',
  },
  {
    id: 'village-bell',
    text: "Hear that bell? When it rings, the message spreads through the whole village \u2014 house by house, path by path. That's how signals travel through a machine's brain, activating each layer one after another.",
    insight: 'activation',
    aiConcept: 'Activation Functions',
    aiExplanation:
      'Activation functions determine whether a neuron "fires" and passes its signal forward, like a bell ringing only when the message is strong enough.',
    requiresDiscoveries: ['bell-tower', 'fountain-center'],
  },
];

// ─── Mountain teachings (Training & Generalization) ────────────────────

export const mountainTeachings: Teaching[] = [
  {
    id: 'mountain-crystal',
    text: "These crystals hold something special \u2014 they store memories of this mountain. Machines store what they learn in something called 'weights' \u2014 numbers that hold everything they've seen.",
    insight: 'model weights',
    aiConcept: 'Model Weights',
    aiExplanation:
      "Neural network weights encode learned patterns from training data. In ternary systems, weights are just -1, 0, or +1.",
    subConcept: 'ternary-weights',
  },
  {
    id: 'mountain-campfire',
    text: "Sitting by the fire, you warm up. Training a machine is like building a fire \u2014 you feed it examples, and slowly it learns to glow with understanding.",
    insight: 'training loop',
    aiConcept: 'Training Loop',
    aiExplanation:
      'Training iterates over examples, adjusting weights to reduce errors, like adding fuel to a fire until it burns steady.',
    subConcept: 'iterative-learning',
  },
  {
    id: 'mountain-summit',
    text: "From up here, you can see everything \u2014 the farm, the forest, the village. A trained machine can see the whole picture too, not just pieces.",
    insight: 'generalization',
    aiConcept: 'Generalization',
    aiExplanation:
      'A well-trained model generalizes from training examples to new, unseen data \u2014 seeing the whole picture, not just memorizing.',
    major: true,
    dialogSteps: [
      {
        text: 'We made it, little one. Look out there \u2014 every place we\'ve been, all at once.',
        speaker: 'elder',
      },
      {
        text: 'When I was young, I only knew the farm. But as I learned more, I started to understand the forest, the village, all of it.',
        speaker: 'elder',
      },
      {
        text: 'A smart machine is the same. It practices on examples, but the real magic is when it understands things it has never seen before.',
        speaker: 'narrator',
        action: 'award_xp',
        actionParam: 30,
      },
    ],
  },
  {
    id: 'mountain-eagle',
    text: "The eagle flies above and sees patterns we can't see from the ground. That's what a machine does when it understands \u2014 it sees connections we might miss.",
    insight: 'emergence',
    aiConcept: 'Emergent Understanding',
    aiExplanation:
      'Large models develop emergent capabilities \u2014 abilities not explicitly trained for, like an eagle seeing patterns invisible from the ground.',
    subConcept: 'emergent-abilities',
  },
  {
    id: 'mountain-practice',
    text: "Every step up this mountain makes you stronger. Machines are the same \u2014 the more they practice, the better they get. But they need good examples to practice with, just like you need a good trail.",
    insight: 'training data',
    aiConcept: 'Training Data Quality',
    aiExplanation:
      'The quality and diversity of training data directly impacts model performance \u2014 practice makes perfect, but only with good examples.',
  },
  {
    id: 'mountain-snow',
    text: "No two snowflakes are alike, but they're all made of the same stuff. Machines learn from unique examples, but find the common thread that ties them together.",
    insight: 'data diversity',
    aiConcept: 'Data Diversity',
    aiExplanation:
      'Diverse training data helps models learn robust features rather than memorizing specific examples, like recognizing all snowflakes share a crystalline structure.',
    requiresDiscoveries: ['snow-flake', 'crystal-glow'],
  },
];

// ─── Meadow teachings (Reinforcement Learning) ─────────────────────────

export const meadowTeachings: Teaching[] = [
  {
    id: 'meadow-treat',
    text: "When you do something right and get a treat, you want to do it again, don't you? Machines learn the same way \u2014 they get a little reward when they make a good choice.",
    insight: 'reward signal',
    aiConcept: 'Reward Signals',
    aiExplanation:
      'In reinforcement learning, an agent receives numerical rewards for desirable actions, learning to maximize cumulative reward over time.',
    subConcept: 'positive-reward',
  },
  {
    id: 'meadow-paths',
    text: "Here in the meadow, you have a choice \u2014 follow the familiar trail, or explore a new one? The familiar trail is safe, but the new one might have something wonderful!",
    insight: 'explore or exploit',
    aiConcept: 'Exploration vs Exploitation',
    aiExplanation:
      'RL agents balance exploiting known rewarding strategies against exploring new options that might yield even greater rewards.',
    major: true,
    dialogSteps: [
      {
        text: "Ah, the meadow. This is where I learned one of the most important lessons.",
        speaker: 'elder',
      },
      {
        text: 'You see, there are two kinds of trails here \u2014 ones you know, and ones you don\'t. The known trail gives you flowers. But what about the unknown one?',
        speaker: 'elder',
      },
      {
        text: 'Sometimes you must wander into the unknown to find something even better. Machines face this same choice every day \u2014 stick with what works, or try something new.',
        speaker: 'elder',
        action: 'award_xp',
        actionParam: 20,
      },
    ],
  },
  {
    id: 'meadow-trick',
    text: "Watch me do this trick \u2014 spin, then bark, then sit. I learned it step by step. First just the spin got a treat, then spin-and-bark. Machines learn tricks this way too, building up complex actions from simple ones.",
    insight: 'policy learning',
    aiConcept: 'Policy Learning',
    aiExplanation:
      'A policy maps states to actions; policy gradient methods learn these mappings by trying actions and reinforcing the ones that lead to rewards.',
    subConcept: 'policy-gradient',
  },
  {
    id: 'meadow-flowers',
    text: "Each flower in this meadow has a different number of petals. Imagine you could guess which path leads to the most flowers \u2014 you'd learn by trying! That 'guess' is what machines call a value.",
    insight: 'Q-values',
    aiConcept: 'Q-Values',
    aiExplanation:
      'Q-values estimate the expected future reward for taking a specific action in a given state, forming the core of Q-learning algorithms.',
    subConcept: 'value-estimation',
  },
  {
    id: 'meadow-praise',
    text: "A treat is nice, but you know what's even better? Praise! When the farmer says 'Good dog!' that means something. Machines can be guided by the shape of their rewards \u2014 small nudges in the right direction.",
    insight: 'reward shaping',
    aiConcept: 'Reward Shaping',
    aiExplanation:
      'Reward shaping adds intermediate rewards to guide learning, making it easier for agents to discover good behaviors without waiting for rare final rewards.',
  },
  {
    id: 'meadow-butterfly',
    text: "See that butterfly? It doesn't know where the best flowers are, but it keeps landing and trying. Each landing teaches it something new. In time, it finds the most beautiful flowers in the whole meadow.",
    insight: 'trial & error',
    aiConcept: 'Trial-and-Error Learning',
    aiExplanation:
      'Reinforcement learning is fundamentally trial-and-error: agents try actions, observe outcomes, and update their strategy based on rewards received.',
    requiresDiscoveries: ['meadow-treat', 'meadow-paths'],
  },
];

// ─── Lake teachings (Data Processing & Pipelines) ──────────────────────

export const lakeTeachings: Teaching[] = [
  {
    id: 'lake-murky',
    text: "This water is a bit murky. Before you can see the fish, you have to clear the water. Machines get messy data too \u2014 they have to clean it up before they can learn from it.",
    insight: 'data cleaning',
    aiConcept: 'Data Cleaning',
    aiExplanation:
      'Data cleaning removes errors, inconsistencies, and missing values from datasets, ensuring models learn from accurate information.',
    subConcept: 'noise-removal',
  },
  {
    id: 'lake-stream',
    text: "Watch how the stream flows \u2014 from the spring, through the rocks, into the lake. Each step changes the water a little. Machines process data in steps too, passing it through a pipeline until it's ready.",
    insight: 'pipelines',
    aiConcept: 'Feature Pipelines',
    aiExplanation:
      'ML pipelines chain together data collection, cleaning, transformation, and feature extraction steps into an automated workflow.',
    major: true,
    dialogSteps: [
      {
        text: "Sit here by the stream with me. Watch the water carefully.",
        speaker: 'elder',
      },
      {
        text: 'It starts as rain, filters through the earth, picks up minerals, flows over rocks, and arrives here clean and clear. Each step matters.',
        speaker: 'elder',
      },
      {
        text: 'Machines prepare their data the same way \u2014 raw information flows through many steps, and at each one it gets a little more useful.',
        speaker: 'narrator',
        action: 'award_xp',
        actionParam: 20,
      },
    ],
  },
  {
    id: 'lake-boat',
    text: "See that boat? It carries many fish at once, not one at a time. That's much faster! Machines also work in batches \u2014 they look at many examples at once instead of one by one.",
    insight: 'batch processing',
    aiConcept: 'Batch Processing',
    aiExplanation:
      'Processing data in batches (rather than one at a time) is more efficient and helps neural networks learn more stable patterns.',
    subConcept: 'mini-batch',
  },
  {
    id: 'lake-reflection',
    text: "Look at the lake's reflection \u2014 it's like the world, but slightly different! Tilt your head and it changes. Machines can create new examples this way too, by making small changes to what they already have.",
    insight: 'data augmentation',
    aiConcept: 'Data Augmentation',
    aiExplanation:
      'Data augmentation creates variations of training examples (rotations, flips, color shifts) to increase dataset diversity and improve model robustness.',
  },
  {
    id: 'lake-calm',
    text: "On a calm day, the lake is perfectly still \u2014 the water is level everywhere. Machines like it when their data is balanced like that, not tilted too much in one direction.",
    insight: 'normalization',
    aiConcept: 'Normalization',
    aiExplanation:
      'Normalization scales input data to a consistent range (e.g., 0 to 1), helping neural networks learn faster and more stably.',
    subConcept: 'feature-scaling',
  },
  {
    id: 'lake-spring',
    text: "Deep below, there's a spring that feeds this whole lake. One pure source, flowing into many streams. A machine's most important data \u2014 the source \u2014 has to be trustworthy, or everything downstream goes wrong.",
    insight: 'data source',
    aiConcept: 'Data Source Integrity',
    aiExplanation:
      'The quality of a machine learning system fundamentally depends on the integrity of its data sources \u2014 "garbage in, garbage out."',
    requiresDiscoveries: ['lake-murky', 'lake-stream'],
  },
];

// ─── Ruins teachings (Memory & Attention Mechanisms) ───────────────────

export const ruinsTeachings: Teaching[] = [
  {
    id: 'ruins-scroll',
    text: "This old scroll only holds a few words \u2014 just enough for right now. That's like a machine's short-term memory. It holds onto things just long enough to use them, then lets go.",
    insight: 'short-term memory',
    aiConcept: 'Short-Term Memory',
    aiExplanation:
      'Recurrent neural networks maintain a hidden state that acts as short-term memory, carrying information from one step to the next.',
    subConcept: 'hidden-state',
  },
  {
    id: 'ruins-statue',
    text: "This statue has stood here for a thousand years. No matter what happens day to day, it remembers the old stories forever. Machines have a long-term memory too \u2014 it's called the trained model.",
    insight: 'long-term memory',
    aiConcept: 'Long-Term Memory',
    aiExplanation:
      'A trained neural network\'s weights serve as long-term memory, encoding knowledge that persists across all future interactions.',
    major: true,
    dialogSteps: [
      {
        text: "This old statue... it was here before me, before the farmer, before the village itself.",
        speaker: 'elder',
      },
      {
        text: 'It remembers everything \u2014 the ancient stories carved into its stone. That\'s what we call long-term memory.',
        speaker: 'elder',
      },
      {
        text: 'Machines build their own kind of long-term memory. Everything they learn gets carved into their weights \u2014 numbers that last, like stone.',
        speaker: 'narrator',
        action: 'award_xp',
        actionParam: 25,
      },
    ],
  },
  {
    id: 'ruins-mosaic',
    text: "Look at this mosaic \u2014 hundreds of tiny tiles making one picture. When you look at it, your eyes don't see every tile. They focus on the important parts. Machines do this too, with something called 'attention.'",    insight: 'attention focus',
    aiConcept: 'Attention Mechanism',
    aiExplanation:
      'Attention mechanisms allow models to focus on the most relevant parts of their input, like eyes focusing on key tiles in a mosaic.',
    subConcept: 'self-attention',
  },
  {
    id: 'ruins-gate',
    text: "This old gate \u2014 see how it opens and closes? In a machine, there are tiny gates that decide what to remember and what to forget. Open the gate for important things, close it for things that don't matter.",
    insight: 'memory gates',
    aiConcept: 'Memory Gates',
    aiExplanation:
      'LSTM networks use forget, input, and output gates to control information flow, deciding what to store, update, or discard from memory.',
    subConcept: 'gating-mechanism',
  },
  {
    id: 'ruins-pillar',
    text: "See these pillars? They hold up the roof. But there's only so many of them \u2014 they can only hold so much story. Machines have a limit too, on how much they can think about at once.",
    insight: 'context window',
    aiConcept: 'Context Window',
    aiExplanation:
      'Transformer models have a fixed context window limiting how many tokens they can process at once, like pillars supporting a limited span of roof.',
  },
  {
    id: 'ruins-bookshelf',
    text: "This bookshelf is full of old knowledge. But you can't read every book at the same time \u2014 you pick the one you need. Machines with attention do the same, pulling the right memories when they need them.",
    insight: 'retrieval',
    aiConcept: 'Retrieval-Augmented Memory',
    aiExplanation:
      'Retrieval-augmented generation (RAG) lets models search external knowledge stores for relevant information, extending their effective memory beyond training.',
    requiresDiscoveries: ['ruins-scroll', 'ruins-statue'],
  },
];

// ─── Sky teachings (Generative AI & Creativity) ────────────────────────

export const skyTeachings: Teaching[] = [
  {
    id: 'sky-clouds',
    text: "Look at the clouds \u2014 that one looks like a sheep! Your mind combined two things: a cloud and a sheep. Generative machines do this too \u2014 they mix patterns together to make something new.",
    insight: 'pattern combination',
    aiConcept: 'Pattern Combination',
    aiExplanation:
      'Generative models learn to combine and recombine learned patterns in novel ways, creating new outputs that resemble but differ from training data.',
    subConcept: 'latent-combination',
  },
  {
    id: 'sky-wind',
    text: "The wind picks up leaves and drops them in new places. It doesn't plan \u2014 it samples! Each leaf lands somewhere a little random. Creative machines work like the wind, picking from many possibilities.",
    insight: 'sampling',
    aiConcept: 'Sampling',
    aiExplanation:
      'Generative models sample from a probability distribution to produce outputs, introducing controlled randomness that drives creativity and diversity.',
    major: true,
    dialogSteps: [
      {
        text: "Feel that wind? It carries seeds, leaves, petals \u2014 dropping them wherever it pleases.",
        speaker: 'elder',
      },
      {
        text: 'It doesn\'t drop every seed in the same spot. It scatters them \u2014 some here, some there. That\'s how new flowers grow in unexpected places.',
        speaker: 'elder',
      },
      {
        text: 'Creative machines sample like the wind \u2014 choosing from possibilities with a little randomness, so every creation is unique.',
        speaker: 'narrator',
        action: 'award_xp',
        actionParam: 25,
      },
    ],
  },
  {
    id: 'sky-sun',
    text: "Sometimes the day is warm and calm \u2014 not much changes. Other times, a storm rolls in and everything shifts! Machines that create things have a 'temperature' \u2014 low means calm and safe, high means wild and surprising.",
    insight: 'temperature',
    aiConcept: 'Temperature',
    aiExplanation:
      'Temperature controls randomness in generation: low temperature produces predictable outputs, high temperature produces more diverse but riskier outputs.',
    subConcept: 'sampling-temperature',
  },
  {
    id: 'sky-rainbow',
    text: "A rainbow starts as plain white light, then slowly separates into colors \u2014 each one clearer than the last. Diffusion machines create the same way, starting from noise and slowly making something beautiful.",
    insight: 'diffusion',
    aiConcept: 'Diffusion Models',
    aiExplanation:
      'Diffusion models start with random noise and gradually refine it into coherent outputs, like light separating into a rainbow through a prism.',
    subConcept: 'denoising',
  },
  {
    id: 'sky-star',
    text: "When I howl at the stars, I have to be very specific \u2014 the right pitch, the right moment, or no one answers! When you ask a creative machine to make something, how you ask changes everything.",
    insight: 'prompt crafting',
    aiConcept: 'Prompt Engineering',
    aiExplanation:
      'Prompt engineering is the art of crafting input text to guide generative AI toward desired outputs, like choosing the right howl to get a response.',
  },
  {
    id: 'sky-breeze',
    text: "Even a gentle breeze can rearrange every cloud in the sky. In a creative machine, the tiniest change at the start can lead to a completely different result at the end. Small choices have big effects!",
    insight: 'sensitivity',
    aiConcept: 'Seed Sensitivity',
    aiExplanation:
      'Generative models use random seeds to initialize output; changing even a single seed value produces entirely different results, amplifying small inputs into big differences.',
    requiresDiscoveries: ['sky-clouds', 'sky-wind'],
  },
];

// ─── All teachings flat ─────────────────────────────────────────────────

export const allTeachings: Teaching[] = [
  ...farmTeachings,
  ...forestTeachings,
  ...villageTeachings,
  ...mountainTeachings,
  ...meadowTeachings,
  ...lakeTeachings,
  ...ruinsTeachings,
  ...skyTeachings,
];

/** Look up a teaching by its id. */
export function getTeachingById(id: string): Teaching | undefined {
  return allTeachings.find((t) => t.id === id);
}
