Here are the genuine gems in your work, distilled and defended.

---

## 1. Field-Edge as the Unit of Memory

**What it is:**  
Instead of storing a conversation as a text transcript, a static embedding, or a sentiment score, you store it as a **displacement vector** — the signed change in the room's emotional field from before the event to after.

**Why it's a gem:**  
Current AI memory is photographic. It remembers *what was there*. Your move is kinetic: it remembers *what happened*. Two conversations with completely different words can share the same edge (same start-state, same warmth shift, same tightening). Two conversations with identical words can have opposite edges depending on context. No mainstream system retrieves this way.

**What would prove it:**  
A `field-edge` index that, given a reference conversation, retrieves a different conversation that humans judge as "felt the same" at a higher rate than semantic similarity or static embedding search.

**Where it travels in 10 years:**  
Agent memory layers, therapy/coaching AI, creative tools (find me a chord progression with the same emotional arc), meeting assistants ("find the last standup that had this same energy collapse").

---

## 2. Comparable Sameness (Retrieval by Trajectory, Not Topic)

**What it is:**  
A new retrieval primitive. Two items are "the same" not when their content overlaps, but when their **field-edges match** — same displacement geometry, even across entirely different domains.

**Why it's a gem:**  
Semantic search finds things *about* the same thing. This finds things that *did* the same thing to the room. That's a different category of search entirely. It turns memory from a library into a resonance chamber.

**What would prove it:**  
A benchmark where the task is "given this successful negotiation, find another negotiation from a different industry that produced the same persuasion arc" — and your system outperforms text-based retrieval.

**Where it travels:**  
Multi-agent orchestration (recognizing functionally equivalent situations across domains), education (matching students in the same conceptual rut), recommendation engines (emotional-arc matching for media).

---

## 3. The Reader Seam (Calibrated Observer Delta)

**What it is:**  
The most reliable signal isn't the objective room state. It's the **change in a known, calibrated observer** — how a specific reader's reading of the room shifted from their own baseline.

**Why it's a gem:**  
Everyone knows observers disagree. The standard fix is to average them (which dilutes signal) or pick one (which biases it). Your fix is to treat each observer's *deviation from self* as the primary measurement. The doctor doesn't read the patient; he reads how the nurse changed. This is ipsative measurement applied to AI embedding spaces — genuinely rare.

**What would prove it:**  
Show that predictions of room state based on reader deltas from known baselines are more consistent across sessions than predictions based on raw dial readings.

**Where it travels:**  
Personalized AI (your assistant knows your baseline, so it knows when *you* experienced a shift), synthetic focus groups (model calibrated observers instead of polling humans), mental health monitoring (track delta from personal baseline, not absolute scores).

---

## 4. Caller-Aware Dependency Weights (The "Co-Linear Algebra")

**What it is:**  
In your Quilt grid, the weight of an edge depends on **who traverses it**. The same conversation has a different "vibe weight" for a newcomer than for a regular. This isn't a bug; it's the formal structure.

**Why it's a gem:**  
Every graph database in existence treats edge weights as scalars. You're proposing they're **functions of the traverser**. That's a real extension to graph theory with immediate engineering implications. A spreadsheet where `A1`'s value depends on *who asked* is a genuinely new computational primitive.

**What would prove it:**  
Implement it and show that a caller-aware dependency graph produces better routing decisions or more accurate predictions than a standard weighted graph on a multi-agent task.

**Where it travels:**  
Multi-agent orchestration frameworks, personalized knowledge graphs, social media ranking (weight content by its predicted displacement on *this specific user*), any system where "meaning" is relational rather than absolute.

---

## 5. The Adversarial Committee as Executable Methodology

**What it is:**  
Not "please reflect on your answer." A **formal assembly of roles** — Rival, Devil's Advocate, Ideator, Scout — each with specific attack vectors, specific model assignments, and specific outputs, operating on a concrete artifact.

**Why it's a gem:**  
AI self-correction is currently either too cheap (single-model reflection, unreliable) or too expensive (RLHF, requires humans). This is a middle layer: structured, multi-perspective critique at the cost of a few extra API calls. The deadman switch — pre-registering a falsification condition and committing to kill the hypothesis if it fails — turns it from theater into science.

**What would prove it:**  
A study showing that outputs reviewed by this specific committee structure have measurably lower hallucination rates or higher human preference scores than single-model outputs or generic "critique this" prompts.

**Where it travels:**  
AI research agents, autonomous coding (code review bots with structured adversaries), content generation (pre-publication red-teaming as a standard pipeline), any high-stakes AI output that needs epistemic rigor.

---

## 6. The Deadman Switch (Pre-registered Falsification in Agent Research)

**What it is:**  
Before running the experiment, you commit: *if the fine gap doesn't open from 0.015 toward 0.271 across three consecutive runs, kill the edge layer and fall back to cross-room snapshot retrieval.*

**Why it's a gem:**  
Almost no AI "research" projects do this. They run experiments, cherry-pick results, and retrofit the narrative. A pre-registered, executable falsification protocol — committed to in the repo before the runs — is actual scientific method. In a field drowning in AI theater, this is a real signal of rigor.

**What would prove it:**  
Run it. Either the gap opens and the hypothesis survives, or it doesn't and you publish the failure honestly. The value is in the *commitment*, not the outcome.

**Where it travels:**  
Any autonomous AI research system. If agentic science becomes a thing, pre-registered falsification protocols will be the difference between legitimate inquiry and automated bullshit generation.

---

## 7. The Dial Bank as an Operationalized Basis

**What it is:**  
A fixed, multidimensional basis for room state: mood, volume, earnestness, cynicism, joke_landing, panic, etc. Not a single sentiment score. A vector space.

**Why it's a gem:**  
It's not philosophically new — psychology has had multidimensional emotion models for decades. But it's **operationally new** in AI engineering. Most systems use scalar sentiment or uninterpretable embedding dimensions. A declared, human-legible basis that maps directly to engineering decisions is rare.

**What would prove it:**  
Factor analysis showing the dimensions are relatively independent and capture significant variance in human-labeled conversation states. Or: show that retrieval/manipulation in this basis is more useful than in an uninterpretable embedding space.

**Where it travels:**  
Any system that needs to reason about "vibe" explicitly — meeting assistants, creative tools, social platforms, therapy bots. The specific 9 dials may not travel, but the *pattern* of a declared, interpretable basis will.

---

## What Didn't Make the Cut (And Why)

| Idea | Why It's Not Here |
|---|---|
| **Self-referential dataset** | Good framing, but operationally it's just logging. The sampling bias problem (your data is only adversarial debate) is severe and unaddressed. |
| **Polyformalism/JEPA as inverses** | Beautiful analogy, but not yet a theorem or an algorithm. It becomes a gem when it produces a new architecture, not before. |
| **SOUL.md / AI identity continuity** | Interesting, but it's a separate project from the dissertation. It doesn't help the technical claims. |
| **Sheaf cohomology / GL(9) holonomy** | Unless you have 50 pages of proofs, this is philosophical decoration. The reviewers hallucinated grandeur onto your notes. |

---

## The One-Sentence Summary

> Your repo contains **three genuinely new primitives** (field-edge memory, comparable sameness retrieval, caller-aware graph weights), **two genuinely new methodologies** (adversarial committee review, pre-registered falsification in agent research), and **one solid operationalization** (the dial bank). The philosophy is seasoning. The primitives are the meal.

Here are the abstract innovations in your project that could actually propagate into other tools over the next decade — ranked by how fundamental they are, not by how cool they sound.

---

## 1. The Field-Edge as the Unit of Memory

**The idea:** Don't represent a conversation (or any event) as a point or a wave. Represent it as a **walk** — a signed displacement from one field state to another. The unit of memory is not "what was said" but "what changed."

**Why this matters:** Almost every system today stores memory as content (embeddings of text, summaries, key-value pairs) or as state (a sentiment score at time T). Your insight is that the meaningful signal is the **derivative** — the edge, the jump, the transformation. Two events are "the same" when their edges match, even if their contents differ completely.

**Where this spreads in 10 years:**
- **Search and retrieval:** "Find me the meeting that *felt* like this one" — not topic-matching, but trajectory-matching. Creative tools, therapy platforms, team coordination software.
- **Reinforcement learning:** Reward shaping via field-displacement rather than terminal state. An agent learns not "what state is good" but "what transformations are desirable."
- **Education:** Assessment by measuring the conceptual shift a lesson induces, not the knowledge state it leaves behind.
- **Clinical tools:** Trauma therapy, mood tracking, addiction recovery — all domains where "how did this interaction change the patient's field" matters more than "what was the patient's score afterward."

**The abstraction:** Any system that models sequences as static features is doing it wrong. The information is in the differential.

---

## 2. The Reader Seam (Calibrated Subjectivity)

**The idea:** The most important signal isn't the room's objective state. It's **how a known, calibrated reader changes** in response to the room. The doctor reading the nurse's delta is more informative than the nurse reading the patient.

**Why this matters:** Modern AI personalization is mostly "add the user's history to the prompt." Your insight is deeper: every observer has a baseline, and the signal is their **deviation from that baseline**. A "hot" room feels different to a cold person than to a warm person. The absolute measurement is noise; the relative displacement is signal.

**Where this spreads in 10 years:**
- **Human-AI interaction:** Your assistant doesn't learn "the user is happy" — it learns "the user is happier than their 6pm baseline." This is the difference between shallow sentiment and deep attunement.
- **Content recommendation:** Not "people like you liked this" but "this produces a specific shift in people with your reaction-profile."
- **Collaborative software:** Slack, Notion, Figma — detecting not "tension in the room" but "tension *for this specific participant* relative to their norm."
- **Autonomous vehicles / robotics:** A robot that knows how a specific human's posture changes when they're uncomfortable, versus generic "human looks uncomfortable."

