# API Design

## Purpose

This document defines the API contract for the Notification Service. It specifies the endpoints, request and response models, validation rules, and expected behavior. The goal is to provide a consistent interface that allows backend services to integrate with the Notification Service independently of its internal implementation.

---

## API Principles

- Follow RESTful API conventions.
- Exchange data using JSON.
- Process notification requests asynchronously.
- Return the current state of the notification request instead of the final delivery status.
- Keep client services independent of notification templates and delivery mechanisms.
- Validate all incoming requests before accepting them.

---

## Authentication

All requests must be authenticated before accessing the Notification Service.

**Version 1 Assumption**

- Communication occurs within a trusted internal network.
- Authentication will initially use an API Key.
- The design can later be extended to support OAuth2 or JWT-based service authentication.

---

# Endpoints

---

## POST /notifications

### Description

Accepts a notification request from a backend service and queues it for asynchronous processing.

### Request

```json
{
  "recipient": {
    "email": "john@example.com",
    "name": "John Doe"
  },
  "template": "ORDER_SHIPPED",
  "data": {
    "orderId": "ORD-1001",
    "trackingId": "TRK123456",
    "carrier": "FedEx"
  }
}
```

### Successful Response

**202 Accepted**

```json
{
  "notificationId": "2b0f6c2a-72d4-4a9c-9d53-2a88a7c7d321",
  "status": "QUEUED",
  "message": "Notification accepted for processing."
}
```

### Error Responses

| Status | Description                     |
| ------ | ------------------------------- |
| 400    | Invalid request payload         |
| 401    | Authentication failed           |
| 404    | Notification template not found |
| 422    | Validation failed               |
| 500    | Internal server error           |

### Validation Rules

- Recipient email must be valid.
- Template name must exist.
- Required template variables must be provided.
- Unknown fields are rejected.

---

## GET /notifications/{notificationId}

### Description

Returns the current processing status of a notification.

### Successful Response

```json
{
  "notificationId": "2b0f6c2a-72d4-4a9c-9d53-2a88a7c7d321",
  "status": "SENT",
  "createdAt": "2026-07-28T09:30:15Z",
  "updatedAt": "2026-07-28T09:30:18Z"
}
```

---

# Data Models

## Notification Request

| Field           | Type   | Required |
| --------------- | ------ | -------- |
| recipient.email | String | Yes      |
| recipient.name  | String | No       |
| template        | String | Yes      |
| data            | Object | Yes      |

---

## Notification Response

| Field          | Type               |
| -------------- | ------------------ |
| notificationId | UUID               |
| status         | NotificationStatus |
| message        | String             |

---

## Notification Status

| Status     | Description                                 |
| ---------- | ------------------------------------------- |
| QUEUED     | Request accepted and waiting for processing |
| PROCESSING | Worker is processing the notification       |
| SENT       | Notification delivered successfully         |
| FAILED     | Delivery failed after all retry attempts    |

---

## Error Handling

The API returns standardized error responses.

Example:

```json
{
  "timestamp": "2026-07-28T09:30:15Z",
  "status": 422,
  "error": "Validation Failed",
  "message": "Recipient email is invalid."
}
```

---

## API Versioning

Version 1 exposes:

```
/api/v1/notifications
```

Future breaking changes will be introduced through a new API version rather than modifying existing endpoints.

---

## Future APIs

The following endpoints are intentionally excluded from Version 1 but may be introduced later.

| Endpoint                       | Purpose                       |
| ------------------------------ | ----------------------------- |
| GET /notifications             | List notifications            |
| POST /notifications/{id}/retry | Retry a failed notification   |
| DELETE /notifications/{id}     | Delete notification history   |
| GET /templates                 | List available templates      |
| POST /templates                | Create notification templates |
