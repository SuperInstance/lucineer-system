#!/usr/bin/env python3
"""One-shot patcher for elephant/tapnight.py (v:2 + staged cold entry)."""
import sys

P = "/home/eileen/projects/elephant/elephant/tapnight.py"
src = open(P, encoding="utf-8").read()

EDITS = [
# 0. import A7
("from elephant.vmf import edge as vmf_edge, vmf_fit, windowed as vmf_windowed",
 "from elephant.vmf import A7 as vmf_A7, edge as vmf_edge, vmf_fit, \\\n"
 "    windowed as vmf_windowed"),
# 1. __init__ signature
("""                 identity: str = "elephant-v0",
                 W: int = 8):""",
 """                 identity: str = "elephant-v0",
                 W: int = 8,
                 reader_schema: int = 1,
                 staged_entries: Optional[Dict[str, "Participant"]] = None):"""),
# 2. __init__ body
("""        self._identity = identity
        self._session_id: Optional[str] = None
        self._last_fit: Optional[dict] = None""",
 """        self._identity = identity
        self._session_id: Optional[str] = None
        self._last_fit: Optional[dict] = None
        # v:2 per-reader logging (additive; 1 = legacy behavior, byte-stable)
        self._reader_schema = int(reader_schema)
        # staged cold entries: personas that engage at their FIRST speak
        # (no roster membership at open, no pre-entry acclimation)
        self._staged: Dict[str, Participant] = dict(staged_entries or {})
        self._reader_known: Dict[str, bool] = {}
        self._entry_mode: Dict[str, str] = {}
        self._reader_hist: Dict[str, list] = {}
        self._zc = np.array([DIAL_CENTER[n] for n in DIAL_NAMES])
        self._zscale = 2.0 / (np.array([DIAL_BOUNDS[n][1] for n in DIAL_NAMES])
                              - np.array([DIAL_BOUNDS[n][0] for n in DIAL_NAMES]))"""),
# 3. start_session reset
("""        self.field = np.zeros(len(DIAL_NAMES))
        self._last_fit = None
        self._session_id = uuid.uuid4().hex""",
 """        self.field = np.zeros(len(DIAL_NAMES))
        self._last_fit = None
        self._reader_known = {n: True for n in self.participants}
        self._entry_mode = {n: "roster" for n in self.participants}
        self._reader_hist = {n: [] for n in self.participants}
        self._session_id = uuid.uuid4().hex"""),
# 4. speak(): capture per-reader eff pre-acclimation, pass into event
("""        # Acclimation: everyone warms to the room at their own rate.
        for pname, p in self.participants.items():
            alpha = 1.0 - math.exp(-p.acclimation_rate)
            self._vibe[pname] += (self.field - self._vibe[pname]) * alpha

        self._emit(self._speak_event(msg, raw, first_by_author))
        return self""",
 """        # Acclimation: everyone warms to the room at their own rate.
        # (captured BEFORE this step: each reader's displaced field, using the
        #  pre-acclimation vibe that drove this speak's displacement — the
        #  exact quantity the v:2 schema logs as field_eff_to_reader)
        readers_pre = None
        if self._reader_schema >= 2:
            readers_pre = {}
            for pname, p in self.participants.items():
                n = self._interactions.get(pname, 0)
                s = 1.0 - math.exp(-p.charisma * n)
                eff = self._clamp(raw + s * (self._vibe[pname] - raw))
                self._reader_hist.setdefault(pname, []).append(eff)
                readers_pre[pname] = eff
        for pname, p in self.participants.items():
            alpha = 1.0 - math.exp(-p.acclimation_rate)
            self._vibe[pname] += (self.field - self._vibe[pname]) * alpha

        self._emit(self._speak_event(msg, raw, first_by_author,
                                      readers_pre=readers_pre))
        return self"""),
# 5. _register + _reader_fit
('''    def _register(self, name: str) -> None:
        """Lazily add an unknown speaker with neutral defaults."""
        self.participants[name] = Participant(
            name, dial_weights=np.full(len(DIAL_NAMES), 1.0 / len(DIAL_NAMES)),
            acclimation_rate=0.2, charisma=0.1,
            vibe=np.full(len(DIAL_NAMES), 0.5))
        self._vibe[name] = self.participants[name].vibe.copy()
        self._vibe_start[name] = self.participants[name].vibe.copy()''',
 '''    def _register(self, name: str) -> None:
        """Lazily add an unknown speaker. A STAGED entry (pre-declared
        persona, cold: engaged at first speak, never pre-warmed) keeps its
        persona; an unstaged stranger gets neutral defaults."""
        if name in self._staged:
            src = self._staged[name]
            p = Participant(src.name,
                            dial_weights=src.dial_weights.copy(),
                            acclimation_rate=src.acclimation_rate,
                            charisma=src.charisma, vibe=src.vibe.copy())
            self._entry_mode[name] = "staged-cold"
        else:
            p = Participant(
                name, dial_weights=np.full(len(DIAL_NAMES), 1.0 / len(DIAL_NAMES)),
                acclimation_rate=0.2, charisma=0.1,
                vibe=np.full(len(DIAL_NAMES), 0.5))
            self._entry_mode[name] = "lazy-neutral"
        self.participants[name] = p
        self._vibe[name] = self.participants[name].vibe.copy()
        self._vibe_start[name] = self.participants[name].vibe.copy()
        self._reader_known[name] = False

    def _reader_fit(self, win: list, weights: np.ndarray) -> Optional[dict]:
        """Light vMF MLE over a reader's own attention-weighted reading
        window (per-reader schema doc: mu_hat/kappa/n; null under n < 3).
        Same Newton estimator as vmf.py's A7 solve; no bootstrap/jackknife
        and no NMIN=10 guard — the reader window is W speaks by design."""
        if len(win) < 3:
            return None
        g = weights / weights.max() if weights.max() > 1e-12 else np.ones(7)
        z = np.stack([self._zscale * g * (v - self._zc) for v in win])
        z = z / np.maximum(np.linalg.norm(z, axis=1, keepdims=True), 1e-12)
        r = z.mean(0)
        rho = float(np.linalg.norm(r))
        if rho < 1e-12:
            return {"mu_hat": None, "kappa": None, "n": len(win)}
        mu = r / rho
        k = float(np.clip(rho * (7 - rho ** 2) / (1 - rho ** 2), 1e-6, 500.0))
        for _ in range(60):
            a = vmf_A7(k)
            gg = 1.0 - a * a - 6.0 * a / k
            if abs(gg) < 1e-12:
                break
            step = (a - rho) / gg
            k = float(np.clip(k - step, 1e-6, 500.0))
            if abs(step) < 1e-9:
                break
        return {"mu_hat": mu.tolist(), "kappa": k, "n": len(win)}'''),
# 6a. _session_open: name the dict
("""    def _session_open(self) -> dict:
        return {""",
 """    def _session_open(self) -> dict:
        evt = {"""),
# 6b. _session_open: v2 descriptor + return
('''                       for n, p in self.participants.items()},
        }

    def _speak_event(self, msg: Message, raw: np.ndarray,
                     first_by_author: bool) -> dict:''',
 '''                       for n, p in self.participants.items()},
        }
        if self._reader_schema >= 2:
            evt["reader_schema"] = {"version": 2,
                                    "field": "field_eff_to_reader",
                                    "lens": ["vibe_now", "weights_now"],
                                    "fit": "vmf-mle-newton-v1",
                                    "gate": "roster"}
            if self._staged:
                evt["staged_entries"] = {n: p.to_dict()
                                         for n, p in self._staged.items()}
        return evt

    def _speak_event(self, msg: Message, raw: np.ndarray,
                     first_by_author: bool,
                     readers_pre: Optional[Dict[str, np.ndarray]] = None) -> dict:'''),
# 7a. _speak_event: name the dict
("""        presence_mask = sorted({m.author for m in trailing})
        return {
            "v": 1, "type": "speak",""",
 """        presence_mask = sorted({m.author for m in trailing})
        evt = {
            "v": 1, "type": "speak","""),
# 7b. _speak_event: v2 blocks + return
('''            "fit": fit,
            "edge": edge,
        }''',
 '''            "fit": fit,
            "edge": edge,
        }
        if self._reader_schema >= 2 and readers_pre is not None:
            evt["v"] = 2
            readers = {}
            for pname, p in self.participants.items():
                eff = readers_pre[pname]
                readers[pname] = {
                    "reader_known": bool(self._reader_known.get(pname, False)),
                    "charisma": p.charisma,
                    "field_eff_to_reader": eff.tolist(),
                    "lens_now": {
                        "vibe_now": self._vibe[pname].tolist(),
                        "weights_now": p.dial_weights.tolist(),
                    },
                    "reader_fit": self._reader_fit(
                        self._reader_hist[pname][-self.W:], p.dial_weights),
                }
            evt["readers"] = readers
            evt["entry_mode"] = dict(self._entry_mode)
            reading_of = {}
            if msg.author in readers_pre:
                a = readers_pre[msg.author]
                na = np.linalg.norm(a)
                for member in presence_mask:
                    if member == msg.author:
                        reading_of[member] = {"cos": 1.0}
                        continue
                    b = readers_pre.get(member)
                    if b is None:
                        continue
                    nb = np.linalg.norm(b)
                    c = (float(np.dot(a, b) / (na * nb))
                         if na > 1e-12 and nb > 1e-12 else 0.0)
                    reading_of[member] = {"cos": c}
            evt["reading_of"] = reading_of
        return evt'''),
# 8a. _session_close: name the dict
('''        return {
            "v": 1, "type": "session_close",''',
 '''        evt = {
            "v": 1, "type": "session_close",'''),
# 8b. _session_close: reader_final + return
('''            "n_messages": len(self.room.messages),
            "notes": "",
        }''',
 '''            "n_messages": len(self.room.messages),
            "notes": "",
        }
        if self._reader_schema >= 2:
            evt["reader_final"] = self._reader_final()
        return evt'''),
# 9. _reader_final helper before _top_dials
("""    def _top_dials(self, k: int) -> List[str]:""",
 """    def _reader_final(self) -> dict:
        \"\"\"Componentwise median of each reader's field_eff_to_reader over
        the night (schema doc: the greppable per-reader baseline fact).\"\"\"
        out = {}
        for name, hist in self._reader_hist.items():
            if not hist:
                continue
            out[name] = np.median(np.stack(hist), axis=0).tolist()
        return out

    def _top_dials(self, k: int) -> List[str]:"""),
]

for i, (old, new) in enumerate(EDITS):
    n = src.count(old)
    if n != 1:
        sys.exit(f"EDIT {i}: {n} matches (need exactly 1)")
    src = src.replace(old, new)

open(P, "w", encoding="utf-8").write(src)
print("tapnight.py patched: all edits applied")
