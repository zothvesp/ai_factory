# Facade

## Philosophy

A facade provides a simpler interface over a complex subsystem. It reduces
coupling when callers need a stable, task-oriented entry point.

## Rules

- A facade should expose use-case language, not internal subsystem mechanics.
- Keep the facade thin; do not turn it into a god service.
- Do not hide failures that callers must handle.
- Do not use a facade to bypass domain boundaries or authorization.
- Test facade workflows at the level of the contract it exposes.

## Bad Example

```python
class AppFacade:
    def do_everything(self, payload: dict[str, Any]) -> dict[str, Any]: ...
```

The facade hides all responsibilities behind one vague method.

## Good Example

```python
class BillingFacade:
    def create_invoice_for_order(self, order_id: OrderId) -> InvoiceId:
        order = self._orders.get(order_id)
        invoice = self._invoices.create_from_order(order)
        self._publisher.publish(InvoiceCreated(invoice.id))
        return invoice.id
```

The facade exposes a coherent subsystem workflow.

## Decision Guidance

Use a facade when many callers depend on a complex subsystem and need a stable
task-oriented API. Do not use it to avoid fixing unclear boundaries inside the
subsystem.

## AI Guidance

- Name the subsystem and caller need before adding a facade.
- Keep facade methods aligned with use cases.
- Avoid generic payloads and result dictionaries.
- Escalate if the facade starts owning unrelated responsibilities.

## Review Checklist

- Facade simplifies a real subsystem boundary.
- Methods are cohesive and use domain language.
- It does not centralize unrelated behavior.
- Failure and authorization behavior are explicit.
- Tests cover facade-level workflows.

## References

- Clean Architecture: `../architecture/clean-architecture.md`
- God Class: `../smells/god-class.md`
- Use Cases: `../product/use-cases.md`
