# TypeScript Audit — Worker & Memory Services

**Date:** 2026-08-03
**Scope:** `lucineer-worker/src/` (relay + Durable Object), `lucineer-memory/src/` (D1-backed memory API)
**Method:** Full read of all source files, `npx tsc --noEmit` on both projects, inspection of `tsconfig.json` / `wrangler.jsonc` / generated `worker-configuration.d.ts`

---

## Headline Finding

`lucineer-worker` compiles clean under `strict: true` — zero `tsc` errors. `lucineer-memory` has **no TypeScript compiler in the project at all**: no `tsconfig.json`, no `typescript` devDependency, no local `tsc` binary. Confirmed by running `npx tsc --init --dry` in that directory, which resolved to nothing installed.

That means the type safety story for these two services is not "does it compile" — one of them literally never has. It's "how much of what's written as TypeScript is actually checked, versus asserted by hand." Most of the real gaps below are of the second kind: code that type-checks (or would, if it were checked) only because an unsafe cast tells the compiler to trust it.

---

## 1. `lucineer-worker` — Type Safety

### 1.1 Two different `Env` types, silently diverging

`src/types.ts` hand-declares:

```ts
export interface Env {
  LUCINEER_SESSION: DurableObjectNamespace;
  LUCINEER_INTERNAL_KEY: string;
  LUCINEER_KEY?: string;
  LUCINEER_SHARED_SECRET?: string;
  LUCINEER_TRAJECTORIES: R2Bucket;
  OPENCLAW_CALLBACK_URL?: string;
}
```

`index.ts` imports and uses *this* `Env` explicitly. But `worker-configuration.d.ts` — the file `wrangler types` generates and that `tsconfig.json`'s `"types"` array points at — declares its **own**, ambient, global `Env`:

```ts
interface __BaseEnv_Env {
  OPENCLAW_CALLBACK_URL: "http://172.22.219.126:18789/api/lucineer/message";
  LUCINEER_SESSION: DurableObjectNamespace<import("./src/index").LucineerSession>;
}
interface Env extends __BaseEnv_Env {}
```

`src/do/LucineerSession.ts` does `extends DurableObject<Env>` with **no import** — it binds to this ambient global, not the one in `types.ts`. So the two files in the same service use two different shapes for `Env`:

| Field | `types.ts` `Env` (index.ts) | generated `Env` (LucineerSession.ts) |
|---|---|---|
| `LUCINEER_SESSION` | `DurableObjectNamespace` (untyped) | `DurableObjectNamespace<LucineerSession>` (typed!) |
| `LUCINEER_TRAJECTORIES` | `R2Bucket` | **missing** |
| `LUCINEER_INTERNAL_KEY` / `LUCINEER_KEY` / `LUCINEER_SHARED_SECRET` | present | **missing** |
| `OPENCLAW_CALLBACK_URL` | optional, and dead per §1.4 | **required** |

The generated file is also stale in its own right: `P0_WORKER_FIXES.md` records that `OPENCLAW_CALLBACK_URL` was removed from `wrangler.jsonc`, and the current `wrangler.jsonc` confirms it — no `vars` block at all. The checked-in `worker-configuration.d.ts` still requires it, meaning `wrangler types` hasn't been re-run since that change.

**Why this hasn't broken anything yet:** `LucineerSession.ts` never references `this.env.*` (confirmed by grep — zero matches). The moment someone adds `this.env.LUCINEER_TRAJECTORIES` or `this.env.LUCINEER_SHARED_SECRET` inside the DO to implement cross-service auth or write trajectories from within the DO, it will either fail to compile against the stale ambient `Env`, or — if `wrangler types` is re-run first — silently succeed against a freshly regenerated `Env` that still won't match what `types.ts` assumes index.ts is passing in.

