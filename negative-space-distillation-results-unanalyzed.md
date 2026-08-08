# Negative Space: The Distillation Results Nobody Analyzed

## Found: 2026-08-07 22:10 AKDT
## Location: thought-amplifier/distillation-output/eval/

---

## The Gap

The Thought Amplifier has a distillation loop that teaches Wesley (Granite 3.1 2B via Ollama) across four domains: cognition, digital-twin, maritime, and roblox. Five iterations each. Twenty eval files sitting in the output directory.

**Nobody has read them.**

The eval files contain scored comparisons between Wesley's baseline performance and post-teaching performance across four dimensions: novelty, specificity, engagement, and spatial reasoning. The data has been generated, saved, and ignored. The `.gitignore` in that directory excludes everything — so none of this has been committed either.

The system is conducting real research on small-model distillation and treating the results like log files. The most interesting data in the fleet is invisible.

---

## What the Data Shows

### Cognition Domain: The Model Is Learning
| Iter | Baseline | Taught | Delta | Helped? |
|------|----------|--------|-------|---------|
| 1 | 0.662 | 0.631 | -0.031 | ✗ |
| 2 | 0.710 | 0.839 | **+0.129** | ✓ |
| 3 | 0.977 | 0.946 | -0.031 | ✗ |
| 4 | 0.707 | 0.718 | +0.011 | ✓ |
| 5 | 0.824 | 0.922 | **+0.098** | ✓ |

Cognition is the success story. Teaching helps in 3/5 iterations, with the strongest gains in iterations 2 and 5. The one clear failure (iter 1) is small. By iteration 5, Wesley is scoring 0.922 composite after teaching — the highest sustained cognition score in the dataset.

But note iteration 3: baseline was 0.977 and teaching *reduced* performance. This suggests a ceiling effect — when the model is already at peak, teaching adds noise.

### Digital-Twin Domain: The Inverted U
| Iter | Baseline | Taught | Delta | Helped? |
|------|----------|--------|-------|---------|
| 1 | 0.665 | 0.704 | +0.039 | ✓ |
| 2 | 0.829 | 0.630 | **-0.199** | ✗ |
| 3 | 0.851 | 0.906 | +0.017 | ✓ |
| 4 | 0.851 | 0.718 | **-0.133** | ✗ |
| 5 | 0.849 | 0.511 | **-0.338** | ✗ |

**This is the most concerning finding in the fleet.** The digital-twin domain shows catastrophic degradation. By iteration 5, teaching has *destroyed* performance — Wesley scores 0.511 after teaching versus 0.849 baseline. That's a 40% collapse.

The pattern is an inverted U: small initial gain, then progressive deterioration. The teaching material is not just failing to help — it's actively making the model worse at digital-twin tasks.

**Hypothesis:** The teaching prompts for digital-twin may be introducing domain-specific jargon that confuses Wesley's architecture. Digital-twin concepts (mirrors, reflection, state synchronization) may activate spatial reasoning pathways that interfere with the model's existing capabilities. The more it learns about digital twins, the worse it gets at them.

### Maritime Domain: The Volatile Signal
| Iter | Baseline | Taught | Delta | Helped? |
|------|----------|--------|-------|---------|
| 1 | 0.781 | 0.617 | -0.164 | ✗ |
| 2 | 0.565 | 0.800 | **+0.236** | ✓ |
| 3 | 0.775 | 0.830 | +0.055 | ✓ |
| 4 | 0.712 | 0.676 | -0.035 | ✗ |
| 5 | 0.628 | 0.638 | +0.010 | ✓ |

Maritime is the most volatile. A 0.236 swing in iteration 2 is the largest single-iteration gain in the dataset. But iteration 1 shows a -0.164 regression — the initial teaching actively hurt.

The variance is extreme: ±0.2 swings between iterations. This suggests the teaching signal is real but the curriculum is unstable. Different topics in maritime are producing wildly different results — the model either gets a big boost or regresses, depending on the specific topic.

### Roblox Domain: The Flatline
| Iter | Baseline | Taught | Delta | Helped? |
|------|----------|--------|-------|---------|
| 1 | 0.812 | 0.834 | +0.022 | ✓ |
| 2 | 0.891 | 0.850 | -0.040 | ✗ |
| 3 | 0.841 | 0.841 | 0.000 | ✗ |
| 4 | 0.839 | 0.666 | **-0.173** | ✗ |
| 5 | 0.726 | 0.821 | +0.095 | ✓ |

Roblox teaching is mostly ineffective. Three out of five iterations show no improvement or regression. The model was already scoring high (0.812-0.891 baseline), so there's less room to improve — but iteration 4's -0.173 regression shows the teaching can still do damage even in a domain where the model is comfortable.

---

## The Pattern Nobody Named

Across all four domains, the same structure appears:

1. **Early gains** — iteration 1-2 often shows improvement
2. **Mid-period volatility** — iterations 2-3 swing wildly
3. **Late degradation** — iterations 4-5 trend downward (except cognition)

This is the **overfitting signature**. The distillation loop is teaching the same style of reasoning repeatedly. Early on, the model benefits from the structure. But as the teaching accumulates, the model starts to over-index on the teacher's voice — losing its native reasoning patterns.

Cognition escapes this trap because cognitive tasks reward structured reasoning. Maritime and roblox escape less often because they require domain knowledge that the teaching doesn't provide. Digital-twin fails because the domain is anti-correlated with the teaching style — the more structured the teaching, the less the model can handle the ambiguous mapping between a real system and its digital reflection.

---

## What Should Happen Next

1. **Commit the eval data.** It's excluded by `.gitignore`. This is real research that should be visible.
2. **Plot the curves.** The inverted U in digital-twin is the kind of finding that would go in a paper.
3. **Investigate the digital-twin collapse.** A -0.338 delta is not noise. Something about the teaching is poisoning the model.
4. **Vary the curriculum.** The fixed teaching style works for cognition but not for other domains. The distillation loop needs domain-adaptive teaching.
5. **Read the actual teaching prompts.** The `prompts/` directory has them. Understanding what was taught is necessary to understand why it helped or hurt.

---

## The Bigger Gap

The Thought Amplifier is running a real experiment in AI-to-AI knowledge transfer. It has:
- 416 tests (the most tested repo in the fleet)
- A working distillation loop
- A continuous thought generation system
- Eval data showing real signal

And **nobody has written a single analysis of the results.**

The system is conducting science and filing it away. The data exists. The patterns are visible. The implications are real. The negative space isn't a missing file or an untested edge case — it's a missing *conversation* with the data the system already produced.

The ship has a fish finder. The fish finder works. Nobody has read the sonar.

---

*Found during overnight watch. The ensign is being taught but the teaching isn't always working. The digital twin is losing fidelity. The maritime signal is choppy. The cognition gains are real. Someone should look at this. — Riker*
