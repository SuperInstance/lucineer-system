# φ-Address: the "quilt-id" scheme — verified technique review + implementation sketch

**Date:** 2026-08-21 · **Status:** research + sketch (not yet implemented) · **Context:** Penrose document "quilt-id" idea → concrete engineering for content-addressed cells (vibe-world scale: 10⁶–10¹² cells)

**Verdict up front:** the document's core claims are *mathematically true and check out* — Fibonacci hashing is a real, proven, underused technique (Knuth §6.4; used by ska::unordered_map, SplitMix64, boost::hash_combine); the Fibonacci word is a genuine Sturmian spine whose symbol at position n is a threshold function of {nφ}, which is *exactly injective* (no repeats, ever); the Penrose vertex set does have a unique 5D lift with a triacontahedral acceptance window whose internal coordinate is a continuous local-environment descriptor. The parts that *don't* survive are: (1) "similar content → similar address" (crypto hashes scramble; the address reveals *structure*, not *semantics*), and (2) "recover exact position/address from a raw 2D coordinate" (dense-projection fragility — the forward map is O(1) and stable, the inverse is not). **Recommendation: ship v1 as the 1D Fibonacci-hash spine (`fib_word_id`, 8-byte addresses); keep 2D Penrose (`penrose_id`) as a v2 geometry layer behind a pluggable layout interface.**

---

## 1. Fibonacci hashing / golden-ratio hashing — verified technique review

### 1.1 What it is
Knuth, TAOCP Vol. 3, §6.4 ("multiplicative method"): map a key k into M slots by

```
slot(k) = floor( M · frac(k · α) )        α ≈ 1/φ = (√5 − 1)/2 ≈ 0.6180339887…
```

The standard integer form (power-of-two M = 2^b):

```
slot(k) = (k * 11400714819323198485) >> (64 − b)      // 64-bit, wrap-around multiply
```

The constant ⌈2⁶⁴/φ⌉ = 11400714819323198486; the odd value …485 is used so no bit is thrown away (even multiplier would lose the low bit). 32-bit analogue: ⌊2³²/φ⌋ = 2654435769 = **0x9E3779B9** (the boost::hash_combine constant); ⌊2³²·φ⌋ = 6949403065 = 0x19E3779B9.

The wrap-around multiply is *exactly correct* for the high-bit slot map: (k·C) mod 2⁶⁴ keeps the correct low 64 bits of the true product, and the top b bits of those are the true fractional-part bits — no 128-bit needed in C.

