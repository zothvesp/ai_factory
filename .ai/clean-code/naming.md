# Naming

## Philosophy

Names are the primary interface for readers. A good name reduces the need for
comments, prevents accidental misuse, and exposes the domain language used by
the business.

## Rules

- Use domain terms from the ubiquitous language for business concepts.
- Name functions with verbs or verb phrases: `calculate_total`, `approve_order`.
- Name values with nouns that state meaning, not representation:
  `customer_id`, not `uuid_str`.
- Use explicit units and time zones when relevant: `timeout_seconds`,
  `created_at_utc`.
- Avoid abbreviations unless they are standard in the domain or platform.
- Avoid type-only suffixes such as `data`, `info`, `obj`, and `dict` unless the
  type itself is the concept being modeled.
- Constants must name the business rule, not just the literal value.
- Test names must describe behavior and condition.

## Bad Example

```python
def proc(d: dict[str, str]) -> bool:
    return d["s"] == "A" and int(d["n"]) > 0
```

The reader must decode `proc`, `d`, `s`, `A`, and `n`.

## Good Example

```python
ACTIVE_STATUS = "A"


def is_active_account(row: Mapping[str, str]) -> bool:
    return row["status"] == ACTIVE_STATUS and int(row["balance_cents"]) > 0
```

The code still exposes a legacy row shape, but the intent is now visible.

## Decision Guidance

Use a shorter name when the scope is tiny and the role is conventional, such as
`row` in a loop. Use a longer name when the value crosses a boundary, expresses
business meaning, or appears in logs, errors, tests, or public APIs.

## AI Guidance

- Rename before refactoring behavior when unclear names hide the design problem.
- Preserve public API names unless a versioned contract change is approved.
- When generating code, derive names from domain, API, or persistence standards,
  not from implementation shortcuts.

## Review Checklist

- Names expose intent without requiring nearby comments.
- Business concepts use the ubiquitous language.
- Units, time zones, and currencies are explicit.
- Constants describe rules rather than literal values.
- Test names state behavior and scenario.

## References

- Domain Language: `../domain/ubiquitous-language.md`
- Magic Values: `../anti-patterns/magic-values.md`
- Python Typing: `../python/typing.md`
