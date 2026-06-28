# Errors

## Philosophy

Error handling is part of the design contract. Clean code makes invalid input,
failed dependencies, and impossible states explicit so callers can respond
correctly.

## Rules

- Fail fast on invalid state and violated invariants.
- Raise or return domain-specific errors rather than generic strings.
- Do not swallow exceptions without recording or converting the outcome.
- Preserve exception context with `raise ... from exc` when translating errors.
- Keep user-facing messages separate from diagnostic details.
- Never expose secrets, SQL, stack traces, or internal identifiers in public API
  error responses.
- Tests must cover important failure paths, not only happy paths.

## Bad Example

```python
try:
    charge_customer(order)
except Exception:
    return False
```

The caller cannot distinguish declined payment, network failure, invalid order,
or a programming bug.

## Good Example

```python
try:
    charge_customer(order)
except PaymentGatewayTimeout as exc:
    raise PaymentUnavailable("payment provider timed out") from exc
except CardDeclined as exc:
    raise PaymentRejected(order.id) from exc
```

The code preserves cause while exposing meaningful application outcomes.

## Decision Guidance

Use exceptions for invalid states and dependency failures that interrupt the
current flow. Use explicit result objects for expected business outcomes that
callers routinely branch on, such as validation results or approval decisions.

## AI Guidance

- Do not add broad `except Exception` blocks unless the boundary owns conversion
  and logging.
- Map infrastructure exceptions at adapter boundaries.
- Keep domain errors independent of HTTP, SQLAlchemy, Redis, and FastAPI types.
- Pair new error behavior with tests and API error-contract updates when
  exposed externally.

## Review Checklist

- Errors distinguish validation, domain, dependency, and programming failures.
- Exception context is preserved.
- Public responses do not leak sensitive internals.
- Failure paths are tested.
- Logs contain correlation context without secrets.

## References

- Python Exceptions: `../python/exceptions.md`
- FastAPI Errors: `../fastapi/errors.md`
- Fail Fast: `../engineering/fail-fast.md`
- Security Agent: `../agents/security.md`
