# Analysis Loop

## Purpose

The Analysis Loop turns unknown code, behavior, dependencies, or risks into
reviewable facts before design or implementation starts.

## Entry Criteria

- Goal, scope, non-scope, and acceptance criteria are known enough to analyze.
- Target files, workflows, documents, or systems are identified.
- Relevant standards and Project Brain entries are available.

## Activities

- Read source files, tests, configuration, documentation, and related standards.
- Identify responsibilities, inputs, outputs, dependencies, side effects,
  invariants, failure modes, and operational behavior.
- Separate facts from assumptions.
- Classify risks using architecture, clean-code, smell, anti-pattern, metrics,
  security, and product standards.
- Identify characterization tests or evidence needed before change.

## Outputs

- Responsibility summary.
- Dependency and data-flow notes.
- Risk-ranked findings.
- Assumptions and open questions.
- Recommended next loop and acceptance evidence.

## Exit Criteria

- The team knows what behavior must be preserved or changed.
- Major unknowns are either resolved or explicitly recorded.
- Next-step recommendations are scoped and testable.

## Checklist

- Facts cite concrete files or artifacts.
- Hidden side effects and dependencies are identified.
- Risks are classified by standard.
- Missing tests or evidence are listed.
- Project Brain updates are proposed for durable knowledge.

## References

- Analyze Module Prompt: `../prompts/analyze-module.md`
- Architecture Standards: `../architecture/README.md`
- Clean Code: `../clean-code/README.md`
