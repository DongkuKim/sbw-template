---
id: your-server-api-id
name: Your Server API Name
layer: server
feature: your-feature-id
domain: your-domain-id
method: GET
path: /your/api/path
---

# Your Server API Name

> Copy and rename this file to define one backend API contract.

## Purpose

Describe what the API provides and why the BFF needs it.

## Request Contract

Describe required path params, query params, headers, and body shape.

## Response Contract

Describe success shape, important fields, pagination, and compatibility notes.

## Auth and Authorization

Describe caller identity, required permissions, and sensitive field rules. Link to shared auth docs when the rule is inherited rather than endpoint-specific.

## Error Model

Describe expected failure categories, status mapping, and retry semantics. Link to shared error docs when the rule is common across endpoints.

## Operational Policy

Describe idempotency, latency budget, timeout policy, cacheability, and observability expectations.

## Implementation Boundary

- Transport: describe routing, auth entry, and request parsing.
- Application: describe use cases and policy orchestration.
- Domain: describe business rules and invariants.
- Integrations: describe downstream systems, storage, or event dependencies.
- Contracts: describe schemas, mappers, and versioned DTOs.
- Tests: describe unit, integration, and contract coverage.
