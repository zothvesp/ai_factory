# Constraints

## Purpose

Constraints are binding limits that shape acceptable solutions for a goal.

## Rules

- Constraints must be specific, reviewable, and relevant to the task.
- Separate hard constraints from preferences.
- Include technology, compatibility, security, compliance, data, performance,
  budget, deployment, and timeline constraints when applicable.
- Constraint violations require owner-approved exceptions.

## Entry Format

```markdown
- Constraint:
- Type: Technology, security, compatibility, data, performance, operations,
  delivery, or governance.
- Source:
- Verification:
- Exception authority:
```

## Bad Example

```text
Make it scalable.
```

## Good Example

```text
Constraint: Public API error response shape must remain backward compatible for
existing clients unless versioning is approved.
Verification: API contract tests and OpenAPI diff.
```

## AI Guidance

- Convert vague constraints into testable statements.
- Do not weaken constraints to simplify implementation.
- Link durable constraints to executive or Project Brain entries.

## Review Checklist

- Constraint is testable.
- Source and authority are clear.
- Verification method exists.
- Exceptions are documented.
- Acceptance criteria reflect the constraint.

## References

- Executive Constraints: `../executive/constraints.md`
- Architecture Constitution: `../architecture/constitution.md`
