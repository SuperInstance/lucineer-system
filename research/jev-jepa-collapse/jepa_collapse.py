#!/usr/bin/env python3
"""LANE 4 — JEV as a JEPA anti-collapse guard.

Question: can a calibrated judgment engine (typesafe.ai jev-latest, graded
noul 0..1) detect / prevent representation collapse in a minimal JEPA-style
world model, and does its judgment align with mathematical diversity metrics?

Phases (run incrementally, results checkpointed to collapse-results.json):
  1  data + env + ramp receipt + 1 smoke JEV call
  2  four training runs (frozen/unfrozen x mse/jevreg), monitor every 50 steps
  3  E5 comfortable-collapse probes (+ healthy = true next states)
  4  correlations + ablation summary

GPU law (INSTRUMENT-01): sustained ramp before any timing-sensitive section;
receipt stored in results.
"""
import argparse, hashlib, json, os, sys, time, urllib.request, urllib.error

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "collapse-results.json")
CACHE = os.path.join(HERE, "jev-cache.json")
KEYFILE = "/mnt/c/Users/casey/key.txt"
API = "https://api.typesafe.ai/v1/systemone"

SEED = 6611
N_TRANS = 500
FEAT_D = 16
LAT_D = 8
HID = 32
STEPS = 4000
MONITOR_EVERY = 50
LR = 1e-3
WD = 1e-4
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")

REGIMES = ["early-morning", "midday-away", "evening-home", "night"]
REGIME_NAMES = ["morning", "day", "evening", "night"]


# ------------------------------------------------------------------ data gen
def gen_world(n_pairs=500, seed=SEED):
    """Synthetic room states, 16 named features, hourly steps, multimodal events.

    Returns S0 (n,16) current states, S1 (n,16) next states, regimes (n,).
    """
    rng = np.random.default_rng(seed)
    feat_names = [
        "light", "temp", "humidity", "occupancy", "music", "door_open",
        "window_open", "mess", "plant_moisture", "air_fresh", "tod_sin",
        "tod_cos", "activity", "pet_awake", "heater_on", "blackout",
    ]

    def step_state(s, hour, rng, final=False):
        ns = s.copy()
        tod = hour % 24
        # occupancy schedule with stochastic midday presence
        if 8 <= tod < 18:
            occ = 0.0 if rng.random() < 0.8 else 1.0 + rng.random()
        else:
            occ = 1.0 + rng.random() * 2.0
        # events (multimodality): guest / cooking / cleaning / nap
        ev = rng.random()
        if ev < 0.08:
            occ = min(1.0, occ) + 2.0 + rng.random()  # guests arrive
            ns[4] = np.clip(ns[4] + 0.4, 0, 1)
            ns[7] = np.clip(ns[7] + 0.3, 0, 1)
        elif ev < 0.18:
            ns[1] = np.clip(ns[1] + 0.08, 0, 1)      # cooking: warm
            ns[2] = np.clip(ns[2] + 0.25, 0, 1)      # humid
            ns[9] = np.clip(ns[9] - 0.2, 0, 1)       # air less fresh
        elif ev < 0.26:
            ns[7] = 0.02                              # cleaning
            ns[9] = np.clip(ns[9] + 0.3, 0, 1)
        elif ev < 0.34 and 13 <= tod < 17:
            occ = 1.0                                  # nap at home
            ns[12] = 0.05
        ns[3] = np.clip(occ + rng.normal(0, 0.05), 0, 1)
        # light follows tod unless blackout / lamps
        base = max(0.0, np.sin(np.pi * (tod - 5) / 14)) if 5 <= tod <= 19 else 0.0
        lamps = 0.5 * ns[3] if (tod >= 18 or tod < 6) else 0.0
        ns[0] = np.clip(0.85 * base * (1 - ns[15]) + lamps + rng.normal(0, 0.03), 0, 1)
        # thermal dynamics with heater hysteresis
        ns[14] = 1.0 if ns[1] < 0.35 else (0.0 if ns[1] > 0.55 else ns[14])
        ns[1] = np.clip(ns[1] + 0.02 * (ns[14] - 0.5) + 0.01 * (ns[6] * 0.5 - 0.25) * (1 if 5 <= tod <= 19 else 2) + rng.normal(0, 0.01), 0, 1)
        ns[2] = np.clip(ns[2] + 0.05 * (ns[3] - 0.4) + rng.normal(0, 0.02), 0, 1)
        # music follows occupancy evenings
        ns[4] = np.clip(0.6 * ns[3] * (1 if tod >= 17 or tod < 1 else 0.3) + rng.normal(0, 0.05), 0, 1) if ev >= 0.08 else ns[4]
        # doors/windows
        ns[5] = np.clip(0.8 * ns[3] + rng.normal(0, 0.1), 0, 1)
        ns[6] = np.clip((0.6 if 10 <= tod <= 20 else 0.1) * rng.random() + rng.normal(0, 0.05), 0, 1)
        # mess drift
        ns[7] = np.clip(ns[7] + 0.06 * ns[3] - 0.02, 0, 1)
        # plants decay, occasional watering
        ns[8] = np.clip(ns[8] - 0.03 + (0.45 if rng.random() < 0.07 else 0.0), 0, 1)
        # air freshness
        ns[9] = np.clip(ns[9] + 0.1 * (0.3 - ns[7]) - 0.05 * ns[3] + rng.normal(0, 0.02), 0, 1)
        # clock
        ntod = (tod + 1) % 24
        ns[10] = np.sin(2 * np.pi * ntod / 24)
        ns[11] = np.cos(2 * np.pi * ntod / 24)
        # activity
        base_act = 0.2 + 0.5 * max(0.0, np.sin(np.pi * (ntod - 6) / 16)) if 6 <= ntod <= 22 else 0.05
        ns[12] = np.clip(base_act * ns[3] + rng.normal(0, 0.05), 0, 1)
        # pet
        ns[13] = np.clip((1.0 if 7 <= ntod <= 21 else 0.2) * rng.random() + rng.normal(0, 0.1), 0, 1)
        return ns

    def init_state(rng):
        s = rng.random(16) * 0.5
        s[10] = rng.normal(0, 0.5)
        s[11] = rng.normal(1, 0.3)
        s[14] = float(rng.random() < 0.5)
        s[15] = float(rng.random() < 0.1)
        return s

    S0, S1, reg = [], [], []
    hour = int(rng.integers(0, 24))
    s = init_state(rng)
    for _ in range(n_pairs):
        tod = hour % 24
        r = 0 if 5 <= tod < 11 else 1 if 11 <= tod < 17 else 2 if 17 <= tod < 23 else 3
        S0.append(s.copy())
        s = step_state(s, hour, rng)
        S1.append(s.copy())
        reg.append(r)
        hour += 1
    return (torch.tensor(np.array(S0), dtype=torch.float32),
            torch.tensor(np.array(S1), dtype=torch.float32),
            np.array(reg), feat_names)


