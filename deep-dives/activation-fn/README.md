# Activation Functions: A Complete Tutorial

> **`activation-fn`** — A Rust library for neural network activation functions  
> **Version:** 0.1.0 · **License:** MIT OR Apache-2.0  
> **Repository:** [SuperInstance/activation-fn](https://github.com/SuperInstance/activation-fn)

---

## Table of Contents

1. [Installation](#installation)
2. [What Are Activation Functions?](#what-are-activation-functions)
3. [The Five Functions](#the-five-functions)
   - [Sigmoid](#1-sigmoid)
   - [ReLU](#2-relu--rectified-linear-unit)
   - [Tanh](#3-tanh--hyperbolic-tangent)
   - [Leaky ReLU](#4-leaky-relu)
   - [Softmax](#5-softmax)
4. [When to Use Each (Decision Tree)](#when-to-use-each-decision-tree)
5. [Line-by-Line Code Walkthrough](#line-by-line-code-walkthrough)
6. [Numerical Examples](#numerical-examples)
7. [Common Pitfalls](#common-pitfalls)
8. [API Reference](#api-reference)

---

## Installation

### As a Cargo dependency

```toml
[dependencies]
activation-fn = "0.1"
```

```rust
use activation_fn::{sigmoid, relu, tanh, leaky_relu, softmax};

fn main() {
    println!("sigmoid(0) = {}", sigmoid(0.0));  // 0.5
    println!("relu(-3) = {}", relu(-3.0));       // 0.0
    let probs = softmax(&[1.0, 2.0, 3.0]);
    println!("softmax = {:?}", probs);           // [0.09, 0.2447, 0.6652]
}
```

### From source

```bash
git clone https://github.com/SuperInstance/activation-fn
cd activation-fn
cargo build --release
cargo test
```

### No-Cargo quick start (copy-paste)

No dependencies needed — just `std`:

```rust
fn sigmoid(x: f64) -> f64 { 1.0 / (1.0 + (-x).exp()) }
fn relu(x: f64) -> f64 { x.max(0.0) }
fn softmax(logits: &[f64]) -> Vec<f64> {
    let max = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exps: Vec<f64> = logits.iter().map(|&x| (x - max).exp()).collect();
    let sum: f64 = exps.iter().sum();
    exps.iter().map(|&e| e / sum).collect()
}
```

---

## What Are Activation Functions?

### The Problem with Pure Linear Networks

Imagine a neural network with 100 layers, all linear:

```
Layer 1:  y₁ = W₁·x + b₁
Layer 2:  y₂ = W₂·y₁ + b₂
...
Layer 100: y₁₀₀ = W₁₀₀·y₉₉ + b₁₀₀
```

You can collapse all 100 layers into a single matrix multiplication:

```
y₁₀₀ = (W₁₀₀ · W₉₉ · ... · W₁) · x + (collapsed bias) = W_eff · x + b_eff
```

**100 layers = 1 layer.** The depth is an illusion. The network can only learn linear relationships.

### The Solution: Non-Linearity

An activation function `f` applied after each linear transform breaks the collapse:

```
Layer 1:  h₁ = f(W₁·x + b₁)
Layer 2:  h₂ = f(W₂·h₁ + b₂)
```

Now `h₂ ≠ (W₂W₁)·x + ...` because `f` is non-linear. The network can approximate **any continuous function** (Universal Approximation Theorem, Cybenko 1989).

### Intuition: Neurons as Decisions

A biological neuron either fires or doesn't — it's a threshold device. An activation function simulates this:

- **Input** = sum of weighted signals from other neurons
- **Activation function** = the "decision" to fire
- **Output** = the signal strength sent onward

Different activation functions = different decision rules:

| Rule | Question it answers |
|------|-------------------|
| Sigmoid | "How confident am I? (0% to 100%)" |
| ReLU | "Is this signal worth passing forward? (yes/all-or-nothing)" |
| Tanh | "Is this good or bad? (-100% to +100%)" |
| Leaky ReLU | "Is this signal worth passing? (mostly yes, tiny bit for no)" |
| Softmax | "Which option should I choose? (probability distribution)" |

---

## The Five Functions

### 1. Sigmoid

**Formula:**
$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

**Output range:** (0, 1) — always positive, never exactly 0 or 1.

**Intuition:** "The squash function." Sigmoid takes any real number and squashes it into a probability between 0 and 1. An input of 0 maps to exactly 0.5 (50/50). Large positive inputs squash toward 1. Large negative inputs squash toward 0.

**Derivative:**
$$\sigma'(x) = \sigma(x) \cdot (1 - \sigma(x))$$

The derivative is beautifully simple — no need to recompute the exponential. Just multiply the output by one minus the output. But note: the maximum derivative is **0.25** at x=0. This means gradients shrink by at least 75% per layer — the **vanishing gradient problem**.

**History:** Introduced by Pierre François Verhulst in 1838 as a model of population growth. Adopted by neural network research in the 1980s-1990s as the default activation.

**When to use:**
- Output layer for binary classification (yes/no predictions)
- Gates in LSTM/GRU recurrent networks (forget gate, input gate, output gate)
- Anywhere you need a smooth probability

**When NOT to use:**
- Hidden layers in deep networks (use ReLU instead)
- Multi-class outputs (use softmax)

---

### 2. ReLU (Rectified Linear Unit)

**Formula:**
$$\text{ReLU}(x) = \max(0, x)$$

**Output range:** [0, +∞)

**Intuition:** "If it's positive, let it through. If it's negative, kill it." ReLU is the simplest possible non-linear function — a single `if` statement. It's the **bent wire** shape: flat for negatives, diagonal for positives.

**Derivative:**
$$\text{ReLU}'(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}$$

The gradient is either 1 or 0. **No vanishing gradient** for positive signals. This is why ReLU enabled training networks with hundreds of layers.

**The Dying ReLU Problem:** If a neuron's weights shift such that its input is always negative, it outputs 0 forever and its gradient is 0 — it can never recover. The neuron is "dead." This happens to 10-40% of ReLU neurons in typical networks.

**History:** First used in biological neuron models (1960s). Popularized for deep networks by Nair & Hinton (2010) and Glorot et al. (2011). Now the default activation for hidden layers.

**When to use:**
- Default choice for hidden layers in feed-forward and convolutional networks
- Any deep network (avoids vanishing gradients)
- When computational efficiency matters (single comparison)

**When NOT to use:**
- Output layer (use sigmoid/softmax for classification, linear for regression)
- When dying neurons are a documented problem (consider Leaky ReLU)

---

### 3. Tanh (Hyperbolic Tangent)

**Formula:**
$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

**Output range:** (-1, 1) — zero-centered.

**Intuition:** "The bipolar sigmoid." Tanh is S-shaped like sigmoid but centered at zero and ranging from -1 to 1. This means positive inputs produce positive outputs, negative inputs produce negative outputs, and the average output is near zero — which helps gradient descent converge faster (because the gradient direction is more informative).

**Derivative:**
$$\tanh'(x) = 1 - \tanh^2(x)$$

Maximum derivative is **1.0** at x=0 (four times better than sigmoid's 0.25). Still saturates for large |x|, but less severely than sigmoid.

**Relationship to sigmoid:**
$$\tanh(x) = 2\sigma(2x) - 1$$

**History:** Used in the original LSTM paper (Hochreiter & Schmidhuber, 1997) and was the default activation in early recurrent networks.

**When to use:**
- Hidden layers in shallow networks (where zero-centering helps)
- State/gate computations in LSTM/GRU cells (tanh for candidate state)
- Anywhere zero-centered output is beneficial

**When NOT to use:**
- Very deep networks (use ReLU to avoid saturation)
- Output layer for classification

---

### 4. Leaky ReLU

**Formula:**
$$\text{LeakyReLU}(x, \alpha) = \begin{cases} x & \text{if } x > 0 \\ \alpha x & \text{if } x \leq 0 \end{cases}$$

where α is a small constant, typically 0.01.

**Output range:** (-∞, +∞) — but with a kink at 0.

**Intuition:** "ReLU with a safety net." Instead of hard-zeroing negatives, Leaky ReLU lets through a small trickle (1% of the negative value). This means **no dead neurons** — even negative inputs have a non-zero gradient, so the neuron can recover during training.

**Derivative:**
$$\text{LeakyReLU}'(x, \alpha) = \begin{cases} 1 & \text{if } x > 0 \\ \alpha & \text{if } x \leq 0 \end{cases}$$

The gradient for negative inputs is α (0.01), which is small but non-zero. This keeps the learning signal alive.

**Variants:**
- **Parametric ReLU (PReLU):** α is learned per neuron during training
- **Randomized Leaky ReLU (RReLU):** α is randomly sampled during training
- **ELU:** Uses exponential for negative inputs (smoother, more expensive)

**History:** Introduced by Maas et al. (2013). He et al. (2015) proposed PReLU (learnable α).

**When to use:**
- When dying ReLU neurons are a problem
- When you want ReLU's benefits but with more safety
- In generative models (Leaky ReLU is standard in GANs)

**When NOT to use:**
- When the simple ReLU is working fine (Leaky ReLU rarely outperforms ReLU significantly)
- When you need smooth derivatives (try ELU or GELU)

---

### 5. Softmax

**Formula:**
$$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}$$

**Numerically stable version:**
$$\text{softmax}(x_i) = \frac{e^{x_i - \max(\mathbf{x})}}{\sum_{j=1}^{n} e^{x_j - \max(\mathbf{x})}}$$

**Output range:** (0, 1) for each element, and all elements sum to 1.

**Intuition:** "The chooser." Softmax takes a vector of raw scores (logits) and converts them into a probability distribution. The "soft" part means it's a smooth/differentiable version of `argmax` — instead of picking one winner, it gives every option a probability, with the highest-scoring option getting the most.

**Why subtract max?** Without it, `e^1000` = overflow → `inf`. By subtracting the max first, the largest exponent becomes `e^0 = 1`, and all others are less than 1. Mathematically identical because:

$$\frac{e^{x_i}}{\sum_j e^{x_j}} = \frac{e^{x_i - m}}{\sum_j e^{x_j - m}}$$

where $m = \max(\mathbf{x})$. The factor $e^m$ cancels in numerator and denominator.

**Derivative (Jacobian):**
$$\frac{\partial \text{softmax}(x_i)}{\partial x_j} = \text{softmax}(x_i) \cdot (\delta_{ij} - \text{softmax}(x_j))$$

where δ_{ij} is the Kronecker delta (1 if i=j, else 0). This means each output depends on all inputs — softmax is a vector function, not element-wise.

**History:** The softmax function originated in statistical mechanics (Boltzmann distribution, 1868). Introduced to neural networks by Bridle (1990) as a generalization of sigmoid for multi-class classification.

**When to use:**
- Output layer for multi-class classification
- Attention mechanism weight computation
- Anywhere you need to convert raw scores into a probability distribution

**When NOT to use:**
- Hidden layers (use ReLU or variants)
- Binary classification (use sigmoid — it's softmax for 2 classes)
- Large vocabulary models (computationally expensive: O(V) per position)

---

## When to Use Each (Decision Tree)

```
                    ┌─────────────────────┐
                    │  What layer is this? │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
        ┌──────────┐    ┌───────────┐    ┌──────────────┐
        │  Output   │    │  Hidden   │    │  Recurrent   │
        │  Layer    │    │  Layer    │    │  (LSTM/GRU)  │
        └─────┬────┘    └─────┬─────┘    └──────┬───────┘
              │               │                  │
     ┌────────┴───────┐       ▼                  ▼
     ▼                ▼   ┌────────┐      ┌──────────┐
┌─────────┐    ┌────────┐│  ReLU  │      │ Sigmoid  │
│ Sigmoid │    │Softmax││ (default│      │ (gates)  │
│(binary) │    │(multi)││ choice)│      │ Tanh     │
└─────────┘    └───────┘└────────┘      │ (states) │
                                      └──────────┘

  Hidden Layer Problems?
  ┌─────────────────────────────────────────┐
  │ Dying neurons?  →  Leaky ReLU (α=0.01) │
  │ Need smoothness? →  GELU or ELU         │
  │ Zero-centered?  →  Tanh (shallow only)  │
  │ Speed critical? →  ReLU (fastest)       │
  └─────────────────────────────────────────┘
```

### Quick Rules

| If you... | Use |
|-----------|-----|
| Are doing binary classification (output) | **Sigmoid** |
| Are doing multi-class classification (output) | **Softmax** |
| Are building a hidden layer for the first time | **ReLU** |
| Have dying ReLU neurons | **Leaky ReLU** |
| Are building an LSTM/GRU | **Sigmoid** (gates) + **Tanh** (states) |
| Are building a GAN | **Leaky ReLU** (discriminator) |
| Need a probability between 0 and 1 | **Sigmoid** |
| Need a signed score between -1 and 1 | **Tanh** |
| Need to choose from N options | **Softmax** |

---

## Line-by-Line Code Walkthrough

### Sigmoid

```rust
pub fn sigmoid(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}
```

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `pub fn sigmoid(x: f64) -> f64` | Public function taking a 64-bit float, returning a 64-bit float |
| 2 | `1.0 / (1.0 + (-x).exp())` | `(-x)` negates the input. `.exp()` computes e^(-x). Add 1, then divide 1 by the result. |

**Step-by-step for x = 2.0:**
1. `-x` = -2.0
2. `(-x).exp()` = e^(-2.0) ≈ 0.1353
3. `1.0 + 0.1353` = 1.1353
4. `1.0 / 1.1353` ≈ **0.8808**

### ReLU

```rust
pub fn relu(x: f64) -> f64 {
    x.max(0.0)
}
```

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `pub fn relu(x: f64) -> f64` | Public function, f64 → f64 |
| 2 | `x.max(0.0)` | `f64::max()` returns the larger of `x` and `0.0`. If x > 0, returns x. If x ≤ 0, returns 0. |

**Note:** `f64::max()` is implemented as a single comparison and branch — it's the fastest possible operation. Notably, `max(NaN, 0.0)` returns 0.0, handling NaN gracefully.

### Tanh

```rust
pub fn tanh(x: f64) -> f64 {
    x.tanh()
}
```

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `pub fn tanh(x: f64) -> f64` | Public function, f64 → f64 |
| 2 | `x.tanh()` | Delegates to Rust's built-in `f64::tanh()` method, which calls the platform's `libm` `tanh()` — typically highly optimized with SIMD instructions. |

**Why delegate instead of implementing?** The naive implementation `(x.exp() - (-x).exp()) / (x.exp() + (-x).exp())` would:
1. Be slower (two `exp` calls + add/sub/div)
2. Risk overflow for large |x| (e^x overflows)

The platform `tanh()` handles these cases internally.

### Leaky ReLU

```rust
pub fn leaky_relu(x: f64, alpha: f64) -> f64 {
    if x > 0.0 { x } else { alpha * x }
}
```

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `pub fn leaky_relu(x: f64, alpha: f64) -> f64` | Takes x and the negative slope α |
| 2 | `if x > 0.0 { x } else { alpha * x }` | If positive: identity (return x unchanged). If negative or zero: multiply by α (typically 0.01). |

**Note the strict `>` not `>=`:** At x = 0.0, the condition is false, so we enter the else branch and return `alpha * 0.0 = 0.0`. This is consistent — Leaky ReLU at 0 should return 0 regardless of α.

### Softmax

```rust
pub fn softmax(logits: &[f64]) -> Vec<f64> {
    let max = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let exps: Vec<f64> = logits.iter().map(|&x| (x - max).exp()).collect();
    let sum: f64 = exps.iter().sum();
    exps.iter().map(|&e| e / sum).collect()
}
```

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `pub fn softmax(logits: &[f64]) -> Vec<f64>` | Takes a slice reference, returns an owned Vec |
| 2 | `let max = ...` | **Pass 1:** Find the maximum logit. `fold` starts at -∞ and keeps the larger of each element. This is O(n). |
| 3 | `let exps: Vec<f64> = ...` | **Pass 2:** For each logit, subtract max (for numerical stability) and compute exp. Collect into a Vec. This is O(n) and allocates. |
| 4 | `let sum: f64 = ...` | Sum all exponentials. O(n). |
| 5 | `exps.iter().map(\|&e\| e / sum).collect()` | **Pass 3:** Divide each exp by the sum to normalize. O(n). Allocates the result Vec. |

**For `[1.0, 2.0, 3.0]`:**
1. max = 3.0
2. exps = [e^(1-3), e^(2-3), e^(3-3)] = [e^(-2), e^(-1), e^(0)] = [0.1353, 0.3679, 1.0]
3. sum = 1.5032
4. result = [0.1353/1.5032, 0.3679/1.5032, 1.0/1.5032] = **[0.09, 0.2447, 0.6652]**

---

## Numerical Examples

### Sigmoid Values

| x | σ(x) | Interpretation |
|---|------|---------------|
| -10 | 0.0000454 | Almost certainly "no" |
| -5 | 0.00669 | Strongly "no" |
| -2 | 0.11920 | Leaning "no" |
| -1 | 0.26894 | Weakly "no" |
| 0 | 0.50000 | 50/50 |
| 1 | 0.73106 | Weakly "yes" |
| 2 | 0.88080 | Leaning "yes" |
| 5 | 0.99331 | Strongly "yes" |
| 10 | 0.99995 | Almost certainly "yes" |

### ReLU Values

| x | ReLU(x) | Interpretation |
|---|---------|---------------|
| -100 | 0 | Signal killed |
| -0.001 | 0 | Signal killed |
| 0 | 0 | Boundary |
| 0.001 | 0.001 | Signal passes |
| 100 | 100 | Signal passes fully |

### Tanh Values

| x | tanh(x) | Interpretation |
|---|---------|---------------|
| -5 | -0.99991 | Strongly negative |
| -2 | -0.96403 | Negative |
| -1 | -0.76159 | Moderately negative |
| 0 | 0.0 | Neutral |
| 1 | 0.76159 | Moderately positive |
| 2 | 0.96403 | Positive |
| 5 | 0.99991 | Strongly positive |

### Leaky ReLU Values (α = 0.01)

| x | Output | Note |
|---|--------|------|
| -100 | -1.0 | Would be 0 with ReLU |
| -10 | -0.1 | Small leak |
| -1 | -0.01 | Tiny leak |
| 0 | 0.0 | Boundary |
| 1 | 1.0 | Pass through |
| 10 | 10.0 | Pass through |

### Softmax Values

**Input: [1.0, 2.0, 3.0]**

| Index | Logit | Exp(x-max) | Probability |
|-------|-------|-----------|-------------|
| 0 | 1.0 | 0.1353 | 0.0900 (9%) |
| 1 | 2.0 | 0.3679 | 0.2447 (24.5%) |
| 2 | 3.0 | 1.0000 | 0.6652 (66.5%) |

**Sum of probabilities: 1.000** ✅

**Temperature effect on softmax([1, 2, 3]):**

| Temperature | Probabilities | Behavior |
|-------------|--------------|----------|
| 0.1 | [0.0000, 0.0001, 0.9999] | Nearly argmax (deterministic) |
| 0.5 | [0.0066, 0.0473, 0.9461] | Strongly favors highest |
| 1.0 | [0.0900, 0.2447, 0.6652] | Standard |
| 2.0 | [0.1863, 0.2812, 0.5325] | More uniform |
| 10.0 | [0.3009, 0.3322, 0.3669] | Nearly uniform |

---

## Common Pitfalls

### 1. Using Sigmoid in Hidden Layers

**Problem:** Sigmoid's maximum gradient is 0.25. After 5 layers, gradients are reduced by 0.25⁵ = 0.1%. The network can't learn.

**Fix:** Use ReLU in hidden layers. Reserve sigmoid for output layers and LSTM gates.

### 2. Not Subtracting Max in Softmax

**Problem:** `softmax([1000, 1001, 1002])` without max-subtraction overflows:
```
e^1000 = inf
inf / (inf + inf + inf) = NaN
```

**Fix:** Always subtract max. The library does this correctly:
```rust
let max = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
// ... (x - max).exp()
```

### 3. Ignoring the Dying ReLU Problem

**Problem:** If a neuron's input is consistently negative (due to bad weight initialization or high learning rate), it outputs 0 forever — gradient is 0, it never updates.

**Diagnosis:** Track the fraction of neurons outputting 0. If >50% are dead, switch to Leaky ReLU.

**Fix:** Use Leaky ReLU, or ensure proper weight initialization (He initialization for ReLU: `std = sqrt(2/fan_in)`).

### 4. Using Softmax for Binary Classification

**Problem:** Softmax over 2 classes is mathematically equivalent to sigmoid, but wastes computation (exp, normalization over 2 elements instead of 1).

**Fix:** Use sigmoid for binary classification. It's the special case of softmax where n=2.

### 5. Confusing Leaky ReLU's Slope Direction

**Problem:** The `alpha` parameter is the slope for **negative** inputs, not positive. Setting `alpha = 2.0` doesn't make positive signals 2× — it makes negative signals leak at 2× their value.

**Fix:** Always remember: positive inputs pass through unchanged (slope = 1.0). Alpha only affects the negative region.

### 6. Expecting ReLU to be Smooth

**Problem:** ReLU has a sharp corner at x=0. Its derivative jumps from 0 to 1 instantaneously. This non-smoothness can cause issues in some optimization landscapes.

**Fix:** If smoothness matters, use GELU (smooth approximation of ReLU) or Softplus (`ln(1 + e^x)`).

### 7. Forgetting Softmax Returns a Distribution

**Problem:** Using individual softmax outputs as independent probabilities. They're not independent — increasing one necessarily decreases others.

**Fix:** Remember softmax outputs sum to 1. They represent a mutually exclusive probability distribution.

---

## API Reference

| Function | Signature | Output Range | Allocates? | Notes |
|----------|-----------|-------------|------------|-------|
| `sigmoid` | `fn(f64) → f64` | (0, 1) | No | Logistic function |
| `relu` | `fn(f64) → f64` | [0, ∞) | No | Single comparison |
| `tanh` | `fn(f64) → f64` | (-1, 1) | No | Delegates to libm |
| `leaky_relu` | `fn(f64, f64) → f64` | (-∞α, ∞) | No | Alpha = negative slope |
| `softmax` | `fn(&[f64]) → Vec<f64>` | (0, 1), Σ=1 | Yes (2×) | Numerically stable |

**Crate characteristics:**
- Zero dependencies
- No `unsafe` code
- No `std::feature` requirements beyond default
- Compatible with Rust edition 2021+
- License: MIT OR Apache-2.0

---

## References

1. Cybenko, G. (1989). "Approximation by Superpositions of a Sigmoidal Function." *Mathematics of Control, Signals, and Systems*, 2(4), 303–314.
2. Nair, V. & Hinton, G. (2010). "Rectified Linear Units Improve Restricted Boltzmann Machines." *ICML*.
3. Glorot, X. & Bengio, Y. (2010). "Understanding the Difficulty of Training Deep Feedforward Neural Networks." *AISTATS*.
4. He, K. et al. (2015). "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification." *ICCV*.
5. Maas, A. et al. (2013). "Rectifier Nonlinearities Improve Neural Network Acoustic Models." *ICML*.
6. Goodfellow, I., Bengio, Y., Courville, A. (2016). *Deep Learning*. MIT Press. Chapter 6.
7. Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)." *arXiv:1606.08415*.
8. Shazeer, N. (2020). "GLU Variants Improve Transformer." *arXiv:2002.05202*.

---

*Part of the [SuperInstance](https://github.com/SuperInstance) framework · MIT/Apache-2.0*
