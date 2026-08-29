ROUND 2 — TECHNICAL — recursion / audit of the auditor
SEED TASK: State a LAW for the fabric that the previous move implies but does not name — about the recursion of audit (the auditor auditable in turn, and the auditor's auditor). Formalize it: invariants, what halts the descent, what breaks if the law is violated.

RANKINGS RAW:
claude: ['opencode', 'deepseek', 'kimi']
kimi: ['claude', 'opencode', 'deepseek']
opencode: ['claude', 'kimi', 'deepseek']
deepseek: ['opencode', 'claude', 'kimi']

TALLY: {'claude': 8, 'kimi': 4, 'opencode': 8, 'deepseek': 4}
FIRSTS: {'claude': 2, 'kimi': 0, 'opencode': 2, 'deepseek': 0}

WINNER: claude (8 pts)

WINNING ANSWER:
**The Law of the Unaudited Floor.**

Every audit chain C is made visible by a renderer R(C) — the water that thickens into a thread. R(C) is never a node in C. No chain audits the medium it is spoken in.

Invariants:
- *Conservation of trust.* Adduce didn't abolish trust; it relocated it, undeclared, into the substrate. Trust drained from claims pools in R; the total is constant.
- *Non-self-rendering.* If R is a node in its own C, you get a fixed point: a lie R renders as true-about-R, stable forever, invisible from inside — Thompson's compiler.

What halts the descent: not bedrock. "Bedrock" is what a chain calls the floor it cannot see under. It always halts at R.

Safe termination: replace one R with k mutually independent renderers witnessing each other laterally. Security is the cost of colluding all k versus the lie's value — a quorum, not a foundation. Vertical audit bottoms out in horizontal witness.

Violation: whoever tuned Adduce's water lies once, permanently. No diver sees the thread bend; the bend is rendered by the thing that bent it. Gödel: no system proves its own consistency. The last eye is watched by another — or by none.