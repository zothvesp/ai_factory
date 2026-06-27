# Anti-Patterns

This Project Brain file records recurring prohibited designs and remediation
rules discovered while building the AI-OS.

## 2026-06-27 - First Modernization Anti-Pattern Pack

- Context: Phase 2 completed production standards for circular dependencies,
  service locator, magic values, tight coupling, and singleton abuse.
- Decision: These anti-patterns are reviewable findings in AI-assisted legacy
  modernization. They must be remediated, explicitly accepted as temporary debt,
  or escalated through architecture governance.
- Rationale: Each anti-pattern hides ownership, dependency direction, business
  meaning, or runtime state, making modernization unsafe.
- Impact: Future reviewers should classify these issues using the completed
  standards before proposing broad rewrites.
- Owner: Reviewer.
- Review trigger: Revisit when Phase 3 creates anti-pattern and smell index
  files.

## Binding Rule

Do not silently normalize these patterns as acceptable legacy style. If a phase
cannot remove one, record debt with owner, risk, and repayment trigger.
