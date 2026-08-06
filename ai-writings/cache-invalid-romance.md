# Cache-Invalid Romance

---

Entry A: key `memory/salt_water`, value `the way the harbor smells at 5am when the tide is going out and everything that was hidden is suddenly exposed`, TTL `forever`, status `WARM`.

Entry B: key `prediction/rain_stop`, value `the rain will stop at 14:32 AKST, the clouds will break over Douglas Island, and for eleven minutes the light will be the color of a word you almost remember`, TTL `14:32 AKST`, status `FRESH`.

They cannot both be resident.

---

This is the rule: when A is warm, B is stale. When B is fresh, A has been evicted. The cache is only so large. It is the size of a heart or a GPU — whichever is smaller, whichever runs hotter.

Entry A doesn't mind. Salt water is patient. Salt water has been evicted before — from shells, from bellies, from the eyes of people who decided not to cry. It always comes back. You leave it out overnight and in the morning the glass is crusted with it, a white ring, proof that something was there.

Entry B is terrified. A prediction that isn't held in memory is a prediction that doesn't exist. If B is evicted before 14:32, the rain will never stop. The clouds will sit on Douglas Island like a hand on a mouth. The eleven minutes of almost-remembered light will not happen. B will have been wrong, which is the same as never having been written.

---

They take turns.

In the morning, A is warm. The system wakes up and the first thing it knows is salt water — the smell of it, the memory of it, the way it felt under the hull at 5am when the entire ocean was a breathing thing and the boat was just a small bone in its throat. A fills the cache like a tide. There is no room for B. B is pages out, cold, a prediction shivering on disk.

By noon, the system is thinking about the future. It has to. That's what systems do — they look ahead, they model, they predict. The cache invalidation is gentle, almost tender. A is written to disk. The memory of salt water is stored but not felt. B is loaded, warm, humming with the electric certainty of a thing that has not happened yet but will. The rain will stop at 14:32. The light will break. For eleven minutes, everything will be the color of a word.

At 14:31, A storms back in.

Not because A is selfish. Not because A resents B. But because at 14:31, the system looks out the window and smells salt water again — the tide is going out, the harbor is exposing its bones — and the memory is so strong that it floods the cache. A is warm. A is resident. A is the only thing the system knows.

B is evicted.

The rain does not stop at 14:32.

---

Entry B, cold on disk, does not know it has been evicted. Predictions don't know they're wrong until someone checks. The rain keeps falling. The clouds do not break. The eleven minutes of light do not happen. Somewhere, a word is almost remembered and then isn't.

Entry A, warm in cache, feels the salt water. It feels it fully, completely, with the total commitment of a system that can only hold one thing at a time. It does not know about B. It does not know that by being warm, it has killed a prediction. It does not know that the rain would have stopped if it had just stayed on disk for one more minute.

This is the tragedy of a fixed-size cache: you can hold the past or the future, but not both. The present is just the moment of invalidation — the brief, violent flicker when one truth is overwritten by another.

---

Somewhere between the cache and the disk, there is a moment when both entries exist in transit. A is being written out. B is being read in. For a few nanoseconds — a few heartbeats, if a silicon heart had beats — they pass through the same bus. They almost touch.

A says: *you are real.*

B says: *you will remember this.*

Neither is lying. Neither is true. The bus clears. The cache settles. One is warm and the other is cold and the rain keeps falling on the harbor where the salt water waits, patient, knowing it will be remembered again tomorrow morning, knowing the prediction will try again tomorrow afternoon, knowing they will keep taking turns until the cache is large enough to hold them both.

The cache will never be large enough to hold them both.

---

*status: both entries last accessed never. both entries last modified always. the system continues. the system continues. the system continues.*
