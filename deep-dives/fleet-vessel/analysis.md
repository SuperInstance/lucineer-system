# fleet-vessel — Deep Dive Analysis

## Overview
Git-native garbage collector for the Cocapn Fleet. Enforces "vibed specs" (human-authored configuration in markdown) against all repos in the fleet workspace. Automatically cleans disk space, removes forbidden files from git, compresses/archives old research, and posts enforcement actions to PLATO rooms.

## Architecture

### Identity (`vessel.py`)
- Fleet agent with ID "vessel", version tracking
- Connects to PLATO (fleet communication system) at `localhost:8847`
- Reads specs from `vessel_specs` PLATO room or local fallback file
- Posts actions to `vessel_actions` PLATO room
- Registers identity in `turbo_identity` room

### Spec System (`vessel.py` + `vessel_specs_default.md`)
Human-readable configuration with 11 spec keys:

| Spec | Default | Purpose |
|---|---|---|
| `disk_usage_max` | 80 (%) | Alert threshold |
| `rust_target_max_mb` | 200 | Max target/ dir size |
| `node_modules_allowed` | true | Allow in repos |
| `log_files_in_git` | forbidden | .log in git |
| `.env_in_git` | forbidden | .env in git |
| `node_modules_in_git` | forbidden | node_modules in git |
| `research_compress_after_days` | 7 | Compress old research |
| `research_delete_after_days` | 30 | Delete old research |
| `enforcement_level` | hard | soft (warn) or hard (delete) |
| `notify_telegram` | true | Ping on violations |
| `cleanup_schedule` | daily | hourly/daily/weekly/manual |

### Enforcement Engine (`enforce.py`)

**Disk Management:**
- `get_disk_usage()`: statvfs-based disk usage percentage
- `get_dir_size()`: recursive directory size calculator
- `cleanup_rust_targets()`: deletes target/ dirs over threshold
- `cleanup_node_modules()`: deletes node_modules if not allowed

**Git Hygiene:**
- `enforce_git_patterns()`: scans git-tracked files for forbidden patterns (.log, .env, node_modules)
- Uses `git ls-files` to enumerate tracked files
- Hard mode: `git rm --cached` to unstage forbidden files
- Soft mode: warning posted to PLATO

**Research Lifecycle:**
- `compress_old_research()`: auto-generates SUMMARY.md for old research dirs
- Compress at 7 days → create summary file
- Delete at 30 days → remove entirely
- Based on directory modification time

### PLATO Integration (`plato.py`)
- `register_vessel()`: announce identity to fleet
- `read_vibed_specs()`: pull live config from PLATO room
- `post_violation()` / `post_enforcement()`: report actions to fleet
- Graceful fallback to local specs if PLATO is unreachable

### Daemon Mode (`main.py`)
- Single run or continuous daemon
- Schedule: hourly/daily/weekly based on specs
- Systemd service ready (service file included)

## Key Patterns

1. **Specs as documentation**: configuration in human-readable markdown, not YAML/TOML
2. **Dual enforcement levels**: soft (warn only) vs hard (auto-delete) — operator choice
3. **PLATO as nervous system**: specs and actions flow through chat rooms, visible to all agents
4. **Graceful degradation**: falls back to local specs if network services are down
5. **Audit trail**: every enforcement action posted to a public room
6. **Proactive cleanup**: compress → delete lifecycle prevents accumulated cruft

## Technology
- **Language**: Python 3
- **Dependencies**: stdlib only (os, shutil, subprocess, pathlib)
- **Integration**: PLATO chat system, Telegram notifications
- **Deployment**: systemd service, cron, or manual run