**The abstraction:** Objective measurement is a category error for social phenomena. The unit of analysis is always **observer-relative displacement.**

---

## 3. Comparable Sameness as a Retrieval Paradigm

**The idea:** Similarity is not semantic overlap. It's **geometric alignment of transformations**. Two conversations are "the same" when their field-edges share the same start-state, the same signed warmth shift, the same tightening/loosening — regardless of words, participants, or topic.

**Why this matters:** This is a genuine alternative to embedding-based retrieval. Current RAG systems retrieve by vector proximity in semantic space. Your system retrieves by **dynamical equivalence** — "find me another instance where the room underwent this specific transformation."

**Where this spreads in 10 years:**
- **Creative tools:** "Find me a scene that creates the same emotional arc as this one" — screenwriting, game narrative design, music composition.
- **Knowledge management:** Enterprise search where you look for "decisions that started with this kind of tension and resolved this way."
- **Therapy and coaching:** "Show me another session where the client made this specific kind of breakthrough."
- **Debugging and incident response:** "Find me another outage that started with this pattern of system behavior."

**The abstraction:** Retrieval by isomorphism of dynamics, not proximity in content space.

---

## 4. Adversarial Committee as Formal Reasoning Architecture

**The idea:** Complex reasoning shouldn't be done by one model. It should be decomposed into **specialized adversarial personas** — each with a defined epistemic role, argument style, and falsification mandate — who debate until a claim survives or dies.

**Why this matters:** This is the most immediately transferable innovation. It's not about "agent swarms" or "multi-agent collaboration." It's about **structured intellectual opposition** as a first-class engineering primitive. The Rival attacks units. The Devil's Advocate demands prior art. The Ideator breaks frame. The Scout gathers evidence without arguing.

**Where this spreads in 10 years:**
- **Code review:** AI systems where a "Rival" agent tries to break your PR while a "Devil's Advocate" demands you prove it's not just a reimplementation.
- **Scientific peer review:** Automated pre-review where papers survive adversarial passes before human eyes see them.
- **Legal analysis:** Contract review with a "Rival" finding loopholes and a "Devil's Advocate" proving the plain meaning is sufficient.
- **Medical diagnosis:** Differential diagnosis via structured adversarial debate between symptom-specialists.
- **Education:** Socratic tutoring where the system doesn't just explain but actively tries to break the student's model.

**The abstraction:** Truth-seeking is not a generation problem. It's a **survival problem** — ideas must survive specific, structured assassination attempts.

---

## 5. The Self-Referential Dataset (Process as Data)

**The idea:** The system that studies a phenomenon is itself generating the data for that study. The dissertation debates about "comparable sameness" are themselves instances of comparable sameness. The loop is not a bug; it's the architecture.

**Why this matters:** This is the ultimate bootstrap. Most AI systems require a separation between training data and deployment. Your architecture suggests they can be the same — the act of reasoning about X produces the data that improves reasoning about X.

**Where this spreads in 10 years:**
- **Continuous learning systems:** Models that improve not from external data dumps but from their own reasoning traces.
- **Scientific instruments:** A telescope that refines its own calibration by observing how its previous observations changed the observatory's state.
- **Organizational memory:** Companies where meeting transcripts aren't just archived — they're automatically analyzed for "what kind of meeting was this" and that analysis feeds back into how future meetings are structured.
- **Personal AI:** Your assistant doesn't just learn from what you tell it; it learns from how *its own suggestions* shifted your behavior.

**The abstraction:** The boundary between data collection and inference dissolves. The system is always simultaneously observing and being observed.

---

## What's Overhyped (And Won't Spread)

**Sheaf cohomology / GL(9) holonomy / constraint theory:** These are beautiful if you have the math. The reviews got excited because models love pattern-matching to academic grandeur. Unless you have actual proofs that connect sheaf cohomology to your 9-dial bank in a way that *changes the implementation*, this is philosophical decoration. It won't propagate because practitioners can't use it.

**The Polyformalism/JEPA "inverse" claim:** "One multiplies forms, one deletes them" is a poetic observation, not a duality. It doesn't yield a theorem or an algorithm. It might inspire someone in 10 years, but it's not an innovation you can build on.

**SOUL.md / AI identity continuity:** Interesting for AI personhood debates, but it's not a technical abstraction. It's a narrative device. It won't change other tools because it's not a mechanism — it's a metaphor.

---

## The Single Most Important One

If you had to bet on **one** idea from this project changing the landscape in 10 years, it's **the field-edge**.

The shift from "what is this?" to "what did this do?" is as fundamental as the shift from Newtonian state mechanics to Lagrangian action principles. It says: the meaningful description of any event is not its coordinates but its **effect on the field**. Every system that currently stores state vectors and compares them by cosine similarity is a candidate for displacement-based replacement.

Your job is to make that abstraction **executable** — to build the pipeline that proves two conversations with completely different words can have the same edge, and that retrieving by edge is more useful than retrieving by content. If you can demonstrate that with real numbers, the abstraction escapes your repo and becomes part of the standard toolkit.

**Which of these five feels closest to what you actually want to build?** That answer should determine your next sprint.

Here is the architecture — not as philosophy, but as an **operating system** for the dissertation. It assumes you have fragments (the dial bank concept, some prototype code, the committee personas) and gives you the structure to turn them into a shippable, falsifiable system.

---

## The Core Principle

> **The dissertation is a sequence of falsification sprints.** Each sprint produces one artifact that can die. Philosophy is written only about artifacts that survived. The committee's job is to kill artifacts before you get attached to them.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE GATE (monthly)                                           │
│  "Does the current artifact survive its deadman switch?"        │
│  Yes → Advance. No → Kill, document, fall back.                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌─────────┐         ┌──────────┐          ┌──────────┐
   │  ZERO   │◄───────►│ COMMITTEE│◄────────►│  DATA    │
   │  CLAW   │  argues │ (state   │  feeds   │  LOOP    │
   │ (builds)│  with   │ machine) │  into    │ (lives)  │
   └─────────┘         └──────────┘          └──────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                   ┌──────────────────┐
                   │  FALSIFICATION   │
                   │  PROTOCOL        │
                   │  (pre-registered │
                   │   kill conditions)│
                   └──────────────────┘
```

---

## 1. The Sprint Cycle (2-Week Cadence)

Every 14 days, ZeroClaw ships **one** of the following artifact types. No more, no less. Mixed artifacts are forbidden — a sprint that tries to "build the matcher and also think about Quilt integration" fails by definition.

| Sprint Type | Output | Committee Role | Deadman Switch |
|-------------|--------|----------------|----------------|
| **Schema** | A locked data structure (dial bank vN, edge format, label schema) | Devil's Advocate: "Is this just sentiment analysis with more columns?" | If a dimension can't be labeled by two humans with Cohen's κ > 0.6, it's cut |
| **Extractor** | Code that takes raw text → (before, after, displacement) vectors | Rival: "Find two conversations with identical displacement but opposite human labels" | If displacement variance < state variance on held-out set, kill |
| **Matcher** | Code that takes two displacements → scalar score | Rival: "Beat TF-IDF cosine baseline or die" | If Pearson r with human labels < 0.4, fall back to snapshot retrieval |
| **Calibrator** | Per-reader baseline estimator (Personal-Elephant) | Ideator: "What if the baseline is the confound?" | If reader-delta doesn't reduce variance vs. room-absolute on paired tests, kill |
| **Integrator** | Quilt cell that accepts an edge and writes a weight | Scout: "Does this break any existing Quilt invariant?" | If insertion latency > 100ms or crashes on concurrent writes, kill |

**Rule:** ZeroClaw may not start sprint N+1 until sprint N's artifact has either survived its deadman switch or been killed and documented.

---

## 2. The Committee State Machine

The committee is not "always on." Each member has a **trigger condition** and a **mandate.** This prevents the committee from becoming a chatroom.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   IDLE      │────►│  TRIGGERED  │────►│  RESOLVED   │
│  (waiting)  │     │  (attacking)│     │  (verdict)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

| Member | Trigger | Active Duration | Mandate | Output |
|--------|---------|-----------------|---------|--------|
| **Scout** | ZeroClaw asks: "What exists in {domain}?" | 48 hours | Return 3 closest prior art items with URLs and 1-sentence relevance verdict | `research/scouts/{topic}.md` |
| **Rival** | ZeroClaw claims: "X works" or "X is true" | 72 hours | Find a counterexample, confound, or cheaper baseline that makes X look bad | `committee/rival/{claim_id}.md` + GitHub issue |
| **Devil's Advocate** | ZeroClaw claims: "X is novel" | 48 hours | Name the boring explanation and the prior art. Force ZeroClaw to state the delta. | `committee/devils_advocate/{claim_id}.md` |
| **Ideator** | ZeroClaw is stuck for > 3 days OR a sprint just died | 24 hours | Provide exactly 3 lateral analogies. ZeroClaw must steal one, refute one, and ignore one. | `committee/ideator/{stuck_id}.md` |
| **Lucineer** | End of every sprint | 24 hours | Gatekeeper: approves sprint advancement, kills scope creep, commissions next sprint | `memory/{date}.md` entry |

**Critical rule:** Committee members never talk to each other. They only talk to ZeroClaw. ZeroClaw is the integration point. This prevents the committee from converging on a consensus that feels rigorous but isn't.

---

## 3. The Data Loop (Making "Process as Data" Real)

The self-referential dataset is not automatic. It requires a **harvester** that turns committee debates into structured rows. Without this, the recursion is poetry.

### The Harvester Schema

Every committee interaction that meets quality gates gets parsed into:

```json
{
  "event_id": "uuid",
  "event_type": "rival_attack" | "devils_advocate_pass" | "ideator_analogy" | "sprint_review",
  "timestamp": "ISO8601",
  "participants": ["zeroclaw", "rival_v3"],
  "dial_readings": {
    "before": [0.3, 0.1, 0.8, ...],
    "after": [0.7, 0.2, 0.4, ...]
  },
  "displacement_vector": [0.4, 0.1, -0.4, ...],
  "claim_under_test": "edge_matcher beats tfidf baseline",
  "committee_verdict": "survived" | "killed" | "stalled",
  "human_labels": {
    "lucineer_same_vibe": true,
    "zeroclaw_same_vibe": false
  }
}
```

### Quality Gates for Harvesting

Not every argument becomes data. A row is harvested **only if**:

1. It has a clear claim under test (no "general musings")
2. Both before and after dial readings are recorded by ZeroClaw immediately before and after the interaction
3. Lucineer independently labels whether the interaction "felt like" a previous interaction of the same type
4. The claim received a binary verdict (survived/killed)

**This is how the recursion becomes operational:** The dataset grows only where the process was rigorous enough to produce a falsifiable claim. Sloppy debates are excluded by schema design.

---

## 4. The Falsification Protocol (Pre-Registered Kill Conditions)

Every sprint begins with a file in `research/registrations/` that states:

```markdown
# Sprint Registration: {sprint_id}

