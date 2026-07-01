# Review Prompt

## Purpose

Use this prompt for code, architecture, documentation, product, security, or
release review.

## Template

```text
Act as Reviewer with support from the relevant specialist roles.

Goal:
- Review [change/artifact] against [goal/acceptance criteria].

Inputs:
- Changed files or artifact:
- Goal and acceptance criteria:
- Relevant standards:
- Risk areas:

Required process:
1. Read the changed artifact and relevant standards.
2. Verify the change against acceptance criteria and exit criteria.
3. Lead with findings ordered by severity.
4. Tie each finding to concrete evidence and a standard.
5. Distinguish required fixes from optional improvements.
6. Identify missing tests, documentation, Project Brain updates, or release
   evidence.

Output:
- Findings first, ordered by severity.
- Open questions or assumptions.
- Required follow-up.
- Residual risk if no issues are found.
```

## Bad Use

Returning praise, summaries, or style preferences before identifying risks.

## Review Checklist

- Findings are specific and actionable.
- Severity is justified.
- File, behavior, or artifact references are included.
- Standards and checklists are cited.
- No unverified claims are made.

## References

- Code Review: `../checklists/code-review.md`
- Architecture Review: `../checklists/architecture-review.md`
- Definition of Done: `../checklists/definition-of-done.md`
