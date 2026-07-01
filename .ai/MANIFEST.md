# AI-OS Manifest

This manifest is the inventory and ownership map for the AI Engineering
Operating System. It records the purpose of each documentation domain, the
primary owner role, and the quality gates that apply before changes are accepted.

## Phase Status

### Phase 20 Scope

Phase 20 completes the remaining Project Brain category standards:

- business rules;
- decisions;
- architecture knowledge;
- roadmap knowledge;
- lessons learned;
- dependencies;
- unresolved questions.

These standards define how durable knowledge is formatted, owned, reviewed, and
converted into future action.

### Phase 19 Scope

Phase 19 completes the engineering loop detail reference set:

- Analysis Loop;
- Design Loop;
- Implementation Loop;
- Testing Loop;
- Review Loop;
- Deployment Loop;
- Documentation Loop;
- Retrospective Loop.

These standards define repeatable entry criteria, activities, outputs, exit
criteria, and checklists for the core execution loops.

### Phase 18 Scope

Phase 18 completes the executive standards reference set:

- executive standards index;
- mission;
- vision;
- charter;
- stakeholders;
- constraints;
- roadmap;
- success metrics;
- release strategy;
- executive glossary.

These standards define strategic direction, authority, constraints,
stakeholders, roadmap sequencing, success measurement, and release governance.

### Phase 17 Scope

Phase 17 completes the prompt template reference set:

- prompt template index;
- analyze module;
- review;
- rewrite module;
- write tests;
- discover domain;
- design API;
- security review;
- performance review;
- generate documentation.

These templates define how future agents must apply goals, loops, Project
Brain, standards, checklists, evidence, and safety gates to repeatable work.

### Phase 16 Scope

Phase 16 completes the delivery checklist reference set:

- delivery checklist index;
- Definition of Ready;
- Definition of Done;
- security review;
- release;
- deployment.

Together with the previously completed code review and architecture review
checklists, these gates define how agents prove readiness, completion, security,
release, and deployment safety.

### Phase 15 Scope

Phase 15 completes the measurement standards reference set:

- metrics standards index;
- quality metrics;
- coverage metrics;
- complexity metrics;
- duplication metrics;
- performance metrics;
- maintainability metrics.

These standards define how AI agents collect, interpret, and act on engineering
metrics without reducing quality review to blind score chasing.

### Phase 14 Scope

Phase 14 completes the product standards reference set:

- product standards index;
- Product Requirements Documents;
- features;
- epics;
- stories;
- personas;
- use cases;
- user journeys;
- acceptance criteria;
- non-functional requirements.

These standards define how AI agents connect modernization work to product
intent, stakeholders, measurable outcomes, acceptance evidence, and quality
attributes.

### Phase 13 Scope

Phase 13 completes the design pattern standards reference set:

- design pattern standards index;
- Adapter;
- Repository;
- Factory;
- Strategy;
- Decorator;
- Facade;
- Builder;
- Observer.

These standards define when common patterns are appropriate, when they are
overengineering, and how they fit architecture, domain, clean-code, and Python
modernization standards.

### Phase 12 Scope

Phase 12 completes the clean-code standards reference set:

- clean-code standards index;
- naming;
- functions;
- classes;
- comments;
- errors;
- formatting;
- testing;
- refactoring;
- heuristics.

These standards define local implementation quality rules for readable,
testable, maintainable Python modernization inside the architecture, domain,
API, and Python standards already established.

### Phase 11 Scope

Phase 11 completes the architecture style and decision standards reference set:

- architecture standards index;
- Clean Architecture;
- Hexagonal Architecture;
- Onion Architecture;
- persistence architecture;
- API architecture guidelines;
- async architecture;
- messaging architecture;
- C4 diagrams;
- Architecture Decision Records.

These standards define how AI agents preserve dependency direction, boundary
ownership, stable contracts, safe data access, reliable asynchronous work, and
durable decision records.

### Phase 10 Scope

Phase 10 completes the domain modeling standards reference set:

- domain standards index;
- bounded contexts;
- ubiquitous language;
- entities;
- value objects;
- aggregates;
- invariants;
- repositories;
- domain services;
- domain events.

These standards define how business behavior remains explicit, cohesive,
testable, and independent of frameworks and persistence.

### Phase 9 Scope

Phase 9 completes the FastAPI API standards reference set:

- FastAPI standards index;
- routers;
- dependencies;
- validation;
- errors;
- auth;
- pagination;
- filtering;
- OpenAPI;
- middleware;
- versioning.

These standards define HTTP transport boundaries that remain thin, secure,
documented, versioned, and aligned with Clean Architecture.

### Phase 8 Scope

Phase 8 completes the Python standards reference set:

- Python standards index;
- Pydantic v2;
- SQLAlchemy 2.x;
- FastAPI usage from the Python perspective;
- pathlib.

The Python standards area now has routing guidance and complete standards for
all Python files currently in the repository.

### Phase 7 Scope

Phase 7 completes the first Python implementation standards pack:

- Python 3.13+;
- typing;
- mypy;
- Ruff;
- pytest;
- exceptions;
- logging;
- AsyncIO.

