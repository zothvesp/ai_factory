# Deployment Checklist

## Philosophy

Deployment readiness verifies that a release can be promoted into an
environment safely, observed during rollout, and recovered if it fails.

## Required Gates

- Target environment, version, configuration, secrets, and dependencies are
  identified.
- Database migrations are ordered, tested, and compatible with running code.
- Health checks, readiness checks, logs, metrics, traces, and alerts are in
  place for changed workflows.
- Rollout strategy is defined: all-at-once, rolling, canary, blue/green, or
  manual.
- Rollback, forward-fix, and incident response paths are documented.
- Post-deployment verification is defined and assigned.

## Bad Example

```text
Deploy and watch if users complain.
```

This lacks proactive verification and recovery.

## Good Example

```text
Deploy as canary to 10% of tenants, verify job search p95 latency and error
rate for 30 minutes, then continue rollout or disable feature flag.
```

## Decision Guidance

Use stricter deployment gates for schema changes, security-sensitive paths,
external integrations, async jobs, queues, and customer-visible behavior.
Documentation-only changes require evidence that published artifacts updated
successfully.

## AI Guidance

- Check configuration and secrets separately from code.
- Treat migrations and async workers as deployment risks.
- Do not propose rollback when data changes are irreversible without mitigation.
- Record deployment lessons and incidents in Project Brain.

## Review Checklist

- Environment and version are known.
- Config, secrets, and dependencies are ready.
- Observability and health checks cover changed behavior.
- Rollout and recovery strategy are explicit.
- Post-deployment verification has owner and criteria.

## References

- Release Checklist: `release.md`
- DevOps Agent: `../agents/devops.md`
- Architecture Messaging: `../architecture/messaging.md`
