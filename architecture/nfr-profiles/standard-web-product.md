# Standard Web Product NFR Profile

## Security

User-facing requests require authenticated sessions for protected routes, role checks at the BFF boundary, and secrets sourced from managed runtime configuration only.

## Reliability and SLO

Interactive product surfaces target 99.9 percent monthly availability and degrade gracefully when optional downstream data is unavailable.

## Performance Budget

BFF responses target 300 ms p95 for cache-assisted reads and 700 ms p95 for uncached aggregation paths.

## Observability

Every request emits structured logs, trace ids, success and failure counters, and latency histograms tagged by feature and endpoint.

## Privacy and Compliance

Personal data is classified, redacted from logs, and retained only through system-of-record policies.

## Rollout and Backout

Production rollout requires staging validation, health checks, and a rollback path that can disable the feature without a schema migration.
