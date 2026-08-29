# Zero-shot playtest — SuperInstance/quilt-mhs @ 0fbfe23 (Phase 215)

Date: 2026-08-27. Fresh clone to ~/projects/quilt-mhs-playtest. No prior context.
Local toolchain: cargo/rustc 1.97.1.

## Headline: as cloned, `cargo test --workspace` and `cargo build --workspace` FAIL AT MANIFEST PARSE. Nothing runs until 4 repairs.

### Repairs applied locally to measure anything (never committed/pushed)
1. Root Cargo.toml: removed `optional = true` from `ureq`/`tokio` in `[workspace.dependencies]` — illegal in Cargo.
2. Root Cargo.toml: removed `[features]` block from virtual manifest — illegal (already duplicated in member crate).
3. conformance.rs:179: added `(Ok(p), None) => fail(...)` match arm — E0004.
4. conformance.rs:179: added `(Ok(p), Some(_)) => fail(...)` unguarded arm — second E0004 (all original arms for those shapes were guarded; never compiled as committed).

## Measured test counts (after repairs, --no-fail-fast)
- lib: 0 | gen_schemas bin: 0 | conformance: 3/3 OK | devices: 11/14 | federation: 5/5 OK | laws: 11/11 OK | schemas: 2/3
- **TOTAL: 36 tests, 32 pass, 4 FAIL.** ("32" in claim = pass count, not total; "all green" false.)
- Plain `cargo test --workspace` (fail-fast) shows only 17 tests then aborts.

### The 4 failures (all deterministic, not environmental)
1. devices::laser_press_citation_is_in_tags — required citation string absent from laser manifest tags.
2. devices::plate_handler_overvolume_rejected — expected SafetyViolation, device returns GrantRequired("pipette.volume_ul_target is destructive"). Error-taxonomy mismatch.
3. devices::plate_handler_volume_under_grant_works — write under grant reads back 0.0, expected 150.0. Mock volume write is a no-op.
4. schemas::examples_parse_into_types — "unknown $type Program": test registry only accepts DeviceManifest|SafetyEnvelope|Command|Sample; all 8 new workflow files use Program/CliSession/McpToolTrace, which have NO Rust types at all. Repo's own contract test rejects its own examples.

## Claim vs reality table
| Claim | Verdict |
|---|---|
| 6 mock devices | VERIFIED (arm, thermal, incubator, microscope, plate-handler, laser) |
| 13 conformance checks C1–C13 | PARTIAL — all 13 emit a check; C12 is an unconditional `ok_assume` stub (always green, tests nothing). C10 code didn't compile as committed. |
| 32 tests, all green | FAILED — 36 total, 32 pass, 4 fail; AND suite cannot even compile/build as committed (2 manifest errors + 2 match non-exhaustiveness). |
| 8 runnable examples | FAILED/MISLEADING — 8 workflow JSONs exist and parse as JSON, but there is NO runner (only bin is gen-schemas), no CLI/executor, and their $type envelopes have no Rust types; repo's own parse test fails on them. They are static docs-as-JSON, not runnable workflows. |
| 7 docs | VERIFIED (undercount) — docs/ has 9 .md (1332 lines): 5 audit reports + integration-guide + device-cookbook + diff-day-runbook + Phase-215-EXPANSION-PLAN. All named files exist with real content. |
| (implied) clean build | FAILED — 0 warnings after repair, but 4 compile-blocking defects as committed; 1 warning in test code (unused import mock_plate_handler in tests/devices.rs). |

## Other notes
- 4 legacy .example.json files DO validate against their schemas (jsonschema 4.19.2): command, device-manifest, safety-envelope, telemetry-sample — all VALID.
- Committed schemas match generated types (schemas.rs test that passed).
- Examples use hand-formatted multi-space JSON (not machine-generated) — cosmetic.
- Verdict for Casey: claim's "all green" is impossible as-committed — the workspace manifest is un-parseable by any cargo, so the report's numbers could not have come from a fresh clone. Post-repair, 4/36 red. Docs and mock-device counts are the only claims that fully hold.
