# Risks

Risks capture uncertain events that could affect modernization quality, delivery,
security, operations, or maintainability.

## Risk Entry Format

```markdown
## YYYY-MM-DD - Short Title

- Risk: What might go wrong.
- Likelihood: Low, medium, or high.
- Impact: Low, medium, or high.
- Mitigation: Action that reduces likelihood or impact.
- Owner: Responsible role.
- Trigger: Signal that the risk is becoming real.
- Status: Open, mitigated, accepted, or closed.
```

## 2026-06-27 - Standards Volume Outpaces Review

- Risk: The AI-OS contains many standards categories, and generating too much at
  once could create shallow or contradictory guidance.
- Likelihood: High.
- Impact: High.
- Mitigation: Work in bounded phases, complete a small set of documents fully,
  update manifest and state, then stop for review.
- Owner: CTO.
- Trigger: A phase attempts to complete broad categories without examples,
  review checklists, and cross-links.
- Status: Mitigated for Phase 4.

## 2026-06-27 - Legacy Application Code Mixed With AI-OS

- Risk: The repository contains legacy Python application files alongside the
  AI-OS documentation, which may blur whether the repository is a handbook,
  application codebase, or modernization target.
- Likelihood: Medium.
- Impact: Medium.
- Mitigation: Record the question in project state and decide whether to split
  AI-OS into a documentation-only repository.
- Owner: CEO.
- Trigger: Future phases need repository-level automation, packaging, or
  releases and cannot distinguish documentation product from application code.
- Status: Open.
