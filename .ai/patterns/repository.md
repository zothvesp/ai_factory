# Repository

## Philosophy

A repository provides collection-like access to aggregates while hiding
persistence mechanics. It protects the domain model from ORM and SQL details.

## Rules

- Repository methods should use domain identifiers, specifications, commands, or
  explicit query objects.
- Return aggregates or read models intentionally; do not return ORM models from
  domain-facing repositories.
- Keep transaction ownership in the application service or unit-of-work pattern,
  not hidden inside every repository method.
- Do not create generic repositories that erase domain language.
- Integration-test mappings, constraints, and transaction behavior.

## Bad Example

```python
class GenericRepository:
    def find(self, table: str, filters: dict[str, Any]) -> list[Any]: ...
```

The interface hides domain intent and encourages stringly typed persistence.

## Good Example

```python
class SqlAlchemyOrderRepository(OrderRepository):
    def get(self, order_id: OrderId) -> Order:
        model = self._session.get(OrderModel, order_id.value)
        if model is None:
            raise OrderNotFound(order_id)
        return to_domain_order(model)
```

The repository speaks domain language and maps infrastructure details.

## Decision Guidance

Use a repository for aggregate persistence and domain-facing data access. Use a
read model or query service for reporting, search, and projections that do not
need aggregate behavior.

## AI Guidance

- Do not expose SQLAlchemy sessions or models to domain objects.
- Keep repository names tied to aggregate or bounded-context language.
- Avoid hiding N+1 queries behind innocent method names.
- Add tests for mapping and transactional edge cases.

## Review Checklist

- Repository interface uses domain language.
- ORM details stay in infrastructure.
- Transaction ownership is explicit.
- Query behavior is observable and efficient.
- Missing records and concurrency conflicts are handled.

## References

- Domain Repositories: `../domain/repositories.md`
- Persistence Architecture: `../architecture/persistence.md`
- SQLAlchemy 2.x: `../python/sqlalchemy2.md`
