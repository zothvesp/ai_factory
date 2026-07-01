# Assumptions

## Purpose

Assumptions are uncertain statements accepted temporarily so work can proceed.
They must be visible, bounded, and reviewable.

## Rules

- Record assumptions separately from facts and decisions.
- Every material assumption needs impact, confidence, owner, and validation
  trigger.
- Do not assume business rules, security policy, data retention, or public API
  compatibility when wrong assumptions would be high impact.
- Convert validated assumptions into facts, rules, or decisions.

## Entry Format

```markdown
- Assumption:
- Impact if wrong:
- Confidence: Low, medium, or high.
- Owner:
- Validation method:
- Review trigger:
```

## Bad Example

```text
Assume users want this.
```

## Good Example

```text
Assumption: Backup operators need failure categories before retry controls.
Impact if wrong: UI work may solve the wrong workflow.
Validation: Review support tickets and operator interview notes.
```

## AI Guidance

- Proceed on low-risk assumptions only when clearly marked.
- Escalate assumptions that affect security, data, release, or acceptance.
- Update Project Brain when an assumption becomes durable knowledge.

## Review Checklist

- Assumption is explicit.
- Impact and confidence are stated.
- Owner and validation method exist.
- High-impact assumptions are not silently accepted.
- Resolved assumptions are converted to durable knowledge.

## References

- Definition of Ready: `../checklists/definition-of-ready.md`
- Unresolved Questions: `../brain/unresolved.md`
