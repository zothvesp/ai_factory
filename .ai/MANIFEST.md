# AI-OS Manifest

This manifest is the inventory and ownership map for the AI Engineering
Operating System. It records the purpose of each documentation domain, the
primary owner role, and the quality gates that apply before changes are accepted.

## Phase Status

### Phase 5 Scope

Phase 5 completes the engineering principles reference set:

- engineering principles index;
- GRASP;
- CUPID;
- Boy Scout Rule.

The engineering principles area now has a routing index and complete standards
for all principle files currently in the repository.

### Phase 4 Scope

Phase 4 completes the first engineering principle pack:

- DRY;
- KISS;
- YAGNI;
- SOLID;
- Dependency Injection;
- High Cohesion and Low Coupling;
- Composition over Inheritance;
- Fail Fast;
- Law of Demeter;
- Tell, Don't Ask.

These standards provide the design rationale behind the completed review pack
and are now usable as source-of-truth references during code and architecture
review.

### Phase 3 Scope

Phase 3 completes the first maintainability review pack:

- remaining smell standards for data clumps, dead code, feature envy, and
  shotgun surgery;
- anti-pattern and smell index pages with severity and routing guidance;
- production code review and architecture review checklists linked to completed
  standards.

The anti-pattern and smell areas now have enough complete guidance to support
consistent AI code review and architecture review findings.

### Phase 2 Scope

Phase 2 completes the first production-quality anti-pattern and smell standards:

- circular dependencies;
- service locator;
- magic values;
- tight coupling;
- singleton abuse;
- duplicate code;
- long method;
- god class;
- primitive obsession;
- hidden side effects.

These documents are now usable as review inputs for legacy Python
modernization. Remaining skeletal anti-pattern and smell files stay in the
modernization backlog until expanded with the same completion rules.

### Phase 1 Scope

Phase 1 establishes the governing spine of the AI-OS:

- root operating contract;
- architecture constitution;
- goal engineering framework;
- engineering loop model;
- AI role model;
- Project Brain operating rules;
- phase state, next task, and changelog.

Detailed expansion of every smell, anti-pattern, design pattern, framework
standard, and checklist is intentionally scheduled for later phases so each
document can be completed with examples and review criteria.

## Documentation Domains

| Domain | Path | Owner Role | Purpose | Required Gate |
| --- | --- | --- | --- | --- |
| Executive direction | `executive/` | CEO | Mission, vision, constraints, roadmap, success metrics, stakeholders, release strategy. | Business goal and constraint review |
| AI agents | `agents/` | CTO | Role definitions, authority, deliverables, escalation, quality gates. | Role clarity review |
| Architecture | `architecture/` | Software Architect | Constitution, architecture styles, ADRs, API, persistence, async, messaging, C4. | Architecture review |
| Goal engineering | `goals/` | Product Manager | Discovery, decomposition, acceptance, exit criteria, KPIs, constraints, risks. | Definition of Ready |
| Engineering loops | `loops/` | CTO | Reusable execution loops and exit criteria for delivery work. | Loop compliance review |
| Project Brain | `brain/` | Technical Writer | Persistent knowledge system for decisions, rules, risks, debt, patterns, and roadmap. | Knowledge update review |
| Product standards | `product/` | Product Manager | PRDs, personas, stories, use cases, NFRs, journeys, acceptance criteria. | Product review |
| Engineering principles | `engineering/` | Software Architect | DRY, KISS, SOLID, GRASP, CUPID, cohesion, coupling, DI, and related principles. | Principle-to-rule traceability |
| Clean code | `clean-code/` | Backend Engineer | Naming, functions, classes, comments, errors, formatting, testing, refactoring. | Code review |
| Python standards | `python/` | Backend Engineer | Python 3.13, typing, mypy, Ruff, pytest, logging, exceptions, async, SQLAlchemy, Pydantic. | Static analysis review |
| FastAPI standards | `fastapi/` | Backend Engineer | Routers, dependencies, auth, validation, errors, pagination, filtering, versioning, OpenAPI, middleware. | API review |
| Domain modeling | `domain/` | Software Architect | Bounded contexts, aggregates, entities, value objects, invariants, events, repositories. | Domain model review |
| Patterns | `patterns/` | Software Architect | Approved patterns and usage guidance. | Pattern fitness review |
| Anti-patterns | `anti-patterns/` | Reviewer | Prohibited designs, detection, remediation, and exceptions. | Refactoring review |
| Smells | `smells/` | Reviewer | Code smell detection, impact, remediation, and review guidance. | Maintainability review |
| Metrics | `metrics/` | QA Engineer | Quality, coverage, complexity, duplication, performance, maintainability. | Measurement review |
| Checklists | `checklists/` | QA Engineer | Ready, done, architecture, code, security, release, deployment review. | Checklist completeness review |
| Prompts | `prompts/` | AI Systems Engineer | Reusable prompts for analysis, domain discovery, review, security, performance, tests, docs. | Prompt safety review |

