# Delivery Checklist Index

Delivery checklists convert AI-OS standards into phase gates. They are used to
decide whether work is ready to start, safe to review, complete, releasable, and
deployable.

## Use This Index

Use this page whenever a task enters or exits a loop, asks for review, changes a
release, or affects production operations.

## Severity Model

| Severity | Meaning | Required Action |
| --- | --- | --- |
| Blocker | Gate is missing a mandatory goal, security, test, architecture, release, or deployment condition. | Stop until fixed or formally accepted. |
| High | Gate evidence is incomplete for a high-risk change. | Fix before phase closure. |
| Medium | Gate has minor missing context with bounded risk. | Add context or record follow-up. |
| Low | Formatting or cross-reference issue. | Fix opportunistically. |

## Checklist Catalog

| Checklist | Use When |
| --- | --- |
| [Definition of Ready](definition-of-ready.md) | Before analysis, design, or implementation starts. |
| [Definition of Done](definition-of-done.md) | Before a task or phase is closed. |
| [Code Review](code-review.md) | Reviewing implementation changes. |
| [Architecture Review](architecture-review.md) | Reviewing structural or boundary changes. |
| [Security Review](security-review.md) | Reviewing trust, auth, privacy, secrets, or dependency risk. |
| [Release](release.md) | Preparing a version, migration, or public change. |
| [Deployment](deployment.md) | Promoting changes into an environment. |

## AI Guidance

- Treat checklists as evidence gates, not paperwork.
- Cite missing checklist items in review findings.
- Do not mark work done when a mandatory gate is unverified.
- Record accepted exceptions as risks, debt, ADRs, or release notes.

## References

- Goal Engineering: `../goals/goal-engineering.md`
- Product Standards: `../product/README.md`
- Metrics Standards: `../metrics/README.md`
- Project Brain: `../brain/README.md`
