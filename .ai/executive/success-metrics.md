# Success Metrics

## Philosophy

Success metrics measure whether the AI-OS is improving modernization outcomes,
not merely producing documents.

## Strategic Metrics

- Standards completion by domain.
- Percentage of phases with updated manifest, state, next task, changelog, and
  Project Brain.
- Number of skeletal documents remaining.
- Review findings tied to standards.
- Rework caused by ambiguous goals.
- Architecture exceptions recorded in ADRs.
- Test evidence coverage for modernization changes.
- Release and deployment gate failures.
- Documentation freshness and unresolved decision age.

## Rules

- Metrics must connect to mission, risk, or stakeholder value.
- Track trends and remaining gaps, not just totals.
- Do not count document volume as success without quality gates.
- Use metrics to adjust roadmap priority.

## Bad Example

```text
Success: 200 pages of documentation.
```

Volume alone can increase noise.

## Good Example

```text
Success: all completed standards have examples, decision guidance, AI guidance,
review checklists, references, manifest entries, and no placeholder sections.
```

## Review Checklist

- Metric is outcome-oriented.
- Threshold or interpretation is clear.
- Owner is identified.
- Metric affects roadmap or governance decisions.
- Measurement does not create perverse incentives.

## References

- Metrics Index: `../metrics/README.md`
- Goal Engineering KPIs: `../goals/goal-engineering.md`
