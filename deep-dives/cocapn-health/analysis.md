# cocapn-health — Deep Dive Analysis

## Overview
Zero-dependency fleet health monitoring system for the SuperInstance/Cocapn fleet. Provides HTTP/TCP/DNS/process/disk/memory/CPU health checks, fleet-wide service monitoring, alert rules with escalation, and EventBus integration for real-time state propagation.

## Architecture

### Core Module (`__init__.py`)
- **`ServiceDef`** dataclass: name, host, port, path, timeout, expect_status, headers, extract (JSON field extraction)
- **`CheckResult`** dataclass: name, ok, latency_ms, status, details, checked_at
- **7 check functions**: `check_http`, `check_tcp`, `check_dns`, `check_process`, `check_disk`, `check_memory`, `check_cpu`
- **`check_system()`**: batch disk + memory + CPU
- **`HealthChecker`**: takes a list of `ServiceDef`, runs `check_all()`, generates reports (JSON/Markdown/oneline)
- **`FLEET_SERVICES`**: 18 predefined fleet services on ports 4042-8899

### Monitor Module (`monitor.py`)
- **`HealthStatus`** enum: HEALTHY / DEGRADED / UNHEALTHY (threshold-configurable)
- **`AgentState`**: per-service tracking with consecutive_failures, consecutive_successes, total_checks, availability %, avg_latency, rolling history (100 entries max)
- **`HealthMonitor`**: orchestrates checks, computes overall_status based on up-ratio thresholds (degraded at <50%, unhealthy at <20%)

### Alert Module (`alert.py`)
- **`AlertRule`**: name, condition callable, severity (INFO/WARNING/CRITICAL), cooldown_seconds, escalation_after_failures
- **`HealthAlert`**: lifecycle states PENDING → FIRING → RESOLVED or ESCALATED
- **Built-in conditions**: `is_down`, `consecutive_failures(N)`, `low_availability(N)`, `high_latency(ms)`
- **`AlertManager`**: evaluates all rules against all agent states, manages cooldowns and auto-escalation

### Report Module (`report.py`)
- **`HealthReport`**: full snapshot with status, failing list, agent_summaries, alerts, system_checks
- Output formats: `to_json()`, `to_markdown()` (with emoji status table), `to_oneline()`

### Check Module (`check.py`)
- **`CustomCheck`**: user-defined check with name, callable, timeout, tags
- **`CheckRegistry`**: register via decorator or `add()`, run by name/tag/all
- **`CheckBuilder`**: fluent builder pattern (`.timeout().tag().build()`)

### Sunset Bridge (`sunset_bridge.py`)
- **`EventBusHealthChecker`**: extends HealthChecker, emits events on state transitions:
  - `service_down` (UP→DOWN), `service_recovered` (DOWN→UP), `fleet_health` (periodic snapshot)
- **Thermal snapshots**: CPU %, memory %, GPU utilization via psutil + nvidia-smi
- Graceful degradation: checks continue even if EventBus/psutil unavailable

### API Module (`api.py`)
- REST server on port 8899 with endpoints: `/health`, `/fleet`, `/system`, `/check/cpu`, `/check/memory`, `/check/disk`, `/refresh`
- **`HealthCache`**: TTL-based caching to avoid hammering services

## Key Patterns

1. **Zero-dependency design**: stdlib only (urllib, socket, subprocess, os, shutil) — drops into any Python environment
2. **Composable checks**: each check returns the same `CheckResult` dataclass → uniform processing
3. **State machine for alerts**: PENDING → FIRING → ESCALATED/RESOLVED with cooldown enforcement
4. **Thermal awareness**: health checks include thermal context (CPU/GPU/memory pressure) not just up/down
5. **Fleet-native**: 18 predefined services, environment variable override for host
6. **Watch mode**: CLI `--watch N` for continuous monitoring, `--fail` for CI exit codes

## Technology
- **Language**: Python 3.10+ (uses `|` union types)
- **Dependencies**: zero (stdlib only); optional: psutil, nvidia-smi, nexus.fleet_event_bus
- **Deployment**: pip package, Docker, CLI tool, REST API, systemd service