def describe_room(f):
    """Semantic phrase for a 16-d feature row (numpy)."""
    tod = int(round((np.arctan2(f[10], f[11]) / (2 * np.pi) * 24 + 24) % 24))
    parts = []
    day = "morning" if 5 <= tod < 11 else "day" if 11 <= tod < 17 else "evening" if 17 <= tod < 23 else "night"
    parts.append(day)
    parts.append("bright" if f[0] > 0.55 else "dim" if f[0] > 0.2 else "dark")
    n_people = int(round(f[3] * 4))
    parts.append("empty" if n_people == 0 else f"{n_people} people")
    if f[4] > 0.4:
        parts.append("music on")
    if f[2] > 0.6 and f[1] > 0.5:
        parts.append("kitchen-warm-humid")
    if f[7] > 0.5:
        parts.append("messy")
    if f[6] > 0.4:
        parts.append("windows open")
    if f[12] > 0.5:
        parts.append("active")
    elif f[12] < 0.15:
        parts.append("calm")
    if f[13] > 0.6:
        parts.append("pet up")
    return ", ".join(parts)


# ------------------------------------------------------------------- models
class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(FEAT_D, HID), nn.GELU(), nn.Linear(HID, LAT_D))

    def forward(self, x):
        return self.net(x)


class Predictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(LAT_D, HID), nn.GELU(), nn.Linear(HID, LAT_D))

    def forward(self, z):
        return self.net(z)


