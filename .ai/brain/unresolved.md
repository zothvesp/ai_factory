# Unresolved Questions

Unresolved questions capture unknowns that affect future decisions, safety,
scope, or sequencing.

## Entry Format

```markdown
## YYYY-MM-DD - Question

- Question: What is unknown.
- Context: Why it matters.
- Impact: What decisions or work it affects.
- Owner: Role responsible for resolution.
- Needed evidence: Information required.
- Due or trigger: When it must be resolved.
- Status: Open, answered, deferred, or obsolete.
```

## Rules

- Record only questions that matter to future work.
- Do not leave blockers hidden in chat history.
- Convert answered questions into decisions, rules, risks, or roadmap updates.
- Close obsolete questions with reason.

## Bad Example

```text
Need to know more.
```

## Good Example

```text
Question: Should AI-OS documentation be split from legacy application source?
Impact: Affects repository automation, release strategy, and ownership.
Owner: CEO.
```

## AI Guidance

- Use unresolved questions when authority or evidence is missing.
- Do not block on questions that do not affect the current phase.
- Revisit unresolved questions during planning and retrospective loops.

## Review Checklist

- Question is specific.
- Impact is clear.
- Owner and needed evidence are named.
- Status is current.
- Answered questions are converted into durable knowledge.

## References

- Retrospective Loop: `../loops/retrospective.md`
- Decisions: `decisions.md`
