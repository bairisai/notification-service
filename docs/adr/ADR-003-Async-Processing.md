# ADR-003: Async Processing and Queueing

**Status:** Accepted  
**Date:** 2026-08-04

---

## Context

The Notification Service must accept requests quickly and process email delivery asynchronously so backend services are not blocked waiting for email provider responses.

The HLD defines a Notification Queue and Worker. We need to select the queuing technology that best fits the current implementation plan and future scaling needs.

## Decision

The service will use a dedicated message queue system backed by Redis and an async task worker framework.

The API will persist notification metadata in PostgreSQL and enqueue a notification processing task after successful request acceptance. A worker process will consume jobs from the queue and perform template rendering and delivery.

## Consequences

- Backend services receive fast feedback with `202 Accepted`.
- Delivery retries and failure handling are managed by the worker pipeline instead of the API request path.
- Queue-based architecture enables scaling workers independently from the ingestion tier.
- Redis is a practical early choice for broker state and pub/sub support.

## Alternatives Considered

- In-process background tasks
  - Simpler, but not scalable and not suitable for production-grade async processing.
- Database polling queue
  - Avoids an external broker, but increases DB load and reduces responsiveness.
- RabbitMQ / Kafka
  - More powerful, but heavier than needed for the first production-grade email notification service.
