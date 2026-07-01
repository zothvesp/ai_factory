# Duplication Metrics

## Philosophy

Duplication metrics reveal repeated code, rules, and knowledge. The highest
risk is duplicated business meaning, not identical syntax.

## Rules

- Track exact duplication, near duplication, repeated business rules, repeated
  validation, and copied test fixtures.
- Prioritize duplicated decisions over duplicated harmless structure.
- Do not abstract code that is similar today but likely to diverge for valid
  reasons.
- Remove duplication only when the abstraction has a clear name and owner.
- Keep intentional symmetry documented when duplication is acceptable.

## Bad Example

```text
Create a generic validate(entity, rules) engine for two unrelated validations.
```

The abstraction may hide domain language and create coupling.

## Good Example

```text
Move duplicate email normalization into EmailAddress value object and reuse it
from registration and import flows.
```

## Decision Guidance

Use DRY when duplicated knowledge creates inconsistent behavior or change
amplification. Keep duplication when it preserves independent evolution,
readability, or boundary separation.

## AI Guidance

- Identify whether duplication is code, data, rule, test, or workflow.
- Prefer domain value objects and named policies for duplicated business rules.
- Avoid generic utility modules for unrelated duplication.
- Link findings to DRY and duplicate-code standards.

## Review Checklist

- Duplication type and risk are identified.
- Proposed abstraction has a domain or architectural name.
- Independent evolution is considered.
- Tests prove behavior remains consistent.
- Accepted duplication is documented where non-obvious.

## References

- Duplicate Code: `../smells/duplicate-code.md`
- DRY: `../engineering/dry.md`
- Value Objects: `../domain/value-objects.md`