## Completion Rules

A document is complete when it contains:

- purpose and scope;
- binding rules;
- rationale and trade-offs;
- examples or decision guidance;
- AI guidance;
- review checklist;
- cross-links to related documents;
- references where useful.

Documents that only contain headings are not accepted as complete production
documents. Existing skeletal documents are tracked as modernization backlog until
expanded in a later phase.

## Completed Standards

| Standard | Path | Completed |
| --- | --- | --- |
| Architecture Constitution | `architecture/constitution.md` | Phase 1 |
| Goal Engineering | `goals/goal-engineering.md` | Phase 1 |
| Engineering Loops | `loops/README.md` | Phase 1 |
| AI Role Model | `agents/README.md` | Phase 1 |
| Project Brain Operating Model | `brain/README.md` | Phase 1 |
| Circular Dependencies | `anti-patterns/circular-dependencies.md` | Phase 2 |
| Service Locator | `anti-patterns/service-locator.md` | Phase 2 |
| Magic Values | `anti-patterns/magic-values.md` | Phase 2 |
| Tight Coupling | `anti-patterns/tight-coupling.md` | Phase 2 |
| Singleton Abuse | `anti-patterns/singleton-abuse.md` | Phase 2 |
| Duplicate Code | `smells/duplicate-code.md` | Phase 2 |
| Long Method | `smells/long-method.md` | Phase 2 |
| God Class | `smells/god-class.md` | Phase 2 |
| Primitive Obsession | `smells/primitive-obsession.md` | Phase 2 |
| Hidden Side Effects | `smells/hidden-side-effects.md` | Phase 2 |
| Data Clumps | `smells/data-clumps.md` | Phase 3 |
| Dead Code | `smells/dead-code.md` | Phase 3 |
| Feature Envy | `smells/feature-envy.md` | Phase 3 |
| Shotgun Surgery | `smells/shotgun-surgery.md` | Phase 3 |
| Anti-Pattern Review Index | `anti-patterns/README.md` | Phase 3 |
| Smell Review Index | `smells/README.md` | Phase 3 |
| Code Review Checklist | `checklists/code-review.md` | Phase 3 |
| Architecture Review Checklist | `checklists/architecture-review.md` | Phase 3 |
| DRY | `engineering/dry.md` | Phase 4 |
| KISS | `engineering/kiss.md` | Phase 4 |
| YAGNI | `engineering/yagni.md` | Phase 4 |
| SOLID | `engineering/solid.md` | Phase 4 |
| Dependency Injection | `engineering/dependency-injection.md` | Phase 4 |
| High Cohesion and Low Coupling | `engineering/high-cohesion-low-coupling.md` | Phase 4 |
| Composition over Inheritance | `engineering/composition-over-inheritance.md` | Phase 4 |
| Fail Fast | `engineering/fail-fast.md` | Phase 4 |
| Law of Demeter | `engineering/law-of-demeter.md` | Phase 4 |
| Tell, Don't Ask | `engineering/tell-dont-ask.md` | Phase 4 |
| Engineering Principles Index | `engineering/README.md` | Phase 5 |
| GRASP | `engineering/grasp.md` | Phase 5 |
| CUPID | `engineering/cupid.md` | Phase 5 |
| Boy Scout Rule | `engineering/boy-scout-rule.md` | Phase 5 |

## Change Control

- Architectural rule changes require updates to `architecture/constitution.md`
  and an ADR entry.
- Role authority changes require updates to `agents/README.md`.
- New knowledge categories require updates to `brain/README.md`.
- Any phase must update `PROJECT_STATE.md`, `NEXT_TASK.md`, and `CHANGELOG.md`.
