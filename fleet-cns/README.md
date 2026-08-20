# fleet-cns

Supervised spool-monitoring daemon — week 1 of the fleet infrastructure
rebuild (see `memory/kimi-infrastructure-proposal.md` §2.3). It tails a
directory of append-only JSONL spool files written by other fleet processes
and processes events reliably. Modeled on the in-fleet Rust service
`murmur-plato-bridge` (serde / serde_json / thiserror / tokio / tracing).

## The four failure modes it kills

1. **Crash on malformed JSON — structurally impossible.** A line that fails
   to parse (or parses as non-object JSON) is not an error of the daemon:
   the poison counter increments, the raw line plus spool filename, byte
   offset, and timestamp is appended to `<spool_dir>/dead-letter.jsonl`, the
   read offset advances past it, and processing continues. No code path
   panics on input data.
2. **Infinite hot loop on broken files.** Every loop iteration ends in a
   `tokio::time::sleep` (poll interval, backoff, or breaker cooldown) or the
   shutdown signal. Consecutive internal failures feed exponential backoff:
   100ms, doubling, capped at 30s, reset on success.
3. **Circuit breaker.** After N (default 5) consecutive *identical* internal
   errors (e.g. spool dir unreadable, dead-letter unwritable), the breaker
   opens: a loud `tracing::error!` alert, a 60s cooldown, and retries at
   cooldown cadence — never spinning, never exiting. The only non-zero exit
   is an unrecoverable configuration fault at startup (spool dir missing and
   `--create` not passed).
4. **Checkpointed offsets.** Per-file byte offsets persist to
   `<state_dir>/offsets.json` (atomic tmp + rename), batched: flush every 32
   consumed lines or 5s, whichever comes first, plus a final flush on
   shutdown. On restart the daemon resumes from offsets. A file smaller than
   its recorded offset was rotated/truncated: the offset resets to 0 with a
   warning and the file is re-read.

Memory is O(chunk): lines stream through a `BufReader` into a reused buffer;
files are never slurped. A trailing partial line (no newline yet) is left
unconsumed until the writer finishes it.

v1 processing: parse as `serde_json::Value`, require a JSON object, log at
`info` with the event fields, count it. A heartbeat logs every 60s: files
tailed, lines processed, lines dead-lettered, backoff state, breaker state.
Downstream sinks arrive in later weeks.

## Configuration

| flag | default | meaning |
|---|---|---|
| `--spool-dir <path>` | `/home/eileen/.openclaw/state/cns-spool` | JSONL spool directory to tail |
| `--state-dir <path>` | `/home/eileen/.openclaw/state/cns` | daemon state (`offsets.json`) |
| `--create` | off | create the spool dir if missing |
| `--poll-interval-ms <n>` | `250` | delay between scans (simple polling; no inotify in v1) |
| `--breaker-threshold <n>` | `5` | consecutive identical internal errors before the breaker opens |

Logging: `tracing-subscriber` with env-filter — set `RUST_LOG` (default
`fleet_cns=info`).

## Run (dev)

```sh
cargo run -- --create
# then, in another shell:
echo '{"kind":"ping","n":1}' >> /home/eileen/.openclaw/state/cns-spool/events.jsonl
echo 'total garbage'   >> /home/eileen/.openclaw/state/cns-spool/events.jsonl
# logs show one processed event + one dead-letter quarantine
```

Graceful shutdown on SIGTERM/SIGINT: offsets flush before exit.

## Test

```sh
cargo test    # poison lines, resume, rotation, breaker, config faults
cargo clippy
```

## Install the systemd unit (manual)

**Installed 2026-08-13 as a user-level unit** (no sudo needed; WSL2 has
lingering enabled for user `eileen`, so it starts at WSL boot). The live
unit is at `~/.config/systemd/user/fleet-cns.service` — identical to the
shipped `fleet-cns.service` except `User=`/`After=` are dropped and
`WantedBy=default.target`. Manage it with:

```sh
systemctl --user status fleet-cns
journalctl --user -u fleet-cns -f
```

For a system-level install instead (requires sudo):

```sh
cargo build --release
sudo cp fleet-cns.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now fleet-cns
journalctl -u fleet-cns -f
```

The unit pins `WorkingDirectory`/`ExecStart` to the paths under
`/home/eileen`, restarts `always` with `RestartSec=5` and
`StartLimitBurst=5`, and fences memory with `MemoryMax=512M`.

## Testing

`cargo test` — 15 tests: 6 daemon integration, 7 checkpoint, 2 breaker. All
timing knobs are bypassed (tests drive `tick`/`process_once` directly), so
the suite is fast and deterministic.

## Layout

```
src/main.rs       CLI (clap), logging (env-filter), signal handling, exit codes
src/lib.rs        crate surface
src/daemon.rs     Daemon: run loop, tick, heartbeat, per-file processing
src/spool.rs      spool scanning, O(chunk) line draining, dead-letter writes
src/checkpoint.rs offsets.json: batched atomic flushes
src/breaker.rs    circuit breaker (closed/open, cooldown)
src/error.rs      CnsError (thiserror)
tests/test_daemon.rs     integration tests (daemon lifecycle, dead-letter, rotation, resume)
tests/test_checkpoint.rs unit tests for offset batching, atomicity, corrupt-state recovery
fleet-cns.service     systemd unit (install manually)
```
