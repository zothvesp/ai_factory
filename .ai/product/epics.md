# Epics

## Philosophy

An epic is a delivery container for related work that is too large for one
reviewable story. It exists to manage sequencing, risk, dependencies, and
incremental value.

## Rules

- Epics must define outcome, scope, dependencies, risks, constraints, and exit
  criteria.
- Split epics into independently reviewable stories.
- Each story must produce useful evidence or value.
- Track cross-cutting NFR, security, migration, and documentation work.
- Close an epic only when acceptance and exit criteria are satisfied.

## Bad Example

```text
Epic: Modernize everything.
```

The scope cannot be reviewed or completed safely.

## Good Example

```text
Epic: Extract backup scheduling rules.
Outcome: Scheduling policy is testable outside framework code.
Slices: characterize current behavior, model schedule value objects, add
application service, migrate API endpoint.
```

## Decision Guidance

Use an epic when work needs sequencing across several stories. Use a PRD when
stakeholder alignment is missing. Use a technical debt entry when no immediate
delivery is planned.

## AI Guidance

- Keep epic slices small enough for focused review.
- Identify the first slice that reduces uncertainty.
- Do not let epics become open-ended buckets.
- Update Project Brain when an epic reveals durable rules or risks.

## Review Checklist

- Epic has a measurable outcome.
- Stories are independently reviewable.
- Dependencies and risks are explicit.
- Exit criteria are objective.
- NFR and documentation work are included.

## References

- Goal Decomposition: `../goals/goal-engineering.md`
- Stories: `stories.md`
- Technical Debt: `../brain/technical-debt.md`
