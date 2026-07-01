# Decisions

Decisions record durable product, engineering, architecture, release, or process
choices that future agents must understand.

## Entry Format

```markdown
## YYYY-MM-DD - Decision Title

- Context: Problem or decision point.
- Decision: Choice made.
- Alternatives: Meaningful options rejected.
- Rationale: Why this choice won.
- Impact: Consequences for future work.
- Owner: Accountable role.
- Review trigger: Event that should reopen the decision.
```

## Rules

- Use ADRs for architecture decisions with broad structural impact.
- Use this file for smaller durable decisions or ADR summaries.
- Record alternatives when they influenced the outcome.
- Do not record temporary guesses as decisions.

## Bad Example

```text
We decided to make it better.
```

## Good Example

```text
Decision: Prompt templates must require Project Brain updates.
Rationale: Future agents otherwise bypass persistent knowledge rules.
```

## AI Guidance

- Separate decision from rationale.
- Escalate missing authority before recording a binding decision.
- Link decisions to affected standards or roadmap entries.

## Review Checklist

- Decision is specific.
- Owner and authority are clear.
- Alternatives and rationale are captured.
- Impact is actionable.
- Review trigger exists.

## References

- ADRs: `../architecture/adrs.md`
- Executive Charter: `../executive/charter.md`
