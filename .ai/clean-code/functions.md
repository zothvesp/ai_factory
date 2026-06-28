# Functions

## Philosophy

Functions should express one coherent step at one level of abstraction. They are
the smallest named units reviewers use to verify behavior.

## Rules

- A function must have one primary reason to change.
- Keep command and query behavior separate unless the side effect is explicit in
  the name and contract.
- Prefer parameters that are domain values, commands, or explicit primitives
  over loosely shaped dictionaries.
- Return explicit results. Do not encode business outcomes in hidden mutation.
- Raise specific exceptions for invalid states and boundary failures.
- Extract functions when code mixes policy, orchestration, parsing,
  persistence, or transport concerns.
- Do not extract functions solely to hide complexity without improving names or
  cohesion.

## Bad Example

```python
def handle(payload: dict[str, Any], db: Session) -> dict[str, Any]:
    user = db.get(UserModel, payload["id"])
    user.status = "A"
    db.commit()
    send_email(user.email)
    return {"ok": True}
```

This function validates nothing and mixes transport shape, persistence,
business policy, transaction control, and notification.

## Good Example

```python
def activate_user(command: ActivateUser, users: UserRepository) -> User:
    user = users.get(command.user_id)
    user.activate(reason=command.reason)
    users.save(user)
    return user
```

The function now orchestrates a single application use case and delegates
business rules to the domain object.

## Decision Guidance

Extract a function when a block can be named after intent, is independently
testable, or removes a lower-level detail from a higher-level workflow. Keep it
inline when extraction would create a misleading name or scatter a simple idea.

## AI Guidance

- Start by identifying the function's responsibility in one sentence.
- If one sentence requires "and", inspect for mixed responsibilities.
- Avoid mechanical extraction that preserves hidden side effects.
- Add tests before changing complex functions with business behavior.

## Review Checklist

- Function name matches its observable behavior.
- Parameters and return values are explicit.
- Abstraction level is consistent.
- Side effects are named, injected, and testable.
- Complex branches are covered by tests.

## References

- Long Method: `../smells/long-method.md`
- Hidden Side Effects: `../smells/hidden-side-effects.md`
- Tell, Don't Ask: `../engineering/tell-dont-ask.md`
