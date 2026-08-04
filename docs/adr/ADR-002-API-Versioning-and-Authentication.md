# ADR-002: API Versioning and Authentication

**Status:** Accepted  
**Date:** 2026-08-04

---

## Context

The Notification Service must expose a stable external contract for backend services that can evolve over time. The first version should be easy to adopt and safe to extend without breaking existing clients.

We also need a simple authentication strategy for an internal service API before a more advanced identity system is available.

## Decision

The service will expose a versioned REST API under `/api/v1` with the following primary endpoints:

- `POST /api/v1/notifications`
- `GET /api/v1/notifications/{notificationId}`

The service will accept requests only from authenticated backend clients using an API key supplied in a request header.

## Consequences

- The API contract can be safely extended in a future `v2` release without breaking current integrations.
- Clients receive a clear, stable path for notification requests and status polling.
- API key authentication is simple enough for early internal deployment and can later be replaced with OAuth2/JWT.
- The service remains consistent with the HLD goal of a centralized notification platform.

## Alternatives Considered

- `POST /notifications` without versioning
  - Simpler initially, but more brittle for future breaking changes.
- OAuth2/JWT from day one
  - More secure, but adds integration complexity for initial internal launch.
- Trusting network-level security only
  - Acceptable for trusted internal deployments, but does not address client-level authentication.
