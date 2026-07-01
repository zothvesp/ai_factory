# Performance Metrics

## Philosophy

Performance metrics measure whether runtime behavior satisfies product and
operational requirements. They must be tied to workloads, thresholds, and user
impact.

## Rules

- Define latency, throughput, concurrency, resource usage, queue lag, error rate,
  and saturation metrics where relevant.
- Every performance metric must state workload, environment, threshold,
  percentile, and measurement method.
- Use p95 or p99 latency for user-facing paths, not averages alone.
- Do not optimize without an NFR, observed bottleneck, or capacity risk.
- Protect performance fixes with regression tests, load tests, or monitoring.

## Bad Example

```text
The endpoint feels slow, so add Redis.
```

This jumps to a solution without measurement.

## Good Example

```text
Backup job search p95 latency must remain under 300 ms for 10,000 jobs per
tenant in staging load tests; current p95 is 740 ms due to missing composite
index.
```

## Decision Guidance

Measure first when performance is uncertain. Optimize only when the measured
path matters to product value, operational cost, reliability, or an explicit
NFR.

## AI Guidance

- Ask for workload and threshold before performance redesign.
- Prefer query/index/data-shape fixes before adding caches.
- Include rollback and observability for runtime behavior changes.
- Record durable performance constraints in NFRs or Project Brain.

## Review Checklist

- Metric has workload, percentile, threshold, and environment.
- User or operational impact is clear.
- Bottleneck evidence exists.
- Fix has regression evidence or monitoring.
- Trade-offs such as consistency, cost, and complexity are documented.

## References

- Product NFRs: `../product/nfrs.md`
- Persistence Architecture: `../architecture/persistence.md`
- Async Architecture: `../architecture/async.md`