These standards give backend agents practical implementation rules for typed,
tested, observable Python modernization.

### Phase 6 Scope

Phase 6 completes the first individual AI role playbook pack:

- CEO;
- Product Manager;
- Software Architect;
- Backend Engineer;
- Database Engineer;
- Security Engineer;
- QA Engineer;
- Reviewer;
- Technical Writer;
- DevOps and Release Manager.

These playbooks align individual role behavior with the cross-role model in
`agents/README.md`.

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
| CEO Agent | `agents/ceo.md` | Phase 6 |
| Product Manager Agent | `agents/product-manager.md` | Phase 6 |
| Software Architect Agent | `agents/architect.md` | Phase 6 |
| Backend Engineer Agent | `agents/backend.md` | Phase 6 |
| Database Engineer Agent | `agents/database.md` | Phase 6 |
| Security Engineer Agent | `agents/security.md` | Phase 6 |
| QA Engineer Agent | `agents/qa.md` | Phase 6 |
| Reviewer Agent | `agents/reviewer.md` | Phase 6 |
| Technical Writer Agent | `agents/tech-writer.md` | Phase 6 |
| DevOps and Release Manager Agent | `agents/devops.md` | Phase 6 |
| Python 3.13+ | `python/python313.md` | Phase 7 |
| Typing | `python/typing.md` | Phase 7 |
| mypy | `python/mypy.md` | Phase 7 |
| Ruff | `python/ruff.md` | Phase 7 |
| pytest | `python/pytest.md` | Phase 7 |
| Exceptions | `python/exceptions.md` | Phase 7 |
| Logging | `python/logging.md` | Phase 7 |
| AsyncIO | `python/async.md` | Phase 7 |
| Python Standards Index | `python/README.md` | Phase 8 |
| Pydantic v2 | `python/pydantic-v2.md` | Phase 8 |
| SQLAlchemy 2.x | `python/sqlalchemy2.md` | Phase 8 |
| FastAPI Python Usage | `python/fastapi.md` | Phase 8 |
| pathlib | `python/pathlib.md` | Phase 8 |
| FastAPI Standards Index | `fastapi/README.md` | Phase 9 |
| FastAPI Routers | `fastapi/routers.md` | Phase 9 |
| FastAPI Dependencies | `fastapi/dependencies.md` | Phase 9 |
| FastAPI Validation | `fastapi/validation.md` | Phase 9 |
| FastAPI Errors | `fastapi/errors.md` | Phase 9 |
| FastAPI Auth | `fastapi/auth.md` | Phase 9 |
| FastAPI Pagination | `fastapi/pagination.md` | Phase 9 |
| FastAPI Filtering | `fastapi/filtering.md` | Phase 9 |
| FastAPI OpenAPI | `fastapi/openapi.md` | Phase 9 |
| FastAPI Middleware | `fastapi/middleware.md` | Phase 9 |
| FastAPI Versioning | `fastapi/versioning.md` | Phase 9 |
| Domain Standards Index | `domain/README.md` | Phase 10 |
| Bounded Contexts | `domain/bounded-contexts.md` | Phase 10 |
| Ubiquitous Language | `domain/ubiquitous-language.md` | Phase 10 |
| Entities | `domain/entities.md` | Phase 10 |
| Value Objects | `domain/value-objects.md` | Phase 10 |
| Aggregates | `domain/aggregates.md` | Phase 10 |
| Invariants | `domain/invariants.md` | Phase 10 |
| Repositories | `domain/repositories.md` | Phase 10 |
| Domain Services | `domain/domain-services.md` | Phase 10 |
| Domain Events | `domain/domain-events.md` | Phase 10 |
| Architecture Standards Index | `architecture/README.md` | Phase 11 |
| Clean Architecture | `architecture/clean-architecture.md` | Phase 11 |
| Hexagonal Architecture | `architecture/hexagonal.md` | Phase 11 |
| Onion Architecture | `architecture/onion.md` | Phase 11 |
| Persistence Architecture | `architecture/persistence.md` | Phase 11 |
| API Architecture Guidelines | `architecture/api-guidelines.md` | Phase 11 |
| Async Architecture | `architecture/async.md` | Phase 11 |
| Messaging Architecture | `architecture/messaging.md` | Phase 11 |
| C4 Diagrams | `architecture/c4.md` | Phase 11 |
| Architecture Decision Records | `architecture/adrs.md` | Phase 11 |
| Clean Code Standards Index | `clean-code/README.md` | Phase 12 |
| Naming | `clean-code/naming.md` | Phase 12 |
| Functions | `clean-code/functions.md` | Phase 12 |
| Classes | `clean-code/classes.md` | Phase 12 |
| Comments | `clean-code/comments.md` | Phase 12 |
| Errors | `clean-code/errors.md` | Phase 12 |
| Formatting | `clean-code/formatting.md` | Phase 12 |
| Testing | `clean-code/testing.md` | Phase 12 |
| Refactoring | `clean-code/refactoring.md` | Phase 12 |
| Clean Code Heuristics | `clean-code/heuristics.md` | Phase 12 |
| Design Pattern Standards Index | `patterns/README.md` | Phase 13 |
| Adapter Pattern | `patterns/adapter.md` | Phase 13 |
| Repository Pattern | `patterns/repository.md` | Phase 13 |
| Factory Pattern | `patterns/factory.md` | Phase 13 |
| Strategy Pattern | `patterns/strategy.md` | Phase 13 |
| Decorator Pattern | `patterns/decorator.md` | Phase 13 |
| Facade Pattern | `patterns/facade.md` | Phase 13 |
| Builder Pattern | `patterns/builder.md` | Phase 13 |
| Observer Pattern | `patterns/observer.md` | Phase 13 |
| Product Standards Index | `product/README.md` | Phase 14 |
| Product Requirements Document | `product/prd.md` | Phase 14 |
| Features | `product/features.md` | Phase 14 |
| Epics | `product/epics.md` | Phase 14 |
| Stories | `product/stories.md` | Phase 14 |
| Personas | `product/personas.md` | Phase 14 |
| Use Cases | `product/use-cases.md` | Phase 14 |
| User Journeys | `product/user-journeys.md` | Phase 14 |
| Acceptance Criteria | `product/acceptance-criteria.md` | Phase 14 |
| Non-Functional Requirements | `product/nfrs.md` | Phase 14 |
| Metrics Standards Index | `metrics/README.md` | Phase 15 |
| Quality Metrics | `metrics/quality.md` | Phase 15 |
| Coverage Metrics | `metrics/coverage.md` | Phase 15 |
| Complexity Metrics | `metrics/complexity.md` | Phase 15 |
| Duplication Metrics | `metrics/duplication.md` | Phase 15 |
| Performance Metrics | `metrics/performance.md` | Phase 15 |
| Maintainability Metrics | `metrics/maintainability.md` | Phase 15 |
| Delivery Checklist Index | `checklists/README.md` | Phase 16 |
| Definition of Ready | `checklists/definition-of-ready.md` | Phase 16 |
| Definition of Done | `checklists/definition-of-done.md` | Phase 16 |
| Security Review Checklist | `checklists/security-review.md` | Phase 16 |
| Release Checklist | `checklists/release.md` | Phase 16 |
| Deployment Checklist | `checklists/deployment.md` | Phase 16 |
| Prompt Template Index | `prompts/README.md` | Phase 17 |
| Analyze Module Prompt | `prompts/analyze-module.md` | Phase 17 |
| Review Prompt | `prompts/review.md` | Phase 17 |
| Rewrite Module Prompt | `prompts/rewrite-module.md` | Phase 17 |
| Write Tests Prompt | `prompts/write-tests.md` | Phase 17 |
| Discover Domain Prompt | `prompts/discover-domain.md` | Phase 17 |
| Design API Prompt | `prompts/design-api.md` | Phase 17 |
| Security Review Prompt | `prompts/security-review.md` | Phase 17 |
| Performance Review Prompt | `prompts/performance-review.md` | Phase 17 |
| Generate Docs Prompt | `prompts/generate-docs.md` | Phase 17 |
| Executive Standards Index | `executive/README.md` | Phase 18 |
| Mission | `executive/mission.md` | Phase 18 |
| Vision | `executive/vision.md` | Phase 18 |
| Charter | `executive/charter.md` | Phase 18 |
| Stakeholders | `executive/stakeholders.md` | Phase 18 |
| Constraints | `executive/constraints.md` | Phase 18 |
| Roadmap | `executive/roadmap.md` | Phase 18 |
| Success Metrics | `executive/success-metrics.md` | Phase 18 |
| Release Strategy | `executive/release-strategy.md` | Phase 18 |
| Executive Glossary | `executive/glossary.md` | Phase 18 |
| Analysis Loop | `loops/analysis.md` | Phase 19 |
| Design Loop | `loops/design.md` | Phase 19 |
| Implementation Loop | `loops/implementation.md` | Phase 19 |
| Testing Loop | `loops/testing.md` | Phase 19 |
| Review Loop | `loops/review.md` | Phase 19 |
| Deployment Loop | `loops/deployment.md` | Phase 19 |
| Documentation Loop | `loops/documentation.md` | Phase 19 |
| Retrospective Loop | `loops/retrospective.md` | Phase 19 |
| Business Rules Brain | `brain/business-rules.md` | Phase 20 |
| Decisions Brain | `brain/decisions.md` | Phase 20 |
| Architecture Brain | `brain/architecture.md` | Phase 20 |
| Roadmap Brain | `brain/roadmap.md` | Phase 20 |
| Lessons Learned Brain | `brain/lessons.md` | Phase 20 |
| Dependencies Brain | `brain/dependencies.md` | Phase 20 |
| Unresolved Questions Brain | `brain/unresolved.md` | Phase 20 |

## Change Control

- Architectural rule changes require updates to `architecture/constitution.md`
  and an ADR entry.
- Role authority changes require updates to `agents/README.md`.
- New knowledge categories require updates to `brain/README.md`.
- Any phase must update `PROJECT_STATE.md`, `NEXT_TASK.md`, and `CHANGELOG.md`.
