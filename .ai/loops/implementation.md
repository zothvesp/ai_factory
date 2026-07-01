# Implementation Loop

## Purpose

The Implementation Loop changes code or documentation while preserving agreed
behavior, standards, and reviewability.

## Entry Criteria

- Definition of Ready is satisfied.
- Design or analysis is sufficient for the risk level.
- Acceptance criteria and tests to run are known.

## Activities

- Make the smallest coherent change that satisfies the goal.
- Follow Python, FastAPI, domain, architecture, clean-code, and pattern
  standards as applicable.
- Add or update tests alongside behavior changes.
- Keep unrelated refactors out of scope.
- Update documentation and Project Brain when durable knowledge changes.

## Outputs

- Changed files.
- Tests or evidence.
- Documentation and Project Brain updates.
- Residual risk or follow-up debt.

## Exit Criteria

- Acceptance criteria are satisfied.
- Required checks are run or limitations are reported.
- Diff is reviewable and scoped.

## Checklist

- Scope matches the goal.
- Behavior changes are intentional.
- Tests cover meaningful risk.
- Standards violations are absent or accepted.
- Git status is understood before handoff.

## References

- Definition of Ready: `../checklists/definition-of-ready.md`
- Python Standards: `../python/README.md`
- Definition of Done: `../checklists/definition-of-done.md`
