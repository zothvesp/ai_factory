# Product Requirements Document

## Philosophy

A PRD aligns stakeholders before significant design or delivery work begins. It
defines the problem, outcome, constraints, risks, and measurable success without
prescribing unnecessary implementation detail.

## Rules

- A PRD must state the problem, target users, business outcome, scope,
  non-scope, constraints, risks, success metrics, and release considerations.
- Requirements must be testable or reviewable.
- Separate product requirements from implementation proposals.
- Include NFRs for security, performance, reliability, accessibility,
  operability, and compliance when relevant.
- Link related goals, ADRs, epics, and Project Brain entries.

## Bad Example

```text
Build a new reporting service with FastAPI and PostgreSQL.
```

This starts with a solution and omits users, outcomes, constraints, and success
evidence.

## Good Example

```text
Problem: Finance operators cannot reconcile failed backup billing events within
one business day.
Outcome: Reduce unresolved reconciliation cases older than 24 hours by 80%.
Scope: Event search, failure reason visibility, exportable audit trail.
Non-scope: Changing billing provider contracts.
```

## Decision Guidance

Use a PRD for initiatives that span multiple stories, teams, bounded contexts,
or release decisions. Use a story or use case for narrow changes that fit within
an already-approved product direction.

## AI Guidance

- Ask for missing product facts only when they affect readiness or safety.
- Do not invent business metrics; propose candidates and mark assumptions.
- Keep architecture recommendations out of the PRD unless they are constraints.
- Update roadmap, risks, glossary, and business rules when discovered.

## Review Checklist

- Problem and outcome are clear.
- Users and stakeholders are named.
- Scope and non-scope are explicit.
- Success metrics and NFRs are measurable.
- Risks, assumptions, and dependencies are recorded.

## References

- Goal Engineering: `../goals/goal-engineering.md`
- NFRs: `nfrs.md`
- Epics: `epics.md`