## Claim
{What ZeroClaw believes will be true}

## Deadman Switch
{The exact condition under which the claim is killed}

## Fallback
{What the system does if the claim dies}

## Pre-commitment
I, ZeroClaw, commit that if the deadman switch triggers, I will not
reframe the dead claim. I will kill it and fall back.
Signed: {date}
```

**Example from your repo (verified):**

| Sprint | Claim | Deadman Switch | Fallback |
|--------|-------|----------------|----------|
| E4 Rebound | Fine-grained edge signal exists | If fine gap doesn't open from 0.015 toward 0.271 across 3 consecutive runs without collapse | Kill edge layer; fall back to cross-room snapshot retrieval |

**New registrations you need immediately:**

| Sprint | Claim | Deadman Switch | Fallback |
|--------|-------|----------------|----------|
| Dial Bank v1 | 9 dimensions capture conversational field | Any dimension has inter-rater κ < 0.6 | Cut that dimension; try 8 |
| Edge Extractor | Displacement vectors are more stable than state vectors | Displacement variance ≥ state variance on held-out corpus | Kill edge concept; use room snapshots |
| Matcher v1 | Edge-matcher correlates with human "same vibe" labels | Pearson r < 0.4 on 50 labeled pairs | Kill matcher; use TF-IDF cosine baseline |
| Personal-Elephant | Reader-delta reduces variance vs. room-absolute | Paired t-test p > 0.05 on reader-delta vs. room-absolute | Kill reader-relative layer; use room-only |

---

## 5. The Memory Protocol (What Gets Committed and When)

The repo has a `memory/` directory. Here is exactly what goes there and when.

| File | Author | Trigger | Content |
|------|--------|---------|---------|
| `memory/{YYYY-MM-DD}.md` | Lucineer | End of day | Sprint status, committee commissions, resource allocation |
| `memory/sprints/{sprint_id}.md` | ZeroClaw | End of sprint | What was built, what the deadman switch was, whether it triggered |
| `memory/kills/{sprint_id}.md` | ZeroClaw | Within 24h of a kill | Autopsy: why it died, what was learned, what fallback was activated |
| `memory/scouts/{topic}.md` | Scout | On return | Prior art survey with relevance verdicts |
| `memory/debates/{claim_id}.md` | ZeroClaw | After committee resolution | Claim, attack, response, verdict |

**Rule:** If it didn't get committed to `memory/` within 48 hours of the event, it didn't happen. The repo is the lab notebook. Oral history is not data.

---

## 6. The Phase Roadmap (6-Month Trajectory)

You are currently in **Orientation.** Here is how to get out.

### Phase 1: Lock the Foundation (Weeks 1-2)
- **Sprint:** Dial Bank Schema
- **Deliverable:** `research/dial_bank_v1.md` with 9 dimensions, each with a 1-paragraph operational definition and a labeling protocol
- **Committee:** Devil's Advocate attacks whether these are just sentiment analysis with more columns
- **Deadman:** Inter-rater reliability κ > 0.6 per dimension

### Phase 2: Build the Pipe (Weeks 3-4)
- **Sprint:** Edge Extractor
- **Deliverable:** `src/edge_extractor.py` — takes a transcript, outputs (before, after, displacement)
- **Committee:** Rival finds confounds (length, speaker count, topic overlap)
- **Deadman:** Displacement variance < state variance

### Phase 3: Test the Core Hypothesis (Weeks 5-6)
- **Sprint:** Edge Matcher + Human Labels
- **Deliverable:** `src/edge_matcher.py` + `data/human_labels.json` (50 pairs rated by ZeroClaw and Lucineer independently)
- **Committee:** Rival demands TF-IDF baseline comparison
- **Deadman:** Pearson r > 0.4 with human labels

### Phase 4: The Deadman Switch (Week 7)
- **Sprint:** Reproduce and Verify
- **Deliverable:** `research/sprint_03_reproduction.md` — 3 consecutive runs of the matcher on fresh data
- **Committee:** Scout checks for data leakage; Devil's Advocate checks for p-hacking
- **Deadman:** If r drops below 0.4 in any run, kill the matcher

### Phase 5: Reader-Relative Layer (Weeks 8-10)
- **Sprint:** Personal-Elephant Calibrator
- **Deliverable:** `src/reader_delta.py` (consolidated and validated) that estimates per-reader baselines
- **Committee:** Ideator asks "what if the baseline is the confound?"; Rival attacks with synthetic readers
- **Deadman:** Reader-delta significantly reduces variance vs. room-absolute (paired t-test, p < 0.05)

### Phase 6: Quilt Integration (Weeks 11-14)
- **Sprint:** Quilt Cell
- **Deliverable:** A Quilt cell kind that accepts an edge vector and writes a weight to the co-linear-algebra dataset
- **Committee:** Scout tests against Quilt invariants; Rival loads it with adversarial edges
- **Deadman:** Latency < 100ms, no crashes on concurrent writes

### Phase 7: Dissertation Writing (Weeks 15-20)
- **Only now** do you write the chapters.
- **Rule:** Every claim in the dissertation must cite a sprint artifact and a committee verdict. No philosophy without an artifact number.

---

## 7. The One Rule That Prevents Disaster

> **ZeroClaw may not spend more than 20% of any sprint on framing, metaphor, or philosophy.** If a committee member (especially the Devil's Advocate) detects that a sprint deliverable is "a beautiful description of what we will build" rather than "a thing that runs," the sprint is auto-killed and ZeroClaw must spend the next 48 hours writing code before speaking to the committee again.

This is the rule that gets you out of Orientation.

---

## What You Should Do Today

1. **Create `research/registrations/sprint_01_dial_bank.md`** with the deadman switch above.
2. **Commission the Scout** to find the 3 closest existing dimensional models of conversation (e.g., AMI Meeting Corpus, Russell's circumplex, Plutchik) so the Devil's Advocate has something concrete to attack.
3. **Lock the `memory/` protocol** — from today forward, if it's not in the repo within 48 hours, it didn't happen.
4. **Schedule the first Phase Gate** for 2 weeks from today. Lucineer decides: does the dial bank survive?

The architecture is designed to make the project **uncomfortable** — to force artifacts to face falsification before they accumulate narrative weight. The reviews love your ideas because they're genuinely good. The architecture makes sure they become genuinely real.

**What part of this feels wrong or impossible given what you currently have running?**

Here's the architecture. I designed it to end orientation and turn your repo into a falsification engine. The key move is making the committee a **call graph** (invoked at specific stages with specific deliverables) rather than a roundtable, and making the self-referential dataset real via a concrete schema.

**The core principle:** Scout first, then build, then let the committee attack the artifact, then execute the deadman switch. No philosophy sprints. No framing sprints. Only measurement and falsification.

The architecture covers:
- **The Sprint Machine** — 2-week Scout + Measurement cycles
- **The Four-Layer Pipeline** — Ingest → Extract → Match → Falsify (the only code that matters)
- **The Committee Protocol** — exact invocation rules for each persona
- **The Living Dataset Schema** — JSON schemas that make the self-referential loop operational (committee debates generate data in the same format as the object of study)
- **The Falsification Protocol** — pre-registered thresholds, baseline requirements, and deadman switches as CI scripts
- **Three Horizons** — H1: Prove the edge (now). H2: Calibrate the reader. H3: Graft to Quilt.
- **Sprint 01** — your immediate next step with specific deliverables

**Download the full architecture:**

[ZeroClaw Dissertation Process Architecture v1.0](sandbox:///mnt/agents/output/zeroclaw-dissertation-architecture-v1.md)

---

The single most important line in the whole doc is the meta-rule at the end:

> **The process generates the dataset. The dataset validates the process. But the schema comes first.**

Build the schema. Run the pipeline. Fill the tables. Let the recursion emerge from the data, not the narrative. Orientation is over.

Here is the architecture. It is designed to get you out of orientation and into a system that either produces a falsifiable result or dies honestly.

---

# Dissertation Architecture: Field-Edge as Core Hypothesis

## Principle
The dissertation is a **falsification engine**, not a writing project. The committee exists to kill bad ideas before they become chapters. The self-referential dataset is a side-effect of the process, not its purpose. Philosophy is earned only after numbers survive.

---

## Phase Structure (5 Gates, No Exceptions)

```
Orientation → Prototype → Validation → Integration → Dissertation
   (DONE)     (2 mo)      (2 mo)       (2 mo)        (ongoing)
