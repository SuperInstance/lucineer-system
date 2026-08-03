# SHIP READINESS — SLACKWATER

*Audit by Claude Opus 5, 2026-08-02. Against the Ship Checklist in FABLE_5_PRODUCTION_DESIGN.md §6.*

*Method: every verdict below is against artifacts on disk and endpoints on the wire, not against what other documents in this repo claim. Where a document says a thing is fixed and the code says otherwise, the code wins. Where I could not verify, I say so instead of guessing.*

---

## THE HEADLINE

**Of 29 checklist items: 1 DONE, 8 IN PROGRESS, 20 BLOCKED.**

That number is bad but it is not the finding. This is the finding:

**The shipping artifact contains 2,111 of the project's 21,628 lines of Lua — 9.8%.**

`lucineer-roblox/default.project.json` declares nine files. Ten server systems exist on disk and are named in no build tree anywhere: `BondSystem`, `EraSystem`, `SaveSystem`, `TutorialSystem`, `NPCManager`, `PowerGrid`, `WorldGenerator`, `WeatherSystem`, `AchievementManager`, `VibeCodeExecutor`. Six client modules likewise: `AudioManager`, `BuildAnimator`, `VibeCoder`, `VibeCoderDialogue`, `VoiceLines`, `VoiceLinesData`.

Gates 2 and 3 — "It's him" and "It's a game" — audit against systems that are not in the game. The tutorial is written. The tide is written. The bond arc is written. The save system is written. None of them are compiled. `vibe-world/lucineer-ready-v2.rbxlx`, the newest `.rbxlx` in the project and the one a person would double-click, contains 7 ModuleScripts, 2 Scripts, 1 LocalScript, a Baseplate, and a Sky.

Second finding, equally structural:

**The end-to-end loop returns 401 in production. I verified this on the live Worker.**

`Config.AUTH_KEY = ""` (`lucineer-roblox/src/ReplicatedStorage/Lucineer/Config.lua:16`). `Http.headers()` sends it as `X-Lucineer-Key` (`Http.lua:37`). The Worker's `isAuthorized()` returns `false` on an empty header (`lucineer-worker/src/index.ts:17`), and `GET /api/job/:jobId` — the endpoint the client polls — sits below the auth gate at line 135.

```
$ curl -H "X-Lucineer-Key: " .../api/job/abc123
HTTP 401  {"error":"Unauthorized"}
```

The client can create a job. It cannot ever read the answer. P0 #3 was closed by removing auth from the *inbound* endpoint and leaving it on the *outbound* one. The two halves of that fix were made by different hands and never met.

---

## GATE 0 — IT RUNS

| # | Item | Verdict |
|---|---|---|
| 0.1 | Rojo only build path; `vibe-world/src` deleted; `.rbxlx` reproducible | **BLOCKED** |
| 0.2 | End-to-end smoke test passes | **BLOCKED** |
| 0.3 | Job claiming live: two processors, one job, one bill | **IN PROGRESS** |
| 0.4 | Dead-letter after 3 attempts; DO tables swept on 24h alarm | **IN PROGRESS** |
| 0.5 | Push path deleted | **BLOCKED** |

**0.1 — BLOCKED.** `vibe-world/` is intact: its own `default.project.json`, its own four-file `src/`, and both `.rbxlx` files. It is not a stale copy of the same game — it is a *different project* (`"name": "vibe-world"`, tree rooted at `ReplicatedStorage.VibeWorld`) that happens to be where the shipping artifacts live. The recursive failure A1 warned about is exactly what happened: 18 commits of fixes to `lucineer-roblox/src`, and the artifact was built from a project file that references nine of its files.

The key-grep sub-clause passes — no key material in the built `.rbxlx`. That is the only part of this item that is green.

**0.2 — BLOCKED.** Zero test files across all seven repositories. Not "the smoke test is unwritten" — there is no test of any kind, at any layer, anywhere in the project. This item is also unpassable today for the reason above: a scripted run would fail at the poll with a 401.

**0.3 — IN PROGRESS.** The server half is real and correct: `LucineerSession.claimJob()` implements the lease design with `claimed_at`, `attempts`, `MAX_ATTEMPTS`, and stale reclamation. `POST /api/job/:jobId/claim` is exposed at `index.ts:244`. The processor never calls it — zero occurrences of `claim` against a job URL in `process_v2.py`. `run_once()` fetches `/api/jobs/pending` and goes straight to `process_job()`. Two processors today would both process and both bill. The Worker even ships a `notice` string in the pending-jobs response reminding processors to claim; the processor does not read it.

