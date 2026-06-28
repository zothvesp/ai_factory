# Classes

## Philosophy

Classes exist to keep related state and behavior together behind a stable
interface. A class is justified when it protects invariants, coordinates a
dependency, or models a cohesive domain concept.

## Rules

- Give every class one clear responsibility and one primary reason to change.
- Put behavior near the data and invariants it protects.
- Prefer composition over inheritance for reuse and variation.
- Keep constructors explicit. Do not perform network, database, or filesystem
  work in constructors.
- Do not create classes as namespaces for unrelated static functions.
- Avoid data-only classes unless they are DTOs, commands, events, or value
  objects with an explicit boundary purpose.
- Inject dependencies through constructors or composition roots.

## Bad Example

```python
class UserManager:
    def create_user(self, payload: dict[str, Any]) -> None: ...
    def export_csv(self) -> bytes: ...
    def send_marketing_email(self) -> None: ...
    def rebuild_indexes(self) -> None: ...
```

The class groups unrelated behavior by noun rather than cohesive responsibility.

## Good Example

```python
class UserRegistrationService:
    def __init__(self, users: UserRepository, emails: EmailGateway) -> None:
        self._users = users
        self._emails = emails

    def register(self, command: RegisterUser) -> UserId:
        user = User.register(command.email)
        self._users.save(user)
        self._emails.send_welcome(user.email)
        return user.id
```

The service owns a single use case and makes dependencies visible.

## Decision Guidance

Use a class when behavior needs durable state, dependency composition, invariant
protection, or a named role in the architecture. Use a function when behavior is
stateless, small, and does not need polymorphism or lifecycle management.

## AI Guidance

- Do not introduce a class just because a file is growing.
- Split classes by responsibility, not by arbitrary method count.
- Favor small protocols or ports for dependency seams.
- Check domain standards before modeling entities, aggregates, or value
  objects.

## Review Checklist

- Class responsibility can be stated in one sentence.
- Public methods belong to the same abstraction.
- Invariants are enforced inside the class.
- Dependencies are explicit and mockable through ports where appropriate.
- Inheritance is justified by substitutability, not convenience.

## References

- God Class: `../smells/god-class.md`
- SOLID: `../engineering/solid.md`
- Composition over Inheritance: `../engineering/composition-over-inheritance.md`
- Domain Entities: `../domain/entities.md`