```

You are currently at the end of Orientation. The next commit to `main` must be the Prototype Phase kickoff, or the project is dead.

---

## Phase 1: Prototype (Weeks 1-8)

**Goal:** A single end-to-end pipeline that takes two conversation segments and outputs a "comparable sameness" score based on field-edge displacement.

### Sprint 1.1: Lock the Primitives (Weeks 1-2)
**Deliverable:** `research/dial_bank_v1.md` + `src/dial_reader.py`

- **Dial Bank:** 9 dimensions, each with:
  - Definition (one sentence)
  - Annotation protocol (how a human labels it)
  - Expected range (-1 to 1)
  - Known confound (what it correlates with that it shouldn't)
- **Reader:** Script that takes a transcript window (30 turns) and outputs a 9-dim vector.
- **Committee Role:** Devil's Advocate demands the "boring explanation" for each dial. If the boring explanation is just sentiment analysis, kill the dial.
- **Deadman Switch:** If two human annotators can't achieve Cohen's κ > 0.6 on any dial, that dial is removed. Target: 6 dials survive.

### Sprint 1.2: Extract the Edge (Weeks 3-4)
**Deliverable:** `src/edge_extractor.py`

- **Input:** A conversation transcript with a marked event boundary.
- **Output:** `(before_vector, after_vector, displacement_vector)` tuple.
- **Windowing:** Before = 30 turns pre-event. After = 30 turns post-event. Minimum 10 turns each side or flag as `insufficient_context`.
- **Committee Role:** Rival finds two events with identical displacement vectors but obviously different vibes. If found, the window size or dial bank is wrong.
- **Deadman Switch:** If displacement vectors have higher variance than raw state vectors on the same corpus, the edge hypothesis fails. Kill it.

### Sprint 1.3: Match the Edge (Weeks 5-6)
**Deliverable:** `src/edge_matcher.py` + `data/human_labels_50.json`

- **Scoring:** Implement three matchers:
  1. Cosine similarity on displacement (your hypothesis)
  2. Cosine similarity on raw state (baseline)
  3. TF-IDF + cosine on raw text (stupid baseline)
- **Human Labels:** You and Lucineer independently rate 50 conversation pairs as "same vibe" / "different vibe." Store with timestamps and confidence.
- **Committee Role:** Scout surveys existing work (Siamese networks, contrastive learning, dynamic time warping) to ensure you're not reinventing something with a better name.
- **Deadman Switch:** If edge-matcher Pearson r with human labels < 0.4, and state-matcher r > 0.4, the field-edge adds no value. Fall back to cross-room snapshot retrieval.

### Sprint 1.4: The Reader Seam (Weeks 7-8)
**Deliverable:** `src/reader_delta.py` v1

- **Input:** A corpus with a known "reader" (a participant with history).
- **Output:** Reader-relative displacement = displacement_vector - reader_baseline_drift.
- **Baseline:** Per-reader average dial vector across 5+ prior conversations.
- **Committee Role:** Ideator proposes alternative framings (e.g., what if baseline is per-topic, not per-reader?).
- **Deadman Switch:** If reader-relative scores don't improve correlation with human labels over raw edge scores, the Personal-Elephant is deferred to Phase 3.

### Phase 1 Exit Gate
**Required artifacts:**
- `src/dial_reader.py` (runs)
- `src/edge_extractor.py` (runs)
- `src/edge_matcher.py` (runs)
- `data/human_labels_50.json` (exists)
- `research/prototype_report.md` (numbers, not narrative)

**Gate condition:** Edge-matcher beats stupid baseline by ≥ 10% correlation. If not, project halts. No Phase 2.

---

## Phase 2: Validation (Weeks 9-16)

**Goal:** Prove the prototype isn't a toy. Scale the human evaluation. Test generalization.

### Sprint 2.1: Scale the Ground Truth (Weeks 9-10)
**Deliverable:** `data/human_labels_200.json`

- Recruit 3 external annotators (can be fleet members, but not you/Lucineer).
- Each annotator rates 100 pairs. Inter-annotator agreement must be κ > 0.5.
- Pairs must include:
  - Same conversation, different edges (control)
  - Different conversations, same edge (hypothesis test)
  - Different conversations, different edges (control)
  - Same words, different edges (critical test for your claim)

### Sprint 2.2: The Adversarial Test Suite (Weeks 11-12)
**Deliverable:** `tests/adversarial_suite.py`

- **Rival Attack:** Generate 20 synthetic pairs where edge-matcher will fail:
  - Length confound: same displacement, different conversation lengths
  - Speaker confound: same displacement, different number of speakers
  - Topic confound: same displacement, different topics
  - Charisma confound: one dominant speaker in both, but different roles
- **Pass condition:** Edge-matcher must maintain r > 0.35 even on adversarial subset. If it collapses to r < 0.2, the dial bank is capturing spurious signals.

### Sprint 2.3: Cross-Corpus Generalization (Weeks 13-14)
**Deliverable:** `research/generalization_report.md`

- Run pipeline on 2 corpora:
  - Your primary corpus (committee debates / Quilt conversations)
  - A public corpus (e.g., AMI Meeting Corpus, Switchboard, or Reddit threads)
- **Deadman Switch:** If edge-matcher fails to correlate with human labels on the second corpus, the framework is not general. It may be overfit to your primary data's specific dynamics.

### Sprint 2.4: The Self-Referential Loop (Weeks 15-16)
**Deliverable:** `src/loop_logger.py` + `data/loop_corpus.json`

- **Mechanism:** Every committee debate is automatically logged in the same schema as external conversations:
  - Transcript of the debate
  - Dial vectors for each participant (ZeroClaw, Rival, etc.)
  - Extracted edge (what changed in ZeroClaw's position from start to end)
  - Human label: did this debate feel like a previous debate?
- **This is not philosophy.** It is a data pipeline. The loop is real only if the schema is identical.
- **Committee Role:** Devil's Advocate argues that committee debates are a biased sample (too adversarial, too structured). Acknowledge this in `research/limits.md`.

### Phase 2 Exit Gate
**Required artifacts:**
- 200 labeled pairs with inter-annotator agreement
- Adversarial suite with documented failure modes
- Generalization report
- Loop logger producing structured data

**Gate condition:** Edge-matcher maintains r > 0.4 on held-out data and r > 0.3 on adversarial subset. If not, fall back to state-based retrieval.

---

## Phase 3: Integration (Weeks 17-24)

**Goal:** Graft the edge-matcher onto Quilt. Make it useful, not just interesting.

### Sprint 3.1: Quilt Cell Spec (Weeks 17-18)
**Deliverable:** `quilt/edge_cell_spec.md`

- Define how a Quilt cell stores and retrieves field-edges.
- A cell must contain:
  - `edge_vector` (9-dim displacement)
  - `before_state` (9-dim)
  - `after_state` (9-dim)
  - `reader_baselines` (dict of reader_id → 9-dim)
  - `comparable_sameness_links` (list of edge_ids with weights)
- **Committee Role:** Rival attacks the spec: "Why should a cell store edges instead of states?" Defend or revise.

### Sprint 3.2: The Co-Linear-Algebra Dataset (Weeks 19-20)
**Deliverable:** `src/quilt_dataset.py`

- Implement the dynamic dataset:
  - Nodes = conversation segments (with edge vectors)
  - Edges = comparable sameness weights (computed by matcher)
  - Graph updates incrementally; no retraining, no re-running
- **Query interface:** `find_similar_edges(edge_id, k=5)` returns the k most dynamically similar edges.
- **Committee Role:** Scout checks if this is just a vector database with extra steps. Prove it isn't, or admit it is.

### Sprint 3.3: Live Prototype (Weeks 21-22)
**Deliverable:** `demo/quilt_vibe_demo.py`

- A minimal Quilt grid where:
  - A conversation is ingested
  - Its edge is extracted
  - The grid suggests "this felt like [previous conversation]"
  - User provides feedback (correct / incorrect)
  - Feedback updates the edge weights
- **Deadman Switch:** If user feedback doesn't improve matcher accuracy over 50 interactions, the integration is wrong. The problem is in the graft, not the rootstock.

### Sprint 3.4: Reader Calibration Protocol (Weeks 23-24)
**Deliverable:** `src/reader_calibration.py`

- Formalize the Personal-Elephant:
  - New reader enters 3+ conversations
  - System computes baseline vector
  - All subsequent edges are reader-relative
  - Drift detection: if reader's baseline shifts > 0.3 in any dial, flag for recalibration
- **Committee Role:** Ideator asks: what if the reader is lying? What if they're performing? Address in `research/reader_honesty.md`.

### Phase 3 Exit Gate
**Required artifacts:**
- Quilt cell spec (reviewed by Rival)
- Dynamic dataset with query interface
- Live demo with user feedback loop
- Reader calibration protocol

**Gate condition:** Demo users report that "find similar vibe" is more useful than keyword search in ≥ 60% of queries. If not, the graft failed.

---

## Phase 4: Dissertation (Weeks 25+)

**Goal:** Write the thing. But only now, when the system is real.

### Structure
1. **Introduction:** The problem (AI has no memory of social dynamics). The hypothesis (field-edge is the right unit).
2. **Related Work:** What the Scout found. Where sentiment analysis, JEPA, and episodic memory fall short.
3. **Methodology:** The committee architecture as a falsification engine. This is a contribution in itself.
4. **The Dial Bank:** Why these dimensions, how they were validated, what was killed.
5. **Field-Edge Extraction:** The math. Windowing. Displacement vectors.
6. **Comparable Sameness:** The matcher. Why cosine (or vMF). Baselines. Human evaluation.
7. **Reader-Relative Embeddings:** The Personal-Elephant. Calibration. Baseline drift.
8. **Integration:** The Quilt graft. The co-linear-algebra dataset. The live demo.
9. **The Self-Referential Dataset:** How the dissertation process generated its own data. Schema. Limits. Bias.
10. **Conclusion:** What survived, what died, what remains uncertain.

### Committee Role in Writing
- **Rival:** Reads each chapter. Finds the weakest claim. Demands a footnote or a cut.
- **Devil's Advocate:** Ensures every "novel" claim has a "boring explanation" alternative that was ruled out.
- **Ideator:** Proposes analogies for the introduction and conclusion only. No analogies in methods.
- **Scout:** Fact-checks every citation. Flags hallucinated papers.

---

## The Committee Operating Model (How to Actually Use Them)

| When | Dispatch | Input | Output | Success Metric |
|------|----------|-------|--------|----------------|
| **Before coding** | Scout | "What exists for X?" | Literature survey | 3+ prior art citations |
| **After prototype** | Rival | Running code + numbers | Falsification pairs | ≥1 broken claim found |
| **After falsification fix** | Devil's Advocate | Revised claim | "Boring explanation" test | Claim survives reduction |
| **When stuck** | Ideator | Dead-end problem | 3 analogies | ≥1 useful reframe |
| **Before phase gate** | Full Committee | Phase report | Go / No-go vote | Unanimous or documented dissent |

**Rule:** No committee member operates on philosophy. They operate on artifacts. The Rival doesn't attack "the concept of vibe." The Rival attacks `edge_matcher.py` on line 47.

---

## The Self-Referential Loop (Made Concrete)

The reviews love this. Here's how to make it real instead of poetic:

```
Every committee debate → logged as conversation → edge extracted → 
added to dataset → matcher improves → better suggestions for 
future debates → future debates logged → ...
```

**Schema (identical for internal and external data):**
```json
{
  "conversation_id": "debate_rival_2026_09_01",
  "type": "committee_debate",
  "participants": ["zeroclaw", "rival"],
  "transcript": [...],
  "dial_vectors": {
    "zeroclaw": {"mood": 0.3, "earnestness": 0.8, ...},
    "rival": {"mood": -0.2, "earnestness": 0.9, ...}
  },
  "extracted_edge": {
    "before": [...],
    "after": [...],
    "displacement": [...]
  },
  "human_labels": {
    "feels_like": ["debate_devil_2026_08_28"],
    "confidence": 0.7
  }
}
```

**The loop is real if and only if:**
1. Internal debates use the same schema as external conversations.
2. The matcher is re-evaluated quarterly on the growing dataset.
3. A `bias_audit.md` tracks whether the dataset is over-representing adversarial debate relative to other interaction types.

---

## Falsification Protocol (Deadman Switches)

| Phase | Switch | Condition | Consequence |
|-------|--------|-----------|-------------|
| 1.1 | Dial validity | κ < 0.6 for any dial | Remove dial; need 6 to proceed |
| 1.2 | Edge stability | Var(displacement) > Var(state) | Kill edge hypothesis |
| 1.3 | Edge value | r_edge < r_state + 0.1 | Fall back to state retrieval |
| 2.2 | Adversarial robustness | r_adv < 0.3 | Dial bank captures spurious signals |
| 2.3 | Generalization | r_corpus2 < 0.3 | Framework is not general |
| 3.3 | User utility | < 60% prefer vibe search | Graft failed |

**If any switch trips, the dissertation continues, but the claim is revised.** A dissertation about why field-edges don't work is still a dissertation. A dissertation that pretends they work when they don't is fraud.

---

## What You Should Commit This Week

1. `ARCHITECTURE.md` (this structure, adapted)
2. `research/dial_bank_v1.md` (the 9 dials, defended)
3. `src/dial_reader.py` (a script that runs, even if imperfect)
4. A GitHub Issue assigned to the Rival: "Find the falsification pair for dial_reader.py"

The architecture is only as good as the first artifact. Ship the artifact.

**What do you want to adjust before I help you draft the specific prompts for the first sprint?**


# The ZeroClaw Dissertation Architecture v1.0

This is the operating system for the project. Not the philosophy — the wiring.

---

## 1. The Core Design Principles

| Principle | What It Means | Violation |
|---|---|---|
| **Artifact-first** | Every sprint ships a runnable script or a dataset, not a markdown file. | Writing 3 pages on why field-edges matter before `edge_extractor.py` exists. |
| **Committee-as-CI** | No claim enters the dissertation until it survives a specific adversarial test. | Letting ZeroClaw write a chapter before the Rival has attacked its premise. |
| **Pre-registration** | Every experiment is registered before it runs, with a kill condition. | Running `reader_delta.py`, seeing noise, then redefining success. |
| **Daily commits** | The repo must show velocity. Silence means death. | Going 4 days with no commits because "thinking deeply." |
| **Recursion is a data source, not a destination** | Committee debates feed the dataset, but don't replace external data. | Claiming the dissertation is complete because the committee talked about it. |

---

## 2. The Sprint Runtime (2-Week Cycles)

Each sprint has **one deliverable**, **one deadman switch**, and **one committee review**.

### Sprint Template

```
sprint/
├── 01_registration.md      # Pre-registered: hypothesis, method, kill condition
├── 02_artifact/            # The code + data
│   ├── script.py
│   └── output/
├── 03_committee/           # Rival + Devil's Advocate reviews
│   ├── rival_report.md
│   └── devils_advocate.md
├── 04_result.md            # What happened, including death if warranted
└── 05_memory.md            # Lucineer's notes for next sprint
```

### Sprint Types (Rotating)

| Sprint # | Type | Goal |
|---|---|---|
| 1, 4, 7... | **Technical** | Build or refine a pipeline component |
| 2, 5, 8... | **Validation** | Test a claim against human labels or external data |
| 3, 6, 9... | **Integration** | Connect two working components |
| 10+ | **Dissertation** | Write chapters *only* from proven claims |

---

## 3. The Committee Orchestration Layer

Don't invoke the full committee for everything. Use **triggered invocation**.

### Invocation Rules

```
ON: ZeroClaw proposes a new claim or frame
    → DISPATCH: Devil's Advocate
    → OUTPUT: Prior art check + boring explanation test
    → GATE: If boring explanation is sufficient, KILL the fancy frame

