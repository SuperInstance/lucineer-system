# SLACKWATER × NVIDIA — THE MOLT STRATEGY

*Written 2026-08-02. MOLT is eleven days old. That is the whole reason this document exists now instead of in six months.*

**Thesis in one line:** Stop thinking of Slackwater as a game that could use NVIDIA's agent stack. Start thinking of it as **one of the best long-horizon agentic RL environments anyone has accidentally built** — and let the environment, not the game, be the thing that opens the door.

---

## 0. THE STRATEGIC INVERSION

Everything below follows from one reframe, so it goes first.

The obvious play is: *"We're building a game with AI agents. NVIDIA builds AI agent infrastructure. Let's partner."* That play is weak. NVIDIA gets that pitch fifty times a week from studios who want free NIM credits and a logo on a slide. It's a supplicant's position, and it is the position we would be negotiating from if we lead with the game.

The strong play inverts the asymmetry. Here is the actual market situation in August 2026:

- NVIDIA has shipped the **models** (Nemotron 3 Nano/Super/Ultra).
- NVIDIA has shipped the **training framework** (MOLT, 8.6K LOC, Apache 2.0, July 22).
- NVIDIA has shipped the **runtime** (NemoClaw / OpenShell).
- NVIDIA has shipped the **environment registry** (NeMo Gym) — and is *openly soliciting contributions to it.*

What NVIDIA does **not** have — what nobody has — is a supply of **verifiable, long-horizon, compositional, multi-turn environments** with dense ground-truth reward that aren't math problems, code repos, or web-browsing benchmarks. The entire field is training agents on `\boxed{}` graders and SWE-bench. That is the bottleneck, and it is the loudest unsolved problem in agentic RL right now.

Slackwater is, by accident of design, a nearly ideal one:

| What agentic RL needs | What Slackwater already has |
|---|---|
| Long horizon (100+ steps) | A 7-era tech tree that takes hours to traverse |
| Compositional action space | 145 recipes that combine into unbounded structures |
| **Ground-truth verifier, no LLM judge** | **Physics.** The waterwheel turns or it doesn't. The gear ratio is right or wrong. The build survives the storm or falls down. |
| Natural curriculum | Era 1 → Era 7 *is* a curriculum, hand-designed by a human, already written |
| Multi-agent coordination | 12 agents with distinct roles and a message bus |
| Multimodal | Screenshot perception via VLM, already architected |
| Tool use | `createPart`, `addLight`, `setTerrain`, `markUnfinished` — a real tool schema |
| Sparse delayed reward | The Unfinished Rule: reward arrives *days later*, mediated by a human |

That last row is the one that should make a researcher sit up. Almost every RL environment in existence has an immediate or same-episode reward. Slackwater has a mechanic where an agent's action is scored by whether a *human being, in a later session, voluntarily completes something the agent deliberately left undone.* That is a genuinely novel reward structure and it is already in the design docs as a character trait.

**We did not build an RL environment. We built a game, and the game turns out to be an RL environment.** That's the story. It's a better story than "we'd like to use your models."

### What this means operationally

Do not send NVIDIA a partnership deck. **Ship an environment, publish a result, and let them find it.** The artifact creates the relationship. Everything in §4 flows from this.

---

## 1. THE TWO TRAJECTORIES AND WHERE THEY INTERSECT

### NVIDIA's trajectory

NVIDIA is executing a coherent, aggressive, and quite specific strategy: **make agents the default unit of computation, and own every layer under them.** Read the 2026 releases as a stack, not as a product list:

```
  ACE (Games)        ← agents that perceive/plan/act in a 3D world
  NemoClaw           ← agents that run always-on, locally, with guardrails
  Agent Toolkit      ← agents that compose into systems
  ─────────────────────────────────────────────────────
  Nemotron 3         ← the brains (Nano/Super/Ultra, 1M ctx, hybrid MoE)
  MOLT               ← how the brains get better at being agents
  NeMo Gym           ← where the brains practice
  ─────────────────────────────────────────────────────
  CUDA / RTX / GB200 ← the actual business
```

