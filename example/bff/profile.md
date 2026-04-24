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

## BFF Path

- Route template: `/bff/profile`
- Route params source of truth: this path template (no params).

## View Inputs

- Route params: none
- Query params: none
- Session/Auth inputs:

```ts
type SessionInput = {
  userId: string;
  roles: string[];
  tenantId?: string;
  permissions?: string[];
  [key: string]: unknown;
};
```

## BFF API (Web-facing)

- Request type:

```ts
type ProfileRequest = {};
```

- Response type:

```ts
type ProfileResponse = {
  profileSummary: {
    displayName: string;
    primaryEmail: string;
    membershipTier?: string;
  };
  viewState: "loading" | "success" | "retryable-error" | "access-denied" | "not-found";
};
```

## Orchestration Flow

1. Parse and validate request.
2. Enforce auth and policy.
3. Call downstream API (`get-user-profile`) using the authenticated user id.
4. Map downstream DTO fields into `ProfileResponse`.
5. Return typed response with user-safe `viewState`.

## Server API Usage

- `get-user-profile`: fetch canonical identity data for the authenticated user on profile page load.

## Failure Handling

- `404` -> `not-found`
- `403` -> `access-denied`
- transport/downstream failure -> `retryable-error`

## Data Protection

The BFF exposes only user-safe identity fields, strips internal metadata, and binds the response to the authenticated session context.

## Implementation Boundary

- Transport: `/bff/profile` handlers validate session state and request shape.
- Application: a profile-read use case coordinates auth, downstream calls, and response assembly.
- Domain: customer identity policy decides which fields may be exposed.
- Integrations: a profile service client calls the backend API with timeout and retry policy.
- Contracts: BFF response schemas and mapping code define the stable web contract.
- Tests: unit, integration, contract, and end-to-end tests cover orchestration, failures, and contract stability.
