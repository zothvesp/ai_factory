# Dependencies

Dependencies record external systems, libraries, services, infrastructure,
runtime tools, and ownership that affect modernization work.

## Entry Format

```markdown
## YYYY-MM-DD - Dependency Name

- Type: Library, service, database, broker, tool, API, infrastructure.
- Purpose: Why the system depends on it.
- Owner: Responsible role or team.
- Version or contract: Version, API contract, or compatibility expectation.
- Risk: Operational, security, performance, licensing, or maintenance risk.
- Review trigger: Upgrade, replacement, incident, or deprecation signal.
```

## Rules

- Record dependencies that affect design, operations, security, testing, or
  release.
- Do not list every transitive package unless it carries material risk.
- Link dependency changes to security, release, and deployment gates.
- Record ownership for external services and runtime infrastructure.

## Bad Example

```text
Uses libraries.
```

## Good Example

```text
Dependency: PostgreSQL.
Purpose: durable relational storage.
Risk: schema migrations can affect availability and rollback.
Review trigger: major version upgrade or migration strategy change.
```

## AI Guidance

- Check dependency risk before introducing new libraries or services.
- Record deprecations and version constraints.
- Escalate unowned production dependencies.

## Review Checklist

- Purpose and owner are clear.
- Version or contract is known where relevant.
- Risks and triggers are explicit.
- Security and release impacts are considered.
- Dependency is linked to affected standards.

## References

- Release Checklist: `../checklists/release.md`
- Security Review: `../checklists/security-review.md`
