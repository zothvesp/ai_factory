# Maintainability Metrics

## Philosophy

Maintainability metrics estimate how safely and quickly the system can change.
They combine code structure, tests, documentation, dependency health, and review
signals.

## Rules

- Track change failure rate, review rework, defect recurrence, dependency
  cycles, complexity trend, duplication trend, test stability, and documentation
  freshness.
- Use maintainability metrics as a dashboard, not a single score.
- Investigate hotspots that combine high churn, high complexity, weak tests, and
  frequent defects.
- Do not improve maintainability numbers by moving complexity to unmeasured
  places.
- Record recurring maintainability issues as debt or standards updates.

## Bad Example

```text
Maintainability is 8.7, so no refactoring is needed.
```

A single score hides local risk.

## Good Example

```text
The scheduler module has high churn, three repeated defects, low branch
coverage, and rising complexity; prioritize characterization tests and boundary
extraction before new scheduling features.
```

## Decision Guidance

Use maintainability metrics to prioritize refactoring and debt repayment where
change risk is highest. Avoid refactoring stable low-risk code only because a
tool reports an abstract score.

## AI Guidance

- Combine quantitative metrics with code review evidence.
- Prefer hotspot analysis over broad rewrites.
- Link findings to smells, clean-code, architecture, and test standards.
- Update technical debt when maintainability risk is accepted.

## Review Checklist

- Metric combines change, defect, test, and structure signals.
- Hotspots are prioritized by business and operational risk.
- Proposed action is specific and bounded.
- Debt and repayment trigger are recorded when deferred.
- Trend is reviewed after remediation.

## References

- Technical Debt: `../brain/technical-debt.md`
- Smells: `../smells/README.md`
- Refactoring: `../clean-code/refactoring.md`
