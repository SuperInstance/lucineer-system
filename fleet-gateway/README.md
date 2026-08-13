# fleet-gateway

Localhost API gateway sidecar — week 2 of the fleet infrastructure rebuild
(see `memory/kimi-infrastructure-proposal.md` §2.4). Every fleet process
calls the gateway, not the vendor. The gateway owns the two failure modes
that kill sessions: **dead API keys with no fallback**, and **no circuit
breaker**. Same idioms as `fleet-cns` / `murmur-plato-bridge`: tokio,
thiserror, tracing + env-filter, clap, plus axum (server) and reqwest
(rustls, streaming) for the proxy path.

## What it does

- Listens on `127.0.0.1:8787` (default) and proxies
  `ANY /v1/{provider}/{*path}` to the provider's `base_url`, with query
  string, streaming request and response bodies — O(chunk), no unbounded
  buffering.
- Strips the client's `Authorization` header and injects
  `Authorization: Bearer <current key>` plus any per-provider
  `extra_headers`. Key material comes from environment variables named in
  the config — literal secrets in config are banned.
- **Key chain rotation:** 401/403 marks the current key dead and retries
  once with the next key. 429 rotates if another key exists, else passes
  the 429 through. Non-auth 4xx (400/404/422…) passes through untouched —
  client bugs never rotate keys. Retries are only safe because request
  bodies are buffered up to `replay_buffer_cap_bytes` (default 1 MiB);
  larger bodies fail fast with 502 and a clear log line.
- **Circuit breaker per provider:** consecutive upstream 5xx / timeouts /
  auth-exhaustion count toward `breaker_threshold` (default 5). At
  threshold the breaker opens and requests get an instant JSON 503 — zero
  upstream calls — until `breaker_cooldown_secs` (default 60) elapses.
  Then exactly one half-open probe goes through: success closes the
  breaker, failure re-opens with doubled cooldown (cap 15 min). Success
  resets the counter.
- **`GET /healthz`:** JSON with uptime and per-provider breaker state,
  consecutive failures, remaining cooldown, and live/total key COUNTS —
  never key material.
- **CNS integration:** startup, key rotations, and breaker open/close are
  appended as JSONL events to `<spool_dir>/gateway.jsonl` (default
  `/home/eileen/.openclaw/state/cns-spool/`), which fleet-cns already
  tails. A missing/read-only spool dir produces one warning; telemetry
  never kills the gateway.
- Graceful SIGTERM/SIGINT shutdown. Startup config faults (unparseable
  config, no providers, duplicate names, bad header values) exit non-zero
  with a clear message. A provider whose env vars don't resolve starts
  with its breaker open — the gateway itself still serves.

## Configuration

Flags:

| flag | default | meaning |
|---|---|---|
| `--config <path>` | `/home/eileen/.openclaw/state/gateway.toml` | TOML config file |
| `--bind <addr>` | `127.0.0.1:8787` | listen address |

Config file (see `gateway.example.toml`):

```toml
[gateway]
spool_dir = "/home/eileen/.openclaw/state/cns-spool"
request_timeout_secs = 30

[[provider]]
name = "openai"
base_url = "https://api.openai.com"
keys = ["OPENAI_API_KEY", "OPENAI_API_KEY_BACKUP"]   # ENV VAR NAMES, never literal keys
breaker_threshold = 5
breaker_cooldown_secs = 60
# extra_headers = { "OpenAI-Organization" = "org-..." }
```

Logging: `RUST_LOG` env-filter (default `fleet_gateway=info`).

## Run (dev)

```sh
cp gateway.example.toml /tmp/gateway.toml   # edit to taste
export OPENAI_API_KEY=sk-... OPENAI_API_KEY_BACKUP=sk-...
cargo run -- --config /tmp/gateway.toml

curl -s http://127.0.0.1:8787/healthz | jq
curl -s http://127.0.0.1:8787/v1/openai/models   # proxied with injected auth
```

## Test

```sh
cargo test    # mock upstreams on ephemeral ports: rotation, 4xx passthrough,
              # breaker open/half-open/close, zero-key providers, healthz, spool events
cargo clippy --all-targets
```

## Install the systemd unit (manual, user-level)

Not installed by the build — system changes are deliberately out of scope.
The shipped `fleet-gateway.service` is a **user** unit
(`WantedBy=default.target`, `MemoryMax=256M`):

```sh
cargo build --release
mkdir -p ~/.config/systemd/user
cp fleet-gateway.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now fleet-gateway
journalctl --user -u fleet-gateway -f
# optional, to survive logout: loginctl enable-linger "$USER"
```

## Layout

```
src/main.rs       CLI (clap), logging, startup faults, shutdown signal
src/lib.rs        router + serve
src/config.rs     TOML schema + validation (env-name keys, header validation)
src/state.rs      AppState, Provider: key chain, rotation, breaker wiring, health
src/proxy.rs      proxy handler: auth injection, rotation loop, streaming responses
src/breaker.rs    circuit breaker (closed/open/half-open, doubling cooldown, 15min cap)
src/spool.rs      CNS spool event writer (tolerates missing/read-only spool dir)
src/health.rs     /healthz
src/error.rs      GatewayError (thiserror)
tests/test_gateway.rs   integration tests against mock upstreams
gateway.example.toml    config template (env var names only — no secrets)
fleet-gateway.service   user-level systemd unit (install manually)
```
