# High-Level Design (HLD)

## Purpose

This High-Level Design (HLD) document describes the overall architecture of the Notification Service and the interactions between its major components. It provides a high-level view of how notification requests flow through the system, from the time a backend service submits a request until the notification is delivered to the end user.

The purpose of this document is to establish a shared understanding of the system's design before implementation. It focuses on the responsibilities of each component and their interactions, without going into low-level implementation details.

---

## System Context

The Notification Service acts as a centralized platform responsible for delivering notifications on behalf of multiple backend services. Business services such as Order, Payment, Inventory, and User Management integrate with the Notification Service through a common API whenever a notification needs to be sent.

The Notification Service processes incoming requests and communicates with an external Email Provider to deliver notifications to end users. While backend services initiate notification requests, the Notification Service owns the complete notification delivery lifecycle.

---

## Core Components

### Notification API

Receives notification requests from backend services, validates incoming requests, and forwards them for processing.

### Notification Processor

Processes validated requests, performs business validations, creates notification jobs, and submits them for asynchronous processing.

### Notification Queue

Temporarily stores notification jobs, enabling asynchronous processing and preventing backend services from waiting for email delivery.

### Notification Worker

Consumes notification jobs from the queue, renders notification templates, sends emails through the configured Email Provider, applies retry logic for transient failures, and updates notification status.

### Notification Database

Stores notification metadata, delivery status, timestamps, and audit information required for tracking and troubleshooting.

### Email Provider

An external service responsible for delivering emails to recipients.

---

## Request Flow

1. A backend service sends a notification request to the Notification API.
2. The Notification API validates the incoming request.
3. The Notification Processor creates a notification job.
4. The notification job is placed into the Notification Queue.
5. The Notification Worker retrieves the job from the queue.
6. The worker renders the appropriate notification template using the provided data.
7. The worker sends the email through the configured Email Provider.
8. The Notification Database is updated with the final delivery status.
9. The backend service is not blocked while the notification is being processed.

---

## Related ADRs

The following architectural decisions influenced this design:

- ADR-001 – Use asynchronous processing for notification delivery.

---

## High-Level Architecture Diagram

```text
                        +----------------------------------+
                        |        Backend Services          |
                        |----------------------------------|
                        | • Order Service                 |
                        | • Payment Service               |
                        | • Inventory Service             |
                        | • User Service                  |
                        +---------------+------------------+
                                        |
                                        | Notification Request
                                        |
                                        v
                      +--------------------------------------+
                      |         Notification API             |
                      +----------------+---------------------+
                                       |
                                       | Validate Request
                                       |
                                       v
                    +------------------------------------------+
                    |      Notification Processor              |
                    +----------------+-------------------------+
                                     |
                                     | Enqueue Job
                                     |
                                     v
                      +-------------------------------+
                      |      Notification Queue       |
                      +---------------+---------------+
                                      |
                                      | Consume Job
                                      |
                                      v
                  +-------------------------------------------+
                  |         Notification Worker               |
                  |-------------------------------------------|
                  | • Render Template                         |
                  | • Send Email                              |
                  | • Retry on Failure                        |
                  | • Update Notification Status              |
                  +-------------+-----------------------------+
                                |                    |
                 Update Status  |                    | Send Email
                                |                    |
                                v                    v
              +-------------------------+     +----------------------+
              | Notification Database   |     |   Email Provider     |
              +-------------------------+     +----------------------+
```