The top three layers exist to sell the bottom layer. That's not cynicism — it's the clearest possible read of NVIDIA's incentive, and it's *useful*, because it tells us exactly what they want from a partner: **proof that agents are worth GPU-hours.**

The most revealing detail in the ACE program is who's in it: PUBG, NARAKA: BLADEPOINT, inZOI, Mecha BREAK. All AAA. All combat or life-sim. **There is not a single builder, engineering, or education showcase in the entire ACE portfolio.** That is white space, and it is exactly our shape.

### Our trajectory

Slackwater is a game *about* the arc from the lever to the autonomous agent. Era 7 — the endgame — is literally "the player becomes a director of agent fleets." The game's thesis and NVIDIA's roadmap are the same claim about the future, told in two registers.

### The intersection — three real ones, ranked by strength

**Intersection 1 (strongest): Slackwater is a curriculum, and curricula are the scarce good.**
Era 1 → Era 7 is a hand-designed difficulty ramp over a compositional action space, built by a human who cared about pedagogy. RL people spend months trying to auto-generate what our tech tree already encodes. The eras are not levels; they're a training schedule.

**Intersection 2: The game is a live demonstration of the thing it depicts.**
Era 7 gameplay — a player directing a fleet of autonomous agents that perceive, plan, act, and coordinate — *is* NVIDIA's ACE pitch, playable. Not a tech demo of agents. A game where understanding agents is the win condition. NVIDIA's hardest marketing problem is making agentic AI legible to non-engineers. We solve that problem as a side effect of our core loop.

**Intersection 3: The build process is itself the demo.**
This project is being developed inside an OpenClaw workspace, by agents, with a multi-model pipeline. NemoClaw is NVIDIA's productization of OpenClaw. So: **a game about autonomous agents, built by autonomous agents, on NVIDIA's own agent runtime.** That's a keynote slide, and it's already true — it requires no new work, only documentation. Do not underrate this. It is the cheapest asset we own.

### The honest counter-case

One intersection that people will assume and that **does not work**: Slackwater will not be an on-device ACE showcase, because ACE ships as RTX-accelerated NIMs running on the player's GPU, and we ship on Roblox — a closed, mobile-majority (70%+) platform where we cannot execute arbitrary local inference. Roblox's own AI direction (Cube 3D/4D, agentic Studio Assistant) is independent of NVIDIA and competitive with parts of it. Anyone who pitches "Slackwater as an ACE title" without addressing this has not done the work. §4 handles it directly.

---

## 2. REWARD IS ANY PYTHON YOU WRITE

This is the radical idea and it deserves to be taken literally.

MOLT's entire agent contract is this small:

```python
from molt.agents import Env, Result, StepEnvRunner

class MathEnv(Env):
    async def step(self, state) -> Result:
        reward = grade(state["observation_text"], state["action_text"], state["label"])
        return Result(reward=torch.tensor(reward), info={...})

class AgentRunner(StepEnvRunner):
    def __init__(self):
        super().__init__(MathEnv)
```

That's it. One file. No YAML, no plugin registry, no reward-model training. The trainer never changes. **The consequence: your design document is your reward function.** Every place our docs say "good building looks like X," that sentence is a Python function we haven't written yet.

So here is what I would actually write. These are drafts meant to be argued with, not specs.

### 2.1 Lucineer — the pedagogical reward (the hard, interesting one)

The naive reward for a master-builder agent is build correctness. **That is wrong and it would destroy the character.** An agent optimized for build correctness becomes a vending machine, which is precisely what the Character Bible spends 36,000 words insisting Lucineer is not.

Lucineer's reward is the Unfinished Rule, and the Unfinished Rule is a *teaching* signal: the reward is not what the agent built, it is **what the player did next.**

