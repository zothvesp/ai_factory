# Refactoring

## Philosophy

Refactoring changes structure without changing externally observable behavior.
It is a disciplined safety practice, not a broad rewrite license.

## Rules

- Define the behavior that must remain unchanged before editing.
- Add characterization tests when legacy behavior is unclear.
- Refactor in small steps that can be reviewed and reverted.
- Separate pure mechanical moves from behavior changes.
- Preserve public contracts unless a versioned change is approved.
- Remove dead code only when ownership and usage are verified.
- Update documentation and Project Brain when refactoring reveals durable rules,
  debt, or architectural decisions.

## Bad Example

```text
Rewrite the payment module, change database schema, rename public fields, and
switch providers in one pull request.
```

This combines refactoring, migration, API change, and vendor replacement.

## Good Example

```text
1. Add characterization tests for current payment retry behavior.
2. Extract payment gateway port.
3. Move provider SDK code into an adapter.
4. Keep API responses unchanged.
5. Commit and review the structural change before changing provider behavior.
```

The sequence protects behavior while improving structure.

## Decision Guidance

Refactor when current structure slows a required change, hides risk, blocks
tests, or violates a completed standard. Do not refactor merely because code is
old, stylistically different, or unfamiliar.

## AI Guidance

- State the preserved behavior before proposing refactoring.
- Prefer incremental extraction, naming, and boundary isolation over rewrites.
- Use smell and anti-pattern indexes to classify the reason for refactoring.
- Stop when the current goal is satisfied; leave unrelated improvements as
  owned follow-up tasks.

## Review Checklist

- Behavior-preservation strategy is explicit.
- Tests or characterization evidence exist for risky paths.
- Public contracts are unchanged or versioned.
- Diff is small enough to review coherently.
- Newly discovered debt or decisions are recorded.

## References

- Boy Scout Rule: `../engineering/boy-scout-rule.md`
- Smells: `../smells/README.md`
- Anti-Patterns: `../anti-patterns/README.md`
- ADRs: `../architecture/adrs.md`