**Fix:** run `npx wrangler types` to regenerate `worker-configuration.d.ts` from the current `wrangler.jsonc` (this alone fixes the `OPENCLAW_CALLBACK_URL` staleness and adds `LUCINEER_TRAJECTORIES`), delete the hand-rolled `Env` in `types.ts`, and have `index.ts` import the single generated `Env`. Note the generated `Env` won't include `LUCINEER_INTERNAL_KEY` / `LUCINEER_KEY` / `LUCINEER_SHARED_SECRET` either, unless those are declared under `vars` (as plaintext, not recommended) or, correctly, as `wrangler secret put` bindings reflected via `wrangler types`.

### 1.2 Non-generic `DurableObjectNamespace` forces an unsafe double cast

Because `types.ts`'s `Env.LUCINEER_SESSION` is `DurableObjectNamespace` (no type parameter) rather than `DurableObjectNamespace<LucineerSession>` — which the generated file shows is available — `index.ts` can't get RPC method types from the stub directly. It works around this in `sessionStub()`:

```ts
function sessionStub(env: Env, sessionId: string) {
  return env.LUCINEER_SESSION.getByName(
    encodeURIComponent(sessionId),
  ) as unknown as import("./types").LucineerSessionRPC & { diag(): Promise<Record<string, unknown>> };
}
```

Casting through `unknown` disables all structural checking at this boundary — every `stub.foo()` call site in `index.ts` is trusted, not verified, against what `LucineerSession` actually implements. This isn't hypothetical drift: `LucineerSession` never declares `implements LucineerSessionRPC`, so nothing enforces the two stay in sync, and `diag()` — a real method on the class — isn't part of `LucineerSessionRPC` at all. It only type-checks because it's bolted onto this one cast site via an intersection type. Any other file wanting to call `.diag()` on a stub would have to redeclare the same workaround.

**Fix:** type `LUCINEER_SESSION` as `DurableObjectNamespace<LucineerSession>` (requires `types.ts` to import the class, or moving to the generated `Env`), add `diag()` to `LucineerSessionRPC`, and have the class declare `implements LucineerSessionRPC` so the compiler catches drift instead of a cast papering over it.

### 1.3 Unsafe `any` and unchecked `as T` on request bodies

- `index.ts:259` — `stub.updateWorldState(body.sessionId, body.worldSnapshot as any)`. This is the one call site where the `WorldSnapshot` type would actually matter, and it's turned off entirely.
- Every POST handler does `body = (await request.json()) as IncomingMessage` (or `JobResult`, or an inline ad hoc type at `/api/state`) with no runtime schema validation. Presence is checked (`!body.sessionId`) but not shape — an object or number sent where a string is expected passes the falsy check (`!{}` is `false`) and gets bound into SQL as whatever `String()`/direct-bind coercion produces. `/api/message` is the one endpoint explicitly documented as unauthenticated (`// No auth required — the Roblox client doesn't have the internal key`), making it the most exposed of these.
- `LucineerSession.ts`'s `rowToJob()` casts `row["status"] as Job["status"]` — a 4-value union — straight off a SQLite `TEXT` column with no guard, and `getJob`/`getWorldState` similarly `JSON.parse(...) as BuildCommand[]` / `as WorldSnapshot` with no validation that the parsed value matches the shape.

None of this is a `tsc` error — every one of these lines type-checks. That's the point: `strict: true` catches missing/incompatible types, not incorrect claims about external data. A schema-validation layer (zod, valibot, or even a handful of manual type guards at the three or four points where external JSON enters the system) would close this without changing much else.

### 1.4 Dead / incomplete interface surface

- `OPENCLAW_CALLBACK_URL?: string` in `types.ts`'s `Env` is vestigial — the push path was deleted (comment at `index.ts:106-108` confirms), `wrangler.jsonc` has no `vars` block, and yet the field is still declared in `types.ts` and still required in the stale generated file (§1.1). Three places disagree about whether this variable exists.
- `LucineerSessionRPC.getMessageHistory` is declared and implemented but **never called** — no route in `index.ts` invokes it. It's the same "built, deployed, wired to nothing" pattern `ROADMAP_whats_next.md` documents for the memory and vector services, just one layer down inside the relay itself.
- `POST /api/jobs/claim`'s multi-session fan-out (`index.ts:205-237`) is shaped like it claims across sessions (`for (const sid of sessionIds) { ... }`) but the comment admits it: `sessionIds` is either a single `?sessionId=` query param or `["default"]` — there's no actual discovery of active session IDs, so the loop only ever runs once. The code *looks* more complete than it is.

