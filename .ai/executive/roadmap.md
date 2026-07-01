# Roadmap

## Philosophy

The roadmap sequences AI-OS growth into reviewable phases. It balances strategic
coverage with bounded delivery and prevents endless generation.

## Roadmap Rules

- Roadmap items must be outcome-oriented and phase-sized.
- Each phase must have entry criteria, exit criteria, completed artifacts,
  Project Brain updates, commit, and push.
- Roadmap priority follows risk: governance, roles, architecture, product,
  implementation, review, metrics, prompts, operations, and knowledge gaps.
- The roadmap must be updated when a phase reveals higher-risk debt.

## Current Roadmap Pattern

1. Complete one standards area fully.
2. Add or update the area index.
3. Update manifest, state, next task, changelog, and Project Brain.
4. Commit and push.
5. Move to the next highest-value skeletal area.

## Bad Example

```text
Next: finish all docs.
```

This cannot be reviewed or sequenced.

## Good Example

```text
Phase 19: expand loop detail pages for analysis, design, implementation,
testing, review, deployment, documentation, and retrospective.
```

## Review Checklist

- Roadmap item is bounded and valuable.
- Dependencies are clear.
- Risk and priority are justified.
- Exit criteria are objective.
- Next task is updated after phase closure.

## References

- Next Task: `../NEXT_TASK.md`
- Project State: `../PROJECT_STATE.md`
