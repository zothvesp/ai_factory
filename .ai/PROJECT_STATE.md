# Project State

## Current Phase

Phase 4: Engineering principle standards.

## Status

Ready for review.

## Completed

- Completed Phase 1 governing spine.
- Expanded five anti-pattern standards into production-quality guidance:
  circular dependencies, service locator, magic values, tight coupling, and
  singleton abuse.
- Expanded five code smell standards into production-quality guidance:
  duplicate code, long method, god class, primitive obsession, and hidden side
  effects.
- Added examples, decision trees, refactoring strategies, AI guidance, review
  checklists, and references for each completed Phase 2 topic.
- Updated Project Brain with recurring modernization rules, anti-pattern
  guidance, and remaining documentation debt.
- Updated manifest, next task, and changelog for Phase 2 closure.
- Completed remaining smell standards for data clumps, dead code, feature envy,
  and shotgun surgery.
- Added anti-pattern and smell index pages with severity models, routing
  decision trees, and review rules.
- Replaced skeletal code review and architecture review checklists with
  actionable gates that reference completed smells and anti-patterns.
- Updated Project Brain with review-routing rules and reduced the documentation
  debt scope.
- Updated manifest, next task, and changelog for Phase 3 closure.
- Expanded ten engineering principle standards: DRY, KISS, YAGNI, SOLID,
  dependency injection, high cohesion and low coupling, composition over
  inheritance, fail fast, Law of Demeter, and Tell, Don't Ask.
- Added examples, decision trees, AI guidance, review checklists, and references
  to connect these principles to the completed smell and anti-pattern review
  pack.
- Updated Project Brain with the principle-to-review rule and reduced the
  documentation debt scope.
- Updated manifest, next task, and changelog for Phase 4 closure.

## Evidence

- Documentation is organized under `.ai/`.
- Phase files exist: `README.md`, `MANIFEST.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, and `CHANGELOG.md`.
- Phase 2, Phase 3, and Phase 4 completed standards are listed in
  `MANIFEST.md`.
- Code review and architecture review now route maintainability findings through
  completed smell and anti-pattern indexes.
- Engineering principle documents now explain the rationale behind core review
  findings and refactoring guidance.
- The Git remote target is `git@github.com:zothvesp/ai_factory.git`.

## Known Constraints

- The workspace contains an empty read-only `.git` directory, so normal local
  Git metadata cannot be stored at `.git`. Publishing must use an external Git
  directory unless the filesystem mount is changed.
- Many pre-existing documents outside the completed review pack are skeletal and
  remain backlog items. They are not treated as completed standards until
  expanded according to the manifest completion rules.

## Review Questions

- Should Phase 5 complete the remaining engineering principles such as GRASP,
  CUPID, and Boy Scout Rule, or switch to the individual AI role files under
  `agents/`?
- Should the legacy application source files remain in this repository, or
  should the AI-OS be separated into a documentation-only repository?