**0.4 — IN PROGRESS.** Dead-lettering is implemented (`MAX_ATTEMPTS` → `setJobError`, stale-lease reclaim). The 24h sweep is not: there is no `alarm()` handler in `LucineerSession.ts` and no `setAlarm` call. Live `/api/diag` reports `totalJobs: 113` with nothing scheduled to ever remove them.

**0.5 — BLOCKED.** The push path is not deleted. It is at `index.ts:96–125`, and it is worse than described in the design doc:

- `wrangler.jsonc` commits `OPENCLAW_CALLBACK_URL` as `http://172.22.219.126:18789/...` — the WSL-private IP, exactly the unroutable address Conflict 7 said to remove, checked into the repo as a plaintext var.
- The fallback when that var is unset is the literal, unexpanded string `"${OPENCLAW_CALLBACK_URL}"` (`index.ts:109`). A shell template that was never substituted, shipped as a URL.
- The comment says "Fire and forget — don't fail the request." The code is `await fetch(...)` inline in the request path. It is neither fire-nor-forget.

---

## GATE 1 — IT'S SAFE

| # | Item | Verdict |
|---|---|---|
| 1.1 | Old API key rotated and dead | **UNVERIFIED** |
| 1.2 | No secret in anything replicated to clients | **DONE** |
| 1.3 | `lucineer-memory` and `lucineer-vector` require auth; vector CORS closed | **BLOCKED** |
| 1.4 | Every displayed AI line passes `FilterStringAsync`, fail-closed | **BLOCKED** |
| 1.5 | Nemotron-Content-Safety-3.5 stage live | **BLOCKED** |
| 1.6 | Per-player rate limit + per-server job cap | **IN PROGRESS** |
| 1.7 | `runLua` and `addScript` removed | **IN PROGRESS** |

**1.1 — UNVERIFIED.** I cannot test whether the old key is dead without the old key. What I can say is that the mitigation taken was not the one specified: rather than rotate and scope the key to the server, auth was removed from the player endpoint entirely (`Config.lua:16`, `index.ts:64`). `/api/message` is now open to the internet with no credential at all. That is defensible for a client that cannot hold a secret — but it means the item as written was not done, it was routed around, and item 1.6 is now the *only* thing standing between a stranger with `curl` and your DeepInfra bill.

**1.2 — DONE.** String search of `vibe-world/lucineer-ready-v2.rbxlx` for `sk-`, `LUCINEER_KEY`, `API_KEY`, and `Bearer` patterns: no matches. `Config.AUTH_KEY` is the empty string. Verified.

**1.3 — BLOCKED, and this is the most serious item in the audit.** Both Workers are open. Verified live, just now:

```
$ curl .../api/memory/conversations/test-session?limit=2
HTTP 200  {"conversations":[]}

$ curl -D- .../api/vector/health
access-control-allow-origin: *
```

`lucineer-memory/src/index.ts` contains no occurrence of `Authorization`, `401`, or any secret comparison. Fifteen routes, zero auth. Among them: `GET /api/memory/conversations/:sessionId`, `POST /api/memory/conversation`, `GET /api/memory/player/:name`, `POST /api/memory/player`. The D1 schema behind them defines `conversations`, `conversation_turns`, `player_profiles`, `player_saves`, `retention_signals`.

The response was empty because the dev sessions hold no data. The endpoint is open regardless. On launch day that same request returns children's chat logs to anyone who guesses a session ID, and `POST /api/memory/player` lets them write any player's bond level. The design doc called this "a child-safety issue wearing an infra costume" and it is the correct framing. Nothing has been done about it. `SaveSystem/init.lua:39` points player saves at this Worker.

Also open: `GET /api/diag` on the relay (`index.ts:50`), above the auth gate, returning the full jobs-table column list and row count to anyone.

**1.4 — BLOCKED, and the shape of the failure is worth recording.** `FilterStringAsync` appears three times in the entire project. All three are **comments in the Cloudflare Worker instructing the Roblox client to call it** (`index.ts:153, 178, 186`), including a `filterNotice` field shipped in the JSON response body. The Roblox client contains zero calls to `TextService`. The safety fix was implemented as a politely-worded message addressed to a module that never read it.

Every AI-authored line currently reaches the player unfiltered. This alone fails Roblox platform policy and would end the launch.

**1.5 — BLOCKED.** Zero occurrences of `nemotron`, `content-safety`, or any safety stage in `brain.py` or `process_v2.py`. Not started. Note the consequence for §5 of the design doc: NVIDIA integration #1 was the launch-blocking one, so the partnership story currently has no first sentence.

