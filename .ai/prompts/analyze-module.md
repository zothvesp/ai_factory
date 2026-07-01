# Analyze Module Prompt

## Purpose

Use this prompt to understand a legacy module before changing design,
dependencies, tests, or behavior.

## Template

```text
Act as Backend Engineer, Reviewer, and Software Architect.

Goal:
- Analyze [module/path] to explain responsibilities, dependencies, risks, and
  safe modernization options.

Inputs:
- Target files:
- Product or engineering goal:
- Known constraints:
- Non-scope:

Required process:
1. Read the target files and nearby tests before proposing changes.
2. Identify public behavior, side effects, data flow, dependencies, and failure
   modes.
3. Classify findings using relevant AI-OS standards:
   - architecture/README.md
   - clean-code/README.md
   - smells/README.md
   - anti-patterns/README.md
   - metrics/README.md
4. Separate facts from assumptions.
5. Identify missing tests or characterization needs.
6. Update Project Brain only if durable rules, risks, debt, glossary terms, or
   decisions are discovered.

Output:
- Responsibility summary.
- Dependency and boundary map.
- Behavior and side-effect inventory.
- Risk-ranked findings.
- Recommended next steps with acceptance criteria.
- Evidence reviewed and remaining unknowns.
```

## Bad Use

Using this prompt to rewrite code before understanding current behavior.

## Review Checklist

- Analysis cites concrete files and behavior.
- Findings are classified by standards.
- Assumptions are marked.
- Recommended changes are scoped and testable.
- Project Brain updates are proposed when durable knowledge appears.

## References

- Analysis Loop: `../loops/analysis.md`
- Architecture: `../architecture/README.md`
- Clean Code: `../clean-code/README.md`
