# Project Brain

The Project Brain is the persistent memory of the AI Engineering Operating
System. It stores knowledge that future agents need in order to make consistent
decisions without rediscovering context from chat history or source inspection.

## Purpose

The Project Brain preserves:

- business rules;
- architecture decisions;
- glossary terms;
- approved patterns;
- prohibited anti-patterns;
- lessons learned;
- technical debt;
- dependencies;
- risks;
- roadmap context;
- unresolved questions.

## Operating Rule

Every task must update the Project Brain when it discovers durable knowledge,
changes a decision, accepts a risk, introduces debt, resolves uncertainty, or
learns a lesson that would matter to a future agent.

No task is complete until either:

- Project Brain was updated; or
- the agent states that no durable knowledge changed.

## Source Files

| File | Purpose |
| --- | --- |
| `business-rules.md` | Domain rules, policies, calculations, and behavioral constraints. |
| `architecture.md` | Current architecture facts, boundaries, integration patterns, and system maps. |
| `decisions.md` | Architecture and product decisions that do not yet warrant a full ADR or summarize ADR outcomes. |
| `glossary.md` | Shared vocabulary and domain language. |
| `patterns.md` | Approved recurring solutions and when to use them. |
| `anti-patterns.md` | Recurring prohibited practices and remediation guidance. |
| `lessons.md` | Retrospective findings and incident learning. |
| `technical-debt.md` | Known debt, owner, risk, and repayment trigger. |
| `dependencies.md` | External services, libraries, runtime dependencies, and ownership. |
| `risks.md` | Active risks, likelihood, impact, mitigation, and owner. |
| `roadmap.md` | Sequencing context and planned modernization phases. |
| `unresolved.md` | Questions that block or influence future decisions. |

Some listed files may need to be created during later phases. When a category is
introduced, add it to this README and the manifest.

## Entry Format

Use short, dated entries:

```markdown
## YYYY-MM-DD - Short Title

- Context: What was discovered or decided.
- Decision: What is now considered true or required.
- Rationale: Why this is the right current position.
- Impact: What future agents must do differently.
- Owner: Responsible role.
- Review trigger: When this entry should be revisited.
```

## Quality Rules

- Store facts, decisions, and risks, not conversational summaries.
- Prefer one authoritative entry over duplicated fragments across files.
- Link to ADRs, standards, or checklists instead of copying long policy.
- Mark assumptions explicitly.
- Give every risk and debt item an owner and review trigger.
- Remove or revise obsolete entries during retrospectives.

## AI Guidance

- Read the relevant Project Brain files before proposing architecture or product
  changes.
- If a source file contradicts Project Brain, treat it as a finding and resolve
  through analysis, not guesswork.
- Do not hide unresolved questions in final summaries. Record them in
  `unresolved.md`.
- When completing a phase, update roadmap and lessons if sequencing or process
  knowledge changed.
