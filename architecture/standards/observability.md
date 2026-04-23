# Observability Standard

## Purpose

Require operational visibility as part of design so teams know what must be emitted before code is written.

## Rules

- Features name the success signal and top failure modes.
- Server and BFF specs declare logs, metrics, traces, and latency budgets.
- Rollout plans include health checks, dashboards, and rollback signals.

## Build Notes

- Can on-call engineers detect and localize a failure from planned signals?
- Does each request path have a latency budget and error metric?
- Is rollback tied to observable conditions rather than intuition?
