# Deployment Loop

## Purpose

The Deployment Loop promotes changes into an environment safely, with rollout,
verification, observability, and recovery plans.

## Entry Criteria

- Release checklist is satisfied.
- Target environment, version, configuration, secrets, and dependencies are
  known.
- Migration and rollback or mitigation plans exist where relevant.

## Activities

- Confirm environment readiness.
- Apply migrations and configuration in the approved order.
- Deploy using the selected rollout strategy.
- Monitor health checks, logs, metrics, traces, alerts, and business signals.
- Execute post-deployment verification.
- Record incidents, lessons, and follow-up actions.

## Outputs

- Deployment record.
- Verification evidence.
- Incident or rollback notes if applicable.
- Project Brain lessons or risks.

## Exit Criteria

- Deployment is verified or rolled back/mitigated.
- Owners know residual issues.
- Operational knowledge is recorded.

## Checklist

- Version and environment are clear.
- Config and secrets are correct.
- Observability covers changed behavior.
- Recovery path is realistic.
- Post-deployment checks have passed or risk is accepted.

## References

- Deployment Checklist: `../checklists/deployment.md`
- Release Checklist: `../checklists/release.md`
- DevOps Agent: `../agents/devops.md`
