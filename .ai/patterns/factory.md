# Factory

## Philosophy

A factory centralizes creation when construction involves invariants, variants,
defaults, or dependency composition that should not be scattered across callers.

## Rules

- Use factories to protect creation rules, not to hide simple constructors.
- Keep domain factories free of infrastructure dependencies.
- Make required inputs explicit.
- Do not use factories as service locators.
- Tests must verify variant selection and invariant enforcement.

## Bad Example

```python
class ServiceFactory:
    def get(self, name: str) -> Any:
        return globals()[name]()
```

This is hidden lookup, not controlled creation.

## Good Example

```python
class InvoiceFactory:
    def create_for_order(self, order: Order, tax_policy: TaxPolicy) -> Invoice:
        lines = [InvoiceLine.from_order_line(line) for line in order.lines]
        return Invoice.create(order.customer_id, lines, tax_policy)
```

Creation is named and keeps invoice invariants together.

## Decision Guidance

Use a factory when creation logic is repeated, conditional, or validates
important rules. Prefer direct construction when the object has a simple and
stable initializer.

## AI Guidance

- Do not add abstract factories before real variation exists.
- Keep composition-root factories separate from domain factories.
- Name the factory after what it creates and why creation is non-trivial.
- Replace magic string selection with typed enums or explicit registries.

## Review Checklist

- Factory exists for real creation complexity.
- Required inputs are explicit.
- It does not hide global lookup or framework state.
- Domain invariants are preserved.
- Tests cover creation variants.

## References

- YAGNI: `../engineering/yagni.md`
- Service Locator: `../anti-patterns/service-locator.md`
- Domain Aggregates: `../domain/aggregates.md`