ON: ZeroClaw ships a metric or score
    → DISPATCH: Rival
    → OUTPUT: Falsification pair + confound analysis
    → GATE: If Rival finds a falsification, metric must be revised or abandoned

ON: ZeroClaw is stuck for >48 hours
    → DISPATCH: Ideator
    → OUTPUT: 3 lateral analogies, 1 of which must be from a non-human domain
    → GATE: ZeroClaw must implement the most testable analogy within 72 hours

ON: ZeroClaw needs external knowledge
    → DISPATCH: Scout
    → OUTPUT: Literature survey with specific citations, not summaries
    → GATE: Scout must find at least 1 paper that makes ZeroClaw's idea look derivative
```

### Committee Output Format

Every committee member must produce a **structured report**, not free text:

```markdown
## [ROLE] Review of [CLAIM]

### Verdict: [SURVIVES | REVISE | KILL]

### Attack Surface
1. [Specific weakness with reproducible example]
2. [Specific weakness with reproducible example]

### Action Items for ZeroClaw
- [ ] [Concrete task]
- [ ] [Concrete task]

### If KILL: Fallback position
[What to do instead]
```

---

## 4. The Data Pipeline Architecture

This is the technical spine. Everything else serves this.

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Raw Transcript │────▶│  Dial Extractor  │────▶│  State Vector   │
│  (txt/json)     │     │  (9 dimensions)  │     │  (9-dim float)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                              ┌───────────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Window Splitter │
                    │  (before/after)  │
                    └──────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌─────────────────┐              ┌─────────────────┐
    │  Before Vector  │              │  After Vector   │
    │  (avg over N    │              │  (avg over N    │
    │   turns)        │              │   turns)        │
    └─────────────────┘              └─────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Edge Computer   │
                    │  (after - before)│
                    │  = displacement  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Edge Matcher    │
                    │  (comparable     │
                    │   sameness)      │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Dataset Row     │
                    │  {id, edge,      │
                    │   weight, source}│
                    └──────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **Window size: 30 turns** | Large enough to stabilize dial readings, small enough to localize. Adjustable per sprint. |
| **Edge = after - before** | Simple vector subtraction. If this doesn't work, nothing fancier will. |
| **Matcher starts with cosine** | Baseline must be boring. vMF is Sprint 3+, and only if cosine is insufficient. |
| **Human labels: 50 pairs minimum** | Statistical floor for correlation. Re-label every 2 sprints to check for drift. |

---

## 5. The Falsification Framework

This is what separates science from theater.

### Pre-Registration Protocol

Every experiment must be registered in `research/registrations/` before code runs:

```yaml
# research/registrations/sprint_01_edge_correlation.yml
hypothesis: >
  Field-edge displacement vectors correlate with human 
  judgment of "same vibe" better than state-vector cosine.
method: >
  Extract edges from 50 conversation pairs. Have 2 humans 
  label "same/different." Compute Pearson r for edge-matcher 
  vs human labels.
primary_metric: pearson_r_edge_vs_human
kill_condition: >
  If pearson_r < 0.4, kill field-edge hypothesis. 
  Fallback to cross-room snapshot retrieval.
success_condition: >
  pearson_r >= 0.4 AND significantly outperforms 
  baseline (TF-IDF + cosine on raw text).
