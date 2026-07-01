# Features

## Philosophy

A feature is a coherent user or operator capability that delivers product value.
It is larger than a story and smaller than a broad product initiative.

## Rules

- Define the user capability, value, boundaries, affected personas, and success
  indicators.
- Link features to PRDs, epics, stories, use cases, and NFRs.
- Keep feature scope outcome-oriented, not technology-oriented.
- Identify rollout, migration, support, and observability needs.
- Avoid feature definitions that bundle unrelated capabilities.

## Bad Example

```text
Feature: Add Redis.
```

This is a technical choice, not a product capability.

## Good Example

```text
Feature: Resume interrupted backup downloads.
Users: Operators managing unreliable network environments.
Value: Reduce manual restart effort and failed backup windows.
```

## Decision Guidance

Create a feature when multiple stories contribute to one user capability. Use an
epic when the work is primarily a delivery grouping. Use an ADR when the concern
is architectural rather than product-facing.

## AI Guidance

- Name the capability from the user's perspective.
- Flag hidden NFRs such as latency, auditability, retention, and permissions.
- Do not split by technical layer unless delivery risk requires it.
- Ensure every story under the feature preserves the feature outcome.

## Review Checklist

- Feature has a clear capability and value.
- Boundaries and exclusions are documented.
- Personas and use cases are linked.
- NFRs and rollout concerns are captured.
- Stories can be traced back to the feature outcome.

## References

- PRD: `prd.md`
- Stories: `stories.md`
- User Journeys: `user-journeys.md`
