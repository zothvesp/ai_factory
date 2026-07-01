# Exit Criteria

## Purpose

Exit criteria define when a task, loop, phase, or release can stop. They prevent
premature closure and endless continuation.

## Rules

- Exit criteria must be observable and tied to the goal.
- Include required artifacts, tests, reviews, documentation, Project Brain
  updates, and Git push when applicable.
- State what evidence is required and who can accept exceptions.
- Do not use effort spent as exit evidence.

## Bad Example

```text
Stop when it feels complete.
```

## Good Example

```text
Exit: All selected goal support pages are complete, placeholder scan is clean,
manifest/state/next/changelog/Project Brain are updated, commit is pushed, and
residual risks are reported.
```

## Decision Guidance

Use stricter criteria for high-risk code, security, data, release, and
architecture work. Use lightweight criteria for small documentation-only changes,
but still require state and evidence.

## AI Guidance

- Check exit criteria before final response.
- Report anything not verified.
- Do not mark work done just because a phase budget is exhausted.

## Review Checklist

- Criteria are observable.
- Evidence and owner are clear.
- Exceptions are documented.
- Criteria match task risk.
- Done state includes required handoff updates.

## References

- Definition of Done: `../checklists/definition-of-done.md`
- Release Strategy: `../executive/release-strategy.md`
