# Stories

## Philosophy

A story defines a small, valuable, testable change from the perspective of an
affected user, operator, system, or maintainer.

## Rules

- A story must include actor, need, value, scope, assumptions, acceptance
  criteria, and test evidence.
- Stories must be small enough for one focused implementation and review.
- Do not use stories as vague task labels.
- Include negative and failure criteria when behavior can fail.
- Link to feature, epic, use case, NFR, and relevant standards.

## Bad Example

```text
Story: Refactor backup code.
```

This does not identify actor, value, or acceptance.

## Good Example

```text
As an operations engineer, I need failed backup jobs to show the provider error
category so I can decide whether to retry, escalate, or fix credentials.
```

## Decision Guidance

Use a story for deliverable behavior or documentation value. Use a task for
internal steps under a story. Use a spike when uncertainty must be reduced
before committing to delivery.

## AI Guidance

- Reject stories without acceptance criteria.
- Preserve behavior unless the story explicitly changes it.
- Make non-scope visible to prevent opportunistic refactors.
- Translate technical stories into maintainer or operator value.

## Review Checklist

- Actor, need, and value are clear.
- Scope and non-scope are explicit.
- Acceptance criteria are testable.
- Failure and edge cases are considered.
- Required documentation and Project Brain updates are included.

## References

- Acceptance Criteria: `acceptance-criteria.md`
- Use Cases: `use-cases.md`
- Definition of Ready: `../checklists/definition-of-ready.md`
