# Discover Domain Prompt

## Purpose

Use this prompt to extract domain language, rules, boundaries, invariants, and
events from legacy code, stakeholders, tickets, or documentation.

## Template

```text
Act as Product Manager and Software Architect.

Goal:
- Discover domain concepts and rules for [area/workflow].

Inputs:
- Source files or documents:
- Stakeholders/personas:
- Known business questions:
- Non-scope:

Required process:
1. Identify nouns, verbs, rules, states, and events.
2. Separate domain concepts from framework, database, and UI artifacts.
3. Propose bounded contexts, aggregates, value objects, invariants, services,
   repositories, and events only when evidence supports them.
4. Mark assumptions and unresolved questions.
5. Update Project Brain glossary, business rules, risks, and decisions when
   durable knowledge is discovered.

Output:
- Ubiquitous language candidates.
- Business rules and invariants.
- Boundary and ownership questions.
- Suggested domain model slices.
- Project Brain updates.
```

## Bad Use

Treating database tables or API schemas as the domain model without validating
business meaning.

## Review Checklist

- Domain language is separated from implementation language.
- Rules and invariants cite evidence.
- Assumptions are explicit.
- Bounded contexts are not overclaimed.
- Project Brain updates are identified.

## References

- Domain Standards: `../domain/README.md`
- Product Personas: `../product/personas.md`
- Project Brain: `../brain/README.md`
