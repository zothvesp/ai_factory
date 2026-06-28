# Heuristics

## Philosophy

Heuristics help reviewers make consistent judgments when code does not clearly
violate one rule but still feels fragile. They are prompts for reasoning, not
automatic rejection criteria.

## Rules

- Prefer boring, explicit code over clever code.
- Optimize for the next reader and maintainer, not the original author.
- Keep abstractions proportional to repeated, proven complexity.
- Treat surprise as a design smell: hidden mutation, hidden I/O, hidden global
  state, and hidden time all require scrutiny.
- Make invalid states hard to represent.
- Review code at the right level: local clean-code issues are different from
  architecture, domain, security, or performance issues.
- Record exceptions when a rule is intentionally violated.

## Useful Questions

- What is the smallest behavior this code is responsible for?
- What would make this code fail in production?
- Can a test describe the intended behavior simply?
- Would a new engineer know where to make the next change?
- Are names, types, tests, and errors telling the same story?
- Is the abstraction based on current needs or speculative reuse?

## Bad Example

```python
def execute(x, y, mode):
    return globals()[mode](x, y)
```

The code is concise but surprising, unsafe, hard to type-check, and difficult
to review.

## Good Example

```python
HANDLERS: Mapping[Operation, OperationHandler] = {
    Operation.APPROVE: approve_order,
    Operation.REJECT: reject_order,
}
```

The dispatch is explicit, typed, and reviewable.

## Decision Guidance

Use heuristics when multiple standards apply or when a change is debatable.
Escalate to a specific standard when the concern becomes concrete: naming,
function size, class responsibility, error handling, testing, architecture, or
security.

## AI Guidance

- Explain which heuristic triggered a concern.
- Do not block on subjective preference without connecting it to risk.
- Prefer a concrete fix or test over a broad style critique.
- When principles conflict, use `../engineering/README.md` to route the
  trade-off.

## Review Checklist

- Code is unsurprising for the repository and domain.
- Abstractions are justified by real variation or complexity.
- Hidden I/O, time, randomness, mutation, and global state are absent or
  explicit.
- Exceptions to standards are documented and owned.
- Review comments distinguish risk from preference.

## References

- KISS: `../engineering/kiss.md`
- YAGNI: `../engineering/yagni.md`
- Principle Routing: `../engineering/README.md`
- Code Review: `../checklists/code-review.md`
