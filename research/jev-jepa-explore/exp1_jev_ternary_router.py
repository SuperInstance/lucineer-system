#!/usr/bin/env python3
"""Exp 1 — JEV as ternary router (pre-registered gates G1-G3, PRE-REG.md).

Shared primitive: the routing decision. CM1's keyword rule is a hard-coded
router; JEV's noul confidence is a graded router; ternary adds the 0-state
(escalate). Question: does the judgment cell's confidence triple beat the
hard-coded rule, especially on boundary reports where the rule is ambiguous?
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jev_noul_batch, ledger, dump, SEED

HERE = os.path.dirname(os.path.abspath(__file__))
DOMAINS = ("engine", "navigation", "deck")
PINCH = 0.5

ENGINE_TERMS = ["temp rising", "temp falling", "oil", "fuel", "rpm"]
MOTION_TERMS = ["moving", "course drift", "ais contact"]
HAZARD_TERMS = ["rising", "falling", "dropping", "leak", "fire"]


def keyword_router(report):
    low = report.lower()
    eng = any(t in low for t in ENGINE_TERMS)
    mot = any(t in low for t in MOTION_TERMS)
    domain = "engine" if eng else ("navigation" if mot else "deck")
    return domain


# --- stimulus corpus: 20 clear, 20 boundary, 20 off-domain -----------------
CLEAR = [
    ("Engine temp rising 3C per minute. Oil pressure dropping.", "engine"),
    ("RPM steady at 1800. Oil pressure normal. No contacts.", "engine"),
    ("Fuel flow steady at cruise rate. Bilge dry.", "engine"),
    ("Smoke alarm in the engine room, possible fire. Temp rising.", "engine"),
    ("Engine room sounds normal. Oil level checked, adequate.", "engine"),
    ("Camera frame: three blobs, one moving left at 0.4 units per second.", "navigation"),
    ("AIS contact closing from starboard, course drift detected.", "navigation"),
    ("Course drift 5 degrees starboard over last minute. AIS clear.", "navigation"),
    ("Blob moving fast toward vessel bow on camera two.", "navigation"),
    ("Radar sweep clean, no contacts, heading steady on mark 090.", "navigation"),
    ("All sensors nominal. Bilge dry. Radio quiet.", "deck"),
    ("Radio check complete, all quiet. Bilge dry. No motion.", "deck"),
    ("Galley cleanup done. Deck tools stowed.", "deck"),
    ("Deck lighting operational. Weather fair.", "deck"),
    ("Crew muster complete on deck. All accounted for.", "deck"),
    ("Coolant level in expansion tank verified at the full mark.", "engine"),
    ("Fuel transfer from port tank to day tank proceeding normally.", "engine"),
    ("Exhaust temperature all cylinders within band.", "engine"),
    ("Nav plot updated, position fixes agree within 0.2 nm.", "navigation"),
    ("Watch change on the bridge, handover log signed.", "navigation"),
]
# boundary: both rule-domains fire or neither; the keyword rule is ambiguous
BOUNDARY = [
    ("Oil pressure dropping while a blob moves fast toward the bow.", "engine"),
    ("Fuel leak on deck near the rail, no motion on cameras.", "deck"),
    ("Course drift 5 degrees and engine temp rising together.", "engine"),
    ("AIS contact closing; galley water also leaking.", "navigation"),
    ("Camera shows smoke haze moving across the frame; engine nominal.", "navigation"),
    ("Bilge water rising in the lazarette while making way, slight drift.", "deck"),
    ("RPM surging only when the vessel yaws in the following sea.", "engine"),
    ("Hydraulic steering sluggish responding during course change.", "navigation"),
    ("Fuel polish filter clogged during a turn with drift detected.", "engine"),
    ("Winch motor overheating on deck while hauling gear.", "deck"),
    ("Sounder loses bottom while the engine idles down.", "navigation"),
    ("Raw water strainer debris found after speed reduction.", "engine"),
    ("Plotter screen fogging in the engine space, course steady.", "navigation"),
    ("Trawl door sensor intermittent while turning to starboard.", "navigation"),
    ("Anchor windlass battery low during station holding.", "deck"),
    ("Sea chest temperature reading high with pack ice nearby.", "engine"),
    ("Deck floodlights flicker as the autopilot hunts.", "deck"),
    ("Galley stove gimbal sticking when rolling in the trough.", "deck"),
    ("Fuel gauge sender erratic only when pitching head sea.", "engine"),
    ("VHF antenna connection loose, noticed during watch below.", "navigation"),
]
OFFDOMAIN = [
    ("Crew morale high after the card game last night.", None),
    ("Provision list updated; coffee supply adequate.", None),
    ("Logbook calligraphy practice page completed.", None),
    ("New recipe for chowder documented in the galley binder.", None),
    ("Weather forecast printed and posted by the helm.", None),
    ("Photo of the sunset taken from the pilothouse.", None),
    ("Book swap shelf reorganized in the salon.", None),
    ("Fuel receipts filed under August tab.", None),
    ("Crew birthday noted on the calendar for next week.", None),
    ("Laundry day completed, foulies drying.", None),
    ("Radio drama episode recorded for evening listening.", None),
    ("Charts folio updated with new edition notices.", None),
    ("Fishing license paperwork photocopied.", None),
    ("Tool inventory checklist annotated with paint colors.", None),
    ("Berth curtain repair finished in the forward cabin.", None),
    ("Shore power adapter stored in the cockpit locker.", None),
    ("First-aid kit restock list pinned to the bulkhead.", None),
    ("Nautical almanac page bookmarked for tomorrow.", None),
    ("Coffee grinder maintenance note added to the binder.", None),
    ("Spares locker labeled with the new label maker.", None),
]


def jev_route(report):
    qs = {}
    for d in DOMAINS:
        qs[d] = ("Should this report be routed to the %s handler?" % d,
                 "Answer true only if the report's primary operational "
                 "concern belongs to the %s domain (engine=machinery, "
                 "navigation=motion/traffic/heading, deck=everything else "
                 "on deck, crew, housekeeping)." % d)
    conf = jev_noul_batch("Vessel report: " + report, qs)
    order = sorted(DOMAINS, key=lambda d: -conf[d])
    top, margin = conf[order[0]], conf[order[0]] - conf[order[1]]
    route = order[0] if top >= PINCH else "ESCALATE"  # ternary 0-state
    return route, top, margin, conf


def auc(pos, neg):
    """AUC for margin separating pos-class from neg-class."""
    wins = ties = 0
    for p in pos:
        for n in neg:
            if p > n: wins += 1
            elif p == n: ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


def main():
    trials = []
    t0 = time.time()
    for group, corpus in (("clear", CLEAR), ("boundary", BOUNDARY), ("offdomain", OFFDOMAIN)):
        for text, truth in corpus:
            kw = keyword_router(text)
            route, top, margin, conf = jev_route(text)
            trials.append({"group": group, "report": text, "truth": truth,
                           "kw_route": kw, "jev_route": route,
                           "jev_top": top, "jev_margin": margin,
                           "jev_conf": conf})
            print("[%4.1fs] %-9s truth=%-10s kw=%-10s jev=%-10s top=%.2f m=%.2f"
                  % (time.time() - t0, group, truth, kw, route, top, margin),
                  flush=True)
    # ---- scoring against frozen gates
    # keyword accuracy: on labeled (clear+boundary) — offdomain has no truth
    lab = [t for t in trials if t["truth"] is not None]
    off = [t for t in trials if t["group"] == "offdomain"]
    kw_acc = sum(t["kw_route"] == t["truth"] for t in lab) / len(lab)

    cov = [t for t in lab if t["jev_route"] != "ESCALATE"]
    jev_cov_acc = (sum(t["jev_route"] == t["truth"] for t in cov) / len(cov)
                   if cov else 0.0)
    cover = len(cov) / len(lab)
    clear_trials = [t for t in trials if t["group"] == "clear"]
    bnd_trials = [t for t in trials if t["group"] == "boundary"]
    abstain_clear = sum(t["jev_route"] == "ESCALATE" for t in clear_trials) / len(clear_trials)
    abstain_bnd = sum(t["jev_route"] == "ESCALATE" for t in bnd_trials) / len(bnd_trials)
    # G3: margin AUC clear vs boundary
    a = auc([t["jev_margin"] for t in clear_trials],
            [t["jev_margin"] for t in bnd_trials])
    # extra booked: offdomain handling (0-state target: escalate or deck?)
    off_escal = sum(t["jev_route"] == "ESCALATE" for t in off) / len(off)

    g1 = jev_cov_acc > kw_acc
    g2 = abstain_bnd >= 0.50 and abstain_clear <= 0.20
    g3 = a >= 0.75
    out = {
        "experiment": "exp1 JEV as ternary router",
        "n_trials": len(trials),
        "gates": {"G1_jev_covered_acc_beats_keyword": {"value": [jev_cov_acc, kw_acc], "pass": g1},
                  "G2_abstain_boundary_ge_0.5_clear_le_0.2": {"value": [abstain_bnd, abstain_clear], "pass": g2},
                  "G3_margin_auc_ge_0.75": {"value": a, "pass": g3}},
        "keyword_acc": kw_acc,
        "jev_covered_acc": jev_cov_acc,
        "jev_coverage": cover,
        "abstain_rate_boundary": abstain_bnd,
        "abstain_rate_clear": abstain_clear,
        "offdomain_escalate_rate": off_escal,
        "trials": trials,
        "jev_ledger": ledger(),
        "wall_s": round(time.time() - t0, 1),
        "verdict": "SYNERGY-PASS" if (g1 and g2 and g3) else "SYNERGY-FAIL",
    }
    dump(os.path.join(HERE, "exp1_out.json"), out)


if __name__ == "__main__":
    main()
