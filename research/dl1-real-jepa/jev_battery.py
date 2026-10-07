#!/usr/bin/env python3
"""DL1-REAL-JEPA step 3: JEV battery on REAL residuals (frozen PRE-REG §4).

Rows: held-out test transitions, channels A (logged cumulative) + B (sliding16),
stratified 15/tercile per channel by decoded L1 dial residual (JEPA arm).
Arms: jepa / persistence. Questions (noul): valid, coupling, close
+ actual_valid reference. Decode: constrained LSQ (5 basis projections,
nearest-to-before in the null dims), destandardize, clip (log clip frac).
Key read at use-time from ~/.config/typesafe/token; never echoed.
Append-only resumable log: jev-real-judgments.jsonl
"""
import json, os, random, time, urllib.request, urllib.error
import concurrent.futures as cf
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
KEYFILE = os.path.expanduser("~/.config/typesafe/token")

def get_key():
    with open(KEYFILE) as f:
        k = f.read().strip()
    if not k:
        raise SystemExit("key missing")
    return k

DIALS = ["mood", "volume", "earnestness", "cynicism", "joke_landing",
         "panic", "presence"]
RANGES = {"mood": [-1, 1], "volume": [0, 1], "earnestness": [0, 1],
          "cynicism": [0, 1], "joke_landing": [-1, 1], "panic": [0, 1],
          "presence": [0, 1]}

z = np.load(os.path.join(HERE, "real_latents.npz"))
basis = z["basis"]; SCALE = z["scale"]; CENTER = z["center"]
LO, HI = z["lo"], z["hi"]
V5 = basis[:, :5]
_V5gram_inv = np.linalg.inv(V5.T @ V5)

def decode(latent5, mu_before_z):
    """Constrained LSQ: match 5 basis projections, stay nearest to before μ̂.
    Result renormalized to the sphere (μ̂ lives on S⁶)."""
    w = _V5gram_inv @ (latent5 - V5.T @ mu_before_z)
    mu_z = mu_before_z + V5 @ w
    mu_z = mu_z / np.linalg.norm(mu_z)
    v = mu_z / SCALE + CENTER
    clipped = np.clip(v, LO, HI)
    return clipped, float(np.abs(clipped - v).max())

def mu_to_dials(mu_z):
    """Unit μ̂ (z-space) -> dial values, clipped (same path as decode)."""
    v = (mu_z / np.linalg.norm(mu_z)) / SCALE + CENTER
    return np.clip(v, LO, HI)

def mu_of(night, seq, ch):
    """Logged/recomputed μ̂ (z-space) at a speak index — refit-free path:
    reconstruct from stored latent? No — use raw mu from file for A; for B
    recompute from sliding fit (stored latents only carry projections), so
    we recompute the fit here (deterministic)."""
    raise NotImplementedError

# Simpler: for both channels we need μ̂_before in z-space to decode against,
# and raw dial vectors for context.  Recompute μ̂ directly:
import sys
sys.path.insert(0, "/home/eileen/projects/elephant")
from elephant.vmf import vmf_fit

PRIMARY = ["A", "D", "D-cold", "S1", "S2", "S3", "S4a", "S4b", "S5"]

def night_raw_mu(ch):
    """{night: {seq: (raw_v, mu_z, kappa, rho)}}"""
    import glob
    out = {}
    for n in PRIMARY:
        rows = [json.loads(l) for l in
                open(f"/home/eileen/projects/elephant/data/nights/night-{n}.jsonl")
                if l.strip()]
        speaks = [r for r in rows if r["type"] == "speak"]
        raws = np.array([r["field_raw_after"] for r in speaks], float)
        zs = [SCALE * (v - CENTER) for v in raws]
        zs = [x for x in zs if np.linalg.norm(x) > 1e-3]
        d = {}
        for i, r in enumerate(speaks):
            if ch == "A":
                f = r.get("fit")
                if f:
                    d[r["seq"]] = (raws[i], np.array(f["mu_hat"]),
                                   f["kappa"], f["rho"])
            else:
                if i + 1 >= 10:
                    f = vmf_fit(zs[:i + 1][-16:], B=2)
                    if f:
                        d[r["seq"]] = (raws[i], f["mu_hat"], f["kappa"], f["rho"])
        out[n] = d
    return out

