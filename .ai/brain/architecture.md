# Architecture Knowledge

Architecture knowledge records current system facts, boundaries, integration
patterns, runtime topology, and architecture exceptions discovered during work.

## Entry Format

```markdown
## YYYY-MM-DD - Architecture Fact

- Context: Where this fact was discovered.
- Fact: Current architecture state.
- Evidence: Files, diagrams, configs, ADRs, or tests.
- Impact: Why future agents need to know.
- Owner: Software Architect.
- Review trigger: Change that invalidates the fact.
```

## Rules

- Record facts, not aspirational design.
- Link durable decisions to ADRs when required.
- Keep framework, persistence, API, async, and deployment facts separate enough
  to review.
- Update stale entries when architecture changes.

## Bad Example

```text
The architecture is clean.
```

## Good Example

```text
Fact: FastAPI routers are transport adapters and must not own domain policy.
Evidence: Architecture Constitution and FastAPI standards.
```

## AI Guidance

- Do not infer architecture solely from directory names.
- Cite evidence.
- Escalate constitution exceptions.

## Review Checklist

- Fact is evidence-backed.
- Impact for future work is clear.
- Owner and review trigger exist.
- ADR linkage is present when needed.
- Stale assumptions are not preserved.

## References

- Architecture Standards: `../architecture/README.md`
- ADRs: `../architecture/adrs.md`
