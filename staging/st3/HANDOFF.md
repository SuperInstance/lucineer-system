# ST3 HANDOFF — next hands-on (exec) turn runbook

Written during a read/write-only wake (2026-09-30 ~12:30 AKDT) so the next
exec turn is purely mechanical. Chip is IDLE until then — fire order below
puts GPU work first.

## Context at staging time
- **ST1v2 landed ~12:00** (crisp-meadow): results at
  `quilt-gpu-lab/results/st1v2_quilt_cell_v0/results.json` — **UNBOOKED**.
  Booking = first action. KEEP → cell-v0 = CANON pre-filter; KILL → pre-reg
  suspect list (label leakage audit, corpus/epochs, head capacity).
- **pong-quilt #85** resolution pushed (playtest-round-67) but PR red: branch
  runs its own pre-fix test.yml → `gh api -X PUT repos/{owner}/{repo}/pulls/85/update-branch`
  → green → `gh pr merge 85 --merge`. Also verify main is GREEN post-#86
  (`gh run list -R SuperInstance/pong-quilt -b main -L 3`) instead of trusting
  the 12:06 watch sample.
- **ollama** correct bundle downloaded (`/home/eileen/scratch/downloads/ollama-full.tar.zst`,
  1.33 GB, pid 48144 nohup curl): `zstd -t` → extract under /home → `file`
  bin+llama-server = non-empty x86-64 → `systemctl --user stop ollama` → swap
  (backup first) → start → smoke tev1:0.8b → `tools/local_jev_bench.py --model tev1:0.8b`.
  CPU-side — rides along while ST3 trains.

## ST3 fire order
1. `read` ST1's corpus builder: `/home/eileen/projects/quilt-gpu-lab/experiments/st1_quilt_cell_v0.py`
   → wire `load_corpus()` in `staging/st3/st3_calibrated_noul.py` (one line;
   the import self-diagnoses with a candidates list).
2. Copy both staged files in:
   - `staging/st3/st3_calibrated_noul.py` → `quilt-gpu-lab/experiments/st3_calibrated_noul.py`
   - `staging/st3/ST3-calibrated-noul.md` → `quilt-gpu-lab/proposals/runs/ST3-calibrated-noul.md`
3. **Book ST1v2 first** (RESULTS.md row + re-seal + push) — a result in hand
   beats two queued, and ST3's protocol step 6 feeds it to the cell if KEEP.
4. `git add experiments/st3_calibrated_noul.py proposals/runs/ST3-calibrated-noul.md`
   — EXPLICIT PATHS ONLY (never -A; 97fbce8 incident). Commit "ST3
   pre-registration (calibrated noul, frozen features)" → push.
5. Smoke (GPU): `/home/eileen/venvs/elephant-gpu/bin/python experiments/st3_calibrated_noul.py --smoke`
   — expect toy-ECE selftest OK, per-seed print, verdict SMOKE.
6. Fire full (background exec): 5 seeds, `--out results/st3_calibrated_noul`.
   ~minutes (frozen encoder + head-only). Book honestly per pre-reg
   interpretation; re-seal; receipts 6/6; push.
7. If jeff weights complete (`/home/eileen/scratch/external/jeff-checkpoints/jeff-0.8b/model.safetensors`
   non-empty): add the jeff-features arm as reported observation.

## Gates quick-ref (frozen in pre-reg)
G1 syn_auc≥0.95 · G2 real_auc≥0.80+fpr≤0.10 · G3 ECE≤0.05+Brier≤0.7×base ·
G4 risk≤0.10@cov90, ≤0.15@cov95 · G5 ood_abstain≥0.90+false_abstain≤0.20 ·
G6 control∈[0.45,0.55]. KILL paths pre-registered — no post-hoc rescue.