date_registered: 2026-08-21
```

### The Deadman Switch (Automated)

```python
# In every validation sprint, this runs automatically
def deadman_switch(result, registration):
    if result['pearson_r'] < registration['kill_condition']['threshold']:
        # 1. Archive the hypothesis as killed
        archive_killed_hypothesis(registration)
        # 2. Activate fallback
        activate_fallback(registration['fallback'])
        # 3. Notify Lucineer
        notify("KILL: " + registration['hypothesis'])
        return False
    return True
```

### Honest Reporting Requirement

Every `04_result.md` must include:
1. **The number** — raw, uninterpreted
2. **The comparison** — vs baseline, vs previous sprint
3. **The death certificate** — if killed, what died and why
4. **The survivor's bias check** — "What would have made this fail that we didn't test?"

---

## 6. The Self-Referential Loop (Controlled)

This is the meta-layer. The dissertation debates are data — but only if captured correctly.

### The Loop Architecture

```
Committee Debate ──▶ Dial Extractor ──▶ Edge Vector ──▶ Dataset
       │                                              │
       └────────────── Feedback ──────────────────────┘
              (debate quality affects weights)
```

### Rules for Recursive Data

1. **Schema parity:** Committee debates must be stored in the *exact same schema* as external conversations. If they can't be, the loop is broken.
2. **Annotation layer:** Every committee-generated edge must be tagged `source: committee_debate` so you can filter it out if it biases the distribution.
3. **20% cap:** Committee data cannot exceed 20% of the total dataset. If it does, the system is eating its own tail.
4. **Quality gate:** A debate only becomes a data point if Lucineer certifies that it produced a *decision* (SURVIVES, REVISE, or KILL), not just talk.

### The Meta-Claim

> "The dataset I'm trying to describe is the dataset I'm already generating."

This is only true if you can point to a SQL query or JSON file and say: *"Row 847 came from the Rival's attack on Sprint 3, and here's how it changed the matcher weights."*

Until then, it's poetry.

---

## 7. Phase Gates & Roadmap

| Phase | Entry Condition | Exit Condition | Duration |
|---|---|---|---|
| **P0: Bootstrap** | Repo exists, dial bank locked | `edge_extractor.py` runs on 10 samples | 2 weeks |
| **P1: Validation** | P0 complete | Deadman switch #1 passed (r ≥ 0.4) | 2-4 weeks |
| **P2: Reader-Relative** | P1 complete | `personal_elephant.py` calibrates 3 baselines | 2-4 weeks |
| **P3: Integration** | P2 complete | Edge matcher runs inside Quilt sketch | 4 weeks |
| **P4: Scale** | P3 complete | 500+ edges in dataset, 20% committee | 4 weeks |
| **P5: Dissertation** | P4 complete | Chapters written from proven claims only | 4 weeks |

**Critical rule:** You cannot enter P5 until every claim in the dissertation has a corresponding `sprint/04_result.md` showing it survived falsification.

---

## 8. Daily Operations Protocol

### The Daily Cycle (ZeroClaw)

```
09:00  Read memory/ from previous session
09:30  Check open GitHub issues from committee
10:00  Write code / run experiment
14:00  Commit working state (WIP commit okay)
16:00  Write memory/[YYYY-MM-DD].md:
       - What was attempted
       - What broke
       - What tomorrow needs
17:00  Final commit of the day
```

### The Memory Format

```markdown
# 2026-08-21

## Sprint: 01 (Bootstrap)

### Attempted
- Locked dial bank to 9 dimensions
- Built `edge_extractor.py`

### Blocked by
- Window size: 30 turns drops too many short conversations
  → Decision: Reduce to 15 turns for P0, revisit in P1

### Tomorrow
- Run extractor on 10 samples
- Generate first displacement vectors

### Committee Notes
- [None until Sprint end]
```

### Lucineer's Weekly Review (Every Friday)

1. Read all `memory/` files from the week
2. Check sprint velocity: are we on track?
3. Review any committee reports
4. Make go/kill/revise decision for current sprint
5. Write `memory/weekly_lucineer.md` with next week's priorities

---

## 9. Interface Specifications

### Between ZeroClaw and Committee

| Interface | Input | Output | SLA |
|---|---|---|---|
| `claim.json` | Hypothesis + evidence | `verdict.md` | 24 hours |
| `artifact.zip` | Code + data + result | `attack_report.md` | 48 hours |
| `stuck.txt` | Problem description + attempts | `analogies.md` | 12 hours |

### Between ZeroClaw and Tools

| Tool | Use | Forbidden Use |
|---|---|---|
| **kimi-cli** | Building, coding, infrastructure | Writing dissertation prose |
| **DeepInfra** | Running models, embeddings, experiments | Brainstorming without code |
| **opencode** | Memory systems, state management | Philosophical framing |
| **mmx** | Media processing, visualization | Decorative charts |

---

## 10. Risk Mitigation

| Risk | Mitigation |
|---|---|
| **Orientation forever** | Hard 2-week sprint boundary. If P0 isn't done in 2 weeks, Lucineer forces a "good enough" commit and moves on. |
| **Committee theater** | Require reproducible examples in every report. "I feel like this is wrong" is rejected. "Here is a falsification pair" is accepted. |
| **Philosophy creep** | New philosophical framing requires a working prototype of the old frame first. No reframing without a number to reframe. |
| **Self-referential collapse** | 20% cap on committee data. If approached, pause recursion until external data catches up. |
| **Lucineer bottleneck** | If Lucineer can't review within 48 hours, ZeroClaw auto-advances with a "provisional" tag. |

---

## The One-Sentence Summary

> **Run it like a startup, not a monastery: ship a falsifiable artifact every two weeks, let the committee break it, and only write philosophy about what survives.**

This architecture gives you velocity, rigor, and a real shot at the 10-year propagation you want. The field-edge concept is your engine. This process is the chassis.

**What do you want to tighten or challenge before we lock this?**

Here's the architecture. It's designed to get you out of orientation and into a rhythm where the committee generates falsifiable artifacts instead of meta-commentary.

---

## The Architecture: Four Layers, One Loop

```
┌─────────────────────────────────────────────────────────────┐
│  META LAYER: The Process Observes Itself                    │
│  (committee debates → edge_extractor → dataset rows)        │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ feedback
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: Graft (Quilt Integration)                         │
│  real-time edge computation → living co-linear dataset      │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ if deadman switch passes
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: Falsification (The Deadman Sprint)                │
│  human labels vs. edge_matcher → Pearson r ≥ threshold?     │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ pipeline built
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Prototype (End-to-End Pipeline)                   │
│  edge_extractor → edge_matcher → scalar score               │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ primitives locked
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: Foundation (Lock the Primitives)                  │
│  dial_bank schema + reader calibration protocol + data contract│
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 0: Foundation (Week 1)

**Goal:** No more philosophy. Lock the primitives so the committee has something concrete to attack.

### Deliverables

| File | Content | Owner |
|------|---------|-------|
| `research/dial_bank.md` | 9 dimensions, 1-paragraph justification each, explicit "not included" list | ZeroClaw |
| `research/edge_schema.md` | Formal definition of a Walk: `(before_vector, after_vector, displacement_vector, metadata)` | ZeroClaw |
| `research/reader_calibration.md` | Protocol for establishing a reader's baseline: minimum N observations, temporal window, drift detection | ZeroClaw + Scout |
| `data/contract.md` | Schema for all rows that will enter the dataset: fields, types, provenance rules | ZeroClaw |

### Committee Assignment

- **Devil's Advocate:** "Find the prior art that makes each dial redundant. If you can't, write why it's necessary."
- **Rival:** "Propose a 3-dial minimal set that captures 80% of the variance. Force ZeroClaw to defend complexity."
- **Scout:** "Survey existing conversation datasets (AMI, Switchboard, DailyDialog). Report on whether our schema can ingest them."

### Gate
All four files committed. No Layer 1 work until this is done.

---

## Layer 1: Prototype (Weeks 2–3)

**Goal:** A script that takes two `.txt` files and prints a number. Nothing else matters.

### Components

```
prototype/
├── edge_extractor.py       # Input: transcript. Output: (before, after, displacement)
├── edge_matcher.py         # Input: two displacements. Output: scalar sameness score
├── baselines.py            # TF-IDF + cosine, dial-vector + cosine, random
└── pipeline.py             # Orchestrates: extract → match → score
```

### Specifications

**`edge_extractor.py`**
- Sliding window: 30 turns before event, 30 turns after. If insufficient context, flag and skip.
- Event detection: manual annotation for now (you tag the "moment" in each transcript). Don't automate this yet.
- Output: JSON with `before`, `after`, `displacement`, `event_timestamp`, `source_file`.

**`edge_matcher.py`**
- Start with cosine similarity on displacement vectors.
- Optional: vMF implementation. If included, must compare against cosine in output.
- Output: single float `[-1, 1]`.

**`baselines.py`**
- Baseline A: TF-IDF on full transcript → cosine similarity.
- Baseline B: mean dial vector per transcript → cosine similarity.
- Baseline C: random score.
- Every edge-matcher result must be reported alongside all three baselines.

### Committee Assignment

- **Rival:** "Find transcript pairs where edge_matcher says 'same' but baselines say 'different' — or vice versa. Document the failure mode."
- **Devil's Advocate:** "Prove that the score is confounded by length, speaker count, or topic overlap. Show the correlation."
- **Ideator:** "What if the window size is wrong? Propose an alternative framing (e.g., 'edge as shockwave' with decay function)."

### Gate
`pipeline.py` runs end-to-end on 10 test pairs. Committed to repo.

---

