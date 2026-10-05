# Exercise 4.1 — Platform Exploration & Architecture Map

## 🎯 Objective

Explore the Swarelic codebase deeply and produce a comprehensive **Architecture Document** that demonstrates your understanding of the system. This is a research exercise — no new code needed.

**Time estimate:** 3–4 hours

---

## Why This Matters

Before writing any code in a production system, the best engineers spend time understanding the existing architecture. This exercise builds that habit. Your architecture document will also serve as a **study guide** for the rest of the track.

---

## 📋 What You Must Produce

Create `submissions/<your-username>/4.1/ARCHITECTURE_ANALYSIS.md` with the following sections:

---

### Section 1: Codebase Map (20 pts)

List and explain the purpose of every top-level directory in the Swarelic codebase. For each directory:
- What does it contain?
- What is its role in the system?
- Which other modules does it depend on?

**Minimum coverage:** At least 8 directories with meaningful explanations (not just file lists).

---

### Section 2: Call Flow Trace (25 pts)

Trace a **complete incoming call** from start to finish through the code. For each step:
- Which file/module handles this step?
- What data is passed between steps?
- What decisions are made?

Your trace should cover at minimum:
1. Incoming webhook from telephony provider
2. Voice pipeline initialization
3. First STT transcription event
4. Rules engine evaluation
5. Agent assignment
6. Call completion and data persistence

---

### Section 3: Rules Engine Deep Dive (20 pts)

Answer these questions about the Rules Engine:
1. How are rules stored? (DB model? JSON? Both?)
2. What does a rule look like in its data representation?
3. How does the engine evaluate conditions?
4. What happens when multiple rules match?
5. What types of actions can a rule trigger?
6. How would you add a new action type?

---

### Section 4: Multi-Tenancy Model (15 pts)

Explain how the platform handles multiple clients (tenants):
1. How is tenant isolation enforced in database queries?
2. Where is the tenant context stored during a request?
3. How does tenant-specific configuration work?
4. What would happen if tenant isolation was bypassed?

---

### Section 5: Improvement Opportunities (10 pts)

Identify **3 areas** where you believe the codebase could be improved. For each:
- Describe the current implementation
- Explain the problem or limitation
- Propose a concrete improvement
- Estimate the effort (S/M/L)

---

### Section 6: Questions (10 pts)

List **5 questions** you have after exploring the codebase. These should be thoughtful, specific questions that show you read the code carefully — not generic questions you could answer by re-reading the docs.

---

## ✅ Acceptance Criteria

- [ ] Document is in `submissions/<username>/4.1/ARCHITECTURE_ANALYSIS.md`
- [ ] All 6 sections are present and non-trivial
- [ ] Section 2 (Call Flow) references specific file names and line numbers
- [ ] Section 3 answers all 6 questions
- [ ] Total word count: 800+ words
- [ ] No copy-paste from the `ARCHITECTURE_OVERVIEW.md` doc — your own analysis only

---

## 💡 Tips

- Use `grep`, ripgrep, or your IDE's search to trace function calls
- Look at the test files — they often show intended usage
- Start with `urls.py` files to see what endpoints exist
- Check `signals.py` files to see cross-app side effects
- Read `celery.py` and `tasks.py` to understand background operations

---

## 📎 Template

A starter template is provided in `exercises/4.1-platform-exploration/TEMPLATE.md`. Copy it to your submissions folder and fill it in.