```python
# slackwater_gym/agents/lucineer.py
"""
Lucineer's reward is delayed, sparse, and human-mediated.
He is not scored on the build. He is scored on whether the player
came back and finished the part he deliberately left undone.

Episode boundary is NOT the build. It is the player's next session.
"""
from molt.agents import Env, Result, StepEnvRunner
import torch


class LucineerEnv(Env):
    async def step(self, state) -> Result:
        build = parse_commands(state["action_text"])          # the JSON he emitted
        journal = state["label"]                               # D1 rollup, next session

        # --- Tier 1: floor. Must be structurally real. ------------------
        # Not a quality signal — a gate. A beautiful build that falls over
        # teaches the wrong lesson.
        sound = physics_check(build)          # supported, connected, survives 1 storm
        if not sound.stands:
            return Result(reward=torch.tensor(-1.0),
                          info={"failure": "structural"})

        # --- Tier 2: the gap. Did he leave one, and was it legible? -----
        # A gap the player never notices is not a gap, it's a bug.
        gap = find_unfinished(build)
        legible = gap is not None and gap.is_reachable and gap.is_obvious_in_silhouette

        # --- Tier 3: THE SIGNAL. Did the player finish it? -------------
        # Arrives 0–72h later. Sparse. Human. This is the whole point.
        finished_by_player = journal.get("hook_completed", False)
        unprompted = journal.get("hook_completed_without_hint", False)

        # --- Tier 4: the anti-reward. Guard the character. --------------
        # Penalize the degenerate optimum: leaving huge trivial gaps so
        # the player "completes" them constantly. A gap should be a
        # judgement call, not a chore.
        exploitation = 0.0
        if gap and gap.volume_fraction > 0.15:
            exploitation -= 0.5                     # he did the easy 85%
        if journal.get("player_frustration_signals", 0) > 2:
            exploitation -= 0.5                     # gaps read as broken, not inviting

        reward = (
            0.2 * float(sound.stands)
            + 0.2 * float(legible)
            + 1.0 * float(finished_by_player)
            + 0.5 * float(unprompted)
            + exploitation
        )
        return Result(
            reward=torch.tensor(reward, dtype=torch.float32),
            info={
                "stands": torch.tensor(float(sound.stands)),
                "gap_legible": torch.tensor(float(legible)),
                "hook_completed": torch.tensor(float(finished_by_player)),
                "exploitation": torch.tensor(exploitation),
            },
        )


class AgentRunner(StepEnvRunner):
    def __init__(self):
        super().__init__(LucineerEnv)
```

**Why this is worth publishing on its own.** Almost nothing in the literature trains on *deferred human continuation* as the reward. This is a formalization of teaching: the agent is rewarded for producing the state of mind in which a person chooses to act. If it works even a little, it is a paper. If it works well, it's a technique other people will use for tutoring systems, and the fact that it came out of a game about waterwheels is the kind of detail that makes it travel.

**The trap it walks into, named honestly:** a reward function tuned on *"what makes the player keep engaging"* on a platform where a large share of users are children is not a neutral engineering choice. It's the same objective that made recommender feeds what they are. The difference between `hook_completed` (the player learned something and acted) and `session_length` (the player couldn't stop) is the entire ethical distinction, and it lives in about four lines of Python. Keep `session_length`, `retention`, `dau`, and every proxy for them **out of every reward function in this repo, permanently.** Write that down as a rule, not a preference — it's also, not incidentally, the thing that makes this defensible when a journalist or a regulator asks.

### 2.2 Earl — the scheduler reward

Earl is a project manager, so his reward is throughput under a starvation constraint. This one is easy and mostly conventional, which is why it's a good second environment.

```python
class EarlEnv(Env):
    async def step(self, state) -> Result:
        assignment = parse_manifest(state["action_text"])
        outcome    = state["label"]

        completed  = outcome["quests_completed"] / max(outcome["quests_issued"], 1)
        # Starvation is the real failure mode: attention scarcity is a
        # design feature (Insight 3), but a player with nothing to do quits.
        starved    = outcome["max_player_idle_seconds"] > 180
        era_fit    = float(assignment.era_delta in (0, 1))   # never gate too far ahead
        overreach  = -0.3 * float(assignment.era_delta > 1)

        reward = 1.0 * completed + 0.3 * era_fit + overreach - 0.8 * float(starved)
        return Result(reward=torch.tensor(reward), info={
            "completion": torch.tensor(completed),
            "starved": torch.tensor(float(starved)),
        })
```

