# Patterns

This Project Brain file records recurring approved solution approaches for
AI-assisted modernization.

## 2026-06-27 - Explicit Boundaries Over Hidden Lookup

- Context: Phase 2 anti-pattern standards repeatedly converged on explicit
  dependencies, ports, value objects, and composition roots.
- Decision: For side-effecting dependencies, use dependency injection and
  boundary ports rather than service locators, mutable singletons, or direct
  framework access from core logic.
- Rationale: Explicit boundaries improve testability, dependency direction,
  observability, and incremental replacement.
- Impact: Future code standards should use ports, repositories, gateways,
  value objects, and application services as preferred remediation patterns.
- Owner: Software Architect.
- Review trigger: Revisit when engineering principle standards are expanded.

## 2026-06-27 - Review Findings Need Routing Before Refactoring

- Context: Phase 3 added anti-pattern and smell indexes plus code and
  architecture review checklists.
- Decision: AI reviewers must classify maintainability findings before
  proposing fixes. Use the smell index for local maintainability issues and the
  anti-pattern index for design failures that affect boundaries, dependency
  direction, or hidden state.
- Rationale: Classification prevents mechanical refactors and helps reviewers
  select the smallest remediation that addresses the actual risk.
- Impact: Future review prompts and checklists should route findings through the
  indexes before recommending implementation changes.
- Owner: Reviewer.
- Review trigger: Revisit when prompt templates are expanded.

## 2026-06-27 - Principles Explain Review Findings

- Context: Phase 4 completed the first engineering principle pack.
- Decision: Review findings should cite both the concrete smell or anti-pattern
  and the engineering principle that explains the design trade-off when useful.
- Rationale: Smell and anti-pattern documents classify the issue; principles
  explain why the remediation is the right design move.
- Impact: Future checklists, prompts, and reviews should pair findings such as
  duplicate code with DRY, hidden side effects with dependency injection and
  fail fast, and feature envy with Tell, Don't Ask or Law of Demeter.
- Owner: Software Architect.
- Review trigger: Revisit when `engineering/README.md` is created.
