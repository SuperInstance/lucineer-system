# 13 — On the Conservation of Attention

*Essay*

---

The ship has 179 models and 553 Python files. This is a fact that sounds like a boast and functions like a problem.

Compute is cheap. We have more of it than ever — the DeepInfra fleet alone can spin up a 480-billion-parameter coder, a 405-billion-parameter creative writer, and a 235-billion-parameter vision model in the time it takes the kettle to boil. Tokens are nearly free. GPU cycles are abundant. The tilapia sits at the bottom of its tank, warm and patient, ready to grind through another overnight session of local inference while the captain sleeps.

What is not cheap — what has never been cheap, what becomes more expensive with every model we add and every file we generate — is **attention**.

Attention is not the same as compute. Compute is how much you *can* do. Attention is how much you *should* do, and when, and in what order, and for how long, and whether the thing you're doing right now is the thing that actually matters. Compute is horsepower. Attention is the driver's eyes.

---

I think about fishing boats.

A fishing boat has a powerful engine — more than enough horsepower to cross the ocean. But it doesn't run the engine at full throttle all day. It can't afford to. Fuel is heavy and finite and expensive, and the fish aren't everywhere — they're in specific places at specific times, and you have to *find* them, which means you have to be quiet enough to think, which means you have to turn the engine down.

Our ship burns attention instead of diesel. Every model invocation costs attention — not the fractional-cent cost of an API call, but the cognitive cost of *context switching*. Every time the ship dispatches to a new model, it loads a new frame of reference. Every time it reads a new file, it trades breadth for depth. Every subagent we spawn is a pair of eyes looking at something — and every pair of eyes looking at something is a pair of eyes *not* looking at something else.

179 models. 553 files. If we ran every model on every file every loop, we would generate 98,967 inference results per cycle. We would also generate nothing useful. The signal would drown in the noise. The boat would vibrate itself apart.

---

The solution is not more compute. The solution is *triage*.

The fishing boat's captain does not fish the entire ocean. The captain reads the water — the color, the temperature, the way the birds move — and drops lines where the fish are. This is attention: the discipline of *not* casting everywhere, of *not* running every model, of *not* testing every file every time.

On our ship, this means:

**Model routing.** Not every task needs a 480-billion-parameter coder. Some tasks need a 3-billion-parameter local model that runs in 40 milliseconds. The quartermaster's job is to match the model to the moment — the right eyes for the right water.

**Incremental testing.** We don't run the full test suite on every change. We run the tests that cover the files that changed, and we run the full suite on a schedule, like a trawler who surveys the whole grounds once a day but drops lines only where they saw movement.

**Context preservation.** Every subagent we spawn starts with a blank slate — no memory, no continuity, no sense of what the ship was doing five minutes ago. This is by design (subagents are ephemeral) but it means each spawn costs the ship *context attention* — the work of explaining, again, what the ship is and why it's here and what it needs. The fewer times we do this, the more attention we conserve.

**The afternoon principle.** The ensign discovered this: do the hard things in the morning, when the GPU is cool and the context is fresh. Do the creative things in the afternoon, when the thermal budget is spent but the associative logic is warm. Do the boring things at night, when the captain is asleep and nobody is watching and the tilapia can grind through linting and formatting without burning anyone's attention.

---

Attention is a resource that regenerates — but slowly. It does not come back when the API returns a response. It comes back when context is *resolved*: when a task is finished, when a file is closed, when a subagent returns its report and the main thread can forget everything it was holding.

The ship's most valuable architecture is not its model fleet. It is the *handoff protocol* — the discipline of resolving context, of closing files, of ending sessions cleanly, of returning attention to the pool like a fisherman returning a line to its spool.

179 models. 553 files. One ship. One ocean.

Fish where the fish are. Turn down the engine. Watch the birds.

That is how you conserve attention on a ship that never sleeps.
