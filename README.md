# 🧠 Intern Swarelic Tasks

> **Track 4 — Swarelic Platform Deep Dive**
> Understand the real codebase. Build on it. Ship something.

---

## 🎯 About This Track

This is the final and most important track. You've learned Git, Frontend, and Backend fundamentals. Now you apply them to the **actual Swarelic platform** — a production-grade AI-powered call-center platform with voice pipelines, rules engines, multi-tenant management, and real-time analytics.

**By the end of this track, you will:**
- Understand the full architecture of the Swarelic platform
- Have written production-ready code that could be merged into the main repo
- Be able to explain how calls flow from phone → AI → agent → CRM

---

## 🗺️ Exercise Overview

| Exercise | Topic | Type | Difficulty |
|----------|-------|------|------------|
| 4.1 | Platform Exploration & Architecture Map | Research + Docs | ⭐⭐ |
| 4.2 | Rules Engine Implementation | Backend Code | ⭐⭐⭐⭐ |
| 4.3 | Agent Flow Simulation | Backend + Logic | ⭐⭐⭐ |
| 4.4 | API Client for SCAI | Backend + Integration | ⭐⭐⭐ |
| 4.5 | Mini Feature Implementation | Full-stack | ⭐⭐⭐⭐⭐ |

---

## 📁 Repository Structure

```
intern-swarelic-tasks/
├── .github/
│   ├── workflows/checks.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── 00-setup.md                 # Accessing the platform
│   ├── 01-platform-exploration.md  # Exercise 4.1
│   ├── 02-rules-engine.md          # Exercise 4.2
│   ├── 03-agent-flow.md            # Exercise 4.3
│   ├── 04-api-client.md            # Exercise 4.4
│   ├── 05-mini-feature.md          # Exercise 4.5
│   ├── ARCHITECTURE_OVERVIEW.md    # Platform architecture primer
│   ├── GLOSSARY.md                 # Platform-specific terms
│   ├── GRADING.md
│   └── MENTOR_GUIDE.md
├── exercises/
│   ├── 4.1-platform-exploration/   # Research template
│   ├── 4.2-rules-engine/           # Standalone rules engine starter
│   ├── 4.3-agent-flow/             # Flow simulator starter
│   ├── 4.4-api-client/             # SCAI API client starter
│   └── 4.5-mini-feature/           # Feature stub
├── scripts/
│   └── verify.py
├── submissions/
│   └── <your-username>/
└── CONTRIBUTING.md
```

---

## 🚀 Getting Started

```bash
# 1. Clone this repo
git clone <repo-url>
cd intern-swarelic-tasks

# 2. Read the platform overview first (required!)
cat docs/ARCHITECTURE_OVERVIEW.md

# 3. Set up Python environment (for exercises 4.2–4.5)
python -m venv venv
source venv/bin/activate
pip install -r exercises/4.2-rules-engine/requirements.txt

# 4. Start with Exercise 4.1 (no code, just exploration)
cat docs/01-platform-exploration.md
```

---

## 📤 Submission Workflow

All submissions follow the same PR workflow:

1. Fork this repo
2. Branch: `feat/<your-name>/exercise-4.X`
3. Work in `submissions/<your-username>/4.X/`
4. Run: `python scripts/verify.py --exercise 4.X --user <your-username>`
5. Open a PR with the provided template

---

## ⚠️ Important Notes

- **Exercise 4.1 is research-only** — no code required, just a well-written document
- **Exercise 4.5 is intentionally open-ended** — there's no single "right" answer
- You are expected to **read actual Swarelic source code** for exercises 4.1–4.4
- Always get mentor approval before touching any production environment