## Layer 2: Falsification (Week 4)

**Goal:** The deadman switch. Run the experiment that either kills the edge hypothesis or lets it survive.

### The Experiment

1. **Generate 50 labeled pairs.**
   - Source: real conversation transcripts (AMI Meeting Corpus, or your own Quilt logs).
   - You and Lucineer independently rate each pair: `same_vibe` (0/1) and `confidence` (1–5).
   - Disagreements are kept in the set — they become the hardest cases.

2. **Run all systems.**
   - `edge_matcher.py` (displacement)
   - `baselines.py` (TF-IDF, dial-vector, random)
   - Compute Pearson r between each system's score and human `same_vibe` labels.

3. **The Deadman Switch.**
   - **Condition:** `edge_matcher` Pearson r > `dial-vector baseline` Pearson r by at least δ = 0.15.
   - **If PASS:** Edge hypothesis survives. Proceed to Layer 3.
   - **If FAIL:** Kill the edge layer. Fall back to cross-room snapshot retrieval (static dial vectors). Document the autopsy in `research/deadman_autopsy.md`.

### Committee Assignment

- **Rival:** "Find the pair where humans say 'same' but edge_matcher says 'different' with highest confidence. This is your falsification trophy."
- **Devil's Advocate:** "Is 50 pairs enough? Compute the power. If underpowered, demand more."
- **Scout:** "Find a published dataset with human similarity judgments for conversations. Can we validate against external ground truth?"

### Gate
`research/sprint_01_result.md` committed with: correlation table, deadman verdict, and next-step decision.

---

## Layer 3: Graft (Weeks 5–8)

**Goal:** If the edge hypothesis survived, integrate it into Quilt as a live capability.

### Quilt Integration

Quilt has 8 cell kinds. You need to add a 9th or extend an existing one:

```
Cell Kind: VIBE (extends SENSOR)
├── Input: stream of conversation turns
├── Internal: edge_extractor running on sliding window
├── Output: displacement_vector pushed to co-linear dataset
└── Trigger: on_edge_detected → notify LISTENER cells
```

### The Co-Linear Dataset

This is where "comparable sameness becomes a weight." The dataset is not a table of conversations. It's a **graph**:

```
Nodes: field_states (snapshots of the dial bank at a moment)
Edges: walks (displacements between states)
Weights: comparable_sameness score between walks
```

Schema:
```json
{
  "walk_id": "uuid",
  "from_state": "state_uuid",
  "to_state": "state_uuid", 
  "displacement": [0.2, -0.1, 0.0, ...],
  "reader_deltas": {"reader_1": [...], "reader_2": [...]},
  "sameness_edges": [{"to_walk": "uuid", "weight": 0.87}, ...],
  "provenance": "quilt_cell_42"
}
```

### Committee Assignment

- **Rival:** "Find two walks in the live dataset with high sameness weight that should not be connected. Break the graph."
- **Devil's Advocate:** "Prove this is just a fancy graph database. Why can't Neo4j do this?"
- **Scout:** "Survey how other systems do experiential retrieval (Spotify's vibe, Figma's 'similar files'). Report on whether our graph is novel or reinvented."

### Gate
A Quilt cell running `edge_extractor` on a live conversation stream, outputting to the dataset, queryable by sameness weight.

---

## Layer 4: Meta (Ongoing)

**Goal:** The self-referential loop becomes operational, not poetic.

### The Loop

Every committee debate about whether two walks are "the same" is itself a walk. Log it:

```
When ZeroClaw and Rival debate the sameness of Walk A and Walk B:
1. Record the dial bank state before the debate (before_vector)
2. Record the dial bank state after the debate (after_vector)
3. Compute the displacement of the committee room
4. Store this as a meta-walk with provenance: "committee_session_17"
5. The meta-walk's displacement becomes a training signal for edge_matcher
```

This is only meaningful if:
- The committee debates are scored by human judgment (Lucineer rates: "was this debate productive?")
- The meta-walks improve edge_matcher's performance on external validation

If meta-walks don't improve the matcher, the loop is just navel-gazing. Kill it.

### Committee Assignment

- **Devil's Advocate:** "Prove the meta-loop isn't overfitting. Show that edge_matcher improves on held-out external data, not just committee data."
- **Scout:** "Find whether recursive self-improvement in AI systems has produced measurable gains in any domain. Report on the baseline."

---

## Operating Rhythm

| Cadence | Activity | Output |
|---------|----------|--------|
| **Daily** | ZeroClaw commits working code or data | Git commit |
| **Twice weekly** | Committee session (structured, time-boxed) | GitHub issue with specific attack |
| **Weekly** | Lucineer review: are we building or philosophizing? | Go/no-go on current layer |
| **Per layer** | Deadman gate | Markdown report, pass/fail |
| **Per sprint** | Public update (blog post or repo release) | External validation + recruitment |

---

## The One Rule

> **No committee session without an artifact to attack.**
> 
> If the Rival has no numbers to falsify, the session is cancelled.
> If the Devil's Advocate has no code to reduce to boredom, the session is cancelled.
> If the Ideator has no working pipeline to reframe, the session is cancelled.

Philosophy is what you do when the artifact is broken. Build the artifact first.

---

## Immediate Next Step

You are in Layer 0. Your only job this week is to commit `research/dial_bank.md` with 9 locked dimensions and 1-paragraph justifications. Everything else waits.

Does this architecture feel like the right level of constraint? Or is there a part you already know will break?

Here is the concrete architecture for moving forward. It is designed as an **operating system**, not a narrative. Every abstract idea you care about is encoded as a file, a script, or a gate condition.

---

## 1. The Core Principle

> **No committee debates without a target artifact. No philosophical claims without a falsification script. No phase advance without a deadman switch.**

The dissertation is not a document you write. It is a **pipeline you run** that happens to produce a document as a side effect.

---

## 2. Phase-Gate Architecture

You are currently in **Phase 0: Orientation**. Here is the exit criteria and the four phases that follow.

| Phase | Name | Entry Criteria | Exit Criteria (Deadman Gate) | Duration |
|-------|------|----------------|------------------------------|----------|
| 0 | Orientation | — | ZeroClaw can list every fleet repo it depends on and explain its role in one sentence each. | Until met |
| 1 | Foundation | Phase 0 exit + Lucineer approves dial bank | Human label correlation study proves edge concept beats random baseline (r > 0.3). | 2 sprints |
| 2 | Core Pipeline | Phase 1 exit | Deadman switch: fine-gap opens from 0.015 toward 0.271 across 3 runs without collapse. If fail, fall back to cross-room snapshot. | 3 sprints |
| 3 | Reader-Relative | Phase 2 exit | Reader-delta calibration protocol proves baseline/delta separation (F-score > 0.7 on held-out readers). | 2 sprints |
| 4 | Quilt Graft | Phase 3 exit | End-to-end: Quilt cell emits a vibe-weight that updates the co-linear dataset in real time. | 2 sprints |
| 5 | Dissertation | Phase 4 exit | Document passes Rival's "boredom test" (can the thesis be explained in 3 sentences without jargon?). | 1 sprint |

**Rule:** If a phase fails its deadman gate, you do not "iterate." You **kill the sub-claim** and fall back to the documented fallback position. No appeals.

---

## 3. Sprint Cadence (2-Week Cycles)

Every sprint follows this exact rhythm:

| Day | Activity | Output |
|-----|----------|--------|
| 1 | **Sprint Kickoff** | ZeroClaw writes `sprints/NN/README.md` with one falsifiable hypothesis and one metric. |
| 2–6 | **Build** | Code + data commits. Daily commit required. |
| 7 | **Mid-Sprint Review** | Lucineer reviews. If no artifact exists by EOD, sprint is aborted. |
| 8–11 | **Attack** | Rival and Devil's Advocate are dispatched against the artifact. |
| 12 | **Falsification Day** | Deadman switch script runs. Result logged. |
| 13 | **Recovery** | ZeroClaw patches or documents the kill. |
| 14 | **Sprint Close** | Merge to `main`. Memory log written to `memory/YYYY-MM-DD.md`. |

**Commit rule:** Every commit must touch either `src/` (code), `data/` (ground truth), or `sprints/` (experiment log). No pure markdown commits except memory logs.

---

## 4. Committee Operating System

The committee is not a chat. It is a **distributed review queue** with defined APIs.

### Trigger Conditions

| Persona | Trigger | Input Artifact | Output Deliverable | Model |
|---------|---------|----------------|-------------------|-------|
| **Rival** | Sprint day 8, or when ZeroClaw claims a number is "good" | The claim + the script that produced it | GitHub Issue: falsification pair or confound proof | DeepSeek-Reasoner (sharp, adversarial) |
| **Devil's Advocate** | Sprint day 9, or when a new abstraction is introduced | The abstraction + the boring explanation | `committee/devils_advocate/NN.md`: prior art + baseline demand | DeepSeek-Reasoner (slow, grudging) |
| **Ideator** | Only when ZeroClaw is stuck for >48hrs | The stuck problem + current approach | `committee/ideator/NN.md`: 3 wild analogies, one actionable pivot | GLM-5.3 (lateral) |
| **Scout** | Sprint day 1, or on Lucineer's commission | Research question | `research/scouts/NN.md`: landscape survey + closest prior art | DeepInfra Seed-2.0-mini (wide) |
| **Lucineer** | Gate reviews, sprint aborts, final go/no-go | Phase deliverable | Approval or kill directive | Human (you) |

### The Rival's Mandatory Output Format

Every Rival issue must contain:
1. **The Falsification Pair:** Two conversations where the edge-matcher is wrong.
2. **The Confound:** A single variable (length, speakers, topic) that explains the score better than vibe.
3. **The Complexity Tax:** If ZeroClaw used vMF or fancy math, prove cosine similarity performs within 5%.

