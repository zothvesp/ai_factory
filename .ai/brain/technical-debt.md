# Technical Debt

Technical debt is an accepted gap between the current system and the desired
standard. Debt is allowed only when it is explicit, owned, risk-assessed, and
paired with a repayment trigger.

## Debt Entry Format

```markdown
## YYYY-MM-DD - Short Title

- Context: Why the debt exists.
- Debt: What standard is not currently satisfied.
- Risk: What can go wrong if it remains.
- Owner: Responsible role.
- Repayment trigger: Event or phase that requires repayment.
- Status: Open, accepted, in progress, or closed.
```

## 2026-06-27 - Skeletal Topic Documents

- Context: The repository already contains many `.ai` topic files with only
  generic section headings.
- Debt: Most files are not production-quality standards yet and do not satisfy
  the AI-OS documentation completion rules. Phase 2 repaid the first ten topic
  documents: five anti-patterns and five smells. Phase 3 repaid the remaining
  smell files and the code and architecture review checklists.
- Risk: Future agents may mistake skeletal pages for authoritative guidance.
- Owner: Technical Writer.
- Repayment trigger: Each topic must be expanded before it is referenced as a
  completed standard or used as a quality gate.
- Status: Open.

## 2026-06-27 - Read-Only Local Git Metadata Path

- Context: The workspace contains an empty read-only `.git` directory that
  prevents normal local Git repository initialization.
- Debt: Git operations require an external git directory instead of standard
  `.git` metadata in the worktree.
- Risk: Future agents may run plain `git status` and incorrectly conclude no
  repository exists.
- Owner: CTO.
- Repayment trigger: Filesystem mount or workspace setup is changed so `.git`
  can be replaced with normal writable Git metadata.
- Status: Open.