### 1.5 Zero test coverage

`@cloudflare/vitest-pool-workers` is a devDependency; there is no `*.test.ts`, no `*.spec.ts`, no `test` script in `package.json`, and no vitest config. The harness was added but never used. This matches `ROADMAP_whats_next.md`'s "zero integration tests" finding — worth noting it's not just missing at the system level, it's missing at the unit level too, in a project that already paid the dependency cost of setting it up.

---

## 2. `lucineer-memory` — Type Safety

### 2.1 No compiler, at all

`package.json` has two devDependencies: `@cloudflare/workers-types` and `wrangler`. No `typescript`, no `tsconfig.json`, no `types` array anywhere. `npx tsc --init --dry` in the directory resolves to nothing installed. `wrangler dev` / `wrangler deploy` transpile the file through esbuild, which strips types without checking them.

Practically: every `Env` field, every `String(body.x || "")` coercion, every `env.DB.prepare(...).first()` result cast has **never been checked by anything**, ever, including at write time. `@cloudflare/workers-types` gives editor autocomplete for `D1Database`, `Request`, etc., but with no `tsconfig.json` there's nothing enforcing it project-wide, and CI (if any is added later) has nothing to run. This is the single largest completeness gap of the two services — bigger than any individual cast in the worker, because it means the "TypeScript" in this file is currently unenforced convention, not a type system.

**Fix:** add a `tsconfig.json` mirroring the worker's (`strict: true`, `types: ["@cloudflare/workers-types"]`), add `typescript` as a devDependency, add a `typecheck` script, and run it in whatever CI/pre-deploy step exists (or add one).

### 2.2 Broad coercions swallow malformed input silently

`String(body.player_name || "")`, `Number(body.command_count ?? 0)`, etc. run throughout every handler. `String({foo: 1})` "succeeds" and stores `"[object Object]"`; `Number("abc")` is `NaN` and gets bound into SQLite with no rejection. There's no schema validation library here either — same shape of gap as `lucineer-worker` §1.3, but with no compiler behind it at all to catch even the categories of mistake `tsc` normally would (e.g., passing the wrong number of arguments, or a genuinely incompatible type at a call site within the file).

### 2.3 Untyped D1 results trusted directly

`env.DB.prepare(...).first()` returns `Promise<Record<string, unknown> | null>` from `@cloudflare/workers-types`. The code accesses `result?.id` (lines 145, 154, 192) as if it's typed, with no local interface describing what a `player_profiles` / `build_history` / `skills` row actually looks like. Combined with §2.1, there is currently no path — compiler or otherwise — by which a column rename in `schema.sql` would be caught before it breaks a handler at runtime.

### 2.4 `LUCINEER_SHARED_SECRET` duplicated with no shared contract

The auth header name (`X-Lucineer-Key`) and the shared-secret comparison logic are hand-written independently in both `lucineer-worker/src/types.ts`/`index.ts` and `lucineer-memory/src/index.ts`. Nothing enforces they stay compatible — no shared package, no shared type, no shared constant. This is a completeness gap more than a type-safety one, but it's the kind of thing that silently breaks inter-service auth the next time either file is touched without the other in mind.

---

## 3. Summary Table

