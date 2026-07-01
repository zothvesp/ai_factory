# Rewrite Module Prompt

## Purpose

Use this prompt to modernize or refactor a module while preserving intended
behavior.

## Template

```text
Act as Backend Engineer with Reviewer and QA Engineer standards.

Goal:
- Rewrite/refactor [module/path] to satisfy [goal] while preserving [behavior].

Inputs:
- Target files:
- Acceptance criteria:
- Behavior that must remain unchanged:
- Non-scope:
- Constraints:

Required process:
1. Analyze current behavior and tests before editing.
2. Add or identify characterization tests for risky behavior.
3. Choose the smallest safe refactor.
4. Preserve public contracts unless explicitly approved.
5. Apply relevant standards from architecture, clean-code, Python, domain, and
   patterns.
6. Run applicable checks and report evidence.
7. Update Project Brain for durable decisions, debt, risks, or lessons.

Output:
- Change summary.
- Behavior preserved or changed.
- Tests/checks run.
- Standards applied.
- Residual risk and follow-up.
```

## Bad Use

Combining refactor, behavior change, dependency replacement, and schema
migration in one unbounded rewrite.

## Review Checklist

- Behavior preservation is explicit.
- Tests protect risky paths.
- Scope is bounded.
- Public contracts are preserved or versioned.
- Evidence and residual risk are reported.

## References

- Refactoring: `../clean-code/refactoring.md`
- Definition of Done: `../checklists/definition-of-done.md`
- Python Standards: `../python/README.md`
