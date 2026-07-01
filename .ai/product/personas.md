# Personas

## Philosophy

Personas make product decisions accountable to real users, operators, buyers,
support teams, and maintainers. They prevent generic solutions that satisfy no
specific need.

## Rules

- A persona must define role, goals, responsibilities, pain points, constraints,
  success signals, and decision authority.
- Include operational and technical personas for modernization work.
- Do not invent demographic detail that does not affect product decisions.
- Link personas to journeys, use cases, features, and acceptance criteria.
- Revisit personas when discovery changes assumptions.

## Bad Example

```text
Persona: Admin user who wants things to work.
```

The persona is too vague to guide decisions.

## Good Example

```text
Persona: Backup Operations Engineer.
Goal: Verify nightly backup completion before business hours.
Pain: Failures require log digging across multiple hosts.
Constraint: Cannot expose database credentials in UI or logs.
```

## Decision Guidance

Create or update a persona when user goals, permissions, workflows, or success
criteria are unclear. Do not create personas for every role if existing
stakeholder definitions already guide the decision.

## AI Guidance

- Include maintainers and operators when internal quality affects outcomes.
- Treat persona assumptions as assumptions until validated.
- Use personas to resolve trade-offs, not to decorate documents.
- Update glossary and business rules when persona language reveals domain terms.

## Review Checklist

- Persona has concrete goals and pain.
- Constraints and authority are explicit.
- Persona links to real workflows.
- No irrelevant demographic filler is present.
- Assumptions are marked and reviewable.

## References

- User Journeys: `user-journeys.md`
- Use Cases: `use-cases.md`
- Glossary: `../brain/glossary.md`
