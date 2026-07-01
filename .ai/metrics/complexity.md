# Complexity Metrics

## Philosophy

Complexity metrics highlight code that is hard to understand, test, and modify.
They point reviewers toward risk; they do not automatically prove bad design.

## Rules

- Track cyclomatic complexity, cognitive complexity, nesting depth, function
  length, class responsibility spread, and dependency fan-in/fan-out.
- Treat rising complexity in critical workflows as a review signal.
- Distinguish essential domain complexity from accidental implementation
  complexity.
- Do not reduce complexity by hiding branches behind misleading abstractions.
- Pair complexity reduction with tests when behavior may change.

## Bad Example

```text
Split one complex function into ten unnamed helpers to reduce the score.
```

The metric improves while readability may get worse.

## Good Example

```text
Extract retry eligibility policy into a named domain service with tests for
credential, timeout, and quota failure cases.
```

## Decision Guidance

Refactor complexity when it blocks understanding, testing, or safe change. Keep
complex code when it accurately represents complex rules and is well named,
tested, and localized.

## AI Guidance

- Explain what makes the code hard: branches, nesting, state, dependencies, or
  abstraction mismatch.
- Prefer naming, guard clauses, value objects, and policy extraction over broad
  rewrites.
- Cite smell and clean-code standards in findings.
- Avoid metric-only refactors.

## Review Checklist

- Complexity hotspot is tied to concrete risk.
- Essential and accidental complexity are distinguished.
- Tests protect refactoring.
- Refactor improves names and responsibilities.
- No new indirection hides the same complexity.

## References

- Long Method: `../smells/long-method.md`
- Functions: `../clean-code/functions.md`
- KISS: `../engineering/kiss.md`
