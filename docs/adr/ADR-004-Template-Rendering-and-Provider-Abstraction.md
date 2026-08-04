# ADR-004: Template Rendering and Provider Abstraction

**Status:** Accepted  
**Date:** 2026-08-04

---

## Context

The Notification Service must centralize notification content generation and support future notification channels such as SMS and push.

We need a clean separation between event payloads, template rendering, and delivery mechanism.

## Decision

Notification content will be rendered using event-driven templates stored by the service. Templates will be rendered with Jinja2 and supplied data from the client request.

Delivery will be implemented through a provider abstraction layer:

- `BaseEmailProvider`
- `ConsoleEmailProvider` / `MockEmailProvider` for development/testing
- `SMTP` or cloud provider implementations for production

## Consequences

- Templates remain centralized and can be updated independently of client code.
- The notification service owns presentation logic and event-to-message mapping.
- Adding new channels later requires only a new provider implementation and template conventions.
- The service can validate required template variables before enqueuing delivery.

## Alternatives Considered

- Client-provided subject/body text
  - Easier for clients, but duplicates template logic across services.
- Template rendering in client services
  - Violates the goal of centralized notification logic and consistent experience.
- Hard-coded string templates in service code
  - Works, but is not flexible for future template extension.
