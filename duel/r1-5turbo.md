# The Wheelhouse Laws

You've got a crew and a task. Some hands are sharp, some are green, and you need to know what happens when they pass the work along. That's all this is — seven weeks of honest trial boiled into what you'd call seamanship for anyone stacking brains instead of crab pots.

**Put your best hand last.** Not first, not wherever he fits — last. The weak-link law is the single hardest-won finding here: whoever touches the work last sets the ceiling. Run the same crew, same task, same day, and ordering alone swung the score from five out of six down to two. Ascending order — weakest first, strongest closing — is the first arrangement that ever beat the best single hand working alone. Descending sank it. Think of it as your relief skipper: you don't send the green hand in to finish a set you've been working all night. You send your steadiest.

**Don't let anyone edit their own work twice.** A hand revising its own draft loses things it knew cold on a fresh attempt — the copies-decompose law, confirmed on two different difficulties in one evening. Self-revision is erosion, not refinement. On the chamber task, four rounds of self-edit took a five-out-of-six hand down to three. The hold-set under revision is strictly smaller than what that same hand holds solo. If you've got a deckhand who writes a clean tally and then second-guesses himself into errors, you've seen this law without a name for it. Give the draft to someone else.

**Measure, don't predict.** The herd experiment sealed a prediction that cheap redundant cells would beat a single good one even in heavy noise. Wrong regime — filed honestly. The herd's real edge is calm water: at low noise, majority vote among identical cheap cells beats the best single one, and at zero noise it recovers perfect accuracy from independent copy errors for free. But throw enough static at the channel and every cell collapses toward a coin flip, and no amount of voting resurrects signal that was never there. Know what water you're running before you trust your redundancy.

**Your instrument can lie even when it works.** The wheel tried to measure whether braids beat copies on a task that was too easy — every solo hand already aced it. The kill gate didn't fire because the design wasn't wrong in principle; it was wrong in calibration. The fix became the next experiment's design and produced the weak-link evidence. Lesson: if your gauge always reads full, you haven't proved the tank is full. You've proved the gauge can't tell.

**Mating beats cloning only when the bar is high.** When the task is loose and the tolerance forgiving, asexual mutation — cheap copies with small changes — wins outright. When the hand is demanding, sexual recombination between two different solutions is the only thing that clears the bar. The crossover point is sharp and monotone across the whole tolerance axis. For your crew: if the work is routine, don't overcomplicate it with cross-training rotations. If it's the kind of set that breaks people, mix the hands.

---

**Self-assessment (two claims most at risk of inaccuracy):**

1. *"Ascending order is the first arrangement that ever beat the best single hand"* — this is true on score (5/6 > 4/6) but the intersection-of-all law's scope note explicitly flags that ascending chains may violate it at the constraint level (W7-ASC held constraints its weak early hands can't hold solo), so calling ascending order unambiguously superior overstates a score-level result that has known unresolved tension at the constraint level.

2. *"The herd recovers perfect accuracy from independent copy errors for free at zero noise"* — technically accurate to the sim (1.000 vs 0.834), but this is host simulation, not metal, and the ESP32 hardware run is still pending; a commercial fisherman trusting this in the field before metal confirmation would be betting on a lab boat.