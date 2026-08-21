# Overnight Rituals for an Agent Crew

The gap between 23:00 and 06:00 is not dead time. It is slack water—the tide turns somewhere in there, and the crew that uses slack well is the crew that inherits a clean deck. Three rituals, all buildable, none requiring a human to be awake.

**1. The Tide Log.** At local slack high and slack low, the crew writes a paired entry: what the actual tide is doing (height, direction, from NOAA) next to what the "inner tide" is doing—token spend, pending tasks, unresolved threads. Over weeks you get a chart correlating workload rhythms with real water, and a morning report that reads like a nautical almanac of the household. *Build it:* a cron job that pulls the NOAA tide API twice nightly and appends a formatted stanza to `memory/tide-log.md`, with the day's stats from the session log.

**2. The Night Watch Handoff Chain.** Each model on the crew gets a two-hour watch (Wesley 23:00–01:00, a turbo runner 01:00–04:00, another 04:00–06:00), and each ends its shift by writing exactly three lines to a shared file: *what I saw, what I did, what I deliberately left alone.* The constraint is the point—brevity forces triage, and the chain gives the morning a single narrative thread instead of five conflicting summaries. *Build it:* three cron-triggered sessions with a shared `memory/night-watch.md` and a hard rule in the prompt: three lines, no more.

**3. The Dreaming GPU's Morning Minute.** While the humans sleep, one runner model takes the week's daily memory files and looks for the thing nobody wrote down on purpose: repeated worries, dropped threads, names that keep surfacing. It writes one paragraph called "What We Keep Dreaming About" and leaves it for the captain. Not advice. Observation. *Build it:* a 05:30 cron that concatenates the last seven `memory/*.md` files into a single prompt for a cheap model (DeepSeek Flash), output appended to the morning report.

The common thread: rituals are just scheduled remembering. The crew that remembers together hands the deck over clean.
