# Quality Metrics

## Philosophy

Quality metrics show whether the system is becoming safer, more correct, and
more reliable for users and maintainers. They must connect to outcomes, not just
activity.

## Rules

- Track escaped defects, severity distribution, review rework, failed releases,
  rollback rate, flaky tests, and unresolved high-risk findings.
- Segment quality metrics by severity, subsystem, and release where possible.
- Do not treat number of commits, files changed, or comments as quality.
- Every quality gate must define threshold, owner, evidence, and exception path.
- Review trends after each phase and release.

## Bad Example

```text
Quality improved because the team closed 40 tickets.
```

Ticket count does not prove correctness or value.

## Good Example

```text
Critical escaped defects: 0 this release.
High severity review findings accepted as debt: 1, owned by Security Engineer,
repayment trigger before public API release.
```

## Decision Guidance

Use quality metrics to decide whether a phase can close, whether risk needs
escalation, or whether process changes are required. Do not block on noisy
metrics without investigating the underlying defect pattern.

## AI Guidance

- Report quality metrics with context and trend.
- Do not bury severe findings in aggregate counts.
- Link findings to standards and Project Brain entries.
- Escalate repeated quality failures into risks or debt.

## Review Checklist

- Metric connects to user, operational, or maintainability risk.
- Severity and ownership are explicit.
- Threshold and exception process are defined.
- Trend is interpreted, not just reported.
- Follow-up action is clear.

## References

- Definition of Done: `../checklists/definition-of-done.md`
- Risks: `../brain/risks.md`
- Code Review: `../checklists/code-review.md`
