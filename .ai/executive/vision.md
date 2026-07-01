# Vision

## Philosophy

The vision describes the future state the AI-OS is building toward. It guides
roadmap decisions and prevents local standards from drifting apart.

## Vision Statement

Future AI agents should be able to enter a legacy modernization effort, discover
goals and domain rules, select the right loops and standards, perform bounded
work, update persistent knowledge, pass review gates, and hand off evidence
without relying on undocumented human memory.

## Rules

- The AI-OS must be coherent across product, architecture, code, review,
  security, performance, documentation, release, and governance.
- Knowledge must become easier to reuse over time.
- Agent outputs must be traceable to goals, standards, evidence, and decisions.
- The system must support incremental modernization rather than broad rewrites.

## Bad Example

```text
Each agent invents its own process for every task.
```

## Good Example

```text
Agents use Goal Engineering, a relevant loop, standards indexes, checklists, and
Project Brain updates for every phase.
```

## Decision Guidance

Prioritize work that improves coherence, traceability, and future agent
execution. Avoid isolated documents that do not connect to the operating model.

## AI Guidance

- Cross-link standards aggressively where it prevents drift.
- Record decisions when exceptions are allowed.
- Keep future agent usability as a primary quality criterion.

## Review Checklist

- Change improves coherence or reuse.
- Traceability is clear.
- Future agents can apply the guidance.
- Incremental modernization remains supported.
- Exceptions are visible.

## References

- Mission: `mission.md`
- Manifest: `../MANIFEST.md`
