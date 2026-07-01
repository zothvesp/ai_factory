# Review Loop

## Purpose

The Review Loop provides independent critique before work is accepted. It finds
defects, risk, standards violations, and missing evidence.

## Entry Criteria

- Work product, goal, acceptance criteria, and relevant standards are available.
- Diff, documentation, tests, or design artifact is ready for review.
- Known limitations are disclosed.

## Activities

- Review against acceptance criteria and exit criteria.
- Apply code, architecture, security, product, metrics, and delivery checklists
  as triggered.
- Lead with findings ordered by severity.
- Distinguish required fixes from optional improvements.
- Identify missing Project Brain updates or documentation.

## Outputs

- Findings with severity and evidence.
- Approval or required changes.
- Open questions and residual risk.
- Follow-up debt or risk entries when accepted.

## Exit Criteria

- Blockers and high-risk findings are fixed or formally accepted.
- Residual risks are visible.
- Work can proceed to Done or the next loop.

## Checklist

- Findings cite concrete evidence.
- Standards and checklists are referenced.
- No subjective preference is treated as mandatory without risk.
- Missing tests or docs are identified.
- Approval states residual risk.

## References

- Review Prompt: `../prompts/review.md`
- Code Review: `../checklists/code-review.md`
- Architecture Review: `../checklists/architecture-review.md`
