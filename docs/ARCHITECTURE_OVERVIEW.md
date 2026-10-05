# Swarelic Platform — Architecture Overview

> This document is your map. Study it before writing a single line of code.

---

## What Is Swarelic?

Swarelic is an **AI-powered call-center platform** (SCAI — Swarelic Call AI). It enables businesses to:
- Route incoming and outgoing phone calls through an AI layer
- Transcribe, analyze, and summarize conversations in real time
- Apply custom business rules to determine call routing and escalation
- Manage multiple clients (tenants) from a single backend

---

## High-Level Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                         CLIENT CALLS                          │
│                  (phone, SIP, WebRTC)                         │
└────────────────────────────┬──────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Telephony Layer │
                    │  (Twilio / SIP)  │
                    └────────┬────────┘
                             │  Audio stream
                    ┌────────▼────────┐
                    │  Voice Pipeline  │
                    │  (STT → AI →     │
                    │   TTS → Agent)   │
                    └────────┬────────┘
                             │  Structured events
                    ┌────────▼────────┐
                    │   Rules Engine   │◄─── Business Rules DB
                    │  (routing,       │
                    │   escalation,    │
                    │   scripts)       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌───────▼──┐  ┌───────▼──────┐
     │  Agent UI  │  │  CRM API │  │  Analytics   │
     │  (React)   │  │  (REST)  │  │  Dashboard   │
     └────────────┘  └──────────┘  └──────────────┘
```

---

## Core Components

### 1. Voice Pipeline (`scaibp/voice/`)
Handles the real-time audio stream:
- **STT (Speech-to-Text)**: Converts caller audio → text transcription
- **AI Processing**: Sends transcript to LLM (Gemini) for intent detection
- **TTS (Text-to-Speech)**: Converts AI response → audio played back to caller
- **Noise Cancellation**: Pre-processes audio for clarity

**Key files to read:**
- `scaibp/voice/pipeline.py`
- `scaibp/voice/transcriber.py`

### 2. Rules Engine (`scaibp/rules/`)
A Python-based rule evaluation system:
- Rules are stored as JSON/database records
- Each rule has: `conditions` (list of checks) + `actions` (what to do)
- Rules are evaluated in priority order
- Actions include: route to agent, play message, escalate, log event

**Key files to read:**
- `scaibp/rules/engine.py`
- `scaibp/rules/models.py`

### 3. Multi-Tenant Management (`scaibp/tenants/`)
- Each business client is a **Tenant**
- Tenants have their own: rules, agents, configurations, call logs
- Data isolation via tenant-scoped querysets

### 4. Agent Management (`scaibp/agents/`)
- Tracks agent availability (online/busy/offline)
- Manages call assignment queues
- Records agent performance metrics

### 5. API Layer (`scaibp/api/`)
- DRF-based REST API
- JWT authentication with role-based access
- Versioned under `/api/v1/`

### 6. Background Workers (`scaibp/tasks/`)
- Celery-based async processing
- Jobs: transcript processing, report generation, webhook delivery

---

## Data Flow: A Complete Call

```
1. Caller dials in
2. Telephony provider (Twilio) sends audio stream → Voice Pipeline
3. STT transcribes audio → text events
4. Events sent to Rules Engine
5. Rules Engine evaluates → decides action (e.g., "route to sales team")
6. Agent receives the call via Agent UI
7. AI assistant provides real-time suggestions to agent
8. Call ends → transcript saved → Celery task triggers report + webhook to CRM
```

---

## Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, DRF |
| Database | PostgreSQL + Redis |
| AI | Google Gemini API |
| Voice | Twilio / WebRTC |
| Background | Celery + Redis |
| Frontend | React (internal), Vanilla JS (embedded widgets) |
| Infra | AWS / Terraform |
| Monitoring | Prometheus + Grafana |

---

## Key Terms (See also: `GLOSSARY.md`)

| Term | Meaning |
|------|---------|
| Tenant | A business client using the platform |
| Agent | A human customer service representative |
| STT | Speech-to-Text |
| TTS | Text-to-Speech |
| Pipeline | The end-to-end audio processing chain |
| Rule | A condition+action pair evaluated during a call |
| Escalation | Routing a call to a higher-tier agent or supervisor |
