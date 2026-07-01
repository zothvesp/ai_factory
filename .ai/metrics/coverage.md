# Coverage Metrics

## Philosophy

Coverage measures test evidence. It is useful only when it reflects meaningful
behavior, risk, and failure paths.

## Rules

- Track line, branch, and critical-path coverage separately.
- Require direct tests for domain rules, security decisions, migrations, API
  contracts, and failure paths that carry high risk.
- Do not lower assertions or test quality to raise coverage.
- Coverage thresholds must be scoped by component risk.
- Characterization tests count as evidence only when they assert real behavior.

## Bad Example

```text
Coverage is 90%, so the release is safe.
```

High percentage can still miss critical behavior.

## Good Example

```text
Coverage: 86% overall, 100% for payment authorization domain rules, branch
coverage added for timeout and declined-card paths.
```

## Decision Guidance

Use broad coverage to detect untested areas and targeted coverage to protect
high-risk behavior. Require stronger evidence for business rules, security,
data migrations, and integration boundaries.

## AI Guidance

- Prefer meaningful assertions over percentage gains.
- Add tests before refactoring unclear legacy behavior.
- Identify critical uncovered paths in review.
- Explain why any uncovered high-risk path is acceptable.

## Review Checklist

- Critical behavior has direct tests.
- Branch and failure paths are considered.
- Coverage changes are interpreted by risk.
- Flaky or superficial tests are not counted as confidence.
- Exceptions are documented with owner and trigger.

## References

- pytest: `../python/pytest.md`
- Testing Standard: `../clean-code/testing.md`
- Acceptance Criteria: `../product/acceptance-criteria.md`
