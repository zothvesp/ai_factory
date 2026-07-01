# Executive Glossary

## Philosophy

The executive glossary keeps strategic terms consistent across roles and phases.
It prevents governance discussions from using the same words differently.

## Terms

- AI-OS: The AI Engineering Operating System in `.ai/`.
- Phase: A bounded, reviewable release unit of AI-OS work.
- Standard: A production-quality document with rules, rationale, examples,
  AI guidance, checklist, and references.
- Project Brain: Persistent knowledge files for rules, decisions, risks, debt,
  lessons, roadmap, glossary, dependencies, and unresolved questions.
- Gate: A checklist condition that must be satisfied or explicitly accepted.
- Exception: A documented deviation from a rule with owner, rationale, risk,
  and review trigger.
- Modernization: Incremental improvement of a legacy system while preserving or
  intentionally changing behavior with evidence.
- Durable knowledge: Information future agents need beyond the current task.

## Rules

- Add terms when ambiguity affects decisions.
- Prefer domain or organizational language over tool-specific jargon.
- Link detailed domain terms to Project Brain glossary.
- Do not duplicate every technical term already defined in standards.

## Bad Example

```text
Done means mostly finished.
```

This conflicts with Definition of Done.

## Good Example

```text
Done means acceptance criteria, exit criteria, evidence gates, documentation,
Project Brain updates, commit, and push are complete.
```

## Review Checklist

- Term affects executive or governance decisions.
- Definition is concise and enforceable.
- Conflicts with other standards are resolved.
- Detailed domain terms route to Project Brain.
- Glossary changes are reflected where used.

## References

- Project Brain Glossary: `../brain/glossary.md`
- Definition of Done: `../checklists/definition-of-done.md`