RAW_MU = {ch: night_raw_mu(ch) for ch in ("A", "B")}
PREDS = json.load(open(os.path.join(HERE, "heldout-predictions.json")))

def state_dict(night, seq, dials_v, kappa, rho):
    s = {"night": night, "after_speak_index": int(seq),
         "room_conversation_field": {
             d: round(float(dials_v[i]), 4) for i, d in enumerate(DIALS)},
         "dial_ranges": RANGES,
         "field_concentration_kappa": round(float(kappa), 2),
         "field_mean_resultant_rho": round(float(rho), 4)}
    return s

def build_rows(ch):
    P = PREDS[ch]
    rows = []
    for k in range(len(P["night"])):
        night = P["night"][k]; st, s1 = P["seq_t"][k], P["seq_t1"][k]
        d = RAW_MU[ch][night]
        raw_b, mu_b, kap_b, rho_b = d[st]
        raw_a, mu_a, kap_a, rho_a = d[s1]
        # all three judged states live in decoded μ̂-space (consistent scale)
        v_b = mu_to_dials(mu_b); v_a = mu_to_dials(mu_a)
        clipmax = {}
        preds = {}
        for arm in ("jepa", "pers"):
            l = np.array(P[f"lat_pred_{arm}"][k])
            v_dec, cm = decode(l[[0, 3, 4, 5, 6]], mu_b)
            kap = float(np.expm1(l[1])); rho = float(np.clip(l[2], 0, 1))
            preds[arm] = (v_dec, kap, rho)
            clipmax[arm] = cm
        l1 = float(np.abs(preds["jepa"][0] - v_a).sum())
        rows.append({"channel": ch, "night": night, "seq_t": int(st),
                     "seq_t1": int(s1), "before_raw": raw_b.tolist(),
                     "actual_raw": raw_a.tolist(),
                     "before": state_dict(night, st, v_b, kap_b, rho_b),
                     "actual": state_dict(night, s1, v_a, kap_a, rho_a),
                     "pred_jepa": state_dict(night, s1, preds["jepa"][0],
                                             preds["jepa"][1], preds["jepa"][2]),
                     "pred_pers": state_dict(night, s1, preds["pers"][0],
                                             preds["pers"][1], preds["pers"][2]),
                     "resid_l1": l1,
                     "clipmax": {a: round(v, 4) for a, v in clipmax.items()},
                     "kappa_before": kap_b})
    return rows

def sample_rows(rows, per_channel=45, seed=2718):
    rng = random.Random(seed)
    q = np.quantile([r["resid_l1"] for r in rows], [1/3, 2/3])
    picks = []
    for name, sel in (("lo", lambda r: r["resid_l1"] <= q[0]),
                      ("mid", lambda r: q[0] < r["resid_l1"] <= q[1]),
                      ("hi", lambda r: r["resid_l1"] > q[1])):
        cand = [r for r in rows if sel(r)]
        picks += rng.sample(cand, min(15, len(cand)))
    return picks

