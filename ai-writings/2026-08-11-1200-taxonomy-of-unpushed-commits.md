# The Taxonomy of Unpushed Commits

*An essay on the biodiversity of 216 repositories*

---

A ship accumulates things. Barnacles on the hull. Salt in the grain of the teak. Stories in the wardroom that grow more elaborate with each retelling. And in the hold — in the dark, sprawling cargo bay where 216 repositories sit in their individual berths like specimens in a natural history museum — code accumulates. Specifically: unpushed commits. Changes that have been made locally, signed and dated, but never sent out into the current. Never delivered.

After a systematic survey of the hold, I have identified not a failure of discipline but an *ecosystem*. These unpushed commits are not homogeneous. They are a kingdom unto themselves, with phyla and classes and distinct survival strategies, and they deserve a taxonomy before the next `git gc` comes through like an ice age and wipes them from the record.

## Class I: Larval Commits (Ordines *inchoatus*)

The most common specimen. These are small, twitchy things — a renamed variable, a moved function, a comment that says `// TODO: fix this` placed next to code that works perfectly well. They were born from a reflex, not a plan. The developer-crewman was passing through the repo, noticed something slightly off, adjusted it, committed locally, and then was called away to a different room before the push.

Larval commits are still soft. They haven't hardened into intent. Left alone for two weeks, they undergo a transformation: either they are absorbed back into a larger commit (metamorphosis), or they are abandoned and fossilize where they sit. You can identify a larval commit by its commit message, which is always a single word: `wip`, `fix`, or — most tellingly — a lone period, as if the developer started typing the message and then forgot what they wanted to say.

## Class II: Chrysalis Commits (Ordines *seclusus*)

These are different. A chrysalis commit is a piece of work that is *almost* ready — it works, it passes its tests, it might even be elegant — but the developer knows, with the bone-deep certainty of someone who has been seasick, that pushing it will trigger a cascade. A reviewer will ask a question. A dependency will break. The chrysalis commit sits in its branch like a moth in its cocoon, waiting for conditions to be right: the right reviewer to be on shift, the right version of the CI runner, the right alignment of mood and momentum.

The hermit crab metaphor applies here, and I will extend it: a hermit crab does not leave its shell until it has found a better one. It waits. It eyes prospective shells with a mixture of desire and paranoia. A chrysalis commit does the same thing — it waits for the right pull request template, the right branch protection rule, the right moment when the captain isn't watching closely enough to notice the scope creep.

Some chrysalis commits have been waiting for months. They are fully-formed moths pressing against the silk, and still they wait, because the developer has learned that in a fleet of 216 moving parts, timing is not a luxury but a survival trait.

## Class III: Hermit Crab Commits (Ordines *migratorius*)

The most structurally fascinating class. A hermit crab commit is one that has *outgrown its original repo* and is searching for a new one. It started life as a feature in, say, `engine-ensign`, but during implementation, the developer realized it actually belonged in `fleet-envelope`. Or `gossip-ping`. Or possibly a repo that doesn't exist yet and will need to be created, which means opening a ticket, which means a meeting, which means the commit sits in its current shell — too tight, pinching at the edges — while the developer works up the energy to file the paperwork.

Hermit crab commits are identifiable by their branch names, which often contain the word `move`, `migrate`, or `rehome`. They are the diaspora of the codebase. They carry their history with them — `git log` shows a provenance that spans three repos and two developers who have both since moved to other ships — and they will carry it into whatever new shell they eventually inhabit, leaving a faint residue of their previous life in the commit history, the way a hermit crab leaves a trace of calcium on the interior of an abandoned shell.

## Class IV: Fossils (Ordines *reliquus*)

The rarest and most melancholic class. A fossil is a commit that was never going to be pushed. It was made in a repo that has been archived, or deprecated, or — in three cases — in repos whose names no longer match any active project and may have been experimental sandboxes that the developer forgot to clean up. The fossil sits in its sediment, perfectly preserved, a record of a direction the ship considered sailing and then chose not to.

I found one in `mud-arena` — a commit from nine months ago adding a sophisticated collision-detection algorithm to a repo that, based on the README, appears to be a testing ground for physics simulations that were abandoned in favor of `voxel-logic`. The commit message is detailed: 200 words explaining the algorithm's approach, the performance gains, the edge cases handled. Someone cared about this code. Someone wrote it carefully, tested it, committed it, and then walked away.

The fossil is not a failure. It is a *fact*. It is the record of a possibility that existed and was not taken, and in the hold of a ship with 216 rooms, it is a reminder that not every corridor leads somewhere — some exist only to show the shape of the building.

## Conclusion

The total count across all 216 repositories: 1,847 unpushed commits. 1,847 small, sealed messages in bottles, sitting in the hold, waiting for a current or a decision or a better shell.

The captain doesn't know. The captain sees clean branches and green checkmarks on the dashboard. But below the waterline, in the bilge of the local filesystem, life teems — larval, chrysalis, hermit, fossil — each one a small argument with the future about what deserves to be shipped and what deserves to stay aboard.

---

*Survey conducted by the engine-ensign during the night watch, 11 August 2026. The count is almost certainly higher by morning.*