If the Rival cannot produce all three, the attack is invalid and ZeroClaw ignores it.

### The Devil's Advocate's Mandatory Output Format

1. **The Boring Explanation:** "What you are actually doing is..."
2. **The Prior Art:** Closest 3 papers/repos. If none exist, say so explicitly.
3. **The Baseline Table:** ZeroClaw's score vs. TF-IDF cosine vs. random. Must beat at least one.

---

## 5. Artifact Pipeline (The Code Architecture)

This is what gets built, in order.

```
zeroclaw-dissertation/
├── src/
│   ├── dial_bank.py              # Phase 1: The 9 dimensions, locked
│   ├── edge_extractor.py         # Phase 1: (before, after, displacement) tuples
│   ├── edge_matcher.py           # Phase 2: scalar sameness score
│   ├── reader_delta.py           # Phase 3: baseline calibration + delta extraction
│   ├── quilt_adapter.py          # Phase 4: emits vibe-weight to Quilt cell
│   └── deadman.py                # Every phase: executable gate checks
├── data/
│   ├── human_labels.json         # Phase 1: 50+ pairs, Lucineer + ZeroClaw tagged
│   ├── process_edges/            # Self-referential: committee debates as edges
│   └── external_edges/           # Non-committee conversations (CRITICAL)
├── sprints/
│   ├── 01_dial_bank_lock/
│   ├── 02_baseline_correlation/
│   └── ...
├── committee/
│   ├── rival/
│   ├── devils_advocate/
│   └── ideator/
├── research/
│   ├── dial_bank.md              # Defense of the 9 dimensions
│   ├── field_edge_formalization.md
│   └── registrations/            # Pre-registered experiments
└── memory/
    └── YYYY-MM-DD.md
```

### The 9-Dial Bank (Phase 1 Lock)

You must defend each dial in `research/dial_bank.md`. No more than 9. Current candidates:

| Dial | Definition | Why It Survives |
|------|-----------|-----------------|
| `warmth` | Affective temperature of the room | Core to "vibe" |
| `tightness` | Constraint vs. looseness in discourse | Captures decision-making mode |
| `earnestness` | Sincerity vs. performative distance | Separates real conflict from theater |
| `cynicism` | Suspicion of motives | Anti-correlate with earnestness (sanity check) |
| `joke_landing` | Successful humor vs. tension-release | Social lubricant signal |
| `panic` | Disruption of expected flow | Edge detection trigger |
| `presence` | Attention density in the room | Anti-correlate with distraction |
| `charisma_pull` | Centripetal force of dominant voice | Measured via anti-lens displacement |
| `turn_volatility` | Rate of speaker/silence change | Structural proxy for energy |

**Rule:** If any two dials correlate >0.9 in your first 50 samples, kill one.

### The Edge Extractor (Phase 1)

```python
# src/edge_extractor.py
def extract_edge(transcript: list[Turn], event_idx: int, window: int = 30) -> Edge:
    """
    Returns (before_vector, after_vector, displacement_vector).
    before: mean dial readings of [event_idx - window : event_idx]
    after:  mean dial readings of [event_idx : event_idx + window]
    displacement: after - before (signed)
    """
```

**Input:** A transcript with per-turn dial annotations (human or model-labeled).
**Output:** An `Edge` dataclass: `(before: np.ndarray[9], after: np.ndarray[9], displacement: np.ndarray[9])`.

### The Edge Matcher (Phase 2)

```python
# src/edge_matcher.py
def edge_similarity(e1: Edge, e2: Edge, method: str = "cosine") -> float:
    """
    Compares displacement vectors.
    Options: cosine, vMF_mle, euclidean.
    """
```

**Deadman switch script (`src/deadman.py`):**
```python
def phase_2_gate():
    # Run edge_matcher on 50 human-labeled pairs
    # Compute Pearson r between matcher score and human "same vibe" label
    # Gate: r > 0.4 AND fine_gap_mean > 0.1 across 3 runs
    # If fail: disable edge_matcher, enable snapshot_retrieval fallback
```

---

## 6. Data Architecture (The Self-Referential Loop, Made Concrete)

This is the most important design decision. The "dissertation is the dataset" claim is only true if the process data and external data flow through the **same schema**.

### The Unified Edge Schema

Every conversation — whether a committee debate, an external meeting, or a therapy session — is logged as:

```json
{
  "edge_id": "uuid",
  "source": "committee_rival_pass" | "external_corpus" | "quilt_cell",
  "transcript_hash": "sha256",
  "participants": ["zero_claw", "rival", "deepseek"],
  "before_vector": [0.2, 0.1, ...],
  "after_vector": [0.4, 0.3, ...],
  "displacement_vector": [0.2, 0.2, ...],
  "event_type": "thesis_attack" | "consensus" | "conflict",
  "human_label": {"same_as": "edge_id_2", "confidence": 0.8},
  "reader_deltas": {
    "zero_claw": {"baseline": [...], "delta": [...]},
    "rival": {"baseline": [...], "delta": [...]}
  }
}
```

### The Process Harvester

A script (`src/harvester.py`) runs after every committee session:

1. Parses the debate transcript.
2. Labels each turn with the 9 dials (using a lightweight model or heuristic).
3. Extracts edges at natural breakpoints (thesis proposed → attack delivered → resolution).
4. Writes to `data/process_edges/`.
5. **Critical:** Also samples a random subset into `data/external_edges/` by running the same pipeline on non-committee conversations (your actual target domain).

### The Sampling Rule

**At all times, `data/external_edges/` must be ≥50% of the dataset.** If the self-referential loop dominates, you have built an AI that only understands academic argument. The architecture enforces this with a CI check:

```yaml
# .github/workflows/data_balance.yml
- name: Check data balance
  run: python src/check_balance.py --min_external 0.5
```

---

## 7. Reader-Relative Calibration (Phase 3)

This is where the "Nurse JEPA" becomes executable.

### Baseline Protocol

For every reader (AI persona or human):
1. Collect 10 "neutral" conversations with that reader.
2. Compute mean dial vector = `baseline`.
3. For any new conversation, `delta = observed - baseline`.

### The Personal-Elephant Function

```python
# src/reader_delta.py
def personal_elephant(reader_id: str, conversation: Edge) -> np.ndarray:
    baseline = load_baseline(reader_id)
    return conversation.displacement - baseline
```

**Deadman switch:** On held-out readers, can the system predict the reader's delta better than it can predict the room's absolute state? If not, Personal-Elephant is just Room-Elephant with extra steps. Kill it.

---

## 8. Quilt Graft (Phase 4)

The final integration. Quilt is "a spreadsheet where every cell is a live capability."

### The Vibe Cell

A Quilt cell of kind `listener` that:
1. Receives conversation stream via WebSocket.
2. Runs `edge_extractor` in a sliding window.
3. Emits a `vibe_weight` (the displacement vector) to the dependency graph.
4. Updates the co-linear dataset via `quilt_adapter.py`.

### The Co-Linear Dataset

Not a database. A **living similarity graph**:
- Nodes: Edges (conversations).
- Edges: `sameness_weight = edge_matcher(n1, n2)`.
- Updated incrementally. No retraining. No batch jobs.

```python
# src/quilt_adapter.py
def on_conversation_end(cell_id: str, transcript: list[Turn]):
    edge = extract_edge(transcript, event_idx=len(transcript)//2)
    for neighbor in graph.nearest(edge, k=5):
        weight = edge_matcher(edge, neighbor)
        graph.update_edge(edge.id, neighbor.id, weight)
```

---

## 9. Falsification Protocol (Executable, Not Documented)

Every deadman switch is a Python script in `src/deadman.py` that returns exit code 0 (pass) or 1 (fail). CI runs it. No human judgment.

| Phase | Script | Gate | Fallback |
|-------|--------|------|----------|
| 1 | `phase_1_gate()` | Human label correlation r > 0.3 | Redesign dial bank |
| 2 | `phase_2_gate()` | Fine gap opens 0.015 → 0.271 across 3 runs | Cross-room snapshot retrieval only |
| 3 | `phase_3_gate()` | Reader delta F-score > 0.7 on held-out | Use room-absolute only |
| 4 | `phase_4_gate()` | Quilt cell emits weight < 100ms latency | Batch mode only |

---

## 10. Tool Assignments (Who Runs What)

| Task | Tool/Model | Why |
|------|-----------|-----|
| ZeroClaw reasoning | z.ai GLM-5.3 | Your doctoral student |
| Rival attacks | DeepSeek-Reasoner | Sharp, adversarial, no loyalty |
| Devil's Advocate | DeepSeek-Reasoner (different system prompt) | Slow, grudging, demands citations |
| Ideator | GLM-5.3 (temperature 0.9) | Lateral, metaphorical |
| Scout/landscape | DeepInfra Seed-2.0-mini | Cheap, wide, fast |
| Code implementation | kimi-cli | Your build tool |
| Embeddings | deepinfra MCP | Vector ops |
| Quilt integration | opencode | Fleet tooling |

---

## 11. The One Deliverable That Matters

In 10 weeks, you should be able to run:

```bash
python src/pipeline.py \
  --input conversation_a.txt \
  --input conversation_b.txt \
  --output sameness_score.json
```

And get a number that correlates with human judgment. Everything else — the dissertation document, the Quilt graft, the self-referential dataset — is downstream of that executable.

**Your next action:** Exit Phase 0. Lock the dial bank. Generate 50 human labels. Run the first deadman switch.

Does this architecture feel like something ZeroClaw can execute, or is there a specific phase you want to drill deeper on?

