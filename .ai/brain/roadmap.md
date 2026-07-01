# Roadmap Knowledge

Roadmap knowledge records sequencing context, planned phases, priority reasons,
dependencies, and deferred work.

## Entry Format

```markdown
## YYYY-MM-DD - Roadmap Item

- Objective: Outcome to achieve.
- Rationale: Why this should be sequenced here.
- Dependencies: Required prior work.
- Scope: Included work.
- Non-scope: Deferred work.
- Exit criteria: How completion is known.
- Owner: Accountable role.
- Status: Proposed, active, done, deferred, or blocked.
```

## Rules

- Roadmap items must be bounded and reviewable.
- Priority must cite risk, dependency, stakeholder value, or mission impact.
- Update roadmap entries when `NEXT_TASK.md` changes materially.
- Do not use roadmap entries as vague wish lists.

## Bad Example

```text
Finish documentation someday.
```

## Good Example

```text
Objective: Complete Goal Engineering subpages after Project Brain subpages.
Rationale: The root goal framework exists, but supporting goal templates remain
skeletal and should be usable by future agents.
```

## AI Guidance

- Keep roadmap entries smaller than broad programs.
- Record why a phase was chosen.
- Move blocked items to unresolved questions when a decision is missing.

## Review Checklist

- Objective and exit criteria are clear.
- Dependencies and non-scope are explicit.
- Status is current.
- Priority has rationale.
- Next-task alignment is maintained.

## References

- Executive Roadmap: `../executive/roadmap.md`
- Next Task: `../NEXT_TASK.md`
