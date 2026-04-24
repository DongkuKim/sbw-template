---
id: your-bff-id
name: Your BFF Name
layer: bff
domain: your-domain-id
view: your-view-id
server_apis:
  - your-server-api-id
---

# Your BFF Name

> Copy and rename this file to define one BFF contract for a web view.

## Purpose

Describe the view-level data and actions this BFF provides.

## BFF Path

- Route template: `/bff/<view-path>/:id?`
- Route params source of truth: this path template

## View Inputs

- Route params: from `BFF Path` template
- Query params:
  - `q?: string`
  - `status?: string`
  - `page: number`
  - `pageSize: number`
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
type <View>Request = {
  q?: string;
  status?: string;
  page: number;
  pageSize: number;
};
```

- Response type:

```ts
type <View>Response = {
  items: <View>Item[];
  page: number;
  pageSize: number;
  total: number;
};

type <View>Item = {
  id: string;
  name: string;
  status: string;
  updatedAt: string;
};
```

## Orchestration Flow

1. Parse and validate request.
2. Enforce auth and policy.
3. Call downstream API(s).
4. Map downstream DTOs to view response.
5. Return typed response.

## Server API Usage

List each downstream API and why it is called.

## Failure Handling

Describe fallback behavior, partial failure policy, and user-safe errors.

## Data Protection

Describe redaction, privacy, and session-boundary rules.

## Implementation Boundary

- Transport: describe BFF routes, request parsing, and auth entry.
- Application: describe orchestration use cases and ports.
- Domain: describe any domain policy or invariants.
- Integrations: describe downstream clients and adapters.
- Contracts: describe response schemas, DTOs, and mappers.
- Tests: describe unit, integration, contract, and end-to-end coverage.
