---
title: "How I Built a GPT-Powered Threat Model Generator"
date: "YYYY-MM-DD"
tags: ["devsecops", "ai", "threatmodeling", "gpt", "python", "automation"]
---

# How I Built a GPT-Powered Threat Model Generator in 48 Hours

On Day 19 of my [60-day GenAI DevSecOps sprint](https://github.com/exampro/free-genai-bootcamp-2025/blob/main/Andrei-Kaparthy/personal-development/readme.md), I'm moving from announcing projects to detailing how they work under the hood. My [GPT Threat Modeling Bot](https://github.com/exampro/free-genai-bootcamp-2025/tree/main/Andrei-Kaparthy/personal-development/day-16/threat_Modeling_bot2) was a huge step forward, but the real story isn't just *what* it does, but *how* it does it reliably.

This post breaks down the engineering decisions—specifically, how I used **few-shot prompting** to turn a general-purpose AI into a specialized security analysis engine.

---

### The Problem: Threat Modeling is a Bottleneck

Traditional threat modeling is essential for secure architecture, but it's also:
*   **Manual and Slow:** It requires hours of meetings with senior security architects.
*   **Expert-Dependent:** It relies on the availability of a small pool of experts.
*   **Hard to Scale:** In a world of rapid, continuous deployment, it often becomes a bottleneck, done too late or not at all.

The goal was to build a tool that could provide a solid, first-pass threat model in seconds, directly within a developer's workflow.

### The "How": Engineering Prompts as Code

My first attempt was a simple **zero-shot prompt**: `"Here is an architecture, find the STRIDE threats."` The result was generic, unstructured, and frankly, not very useful. It was a toy, not a tool.

The breakthrough came when I stopped *asking* the AI and started *showing* it. This is the essence of **few-shot prompting**. I realized the prompt itself is the most critical piece of code in the entire system.

My bot's "brain" consists of two master prompts: `stride_prompt.md` and `owasp_prompt.md`. Here’s how they work.

#### Dissecting the `stride_prompt.md`

Instead of a vague question, this prompt is a carefully constructed template that teaches the AI how to behave. It contains three key parts:

1.  **The Persona:** It starts with `You are an expert security architect...` This immediately puts the model into a specific mode, priming it to use the right terminology and adopt a security-first mindset.
2.  **The Task:** A crystal-clear instruction. `Analyze the provided system architecture and generate a threat model report using the STRIDE framework.` No ambiguity.
3.  **The Example (The "Shot"):** This is the core of the technique. I wrote a high-quality, detailed example of a STRIDE analysis for a sample component. This example demonstrates:
    *   **The exact Markdown format** I want for the final report.
    *   **The tone and depth** of a real security review.
    *   **The reasoning process** for identifying a threat.
    *   **Actionable, specific mitigations.**

By providing this "shot," the LLM doesn't have to guess what a good report looks like. It learns the pattern and meticulously replicates it for the new, unseen architecture the user provides.

The `owasp_prompt.md` follows the same principle, but with an example tailored to mapping architectural components to the OWASP Top 10 web vulnerabilities.

### The Python "Glue"

The Python code for this project is surprisingly simple, and that's by design. All it does is:
1.  Read the user's `architecture.md` file.
2.  Load the `stride_prompt.md` and `owasp_prompt.md` templates.
3.  Inject the user's architecture into each prompt.
4.  Make two separate API calls to the OpenAI API—one for STRIDE, one for OWASP.
5.  Concatenate the results and save them to `THREAT_MODEL_REPORT.md`.

The real engineering work wasn't in writing complex Python logic, but in crafting the high-quality examples that serve as the AI's instruction manual.

### Conclusion: The Prompt is the Program

This project cemented a core principle of AI-Native engineering for me: **the prompt is the program.** The quality and reliability of your AI system are a direct function of the quality of the examples and instructions you provide it. By treating prompts as version-controlled, engineered assets, we can transform a creative, generalist AI into a deterministic, specialist tool that solves real-world problems.

This is how we build the future of DevSecOps—not by replacing engineers, but by scaling their expertise with AI.

---

I've documented the entire project, including the powerful few-shot prompts that serve as the bot's "brain."

🎥 **Watch the Loom Demo:** [Link to Your Loom Video]  
뜯 **Explore the Code on GitHub:** [Link to Your GitHub Repo/Project]  
🧠 **Read my Daily Learnings:** [Link to Your GitHub Notebook]

I'm building the tools for the next generation of secure development. If your team is focused on leveraging AI to solve complex security and automation challenges, I'm ready to contribute. Let's connect.

#ThreatModeling #DevSecOps #GenAI #AppSec #OWASP #STRIDE #Python #PromptEngineering #HowTo #Tutorial #OpenToWork