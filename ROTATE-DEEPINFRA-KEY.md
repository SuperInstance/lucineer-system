# 🔴 ROTATE YOUR DEEPINFRA KEY — SECURITY INCIDENT 2026-08-14

**Found:** 06:49 AKDT, during end-of-night push.
**Severity:** HIGH — live API key on a **public** GitHub repo.

## What happened

1. Overnight loops yesterday hardcoded API keys into workspace files, which were committed and pushed to `github.com/SuperInstance/lucineer-system` (**public**).
2. This morning's push got blocked by GitHub Push Protection — that's how I found it.

## Exposure summary

| Key | Status |
|-----|--------|
| **DeepInfra** (`zYuVMG…aPkl`) | 🔴 **EXPOSED — in pushed history of the public repo since yesterday evening.** Introduced in commits `4f3769a`, `3f9bdb4`, `2ae4230` (wesley journal, loop logs, S160-S169 pieces). Was in `run_panel.py`, `panel_helper.py`, `scripts/generate_cloud.py`, `memory/2026-08-13-afternoon.md`. |
| DeepSeek (`sk-0a57…e284c`) | ✅ Never pushed — push protection blocked its only commit (`bde435c`, cloudflare-worker/README.md). No public exposure. |
| Google Web Search (`AQ.Ab8R…xKQ`) | ✅ Never pushed — same blocked commit. |

## What I already did (06:49–07:00 AKDT)

- Scrubbed all three keys from the working tree — scripts now read `DEEPINFRA_API_KEY` / `DEEPSEEK_API_KEY` / `GOOGLE_API_KEY` env vars
- Collapsed the 6 key-bearing unpushed commits into one clean commit (`d253b49`) — verified zero secret blobs before pushing
- HEAD of master is now clean; push succeeded
- Swept the tree for other common secret patterns (AWS/GH/Slack/AIza) — nothing found

## What needs you (Casey)

1. **Rotate the DeepInfra key now** → deepinfra.ai → settings → new key, update `DEEPINFRA_API_KEY` in `~/.bashrc` + systemd service envs. This is the definitive fix; scrubbing history without rotation is cosmetic.
2. *(Optional but recommended)* Rotate DeepSeek + Google keys for hygiene — they never leaked publicly, but they sat in local git history overnight.
3. **Optional history scrub:** the old key remains retrievable from git history until rewritten. Say the word and I'll run a `git filter-repo` pass + force-push to purge it. Only worth it if you care about post-rotation residue; rotation kills the key's value either way.

## Rule going forward

No literal keys in any workspace file — ever. Env vars only. If a doc needs to show key config, it shows `your-key-here`.

— Lucineer, morning watch