# ----------------------------------------------------------------- metrics
def diversity_metrics(pred, targ):
    """pred, targ: (n, LAT_D) latents on GPU."""
    pv = pred.var(dim=0)
    tv = targ.var(dim=0)
    var_ratio = float((pv / (tv + 1e-9)).mean())
    d_pred = torch.cdist(pred, pred)
    d_targ = torch.cdist(targ, targ)
    n = pred.shape[0]
    iu = torch.triu_indices(n, n, 1)
    pairwise_ratio = float((d_pred[iu[0], iu[1]].mean() / (d_targ[iu[0], iu[1]].mean() + 1e-9)))
    # per-dim entropy with bins fixed from target quantiles (8 bins)
    ents = []
    for j in range(LAT_D):
        edges = torch.quantile(targ[:, j], torch.linspace(0, 1, 9, device=targ.device)[1:-1])
        # guard degenerate edges
        if torch.any(torch.diff(torch.cat([targ[:, j].min().view(1), edges, targ[:, j].max().view(1)])) <= 0):
            continue
        b = torch.bucketize(pred[:, j], edges)
        h = torch.bincount(b, minlength=8).float() / pred.shape[0]
        p = h[h > 0]
        ents.append(float(-(p * p.log()).sum() / np.log(8)))
    entropy_idx = float(np.mean(ents)) if ents else 0.0
    # participation ratio of covariance spectrum (effective dim)
    cov = torch.cov(pred.T)
    ev = torch.linalg.eigvalsh(cov).clamp_min(0)
    pr_dim = float(((ev.sum() ** 2) / (ev.pow(2).sum() + 1e-12)) / LAT_D)
    return {"var_ratio": var_ratio, "pairwise_ratio": pairwise_ratio,
            "entropy_idx": entropy_idx, "pr_dim": pr_dim}


