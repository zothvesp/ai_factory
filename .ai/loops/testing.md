# Testing Loop

## Purpose

The Testing Loop proves behavior, protects refactoring, and supplies evidence
for acceptance and release decisions.

## Entry Criteria

- Behavior or risk to verify is defined.
- Test level is selected: unit, integration, contract, migration, performance,
  security, or characterization.
- Required test data and dependencies are available.

## Activities

- Map acceptance criteria and risks to tests.
- Add focused tests for success, failure, edge, and permission paths.
- Use deterministic fixtures and avoid real external services unless required.
- Run targeted checks first, then broader checks when risk warrants it.
- Interpret coverage and failures with context.

## Outputs

- Test cases and fixtures.
- Test command results.
- Coverage or gap notes.
- Defects or follow-up risks.

## Exit Criteria

- Critical behavior has evidence.
- Tests are deterministic and meaningful.
- Unverified paths are reported with risk and owner.

## Checklist

- Tests verify observable behavior.
- Failure paths are covered where important.
- Assertions are meaningful.
- Flaky or superficial tests are avoided.
- Evidence is reported accurately.

## References

- pytest: `../python/pytest.md`
- Testing Standard: `../clean-code/testing.md`
- Coverage Metrics: `../metrics/coverage.md`
