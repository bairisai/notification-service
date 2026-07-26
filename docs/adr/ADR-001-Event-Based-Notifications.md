# ADR-001: Event-Based Notification Requests

**Status:** Accepted  
**Date:** July 26, 2026

---

## Context

The Notification Service will be used by multiple backend applications such as Order, Payment, User, and Inventory services.

We needed to define how these applications should communicate with the Notification Service while keeping the design scalable, maintainable, and easy to extend as new notification channels are introduced.

Three approaches were considered.

---

## Decision

The Notification Service will use an **event-based request model**.

Instead of sending a fully formatted email, client services will send:

- The notification event (e.g., `ORDER_SHIPPED`)
- Recipient information
- The dynamic data required to populate the notification template

The Notification Service will be responsible for:

- Selecting the appropriate template
- Rendering the notification content
- Delivering the notification
- Handling retries and failures
- Supporting additional notification channels in the future

This keeps notification logic centralized while allowing business services to remain focused on their own responsibilities.

---

## Options Considered

### Option 1 — Direct Email Requests

Each service constructs the email and sends the complete subject and body to the Notification Service.

**Pros**

- Simple to implement
- Gives each service full control over email content

**Cons**

- Notification templates are duplicated across services
- Template updates require changes in multiple codebases
- Business services become responsible for presentation logic

---

### Option 2 — Pure Event Model

Each service sends only the notification event. The Notification Service retrieves any additional information by calling other services.

**Pros**

- Clean separation of responsibilities
- Very small request payloads

**Cons**

- Additional service-to-service communication
- Increased latency
- Higher operational complexity

---

### Option 3 — Event + Template Data (**Selected**)

Each service sends the notification event together with the data required to populate the notification template.

**Pros**

- Keeps services loosely coupled
- Avoids unnecessary service calls
- Centralizes notification templates
- Easy to support new notification channels
- Simple API for client services

**Cons**

- Client services must provide the required template data

---

## Consequences

### Positive

- Notification logic is managed in one place.
- Templates can be updated without modifying client services.
- New notification channels can be added with minimal impact on existing integrations.
- Business services remain focused on business logic.

### Trade-off

Client services are responsible for supplying the dynamic data required to render a notification. This slightly increases the request payload but keeps the Notification Service independent of other business services.

---

## Notes

This decision establishes the Notification Service as a notification platform rather than an email sender. Client services publish notification events, while the Notification Service owns template management, delivery, and future channel expansion.
