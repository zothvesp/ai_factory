# Lessons Learned

Lessons capture reusable learning from phases, incidents, reviews, failed
assumptions, and delivery friction.

## Entry Format

```markdown
## YYYY-MM-DD - Lesson Title

- Context: What happened.
- Lesson: What future agents should remember.
- Evidence: Review, test, incident, or phase outcome.
- Change: Standard, prompt, checklist, roadmap, or process update made.
- Owner: Role responsible for follow-through.
- Review trigger: When to revisit.
```

## Rules

- Lessons must be actionable for future work.
- Do not record blame.
- Convert recurring lessons into standards, prompts, checklists, or risks.
- Close the loop by linking to changes made.

## Bad Example

```text
Things were confusing.
```

## Good Example

```text
Lesson: External Git metadata in `/tmp` may disappear between sessions; agents
must be prepared to rebuild it from `origin/main`.
```

## AI Guidance

- Record lessons after surprises, blocked work, or repeated review findings.
- Prefer specific operating changes over generic observations.
- Keep lessons short and link to affected standards.

## Review Checklist

- Lesson is specific and reusable.
- Evidence is named.
- Follow-through action is clear.
- Owner and trigger exist.
- Lesson is not duplicating an existing rule.

## References

- Retrospective Loop: `../loops/retrospective.md`
- Technical Debt: `technical-debt.md`
