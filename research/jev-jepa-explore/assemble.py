#!/usr/bin/env python3
"""assemble.py — merge all experiment outputs into explore-results.json."""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name)
    with open(p) as f:
        return json.load(f)


def slim_exp1(r):
    return {"verdict": r["verdict"], "n_trials": r["n_trials"],
            "keyword_acc": r["keyword_acc"], "jev_covered_acc": r["jev_covered_acc"],
            "jev_coverage": r["jev_coverage"],
            "abstain_rate_boundary": r["abstain_rate_boundary"],
            "abstain_rate_clear": r["abstain_rate_clear"],
            "offdomain_escalate_rate": r["offdomain_escalate_rate"],
            "gates": r["gates"], "jev_ledger": r["jev_ledger"], "wall_s": r["wall_s"]}


def slim_exp2(r):
    return {"verdict": r["verdict"], "n_runs": r["n_runs"], "d": r["d"],
            "gpu_ramp_receipt": r["gpu_ramp_receipt"],
            "aggregate_by_k": r["aggregate_by_k"],
            "random_proj_baseline": r["random_proj_baseline"],
            "gates": r["gates"]}


def slim_exp2b(r):
    return {"post_hoc": True, "aggregate": r["aggregate"],
            "note": r["note"]}


def slim_exp3(r):
    return {"verdict": r["verdict"], "n_runs": r["n_runs"], "d": r["d"],
            "bits": r["bits"], "gates": r["gates"],
            "mean_by_noise": r["mean_by_noise"]}


def slim_exp4(r):
    return {"verdict": r["verdict"], "n_trials": r["n_trials"],
            "thresholds": r["thresholds"], "scores": r["scores"],
            "gates": r["gates"],
            "complementarity_jev_jepa_disagreements": r["complementarity_jev_jepa_disagreements"],
            "jev_ledger": r["jev_ledger"], "wall_s": r["wall_s"]}


def slim_exp5(r):
    return {"verdict": r["verdict"], "n_events": r["n_events"],
            "combined_3way_acc": r["combined_3way_acc"],
            "binary_baselines_honest": r["binary_baselines_honest"],
            "per_class": r["per_class"], "gates": r["gates"],
            "jev_ledger": r["jev_ledger"]}


def slim_exp5b(r):
    return {k: v for k, v in r.items() if k != "rows"}


def main():
    total_jev = {}
    for f in ("exp1_out.json", "exp4_out.json", "exp5_out.json"):
        led = load(f)["jev_ledger"]
        for k, v in led.items():
            total_jev[k] = total_jev.get(k, 0) + v
    out = {
        "meta": {
            "title": "JEV x JEPA x Ternary creative explore (ternary-synergy-miner style)",
            "date": "2026-10-06",
            "lane": "5 creative explore",
            "pattern": "shared primitive -> novel composition -> falsifiable claim -> frozen gates -> negative controls",
            "pre_reg": "PRE-REG.md (frozen before firing)",
            "components": {
                "JEV": "typesafe judgment cell (jev-latest, graded noul confidence; CM1 pinch-gate lineage)",
                "JEPA": "transitional JEPA (quilt-gpu-lab tools/transition_kernel.py) + elephant jepa_rag dial alphabet",
                "ternary": "SuperInstance {-1,0,+1} ecosystem (TERNARY-WIKI.md, 200 repos)"
            },
            "total_jev_ledger": total_jev,
        },
        "exp1_jev_ternary_router": slim_exp1(load("exp1_out.json")),
        "exp2_jepa_ternary_encoder": slim_exp2(load("exp2_out.json")),
        "exp2b_structured_arm_posthoc": slim_exp2b(load("exp2b_out.json")),
        "exp3_ternary_jepa_lattice": slim_exp3(load("exp3_out.json")),
        "exp4_pinch_mesh_composed": slim_exp4(load("exp4_out.json")),
        "exp5_impossible_detector": slim_exp5(load("exp5_out.json")),
        "exp5b_zscore_posthoc": slim_exp5b(load("exp5b_out.json")),
        "verdicts_summary": {
            "exp1": load("exp1_out.json")["verdict"],
            "exp2": load("exp2_out.json")["verdict"],
            "exp2b": "structured arm also fails smooth-geometry (err ~0.17 @ k=4, rho ~0.38)",
            "exp3": load("exp3_out.json")["verdict"],
            "exp4": load("exp4_out.json")["verdict"],
            "exp5": load("exp5_out.json")["verdict"],
            "exp5b": load("exp5b_out.json")["verdict"],
        },
    }
    with open(os.path.join(HERE, "explore-results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote explore-results.json")
    print(json.dumps(out["verdicts_summary"], indent=1))
    print("total JEV ledger:", total_jev)


if __name__ == "__main__":
    main()
