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

## 2026-06-27 - FastAPI Is an HTTP Adapter

- Context: Phase 9 completed FastAPI standards for routers, dependencies,
  validation, errors, auth, pagination, filtering, OpenAPI, middleware, and
  versioning.
- Decision: FastAPI code must remain a transport boundary that composes
  dependencies, validates HTTP input, authorizes access, calls application
  services, and maps responses.
- Rationale: Keeping FastAPI thin prevents framework-driven architecture and
  preserves domain testability.
- Impact: Backend, Security, Reviewer, and Architect agents should use
  `fastapi/README.md` before changing HTTP behavior or API contracts.
- Owner: Software Architect.
- Review trigger: Revisit when API guidelines and architecture standards are
  expanded.

## 2026-06-28 - Domain Model Before Framework Model

- Context: Phase 10 completed domain modeling standards for boundaries,
  language, entities, value objects, aggregates, invariants, repositories,
  services, and events.
- Decision: Agents should identify domain language, invariants, and ownership
  before selecting Pydantic schemas, SQLAlchemy models, FastAPI routes, or
  storage structures.
- Rationale: Framework-first modeling scatters business rules and makes legacy
  modernization harder to verify.
- Impact: Backend and Architect agents should route business behavior questions
  through `domain/README.md` before changing framework or persistence code.
- Owner: Software Architect.
- Review trigger: Revisit when architecture style standards are expanded.

## 2026-06-28 - Structural Decisions Need Routing and Records

- Context: Phase 11 completed architecture standards for layers,
  ports/adapters, persistence, API contracts, async workflows, messaging,
  diagrams, and ADRs.
- Decision: Agents should route structural questions through
  `architecture/README.md` and record durable trade-offs in ADRs when a change
  affects dependency direction, data ownership, integration contracts,
  deployment behavior, or cross-team coordination.
- Rationale: Architecture drift usually starts as undocumented exceptions.
  Explicit routing and ADRs keep exceptions visible, reviewed, and reversible.
- Impact: Architect, Backend, Reviewer, Security, QA, and DevOps agents should
  cite the relevant architecture standard before accepting structural changes.
- Owner: Software Architect.
- Review trigger: Revisit when deployment, operations, or governance standards
  are expanded.

## 2026-06-28 - Clean Code Review Needs Specific Routing

- Context: Phase 12 completed clean-code standards for names, functions,
  classes, comments, errors, formatting, tests, refactoring, and heuristics.
- Decision: Agents should route local implementation findings through
  `clean-code/README.md` before recommending a fix, then cite the specific
  standard that explains the risk.
- Rationale: "Clean code" is too broad to be actionable without classification.
  Specific routing separates readability, testability, failure handling, and
  refactoring safety concerns.
- Impact: Backend, Reviewer, QA, and Architect agents should distinguish
  subjective preference from concrete maintainability risk.
- Owner: Reviewer.
- Review trigger: Revisit when prompt templates or automated review standards
  are expanded.

## 2026-06-30 - Patterns Must Answer a Real Design Force

- Context: Phase 13 completed standards for Adapter, Repository, Factory,
  Strategy, Decorator, Facade, Builder, Observer, and the pattern index.
- Decision: Agents should introduce a design pattern only after naming the
  recurring design force, boundary, variation, or construction complexity it
  solves.
- Rationale: Pattern-first design creates unnecessary indirection. Force-first
  design keeps patterns aligned with KISS, YAGNI, dependency direction, and
  testability.
- Impact: Architect, Backend, and Reviewer agents should route pattern choices
  through `patterns/README.md` and reject decorative pattern use.
- Owner: Software Architect.
- Review trigger: Revisit when prompt templates or automated architecture
  review standards are expanded.

## 2026-06-30 - Product Intent Gates Engineering Work

- Context: Phase 14 completed product standards for PRDs, features, epics,
  stories, personas, use cases, journeys, acceptance criteria, and NFRs.
- Decision: Agents should not begin implementation or architecture design for
  product-affecting work until product intent, constraints, stakeholders,
  acceptance criteria, and relevant NFRs are explicit.
- Rationale: Modernization work without product intent optimizes code while
  risking user value, compliance, supportability, and release quality.
- Impact: Product, Architect, Backend, QA, Reviewer, and Technical Writer agents
  should route readiness through `product/README.md` and Goal Engineering.
- Owner: Product Manager.
- Review trigger: Revisit when delivery checklists and prompt templates are
  expanded.

## 2026-06-30 - Metrics Are Signals, Not Goals

- Context: Phase 15 completed standards for quality, coverage, complexity,
  duplication, performance, maintainability, and the metrics index.
- Decision: Agents should interpret metrics as evidence tied to risk,
  thresholds, trends, and product or engineering goals rather than as isolated
  targets.
- Rationale: Metric chasing can weaken tests, create superficial refactors, or
  optimize low-value paths. Review quality improves when metrics are connected
  to outcomes and action.
- Impact: QA, Reviewer, Performance, Product, Architect, and DevOps agents
  should route metric findings through `metrics/README.md`.
- Owner: QA Engineer.
- Review trigger: Revisit when delivery checklists and CI standards are
  expanded.

## 2026-06-30 - Delivery Gates Require Evidence

- Context: Phase 16 completed delivery checklists for readiness, done, security,
  release, deployment, and the checklist index.
- Decision: Agents should treat checklist items as evidence gates and must
  report missing verification, accepted exceptions, and residual risk before
  closing work.
- Rationale: Checklists prevent phase closure based on activity alone and make
  safety, release, and deployment assumptions visible.
- Impact: All delivery agents should route phase closure through
  `checklists/README.md` and update Project Brain when gates reveal new debt,
  risks, or decisions.
- Owner: CTO.
- Review trigger: Revisit when prompt templates and CI standards are expanded.

## 2026-06-30 - Prompts Must Carry the Operating System

- Context: Phase 17 completed reusable prompt templates for analysis, review,
  rewrite, tests, domain discovery, API design, security review, performance
  review, and documentation generation.
- Decision: Prompt templates must require goals, scope, relevant standards,
  Project Brain updates, checklist gates, and evidence reporting.
- Rationale: A prompt that omits AI-OS governance lets future agents bypass the
  standards the repository exists to enforce.
- Impact: AI Systems Engineer and Technical Writer agents should route reusable
  prompt work through `prompts/README.md`.
- Owner: AI Systems Engineer.
- Review trigger: Revisit when agent orchestration or automation standards are
  expanded.