| # | File(s) | Issue | Severity |
|---|---|---|---|
| 1.1 | `types.ts`, `worker-configuration.d.ts`, `LucineerSession.ts` | Two divergent, one stale, `Env` types across the same service | High — latent, will surface the next time the DO reads `this.env` |
| 1.2 | `index.ts` `sessionStub()` | Non-generic `DurableObjectNamespace` forces `as unknown as` double cast; `LucineerSession` doesn't `implements LucineerSessionRPC` | Medium |
| 1.3 | `index.ts`, `LucineerSession.ts` | Unsafe `as any` / unchecked `as T` on all external JSON in and DB rows out | Medium — highest risk at the one unauthenticated endpoint |
| 1.4 | `types.ts`, `index.ts` | Dead `OPENCLAW_CALLBACK_URL` field; unreachable `getMessageHistory`; `jobs/claim` fan-out that doesn't actually fan out | Low–Medium |
| 1.5 | `package.json` | Test harness installed, never used; zero tests | Medium |
| 2.1 | whole `lucineer-memory` project | No TypeScript compiler configured at all | **Highest** — nothing here has ever been type-checked |
| 2.2 | `index.ts` | Silent coercion of malformed input (`String()`/`Number()` fallbacks) | Medium |
| 2.3 | `index.ts` | Untyped D1 row access | Low–Medium |
| 2.4 | both services | Shared-secret auth contract duplicated by hand, no shared type | Low |

---

## 4. Persistence Layer D1 Schema — What Was Designed

Per `INTEGRATED_ARCHITECTURE.md` §3 (Layer 0 / Persistence) and the detailed specs in `PERSISTENCE_LAYER_DESIGN.md` and `CHISEL_PATTERN_DESIGN.md`, a migration covering the four requested stores — **Tubes, Guano, Claw Marks, Grain** — has been written to:

```
lucineer-memory/schema-persistence.sql
```

It follows the repo's existing convention of flat, hand-applied `schema-*.sql` files (matching `schema-achievements.sql`, `schema-eras.sql`, `schema-saves.sql`) rather than introducing `wrangler d1 migrations`' numbered-directory format, for consistency with what's already there. It was validated by executing it against a scratch SQLite database — all 9 new tables plus `schema_info` create cleanly with no syntax errors.

**Tables added:**

| Store | Tables | Notes |
|---|---|---|
| Tubes | `tubes`, `tube_patches`, `session_records` | `tube_patches` is append-only (never updated in place), matching the "cumulative wear" design principle |
| Guano | `behavioral_patterns`, `guano_decay_runs` | Only the SOIL tier lands in D1 per the design (FRESH/COMPOSTING are R2, SUBSTRATE embeddings live in Vectorize referenced by `embedding_id`); `guano_decay_runs` implements the doc's explicit "decay is observable" requirement |
| Claw Marks | `prompt_history`, `config_patches` | Covers the two D1-mapped categories (polished marks, fossilized marks); LoRA adapters (grooved marks) stay in R2 per the design and aren't D1 rows |
| Grain | `grain_entries`, `grain_patterns` | Field-for-field from `CHISEL_PATTERN_DESIGN.md`'s `GrainEntry`/`GrainPattern` types, including `context_bucket` on patterns to support the documented "max 50 patterns per tool per context-bucket" pruning rule |

**Deliberately excluded:** Lineage (`lineage_chains`, `agent_reproductions`) — the fifth Layer-0 component in the architecture doc's table mapping — was not requested and is not part of this migration.

**Important caveat, restated from `ROADMAP_whats_next.md`:** this entire layer is assessed at ~5% implemented and is explicitly filed as "Phase 2 design reference — not needed for MVP," alongside Chisel, Bridge, Swarm, and both Gamification docs. The roadmap's recommendation is to not touch any of this until the single-agent core loop (player message → build → reply) closes end-to-end. This schema exists so the design is ready to apply when that phase starts — applying it now doesn't unblock anything on the 21-hour critical path in the roadmap, and wiring code to it before the MVP loop works would be exactly the "generating instead of integrating" pattern the roadmap calls out as the project's real problem.

---

*Audit method: full source read (`lucineer-worker/src/{index,types,do/LucineerSession}.ts`, `lucineer-memory/src/index.ts`), `npx tsc --noEmit` in both projects, inspection of `tsconfig.json`, `wrangler.jsonc`, and generated `worker-configuration.d.ts`, cross-referenced against `INTEGRATED_ARCHITECTURE.md`, `ROADMAP_whats_next.md`, `PERSISTENCE_LAYER_DESIGN.md`, and `CHISEL_PATTERN_DESIGN.md`.*
