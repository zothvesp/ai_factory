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
  smell files and the code and architecture review checklists. Phase 4 repaid
  ten engineering principle documents. Phase 5 repaid the remaining engineering
  principle files and added the engineering index. Phase 6 repaid the primary
  individual role playbook files under `agents/`. Phase 7 repaid eight Python
  implementation standards. Phase 8 repaid the remaining Python standard files
  and added the Python standards index. Phase 9 repaid all FastAPI standard
  files and added the FastAPI standards index. Phase 10 repaid all domain
  modeling standard files and added the domain standards index. Phase 11 repaid
  the architecture style and decision standard files and added the architecture
  standards index. Phase 12 repaid all clean-code standard files and added the
  clean-code standards index. Phase 13 repaid all design pattern standard files
  and added the design pattern standards index. Phase 14 repaid all product
  standard files and added the product standards index. Phase 15 repaid all
  metrics standard files and added the metrics standards index. Phase 16 repaid
  the remaining checklist files and added the delivery checklist index. Phase
  17 repaid all prompt template files and added the prompt template index.
  Phase 18 repaid all executive standard files and added the executive standards
  index. Phase 19 repaid all engineering loop detail files. Phase 20 repaid the
  remaining Project Brain category files. Phase 21 repaid all remaining Goal
  Engineering support files and added the goal standards index. A full `.ai`
  scan found no remaining skeletal markers.
- Risk: Future agents may mistake skeletal pages for authoritative guidance.
- Owner: Technical Writer.
- Repayment trigger: Each topic must be expanded before it is referenced as a
  completed standard or used as a quality gate.
- Status: Closed.

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
