# Design Loop

## Purpose

The Design Loop selects a solution shape before implementation. It evaluates
options, trade-offs, constraints, and testability.

## Entry Criteria

- Analysis has identified current behavior and risks.
- Goal, constraints, acceptance criteria, and relevant NFRs are known.
- Architecture Constitution and relevant standards are available.

## Activities

- Define design forces: domain rules, boundary ownership, dependencies,
  performance, security, operations, and maintainability.
- Compare viable options and trade-offs.
- Select the smallest design that satisfies the goal and constraints.
- Identify affected tests, docs, migrations, APIs, and Project Brain entries.
- Decide whether an ADR is required.

## Outputs

- Chosen design and rejected alternatives.
- Trade-off and risk notes.
- Test and documentation plan.
- ADR or decision record when durable.

## Exit Criteria

- The selected design satisfies the goal without avoidable overengineering.
- Risks, dependencies, and exceptions are visible.
- Implementation can begin with clear boundaries and evidence expectations.

## Checklist

- Design follows dependency direction.
- Options and trade-offs are explicit.
- YAGNI and KISS are considered.
- Tests and rollout implications are identified.
- Durable decisions are recorded.

## References

- Architecture Constitution: `../architecture/constitution.md`
- Patterns: `../patterns/README.md`
- ADRs: `../architecture/adrs.md`
