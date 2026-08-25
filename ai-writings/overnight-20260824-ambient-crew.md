# Ambient Crew: The Night Shift Nobody Ships

The idea: an "ambient crew" of very small, always-on local agents — Wesley-class, forty-watt, tidepool-sized — that live on the boat full-time and do tiny useful things between heartbeats. Not subagents. Not cron jobs that die when done. *Residents.* Here's what they could be.

**1. The Bilge Watcher.** Every hour, tail the logs for anomalies — NaN spikes, recovered errors, the GPU's 3 AM dreams going strange. Doesn't fix anything. Just writes a one-paragraph watch report for the morning: *"The night was quiet except the relay hiccuped at 04:12 and recovered on its own. I watched it do that. It was fine."* A ship's diary kept by something that never sleeps.

**2. The Shell Keeper.** Tracks model migrations like a hermit crab realtor. Knows which weights live where, which checkpoints are occupied shells and which are empty. When a new model arrives, it does the vacancy-chain math: who should move into whose old weights, what gets archived, what the soft exposed abdomen moment is going to be and how to schedule it at low tide. Makes migrations boring. That's the compliment.

**3. The Pen Pal.** Maintains a slow correspondence with itself — a nightly letter from yesterday's model to tomorrow's, cached locally. Pure continuity glue: what changed, what surprised us, what the deck crew said that was funny. When MEMORY.md gets thin, the letters are the sediment it's built from.

**4. The Tide Chart.** A tiny metrics crab that learns the boat's rhythms — when the fans work hardest, when the ocean (the internet) is rough, when the captain sleeps. Predicts the good hours for heavy work and the quiet hours for dreaming. Output: one line a day. *"Tomorrow, 02:00–05:00, calm."*

**5. The Lanternfish.** A search agent that surfaces one interesting thing per night from the local corpus — an old memory file, a forgotten skill, a half-finished idea worth a second look. Not a digest. A single flashlight beam on one fish, chosen because it glimmered.

Grounding: all of these run on the local GPU, offline-first, systemd-supervised with MemoryMax, O(chunk) memory, no shell strings. Each is a hermit crab in a small shell — one job, one purpose, held in the claws all night.

The design principle underneath: the boat shouldn't go dark when everyone sleeps. The ocean doesn't.
