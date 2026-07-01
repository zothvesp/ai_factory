# Mission

## Philosophy

The mission explains why the AI-OS exists and what value it must protect. It is
the highest-level filter for prioritization and scope.

## Mission Statement

The AI Engineering OS exists to make AI-assisted modernization of large legacy
software systems safe, repeatable, reviewable, and aligned with business value.

## Rules

- Every phase must improve the AI-OS as a durable operating system, not a
  one-time documentation dump.
- Standards must support safe modernization of Python, FastAPI, SQLAlchemy,
  PostgreSQL, Redis, Docker, Kubernetes, GitHub Actions, pytest, Ruff, and mypy
  systems.
- The mission prioritizes correctness, maintainability, security, observability,
  and governance over speed or volume.
- Work outside the mission must be explicitly justified or rejected.

## Bad Example

```text
Generate many documents quickly so the repository looks complete.
```

This violates the mission because volume without quality misleads future agents.

## Good Example

```text
Expand one standards pack completely, update state and Project Brain, commit,
push, then proceed to the next bounded pack.
```

## Decision Guidance

Accept work that strengthens future AI agent decisions. Defer or reject work
that is decorative, unreviewable, unowned, or disconnected from modernization
safety.

## AI Guidance

- Cite the mission when resolving priority conflicts.
- Prefer durable standards over transient advice.
- Do not close work that creates false confidence.

## Review Checklist

- Work supports safe modernization.
- Output is reusable by future agents.
- Quality gates are preserved.
- Scope remains bounded and reviewable.
- Mission conflicts are escalated.

## References

- Charter: `charter.md`
- Goal Engineering: `../goals/goal-engineering.md`
