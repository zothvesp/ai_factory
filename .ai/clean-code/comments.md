# Comments

## Philosophy

Comments should explain intent, constraints, and non-obvious trade-offs. They
must not compensate for unclear names, tangled functions, or missing tests.

## Rules

- Prefer clearer code over explanatory comments.
- Use comments for business constraints, security rationale, compatibility
  requirements, and unusual implementation trade-offs.
- Keep comments close to the code they explain.
- Remove stale comments immediately when behavior changes.
- Do not comment obvious mechanics.
- Public APIs may need docstrings when the contract is not obvious from types
  and names.
- Complex migrations, concurrency, and security-sensitive code should include
  rationale comments when future edits could be dangerous.

## Bad Example

```python
# increment i by one
i += 1
```

The comment repeats the operation without explaining intent.

## Good Example

```python
# Keep this query ordered by id so retry batches are deterministic after a
# worker crash.
statement = statement.order_by(UserModel.id)
```

The comment explains an operational constraint that is not obvious from syntax.

## Decision Guidance

Write a comment when deleting it would remove important context that code cannot
express cleanly. Refactor instead when the comment merely explains confusing
control flow or naming.

## AI Guidance

- Do not generate boilerplate comments for every function.
- Preserve rationale comments unless the underlying constraint is removed.
- When adding comments, mention the constraint, not the implementation trivia.
- Use ADRs for durable architecture decisions instead of burying them in code.

## Review Checklist

- Comments explain why, constraints, or trade-offs.
- Comments are accurate after the change.
- Obvious comments were not added.
- Public docstrings describe stable contracts where needed.
- Security and concurrency comments are reviewed carefully.

## References

- ADRs: `../architecture/adrs.md`
- Refactoring: `refactoring.md`
- Clean Code Heuristics: `heuristics.md`
