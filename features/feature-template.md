---
id: your-feature-id
name: Your Feature Name
layer: feature
feature: your-feature-id
domain: your-domain-id
views:
  - your-view-id
bffs:
  - your-bff-id
server_apis:
  - your-server-api-id
---

# Your Feature Name

> Copy and rename this file to define one feature slice that is ready for implementation.

## Goal

Describe the product outcome and the business reason the feature exists.

## Scope

List what is in and out for this feature.

## Actors

List primary actors, roles, or systems that participate in the flow.

## User Flows

Describe the happy path and the most important edge flows.

## Linked Specs

List the related domain, server, BFF, web, and optional architecture reference docs with a brief purpose for each. Prefer links to canonical docs instead of copying shared rules into this file.

## Implementation Boundary

- Transport: describe route handlers and auth entry points.
- Application: describe use cases, orchestration, and ports.
- Domain: describe business rules and invariants.
- Integrations: describe downstream APIs, persistence, or events.
- Contracts: describe DTOs, schemas, and mappers.
- Tests: describe required unit, integration, contract, and end-to-end coverage.

## Acceptance Scenarios

Describe the concrete scenarios that must pass before implementation is done.

## Rollout and Backout

Describe release gating, monitoring, rollback, and ownership.
