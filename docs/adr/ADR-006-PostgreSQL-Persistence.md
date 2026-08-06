# ADR-006: Use PostgreSQL for Durable Notification Persistence

## Status

Accepted

## Date

2026-08-05

## Context

The Notification Service currently uses an in-memory notification store to maintain notification metadata and processing status.

The current implementation stores notification records in a Python dictionary within the application process. While this is sufficient for early development and testing, it has several limitations:

- Notification data is lost when the application restarts.
- Multiple application instances cannot share notification state.
- Notification history cannot be reliably persisted or audited.
- Worker processes cannot rely on a shared durable source of truth.
- The system cannot reliably recover notification state after failures.

As the Notification Service evolves toward a production-oriented asynchronous architecture, notification state must be stored durably and remain available across application restarts and multiple service instances.

The system also needs to track the lifecycle of each notification:

```text
QUEUED
   ↓
PROCESSING
   ↓
SENT
```

and eventually:

```text
QUEUED
   ↓
PROCESSING
   ↓
FAILED
```

A persistent database is therefore required to maintain the authoritative state of each notification.

## Decision

We will use **PostgreSQL** as the primary durable persistence layer for notification metadata and processing state.

The application will use **SQLAlchemy 2.x** as the ORM and database access layer, with asynchronous database access through the PostgreSQL `asyncpg` driver.

**Alembic** will be used to manage database schema migrations.

The persistence architecture will follow this structure:

```text
Notification Service
        ↓
Notification Repository
        ↓
SQLAlchemy AsyncSession
        ↓
PostgreSQL
```

The Notification Service will interact with a repository abstraction rather than directly accessing SQLAlchemy or PostgreSQL.

The repository will initially support operations such as:

- Create a notification record.
- Retrieve a notification by ID.
- Update notification status.
- Persist notification timestamps and metadata.

PostgreSQL will become the **source of truth for notification state**.

The message queue will remain responsible for **transporting work to background workers** and will not replace the database as the authoritative source of notification state.

## Data Ownership

The responsibilities of each infrastructure component are separated as follows:

```text
PostgreSQL
    ↓
Stores the durable state of notifications.

Queue
    ↓
Transports notification processing tasks.

Worker
    ↓
Processes queued notification tasks.

Notification Service
    ↓
Coordinates business operations.
```

This separation allows the persistence and messaging technologies to evolve independently.

## Alternatives Considered

### In-Memory Storage

The current implementation uses an in-memory dictionary.

#### Advantages

- Simple to implement.
- No external infrastructure required.
- Useful for local development and early testing.

#### Disadvantages

- Data is lost when the application restarts.
- Cannot be shared between multiple application instances.
- Not suitable as a durable source of truth.
- Cannot reliably support production workloads.

#### Decision

Rejected for production persistence.

### MongoDB

MongoDB was considered as a document-oriented persistence layer.

#### Advantages

- Flexible document structure.
- Natural representation of notification payload data.
- Easy horizontal scaling.

#### Disadvantages

- A relational database is sufficient for the current notification data model.
- Notification state and lifecycle updates fit well within a relational model.
- PostgreSQL provides strong transactional guarantees and mature relational tooling.

#### Decision

Rejected for the initial implementation.

### PostgreSQL

#### Advantages

- Strong transactional guarantees.
- Mature ecosystem.
- Reliable persistence.
- Excellent support for relational data.
- Strong tooling and migration support.
- Suitable for structured notification metadata and lifecycle state.
- Supports future reporting and querying requirements.

#### Disadvantages

- Requires additional infrastructure.
- Requires database connection management.
- Schema changes require migrations.

#### Decision

Accepted.

## Consequences

### Positive Consequences

- Notification data survives application restarts.
- Multiple application instances can share the same notification state.
- Notification history can be retained for auditing and troubleshooting.
- Workers can update notification status using a shared durable data source.
- The service can recover notification state after failures.
- The repository abstraction allows the persistence implementation to evolve independently of business logic.

### Negative Consequences

- PostgreSQL becomes an additional infrastructure dependency.
- Database connections must be managed correctly.
- Database migrations must be maintained.
- Local development requires PostgreSQL infrastructure, such as Docker Compose.
- Database availability becomes an operational concern.

## Target Persistence Architecture

The initial persistence architecture will be:

```text
                Notification API
                       ↓
              Notification Service
                 /           \
                ↓             ↓
         Notification       Queue
          Repository          ↓
                ↓          Worker
                ↓             ↓
           PostgreSQL ←───────┘
```

The responsibilities are:

```text
Notification Service
    ↓
Coordinates the business workflow.

Notification Repository
    ↓
Provides persistence operations.

PostgreSQL
    ↓
Stores the authoritative notification state.

Queue
    ↓
Carries work that needs asynchronous processing.

Worker
    ↓
Consumes queued work and updates notification state.
```

## Future Considerations

The initial implementation will use PostgreSQL together with the existing in-memory queue.

The architecture will eventually evolve toward:

```text
                  Backend Services
                         │
                         ▼
                Notification API
                         │
                         ▼
              Notification Service
                   /          \
                  ↓            ↓
          Notification       Queue
           Repository          │
                  ↓            ▼
             PostgreSQL      Worker
                                │
                                ▼
                       Update Notification
                              Status
```

The current decision does not define the final queue technology.

A separate ADR will be created when selecting the production message broker.

Future reliability improvements may also require evaluating patterns such as the **Transactional Outbox Pattern** to address scenarios where:

- Database persistence succeeds but queue publishing fails.
- Queue publishing succeeds but database persistence fails.

The final reliability strategy will be documented in a separate architectural decision record when the production queue technology is selected.

## Migration Plan

The migration from the current in-memory store to PostgreSQL will happen incrementally.

### Current State

```text
NotificationService
        ↓
InMemoryNotificationStore
        ↓
Python Dictionary
```

### Target State

```text
NotificationService
        ↓
NotificationRepository
        ↓
SQLAlchemy AsyncSession
        ↓
PostgreSQL
```

The migration will follow these steps:

1. Introduce PostgreSQL as a local development dependency.
2. Add SQLAlchemy asynchronous database configuration.
3. Create the PostgreSQL notification table.
4. Configure Alembic migrations.
5. Implement the Notification Repository.
6. Update `NotificationService` to use the repository.
7. Update the Notification Worker to update notification status through the repository.
8. Remove the in-memory store from the production request flow.
9. Update integration tests to verify PostgreSQL persistence.

The API contract will remain unchanged during this migration.

The following endpoints will continue to work without client-side changes:

```text
POST /api/v1/notifications
GET  /api/v1/notifications/{notification_id}
```

## Resulting Architecture After Migration

After completing this ADR's implementation, the expected architecture will be:

```text
                         Backend Services
                       /       |        \
                      /        |         \
                 Order      Payment    Inventory
                      \        |         /
                       \       |        /
                        ▼      ▼       ▼
                    Notification API
                           │
                   Authentication
                           │
                     Validation
                           │
                           ▼
                  Notification Service
                     /            \
                    /              \
                   ▼                ▼
          Notification         In-Memory Queue
           Repository                 │
                   │                  ▼
                   ▼           Notification Worker
              PostgreSQL              │
                   ▲                  │
                   └──────────────────┘
                    Status Updates
```

The in-memory queue is intentionally retained at this stage.

A future ADR will define the production queue technology and the reliability guarantees required for coordinating database persistence and asynchronous processing.