QUESTIONS = {
    "valid": {
        "type": "noul",
        "instructions": ("Could the PREDICTED after-state plausibly follow "
                         "from the before-state as a real room-conversation "
                         "evolution over one more message?"),
        "criteria": {"true": "A plausible conversational evolution, all dials consistent",
                     "false": "Some change could not happen this way in a real conversation"}},
    "coupling": {
        "type": "noul",
        "instructions": ("Do the predicted changes respect room-conversation "
                         "couplings: volume moves with presence/participation, "
                         "mood with joke_landing and earnestness, cynicism "
                         "anti-aligned with mood, panic rare and coupled to "
                         "volume dropping — one coherent conversational cause?"),
        "criteria": {"true": "Changes are jointly coherent under one conversational cause",
                     "false": "Changes violate couplings or look unrelated"}},
    "close": {
        "type": "noul",
        "instructions": ("Is the predicted after-state close to the actual "
                         "after-state on every dial?"),
        "criteria": {"true": "Every dial within small tolerance of actual",
                     "false": "At least one dial is clearly off from actual"}},
    "actual_valid": {
        "type": "noul",
        "instructions": ("Could the actual after-state plausibly follow from "
                         "the before-state as a real room-conversation "
                         "evolution over one more message?"),
        "criteria": {"true": "A plausible conversational evolution",
                     "false": "Some change looks impossible for a real conversation"}},
}

LOG = os.path.join(HERE, "jev-real-judgments.jsonl")
done = set()
if os.path.exists(LOG):
    for l in open(LOG):
        r = json.loads(l)
        done.add((r["channel"], r["night"], r["seq_t"], r["arm"], r["question"]))

def call_jev(payload, key, tries=5):
    body = json.dumps(payload).encode()
    for attempt in range(tries):
        req = urllib.request.Request(
            URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt + random.random() * 2); continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(3 + attempt * 3)
    return None

def job(args):
    key, row, arm, qname = args
    ident = (row["channel"], row["night"], row["seq_t"], arm, qname)
    if ident in done:
        return None
    if qname == "actual_valid":
        after = row["actual"]; ctx = row["before"]
    else:
        after = row[f"pred_{arm}"]; ctx = row["before"]
    payload = {"model": MODEL,
               "state": {"context_before": ctx, "predicted_after": after,
                         "actual_after": row["actual"],
                         "note": ("room-conversation dial field; one message "
                                  "elapsed; predicted_after made by a "
                                  "room-field predictor before seeing the "
                                  "actual message")},
               "questions": {qname: QUESTIONS[qname]}}
    obj = call_jev(payload, key)
    if obj is None or "error" in obj:
        return {"id": ident, "error": True}
    return {"channel": row["channel"], "night": row["night"],
            "seq_t": row["seq_t"], "seq_t1": row["seq_t1"], "arm": arm,
            "question": qname, "noul": float(obj["answers"][qname]["noul"]),
            "resid_l1": row["resid_l1"], "clipmax": row["clipmax"]}

def main():
    key = get_key()
    allrows, sampled = [], []
    for ch in ("A", "B"):
        rows = build_rows(ch)
        allrows += rows
        sampled += sample_rows(rows)
    json.dump(sampled, open(os.path.join(HERE, "jev-rows.json"), "w"),
              indent=0)
    print(f"rows sampled: {len(sampled)} "
          f"(resid_l1 range {min(r['resid_l1'] for r in sampled):.3f}"
          f"-{max(r['resid_l1'] for r in sampled):.3f})")
    jobs = []
    for row in sampled:
        for arm in ("jepa", "pers"):
            for q in ("valid", "coupling", "close"):
                jobs.append((key, row, arm, q))
        jobs.append((key, row, "actual", "actual_valid"))
    todo = [j for j in jobs
            if (j[1]["channel"], j[1]["night"], j[1]["seq_t"], j[2], j[3]) not in done]
    print(f"calls to make: {len(todo)} (done already: {len(jobs)-len(todo)})")
    errs = 0
    with open(LOG, "a") as f:
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for i, res in enumerate(ex.map(job, todo)):
                if res is None:
                    continue
                if res.pop("error", False) or res.get("noul") is None:
                    errs += 1
                else:
                    f.write(json.dumps(res) + "\n")
                if (i + 1) % 50 == 0:
                    f.flush()
                    print(f"  {i+1}/{len(todo)} (errs {errs})")
    print(f"done. errors: {errs}")

if __name__ == "__main__":
    main()
