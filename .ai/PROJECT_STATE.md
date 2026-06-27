# Project State

## Current Phase

Phase 2: Anti-pattern and code smell standards.

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

## Evidence

- Documentation is organized under `.ai/`.
- Phase files exist: `README.md`, `MANIFEST.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, and `CHANGELOG.md`.
- Phase 2 completed standards are listed in `MANIFEST.md`.
- The Git remote target is `git@github.com:zothvesp/ai_factory.git`.

## Known Constraints

- The workspace contains an empty read-only `.git` directory, so normal local
  Git metadata cannot be stored at `.git`. Publishing must use an external Git
  directory unless the filesystem mount is changed.
- Many pre-existing documents are skeletal and remain backlog items. They are
  not treated as completed standards until expanded according to the manifest
  completion rules.

## Review Questions

- Should Phase 3 complete the remaining smell and anti-pattern documents, or
  switch to engineering principle standards such as DRY, KISS, SOLID, and
  dependency injection?
- Should the legacy application source files remain in this repository, or
  should the AI-OS be separated into a documentation-only repository?
