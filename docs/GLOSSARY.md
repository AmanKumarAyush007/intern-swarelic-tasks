# Glossary — Swarelic Platform Terms

| Term | Definition |
|------|-----------|
| **SCAI** | Swarelic Call AI — the AI-powered call management system |
| **Tenant** | A business client using the Swarelic platform; data is isolated per tenant |
| **Agent** | A human customer service representative who handles calls |
| **Supervisor** | A senior agent who can monitor and intercept calls |
| **STT** | Speech-to-Text — converts caller audio to transcript text |
| **TTS** | Text-to-Speech — converts AI-generated text back to audio |
| **Voice Pipeline** | The end-to-end chain: audio in → STT → AI → TTS → audio out |
| **Rules Engine** | Python-based decision system that evaluates rules against call context |
| **Rule** | A condition + action pair; if conditions are met, the action is taken |
| **Action** | What to do when a rule matches: route, voicemail, escalate, hangup |
| **Context** | The dictionary of call attributes evaluated by the Rules Engine |
| **Escalation** | Transferring a call to a supervisor or higher-tier agent |
| **Call Queue** | A waiting line of calls assigned to an agent group |
| **Webhook** | An HTTP callback Swarelic sends to external systems when events happen |
| **CRM** | Customer Relationship Management system; Swarelic integrates with these |
| **JWT** | JSON Web Token — the authentication mechanism used by the SCAI API |
| **Celery** | Python task queue; used for async processing (transcripts, reports) |
| **Beat** | Celery Beat — the scheduler that triggers periodic tasks |
| **Tenant Isolation** | Ensuring one tenant cannot see or modify another tenant's data |
| **Noise Cancellation** | Pre-processing step to clean audio before STT |
| **Intent Detection** | AI classifying what a caller wants (e.g., billing, support, sales) |
| **Transcript** | The text record of a call conversation |
| **Call Log** | A database record of a completed call with metadata |
| **SIP** | Session Initiation Protocol — a telephony standard |
| **WebRTC** | Web Real-Time Communication — browser-based audio/video |