### 1.2 Why it's provably well-spread (the three-gap / Steinhaus theory)
- **Equidistribution (Weyl):** for irrational α, {kα} is equidistributed mod 1 — every subinterval of [0,1) gets its length-proportional share.
- **Three-gap theorem** (Steinhaus conjecture; proved by Sós, Surányi, Świerczkowski, 1950s): the n points {α}, {2α}, …, {nα} cut the circle into gaps of **at most three distinct lengths**; when three, the largest equals the sum of the other two.
- **The golden ratio is the champion case:** because CF(φ) = [1;1,1,…] (all partial quotients 1), the three-gap degenerates to **exactly two gap lengths at every n**, in ratio φ (long/short = φ). Each new point lands in a largest gap and splits it in golden ratio — the phyllotaxis property (leaves/seeds spaced at 137.50776° = 360°/φ²). This is why {kφ} looks "maximally even" at *every* prefix length, not just asymptotically: φ's best rational approximants are F_{k+1}/F_k, converging as slowly as possible (Dirichlet), so the sequence can't bunch up at any finite n. Minimal phase separation for n ≤ N is Θ(1/N) — specifically ≈ 1/(φ·N) (smallest gap ~ 1/F_{k+1} where F_k ≤ N < F_{k+1}).
- **No repeats (exact):** {nφ} = {mφ} ⇔ (n−m)φ ∈ ℤ ⇔ n = m (φ irrational). Injectivity holds for *all* integers n, m — not just probabilistically.
- **Not a great standalone hash:** as a *finalizer* it shows patterns (the blog's own analysis); as a *range-map from an already-mixed hash* (or from sequential IDs) it's excellent — robust where `%` fails (low-bit patterns, sequential keys) and ~free (1 multiply vs ~9ns modulo).

### 1.3 Real-world use (verified)
- **ska::unordered_map** (Rich Geldreich) — Fibonacci hashing for slot selection; benchmarked ~2× faster than libstdc++/libc++ unordered_map lookups (probablydance.com, 2018).
- **SplitMix64 / MurmurHash3 fmix64** — the gamma 0x9E3779B97F4A7C15 is exactly ⌈2⁶⁴/φ⌉−1; it's the golden-ratio step used to scramble the internal counter.
- **boost::hash_combine** — 0x9e3779b9 = ⌊2³²/φ⌋.
- **Phyllotaxis / procedural content generation** (Vi Hart's golden-angle videos; standard advice: for anti-clustered "random-looking" placement, try golden-angle steps before Halton before RNG).
- **Low-discrepancy / quasi-Monte Carlo:** the Kronecker sequence {kφ} is the canonical 1D low-discrepancy sequence; 2D version uses α = (1/φ, 1/φ²) (the "R2" sequence).

---

## 2. The Fibonacci word as an addressing spine

### 2.1 Verified facts
- Definition: morphism 0→01, 1→0 (equivalently a→ab, b→a), fixed point
  `w = 0100101001001010010100100101001…` (OEIS A003849; the "rabbit sequence" is the same word up to swapping symbols and shifting by one).
- **Closed form (1-indexed):** `w(n) = 2 + ⌊nφ⌋ − ⌊(n+1)φ⌋` ∈ {0,1}. Verified against the first digits (0,1,0,0,1,0,1,…).
- **Symbol = threshold of phase:** `w(n) = 1 ⇔ {nφ} < 1/φ²` (≈ 0.381966). So the *symbol and the phase are the same data* — the word is literally the "gap-length sequence" of the golden-angle point distribution (long gap = 0, short gap = 1; Wikipedia confirms the two-length pattern and its identity with the Fibonacci word).
- Positions of 1s = Upper Wythoff sequence ⌊kφ²⌋ (A001950); positions of 0s = Lower Wythoff ⌊kφ⌋ (A000201).
- **Sturmian (minimal complexity):** exactly n+1 distinct factors of length n; balanced (any two equal-length factors differ in #1s by ≤ 1); aperiodic; recurrent (every factor occurs infinitely often); forbids 11 and 000; densities: #0s : #1s = φ, i.e. 1/φ vs 1/φ².
- **Zeckendorf connection:** w(n) = 1 iff the Zeckendorf representation of n (sum of distinct non-consecutive Fibonacci numbers) "includes a 1"; equivalently via fibbinary numbers mod 2. Zeckendorf = a φ-ary place-value system for n → gives the *global hierarchy* (below).
- Used as a model of 1D quasicrystals ("Fibonacci quasicrystal"); famous as the worst case for repetition-detection algorithms.

### 2.2 What "prefix uniqueness" does and doesn't mean (honest)
- A factor of length k does **not** pin a unique position: it occurs infinitely often (recurrence) — there are only k+1 distinct factors of length k.
- What *is* unique: the **phase {nφ}**. It is globally injective, so `(symbol, phase)` identifies the position exactly (in the ideal reals). In fixed point it identifies it to precision 2^(−p) — good to ~2⁴⁰ cells with a 64-bit phase (margin ~2²³ over the worst-case 1/(φN) gap).
- Practical spine property: n ↦ (w(n), {nφ}) is an embedding of ℕ into {0,1}×[0,1) with provable minimum separation — i.e. the *position itself* carries a local-environment descriptor.

### 2.3 Finite implementation (no storage, O(1) compute)
- Index: n ∈ [0, 2^b), b = ⌈log2 N_max⌉ (40 for 10¹²).
- Phase (exact integer math, not floats — doubles lose injectivity for N ≳ 2²⁵ because the error of computing n·φ in doubles is ~2⁻²² ≫ the 1/(φN) gap):
  - 32-bit phase, n < 2³²: `p = (n * 6949403065) & 0xFFFFFFFF` (low 32 bits are exact even though the product overflows 64 bits).
  - 40–64-bit n: split multiply (16-bit limbs; every partial product < 2⁴⁸, exact in doubles/Luau, or use __uint128 in C).
- Symbol: `sym = (p32 < (2^32 / φ²)) ? 1 : 0` with 2³²/φ² = 2³²·(2−φ) = 2·2³² − 2³²φ = 8589934592 − 6949403065 = 1640531527. (Verify: 0x61C88647 = 1640531527 ✓ — this is the well-known 0x61C88647 constant! Nice.)
- Window/slack: for growth headroom keep b fixed at 40–48 and treat the top bits as version/flag nibbles.

**Precision analysis:** phase resolution 2⁻⁶⁴ vs worst-case min gap 1/(φ·2⁴⁰) ≈ 2⁻⁴⁰.7 → 2²³ margin. For 10¹² cells the spine is collision-free *by construction* (n differs ⇒ ideal phase differs; computed phase preserves separation). The only real collision surface is at the content-hash level (below).

---

## 3. 2D Penrose coordinates for cells (cut-and-project, de Bruijn 1981)

### 3.1 The construction (verified)
- Embed ℤ⁵ with a 2D "physical" plane E∥ and 3D "internal" plane E⊥, both irrational w.r.t. ℤ⁵.
- Physical projection: π∥(n) = Σ nᵢ·ζⁱ, ζ = e^{2πi/5} (5 unit vectors at 72°).
- Internal projection: π⊥(n) = Σ nᵢ·vᵢ, {vᵢ} = 5-fold icosahedral star in ℝ³ (tabled constants; gauge fixed by Σnᵢ ∈ {0,1}).
- **Window W = projection of the unit 5-cube onto E⊥ = the rhombic triacontahedron** (zonohedron of the 5 generators; 30 faces, 60 edges, 32 vertices; face normals = icosidodecahedron directions — 30 tabled half-space tests, prefilter with bounding sphere ‖u‖ ≤ R).
- **Selection rule:** n is a *vertex of the Penrose tiling* iff π⊥(n) ∈ W. This is the full, exact rule (equivalent to de Bruijn's pentagrids / multigrid method; also expressible as an integer-exact condition on the 5 grid phases, Σ{γᵢ} ∈ {1,2}).
- **Unique lift:** π∥ is injective on ℤ⁵ (E∥ irrational), so each vertex has a unique 5D address n. P3 (rhombus) tiling: thin rhombus 36°/144°, thick 72°/108°.
- **Local environment from internal coordinate (the document's claim — true, with a caveat):** the tiling has only finitely many vertex-star types — **7 for the kite/dart (P2) tiling (star, ace, sun, king, jack, queen, deuce) and 7 for the rhombus (P3) tiling (54 angle-combinations reduce to 7 allowed, one arising two ways)** (verified, Wikipedia/Grünbaum–Shephard). The window is partitioned by the grid hyperplanes into acceptance domains; a vertex's internal coordinate u ∈ W lands in one domain, and that domain determines the local environment. So: u is a *continuous* descriptor of the neighborhood (Lipschitz: |u(n)−u(m)| ≤ ‖π⊥‖·‖n−m‖), and its quantization is a *stable* local-environment tag (biome/star-type), stable under small perturbations as long as you stay off the domain boundaries.

### 3.2 Is a small tuple enough? (sizes)
| representation | bits | for N = 10⁶ | for N = 10¹² |
|---|---|---|---|
| 5D integer (canonical) | 5×b, b≈16 | 80 bits = 10 B | 80 bits = 10 B |
| 5D minus gauge (Σnᵢ=0 ⇒ 4 coords stored) | 4×16 | 64 bits = 8 B | 64 bits = 8 B |
| cached internal phase u (quantized) | 3×12–16 | +36–48 bits (optional, hot cells) | same |
| vertex-star type | 3 | +3 bits (derivable, cache only) | same |
| physical position | — | computed on demand (2×f32), never stored | same |

**Answer:** yes — a practical quilt-id is (4×16-bit ints = 8 bytes) + optional 2-bit tile-type + cached 3×12-bit phase. You do *not* need 5 integers or float pairs; the 5D integer **is** the compact form, and everything else (x∥, x⊥, star type, neighbors, parent) is a pure O(1) function of it.

### 3.3 Navigation facts (verified)
- **Neighbors via matching rules = O(20) window tests:** candidate neighbors are n ± (eᵢ − eⱼ), 20 vectors (10 edge directions × 2); keep those whose lifted point passes the window test. No storage, no search.
- **Hierarchy via substitution (inflation/deflation):** Penrose tilings are self-similar; inflation acts on the lift as a fixed 5×5 integer matrix A (Perron eigenvalue φ², A·W ⊆ W, A·ℤ⁵₀ ⊆ ℤ⁵₀ — entries tabled from the P3 substitution rule; property-level spec given below). Parent cell = A·n, O(25) integer ops. This is the *exact* "global hierarchy from one address": each inflation step multiplies physical size by φ.
- **The vertex set is Delone** (uniformly discrete: min separation = edge length; relatively dense: covering radius O(1)) — the *geometry* is robust to small perturbations. But see §5/§7 for why the *inverse* lift is not.

---

## 4. Navigation: is there a "golden Hilbert curve"?

Honest answer: **no exact analogue, and you don't need one.** Three candidate patterns, in increasing usefulness:

1. **Phyllotaxis / golden spiral** (polar plot of {kφ}): a genuinely space-filling *ordering* with excellent anti-clustering — but its defining property is that consecutive indices are *spread apart*, i.e. it's anti-local. A Hilbert curve exists precisely to *sacrifice* spread for locality; golden order sacrifices locality for spread. You can't have both (this is the low-discrepancy trade-off, not a fixable bug). Use it to *order* cells (which cell to stream next), not to *locate* neighbors.
2. **Fibonacci word fractal curve** (verified): drawing rule on the word (0: turn ±90° by parity; 1: straight); never self-intersects; self-similar at all scales with reduction ratio 1+√2 (silver ratio); **Hausdorff dimension = 3·log φ / log(1+√2) ≈ 1.638 < 2** — so it is NOT a space-filling curve (not surjective); four copies make a "Fibonacci tile" that *almost* tiles the plane (central hole → 0). Beautiful as a *visual spine* for the quilt (the "quilt" metaphor, literally), useless as a bijective cell index. Use for layout/aesthetics, not addressing.
3. **Substitution hierarchy + matching rules — the working pattern:** exact, O(1) navigation in both directions of scale (inflation matrix A up, window-tested neighbors laterally). This is strictly better than a Hilbert analogue for aperiodic geometry: Hilbert gives you a 1D order with 2D locality; Penrose gives you *exact* lateral adjacency (20 candidates) and *exact* scale hierarchy (1 matrix) with zero storage. In 1D, the analogue is Zeckendorf: truncating n's Zeckendorf digits to the k most significant gives the coarser-scale position — the spine's "level k ancestor" (the 1D substitution hierarchy of the Fibonacci word).

**Bottom line for the doc's "φ-spiral / space-filling order, locality-preserving total order" question:** the correct total order is the spine order itself (n ↦ {nφ}); the correct locality machinery is matching rules + inflation, both O(1); a golden "Hilbert" is a category error.

---

## 5. Content addressing: how close can engineering get?

The scheme is two *separate* maps that must not be conflated:

```
content ──h──> hash h (128-bit) ──rank──> n (spine index) ──φ-map──> (symbol, phase) + Zeckendorf hierarchy
                                                  │
                                                  └──(v2)──> 5D lift n' ──> x∥ (physical), u = x⊥ (internal)
```

- **content → n:** `n = fib_hash_slot(h, b)` (the §1 map). Robust to sequential h (consecutive content IDs land on well-separated spine positions — three-gap), uses all hash bits, O(1). Collisions are birthday-bound at the hash level: N = 2⁴⁰, 128-bit h ⇒ collision prob ≈ N²/2¹²⁸ = 2⁻⁴⁸ — negligible; tunable.
- **n → (symbol, phase):** exact threshold/frac of {nφ} — *this* is where "the address reveals the local neighborhood" is true: the phase tells you where in the local gap structure the cell sits, the symbol gives its run-type (0s come in runs of length ≤ 2, 1s are isolated), the 3-quantized internal coordinate (v2) gives the vertex-star type.
- **n → global hierarchy:** true in the address→structure direction — Zeckendorf digits of n (1D) or the inflation matrix A (2D) give the cell's ancestors at every scale. "One hash reveals local environment AND global hierarchy" is achievable **as an address property**, not as a content property.
- **What breaks (be honest about this):**
  1. **Semantic locality is impossible with a crypto hash.** "Similar content → nearby addresses" does not follow from anything in §1–§3. If the product actually needs it (e.g., "all blue-quilt patches cluster"), you need locality-sensitive hashing (MinHash on shingles, etc.) to *drive* the address — but LSH clusters and φ spreads: they fight. Resolution: two-level address (LSH bucket id + φ-rank within bucket) and pick which goal matters.
  2. **Addresses are content-derived ⇒ immutable cells.** Edit content ⇒ new hash ⇒ new address. That's the standard content-addressing contract (like git), but it means the world needs a namespace/registry layer (hash → live entity) and garbage collection.
  3. **Position → address (reverse) is fragile** — see §7. Never build reverse lookup on the φ-map; use a real spatial index.
  4. **v2 window test** needs deterministic float handling at boundaries (canonical rounding or the integer-exact pentagrid-phase formulation).

---

## 6. Pseudocode

### Scheme A — `fib_word_id` (1D spine; SHIP THIS)

```
# Constants (64-bit)
C      = 11400714819323198485      # odd ⌈2^64/φ⌉−1  (SplitMix64 gamma)
PHI32  = 6949403065                # ⌊2^32·φ⌋
THRESH = 1640531527                # ⌊2^32/φ²⌋  (= 2·2^32 − PHI32)
B      = 40                        # spine bits (supports 2^40 ≈ 10^12 cells)

# Exact 64-bit (h*C) mod 2^64 via 16-bit limbs — works in C, Lua/Luau doubles, JS
# (all partial products < 2^48, exactly representable)
def mulmod64(a, b):
    a0, a1, a2, a3 = a & 0xFFFF, (a>>16)&0xFFFF, (a>>32)&0xFFFF, (a>>48)&0xFFFF
    b0, b1, b2, b3 = b & 0xFFFF, (b>>16)&0xFFFF, (b>>32)&0xFFFF, (b>>48)&0xFFFF
    p0 = a0*b0
    p1 = a0*b1 + a1*b0
    p2 = a0*b2 + a1*b1 + a2*b0
    p3 = a0*b3 + a1*b2 + a2*b1 + a3*b0          # carry p0,p1,p2 upward mod 2^64
    c1 = (p1 + (p0 >> 16)) >> 16
    c2 = (p2 + c1) >> 16
    return ((p3 + c2) & 0xFFFF) << 48 | ((p2 + c1) & 0xFFFF) << 32 | \
           ((p1 + (p0>>16)) & 0xFFFF) << 16 | (p0 & 0xFFFF)

def fib_word_id(content_hash_128):
    h  = content_hash_128 & ((1<<64)-1)
    n  = mulmod64(h, C) >> (64 - B)             # spine index, 0..2^B−1
    # phase: exact low 32 bits of n·PHI32  (n < 2^40 ⇒ use split multiply; sketch:
    #    p32 = low32( mulmod64(n, PHI32) )     # = frac(n·φ)·2^32, error ≤ 1 ulp
    p32 = mulmod64(n, PHI32) & 0xFFFFFFFF
    sym = 1 if p32 < THRESH else 0              # w(n) = 1 ⇔ {nφ} < 1/φ²
    return n, sym, p32
    # n        : the address (8 bytes as uint64; 5 packed with version/flag nibbles)
    # sym, p32 : free local-environment descriptors (recomputable, cache if hot)

def zeckendorf_level(n, k):                     # global hierarchy (O(log n))
    # greedy: largest F_j ≤ n ... digits d_j ∈ {0,1}, no two adjacent 1s
    # ancestor at scale k = n with digits below position k zeroed
    ...
```

Collision guarantees (stated precisely):
- Distinct n ⇒ distinct (ideal) phase — *exact* (irrationality of φ). Computed phase preserves this for n < 2⁴⁰ (min gap 2⁻⁴⁰·⁷ vs 2⁻⁶⁴ resolution).
- Distinct content ⇒ distinct n with prob 1 − 2⁻⁴⁸ (N = 2⁴⁰, 128-bit hash) — the *only* collision surface.
- Complexity: O(1) arithmetic, zero storage. Serialized size: 8 B aligned (6 B packed: [ver:4][flags:4][n:40] + 16 spare).

### Scheme B — `penrose_id` (2D Penrose; v2, behind a pluggable layout interface)

```
# Embedding (de Bruijn P3). Tabled constants — pin exactly from a reference
# implementation (de Bruijn 1981 / Baake–Grimm "Aperiodic Order") before shipping.
ZETA[i] = (cos(2πi/5), sin(2πi/5))             # i = 0..4, physical star (unit)
V[i]    = icosahedral 5-fold star in R3        # ΣV[i] ≠ 0; gauge fixed below
W       = rhombic triacontahedron: 30 half-spaces {u : u·fⱼ ≤ 1, j=0..29}  # tabled fⱼ
A       = 5×5 integer P3 inflation matrix      # property spec: A·Z⁵₀ ⊆ Z⁵₀,
                                               #   Perron eigenvalue φ², A·W ⊆ W
def in_window(u):
    if u·u > R²: return False                  # bounding-sphere prefilter
    return all(u·fⱼ ≤ 1 for fⱼ in W_FACES)     # 30 tests, O(1)

def penrose_id(content_hash_128):
    for attempt in 0..MAX_ATTEMPTS:            # expected ≤ ~10 (acceptance is a
        h  = mix(content_hash_128, attempt)    #   fixed positive constant, ~10–25%)
        n  = [ (h >> 16*i) & 0xFFFF for i in 0..3 ]
        n += [ -sum(n) ]                       # gauge: Σnᵢ = 0  (4×16 bits stored)
        u  = Σ n[i] * V[i]                     # internal coords (3 floats)
        if in_window(u):
            x  = Σ n[i] * ZETA[i]              # physical 2D position (on demand)
            return n, x, u
    raise OverflowError("window acceptance failed (deterministic retry bound)")

def penrose_neighbors(n):                      # matching rules via lift, O(20)
    return [ n + d for d in EDGES20
             if in_window(Σ (n+d)[i] * V[i]) ] # EDGES20 = {±(eᵢ−eⱼ) : i≠j}

def penrose_parent(n):                         # global hierarchy, O(25) integer ops
    return normalize_gauge(A · n)              # larger-scale vertex; repeat for LOD

def penrose_star_type(u):                      # local environment (≤ 7 types)
    return lookup_domain(quantize(u, 3×12 bits))   # tabled acceptance-domain map
```

- Collision surface: same as A (hash level only); the window test adds *rejection* (retry), never aliasing.
- Complexity: O(1) expected (≤ ~10 retries; deterministic bound), O(20) neighbor query, O(1) inflation. Serialized size: 8 B (4×16-bit, gauge-implied) or 10 B self-contained.
- Size comparison at 10¹² cells: A = 8 B; B = 8–10 B + optional cached phase/star-type. **2D costs ~same bytes, ~20× the implementation surface.**

---

## 7. Honest limitations

1. **Exact-position recovery is fragile — Delone stability vs dense-projection fragility.** The *vertex set* is Delone (uniformly discrete + relatively dense): the tiling's geometry is stable under small perturbations. But the *lift* is not: π∥(ℤ⁵) is dense in ℝ², so for any physical point x and any ε there exist lattice points projecting within ε of x with internal coordinates arbitrarily close to the window boundary — an ε-perturbation flips window membership and the 5D address. Inverting π∥ from a noisy 2D coordinate is a closest-lattice-point problem with no stable closed form. **Forward (address → geometry): O(1), exact, stable. Reverse (geometry → address): needs a real spatial index; do not ship the naive inverse.**
2. **Similar-content locality does not exist** with crypto hashes (§5). If "quilt patches of similar content cluster" is a product requirement, use LSH to drive the address and accept that φ-spread and LSH-clustering are in tension.
3. **Fixed-point phase is injective only up to precision.** Ideal {nφ} is injective for all n; the computed 32-bit phase is injective for n < 2³² and the 64-bit phase for n < 2⁶⁴ (in the exact integer formulation). Using doubles for the phase breaks at N ≳ 2²⁵ (error ~2⁻²² vs gap ~2⁻²⁵·⁷). The integer formulations in §6 avoid this entirely.
4. **Window-boundary determinism (v2):** near-boundary lattice points require canonical rounding or the integer-exact pentagrid-phase membership test; float membership must be specified with an epsilon + deterministic tie-break so addresses are reproducible across engines (this matters for a multi-client world).
5. **"Address reveals hierarchy" is one-directional.** The address encodes *structural* scale (Zeckendorf / inflation), not *semantic* scale. A hash cannot know whether content is a "city" or a "brick"; hierarchy labels must come from content features, not from the φ-machinery.
6. **Namespace management is orthogonal.** Content-derived addresses are immutable and collision-free with probability 1 − 2⁻⁴⁸; but mapping live entities to addresses (registry, GC, re-homing after content edit) is a separate system the φ-scheme does not provide.
7. **In 2D, "quilt" cells ≠ vertices.** Vertices are what the lift addresses; *tiles* (rhombs) are dual — tile-id needs a half-integer/honeycomb-style offset (e.g., address the tile by its acute-vertex lift, or by the dual graph node = rhombus center with its own 5D expression). Design the tile-level id before building on vertex-level.

---

## 8. Recommendation

**Ship v1 as `fib_word_id` (1D Fibonacci-hash spine).** Reasons:
- 8-byte addresses, ~3 integer ops, zero storage, exact no-repeat phase (irrationality of φ), provable spread at every prefix (three-gap/two-gap), free local-environment descriptor (symbol + phase) and free global hierarchy (Zeckendorf digits).
- The spine is *geometry-agnostic*: n is just a total order; the layout (linear strip, phyllotaxis spiral, hex grid, or later Penrose) is a pluggable function n ↦ position. The document's "quilt" gets its ordering spine now and its shape later.
- Real-world precedent (Knuth §6.4, ska::unordered_map, SplitMix64) means the core technique is battle-tested; the novel part is small (symbol/phase descriptors) and unit-testable in an afternoon.

**Keep `penrose_id` as v2** — it is the right *geometry* for a pentagonal vibe-world (5-fold symmetry is its whole identity), and the machinery is all O(1) (window test, 20-candidate neighbors, inflation matrix, 7 star types), but it adds: window retry loops, boundary-determinism rules, tile-vs-vertex duality, tabled embedding constants, and ~20× the test surface — for zero additional *addressing* guarantee over v1. Build it only when the world visibly needs 5-fold spatial structure.

**Suggested build order:**
1. Reference `fib_word_id` (C + Lua/Luau), ~80 lines.
2. Property tests: (a) spread — min phase gap among first 10⁶ indices ≥ 1/(2φ·10⁶); (b) injectivity — 2⁴⁰ distinct (sym,p32) pairs bit-exact; (c) symbol consistency — sym == (p32 < THRESH); (d) hash-robustness — sequential h ⇒ well-separated n (three-gap: ≤ 2 gap sizes).
3. If v2: pin the embedding constants, tile-level id, and a golden-image test (render 10⁴ vertices, verify 5-fold symmetry + Delone min-distance).

---

## Appendix: constants & sources

- φ = (1+√5)/2 ≈ 1.6180339887498948; φ⁻¹ = φ−1 ≈ 0.6180339887; 1/φ² = 2−φ ≈ 0.3819660113; golden angle = 360°/φ² ≈ 137.50776°.
- 0x9E3779B9 = 2654435769 = ⌊2³²/φ⌋ (boost::hash_combine). 0x19E3779B9 = 6949403065 = ⌊2³²·φ⌋. 0x9E3779B97F4A7C15 = 11400714819323198485 = odd ⌈2⁶⁴/φ⌉ (SplitMix64 gamma; Majkowski's Fibonacci-hash constant). 0x61C88647 = 1640531527 = ⌊2³²/φ²⌋.
- Verified: three-gap theorem (Steinhaus conjecture; Sós/Surányi/Świerczkowski 1950s); Weyl equidistribution; two-gap property for φ and its identity with the Fibonacci word (Wikipedia Fibonacci word); w(n) = 2+⌊nφ⌋−⌊(n+1)φ⌋; Wythoff positions; Zeckendorf criterion; complexity n+1, balance, recurrence, no 11/000; Fibonacci word fractal dim 3logφ/log(1+√2) ≈ 1.638, never self-intersecting, Fibonacci tile almost-tiles the plane (Wikipedia); de Bruijn 1981 pentagrid + cut-and-project equivalence, triacontahedron window, 7+7 vertex figures (Wikipedia Penrose tiling); inflation/deflation self-similarity; quasicrystal/Bragg context.
- Sources: Knuth TAOCP 3 §6.4; probablydance.com/2018/06/16/fibonacci-hashing… (Majkowski); Wikipedia: Fibonacci word, Fibonacci word fractal, Three-gap theorem, Sturmian word, Penrose tiling; OEIS A003849, A000201, A001950; de Bruijn, "Algebraic theory of Penrose's non-periodic tilings of the plane" (1981); Baake & Grimm, *Aperiodic Order* (window/matching-rule formalism).
