# Code Review Checklist

Code review verifies that a change satisfies its goal without introducing
avoidable defects, unsafe coupling, hidden behavior, or unmaintainable structure.
Review findings must be specific, actionable, and tied to risk.

## Review Inputs

Before reviewing code, read:

- goal and acceptance criteria;
- changed files and tests;
- relevant Project Brain entries;
- Architecture Constitution when boundaries or dependencies change;
- smell and anti-pattern index pages for maintainability findings.

## Severity Rules

| Severity | Use When | Action |
| --- | --- | --- |
| Blocker | Change is incorrect, unsafe, untestable, insecure, or violates a non-negotiable architecture rule. | Must fix or formally accept before completion. |
| High | Change likely causes defects, hidden coupling, data risk, or future unsafe change amplification. | Fix in current phase unless explicitly deferred with debt owner. |
| Medium | Maintainability, clarity, or coverage issue with bounded risk. | Fix when practical or record follow-up. |
| Low | Local readability or consistency issue. | Optional Boy Scout improvement. |

## Functional Correctness

- The change satisfies the stated acceptance criteria.
- Existing behavior is preserved unless the goal explicitly changes it.
- Edge cases, error paths, and failure modes are handled.
- Inputs are validated at appropriate boundaries.
- Exceptions are meaningful and do not leak infrastructure details to API
  callers.
- Time, randomness, and external state are controlled in tests.

## Design and Maintainability

- Responsibilities are cohesive and named in domain or operational language.
- No new god class, long method, data clump, primitive obsession, or duplicate
  business rule was introduced.
- Side effects are explicit and injected.
- Dependencies are visible in constructors, function parameters, or composition
  roots.
- Values with business meaning have names, units, enums, value objects, or typed
  settings.
- Dead code and commented-out code were removed or explicitly justified.

## Architecture Compliance

- Domain and application logic do not depend on FastAPI, SQLAlchemy sessions,
  external clients, or environment lookups.
- Dependency direction remains inward.
- Cross-boundary calls use ports, adapters, repositories, DTOs, API contracts,
  or domain events as appropriate.
- No circular dependency, service locator, singleton abuse, or tight coupling
  was introduced.
- Persistence and transport models do not become accidental domain models.

## Python, FastAPI, and Data

- Type hints are meaningful and compatible with mypy expectations.
- Pydantic v2 models are used for request/response validation at boundaries.
- SQLAlchemy 2.x usage keeps transactions explicit and scoped.
- Alembic migrations include operational safety notes when schema changes are
  present.
- Async functions do not hide blocking I/O.
- Resource lifetimes are managed through application startup, dependency
  wiring, context managers, or lifespan hooks.

## Tests

- Tests prove behavior, not incidental implementation details.
- Important domain rules have direct tests.
- API changes include contract-level tests where applicable.
- Persistence changes include integration or migration evidence when risk
  warrants it.
- Security-sensitive and failure paths are tested.
- Tests remain deterministic and do not depend on global state or ordering.

## Observability and Operations

- Important workflows produce useful logs, metrics, traces, or audit events.
- Sensitive data is not logged.
- Errors provide enough context for diagnosis.
- New dependencies, jobs, queues, caches, or external calls have ownership and
  failure handling.
- Rollback or mitigation is documented when runtime behavior changes.

## Documentation and Project Brain

- Public behavior changes are documented.
- Architecture decisions or exceptions are recorded.
- Recurring rules, risks, debt, or lessons are added to Project Brain.
- `MANIFEST.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`, and `CHANGELOG.md` are
  updated when closing a phase.

## Maintainability Finding Routing

- Duplicate logic: `../smells/duplicate-code.md`
- Long methods: `../smells/long-method.md`
- God classes: `../smells/god-class.md`
- Primitive obsession: `../smells/primitive-obsession.md`
- Hidden side effects: `../smells/hidden-side-effects.md`
- Data clumps: `../smells/data-clumps.md`
- Dead code: `../smells/dead-code.md`
- Feature envy: `../smells/feature-envy.md`
- Shotgun surgery: `../smells/shotgun-surgery.md`

## Anti-Pattern Finding Routing

- Circular dependencies: `../anti-patterns/circular-dependencies.md`
- Service locator: `../anti-patterns/service-locator.md`
- Magic values: `../anti-patterns/magic-values.md`
- Tight coupling: `../anti-patterns/tight-coupling.md`
- Singleton abuse: `../anti-patterns/singleton-abuse.md`

## AI Guidance

- Lead with bugs and risks, not praise.
- Cite file paths and behavior for each finding.
- Do not request broad rewrites when a smaller safe refactor addresses the risk.
- Distinguish required fixes from optional improvements.
- If no issues are found, state remaining test gaps or residual risk.

## References

- Architecture Constitution: `../architecture/constitution.md`
- Smell Review Index: `../smells/README.md`
- Anti-Pattern Review Index: `../anti-patterns/README.md`
- Definition of Done: `definition-of-done.md`
