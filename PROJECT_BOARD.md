# Notification Service

## Sprint 0

- [x] Product Requirements Document
- [x] High Level Design
- [x] API Design
- [x] ADR-001 Event Based Notifications

---

## Sprint 1 — Core API & Validation

- [ ] FastAPI app factory and `app/main.py`
- [ ] Request/response Pydantic models
- [ ] REST contract for POST `/api/v1/notifications`
- [ ] Basic health endpoint
- [ ] Structured logging and environment config
- [ ] API key authentication design
- [ ] Unit tests for request validation and API contract

---

## Sprint 2 — Persistence & Async Processing

- [ ] PostgreSQL integration for notification metadata
- [ ] Notification database schema and migrations
- [ ] Async queue design ADR
- [ ] Background worker framework and queue broker integration
- [ ] Enqueue notification jobs after submission
- [ ] Worker state transition `QUEUED` → `PROCESSING`
- [ ] Integration tests for DB and worker flow

---

## Sprint 3 — Template Rendering & Delivery

- [ ] Jinja2 event template engine
- [ ] Notification template registry and validation
- [ ] Email provider abstraction layer
- [ ] Initial console/mock provider implementation
- [ ] Worker delivery flow and `SENT` status update
- [ ] GET `/api/v1/notifications/{notificationId}` status endpoint
- [ ] Provider configuration via environment variables

---

## Sprint 4 — Resilience & Reliability

- [ ] Retry strategy with exponential backoff and jitter
- [ ] Failure handling and `FAILED` state
- [ ] Dead letter / retry limit policy
- [ ] Idempotency key support for duplicate suppression
- [ ] Database indexes for status polling
- [ ] ADR for retry/failure design

---

## Sprint 5 — Observability, Security & E2E

- [ ] Correlation IDs and request tracing
- [ ] Prometheus metrics and structured logs
- [ ] Health readiness and dependency checks
- [ ] API key auth enforcement and service security
- [ ] End-to-end and smoke tests
- [ ] Update docs and operational runbook

---

## Sprint 6 — Production Release

- [ ] Containerization and `docker-compose`
- [ ] CI/CD pipeline and release automation
- [ ] Deployment manifests / Helm charts
- [ ] Production readiness review and staging rollout
- [ ] Release version 1.0.0
