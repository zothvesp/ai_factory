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

## 2026-06-27 - Principle Routing Is a First-Class Review Tool

- Context: Phase 5 created `engineering/README.md` and completed GRASP, CUPID,
  and Boy Scout Rule.
- Decision: Agents should use the engineering principles index when a design
  question spans multiple principles or when principles appear to conflict.
- Rationale: The index prevents principle shopping and gives agents a consistent
  way to balance KISS, YAGNI, SOLID, DRY, GRASP, CUPID, and Boy Scout Rule.
- Impact: Future role playbooks and prompts should reference
  `engineering/README.md` for design trade-off routing.
- Owner: Software Architect.
- Review trigger: Revisit when role playbooks are expanded.

## 2026-06-27 - Role Playbooks Own Operating Behavior

- Context: Phase 6 completed individual AI role playbooks.
- Decision: Agents should use `agents/README.md` for cross-role authority and
  the individual role file for execution behavior, checklists, escalation, and
  deliverables.
- Rationale: Central role definitions prevent authority drift, while individual
  playbooks make each role actionable during real tasks.
- Impact: Future prompts and workflows should reference role playbooks before
  assigning work or accepting a phase gate.
- Owner: CTO.
- Review trigger: Revisit when prompt templates or agent orchestration standards
  are expanded.

## 2026-06-27 - Python Modernization Requires Typed, Tested, Observable Code

- Context: Phase 7 completed Python implementation standards for language
  baseline, typing, mypy, Ruff, pytest, exceptions, logging, and AsyncIO.
- Decision: Backend modernization should treat type contracts, deterministic
  tests, explicit failure handling, safe logs, and honest async as one connected
  implementation quality model.
- Rationale: Legacy Python risk usually appears where dynamic data, hidden side
  effects, broad exceptions, weak tests, and blocking I/O overlap.
- Impact: Backend, QA, Reviewer, Security, and DevOps agents should use the
  Python standards together during implementation and review.
- Owner: Backend Engineer.
- Review trigger: Revisit when `python/README.md` is created.

## 2026-06-27 - Python Frameworks Stay at Boundaries

- Context: Phase 8 completed Python standards for Pydantic v2, SQLAlchemy 2.x,
  FastAPI usage, pathlib, and the Python standards index.
- Decision: Pydantic, FastAPI, SQLAlchemy, and filesystem access are boundary or
  infrastructure concerns unless explicitly mapped into domain value objects,
  commands, repositories, or application services.
- Rationale: Keeping framework concerns at the edge preserves testability,
  dependency direction, and domain clarity.
- Impact: Backend and Architect agents should route boundary model questions
  through `python/README.md` before changing API, persistence, or filesystem
  code.
- Owner: Software Architect.
- Review trigger: Revisit when FastAPI and persistence architecture standards
  are expanded.
