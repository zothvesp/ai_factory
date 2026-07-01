# Observer

## Philosophy

Observer lets independent subscribers react to events without coupling the
publisher to every consequence. In modernization work, this often appears as
domain events, application events, or message subscribers.

## Rules

- Publish events that describe facts that already happened.
- Keep event schemas stable, versioned where needed, and owned.
- Subscribers must be idempotent when delivery can repeat.
- Do not use observer when the publisher requires an immediate result from the
  subscriber.
- Make delivery semantics explicit: in-process, transactional outbox, broker, or
  scheduled dispatch.

## Bad Example

```python
def approve_order(order: Order) -> None:
    for handler in global_handlers:
        handler(order)
```

The global subscriber list hides ordering, errors, ownership, and delivery
semantics.

## Good Example

```python
order.approve()
events.record(OrderApproved(order.id, occurred_at=clock.now()))
```

The application can later dispatch the recorded event through an explicit
mechanism.

## Decision Guidance

Use observer for independent reactions to facts. Use direct calls when the
caller needs a synchronous answer, transactional consistency with the callee, or
clear command flow.

## AI Guidance

- Distinguish domain events from integration events.
- Do not publish events before the state change is committed unless the delivery
  model is intentionally transactional.
- Add idempotency and retry guidance for broker-backed observers.
- Record event ownership in the Project Brain or ADR when durable.

## Review Checklist

- Event name describes a past fact.
- Schema ownership and compatibility are clear.
- Delivery semantics are explicit.
- Subscribers are idempotent where required.
- Failures do not silently lose critical work.

## References

- Domain Events: `../domain/domain-events.md`
- Messaging Architecture: `../architecture/messaging.md`
- Async Architecture: `../architecture/async.md`
