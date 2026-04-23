---
id: profile-experience
name: Profile Experience
layer: feature
feature: profile-experience
domain: customer-identity
views:
  - profile
bffs:
  - profile
server_apis:
  - get-user-profile
---

# Profile Experience

## Goal

Give signed-in users a reliable profile page that loads core identity information through a BFF contract that is safe to evolve independently from backend service contracts.

## Scope

In scope are authenticated profile reads, BFF shaping, and the primary profile view states. Profile editing, avatar uploads, and notification settings are out of scope.

## Actors

- Authenticated customer
- Web BFF
- Profile backend service

## User Flows

The user opens `/profile`, the route guard confirms a signed-in session, the BFF loads profile data from the backend API, and the web view renders the summary card. If the backend is unavailable, the page renders a retryable error state without leaking backend details.

## Linked Specs

- Domain: [customer-identity](../domains/customer-identity.md) defines the canonical user profile language.
- Architecture: [adr-001-vertical-slice-bff](../architecture/adrs/adr-001-vertical-slice-bff.md) and [clean-code](../../architecture/standards/clean-code.md) define the shared slice and code-shape defaults used by this feature.
- Server: [get-user-profile](../server/get-user-profile.md) provides the source system contract.
- BFF: [profile](../bff/profile.md) shapes backend data into a stable view contract.
- Web view: [profile](../web/views/profile.md) renders the feature through [account-shell](../web/layouts/account-shell.md) and [user-summary-card](../web/shared-components/user-summary-card.md).

## Implementation Boundary

- Transport: `/profile` web route and `GET /bff/profile` entry perform session checks and request parsing.
- Application: a profile-read use case coordinates identity lookup, authorization, and response mapping.
- Domain: profile visibility rules and identity invariants live in the customer identity domain.
- Integrations: a backend profile client calls the profile service and maps service failures.
- Contracts: backend DTOs, BFF response schemas, and web view props remain versioned and explicit.
- Tests: unit tests cover mapping and policy rules, integration tests cover downstream calls, contract tests protect response shapes, and end-to-end tests cover the signed-in profile journey.

## Acceptance Scenarios

- A signed-in user can load the profile page and see their name, email, and membership tier.
- An expired session is redirected or blocked by the route guard before downstream calls occur.
- A backend timeout surfaces a user-safe error state and emits observable failure signals.

## Rollout and Backout

Release behind normal web deployment gates, watch profile latency and error dashboards, and back out by disabling the route and BFF exposure without a schema migration.
