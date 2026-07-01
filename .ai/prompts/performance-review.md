# Performance Review Prompt

## Purpose

Use this prompt to evaluate latency, throughput, capacity, query efficiency,
resource usage, async behavior, or scalability.

## Template

```text
Act as Performance Engineer, Backend Engineer, and Software Architect.

Goal:
- Review [workflow/module/API] against [performance goal or NFR].

Inputs:
- Workload and environment:
- Metric threshold:
- Current evidence:
- Constraints and non-scope:

Required process:
1. Confirm the product or operational reason for performance work.
2. Identify workload, p95/p99 latency, throughput, resource use, saturation,
   queue lag, and error rate where relevant.
3. Inspect data access, indexes, transactions, async behavior, caching, and
   external calls.
4. Recommend measured fixes before architectural changes.
5. Define verification and monitoring evidence.

Output:
- Bottleneck hypothesis with evidence.
- Recommended fixes ordered by risk and impact.
- Measurement plan.
- Trade-offs and residual risk.
```

## Bad Use

Adding cache, async, queues, or new infrastructure without a measured bottleneck
or explicit NFR.

## Review Checklist

- Workload and threshold are clear.
- Evidence supports the bottleneck.
- Recommendation is proportionate.
- Trade-offs are documented.
- Regression evidence or monitoring is planned.

## References

- Performance Metrics: `../metrics/performance.md`
- Product NFRs: `../product/nfrs.md`
- Async Architecture: `../architecture/async.md`
