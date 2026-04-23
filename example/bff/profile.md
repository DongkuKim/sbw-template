---
id: profile
name: Profile BFF
layer: bff
domain: customer-identity
view: profile
server_apis:
  - get-user-profile
---

# Profile BFF

## Purpose

Provide the single web-facing contract required to render the signed-in profile view.

## View Inputs

The BFF receives the signed-in session, the route context for `/profile`, and no user-supplied mutation payload.

## Orchestration Flow

The BFF authenticates the session, resolves the effective user id, calls `get-user-profile`, maps the backend fields into stable view props, and classifies downstream failures into user-safe view states.

## Server API Usage

`get-user-profile` is invoked on each profile page load to fetch canonical identity data for the current user.

## View Contract

The response returns `profileSummary` with display name, primary email, membership tier, and a `viewState` envelope that lets the web layer render loading, success, or retryable error states without backend-specific branching.

## Failure Handling

Backend `404` becomes a recoverable empty or not-found experience, `403` becomes an access-denied state, and transport failures become retryable generic errors. The BFF does not leak internal stack or vendor details.

## Data Protection

The BFF exposes only user-safe identity fields, strips internal metadata, and binds the response to the authenticated session context.

## Implementation Boundary

- Transport: `/bff/profile` handlers validate session state and request shape.
- Application: a profile-read use case coordinates auth, downstream calls, and response assembly.
- Domain: customer identity policy decides which fields may be exposed.
- Integrations: a profile service client calls the backend API with timeout and retry policy.
- Contracts: BFF response schemas and mapping code define the stable web contract.
- Tests: unit, integration, contract, and end-to-end tests cover orchestration, failures, and contract stability.
