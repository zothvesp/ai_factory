# Prompt Template Index

Prompt templates standardize how future AI agents use the AI-OS. They are
operating instructions, not shortcuts around engineering judgment.

## Use This Index

Use this page when assigning repeatable AI work: analysis, review, rewrite,
tests, domain discovery, API design, security review, performance review, or
documentation.

## Template Rules

- Every prompt must require a goal, scope, non-scope, constraints, risks,
  acceptance criteria, and exit criteria.
- Every prompt must reference relevant standards and checklists.
- Every prompt must require Project Brain updates when new durable knowledge is
  discovered.
- Prompts must prohibit placeholders, broad rewrites, invented facts, and
  unverified claims.
- Prompts must require evidence reporting: tests run, reviews performed, files
  changed, residual risk, and Git status when applicable.

## Template Catalog

| Template | Use When |
| --- | --- |
| [Analyze Module](analyze-module.md) | Understanding legacy code before design or rewrite. |
| [Review](review.md) | Performing code, architecture, documentation, or standards review. |
| [Rewrite Module](rewrite-module.md) | Modernizing implementation while preserving behavior. |
| [Write Tests](write-tests.md) | Adding characterization, unit, integration, or regression tests. |
| [Discover Domain](discover-domain.md) | Extracting business language, rules, and boundaries. |
| [Design API](design-api.md) | Designing or changing FastAPI/API contracts. |
| [Security Review](security-review.md) | Reviewing trust, auth, secrets, privacy, or dependency risk. |
| [Performance Review](performance-review.md) | Reviewing latency, throughput, resource use, or scalability. |
| [Generate Docs](generate-docs.md) | Creating or updating production documentation. |

## AI Guidance

- Use the smallest template that fits the task.
- Merge templates only when the task truly spans multiple modes.
- Do not omit readiness or done gates for speed.
- If a template conflicts with a higher-level standard, follow the higher-level
  standard and update the template in a later phase.

## References

- Goal Engineering: `../goals/goal-engineering.md`
- Checklists: `../checklists/README.md`
- Project Brain: `../brain/README.md`
- Architecture Constitution: `../architecture/constitution.md`
