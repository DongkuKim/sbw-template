---
id: your-bff-id
name: Your BFF Name
layer: bff
feature: your-feature-id
domain: your-domain-id
view: your-view-id
server_apis:
  - your-server-api-id
---

# Your BFF Name

> Copy and rename this file to define one BFF contract for a web view.

## Purpose

Describe the view-level data and actions this BFF provides.

## View Inputs

Describe route params, query params, and session inputs.

## Orchestration Flow

Describe how the BFF sequences downstream calls, policy checks, and mapping.

## Server API Usage

List each downstream API and why it is called.

## View Contract

Describe the exact web-facing payload and action surface.

## Failure Handling

Describe fallback behavior, partial failure policy, and user-safe errors. Link to shared error docs when the BFF follows a common policy.

## Data Protection

Describe redaction, privacy, and session-boundary rules.

## Implementation Boundary

- Transport: describe BFF routes, request parsing, and auth entry.
- Application: describe orchestration use cases and ports.
- Domain: describe any feature policy or invariants.
- Integrations: describe downstream clients and adapters.
- Contracts: describe response schemas, DTOs, and mappers.
- Tests: describe unit, integration, contract, and end-to-end coverage.
