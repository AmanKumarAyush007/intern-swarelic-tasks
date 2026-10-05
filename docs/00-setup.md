# Setup Guide — Swarelic Track

## What You Need

Most exercises in this track (4.2–4.4) are **standalone Python projects** — they don't require Django or a database. Exercise 4.5 is the exception.

---

## Exercise 4.1: No Setup Required

Exercise 4.1 is research-only. You just need:
- Read access to the Swarelic GitHub repository (ask your mentor for access)
- A Markdown editor (VS Code is recommended)

---

## Exercises 4.2 & 4.3: Pure Python

```bash
# Navigate to the exercise
cd exercises/4.2-rules-engine   # or 4.3-agent-flow

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

**Verify your setup:**
```bash
pytest tests/ --collect-only   # Should list all test functions without errors
```

---

## Exercise 4.4: Python + requests

```bash
cd exercises/4.4-api-client

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests (all mocked — no real server needed)
pytest tests/ -v
```

The `responses` library intercepts all HTTP calls during tests, so you don't need a running SCAI server.

---

## Exercise 4.5: Full Django Setup

Exercise 4.5 needs a full Django environment:

```bash
cd exercises/4.5-mini-feature

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # (you'll create this)

python manage.py migrate
python manage.py runserver
```

If you chose Option A (Call Queue with Celery):
```bash
# Also start Redis
redis-server   # or: docker run -d -p 6379:6379 redis:alpine

# Celery worker
celery -A project worker --loglevel=info
```

---

## Accessing the Swarelic Codebase (for 4.1 & 4.5)

Your mentor will provide:
- GitHub access to the main Swarelic repository
- Read-only database credentials for the staging environment (do NOT write to staging)
- Postman collection for the SCAI API

**Important:** Never push changes to the main Swarelic repository. All your work goes in **this** intern tasks repo under `submissions/<your-username>/`.

---

## Common Issues

| Problem | Solution |
|---------|---------|
| `ModuleNotFoundError: No module named 'rules_engine'` | Run pytest from the exercise root directory, not the `tests/` folder |
| `ImportError: cannot import name 'responses'` | Run `pip install responses` |
| `pytest: command not found` | Activate your venv first |
| `redis.exceptions.ConnectionError` | Start Redis: `redis-server` or `docker run -d -p 6379:6379 redis:alpine` |
