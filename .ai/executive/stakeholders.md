# Stakeholders

## Philosophy

Stakeholders are people or roles affected by AI-OS decisions, modernization
outcomes, risks, or release timing. Clear stakeholder mapping prevents hidden
requirements and late surprises.

## Stakeholder Classes

- Executive sponsors: mission, investment, risk acceptance.
- Product stakeholders: user value, roadmap, acceptance criteria.
- Engineering stakeholders: architecture, maintainability, implementation.
- Operations stakeholders: deployment, observability, support, incident
  response.
- Security and compliance stakeholders: trust, privacy, policy, audit.
- Users and operators: workflows, usability, reliability, documentation.
- Future agents: durable knowledge, standards, prompts, and handoff evidence.

## Rules

- Every significant goal must identify affected stakeholders.
- Risk acceptance must come from the stakeholder with authority.
- Stakeholder needs must be translated into acceptance criteria, NFRs, or
  constraints.
- Project Brain must record durable stakeholder rules or glossary terms.

## Bad Example

```text
The engineering agent decides release timing without product or operations.
```

## Good Example

```text
Release timing is approved after Product confirms user impact, DevOps confirms
deployment readiness, and Security accepts residual auth risk.
```

## Review Checklist

- Stakeholders are named by role.
- Authority for decisions and risk is clear.
- Needs map to criteria or constraints.
- Operators and future maintainers are considered.
- Durable stakeholder knowledge is recorded.

## References

- Product Personas: `../product/personas.md`
- Role Model: `../agents/README.md`
