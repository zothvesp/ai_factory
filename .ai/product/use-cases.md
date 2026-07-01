# Use Cases

## Philosophy

Use cases describe how an actor interacts with the system to achieve a goal.
They clarify main flows, alternate flows, failure paths, permissions, and system
responsibilities before implementation.

## Rules

- Define actor, goal, trigger, preconditions, main flow, alternate flows,
  failure flows, postconditions, and acceptance evidence.
- Keep use cases technology-neutral unless technology is a constraint.
- Include authorization, audit, error, and recovery behavior where relevant.
- Link to stories, NFRs, API standards, and domain rules.
- Do not hide business rules inside vague flow steps.

## Bad Example

```text
User clicks button and system handles it.
```

The use case does not describe system responsibilities or outcomes.

## Good Example

```text
Actor: Backup Operations Engineer.
Trigger: A nightly backup job fails.
Main flow: View failed job, inspect categorized reason, retry eligible job,
receive retry result, audit entry is recorded.
Failure flow: Retry is blocked when credentials are invalid.
```

## Decision Guidance

Use a use case when interaction detail matters. Use a journey when the
end-to-end experience across stages matters. Use acceptance criteria to convert
flows into completion checks.

## AI Guidance

- Capture negative and recovery flows early.
- Keep actor intent separate from UI implementation.
- Extract business rules into Project Brain when durable.
- Use cases should inform API, domain, and test design.

## Review Checklist

- Actor, trigger, and goal are clear.
- Preconditions and postconditions are explicit.
- Main, alternate, and failure flows are covered.
- Permissions and audit needs are addressed.
- Criteria can be tested or reviewed.

## References

- Acceptance Criteria: `acceptance-criteria.md`
- Domain Rules: `../brain/business-rules.md`
- API Guidelines: `../architecture/api-guidelines.md`
