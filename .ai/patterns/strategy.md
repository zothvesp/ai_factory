# Strategy

## Philosophy

Strategy encapsulates interchangeable behavior behind a stable interface. It is
useful when policy varies independently from the caller.

## Rules

- Use strategy when there are multiple behavior variants with the same contract.
- Keep strategy interfaces narrow and typed.
- Select strategies explicitly in the composition root or application service.
- Do not use strategy to avoid a simple and readable branch.
- Test each strategy against the shared contract and its unique edge cases.

## Bad Example

```python
if mode == "a":
    ...
elif mode == "b":
    ...
elif mode == "c":
    ...
```

This may be fine if the branch is small. It becomes a problem when each branch
contains complex, independently changing policy.

## Good Example

```python
class DiscountPolicy(Protocol):
    def calculate(self, cart: Cart) -> Money: ...


class LoyaltyDiscountPolicy:
    def calculate(self, cart: Cart) -> Money:
        return cart.subtotal * Decimal("0.10")
```

The caller depends on a behavior contract, not a pile of conditional policy.

## Decision Guidance

Keep a branch when variants are few, short, and stable. Introduce strategy when
variants grow, need independent tests, or are selected by configuration,
tenant, product, or external capability.

## AI Guidance

- Do not introduce strategy before naming the shared contract.
- Keep selection logic separate from strategy behavior.
- Avoid stringly typed strategy lookup.
- Verify all strategies satisfy the same expectations.

## Review Checklist

- Variation is real and independently changing.
- Shared interface is small and typed.
- Selection is explicit and testable.
- Strategies do not mutate unexpected shared state.
- Tests cover common contract and variant-specific behavior.

## References

- Open/Closed Principle: `../engineering/solid.md`
- KISS: `../engineering/kiss.md`
- Testing: `../clean-code/testing.md`
