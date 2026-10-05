# Contributing Guide

## Submission Workflow

1. Fork this repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feat/<your-name>/exercise-4.X`
4. Copy the exercise starter:
   - For 4.1: Copy `exercises/4.1-platform-exploration/TEMPLATE.md` → `submissions/<username>/4.1/ARCHITECTURE_ANALYSIS.md`
   - For 4.2–4.4: Copy the exercise folder → `submissions/<username>/4.X/`
   - For 4.5: Start fresh in `submissions/<username>/4.5/`
5. Complete the exercise
6. Run: `python scripts/verify.py --exercise 4.X --user <your-username>`
7. Commit, push, open Pull Request

## Branch Convention

```
feat/<your-name>/exercise-4.1
feat/<your-name>/exercise-4.2
...
```

## Submission Directory

```
submissions/
└── alice/
    ├── 4.1/
    │   └── ARCHITECTURE_ANALYSIS.md
    ├── 4.2/
    │   ├── rules_engine/
    │   │   ├── engine.py
    │   │   └── loader.py
    │   └── tests/
    │       └── test_engine.py
    ├── 4.3/ ...
    ├── 4.4/ ...
    └── 4.5/ ...
```

## Code Standards

- PEP 8 (max 120 chars)
- Type hints on all public function signatures
- Docstrings on all public methods
- `logging` not `print()`
- No credentials in source code

## Getting Help

- Re-read the exercise doc in `docs/`
- Check `docs/GLOSSARY.md` for term definitions
- Ask your mentor by commenting `@mention` in your PR
- Do NOT share code with other interns

## Questions?

Open a GitHub Issue with the label `question`.