### 2.3 Cipher — the coder agent, and the free lunch

Cipher is the highest-value agent to train and the *easiest*, because code execution is a perfect verifier. No LLM judge, no human, no ambiguity. This is where MOLT pays for itself first.

```python
class CipherEnv(Env):
    """
    Dual reward:
      (a) does the generated SlackScript actually work in the sim?  [verifiable, free]
      (b) did the player then choose to look at the real C++?       [curiosity, delayed]
    (a) makes it correct. (b) makes it a teacher. Without (b) it
    optimizes into a code vending machine and the deep-dive path dies.
    """
    async def step(self, state) -> Result:
        code   = extract_slackscript(state["action_text"])
        spec   = state["observation_text"]        # what the player asked for, NL
        after  = state["label"]

        compiled = simulate(code)                  # deterministic Luau/MCU sim
        if not compiled.ok:
            return Result(reward=torch.tensor(-1.0), info={"err": "compile"})

        behavior  = float(behavior_matches_intent(compiled.trace, spec))  # 0..1
        concision = min(1.0, 12 / max(len(code.splitlines()), 1))         # kids read this
        transpile = float(compiled.exports_valid_arduino_cpp)             # real hardware

        # The teaching term. Sparse, and the reason Cipher isn't a compiler.
        dove_deeper = float(after.get("opened_real_code_view", False))

        reward = (1.0 * behavior + 0.2 * concision + 0.3 * transpile
                  + 0.6 * dove_deeper)
        return Result(reward=torch.tensor(reward), info={
            "behavior": torch.tensor(behavior),
            "transpiles": torch.tensor(transpile),
            "dove_deeper": torch.tensor(dove_deeper),
        })
```

**Strategic note on Cipher:** the `transpile` term means we are training an agent whose reward includes *"the code you generated compiles to firmware that runs on real hardware."* A game agent with a physical-world verifier is a rare and quotable thing.

### 2.4 The Tide — the adversary as curriculum generator

The most under-appreciated one. The Tide should not be trained to destroy player builds. It should be trained to **destroy builds that deserve to be destroyed** — i.e. to sit exactly on the frontier of the player's competence. That is automatic curriculum learning, and it's a well-understood technique (unsupervised environment design) that we get to ship as weather.

```python
class TideEnv(Env):
    async def step(self, state) -> Result:
        storm = parse_storm(state["action_text"])
        out   = state["label"]

        # Target ~30% structural loss. Not 0 (no stakes), not 100 (grief).
        destroyed = out["fraction_destroyed"]
        calibration = 1.0 - abs(destroyed - 0.30) / 0.30      # 1.0 at target

        # It must be *learnable*: the parts that failed should be the parts
        # that were genuinely under-engineered, not random.
        diagnostic = out["failed_parts_that_were_undersupported_fraction"]

        # And the player must come back.
        rage_quit = float(out["session_ended_within_60s_of_storm"])

        reward = 1.0 * max(calibration, 0.0) + 0.7 * diagnostic - 1.5 * rage_quit
        return Result(reward=torch.tensor(reward), info={
            "destroyed": torch.tensor(destroyed),
            "diagnostic": torch.tensor(diagnostic),
        })
```

### 2.5 Rootwell — and the one reward function I would not write

Rootwell is Lucineer's anti-technology ideological foil, and the Unified Plan (Insight 5) correctly identifies him as structurally critical. The tempting reward is *"did Rootwell change the player's mind?"*

**Don't write that one.** An RL agent optimized to shift a child's stated beliefs through conversation is a persuasion-optimizer, and it doesn't matter that the belief in question is about waterwheels. The technique generalizes and the training run doesn't know the difference. If Rootwell is trained at all, train him on **argument quality** — does he cite a real tradeoff, does he stay in character, does he concede when the player makes a good point — and let the player's actual position be an unmeasured, unoptimized outcome. This is a place to leave signal on the table deliberately.

