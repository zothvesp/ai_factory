# Builder

## Philosophy

A builder makes complex object construction readable and safe. In this AI-OS,
builders are most useful for tests, fixtures, and complex immutable value
creation.

## Rules

- Use builders when construction has many optional fields, nested values, or
  meaningful defaults.
- Required fields must remain explicit or fail fast at build time.
- Builders must not create invalid domain objects silently.
- Test builders should optimize readability without hiding the behavior under
  test.
- Do not use builders for simple objects with clear constructors.

## Bad Example

```python
order = Order(None, "", [], None, False, "x")
```

The call is unreadable and likely invalid.

## Good Example

```python
order = (
    OrderBuilder()
    .for_customer(CustomerId("cust_123"))
    .with_line(sku="SKU-1", quantity=2)
    .build()
)
```

The builder makes fixture intent visible.

## Decision Guidance

Use a builder when repeated construction noise obscures test or domain intent.
Prefer dataclass or Pydantic construction when fields are few and explicit.

## AI Guidance

- Keep production builders rare; domain factories may be a better fit.
- Do not hide mandatory fields behind arbitrary defaults.
- Make test builders live near test support code unless reused broadly.
- Keep builders aligned with domain invariants.

## Review Checklist

- Builder improves readability for complex construction.
- Required fields are enforced.
- Defaults are meaningful and documented.
- It does not bypass validation or invariants.
- Tests remain clear about behavior being verified.

## References

- Testing: `../clean-code/testing.md`
- Factory: `factory.md`
- Domain Value Objects: `../domain/value-objects.md`