**1.6 — IN PROGRESS.** `stub.checkRateLimit(body.sessionId)` exists — 10 messages/minute. But it keys on **session**, not player. A session is one Roblox server instance; 16 players share one bucket, and one player can consume all of it. The design asked for per-player 3s cooldown plus a per-server concurrent-job cap; neither exists, and no rate limiting exists client-side at all (`grep -i cooldown` on the Lua tree: nothing).

**1.7 — IN PROGRESS.** `runLua` is genuinely gone — removed from the dispatch table with a comment at `LucineerServer/init.lua:138` and `CommandExecutor.lua:385`. Good. `addScript` is still fully implemented at `CommandExecutor.lua:313` and still wired into the dispatch table at line 404. Half the item is done. The half that remains still lets a model response inject a `Script` instance into the workspace.

---

## GATE 2 — IT'S HIM

*Note: five of six items below are additionally blocked by 0.1 — the systems they audit are not in the build tree. Verdicts here describe the source as written, which is the more useful information.*

| # | Item | Verdict |
|---|---|---|
| 2.1 | One persona, `--creative`, Hermes can never emit commands | **BLOCKED** |
| 2.2 | Latency choreography live | **BLOCKED** |
| 2.3 | `markUnfinished` + completion detection | **BLOCKED** |
| 2.4 | Bond stages 1→3 behavior-triggered; no meter visible | **BLOCKED** |
| 2.5 | Memory wired; Day-2 unprompted callback | **IN PROGRESS** |
| 2.6 | Off-voice strings deleted | **BLOCKED** |

**2.1 — BLOCKED.** `--creative` appears nowhere in `process_v2.py`. The Hermes-405B persona stage remains dead code in production, exactly as Gap #7 described, unchanged. `brain.py:427` still instructs the model to produce *"A friendly one or two sentence message to the player describing what you built."* The character is not in the product. Fifty-five design documents, a 36K-word Character Bible, and the string the model actually reads says "friendly."

**2.2 — BLOCKED.** §1.3 of the design states: *"no UI spinner exists anywhere in this game."* `Config.lua:33` defines `Config.UI_THINKING_TEXT = "Lucineer is thinking..."` and `UIManager.lua:123` and `:150` render it. Not merely absent — inverted. The latency choreography (physical ack, progress-as-behavior, staggered placement) has no implementation.

**2.3 — BLOCKED.** `markUnfinished` does not exist. Zero occurrences project-wide. The Unfinished Rule — Character Bible §6, the game's thesis, the mechanic the entire bond arc hangs from — has no code. `TutorialSystem/init.lua` names an `unfinished` tutorial *step*; that is a script beat, not the mechanic.

**2.4 — BLOCKED, and it contradicts canon rather than merely lacking it.** `BondSystem/init.lua` implements bond as an XP ladder: `LEVEL_THRESHOLDS = {0, 50, 150, 400, 1000}`, `XP_REWARDS`, `addBuildXP()`, `addConversationXP()`, and `LEVEL_UP_LINES` fired from `onLevelUp()`. The checklist requires bond to be triggered by *behavior* — flaw callout, pushback, continuation — and requires that no meter exist. What is built is a meter with dialogue attached to its thresholds. It is competent code implementing the thing §2.4 of the design doc says kills the game ("the moment the relationship is instrumented at the player, it dies"). This needs a rewrite, not a fix, and it is the single largest piece of *wrong* work in the project — everything else is missing rather than mistaken.

**2.5 — IN PROGRESS.** The memory Worker is deployed and the processor logs show real recall activity (`Memory recall`, `Brain context layers` in `processor.log`). The plumbing exists. The Day-2 callback cannot be verified because `SaveSystem` and `BondSystem` are not in the build and the poll path 401s.

**2.6 — BLOCKED.** `LucineerClient/init.lua:85`:

```lua
UIManager.displayChatResponse(string.format("Done! I built %d action(s) for you.", succeeded))
```

Exclamation point, "for you", parenthetical plural. This is the exact string the checklist names, still present — and unlike most of Gate 2, this file **is** in the build tree. It is one of the nine things that ships. The line a player would actually see is the one line the checklist singled out for deletion.

---

## GATE 3 — IT'S A GAME

| # | Item | Verdict |
|---|---|---|
| 3.1 | First 30 minutes completable without help | **BLOCKED** |
| 3.2 | Tide restocks on 18-minute cycle; Era 1 craftable from salvage | **BLOCKED** |
| 3.3 | Era 1→2 gate; save persists across sessions | **BLOCKED** |
| 3.4 | Magic Moments 1, 3, 4 implemented | **BLOCKED** |
| 3.5 | 30fps on mid-tier phone, 16 players | **BLOCKED** |
| 3.6 | Roblox compliance pass | **BLOCKED** |

