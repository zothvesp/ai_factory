# Security Review Checklist

## Philosophy

Security review verifies that a change preserves trust boundaries, protects
data, handles secrets safely, and fails without exposing users or operations to
unacceptable risk.

## Review Triggers

- Authentication, authorization, sessions, tokens, secrets, or cryptography.
- User input, file handling, deserialization, SQL, shell commands, or external
  calls.
- Logging, metrics, traces, audit events, or error responses containing
  sensitive context.
- Dependency, container, CI/CD, deployment, or infrastructure changes.
- Privacy, retention, compliance, or tenant isolation changes.

## Required Gates

- Trust boundaries and actors are explicit.
- Server-side authorization is enforced for protected actions.
- Inputs are validated and outputs are encoded or constrained.
- Secrets are not stored in source, logs, exceptions, tests, Project Brain, or
  artifacts.
- Sensitive errors are mapped to safe public responses.
- Dependencies and containers have acceptable supply-chain risk.
- Audit and monitoring cover security-sensitive workflows.

## Bad Example

```python
logger.info("login failed", extra={"password": password})
```

The log leaks a secret.

## Good Example

```python
logger.info("login failed", extra={"user_id": user_id, "reason": "bad_credentials"})
```

The event is useful without exposing the credential.

## Decision Guidance

Block when a change leaks secrets, bypasses authorization, weakens tenant
isolation, or introduces unreviewed execution paths. Record accepted lower-risk
findings with owner and trigger.

## AI Guidance

- Assume user input is hostile at boundaries.
- Do not suggest storing secrets in documentation or examples.
- Check logs, tests, fixtures, and error messages for sensitive data.
- Escalate unclear auth, crypto, or compliance questions to Security Engineer.

## Review Checklist

- Authn and authz behavior is explicit and tested.
- Input validation and output safety are addressed.
- Secrets and sensitive data are protected.
- Dependency and deployment risks are considered.
- Audit and incident diagnosis needs are satisfied safely.

## References

- Security Agent: `../agents/security.md`
- FastAPI Auth: `../fastapi/auth.md`
- Error Handling: `../clean-code/errors.md`
