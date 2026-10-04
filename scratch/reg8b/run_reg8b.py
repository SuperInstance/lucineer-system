"""REG-8B — the Bragg test. Executes docs/REG-8B-BRAGG.md pre-registration verbatim."""
import json, numpy as np

NIGHTS = "A D D-cold S1 S2 S3 S4a S4b S5".split()
N = 47; DT = 60.0
SEED = 20260903; NSURR = 10000

reg1 = json.load(open('/home/eileen/projects/elephant/data/slope/reg1-rotation-results.json'))
vstar = np.array(list(reg1['waves']['wave1']['primary_full7']['v_star'].values()))

series = {}
for n in NIGHTS:
    ev = [json.loads(l) for l in open(f'/home/eileen/projects/elephant/data/nights/night-{n}.jsonl')]
    f = [e for e in ev if isinstance(e.get('fit'), dict) and e['fit'].get('mu_hat')]
    x = np.array([vstar @ np.array(e['fit']['mu_hat']) for e in f])
    k = np.array([e['fit']['kappa'] for e in f])
    t = np.array([e['ts'] for e in f])
    series[n] = dict(x=x, k=k, t=t)
    assert np.allclose(np.diff(t), DT) and t[0] == 540

tgrid = np.arange(N) * DT
freqs = np.fft.rfftfreq(N, DT)

def prep(x, detrend=True, pad_to=N, L=None):
    L = len(x); tt = np.arange(L) * DT
    y = x - x.mean()
    if detrend: y = y - np.polyval(np.polyfit(tt, y, 1), tt)
    w = np.hanning(L + 2)[1:-1]
    y = y * w
    ypad = np.zeros(pad_to); ypad[:L] = y
    c = np.fft.rfft(ypad)
    a = c / (np.linalg.norm(c) + 1e-300)
    return a, L

def stack(series_dict, key, detrend=True):
    cs = []
    for n in NIGHTS:
        a, L = prep(series_dict[n][key], detrend=detrend)
        cs.append(a)
    cs = np.array(cs)
    R = np.abs(cs.sum(0))**2 / (np.abs(cs)**2).sum(0)
    return R, cs

def surrogates(series_dict, key, detrend=True, rng=None):
    rng = rng or np.random.default_rng(SEED)
    R = np.zeros((NSURR, len(freqs)))
    for s in range(NSURR):
        cs = []
        for n in NIGHTS:
            x = series_dict[n][key]
            L = len(x); tt = np.arange(L) * DT
            y = x - x.mean()
            if detrend: y = y - np.polyval(np.polyfit(tt, y, 1), tt)
            F = np.fft.rfft(y)
            ph = rng.uniform(0, 2*np.pi, len(F)); ph[0] = 0
            if len(F) % 2 == 0: ph[-1] = 0
            ys = np.fft.irfft(np.abs(F) * np.exp(1j * ph), n=L)
            # renormalize to preserve variance exactly
            ys = ys * (np.std(y) / (np.std(ys) + 1e-300))
            cs.append(prep(ys, detrend=False)[0])  # already detrended; same Hann+pad
        cs = np.array(cs)
        R[s] = np.abs(cs.sum(0))**2 / (np.abs(cs)**2).sum(0)
    return R

# exclusion zone: DC + 2 near-DC + top 2 bins
valid = np.ones(len(freqs), bool)
valid[[0,1,2]] = False; valid[-2:] = False

results = {}
rng = np.random.default_rng(SEED)
for key, label in [('x', 'x=v*·mu_hat (primary)'), ('k', 'kappa (primary-2)')]:
    for det in [True, False]:
        R, _ = stack(series, key, detrend=det)
        Rs = surrogates(series, key, detrend=det, rng=rng)
        band95 = np.percentile(Rs, 95, axis=0)
        exceeds = (R > band95) & valid
        results[(key, det)] = dict(R=R, band=band95, n_exceed=int(exceeds.sum()),
                                   f_exceed=freqs[exceeds].tolist())
        print(f"{label} detrend={det}: {int(exceeds.sum())} freqs exceed 95% surrogate band",
              results[(key, det)]['f_exceed'])

# SECONDARY (exploratory): zero-crossing point process
counts = []
for n in NIGHTS:
    x = series[n]['x']; tt = np.arange(len(x)) * DT
    y = x - np.mean(x); y = y - np.polyval(np.polyfit(tt, y, 1), tt)
    ctr = np.zeros(N)
    for i in range(len(y) - 1):
        if y[i] * y[i+1] < 0: ctr[i + 1] += 1
    counts.append(ctr)
counts = np.array(counts)  # nights x grid
def stack_counts(detrend=True):
    cs = []
    for c in counts:
        L = N  # already on full grid
        y = c - c.mean()
        w = np.hanning(L + 2)[1:-1]
        F = np.fft.rfft(y * w); F = F / (np.linalg.norm(F) + 1e-300)
        cs.append(F)
    cs = np.array(cs)
    return np.abs(cs.sum(0))**2 / (np.abs(cs)**2).sum(0)
Rc = stack_counts()
Rcs = np.zeros((NSURR, len(freqs)))
for s in range(NSURR):
    cs = []
    for c in counts:
        y = c.copy()
        F = np.fft.rfft(y - y.mean())
        ph = rng.uniform(0, 2*np.pi, len(F)); ph[0] = 0
        if len(F) % 2 == 0: ph[-1] = 0
        ys = np.fft.irfft(np.abs(F) * np.exp(1j * ph), n=N)
        w = np.hanning(N + 2)[1:-1]
        Fs = np.fft.rfft((ys - ys.mean()) * w); Fs = Fs / (np.linalg.norm(Fs) + 1e-300)
        cs.append(Fs)
    cs = np.array(cs)
    Rcs[s] = np.abs(cs.sum(0))**2 / (np.abs(cs)**2).sum(0)
bandc = np.percentile(Rcs, 95, axis=0)
exc_c = (Rc > bandc) & valid
nevents = int(counts.sum())
print(f"SECONDARY zero-crossing process: {nevents} events pooled; {int(exc_c.sum())} freqs exceed; {freqs[exc_c].tolist()}")

np.save('reg8b_results.npy', results, allow_pickle=True)
json.dump({f"{k[0]}_{k[1]}": dict(n_exceed=v['n_exceed'], f_exceed=v['f_exceed'],
                                  R=v['R'].tolist(), band=v['band'].tolist())
           for k, v in results.items()} |
          {"secondary": dict(n_events=nevents, n_exceed=int(exc_c.sum()),
                             f_exceed=freqs[exc_c].tolist(), R=Rc.tolist(), band=bandc.tolist()),
           "freqs": freqs.tolist(), "valid": valid.tolist(), "nights": NIGHTS},
          open('reg8b_results.json', 'w'), indent=1)
print("saved.")
