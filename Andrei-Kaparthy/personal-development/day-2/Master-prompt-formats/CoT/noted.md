# Master prompt format

# 🔍 Chain-of-Thought (CoT) in LLMs: Explained

## 🔹 What is CoT?

**Chain-of-Thought (CoT)** is a prompting technique used in LLMs where **intermediate reasoning steps** are included in the input prompt to **guide** the model towards a correct answer. Rather than asking the model for a final answer directly, we **encourage it to "think out loud"**, mimicking human reasoning.


## 🔹 Why CoT Works

* **LLMs are autoregressive** — they generate one token at a time based on prior tokens. If the prior tokens include logical steps, the next ones are more likely to follow sound reasoning.
* It **leverages latent reasoning capabilities** that may not emerge with direct prompting.
* Especially effective for **multi-step problems** (math, logic, causal reasoning, etc.).


## 🔹 Key Forms of CoT

1. **Manual CoT Prompting**
   You explicitly write intermediate steps in the prompt.
   ✅ Simple but not scalable.

2. **Few-Shot CoT Prompting**
   You provide few-shot examples where the reasoning is demonstrated.

3. **Zero-Shot CoT Prompting**
   You use trigger phrases like **"Let's think step by step"** to coax the model into reasoning.

4. **Auto-CoT (Automatic Chain-of-Thought Generation)**
   Generate CoT examples using a model and refine them for better prompting.

5. **Tree-of-Thoughts (ToT)**
   An advanced form where multiple CoT paths are explored in a search-like process.



## 🔹 CoT vs Direct Prompting

| Feature          | Direct Prompting       | CoT Prompting                           |
| ---------------- | ---------------------- | --------------------------------------- |
| Output           | Final answer only      | Reasoning steps + final answer          |
| Accuracy         | Lower on complex tasks | Significantly higher on reasoning tasks |
| Interpretability | Low                    | High – reasoning path visible           |
| Example size     | Short                  | Longer, more tokens                     |



## 🔹 Example 1: Arithmetic Reasoning

### 🟥 Direct Prompt:

> **Q:** If a train travels at 60 mph for 2.5 hours, how far does it go?
> **A:** ?

**Likely Output:**

> 150

### 🟩 CoT Prompt:

> **Q:** If a train travels at 60 mph for 2.5 hours, how far does it go?
> **A:** Let's think step by step.
> The speed is 60 miles per hour.
> The time is 2.5 hours.
> Distance = Speed × Time = 60 × 2.5 = 150 miles.
> **Answer: 150**

> ✅ Better accuracy, and interpretable.


## 🔹 Example 2: Commonsense Reasoning

### 🟥 Direct Prompt:

> **Q:** John put his shoes under the bed. Where are his shoes now?

**Output (often correct, but not always):**

> Under the bed.

### 🟩 CoT Prompt:

> **Q:** John put his shoes under the bed. Where are his shoes now?
> **A:** Let's think it through. John placed the shoes under the bed. He hasn't moved them since.
> Therefore, the shoes are still under the bed.
> **Answer: Under the bed.**

> ✅ Robust to subtle variations in input.



## 🔹 CoT in Advanced LLM Use Cases

### 1. **Math Word Problems (e.g., GSM8K, MATH)**

Prompt:

> **Q:** Mary has 3 times as many apples as Tom. Tom has 4 apples. How many does Mary have?

CoT:

> Tom has 4 apples.
> Mary has 3 times as many, so 3 × 4 = 12.
> **Answer: 12**

Accuracy with CoT on GSM8K dataset improves from \~17% to **80%+** with few-shot CoT using GPT-4.


### 2. **Program Synthesis (e.g., Code Generation)**

Prompt with CoT:

> I want a function that returns the factorial of a number.
> Let's think step-by-step.
> First, check if the number is 0 or 1 — base case.
> Else, recursively call factorial on (n - 1) and multiply.
> Then return the result.

→ Model is more likely to generate:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## 🔹 Limitations of CoT

1. **Token Efficiency**
   CoT consumes more tokens, potentially impacting context window usage.

2. **Incoherent Chains**
   Model can hallucinate or generate flawed reasoning unless supervised.

3. **Prompt Sensitivity**
   Minor changes in wording can impact performance (especially in zero-shot CoT).

4. **Task Specificity**
   Works best in reasoning-heavy tasks. Less impact on perceptual or factual tasks.


## 🔹 Related Techniques & Extensions

| Technique                      | Description                                                           |
| ------------------------------ | --------------------------------------------------------------------- |
| **Tree-of-Thought (ToT)**      | CoT + branching decisions + search; explore multiple reasoning paths. |
| **Self-Consistency**           | Sample multiple CoTs → choose majority/most coherent answer.          |
| **ReAct (Reasoning + Acting)** | CoT + tool use (search, calculator) → interactive reasoning agents.   |
| **Reflection**                 | Model critiques its own CoT and revises answer.                       |
| **Toolformer**                 | LLM uses tools (APIs, search) during CoT reasoning.                   |


## 🔹 CoT Engineering: Best Practices

1. **Start with Zero-shot CoT:**
   Use phrases like:

   * "Let's think step by step."
   * "Let's work this out carefully."

2. **Use Few-shot CoT for Complex Tasks:**
   Curate 2–5 examples with step-by-step reasoning for tasks like:

   * Logical deduction
   * Math word problems
   * Legal/contract analysis

3. **Combine with Self-Consistency:**
   Generate multiple CoTs and majority-vote the result.

4. **Prompt Optimization:**

   * Use domain-specific vocabulary
   * Use formatting (`-`, `→`, numbered steps) to structure thoughts


## 🔹 Real-world Use Cases

| Domain                | Use of CoT                                                         |
| --------------------- | ------------------------------------------------------------------ |
| **Security Analysis** | Reason through threat modeling or incident response scenarios      |
| **Finance**           | Step-by-step analysis of investment scenarios                      |
| **DevSecOps**         | Debugging pipeline logic or analyzing complex config drifts        |
| **Healthcare**        | Diagnosing based on symptoms with probabilistic reasoning          |
| **Legal Tech**        | Analyzing contractual logic with intermediate interpretation steps |

---

## 🔹 Research Papers Worth Reading

1. **"Chain of Thought Prompting Elicits Reasoning in Large Language Models"**
   *Wei et al., 2022 (Google Brain)*
   [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)

2. **"Tree of Thoughts: Deliberate Problem Solving with Language Models"**
   *Yao et al., 2023*
   [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)

3. **"ReAct: Synergizing Reasoning and Acting in Language Models"**
   *Yao et al., 2022*
   [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

4. **"Self-Consistency Improves Chain of Thought Reasoning in Language Models"**
   *Wang et al., 2022*
   [https://arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

---

## 🔚 TL;DR for Experts

> **CoT prompting** transforms LLMs from answer-generators to reasoners.
> It's foundational for reasoning-heavy tasks, compositional logic, and agentic behavior.
> Combine CoT with **self-consistency**, **search**, and **tool use** for next-level capability.