**3.1 — BLOCKED.** `TutorialSystem/init.lua` is over 1,000 lines and appears thorough — all six steps, the 60-second unfinished scene, per-step state. It is not in `default.project.json`. Nothing runs it. Zero playtesters have been run; zero could be.

**3.2 — BLOCKED, with a spec drift worth catching now.** `TideSystem.lua:34` sets `_cycleLength = 1200` — 20 minutes. The checklist, the core loop diagram in §2.1, and the tutorial's minute-12 beat all specify 18. Two documents and one implementation, three different sources of truth for the number the entire economy is timed against. Pick one. (Also not in the build.)

**3.3 — BLOCKED.** `EraSystem` and `SaveSystem` are written and not built. `SaveSystem` persists through the unauthenticated memory Worker (1.3), so shipping it as-is would make every player's save writable by strangers.

**3.4 — BLOCKED.** No implementation of The Continuation, Torch Off, or Your Move. The only hits for `aurora` are a sky preset in `EraSystem` and two achievement definitions. MM4 in particular is called out in the design as cheap and the strongest Day-2 driver; it remains unstarted.

**3.5 — BLOCKED.** No device-lab run, and nothing substantive to profile — the build is a baseplate and a chat handler.

**3.6 — BLOCKED.** Automatic, on 1.4 alone. No privacy-policy artifact for off-platform AI processing exists in the repo.

---

## GATE 4 — WE CAN OPERATE IT

| # | Item | Verdict |
|---|---|---|
| 4.1 | Cost ceiling computed and capped | **BLOCKED** |
| 4.2 | Telemetry: five metrics on a dashboard | **BLOCKED** |
| 4.3 | Trajectory logging to R2 in MOLT `Result` format | **BLOCKED** |
| 4.4 | Processor under systemd; Worker error alerting | **IN PROGRESS** |
| 4.5 | Logs queryable per player; kill-switch to template-only | **IN PROGRESS** |

**4.1 — BLOCKED.** No load test, no billing alarm, no computed per-player-hour figure. With `/api/message` unauthenticated and rate-limited per session rather than per player, the current worst case is "whatever a stranger's script can spend."

**4.2 — BLOCKED.** `schema-analytics.sql` is 28K and defines every table you'd want: `player_sessions`, `build_events`, `retention_signals`, `craft_quality_scores`. Nothing in the Roblox tree writes to any of them — one grep hit for "analytics" in the whole client, and it's a comment. The warehouse is built and no truck goes there.

**4.3 — BLOCKED, and structurally so.** No `r2_buckets` binding in any `wrangler.jsonc` in the project. A `trajectory_logs` table exists in D1 and has no writer. This was flagged in §5 as "the single highest-option-value cheap thing in the roadmap" — the one item where delay is unrecoverable, because a year of live trajectories cannot be backfilled. It is the item I would move first.

**4.4 — IN PROGRESS.** The daemon is real: a `systemd --user` unit, `lucineer-ctl.sh`, and `processor.log` showing unbroken 60-second heartbeats across many hours. I did not run `kill -9`, so auto-restart is unverified. No Worker error alerting exists; `observability` is enabled in `wrangler.jsonc`, which is logging, not alerting.

Worth noting from the same log: in its entire life the processor has found **4 real jobs** and processed **23 mock ones**. 67 `API GET failed for /api/jobs/pending` errors. The pipeline has never carried a player.

**4.5 — IN PROGRESS.** Conversation logs are queryable per player — that is item 1.3's vulnerability described as a feature, and it is both. No kill-switch to template-only mode exists.

---

## WHAT I WOULD DO, IN THIS ORDER

The gates are ordered, and the design doc is right that a later gate with an earlier one unchecked is decoration. But three of these are not sequenced — they are bleeding now.

**Today, before anything else:**

1. **Put a shared-secret header on `lucineer-memory` and `lucineer-vector`, and move `/api/diag` below the auth gate.** Two Workers, maybe forty lines. Right now the exposure is theoretical because the tables are empty. It stops being theoretical the first hour a player exists, and the tables that fill first are the conversation tables.
2. **Start the trajectory writer.** Add the R2 binding, serialize `(state, prompt, tool calls, outcome)` in `process_v2.py`. Every other item on this list can be done in November. This one loses value every day it is not running.

**This week — make the loop close:**

