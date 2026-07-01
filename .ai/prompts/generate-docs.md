# Generate Docs Prompt

## Purpose

Use this prompt to create or update production documentation without
placeholders, duplicated guidance, or unverified claims.

## Template

```text
Act as Technical Writer with support from the relevant specialist role.

Goal:
- Create/update documentation for [topic/artifact].

Inputs:
- Audience:
- Source files or standards:
- Required decisions or rules:
- Non-scope:

Required process:
1. Read source material before writing.
2. Identify audience, purpose, scope, rules, rationale, examples, checklists,
   AI guidance, and references.
3. Cross-link existing standards instead of duplicating them.
4. Avoid placeholders, stubs, invented facts, and marketing filler.
5. Update manifest, state, changelog, next task, and Project Brain when closing
   a phase.

Output:
- Documentation changes.
- Cross-links added.
- Evidence sources.
- Remaining gaps or review questions.
```

## Bad Use

Generating headings with "TODO", generic sections, or content that is not
usable by an experienced engineer.

## Review Checklist

- Document is complete for its audience.
- Rules include rationale and exceptions.
- Examples and checklists are actionable.
- Cross-links reduce duplication.
- Phase records are updated when required.

## References

- Manifest Completion Rules: `../MANIFEST.md`
- Project Brain: `../brain/README.md`
- Technical Writer: `../agents/tech-writer.md`
