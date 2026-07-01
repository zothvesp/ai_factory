# Business Rules

Business rules are durable domain policies, calculations, validations,
eligibility decisions, state transitions, and behavioral constraints discovered
during modernization.

## Entry Format

```markdown
## YYYY-MM-DD - Rule Name

- Context: Where the rule was discovered.
- Rule: The binding business behavior.
- Source: Code, stakeholder, ticket, test, or document evidence.
- Scope: Bounded context, workflow, or feature affected.
- Exceptions: Approved exceptions or edge cases.
- Owner: Product Manager or domain owner.
- Review trigger: When the rule must be revisited.
```

## Rules

- Record business meaning, not implementation trivia.
- Mark unvalidated assumptions as unresolved questions.
- Link rules to domain standards, use cases, tests, or acceptance criteria.
- Update the entry when behavior changes.

## Bad Example

```text
The status column can be A.
```

## Good Example

```text
Rule: An account with active status and positive balance is eligible for backup
billing reconciliation.
Source: Legacy reconciliation job and finance operator workflow.
```

## AI Guidance

- Do not invent business rules from code names alone.
- Preserve uncertainty explicitly.
- Prefer ubiquitous language over database or API field names.

## Review Checklist

- Rule is observable and domain-level.
- Source evidence is named.
- Scope and owner are clear.
- Exceptions are captured.
- Tests or criteria can verify the rule.

## References

- Domain Standards: `../domain/README.md`
- Product Use Cases: `../product/use-cases.md`
