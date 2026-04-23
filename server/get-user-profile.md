---
id: get-user-profile
name: Get User Profile
layer: server
feature: profile-experience
domain: customer-identity
method: GET
path: /users/{userId}/profile
---

# Get User Profile

## Purpose

Return the source-of-truth profile information needed to render the signed-in profile experience.

## Request Contract

The caller passes `userId` as a path parameter plus a service identity token in headers. The endpoint is read-only and does not accept a body.

## Response Contract

The success payload returns user id, display name, primary email, membership tier, and profile last-updated metadata. Compatibility is additive only.

## Auth and Authorization

Only trusted internal callers may invoke this endpoint. The service verifies caller identity and ensures the requested profile belongs to the authorized user context.

## Error Model

Return `404` when the user does not exist, `403` when the caller is not authorized, and `5xx` for downstream or infrastructure failures. Timeouts are safe to retry from the BFF.

## Operational Policy

The endpoint is idempotent, targets 250 ms p95 latency, allows short-lived BFF caching for stable profile reads, and emits request, error, and latency telemetry tagged by endpoint and caller.

## Implementation Boundary

- Transport: an HTTP handler parses path params and caller identity.
- Application: a profile-read use case enforces visibility and orchestration.
- Domain: customer identity rules define what constitutes a valid visible profile.
- Integrations: repository or source-system adapters fetch the profile record.
- Contracts: request and response DTOs are versioned and mapped explicitly.
- Tests: unit, integration, and contract tests guard authorization, mapping, and error translation.
