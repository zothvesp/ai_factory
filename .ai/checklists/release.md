# Release Checklist

## Philosophy

Release readiness verifies that a versioned change is understandable,
compatible, reversible where possible, and supported by evidence.

## Required Gates

- Release scope, user impact, compatibility, and rollout plan are documented.
- Acceptance, test, security, architecture, and metric gates are satisfied.
- Database migrations, feature flags, configuration, and dependencies have
  sequencing and rollback or mitigation plans.
- Public API, documentation, changelog, and support notes are updated.
- Operational owners know monitoring, alerting, and incident response changes.
- Known residual risks are accepted by the proper authority.

## Bad Example

```text
Release after merge because CI passed.
```

CI is necessary evidence, not the full release decision.

## Good Example

```text
Release includes migration dry-run evidence, API compatibility notes, rollback
plan, p95 latency check, and support guidance for new retry failure categories.
```

## Decision Guidance

Use a release checklist for any production-visible behavior, schema, API,
security, dependency, or operational change. Lightweight documentation-only
phases may use changelog and phase state as the release evidence.

## AI Guidance

- Do not hide incompatible changes in minor releases.
- Surface migration and rollback risk early.
- Link release notes to product value and operational impact.
- Stop release when required evidence is missing.

## Review Checklist

- Scope and impact are clear.
- Compatibility and migration risks are handled.
- Rollback or mitigation is documented.
- Monitoring and support are ready.
- Changelog and documentation are current.

## References

- DevOps Agent: `../agents/devops.md`
- Product NFRs: `../product/nfrs.md`
- Metrics: `../metrics/README.md`
