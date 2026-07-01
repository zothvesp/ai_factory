# Write Tests Prompt

## Purpose

Use this prompt to add meaningful tests for current behavior, new behavior,
regressions, or refactoring safety.

## Template

```text
Act as QA Engineer and Backend Engineer.

Goal:
- Add tests for [behavior/risk] in [module/path].

Inputs:
- Acceptance criteria:
- Current tests:
- Risk areas:
- Test level required: unit, integration, contract, migration, or
  characterization.

Required process:
1. Read behavior and existing tests before adding tests.
2. Choose the lowest test level that proves the risk.
3. Cover success, failure, edge, and permission paths where relevant.
4. Avoid brittle assertions against private implementation.
5. Use pytest and repository test patterns.
6. Run targeted tests and report output.

Output:
- Tests added or changed.
- Behavior covered.
- Test command and result.
- Remaining coverage gaps.
```

## Bad Use

Adding tests that assert `True`, only exercise mocks, or encode implementation
details that should be free to change.

## Review Checklist

- Tests verify observable behavior.
- Failure paths are covered where important.
- Tests are deterministic.
- Assertions would catch real regressions.
- Coverage gaps are explicit.

## References

- Testing: `../clean-code/testing.md`
- pytest: `../python/pytest.md`
- Coverage Metrics: `../metrics/coverage.md`
