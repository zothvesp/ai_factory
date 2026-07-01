# Non-Functional Requirements

## Philosophy

NFRs define quality attributes such as security, performance, reliability,
operability, maintainability, compatibility, accessibility, and compliance.
They are product requirements because they shape user trust and delivery risk.

## Rules

- NFRs must be measurable, testable, or reviewable.
- Define scope, metric, threshold, measurement method, owner, and review cadence.
- Include security, privacy, observability, recovery, and performance for
  production-facing work.
- Do not use vague terms such as fast, scalable, secure, or robust without
  thresholds.
- Link NFRs to tests, monitoring, architecture decisions, and release gates.

## Bad Example

```text
The API must be fast and secure.
```

The requirement cannot guide design or verification.

## Good Example

```text
For authenticated backup job search, p95 response time must be under 300 ms for
10,000 jobs per tenant in staging load tests, excluding cold cache startup.
```

## Decision Guidance

Create explicit NFRs whenever quality attributes affect user trust, compliance,
cost, operations, or architecture. Keep NFRs proportional for internal
documentation-only changes.

## AI Guidance

- Convert vague quality words into measurable thresholds.
- Escalate missing security, privacy, or reliability NFRs for production work.
- Align NFRs with architecture, performance, security, and observability
  standards.
- Update metrics and release checklists when NFRs become gates.

## Review Checklist

- NFR has metric, threshold, and measurement method.
- Scope and exclusions are clear.
- Owner and review cadence are defined.
- Verification evidence is planned.
- Architecture and release gates reflect the NFR.

## References

- Performance Metrics: `../metrics/performance.md`
- Security Review: `../checklists/security-review.md`
- Architecture Review: `../checklists/architecture-review.md`
