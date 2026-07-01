# Definition of Ready

## Philosophy

Ready means the team has enough intent, context, constraints, and evidence to
start work without guessing. It prevents AI agents from turning ambiguity into
unreviewable output.

## Required Gates

- Goal statement is explicit and tied to product, risk, debt, or governance
  value.
- Scope and non-scope are defined.
- Stakeholders and responsible AI roles are named.
- Acceptance criteria and exit criteria are testable.
- Constraints, risks, assumptions, dependencies, and required loops are
  recorded.
- Relevant standards, Project Brain entries, and existing behavior are known.
- Security, privacy, migration, NFR, and release implications are identified.

## Bad Example

```text
Ready: Refactor the service to be cleaner.
```

This lacks outcome, scope, acceptance, and risk.

## Good Example

```text
Ready: Extract backup retry eligibility into a tested domain policy while
preserving current API behavior; non-scope is provider replacement; acceptance
requires characterization tests for timeout, credential, and quota failures.
```

## Decision Guidance

Start work when the missing context cannot materially change design or safety.
Pause when missing context affects user behavior, security, data, compatibility,
or acceptance.

## AI Guidance

- Ask for clarification only for readiness gaps that block safe progress.
- Mark assumptions explicitly when proceeding.
- Do not invent acceptance criteria for business decisions.
- Update Project Brain before starting if known rules or risks are missing.

## Review Checklist

- Goal, scope, non-scope, and value are clear.
- Acceptance and exit criteria are verifiable.
- Constraints, risks, and dependencies are recorded.
- Required standards and loops are identified.
- No critical unknown blocks safe work.

## References

- Goal Engineering: `../goals/goal-engineering.md`
- Product Standards: `../product/README.md`
- Risk Register: `../brain/risks.md`
