# Architecture Review Checklist

Architecture review verifies that a change preserves system direction,
boundaries, quality attributes, operational safety, and long-term maintainability.
It is required for changes that affect dependency direction, data ownership,
integration, security boundaries, deployment, or major design patterns.

## Review Inputs

- Goal, constraints, risks, acceptance criteria, and exit criteria.
- Architecture Constitution.
- Relevant ADRs and Project Brain entries.
- Diagrams, API contracts, data model changes, and deployment notes.
- Code diff and tests when implementation already exists.

## Review Triggers

Run architecture review when a change:

- introduces or changes a bounded context, aggregate, service, repository,
  adapter, or integration;
- changes database schema, migration strategy, or data ownership;
- changes authentication, authorization, secrets, or trust boundaries;
- introduces async workflows, queues, scheduled jobs, caches, or external calls;
- changes deployment topology, runtime configuration, or operational failure
  modes;
- requires an exception to the Architecture Constitution.

## Boundary and Dependency Direction

- Domain logic is independent of FastAPI, SQLAlchemy sessions, Redis clients,
  environment variables, external APIs, and framework lifecycle.
- Dependencies point inward from transport and infrastructure toward
  application and domain policy.
- Ports are owned by the layer that needs the capability.
- Adapters implement ports without leaking infrastructure exceptions inward.
- Cross-context collaboration uses explicit contracts, events, or APIs.
- No circular dependencies were introduced.

## Domain and Application Design

- Business rules live in domain or application layers, not routers, ORM models,
  migrations, or infrastructure glue.
- Aggregates protect invariants.
- Value objects name important concepts and enforce local rules.
- Application services orchestrate use cases without becoming god classes.
- Domain services are used only when behavior genuinely spans domain objects.
- Ubiquitous language is consistent with Project Brain and glossary entries.

## API and Integration Contracts

- FastAPI endpoints expose stable Pydantic v2 request and response models.
- Internal ORM models and infrastructure errors do not leak through API
  contracts.
- Versioning, pagination, filtering, error shapes, and authentication behavior
  are explicit when applicable.
- External integration failures have retry, timeout, idempotency, and fallback
  decisions where needed.
- Message and event schemas have owners and compatibility expectations.

## Persistence and Data

- SQLAlchemy mappings do not become the accidental domain model.
- Repository or unit-of-work boundaries are used where domain behavior and
  transaction scope matter.
- Alembic migrations include sequencing, rollback or mitigation, data integrity
  checks, and operational notes.
- Indexes and constraints support expected access patterns and invariants.
- Data retention, privacy, and audit requirements are addressed.

## Security and Privacy

- Trust boundaries are explicit.
- Authentication and authorization are enforced server-side.
- Secrets are not stored in source, logs, exceptions, or Project Brain entries.
- Input validation is performed at boundaries and domain invariants are enforced
  in core logic.
- Sensitive workflows produce audit events without exposing sensitive data.
- Dependency and supply-chain risk is considered for new libraries.

## Performance and Reliability

- Async code does not hide blocking I/O.
- Timeouts, retries, circuit breakers, idempotency, and backpressure are
  considered for remote calls and queues.
- Caching is justified by a performance goal and has invalidation ownership.
- Critical workflows are observable through logs, metrics, traces, or audits.
- Failure modes are explicit and testable.

## Maintainability and Evolution

- The design avoids service locator, singleton abuse, tight coupling, and magic
  values.
- Variation points are explicit without speculative plugin systems.
- A single conceptual change has a clear primary owner.
- Architectural exceptions include owner, rationale, risk, expiry condition, and
  Project Brain entry.
- The design can be migrated incrementally from the current legacy state.

## Required Outputs

- Approval, required changes, or documented exception.
- ADR when the change affects lasting architecture direction.
- Project Brain updates for decisions, risks, debt, dependencies, or lessons.
- Updated diagrams or contracts when they materially help future agents.

## AI Guidance

- Start from the goal and quality attributes, not from preferred patterns.
- Challenge hidden dependencies and unclear ownership early.
- Prefer small, reversible architecture moves over sweeping rewrites.
- Use the anti-pattern index to classify architecture findings consistently.
- Escalate unresolved constitution violations instead of normalizing them.

## References

- Architecture Constitution: `../architecture/constitution.md`
- Anti-Pattern Review Index: `../anti-patterns/README.md`
- Smell Review Index: `../smells/README.md`
- ADRs: `../architecture/adrs.md`
- Project Brain: `../brain/README.md`
