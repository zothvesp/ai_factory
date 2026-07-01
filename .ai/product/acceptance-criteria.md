# Acceptance Criteria

## Philosophy

Acceptance criteria define observable conditions that prove a story, feature, or
phase satisfies its goal. They are the bridge between product intent, tests, and
review.

## Rules

- Criteria must be specific, observable, unambiguous, and testable.
- Include positive, negative, edge, permission, and failure behavior when
  relevant.
- Avoid implementation-only criteria unless implementation is the requirement.
- Tie criteria to user value, NFRs, business rules, or governance rules.
- Do not close work until criteria and exit criteria are both satisfied.

## Bad Example

```text
The page should work well.
```

This cannot be tested or reviewed.

## Good Example

```text
Given a failed backup caused by invalid credentials, when an operator views the
job detail, then the failure category is "credential_error" and retry is
disabled with remediation guidance.
```

## Decision Guidance

Use scenario format when behavior depends on state or actor action. Use a
checklist format for documentation, governance, or non-interactive deliverables.

## AI Guidance

- Refuse to implement ambiguous work until criteria are clear enough to verify.
- Generate tests from acceptance criteria when possible.
- Keep criteria stable during implementation unless discovery changes the goal.
- Record changed criteria in the changelog or Project Brain when material.

## Review Checklist

- Criteria are observable and testable.
- Important failure paths are included.
- Criteria trace to goals and user value.
- NFRs are represented where relevant.
- Evidence is available before completion.

## References

- Goal Engineering: `../goals/goal-engineering.md`
- Testing: `../clean-code/testing.md`
- Definition of Done: `../checklists/definition-of-done.md`
