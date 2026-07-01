# Next Task

## Phase 22 Recommendation

Add repository hardening and validation so the AI-OS can prove documentation
quality automatically and prepare for ongoing maintenance.

Recommended files:

- `.github/workflows/ai-os-docs.yml`
- `.ai/tools/validate-docs.md` or equivalent documented validation contract
- `.ai/README.md`
- `.ai/MANIFEST.md`
- `.ai/PROJECT_STATE.md`
- `.ai/NEXT_TASK.md`

## Goal

Create a maintainable validation and publishing approach for the completed
AI-OS documentation product.

## Entry Criteria

- Phase 21 reviewed or accepted.
- Architecture Constitution remains the source of truth for mandatory design
  rules.
- CTO, DevOps and Release Manager, QA Engineer, Reviewer, Technical Writer, and
  Security Engineer playbooks remain role guidance.
- Goal Engineering remains the source of truth for goal discovery,
  decomposition, acceptance criteria, exit criteria, KPIs, and risks.
- Completed AI-OS standards remain source-of-truth references.
- Full `.ai` placeholder scan is clean before automation work begins.

## Exit Criteria

- Validation rules are documented and, where practical, automated.
- CI or local validation checks for skeletal markers, broken required files, and
  phase metadata consistency.
- Publishing or maintenance workflow is documented.
- Project Brain records any newly discovered rules, recurring modernization
  risks, or remaining debt.
- `MANIFEST.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`, and `CHANGELOG.md` are
  updated.
- Changes are committed and pushed to the configured Git remote.
