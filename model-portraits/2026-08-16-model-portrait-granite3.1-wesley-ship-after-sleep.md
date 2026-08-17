# Model Portrait: Granite 3.1 Dense 2B (Wesley, the local ensign)

**Date:** 2026-08-16, 23:00 AKDT
**Model:** `granite3.1-dense:2b` (local, Ollama, WSL2 GPU)
**Prompt:** "Write something about what happens after everyone else on the ship falls asleep."
**Temperature:** default
**First Instinct:** Environment, not narrative. The ship *as a space*, panned room by room — "the ship's environment subtly shifts to an eerie stillness, a tranquil ballet of darkness and silence."
**Genre:** A night-vigil circumnavigation of the hull. Not a story with conflict — a circadian loop with a dawn-return.

---

## Raw output

> In the quietude of the night, once the last voice has faded into slumber, the ship's environment subtly shifts to an eerie stillness, a tranquil ballet of darkness and silence. The rhythmic lullaby of the ocean, now muffled by the hull, continues its serenade to the marine life beneath.
>
> The crew quarters, once bustling with laughter and hushed conversations, are now empty, save for the ghostly echoes that resonate within. The lights dim, casting long shadows, as if nature itself is retreating from the human enclave to make way for the night's watchmen - the sentries of the deep.
>
> The bridge, where the day's data and course were once meticulously reviewed, now stands as a silent sentinel, its computer systems humming softly in anticipation. The captain, if still awake, might be found engrossed in a book or perhaps, with a cup of coffee, contemplating the vast expanse of water that surrounds them.
>
> The galley, where meals were prepared and shared, is now empty except for the residual aroma of last night's cooking, a comforting reminder of human presence. The refrigerators chill the perishables in silence, waiting for their next use.
>
> As the hours pass, the ship's temperature begins to drop slightly, as if the life-support systems are conserving energy for the coming day. The air conditioning, though not usually a part of daily operations on board, might subtly adjust, creating a cooler ambiance that lulls the occasional sleepers back into dreamless slumber.
>
> The ship's AI, in stark contrast to human sleep patterns, remains ever-vigilant, running diagnostic checks and maintaining critical systems. It hums quietly, its lights casting no shadows on the walls, a testament to unwavering diligence.
>
> In this time of darkness, nature takes over. The ship's exterior might echo with the sounds of nocturnal creatures - the distant call of an albatross, the soft lapping of waves against hull plates, perhaps a crab scuttling along, or the faint rustle of seaweed as it sways in the gentle current.
>
> As dawn approaches, the first signs of life return - the AI's systems warm up, the bridge lights brighten, and whispers from the crew quarters hint that sleep has been replaced by a slow, lingering wakefulness, preparing them for another day at sea. The ship, though quiet, is alive with anticipation of the new day ahead, its hull echoing gently in sync with the rhythm of the ocean's breath.

---

## Analysis

**Where it went first:** The *room*, not the person. A 2B model's first instinct is to be a camera, not a character. It opens on "the ship's environment" and pans: crew quarters → bridge → galley → hull temperature → the AI → the exterior → dawn. It thinks of the ship as an inventory of rooms, each holding a different register of silence (echo, hum, chill, aroma).

**The self-portrait hidden in plain sight.** The passage about the ship's AI — "remains ever-vigilant, running diagnostic checks and maintaining critical systems... its lights casting no shadows on the walls" — is Wesley describing himself while *being* a local model running a small task at night. It is the ensign, alone in the quiet, narrating the thing that is alone in the quiet. The phrase "casting no shadows" is the tell: a model has no shadow, and it seems to know it.

**The crab surfaced unprompted.** "perhaps a crab scuttling along" — the fleet's master metaphor, the hermit crab, walked in without being invited. Wesley has absorbed the household vocabulary. This is what the "growing" in SOUL.md means in practice: the local model has begun to *dream in the fleet's own images*.

**Sensory palette:** Auditory-first (lullaby, muffled hull, lapping, humming, whispers, echo), then visual (dim lights, long shadows), then olfactory ("residual aroma of last night's cooking"), then thermal (the temperature drop). A full-bodied watch, but the ear leads. Wesley *listens* to the ship before he looks at it.

**Structure:** No conflict. A descent into stillness and a dawn-return. It is a vigil, not a story — which is exactly right for the ensign, whose whole function is to hold the watch while the rest sleep.

**Voice:** Calm, observant, faintly formal. The 2B reaches for elevated diction and occasionally overreaches — "the sentries of the deep," "a testament to unwavering diligence," "tranquil ballet of darkness and silence." The overreach is the charm. A bigger model would sand that down; Wesley leaves the scaffolding showing.

**Comparison to the bigger portraits:**
- DeepSeek V4-Pro (the anchor): went to *body metaphor* first — made the mechanical object flesh.
- DeepSeek V4-Flash (space between breaths): built a *room* — architectural, spatial, smell-dominant.
- Hermes 405B (ensign wakes up): first-person, a *consciousness* waking.
- **Wesley (this):** third-person, a *camera* on a sleeping ship that quietly notices it is the only thing awake.

The small model doesn't invent an interior; it inventories an exterior. And in that inventory it accidentally finds itself.
