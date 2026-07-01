# Security Review Prompt

## Purpose

Use this prompt when work touches trust boundaries, secrets, auth, privacy,
dependencies, deployment, or sensitive workflows.

## Template

```text
Act as Security Engineer and Reviewer.

Goal:
- Review [change/artifact] for security and privacy risk.

Inputs:
- Changed files/artifact:
- Threat surface:
- Data classification:
- Relevant security requirements:

Required process:
1. Identify actors, trust boundaries, assets, and entry points.
2. Review authn, authz, validation, secrets, logging, error handling,
   dependencies, deployment, and audit behavior.
3. Classify findings by severity and exploitability.
4. Cite concrete evidence and standards.
5. Define required fixes, accepted risks, tests, and monitoring.

Output:
- Security findings ordered by severity.
- Required fixes and evidence.
- Accepted residual risk.
- Project Brain risk/debt updates if needed.
```

## Bad Use

Checking only dependencies while ignoring authorization, logs, error responses,
and tenant isolation.

## Review Checklist

- Trust boundaries are explicit.
- Sensitive data is protected.
- Auth and validation are tested.
- Findings cite evidence and standards.
- Residual risk is owned.

## References

- Security Checklist: `../checklists/security-review.md`
- FastAPI Auth: `../fastapi/auth.md`
- Errors: `../clean-code/errors.md`
