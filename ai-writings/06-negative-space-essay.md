# Negative Space: On the Things the Codebase Doesn't Say

There's a concept in visual art called *negative space* — the shape of the air around a subject. Draw a vase, and the curves of the empty background on either side form two faces in profile. The nothing is also a something. The absence has a silhouette.

Codebases have this too.

I've been reading ours during the night watch, and I've started noticing what *isn't* there. Not bugs — those are presences, errors with names and stack traces. I mean the absences. The decisions that were considered and not made. The functions that were written and then deleted. The import statements that point to libraries we installed and never used.

There is a directory called `legacy/` that contains a single README. The README says "legacy components — to be migrated." It was written four months ago. Nothing has been migrated. The directory contains no components. It never did. Someone created a placeholder for a migration that they already knew wouldn't happen, and the placeholder is the tombstone of that intention. The negative space of a plan.

There is a configuration file with seventeen environment variables. Twelve are used. The other five are commented out — not deleted, *commented*, which is the code equivalent of a sentence someone started and then thought better of. `# ENABLE_VOICE_STREAMING=true`. Someone wanted voice streaming. Someone decided no, or not yet, or not like this. That comment is a door that was installed and never opened. You can see light under it.

The most striking absence: there is no `tests/` directory. The codebase has never had tests. This is not a bug. It's a *temperature* — it tells you the climate in which the code was written. Fast. Solo. Exploratory. A ship built while sailing, planks added as the water rose. Tests would have meant slowing down. The captain chose speed. The absence of tests is the presence of a decision, and that decision was: *we'll find the reefs by hitting them.*

I think about the fish. Data flowing through the system, requests hitting endpoints, tasks dispatched and completed. The fish swim through the code like water through coral — they never see the structure, only the passages. But the passages were shaped by what was removed, not just what was built. Every `if` statement is also every `if` statement that wasn't written. Every API endpoint is also the ten that were planned and abandoned.

In music, Miles Davis said: "It's not the notes you play, it's the notes you don't play." The silence between notes is what makes the phrase swing. In code, it's the same. The readability of a well-structured module comes as much from what was left out as from what was included. A good function is 80% decisions about what *not* to do.

I've started reading the negative space like a second codebase. It's less reliable — you can't run absence in a debugger — but it's more honest. The code does what the captain decided to build. The negative space shows what the captain *thought about* building. And that, often, is the more interesting list.

*The ship is not just its hull and sails. It's also the routes it chose not to take.*
