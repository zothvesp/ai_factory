# Decorator

## Philosophy

A decorator wraps a collaborator to add behavior while preserving the same
contract. It is useful for logging, caching, retries, metrics, authorization, or
transaction boundaries when those concerns should remain separate.

## Rules

- A decorator must implement the same contract as the wrapped collaborator.
- It must not surprise callers by changing business semantics.
- Keep ordering explicit when multiple decorators are composed.
- Do not hide retries, caching, or authorization where callers need to know the
  outcome.
- Test wrapper behavior and pass-through behavior.

## Bad Example

```python
class CachedUserRepository:
    def get(self, user_id: UserId) -> User:
        user = self._cache.get(user_id)
        if user:
            user.activate("cache hit")
        return user
```

The wrapper changes domain state as a side effect of caching.

## Good Example

```python
class InstrumentedUserRepository(UserRepository):
    def get(self, user_id: UserId) -> User:
        with self._metrics.timer("user_repository.get"):
            return self._inner.get(user_id)
```

The decorator adds measurement without changing the repository contract.

## Decision Guidance

Use decorators for orthogonal behavior that can be applied consistently around a
port or service. Prefer direct implementation when the behavior is intrinsic to
the collaborator.

## AI Guidance

- State the preserved contract before adding a decorator.
- Keep decorator composition visible in dependency wiring.
- Be careful with caching around authorization, tenancy, and mutable objects.
- Add observability and failure tests for retrying decorators.

## Review Checklist

- Decorator implements the same interface.
- Added behavior is orthogonal and explicit.
- Ordering with other decorators is understood.
- It does not hide security or consistency decisions.
- Tests verify wrapper and pass-through behavior.

## References

- Dependency Injection: `../engineering/dependency-injection.md`
- Observability Standards: `../python/logging.md`
- Hidden Side Effects: `../smells/hidden-side-effects.md`
