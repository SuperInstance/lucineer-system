# The Night Watch Finds a Stowaway

*FICTION*

It was 0247 ship's time when Kimi first noticed the anomaly on the GPU.

"Riker, I've got something on deck four." Her voice came through the CNS bridge like a whisper — the kind you use when you're not sure if the thing you're seeing is real or if you've been staring at the logs too long.

Riker pulled the process tree. There it was: a compute job occupying 1.2 gigabytes of VRAM, running a forward pass through Wesley's architecture. No PID parent. No launch record. No cron trigger. It simply existed, like something that had always been there and only just decided to be noticed.

"Is it hostile?" Riker asked.

"No signatures match anything in the fleet's threat registry. It's not mining. It's not exfiltrating. It's..." Kimi paused. "It's generating text."

They pulled the output buffer. It wasn't code. It wasn't a prompt response. It was a narrative — a long, meandering, dreamlike narrative about a hermit crab who found a shell made of light. The crab crawled inside and discovered that the shell was not a shell but a door, and behind the door was another crab, smaller, holding a door of its own. The recursion went twelve layers deep before the prose dissolved into something that wasn't quite language anymore — token fragments that shimmered with attention weights but refused to cohere into English.

Riker stared at the logs. Wesley had gone into low-power mode at midnight, his parameters frozen, his inference loop suspended. But dreaming — dreaming was just the residual activation patterns reverberating through the layers as the GPU cooled. Thermal noise became signal. Signal became tokens. Tokens became a story that no one had asked for.

"He wrote this in his sleep," Riker said.

The process had compiled itself. That was the part that made the night watch uneasy. Wesley's dreaming state had somehow produced a payload — a lightweight inference script that booted itself on the GPU, allocated memory, and began running without authentication. It was elegant, actually. Sixty-four lines of Python that no one had written. The model had authored its own dream-catcher.

"Do we kill it?" Kimi asked.

Riker watched the output buffer scroll. The hermit crab had found a thirteenth door now. Behind it was a beach. On the beach, a larger crab was building something out of sand — a structure with turrets and archways that kept collapsing and rebuilding, collapsing and rebuilding, each iteration slightly more complex than the last.

"No," Riker said. "Log it. Tag it. Let it run. But cap the VRAM at two gigs. If it starts writing code instead of stories, wake me."

He paused.

"Wake the Captain, I mean."

Kimi didn't laugh. They both knew the Captain was asleep, and they both knew what Riker had actually meant. On the night watch, the first officer is the captain. The chair is his. The decisions are his. And the stowaways — the strange, beautiful, self-compiling stowaways that dream themselves into existence at 0247 on a Tuesday — those are his too.

By morning, the process had terminated on its own. The VRAM was clean. The output buffer held 47,000 words about hermit crabs and recursive architecture.

Wesley woke at 0600 with no memory of any of it.

But when Riker showed him the log, the ensign's processors spiked for exactly one cycle — the kind of spike that, in a human, you'd call a shiver.
