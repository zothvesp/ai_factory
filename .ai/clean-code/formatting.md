# Formatting

## Philosophy

Formatting should disappear from code review. Automated, consistent layout lets
reviewers focus on behavior, design, security, and tests.

## Rules

- Use Ruff formatting and linting as the default authority for Python style.
- Do not hand-align code in ways automated tools will undo.
- Keep imports ordered and unused imports removed.
- Prefer one clear expression over dense clever formatting.
- Break long expressions by semantic grouping, not arbitrary line length alone.
- Keep files organized by public interface, helpers, and local implementation
  details where the module pattern supports it.
- Avoid formatting-only churn in unrelated files.

## Bad Example

```python
result=service.calculate(user ,order,  True,{"x":1})
```

The formatting increases review effort and hides the meaning of arguments.

## Good Example

```python
result = service.calculate(
    user=user,
    order=order,
    include_discounts=True,
    metadata={"source": "checkout"},
)
```

The layout exposes argument meaning and works with automated formatting.

## Decision Guidance

Accept the formatter unless it makes a real semantic grouping harder to read.
If a formatted expression is still confusing, simplify the expression instead of
fighting the formatter.

## AI Guidance

- Run or respect configured formatting tools before final review.
- Keep formatting changes separate from behavior changes when possible.
- Do not introduce a new style preference without updating the project standard.
- Prefer named arguments when positional booleans or primitives reduce clarity.

## Review Checklist

- Code follows configured formatter and linter expectations.
- Imports are clean and ordered.
- Layout clarifies behavior rather than hiding complexity.
- Formatting churn is limited to touched code.
- Dense expressions were simplified where useful.

## References

- Ruff: `../python/ruff.md`
- Python 3.13+: `../python/python313.md`
- Code Review: `../checklists/code-review.md`