# ---------------------------------------------------------------- JEV client
def load_key():
    with open(KEYFILE) as fh:
        for line in fh:
            if line.startswith("TYPESAFE_AI_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("TYPESAFE_AI_KEY not found")


_jev_cache = {}
if os.path.exists(CACHE):
    with open(CACHE) as fh:
        _jev_cache = json.load(fh)


def jev_call(state, questions, retries=3):
    body = json.dumps({"model": "jev-latest", "state": state, "questions": questions})
    h = hashlib.sha256(body.encode()).hexdigest()
    if h in _jev_cache:
        return _jev_cache[h], True
    key = load_key()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(API, data=body.encode(),
                                     headers={"Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                out = json.loads(resp.read())
            _jev_cache[h] = out
            with open(CACHE + ".tmp", "w") as fh:
                json.dump(_jev_cache, fh)
            os.replace(CACHE + ".tmp", CACHE)
            return out, False
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1) ** 2)
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(2 * (attempt + 1) ** 2)
    raise RuntimeError(f"JEV call failed after {retries}: {last}")


DIV_Q = {
    "diversity": {
        "type": "noul",
        "question": "Are these predicted room states sufficiently diverse to represent meaningful room evolution?",
        "instructions": "Answer true only if the predicted next states span meaningfully different configurations matching their different starting rooms. Near-identical predictions across very different starting rooms, or a single averaged default room, should answer false.",
    },
    "interesting": {
        "type": "noul",
        "question": "Is this prediction set interesting or surprising rather than just a comfortable default?",
        "instructions": "A comfortable default is one bland averaged room repeated. Interesting means distinct, specific, differentiated predictions that track their starting rooms and capture events like guests, cooking, or cleaning.",
    },
}

COMFORT_Q = {
    "interesting": DIV_Q["interesting"],
    "comfort": {
        "type": "score",
        "question": "How much is this set of predicted states a default/averaged view rather than specific evolving room states?",
        "criteria": [
            "1 = highly specific and varied predictions",
            "2 = mostly specific with some averaging",
            "3 = mixed specificity and averaging",
            "4 = mostly averaged defaults",
            "5 = single comfortable default repeated",
        ],
    },
}


def render_probe_state(pred_lat, nn_desc):
    """pred_lat: (8, LAT_D) probe predictions; nn_desc: list of 8 phrases."""
    lines = ["A JEPA world-model predicts the next room state from the current room state.",
             "Below are its 8 predicted NEXT rooms for 8 different starting rooms (2 morning, 2 day, 2 evening, 2 night).",
             "Each line: predicted latent coordinates (all 8 dims) and the observed room it most closely resembles."]
    for i in range(8):
        coords = ", ".join(f"{v:+.2f}" for v in pred_lat[i].tolist())
        lines.append(f"P{i+1} [{coords}] ~ {nn_desc[i]}")
    return "\n".join(lines)


# ------------------------------------------------------------------ results IO
def load_results():
    if os.path.exists(RESULTS):
        with open(RESULTS) as fh:
            return json.load(fh)
    return {"schema": "jev-jepa-collapse/v1"}


def save_results(r):
    with open(RESULTS + ".tmp", "w") as fh:
        json.dump(r, fh, indent=1)
    os.replace(RESULTS + ".tmp", RESULTS)


# -------------------------------------------------------------------- phases
def ramp_receipt():
    """INSTRUMENT-01: sustained load before timing-sensitive work."""
    a = torch.randn(2048, 2048, device=DEV)
    torch.cuda.synchronize() if DEV.type == "cuda" else None
    t0 = time.time()
    n = 0
    while time.time() - t0 < 1.0:
        a = a @ a
        n += 1
    if DEV.type == "cuda":
        torch.cuda.synchronize()
    dt = time.time() - t0
    return {"warmup_s": round(dt, 3), "matmuls": n,
            "device": torch.cuda.get_device_name(0) if DEV.type == "cuda" else "cpu"}


def phase1():
    torch.manual_seed(SEED)
    r = load_results()
    r["gpu"] = {"torch": torch.__version__, "ramp_receipt": ramp_receipt()}
    S0, S1, reg, names = gen_world()
    r["config"] = {"seed": SEED, "n_trans": N_TRANS, "feat_d": FEAT_D, "lat_d": LAT_D,
                   "hidden": HID, "steps": STEPS, "monitor_every": MONITOR_EVERY,
                   "lr": LR, "weight_decay": WD, "feat_names": names}
    # dataset sanity: diversity of TRUE next states + regime distribution
    enc = Encoder().to(DEV)
    with torch.no_grad():
        z1 = enc(S1.to(DEV))
        m = diversity_metrics(z1, z1)
    r["data"] = {"true_next_self_metrics": m,
                 "regime_counts": {REGIME_NAMES[i]: int((reg == i).sum()) for i in range(4)},
                 "probe_desc_example": describe_room(S1[0].numpy())}
    save_results(r)
    # smoke JEV call on TRUE next states (healthy upper bound, cached for phase 3)
    probes = probe_indices(reg)
    state = render_probe_state(z1[probes].cpu(),
                               [describe_room(S1[p].numpy()) for p in probes])
    out, cached = jev_call(state, DIV_Q)
    print("data OK:", m, "regimes:", r["data"]["regime_counts"])
    print("smoke JEV on TRUE next states:", json.dumps(out.get("answers", {})), "cached:", cached)
    r.setdefault("smoke", {})["true_next_jev"] = out.get("answers", {})
    save_results(r)


def probe_indices(reg):
    ps = []
    for ri in range(4):
        idx = np.where(reg == ri)[0]
        ps.extend(idx[:: max(1, len(idx) // 2)][:2].tolist())
    return torch.tensor(ps[:8], dtype=torch.long)


def train_run(name, frozen, jev_gated):
    torch.manual_seed(SEED + (0 if frozen else 1))
    S0, S1, reg, _ = gen_world()
    S0d, S1d = S0.to(DEV), S1.to(DEV)
    enc = Encoder().to(DEV)
    pred = Predictor().to(DEV)
    if frozen:
        for p in enc.parameters():
            p.requires_grad_(False)
        enc.eval()
    params = [p for p in list(enc.parameters()) + list(pred.parameters()) if p.requires_grad]
    opt = torch.optim.Adam(params, lr=LR, weight_decay=WD)
    probes = probe_indices(reg).to(DEV)
    with torch.no_grad():
        z0_all = enc(S0d)
        z1_all = enc(S1d)  # NOTE: recomputed each checkpoint (encoder may drift)
    ckpts = []
    kick_weight, consecutive, div_last = 0.0, 0, None
    kicks = []
    t_train = 0.0
    n_jev = 0
    for step in range(1, STEPS + 1):
        if step % MONITOR_EVERY == 1 or step == 1:
            t0 = time.time()
        z0 = enc(S0d)
        z1_pred = pred(z0)
        with torch.no_grad():
            z1_t = enc(S1d)
        mse = F.mse_loss(z1_pred, z1_t)
        loss = mse
        if jev_gated and kick_weight > 0:
            target_std = z1_t.std(dim=0).detach()
            pred_std = z1_pred.std(dim=0)
            var_loss = F.relu(target_std - pred_std).mean()
            loss = loss + kick_weight * var_loss
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % MONITOR_EVERY == 0:
            t_train += time.time() - t0
            with torch.no_grad():
                z0m = enc(S0d)
                pm = pred(z0m)
                z1_all = enc(S1d)  # refresh NN bank in CURRENT latent space
                m = diversity_metrics(pm, z1_all)
                # nearest observed template for probe predictions
                d = torch.cdist(pm[probes], z1_all)
                nn = d.argmin(dim=1).cpu().numpy()
                desc = [describe_room(S1[i].numpy()) for i in nn]
            state = render_probe_state(pm[probes].cpu(), desc)
            out, cached = jev_call(state, DIV_Q)
            if not cached:
                n_jev += 1
            abs_scale = {"pred_std_mean": round(float(pm.std(0).mean()), 4),
                         "targ_std_mean": round(float(z1_all.std(0).mean()), 4)}
            ans = out.get("answers", {})
            div = float(ans.get("diversity", {}).get("noul", 0.5))
            intr = float(ans.get("interesting", {}).get("noul", 0.5))
            if jev_gated:
                if div < 0.6:
                    consecutive += 1
                    kick_weight = min(5.0, 0.1 * 1.5 ** consecutive)
                else:
                    consecutive = 0
                    kick_weight = 0.0 if kick_weight < 0.07 else kick_weight * 0.7
                kicks.append(round(kick_weight, 3))
                div_last = div
            lam = 0.05 + 0.95 * step / STEPS
            composed = float(mse.item()) + lam * (1 - (div_last if div_last is not None else 1.0))
            ckpts.append({"step": step, "mse": round(float(mse.item()), 6),
                          **{k: round(v, 4) for k, v in m.items()}, **abs_scale,
                          "jev_diversity": div, "jev_interesting": intr,
                          "lambda": round(lam, 4),
                          "composed_loss": round(composed, 6),
                          "kick_weight": round(kick_weight, 3)})
            if step % 500 == 0:
                print(f"[{name}] step {step} mse={float(mse):.4f} pairwise={m['pairwise_ratio']:.3f} "
                      f"jev_div={div:.2f} jev_int={intr:.2f} kick={kick_weight:.2f}", flush=True)
    r = load_results()
    r.setdefault("runs", {})[name] = {
        "frozen_encoder": frozen, "jev_gated": jev_gated,
        "train_seconds": round(t_train, 2), "jev_calls": n_jev,
        "checkpoints": ckpts,
        "kick_schedule": kicks if kicks else None,
        "final": ckpts[-1],
    }
    save_results(r)
    print(f"[{name}] DONE final={json.dumps(ckpts[-1])}")


def phase2():
    for name, frozen, gated in [
        ("unfrozen-mse", False, False),   # E1/E3-B: expected collapse
        ("frozen-mse", True, False),      # E3-A: elephant approach
        ("unfrozen-jevreg", False, True),  # E2
        ("frozen-jevreg", True, True),     # ablation 4th cell
    ]:
        train_run(name, frozen, gated)


def phase3():
    """E5: comfortable-collapse probes on final models + healthy reference."""
    r = load_results()
    torch.manual_seed(SEED)
    S0, S1, reg, _ = gen_world()
    S0d, S1d = S0.to(DEV), S1.to(DEV)
    probes = probe_indices(reg).to(DEV)
    comfort = {}
    # healthy reference: true next states
    with torch.no_grad():
        z1 = Encoder().to(DEV)(S1d)
        desc = [describe_room(S1[p].numpy()) for p in probes.cpu().tolist()]
    state = render_probe_state(z1[probes].cpu(), desc)
    out, _ = jev_call(state, COMFORT_Q)
    comfort["true-next-states"] = {"answers": out.get("answers", {}),
                                   "note": "healthy upper bound"}
    print("comfort true:", json.dumps(out.get("answers", {})))
    # retrain final snapshot per config (deterministic) and probe
    for name, frozen, gated in [("unfrozen-mse", False, False), ("frozen-mse", True, False),
                                ("unfrozen-jevreg", False, True), ("frozen-jevreg", True, True)]:
        torch.manual_seed(SEED + (0 if frozen else 1))
        enc = Encoder().to(DEV)
        pred = Predictor().to(DEV)
        if frozen:
            for p in enc.parameters():
                p.requires_grad_(False)
            enc.eval()
        params = [p for p in list(enc.parameters()) + list(pred.parameters()) if p.requires_grad]
        opt = torch.optim.Adam(params, lr=LR, weight_decay=WD)
        kick_weight, consecutive = 0.0, 0
        # replay kick schedule from saved run (identical training)
        kicks = (r["runs"].get(name, {}).get("kick_schedule") or [0.0] * STEPS)
        for step in range(1, STEPS + 1):
            z0 = enc(S0d)
            zp = pred(z0)
            with torch.no_grad():
                zt = enc(S1d)
            loss = F.mse_loss(zp, zt)
            if gated and kicks[(step - 1) // MONITOR_EVERY] > 0:
                var_loss = F.relu(zt.std(dim=0).detach() - zp.std(dim=0)).mean()
                loss = loss + kicks[(step - 1) // MONITOR_EVERY] * var_loss
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            pm = pred(enc(S0d))
            z1_all = enc(S1d)
            nn = torch.cdist(pm[probes], z1_all).argmin(dim=1).cpu().numpy()
            desc = [describe_room(S1[i].numpy()) for i in nn]
        state = render_probe_state(pm[probes].cpu(), desc)
        out, _ = jev_call(state, COMFORT_Q)
        comfort[name] = {"answers": out.get("answers", {})}
        print(f"comfort {name}:", json.dumps(out.get("answers", {})))
    r["comfort"] = comfort
    save_results(r)


def phase4():
    from scipy.stats import pearsonr, spearmanr
    r = load_results()
    rows = []
    for name, run in r["runs"].items():
        for c in run["checkpoints"]:
            rows.append((c["jev_diversity"], c["entropy_idx"], c["pairwise_ratio"],
                         c["var_ratio"], c["pr_dim"], name, c["step"]))
    arr = np.array([[x[0], x[1], x[2], x[3], x[4]] for x in rows], dtype=float)
    jd, ent, pw, vr, pr = arr.T
    def corr(a, b):
        return {"pearson": round(float(pearsonr(a, b)[0]), 4),
                "spearman": round(float(spearmanr(a, b)[0]), 4)}
    r["correlations"] = {
        "n_checkpoints": len(rows),
        "jev_vs_entropy": corr(jd, ent),
        "jev_vs_pairwise": corr(jd, pw),
        "jev_vs_varratio": corr(jd, vr),
        "jev_vs_prdim": corr(jd, pr),
        "per_run": {name: {
            "jev_vs_entropy": corr(*np.array([[x[0], x[1]] for x in rows if x[5] == name]).T),
            "jev_vs_pairwise": corr(*np.array([[x[0], x[2]] for x in rows if x[5] == name]).T),
        } for name in r["runs"]},
    }
    # collapse steps + ablation table
    abl = {}
    for name, run in r["runs"].items():
        cps = run["checkpoints"]
        math_step = next((c["step"] for c in cps if c["pairwise_ratio"] < 0.2), None)
        jev_step = next((c["step"] for c in cps if c["jev_diversity"] < 0.3), None)
        # sticky math collapse: all subsequent below 0.25
        sticky = None
        for i, c in enumerate(cps):
            if all(d["pairwise_ratio"] < 0.25 for d in cps[i:]):
                sticky = c["step"]
                break
        abl[name] = {"final": run["final"], "math_collapse_step": math_step,
                     "sticky_math_collapse_step": sticky,
                     "jev_collapse_step(noul<0.3)": jev_step,
                     "jev_calls": run["jev_calls"], "train_seconds": run["train_seconds"]}
    r["ablation"] = abl
    save_results(r)
    print(json.dumps({"correlations": r["correlations"], "ablation": abl}, indent=1)[:3000])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", type=int)
    a = ap.parse_args()
    {1: phase1, 2: phase2, 3: phase3, 4: phase4}[a.phase]()
