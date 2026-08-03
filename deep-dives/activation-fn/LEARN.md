# LEARN: Activation Functions — Deep Teaching

> A self-contained course on neural network activation functions: the math, the history, the neuroscience, and why SwiGLU runs modern AI.

---

## Table of Contents

1. [Foundations: Why Non-Linearity Matters](#1-foundations-why-non-linearity-matters)
2. [The Math (with Derivations)](#2-the-math-with-derivations)
3. [History: Who Invented Each and Why](#3-history-who-invented-each-and-why)
4. [Connections to Neuroscience](#4-connections-to-neuroscience)
5. [Why SwiGLU Matters for Transformers](#5-why-swiglu-matters-for-transformers)
6. [Exercises with Solutions](#6-exercises-with-solutions)
7. [Further Reading](#7-further-reading)

---

## 1. Foundations: Why Non-Linearity Matters

### The Universal Approximation Theorem

**Theorem (Cybenko, 1989; Hornik, 1991):** A feed-forward network with a single hidden layer containing a finite number of neurons, using any non-constant bounded continuous activation function, can approximate any continuous function on a compact subset of ℝⁿ to arbitrary precision.

**What this means:** Give a neural network enough neurons and any non-linear activation, and it can learn any input-output mapping. Without non-linearity, no amount of neurons or layers can approximate anything beyond a linear function.

**Proof sketch (intuitive):**
A sigmoid neuron outputs a "step" — 0 for very negative inputs, 1 for very positive inputs, with a smooth transition. By shifting the transition point (adjusting weights and bias) and combining many such steps, you can build a staircase that approximates any function. This is the same principle as Riemann sums in integral calculus — enough rectangles approximate any curve.

**The catch:** "Enough neurons" might be exponentially many for some functions. Depth (more layers) allows exponentially more efficient representation — a deep network can represent functions that would require exponentially more neurons in a shallow network.

### Why Multiple Layers?

Consider the parity function (output 1 if odd number of 1s in input). A shallow network needs O(2ⁿ) neurons for n inputs. A deep network can do it with O(n) neurons per layer across O(log n) layers.

**Key insight:** Depth + non-linearity = exponential expressivity. Without non-linearity, depth is useless (layers collapse to one linear transform).

---

## 2. The Math (with Derivations)

### 2.1 Sigmoid (Logistic Function)

**Definition:**
$$\sigma(x) = \frac{1}{1 + e^{-x}} = \frac{e^x}{e^x + 1}$$

**Derivative derivation:**

Starting from σ(x) = (1 + e^{-x})^{-1}:

$$\sigma'(x) = -(1 + e^{-x})^{-2} \cdot (-e^{-x}) = \frac{e^{-x}}{(1 + e^{-x})^2}$$

Now express this in terms of σ(x):

$$\sigma'(x) = \frac{e^{-x}}{(1 + e^{-x})^2} = \frac{1}{1 + e^{-x}} \cdot \frac{e^{-x}}{1 + e^{-x}}$$

Note that $\frac{e^{-x}}{1 + e^{-x}} = 1 - \frac{1}{1 + e^{-x}} = 1 - \sigma(x)$:

$$\boxed{\sigma'(x) = \sigma(x)(1 - \sigma(x))}$$

**Maximum gradient:** At x=0, σ(0) = 0.5, so σ'(0) = 0.5 × 0.5 = **0.25**. This is the steepest the sigmoid ever gets.

**Limits:**
- As x → +∞: σ(x) → 1, σ'(x) → 0 (saturation)
- As x → -∞: σ(x) → 0, σ'(x) → 0 (saturation)

**Second derivative:**
$$\sigma''(x) = \sigma(x)(1 - \sigma(x))(1 - 2\sigma(x))$$

Inflection point at σ(x) = 0.5, i.e., x = 0.

### 2.2 ReLU (Rectified Linear Unit)

**Definition:**
$$\text{ReLU}(x) = \max(0, x) = \begin{cases} x & x > 0 \\ 0 & x \leq 0 \end{cases}$$

**Derivative:**
$$\text{ReLU}'(x) = \begin{cases} 1 & x > 0 \\ 0 & x < 0 \end{cases}$$

At x = 0, the derivative is **undefined** (the function has a corner). In practice, we use:
- ReLU'(0) = 0 (left convention)
- ReLU'(0) = 1 (right convention)
- ReLU'(0) = random {0, 1} (subgradient sampling)

The implementation uses the left convention (x > 0, not x ≥ 0).

**Integral (Softplus):**
$$\int_0^x \text{ReLU}(t) \, dt = \begin{cases} \frac{x^2}{2} & x > 0 \\ 0 & x \leq 0 \end{cases}$$

The smooth approximation to ReLU is Softplus: $\text{Softplus}(x) = \ln(1 + e^x)$, whose derivative is σ(x).

### 2.3 Hyperbolic Tangent

**Definition:**
$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} = \frac{\sinh(x)}{\cosh(x)}$$

**Derivative derivation:**

Using the quotient rule on tanh(x) = sinh(x)/cosh(x):

$$\tanh'(x) = \frac{\cosh^2(x) - \sinh^2(x)}{\cosh^2(x)} = \frac{1}{\cosh^2(x)} = \text{sech}^2(x)$$

Using the identity $\cosh^2(x) - \sinh^2(x) = 1$ and $\tanh^2(x) + \text{sech}^2(x) = 1$:

$$\boxed{\tanh'(x) = 1 - \tanh^2(x)}$$

**Maximum gradient:** tanh'(0) = 1 - 0² = **1.0** — four times sigmoid's maximum.

**Relationship to sigmoid:**
$$\tanh(x) = 2\sigma(2x) - 1$$

Proof:
$$2\sigma(2x) - 1 = \frac{2}{1 + e^{-2x}} - 1 = \frac{2 - 1 - e^{-2x}}{1 + e^{-2x}} = \frac{1 - e^{-2x}}{1 + e^{-2x}}$$

Multiply numerator and denominator by $e^x$:

$$= \frac{e^x - e^{-x}}{e^x + e^{-x}} = \tanh(x) \quad \checkmark$$

### 2.4 Leaky ReLU

**Definition:**
$$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}$$

**Derivative:**
$$f'(x) = \begin{cases} 1 & x > 0 \\ \alpha & x < 0 \end{cases}$$

At x = 0, subgradient: any value in [α, 1] is a valid subgradient.

**Key property:** The gradient is always ≥ α > 0 (for positive α). This means **the neuron never fully dies** — there's always some learning signal flowing backward.

**Expected value of the gradient:** If x ~ N(0, 1) (standard normal), then P(x > 0) = 0.5, so:
$$E[f'(x)] = 0.5 \cdot 1 + 0.5 \cdot \alpha = \frac{1 + \alpha}{2}$$

For α = 0.01: E[f'(x)] = 0.505 — almost identical to the gradient flow of ReLU.

### 2.5 Softmax

**Definition:**
$$\text{softmax}(\mathbf{x})_i = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}$$

**Stable version:** Subtract max before exponentiating:
$$\text{softmax}(\mathbf{x})_i = \frac{e^{x_i - m}}{\sum_{j=1}^{n} e^{x_j - m}}, \quad m = \max(\mathbf{x})$$

**Proof of equivalence:**
$$\frac{e^{x_i - m}}{\sum_j e^{x_j - m}} = \frac{e^{x_i} \cdot e^{-m}}{\sum_j e^{x_j} \cdot e^{-m}} = \frac{e^{x_i}}{\sum_j e^{x_j}} \quad \checkmark$$

**Jacobian derivation:**

Let $s_i = \text{softmax}(\mathbf{x})_i$. For the partial derivative $\frac{\partial s_i}{\partial x_j}$:

**Case 1: i = j**
$$\frac{\partial s_i}{\partial x_i} = \frac{e^{x_i} \cdot \sum_j e^{x_j} - e^{x_i} \cdot e^{x_i}}{(\sum_j e^{x_j})^2} = \frac{e^{x_i}}{\sum_j e^{x_j}} - \frac{e^{2x_i}}{(\sum_j e^{x_j})^2} = s_i - s_i^2 = s_i(1 - s_i)$$

**Case 2: i ≠ j**
$$\frac{\partial s_i}{\partial x_j} = \frac{0 \cdot \sum - e^{x_i} \cdot e^{x_j}}{(\sum)^2} = -\frac{e^{x_i}}{\sum} \cdot \frac{e^{x_j}}{\sum} = -s_i \cdot s_j$$

**Combined (using Kronecker delta δ_{ij}):**
$$\boxed{\frac{\partial s_i}{\partial x_j} = s_i(\delta_{ij} - s_j)}$$

**Cross-entropy gradient:** When softmax is paired with cross-entropy loss L:

$$L = -\sum_i y_i \log(s_i)$$

$$\frac{\partial L}{\partial x_j} = \sum_i \frac{\partial L}{\partial s_i} \cdot \frac{\partial s_i}{\partial x_j} = s_j - y_j$$

This beautifully simple gradient is why softmax + cross-entropy is the standard pair for classification.

---

## 3. History: Who Invented Each and Why

### 3.1 Sigmoid (1838 / 1943 / 1958)

**Pierre François Verhulst (1838):** A Belgian mathematician who proposed the logistic function as a model of population growth. Populations don't grow exponentially forever — they saturate at a carrying capacity. The logistic function captures this S-curve. Verhulst called it the "logistique" (from the French for "lodging" — the logarithm of the quotient).

**Warren McCulloch & Walter Pitts (1943):** First to use a step-function approximation of sigmoid as a model of biological neuron firing. Their MCP neuron is the ancestor of all artificial neural networks.

**Frank Rosenblatt (1958):** The Perceptron used a threshold activation (binary step). Sigmoid was adopted later as a differentiable approximation of this step function, enabling gradient-based learning.

**Why sigmoid won (temporarily):** It's smooth, differentiable, outputs a natural probability, and its derivative has the elegant σ(1-σ) form. Before ReLU, it was the default.

### 3.2 ReLU (1969 / 2010 / 2011)

**Early biological models (1960s-1970s):** ReLU-like threshold functions were used in early computational neuroscience to model the firing rate of biological neurons (below threshold → no firing, above threshold → linear increase).

**Nair & Hinton (2010):** Introduced ReLU to deep learning in "Rectified Linear Units Improve Restricted Boltzmann Machines." They showed that ReLU dramatically improved training of deep belief networks compared to sigmoid/tanh.

**Glorot, Bordes & Bengio (2011):** "Deep Sparse Rectifier Neural Networks" demonstrated that ReLU enabled training networks without pre-training, and showed biological plausibility (half-rectification matches the behavior of real neurons).

**Krizhevsky et al. (2012, AlexNet):** ReLU was a key ingredient in AlexNet's ImageNet victory, training networks 6× faster than tanh.

**Why ReLU won:** (1) No vanishing gradient for positive inputs, (2) computational simplicity (one comparison), (3) biological plausibility, (4) induces sparse representations.

### 3.3 Tanh (1991 / 1997)

**Historical math:** The hyperbolic tangent was defined by Vincenzo Riccati in 1757. It's a fundamental function in mathematics with connections to special relativity (rapidity), electrical engineering (transmission lines), and differential equations.

**Siegelmann & Sontag (1991):** Proved that recurrent neural networks with sigmoid activations are Turing complete. Tanh was used as a bounded, zero-centered alternative.

**Hochreiter & Schmidhuber (1997, LSTM):** The LSTM architecture used tanh for the cell state candidate and sigmoid for the gates. This combination became standard for 20 years of recurrent network research.

**Why tanh mattered:** Zero-centered outputs (-1 to 1) produce better gradient flow than sigmoid's (0, 1) because the mean activation is near zero, preventing bias shifts during training.

### 3.4 Leaky ReLU (2013)

**Andrew Maas, Awni Hannun, Andrew Ng (2013):** "Rectifier Nonlinearities Improve Neural Network Acoustic Models." Introduced Leaky ReLU at a Stanford/Google workshop. The motivation was biological: real neurons have a small baseline firing rate even when not stimulated, rather than being completely silent.

**Why α = 0.01?** The value was chosen empirically. It's small enough to maintain ReLU's benefits (sparse activation, strong positive gradients) but large enough to keep neurons alive. Later work (He et al., 2015) showed that learning α per neuron (PReLU) can slightly improve performance.

**Why it's not the default:** Despite solving the dying neuron problem, Leaky ReLU rarely outperforms standard ReLU in practice. The dying neuron problem, while real, is usually not the bottleneck for performance.

### 3.5 Softmax (1868 / 1959 / 1990)

**Ludwig Boltzmann (1868):** The Boltzmann distribution in statistical mechanics assigns probabilities to states proportional to e^{-E/kT}, where E is energy and T is temperature. Softmax is the machine learning analogue: logits = -E/kT.

**John Bridle (1990):** "Probabilistic Interpretation of Feedforward Classification Network Outputs" — introduced softmax as the standard output layer for multi-class classification. He called it the "softmax activation function" as a differentiable approximation of the argmax operation.

**Why softmax won:** (1) It's the maximum entropy distribution consistent with given class constraints, (2) paired with cross-entropy, it produces the clean s_i - y_i gradient, (3) it naturally extends logistic regression to multiple classes.

---

## 4. Connections to Neuroscience

### 4.1 Biological Neurons and ReLU

A biological neuron receives input through dendrites (synaptic connections). Each synapse has a weight (synaptic strength). The neuron sums these weighted inputs. If the total exceeds a **threshold**, the neuron fires an action potential.

**The firing rate** of a biological neuron is approximately linear above the threshold and zero below it:

```
Firing rate
    │
    │        /
    │       /
    │      /
    │_____/
    │
    └────── threshold ── input current
```

This is **exactly ReLU** (with a bias term to shift the threshold). ReLU is the most biologically plausible activation function.

### 4.2 Sigmoid and the Nernst Equation

The sigmoid function appears in the **Nernst equation**, which describes how the membrane potential of a neuron depends on ion concentrations:

$$E_{ion} = \frac{RT}{zF} \ln\frac{[\text{ion}]_{\text{out}}}{[\text{ion}]_{\text{in}}}$$

The probability of an ion channel being open often follows a sigmoid-like curve (Boltzmann sigmoid), where voltage-gated channels transition from closed to open with increasing voltage.

### 4.3 Lateral Inhibition and Softmax

In the retina, **lateral inhibition** causes active neurons to suppress their neighbors — exactly what softmax does. When one output is large, it suppresses all others through the normalization denominator. This is called **winner-take-all** behavior, and it's fundamental to how biological sensory systems create sparse, selective representations.

### 4.4 Neuromodulation and Leaky ReLU

The brain doesn't use a fixed activation function. **Neuromodulators** (dopamine, serotonin, acetylcholine) change the gain of neural responses:

- **High dopamine/attention:** Neurons are more selective (sharper activation, more like ReLU)
- **Low arousal:** Neurons are more leaky (more neurons fire weakly, like Leaky ReLU with high α)

This maps to the idea of **temperature** in softmax and **alpha** in Leaky ReLU — the brain dynamically adjusts its activation function based on cognitive state.

### 4.5 The 294:1 Avoidance Ratio

The SuperInstance framework documents a **294:1 avoidance-to-choose ratio** in the γ + η = C conservation model. This has a neuroscientific analogue:

The brain's **basolateral amygdala** has been shown to have roughly 10:1 ratio of inhibitory to excitatory connections for threat detection. The amygdala is designed to detect threats (avoidance) far more than opportunities (approach), because in evolution, missing a threat is fatal while missing an opportunity is merely costly.

ReLU's design mirrors this: negative signals (threats/incompatibilities) are completely suppressed (zero output), while positive signals (opportunities/compatible options) pass through. The asymmetry is a feature, not a bug.

---

## 5. Why SwiGLU Matters for Transformers

### 5.1 The Evolution of Transformer Activations

```
2017  ────  ReLU     (original Transformer, "Attention Is All You Need")
2018  ────  GELU     (BERT, GPT-2)
2019  ────  GELU     (GPT-2 full, RoBERTa, T5)
2020  ────  SwiGLU   (PaLM, LLaMA, Mistral — current SOTA)
```

### 5.2 What Is GELU?

**Gaussian Error Linear Unit (GELU):**
$$\text{GELU}(x) = x \cdot \Phi(x)$$

where Φ(x) is the cumulative distribution function of the standard normal distribution.

**Intuition:** GELU multiplies the input by the probability that a Gaussian random variable is less than x. For large positive x, Φ(x) → 1, so GELU(x) → x (like ReLU). For large negative x, Φ(x) → 0, so GELU(x) → 0 (like ReLU). But near x = 0, GELU is **smooth** — no sharp corner.

**Comparison to ReLU:**
- ReLU: hard gate (0 or 1 multiplier)
- GELU: soft probabilistic gate (0.0 to 1.0 multiplier, smooth)
- GELU is smoother → better optimization landscape → faster convergence

**Approximation:**
$$\text{GELU}(x) ≈ 0.5x\left(1 + \tanh\left[\sqrt{2/\pi}\left(x + 0.044715x^3\right)\right]\right)$$

### 5.3 What Is GLU (Gated Linear Unit)?

**Gated Linear Unit (Dauphin et al., 2017):**
$$\text{GLU}(x, \text{gate}) = (xW + b) \otimes \sigma(xV + c)$$

where σ is sigmoid and ⊗ is element-wise multiplication.

**Intuition:** The input is split into two paths — one path carries information, the other path acts as a **gate** (via sigmoid) that decides how much information to let through. It's an attention mechanism baked into the activation function.

### 5.4 SwiGLU = Swish + GLU

**SwiGLU (Shazeer, 2020):** Replace the sigmoid gate in GLU with the **SiLU** (Swish) activation:

$$\text{SiLU}(x) = x \cdot \sigma(x) \quad \text{(also called Swish)}$$

$$\text{SwiGLU}(x, \text{gate}) = \text{SiLU}(xW + b) \otimes (xV + c)$$

**Why it works:**

1. **Gating mechanism:** The gate path provides dynamic routing — different inputs activate different dimensions, enabling richer computation than a fixed activation function.

2. **SiLU > ReLU as a gate:** SiLU has a small negative dip for moderately negative inputs, which acts as a "soft inhibition" — slightly suppressing information that's weakly negative, rather than hard-zeroing it. This provides a richer gradient signal.

3. **Empirical results:** Shazeer (2020) showed SwiGLU improves transformer quality by 0.5-1.0 BLEU/factor points over GELU on machine translation, with the same parameter count.

4. **Why LLaMA uses it:** Meta's LLaMA (2023) adopted SwiGLU because it gives better performance-per-FLOP than GELU, especially at scale. The gating mechanism becomes more powerful as model size increases.

### 5.5 Why This Matters Beyond Transformers

The GLU pattern — **split the signal into a data path and a gate path** — is a general principle for dynamic computation:

- **Transformers:** SwiGLU in feed-forward layers
- **CNNs:** Gated convolutions (GLU-style) for image generation
- **Recurrent networks:** LSTM/GRU gates are a form of GLU
- **Mixture of Experts:** The gating network in MoE is essentially a GLU

This suggests that the future of activation functions isn't a fixed mathematical formula, but a **learned gating mechanism** that adapts based on context.

---

## 6. Exercises with Solutions

### Exercise 1: Derive the Softmax-CrossEntropy Gradient

**Problem:** Given softmax output $s_i$ and one-hot target $y_i$, with cross-entropy loss $L = -\sum_i y_i \log s_i$, show that $\frac{\partial L}{\partial x_j} = s_j - y_j$.

**Solution:**

Using the chain rule:
$$\frac{\partial L}{\partial x_j} = \sum_i \frac{\partial L}{\partial s_i} \cdot \frac{\partial s_i}{\partial x_j}$$

**Step 1:** Compute $\frac{\partial L}{\partial s_i}$:
$$\frac{\partial L}{\partial s_i} = -\frac{y_i}{s_i}$$

**Step 2:** Use the Jacobian from §2.5: $\frac{\partial s_i}{\partial x_j} = s_i(\delta_{ij} - s_j)$

**Step 3:** Substitute:
$$\frac{\partial L}{\partial x_j} = \sum_i \left(-\frac{y_i}{s_i}\right) \cdot s_i(\delta_{ij} - s_j) = -\sum_i y_i(\delta_{ij} - s_j)$$

**Step 4:** Expand the sum:
$$= -\sum_i y_i \delta_{ij} + \sum_i y_i s_j = -y_j + s_j \sum_i y_i$$

**Step 5:** Since y is one-hot, $\sum_i y_i = 1$:
$$\boxed{\frac{\partial L}{\partial x_j} = s_j - y_j}$$

This is the prediction error — when the prediction s_j matches the target y_j, the gradient is zero.

---

### Exercise 2: Dead Neuron Analysis

**Problem:** In a network using ReLU, a neuron has weights such that its pre-activation z = w·x + b is always negative for all training examples. What happens to its weights during gradient descent? Prove that it can never recover.

**Solution:**

**Forward pass:** Since z < 0 always, ReLU(z) = 0 always.

**Backward pass:** The gradient of the loss with respect to z is:
$$\frac{\partial L}{\partial z} = \frac{\partial L}{\partial h} \cdot \text{ReLU}'(z)$$

Since ReLU'(z) = 0 for z ≤ 0:
$$\frac{\partial L}{\partial z} = \frac{\partial L}{\partial h} \cdot 0 = 0$$

**Weight gradient:** 
$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot x = 0 \cdot x = 0$$

Since all weight gradients are zero, gradient descent never updates the weights. The neuron remains frozen at z < 0 forever. ∎

**This is why Leaky ReLU exists:** With Leaky ReLU, ReLU'(z) = α > 0, so $\frac{\partial L}{\partial z} = \frac{\partial L}{\partial h} \cdot \alpha \neq 0$, and the weights can update.

---

### Exercise 3: Temperature Scaling

**Problem:** Show that softmax with temperature T converges to argmax as T → 0 and to uniform as T → ∞.

**Solution:**

**As T → 0:**

$$\text{softmax}(x/T)_i = \frac{e^{x_i/T}}{\sum_j e^{x_j/T}}$$

Let $m = \max(\mathbf{x})$, and let the max be achieved at index k. Then:

$$\frac{e^{x_i/T}}{e^{x_k/T}} = e^{(x_i - x_k)/T}$$

As T → 0⁺ and $x_i < x_k$: $(x_i - x_k)/T → -\infty$, so $e^{(x_i - x_k)/T} → 0$.

Therefore $\text{softmax}(x/T)_i → 0$ for $i \neq k$ and $→ 1$ for $i = k$ — this is argmax. ✓

**As T → ∞:**

$(x_i - x_k)/T → 0$ for all i, so $e^{(x_i - x_k)/T} → 1$.

Therefore $\text{softmax}(x/T)_i → 1/n$ for all i — this is uniform. ✓

---

### Exercise 4: Prove tanh Saturates Slower than Sigmoid

**Problem:** Show that tanh's gradient at saturation (large |x|) decays as $4e^{-2|x|}$ while sigmoid's decays as $e^{-|x|}$, making tanh more resistant to vanishing gradients.

**Solution:**

**Sigmoid gradient at large positive x:**
$$\sigma'(x) = \sigma(x)(1 - \sigma(x)) ≈ 1 \cdot e^{-x} = e^{-x}$$

since $\sigma(x) ≈ 1 - e^{-x}$ for large x, so $1 - \sigma(x) ≈ e^{-x}$.

**Tanh gradient at large positive x:**
$$\tanh'(x) = 1 - \tanh^2(x)$$

For large x, $\tanh(x) ≈ 1 - 2e^{-2x}$ (from the Taylor expansion of tanh at infinity):

$$\tanh'(x) ≈ 1 - (1 - 2e^{-2x})^2 ≈ 1 - (1 - 4e^{-2x}) = 4e^{-2x}$$

**Comparison at x = 5:**
- Sigmoid: $e^{-5} ≈ 0.0067$
- Tanh: $4e^{-10} ≈ 0.0002$

Wait — this shows tanh decays **faster**! The resolution is that tanh starts from a higher base (1.0 vs 0.25 at x=0), so it has more gradient to work with in the critical region around 0. For x ∈ [-3, 3], tanh's gradient is consistently 2-4× larger than sigmoid's.

The key advantage of tanh isn't slower saturation — it's **zero-centered output**, which prevents the zig-zag gradient descent problem.

---

### Exercise 5: GELU Approaches ReLU

**Problem:** Show that GELU(x) → ReLU(x) as x → ±∞.

**Solution:**

GELU(x) = x · Φ(x), where Φ is the standard normal CDF.

**As x → +∞:** Φ(x) → 1, so GELU(x) → x · 1 = x = ReLU(x). ✓

**As x → -∞:** Φ(x) → 0. Specifically, Φ(x) ≈ φ(x)/|x| for large negative x (Mills ratio), where φ(x) = (2π)^{-1/2} e^{-x²/2} is the normal PDF.

GELU(x) = x · Φ(x) ≈ x · \frac{φ(x)}{|x|} = x · \frac{e^{-x²/2}}{|x|\sqrt{2π}}

As x → -∞: $e^{-x²/2}$ decays much faster than any polynomial, so GELU(x) → 0 = ReLU(x). ✓

---

### Exercise 6: Implement in Rust

**Problem:** Implement the derivative of each activation function in Rust.

**Solution:**

```rust
/// Derivative of sigmoid: σ'(x) = σ(x)(1 - σ(x))
pub fn sigmoid_deriv(x: f64) -> f64 {
    let s = sigmoid(x);
    s * (1.0 - s)
}

/// Derivative of ReLU: 1 if x > 0, else 0
pub fn relu_deriv(x: f64) -> f64 {
    if x > 0.0 { 1.0 } else { 0.0 }
}

/// Derivative of tanh: 1 - tanh²(x)
pub fn tanh_deriv(x: f64) -> f64 {
    let t = x.tanh();
    1.0 - t * t
}

/// Derivative of Leaky ReLU: 1 if x > 0, else alpha
pub fn leaky_relu_deriv(x: f64, alpha: f64) -> f64 {
    if x > 0.0 { 1.0 } else { alpha }
}

/// Jacobian of softmax: J[i][j] = s_i * (δ_ij - s_j)
/// Returns the full n×n Jacobian matrix.
pub fn softmax_jacobian(logits: &[f64]) -> Vec<Vec<f64>> {
    let s = softmax(logits);
    let n = s.len();
    (0..n).map(|i| {
        (0..n).map(|j| {
            if i == j {
                s[i] * (1.0 - s[j])
            } else {
                -s[i] * s[j]
            }
        }).collect()
    }).collect()
}
```

---

## 7. Further Reading

### Foundational Papers

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| Verhulst, "Notice sur la loi que la population suit dans son accroissement" | 1838 | Logistic function |
| Cybenko, "Approximation by Superpositions of a Sigmoidal Function" | 1989 | Universal Approximation Theorem |
| Bridle, "Probabilistic Interpretation of Feedforward Classification Outputs" | 1990 | Softmax for classification |
| Hochreiter & Schmidhuber, "LSTM" | 1997 | tanh + sigmoid in recurrent gates |
| Nair & Hinton, "Rectified Linear Units Improve RBMs" | 2010 | ReLU for deep networks |
| Glorot et al., "Understanding the Difficulty of Training Deep Feedforward Networks" | 2010 | Vanishing gradient analysis |
| Maas et al., "Rectifier Nonlinearities Improve Neural Network Acoustic Models" | 2013 | Leaky ReLU |
| He et al., "Delving Deep into Rectifiers" | 2015 | PReLU, He initialization |
| Hendrycks & Gimpel, "Gaussian Error Linear Units (GELUs)" | 2016 | GELU |
| Dauphin et al., "Language Modeling with Gated Convolutional Networks" | 2017 | GLU |
| Shazeer, "GLU Variants Improve Transformer" | 2020 | SwiGLU |

### Textbooks

- Goodfellow, Bengio, Courville. *Deep Learning* (2016). Chapter 6: Deep Feedforward Networks.
- Bishop. *Pattern Recognition and Machine Learning* (2006). Chapter 5: Neural Networks.
- Nielsen. *Neural Networks and Deep Learning* (2015). Free online. Chapter 3-4.

### Online Resources

- [Visualizing activation functions](https://www.desmos.com/calculator/h8s7gpytbb) — interactive Desmos graph
- [Deep Learning Book — Chapter 6](https://www.deeplearningbook.org/contents/mlp.html) — free online
- [Distill: Attention? Attention!](https://distill.pub/2016/a-walk-through-spatial-attention/) — visual explanation of attention (which uses softmax)

---

*Part of the [SuperInstance](https://github.com/SuperInstance) framework · MIT/Apache-2.0*
