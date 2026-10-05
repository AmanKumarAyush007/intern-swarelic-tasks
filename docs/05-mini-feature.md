# Exercise 4.5 — Mini Feature Implementation

## 🎯 Objective

Implement a **real, production-ready mini feature** in a standalone service that mirrors the Swarelic platform. This is the capstone exercise — you choose your approach and deliver end-to-end.

**Time estimate:** 8–12 hours (spread across 2–3 sessions)

---

## ⚠️ This Is Different

Unlike previous exercises, **Exercise 4.5 has no single correct solution**. You are evaluated on:
- Quality of your implementation
- How well you understand the platform
- How you approach design decisions
- Code quality, tests, and documentation

---

## 🛠️ Choose Your Feature

Pick **one** of the following mini features to implement:

---

### Option A: Call Queue Dashboard (Recommended)

**What:** A real-time call queue status API with statistics.

**Build:**
- Django model `CallQueue` with fields: `name`, `tenant`, `max_size`, `current_calls`
- API endpoints:
  - `GET /api/v1/queues/` — List all queues with current statistics
  - `GET /api/v1/queues/<id>/stats/` — Detailed stats: avg wait time, longest wait, abandonment rate
  - `POST /api/v1/queues/<id>/enqueue/` — Add a call to the queue
  - `POST /api/v1/queues/<id>/dequeue/` — Remove next call from queue
- Celery task: Send alert when queue size > threshold
- Unit tests: 10+ test cases

**Stretch goals:**
- `WebSocket` endpoint for real-time queue updates (Django Channels)
- Queue priority levels (VIP calls go to front)

---

### Option B: Agent Performance Report Generator

**What:** A Celery task that generates PDF/JSON performance reports for agents.

**Build:**
- `ReportConfig` model: `agent`, `period_start`, `period_end`, `metrics` (list of requested metrics)
- `GenerateAgentReport` Celery task that:
  - Fetches call logs for the agent + period
  - Computes: total calls, avg duration, call outcome breakdown, busiest hour
  - Stores the result as a `Report` model instance
- API endpoint: `POST /api/v1/reports/generate/` that triggers the task and returns task ID
- API endpoint: `GET /api/v1/reports/<task_id>/` that returns status + result when ready
- Unit tests: 10+ test cases

**Stretch goals:**
- Export report as CSV
- Schedule periodic report generation via Celery Beat

---

### Option C: Webhook Event System

**What:** A configurable webhook delivery system where tenants can subscribe to platform events.

**Build:**
- `WebhookSubscription` model: `tenant`, `target_url`, `events` (list), `secret`, `is_active`
- `WebhookDelivery` model: logs every delivery attempt with status, response code, duration
- Celery task: `deliver_webhook(event_type, payload, subscription_id)` with retry logic
- API endpoints:
  - `POST /api/v1/webhooks/` — Register a new webhook subscription
  - `GET /api/v1/webhooks/` — List subscriptions
  - `GET /api/v1/webhooks/<id>/deliveries/` — View delivery history
  - `POST /api/v1/webhooks/<id>/test/` — Send a test event
- Unit tests: 10+ test cases

**Stretch goals:**
- HMAC signature verification on delivery
- Exponential backoff retry strategy
- Automatic deactivation after 5 consecutive failures

---

## 📋 Deliverables (All Options)

Your submission at `submissions/<username>/4.5/` must include:

```
4.5/
├── project/                   # Django project
│   ├── settings.py
│   └── urls.py
├── <feature_app>/             # Your feature app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tasks.py               # (if using Celery)
│   └── tests/
│       └── test_<feature>.py
├── requirements.txt
├── README.md                  # Document your design decisions
└── DESIGN_NOTES.md            # Explain: Why did you design it this way?
```

### Required Documentation in `DESIGN_NOTES.md`

1. **Which option did you choose and why?**
2. **What are the key design decisions you made?** (At least 3 specific decisions)
3. **What trade-offs did you make?** (e.g., simplicity vs completeness)
4. **What would you do differently with more time?**
5. **What edge cases did you handle? What edge cases did you skip?**

---

## ✅ Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Feature completeness (all required endpoints/models work) | 30% |
| Code quality (clean, readable, idiomatic Django/Python) | 25% |
| Tests (coverage, meaningful assertions, edge cases) | 20% |
| Design notes (thoughtful, specific, shows understanding) | 15% |
| Error handling (proper HTTP codes, meaningful error messages) | 10% |

---

## 💡 Advice From the Mentor Team

> "The best interns don't just make the tests pass — they think about the person who will use this feature, the engineer who will maintain it, and the system that has to scale it."

Start with the **simplest possible working implementation**, then improve it. Don't spend 6 hours on a perfect design and 2 hours on a broken implementation.

The `DESIGN_NOTES.md` is as important as the code — it shows us how you think.

---

## 📎 Kickoff Checklist

Before writing code:
- [ ] Choose an option
- [ ] Sketch the data model on paper (even a napkin sketch counts)
- [ ] List all the API endpoints you'll build
- [ ] Identify what Celery tasks you need
- [ ] Identify potential failure points and how you'll handle them
- [ ] Show your plan to your mentor before starting

---

## 📚 References

- [Django Channels (for Option A WebSocket)](https://channels.readthedocs.io/)
- [HMAC Signatures (for Option C)](https://docs.python.org/3/library/hmac.html)
- [Django select_for_update (for queue operations)](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-for-update)
