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
