# Release Strategy

## Philosophy

The AI-OS is released as a sequence of pushed, reviewable documentation phases.
Each release must leave the repository more trustworthy for future agents.

## Rules

- Each phase is a release unit.
- Every release must update `README`, `MANIFEST`, `PROJECT_STATE`, `NEXT_TASK`,
  `CHANGELOG`, and Project Brain where relevant.
- Release notes must state completed scope and next priority.
- Pushed commits are required for durable handoff.
- Incomplete documents must remain unlisted as completed standards.
- Backward-incompatible governance changes require explicit changelog notes and
  owner approval.

## Bad Example

```text
Edit several unrelated standards and leave them uncommitted.
```

## Good Example

```text
Complete the metrics standards pack, update phase records, commit as one phase,
and push to `origin/main`.
```

## Decision Guidance

Use one commit per coherent phase unless a safety fix must be pushed
separately. Avoid mixing unrelated standards areas in one release.

## AI Guidance

- Verify `git status` before and after phase commits.
- Push every completed phase.
- Report commit hash and residual risk.
- Do not mark skeletal documents complete.

## Review Checklist

- Phase scope is coherent.
- Release records are updated.
- Commit and push are complete.
- Completed standards are listed in manifest.
- Next task is actionable.

## References

- Release Checklist: `../checklists/release.md`
- Changelog: `../CHANGELOG.md`