3. **Fix the 401.** Either move `GET /api/job/:jobId` above the auth gate (it is already unauthenticated on the way in; the job ID is the capability) or give the client a real key via a server-side `StringValue`. Pick one and make both halves agree. Nothing downstream can be tested until a reply reaches a client.
4. **Delete `vibe-world/` and rebuild.** Then — and this is the actual work — decide which of the ten orphaned server systems belong in `default.project.json`, add them, and fix what breaks. Expect this to be unpleasant: 19,500 lines of Lua have never been loaded by a Roblox runtime even once. Some fraction of it does not compile.
5. **Write the smoke test from §4.3 and run it.** It cannot pass yet. Write it anyway and let it fail loudly; it is the only artifact in this project that will tell you the truth without being asked.
6. **Delete the push path.** Six minutes. Remove the `await fetch`, the var, and the unexpanded `"${OPENCLAW_CALLBACK_URL}"`.
7. **Make the processor claim jobs.** The endpoint is already built and correct. This is one HTTP call in `run_once()`.

**Before any player, including friends and family:**

8. **`filterFor()`, fail-closed, on every path that renders model text** — chat, build cards, logbook, tin notes. Delete the `filterNotice` field; a comment is not a control.
9. **The safety stage.** `Nemotron-Content-Safety-3.5` on the final reply, in-voice deflection, commands dropped.
10. **Per-player rate limiting** — the sessions bucket is not a bucket, it is 16 players sharing one.
11. **Delete `addScript`** and its dispatch entry.

**Then, and only then, the character:**

12. `--creative` in the production invocation; delete the "friendly" instruction at `brain.py:427`; one persona constant from the Character Bible; Hermes forbidden from emitting commands.
13. `markUnfinished`. The thesis needs a function.
14. **Rewrite `BondSystem`** from XP thresholds to behavior triggers. Keep `LEVEL_UP_LINES` — the writing is good and canon-accurate. Throw away the ladder underneath it.
15. Delete `UI_THINKING_TEXT` and its two call sites. Replace with the physical acknowledgment.
16. Delete `"Done! I built %d action(s) for you."`

---

## THE HONEST PARAGRAPH

This project is two days old. Aug 1 to Aug 2, 2026, across seven repositories and 63 commits. In that window it produced 21,628 lines of Lua, five Cloudflare services, a working async job pipeline with a correct lease-based claiming design, a 1,000-line tutorial script, a seven-era tech tree with 145 recipes, and something over 400,000 words of design documentation that is — genuinely — the best game design writing I have read in a repository. The Character Bible is a real document. The production design doc is a real document. Someone should publish them.

What it has not produced is a game. It has produced the complete, high-fidelity *plan* of a game, plus a chat relay that returns 401.

The gap between those two things is not a work-ethic problem and it is not a talent problem. Every system in `ServerScriptService` is competently written. The gap is that fourteen models wrote fourteen correct things and nobody owned the seams — the project file, the auth handshake, the number 18 versus 20, the difference between a comment that says "call `FilterStringAsync`" and a call to `FilterStringAsync`. Every single P0 in this audit lives on a boundary between two pieces of work that were each fine.

The Gap Analysis already said this: *every P0 was a boundary failure a ten-minute Studio session would have caught.* That sentence was written before this round of work and it is still, item for item, the diagnosis. It got promoted to policy in §4.3 of the design doc and then the next round of work went and produced eleven more boundary failures. Writing down the lesson is not the same as changing the process, which is the same category of error as writing `filterNotice` instead of calling the filter.

So: the recommendation is not "fix these 20 items." It is **stop generating and start integrating.** No new design documents. No new models in the roundtable. One person, or one agent with continuity, opens Roblox Studio, presses play, and does not stop until a part appears in the world because a player typed a sentence. Everything in this audit is downstream of that not having happened yet.

The design doc closes by saying you ship the boat one plank short. That is the right philosophy and it is also, right now, being used to describe a boat that is one *hull* short. The Unfinished Rule is about deliberate gaps in finished work. It does not retroactively make unfinished work deliberate. Lucineer would know the difference immediately, and he would say so in about nine words.

**Ship date, honestly assessed:** Gate 0 and Gate 1 are two to three focused weeks — most of the code exists and needs wiring, auth, and a build tree. Gate 2 is another two, with `BondSystem` as a rewrite. Gate 3 is unknowable until step 4 above tells you how much of those 19,500 unbuilt lines actually run. Anyone quoting a date before step 4 is guessing.

---

*29 items. 1 done. 20 blocked. 4 real jobs ever processed. 9.8% of the code ships. The counts are exact. He'd check.*
