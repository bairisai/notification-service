# ADR-005: Observability and Health Probes

**Status:** Accepted  
**Date:** 2026-08-04

---

## Context

A production-grade notification service must be observable and easy to operate. Early instrumentation is important for debugging delivery problems and ensuring platform availability.

We must decide how to expose health and metric signals, as well as correlate API requests with background worker execution.

## Decision

The service will implement:

- Structured JSON logging with correlation IDs
- Health endpoints:
  - `GET /health/live`
  - `GET /health/ready`
- Metrics endpoint for monitoring
- Traceable request context passed through API → queue → worker

## Consequences

- Operators can detect startup and dependency failures quickly.
- Request flow can be traced across service boundaries for debugging.
- Metrics enable capacity planning and SLA monitoring.
- Logging can include safe request identifiers instead of raw payload content.

## Alternatives Considered

- Minimal logging only
  - Easier initially, but insufficient for production troubleshooting.
- No readiness probe
  - Simpler, but makes orchestration and deployment health checks less reliable.
- Tracing only in API layer
  - Limits ability to diagnose worker-side failures.
