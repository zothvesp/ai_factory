# Adapter

## Philosophy

An adapter translates between an internal port and an external system, framework,
or protocol. It keeps the application core independent from infrastructure
details.

## Rules

- Define the internal port in application or domain-facing code.
- Put SDK, HTTP, SQLAlchemy, Redis, filesystem, and FastAPI details in the
  adapter.
- Translate external errors into application or domain errors at the boundary.
- Keep adapters thin; business rules belong in domain or application services.
- Test adapters with integration tests or contract tests where serialization,
  credentials, or protocols matter.

## Bad Example

```python
def approve(order_id: OrderId) -> None:
    response = stripe.Customer.retrieve(str(order_id))
    if response["status"] == "ok":
        Order.approve(order_id)
```

Core behavior depends directly on a provider SDK shape.

## Good Example

```python
class StripePaymentGateway(PaymentGateway):
    def authorize(self, payment: PaymentRequest) -> PaymentAuthorization:
        try:
            response = self._client.authorize(payment.to_provider_payload())
        except StripeError as exc:
            raise PaymentUnavailable("stripe authorization failed") from exc
        return PaymentAuthorization.from_provider(response)
```

The provider details remain outside the application core.

## Decision Guidance

Use an adapter when code crosses a boundary you do not own. Do not add an
adapter around simple in-process collaborators that already belong to the same
layer and change for the same reason.

## AI Guidance

- Identify the port before writing the adapter.
- Do not leak provider response objects past the adapter.
- Keep retries, timeouts, and error translation explicit.
- Pair adapter changes with integration or contract tests.

## Review Checklist

- Internal code depends on a port, not provider types.
- Translation is explicit and tested.
- Adapter contains no domain policy.
- Failure modes are mapped safely.
- Observability does not leak secrets.

## References

- Hexagonal Architecture: `../architecture/hexagonal.md`
- Dependency Injection: `../engineering/dependency-injection.md`
- Errors: `../clean-code/errors.md`
