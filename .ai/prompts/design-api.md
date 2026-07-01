# Design API Prompt

## Purpose

Use this prompt to design or change HTTP/API contracts while preserving
architecture boundaries and product intent.

## Template

```text
Act as Product Manager, Software Architect, Backend Engineer, Security Engineer,
and QA Engineer.

Goal:
- Design API behavior for [capability].

Inputs:
- Product goal and acceptance criteria:
- Personas/use cases:
- Existing API contracts:
- NFRs and compatibility constraints:

Required process:
1. Start from use cases and acceptance criteria.
2. Define resources, operations, request/response models, errors, auth,
   pagination/filtering, versioning, and OpenAPI impact.
3. Keep FastAPI as transport adapter; do not leak ORM or domain internals.
4. Address security, privacy, compatibility, observability, and tests.
5. Record ADR or Project Brain updates for durable API decisions.

Output:
- API contract proposal.
- Error and auth model.
- Compatibility and versioning notes.
- Test and documentation plan.
- Risks and open questions.
```

## Bad Use

Designing endpoints from database tables instead of user workflows and domain
boundaries.

## Review Checklist

- API traces to product use cases.
- Request/response models are stable and explicit.
- Auth, errors, pagination, filtering, and versioning are addressed.
- Domain and persistence internals do not leak.
- Tests and OpenAPI documentation are planned.

## References

- FastAPI Standards: `../fastapi/README.md`
- API Guidelines: `../architecture/api-guidelines.md`
- Product Use Cases: `../product/use-cases.md`
