# Testing

## Philosophy

Tests are executable specifications. Clean tests explain expected behavior,
protect refactoring, and keep modernization from becoming guesswork.

## Rules

- Test observable behavior, not private implementation details.
- Name tests after scenario and expected outcome.
- Use Arrange, Act, Assert structure when it improves readability.
- Prefer focused unit tests for domain and application behavior.
- Use integration tests for adapters, database mappings, migrations, API
  contracts, and messaging boundaries.
- Avoid sleeps, shared mutable state, real network calls, and order-dependent
  tests.
- Every bug fix should add or update a regression test unless the risk is
  explicitly documented.

## Bad Example

```python
def test_user():
    service.create({"email": "a@example.com"})
    assert True
```

The test does not specify behavior or verify an outcome.

## Good Example

```python
def test_register_rejects_duplicate_email(users: InMemoryUserRepository) -> None:
    users.save(User.register(EmailAddress("a@example.com")))

    with pytest.raises(DuplicateEmail):
        register_user(RegisterUser(email="a@example.com"), users)
```

The test names the scenario and asserts the contract.

## Decision Guidance

Use unit tests when behavior can be verified without external systems. Use
integration tests when correctness depends on serialization, SQL, transactions,
middleware, dependency wiring, or broker behavior.

## AI Guidance

- Add characterization tests before refactoring unclear legacy behavior.
- Do not weaken assertions to make tests pass.
- Prefer factories and builders over copy-pasted fixture blobs.
- Keep test data meaningful and minimal.
- Verify failure paths and edge cases for every rule change.

## Review Checklist

- Tests describe behavior, scenario, and expected outcome.
- Assertions would fail for meaningful regressions.
- Test boundaries match the risk being verified.
- Tests are deterministic and isolated.
- New behavior and important failure paths are covered.

## References

- pytest: `../python/pytest.md`
- Definition of Done: `../checklists/definition-of-done.md`
- Refactoring: `refactoring.md`
