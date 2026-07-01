# User Journeys

## Philosophy

A user journey maps an end-to-end experience across time, channels, decisions,
and handoffs. It reveals friction that isolated stories and API tasks miss.

## Rules

- Define persona, trigger, stages, goals, pain points, decisions, handoffs,
  success signals, and failure recovery.
- Include backstage operational steps when they affect user outcomes.
- Identify moments that require observability, support, audit, or documentation.
- Link journey pain points to features, epics, stories, and NFRs.
- Keep journeys current when workflows change.

## Bad Example

```text
Journey: User logs in and uses the app.
```

This is too broad to reveal decisions or friction.

## Good Example

```text
Stage: Diagnose failed backup.
User goal: Understand whether failure is retryable.
Pain: Logs expose provider text but no category.
Opportunity: Categorize failure and link to remediation guidance.
```

## Decision Guidance

Use a journey when work spans several screens, jobs, systems, or teams. Use a
use case when one actor-system interaction needs precision.

## AI Guidance

- Look for operational handoffs and support burden.
- Do not optimize one step while worsening the full journey.
- Convert journey pain into testable stories and NFRs.
- Update roadmap when journey analysis reveals larger opportunities.

## Review Checklist

- Persona and trigger are clear.
- Stages and handoffs are mapped.
- Pain points connect to deliverable work.
- Success and recovery are defined.
- Documentation and support implications are captured.

## References

- Personas: `personas.md`
- Features: `features.md`
- Roadmap: `../brain/roadmap.md`