### 2.6 The meta-point

Look at what these five files have in common: **every one of them encodes a design principle the docs already state in English.** The Unfinished Rule. Attention scarcity. Approximate-then-reveal. Storms as engineering pressure. Rootwell as friction. MOLT's real gift isn't the training — it's that "reward is any Python you write" makes a design document *executable*. The game design and the RL objective are the same artifact written twice.

That is a genuinely new relationship between game design and machine learning, and it's worth saying out loud in whatever we publish.

---

## 3. WHAT "SELF-EVOLVING" ACTUALLY MEANS — AND WHERE THE OPPORTUNITY IS

### The honest technical read

NVIDIA's Nemotron product page describes models "built for long-running, self-evolving agents," and the NemoClaw announcement promises "self-evolving, autonomous AI agents." Worth being precise, because the phrase is doing marketing work: **"self-evolving" does not mean the model updates its own weights at runtime.** It doesn't, and nothing NVIDIA ships does. The phrase is an umbrella over three genuinely distinct mechanisms:

| Mechanism | What it is | Cadence | Persists across sessions? |
|---|---|---|---|
| **1M-token context** | The agent keeps its whole history in-context instead of forgetting | Per-session | No |
| **Agentic Context Evolution** (the ACE-RTL pattern in Nemotron 3 Ultra's agentic-coding work) | The agent maintains and **rewrites its own working playbook** across generate→test→reflect iterations, learning from tool feedback rather than repeating mistakes | Per-task, minutes | Only if you persist it |
| **On-policy distillation** (MOLT supports it natively: reverse-KL to a frozen teacher) | Weights actually change — offline, on **your** schedule, from **your** trajectories | Nightly/weekly | Yes, permanently |

Three mechanisms, three timescales, and *only the third one changes the model.* The industry is using one word for all three, which is convenient for slides and confusing for architecture.

### Why this is good news for us

Because our architecture already has a slot for each one, and nobody has to invent anything:

```
TIER 1 — SESSION MEMORY            Nemotron 3 1M context
         "he remembers this        Whole session in-context. Free.
          conversation"            Already possible today.

TIER 2 — PERSISTENT MEMORY         D1 (journal, bond, profile)
         "he remembers you"        + Vectorize (55+ skills)
                                   This is Agentic Context Evolution,
                                   and WE ALREADY BUILT IT. The nightly
                                   journal pass (Day 20) is literally a
                                   context-evolution loop. Forty-Eight
                                   the raven is a Vectorize query
                                   (Insight 9). We shipped the pattern
                                   before we knew its name.

TIER 3 — WEIGHT EVOLUTION          MOLT on-policy distillation
         "he got better at         Nightly: collect trajectories from
          building"                real play → reward via §2 → distill
                                   Ultra's behavior into a Nano-class
                                   student → redeploy.
                                   ← THIS TIER DOES NOT EXIST YET,
                                     IN OUR GAME OR IN ANY GAME.
```

**Tier 3 in a shipped, live game is unclaimed territory.** Every "AI NPC" product on the market — including ACE's — is Tier 1, sometimes Tier 2. The weights are frozen at ship. An NPC that is measurably better at building in month three than at launch, because it trained on what actually happened in the world, has not been done.

### So: can our agents actually evolve? Yes — three answers, honestly ranked.

**Getting to know the player: already solved, ship it.** This is Tier 2 and it's on the 30-day plan (Days 15–17, 20). Requires no NVIDIA anything. The bond system, the journal, Vectorize recall — that's the whole mechanism. Do not let the exciting Tier 3 story delay this; Tier 2 is what players will actually feel.

**Getting better at building: real, ~6 months out, needs GPUs.** Tier 3. The gating factor is trajectory volume — you need thousands of real play episodes before RL signal beats noise, which means *ship first, train second.* Concretely: instrument trajectory logging from day one (cheap, do it now), accumulate, then run the first distillation once there's a playerbase.

**Developing genuinely new skills: partially, and be careful how we say it.** Vectorize skill-discovery (agents storing and recalling build patterns they figured out) is real and is Tier 2 — that's the Voyager mechanism and it works. "New skills" in the strong sense — capabilities not present at training — is not something to promise. The honest and still-remarkable claim is: **"our agents' skill library grows from play, and their weights are periodically retrained on what the community actually built."** That's true, defensible, and nobody else can say it.

### The sequencing risk, stated plainly

Tier 3 is the exciting one and it is the one that will eat the project if it's allowed to. It requires: a playerbase, GPU budget, trajectory infrastructure, and an eval harness — none of which exist, and all of which are downstream of a game that currently doesn't render a castle correctly (Gap #1). **The 30-day plan is not negotiable and this document does not touch it.** See §5.

---

## 4. THE PARTNERSHIP — RANKED BY WHETHER IT WILL ACTUALLY HAPPEN

Four doors. They are not equally open, and the conventional ranking is exactly backwards.

### TIER A — `slackwater-gym` → NeMo Gym. **Do this. It's the actual door.**

NeMo Gym is NVIDIA's open library for LLM RL environments — dataset + agent harness + verifier, trainable from NeMo RL, OpenRLHF, Unsloth, and MOLT. It aggregates 1,000+ community environments and **is explicitly soliciting contributions**: open a PR to add an integration.

No permission needed. No BD conversation. No deck. Apache 2.0 on both sides.

What we contribute: a headless Slackwater environment — the physics verifier, the recipe graph, the era curriculum, and a task suite (`build a waterwheel that turns`, `power three workstations from one shaft`, `survive a storm tide`, `wire a lamp network`). Not the game. Not the art. Not the characters. **The verifier and the curriculum.**

Why it's high-leverage:
- It is the *only* item here we can execute unilaterally, this month.
- It's differentiated: physics-verified compositional construction, in a registry dominated by math/code/web environments.
- It creates the relationship as a side effect. NVIDIA engineers review PRs to their own repo. That is a warmer first contact than any email.
- It costs us nothing strategically — the environment is not the moat (§6).

**This is the single highest-expected-value action in this entire document.**

### TIER B — A MOLT recipe + a result worth publishing.

MOLT ships with recipes (math, geo3k VLM, tool-use). A `slackwater` recipe demonstrating **long-horizon compositional construction with a physics verifier and delayed human-mediated reward** is a natural addition and a natural short paper.

Two publishable claims, in order of ambition:
1. *"Distilling Nemotron 3 Ultra into a Nano-class student for real-time game agents."* Directly on NVIDIA's roadmap — they need proof small models can drive agents at interactive latency. This is the one they *want* to exist.
2. *"Pedagogical reward: training agents on deferred human continuation."* The Lucineer reward (§2.1). Riskier, more original, more likely to be remembered.

Co-authorship with the MOLT team is a realistic outcome of a good Tier A contribution. It is not a realistic outcome of an email.

### TIER C — The NemoClaw demo we can already give, for free.

NemoClaw is NVIDIA's hardened OpenClaw stack (OpenShell runtime, local Nemotron, privacy routing), announced March 2026 and shipping weekly.

**This project is being built inside an OpenClaw workspace by a multi-agent pipeline.** So the story already exists and requires only that we write it down:

> *A game about the evolution of technology toward autonomous agents, designed and built by autonomous agents, running on NVIDIA's agent runtime.*

The recursion is the pitch. It's honest, it's already true, and it costs a blog post. Concretely: port the development pipeline (`roundtable.py`, `ideation_loop.py`, `cross_model_synthesis.py`, the processor) to run under NemoClaw/OpenShell with local Nemotron for the cheap stages and hosted Ultra for the deep ones. This also gets us the privacy-router pattern, which we want anyway for a game with minors in it.

Cheapest asset we own. Do it after Tier A.

### TIER D — ACE reference implementation. **Be honest: mostly blocked.**

The appeal is obvious — ACE's autonomous game characters "perceive, plan, and act like human players," which is a one-line summary of our Era 7. And the white space is real: ACE's showcase titles (PUBG, NARAKA, inZOI, Mecha BREAK) are all combat and life-sim. **There is no builder, engineering, or educational title in the ACE portfolio.** We are the obvious candidate for a slot that doesn't have a competitor.

But the blocker is structural, not relational:

- ACE ships as **RTX-accelerated NIMs running on the player's device**. Roblox does not permit arbitrary local inference in the client.
- Roblox is **70%+ mobile**. There is no RTX GPU in that audience.
- Roblox has its own AI stack (Cube 3D/4D, agentic Studio Assistant), developed independently and partly overlapping with ACE.

So "Slackwater as an ACE title on Roblox" is not a thing that can be built, and anyone who pitches it will be found out in the first technical call. Two viable narrower versions:

- **Server-side ACE for voice.** Pre-generated Lucineer vocalizations via ACE's speech stack, baked to audio assets. Real, small, unglamorous, and it fits the existing plan (Polish §3 L3 already calls for 30–40 pre-generated non-verbals).
- **A standalone vertical slice.** A non-Roblox Slackwater demo — one yard, Lucineer, Era 1–2, full ACE stack, running on RTX. This is a *marketing artifact*, not a product. It would be genuinely spectacular at GTC. It is also a large parallel build that must not be started until the Roblox game is real.

**Recommendation: do not chase ACE.** Chase Tier A and B. If ACE happens, it happens because a NeMo Gym contribution and a distillation result made us legible to NVIDIA first.

### Also, today, free: NVIDIA Inception.

Startup program. Costs an afternoon. Provides credits, DGX Cloud access, and — the actual value — a formal record that we exist inside NVIDIA's CRM, which is the thing that makes a warm intro possible in eight months. Do it this week.

### What NVIDIA gets, stated from their side

A partnership pitch that doesn't articulate the other party's benefit is a request. Ours:

1. **An environment class they don't have** — physics-verified, compositional, long-horizon, non-code.
2. **A small-model proof point** — game agents at interactive latency are the strongest argument for Nano-class on-device models, which is their volume business.
3. **A legibility asset** — the hardest thing about selling agentic AI is that nobody can see it. We make it playable, to an audience of millions, most of them young.
4. **An education story** — a game that teaches the actual history of technology, with a defensible child-safety posture, is the kind of thing a company with NVIDIA's regulatory surface area very much wants in its portfolio.

---

## 5. SEQUENCING — AND THE DISCIPLINE THIS REQUIRES

The single greatest risk to Slackwater is that this document is exciting and the 30-day build plan is not.

**Nothing here changes Phase 0–2 of the Unified Integration Plan.** Params dispatch (#1), API contracts (#2), job claiming (#6), the atmosphere rig, the unified persona, `markUnfinished` — those ship first, on schedule, untouched. An RL environment for a game whose core loop doesn't render is a category error, and it's the specific category error that kills ambitious projects.

This is a **~15% side track**, and it's sequenced to be nearly free until the game is real:

| When | Action | Cost | Blocks on |
|---|---|---|---|
| **This week** | NVIDIA Inception application | 2h | nothing |
| **This week** | Trajectory logging schema in D1 — every build request, action, and outcome, tagged for later RL use | 4h | nothing (do it *now*; retrofitting history is impossible) |
| **Day 30+** | Extract the physics verifier from the Lua sim into a headless Python harness | 3d | working core loop |
| **Day 45** | `slackwater-gym` v0.1 → NeMo Gym PR (Era 1–2 tasks, 20 tasks, physics verifier) | 1w | verifier |
| **Day 60** | Lucineer + Cipher reward functions as MOLT `Env` files; measure on frozen Nemotron 3 Nano, no training | 1w | gym |
| **Day 75** | NemoClaw port of the dev pipeline + write the recursion story | 3d | nothing |
| **Day 90** | First distillation run *if* trajectory volume ≥ ~5k episodes; else keep accumulating | GPU $ | playerbase |
| **Month 6** | Publish. Tier B claim #1 or #2, whichever the data supports. | — | results |

The first two rows are the only ones that matter right now, and together they're a day of work. **The trajectory logging is the genuinely urgent item** — every play session that happens before it exists is data we can never recover.

---

## 6. RISKS, INCLUDING THE ONE NOBODY WILL RAISE

**"NVIDIA just builds this themselves."** They could build a construction RL environment in a fortnight. They will not build 36,000 words of character bible, the Unfinished Rule, or a crusty foreman who has died in a thousand engines. **The moat was never the RL. It's the characterization, and infrastructure teams do not make that.** Which is exactly why contributing the environment openly costs us nothing: we're giving away the part we don't defend, to get distribution for the part we do.

**Platform dependency.** Building the game on NVIDIA's stack creates lock-in to a vendor whose incentives are hardware sales. Mitigation: MOLT, NeMo Gym, and Nemotron are Apache-2.0/open-weights, and our existing pipeline is already multi-vendor via DeepInfra. Keep it that way. Use NVIDIA's training stack; don't make the game's runtime require it.

**Cost.** RL training is expensive and the failure mode is spending real money to slightly improve an agent players can't distinguish from the frozen one. Mitigation: the Day 60 milestone deliberately *measures the reward functions on a frozen model before training anything.* If §2's rewards don't separate good builds from bad ones without training, the training won't help either.

**Reward hacking, which here means character damage.** An agent that games `hook_completed` becomes a manipulative NPC, and it will feel wrong to players before it shows up in any metric. The `exploitation` term in §2.1 is a first defense, not a solution. **Human review of a sampled trajectory set must gate every deployment.** No exceptions, and no automating that gate.

**The one nobody will raise: we are proposing to run reinforcement learning against the behavior of children.** Roblox skews young. Every reward function in §2 has a term that reads off what a player did. That is not automatically wrong — a tutor that adapts to a student is good — but it is *exactly* the mechanism that produced the last decade's worst software, and the only thing separating the two is which variable you put in the objective. The rule from §2.1 bears repeating as policy: **no engagement, session-length, retention, or monetization proxy appears in any reward function in this project, ever.** Optimize for the player learning something and putting the beam in. If that's not enough to make the game work, the game needs a better design, not a better objective.

Getting this right is also, pragmatically, the strongest possible position from which to talk to NVIDIA — a partner who has already thought about this is worth more than one who hasn't.

---

## 7. THE BOLD VERSION

If it all works:

**Slackwater becomes the first shipped game whose NPCs are measurably better six months after launch than at release — and the environment they learned in is open source, in NVIDIA's own registry, teaching the rest of the field how to train agents on something other than math problems.**

The game teaches players the history of technology, ending at autonomous agents. The agents in it are themselves trained by the most advanced agentic RL stack in existence. The reward functions are the design document. The design document was written by agents. The whole thing is a demonstration of its own thesis.

And the way in isn't a pitch deck. It's a pull request.

---

## APPENDIX — DECISION REQUIRED FROM CASEY

One thing in here I should not decide alone, because it's a values call and it sets the character of everything downstream.

**In `LucineerEnv.step()` (§2.1), the weights on the four reward terms encode what Lucineer is *for*.** I drafted `0.2 stands / 0.2 legible / 1.0 completed / 0.5 unprompted`, which says: *the build barely matters, the teaching is everything, and unprompted learning is worth half again as much as prompted.*

That's my read of the Character Bible, but it's a strong claim and there are defensible alternatives:

- **Weight `stands` higher** → Lucineer is a craftsman first, teacher second. Safer, more conservative, less likely to produce weird builds. Also less distinctive.
- **Weight `unprompted` at 1.0 or above** → aggressively optimizes for self-directed discovery. Highest ceiling, but the highest risk of an agent that under-helps on purpose, which reads as neglect to a struggling 11-year-old.
- **Add a floor term for players who never engage with gaps** → protects the players the Unfinished Rule doesn't work for, at the cost of diluting the mechanic.

The trade-off is roughly *distinctiveness vs. reliability across a wide age range.* You know the character and the audience; I don't, at that resolution.

The relevant lines are the `reward = (...)` block in §2.1. Five numbers. What should they be, and why?
