# Definition of Done

## Philosophy

Done means the work satisfies its goal and leaves enough evidence for future
agents to trust, review, operate, and extend it.

## Required Gates

- Acceptance criteria and exit criteria are satisfied.
- Tests, review, documentation, and metrics evidence match the risk.
- Architecture, security, product, and code review gates are complete where
  triggered.
- Project Brain is updated with new rules, decisions, risks, debt, lessons, or
  glossary terms.
- Manifest, project state, next task, and changelog are updated for phase
  closures.
- Changes are committed and pushed to the configured Git remote.
- Known residual risk has an owner and repayment or review trigger.

## Bad Example

```text
Done: Files were edited.
```

Editing is activity, not completion.

## Good Example

```text
Done: Acceptance criteria passed, tests cover retry edge cases, ADR records the
new outbox decision, Project Brain risk is updated, and the phase commit is
pushed.
```

## Decision Guidance

Close work only when evidence exists. If evidence is impossible in the current
environment, record what was not verified, why, risk level, and next action.

## AI Guidance

- Do not claim tests or reviews were run unless they were.
- Report residual risk clearly.
- Keep phase metadata current before final status.
- Avoid unrelated cleanup after Done is achieved.

## Review Checklist

- Goal and criteria are met.
- Required tests or review evidence exists.
- Documentation and Project Brain are updated.
- Git commit and push are complete when required.
- Residual risks are owned and visible.

## References

- Metrics: `../metrics/README.md`
- Changelog: `../CHANGELOG.md`
- Project State: `../PROJECT_STATE.md`
