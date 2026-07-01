# Goal Risks

## Purpose

Goal risks capture uncertain events that could prevent the goal from succeeding
or create unacceptable side effects.

## Rules

- Record likelihood, impact, mitigation, owner, trigger, and status.
- Separate risks from active defects and known debt.
- High-impact risks must influence scope, design, tests, or release gates.
- Accepted risks require authority and review trigger.

## Entry Format

```markdown
- Risk:
- Likelihood: Low, medium, or high.
- Impact: Low, medium, or high.
- Mitigation:
- Owner:
- Trigger:
- Status:
```

## Bad Example

```text
Risk: Something may break.
```

## Good Example

```text
Risk: Refactoring retry eligibility may change behavior for credential failures.
Mitigation: Add characterization tests before extraction.
Owner: Backend Engineer.
Trigger: Before implementation loop.
```

## AI Guidance

- Tie risks to tests, design choices, and checklists.
- Escalate security, data loss, and release risks early.
- Move durable risks into `../brain/risks.md`.

## Review Checklist

- Risk is specific.
- Likelihood and impact are stated.
- Mitigation is actionable.
- Owner and trigger exist.
- Accepted risk has authority.

## References

- Project Brain Risks: `../brain/risks.md`
- Security Review: `../checklists/security-review.md`
