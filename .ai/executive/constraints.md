# Constraints

## Philosophy

Constraints are binding limits that shape acceptable solutions. They protect
compliance, compatibility, budget, technology direction, and operational safety.

## Standing Constraints

- Technology stack targets Python 3.13+, FastAPI, SQLAlchemy 2.x, Pydantic v2,
  PostgreSQL, Alembic, Redis, AsyncIO, Docker, Kubernetes, GitHub Actions,
  pytest, Ruff, and mypy.
- Architecture must comply with the Architecture Constitution.
- Every phase must update manifest, project state, next task, changelog, and
  Project Brain where relevant.
- Phase work must be committed and pushed to the configured GitHub repository.
- Placeholder and skeletal documents are not production standards.

## Rules

- Constraints must be specific and reviewable.
- Conflicting constraints require escalation to the accountable role.
- Accepted constraint violations must be documented as exceptions, debt, risks,
  or ADRs.
- Do not silently weaken security, data, compatibility, or release constraints.

## Bad Example

```text
Keep it enterprise-grade.
```

This is too vague to verify.

## Good Example

```text
All production API changes must preserve documented error response compatibility
unless versioning is approved.
```

## Review Checklist

- Constraints are explicit and testable.
- Technology and governance constraints are respected.
- Violations are documented and owned.
- Constraints are reflected in acceptance criteria.
- New durable constraints update Project Brain.

## References

- Architecture Constitution: `../architecture/constitution.md`
- Goal Constraints: `../goals/goal-engineering.md`
