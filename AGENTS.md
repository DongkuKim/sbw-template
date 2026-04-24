# AGENTS.md

Canonical guide for AI agents using this template.

This repository has two primary uses:

1. Write or update the planning docs that define a product surface.
2. Implement a product surface from completed planning docs.

Use this file as the operational guide. Use the Markdown files in the repo as the actual planning source of truth.

## What This Template Is For

This template describes a product through linked Markdown specs before implementation starts.

- `domains/` defines canonical terminology, entities, invariants, and lifecycle rules.
- `server/` defines backend API contracts.
- `bff/` defines web-facing orchestration and response shaping.
- `web/views/` defines fully domain-specific route surfaces that select a layout and map domain/BFF values into shared-component inputs to compose complete view components.
- `web/layouts/` defines reusable page shells with slot boundaries; layouts can compose shared components but should not own route policy or data fetching.
- `web/shared-components/` defines pure, non-domain reusable presentational building blocks. Shared components are either `custom` components or `wrapper` components around upstream primitives.
- `example/` contains a worked example that mirrors the same planning structure.
- `.sbw-template/` contains the validator, schemas, and tests for the template itself.

Editable planning input lives in `domains/`, `server/`, `bff/`, and `web/`. The `example/` tree is a worked reference that uses the same format but should not be treated as the primary planning surface for a new product.

Do not edit `.sbw-template/` unless your task is to maintain the template contract, validator, or validator tests.

## Source Of Truth Rules

Treat each doc type as authoritative for a specific concern.

- `domain` is authoritative for canonical names, entities, invariants, and lifecycle rules.
- `web-view` is authoritative for fully domain-specific route identity, layout selection, shared-component composition, and mapping route/BFF/domain values into shared-component inputs.
- `web-layout` is authoritative for shell structure, slot behavior, and the per-element shared-component composition owned by the layout.
- `web-shared-component` is authoritative for pure non-domain reusable presentational behavior, public interface, internal structure, and the per-element base components, inputs, states, and interactions it composes from the listed UI libraries.
- `bff` is authoritative for the web-facing contract, orchestration flow, failure handling, and data protection at the web boundary.
- `server` is authoritative for backend request and response contracts, auth/authz behavior, error model, and operational policy.

When docs appear to overlap, prefer the more specific owning doc type over a broader one.

- `server` beats `bff` for backend wire contract details.
- `bff` beats `web-view` for the web-facing data contract.

If two docs truly conflict and the conflict is not obviously “default vs exception,” stop and resolve the discrepancy before implementation.

## Link Instead Of Repeat

This template is optimized for linked canonical docs, not duplicated prose.

- Use front matter ids for machine-readable links required by the schema.
- Use Markdown links in body sections like `Linked Specs` when an agent should open the referenced file directly.
- Put shared rules in the most appropriate owning runtime doc and link to that doc instead of re-explaining the same rule in multiple places.
- Only repeat information when a layer-specific transformation, narrowing, or exception must be explicit.

Prefer canonical link direction:

- `domain` is linked from the runtime docs that depend on it.
- `web/views` links to `web/layouts`, `web/shared-components`, and `bff`.
- `bff` links to `server`.

Do not invent reverse links or duplicate mapping tables unless the schema requires them.

## Workflow 1: Author Or Update Specs

Use this workflow when the task is to create, refine, or correct the planning docs.

### Authoring Order

1. Start with the domain.
2. Define the runtime docs:
   - `server/`
   - `bff/`
   - `web/views/`
   - `web/layouts/`
   - `web/shared-components/`
3. Run validation.

### Authoring Checklist

- Copy the appropriate starter template and rename the file to the final `id`.
- Keep filenames aligned with front matter `id`.
- Fill required front matter and required sections.
- For `bff`, document `## BFF Path`, request/response types in `## BFF API (Web-facing)`, orchestration, downstream server API usage, failure mapping, data protection, and implementation boundaries.
- For `web/views`, keep the body focused on fully domain-specific layout/shared-component composition. Document which layout slots are filled, how domain/BFF/route values map into each shared-component input, and any route guard or entry policy the view depends on. Keep route path in front matter.
- For `web/layouts`, document the layout as code-level composition in `## Structure`, then document each important layout element in `## Elements` with its shared components, slot usage, structure notes, and responsive behavior.
- For `web/shared-components`, keep them pure non-domain and document the machine-readable `component_kind` and `libraries` fields in front matter. Use `component_kind: custom` for real custom components and `component_kind: wrapper` plus `wraps` for restricted wrappers around upstream primitives.
- For `web/shared-components`, document the public interface, component structure, and each important element with its base components, inputs, states, and interactions. Write interactions using explicit event notation like `<onHover>: ...`, `<onClick>: ...`, and `<onChange>: ...`. Name major areas and then name the elements inside them so another agent can map the spec directly to component structure.
- Prefer links to existing canonical docs instead of copying shared constraints.
- Make implementation boundaries concrete enough that another agent could build from them without making major structural decisions.
- Ensure domain, server, BFF, and web docs all point to the correct linked ids.

### Starter Templates

- [domains/domain-template.md](./domains/domain-template.md)
- [server/server-api-template.md](./server/server-api-template.md)
- [bff/view-bff-template.md](./bff/view-bff-template.md)
- [web/views/view-template.md](./web/views/view-template.md)
- [web/layouts/layout-template.md](./web/layouts/layout-template.md)
- [web/shared-components/shared-component-template.md](./web/shared-components/shared-component-template.md)
- [web/shared-components/shared-component-custom-template.md](./web/shared-components/shared-component-custom-template.md)
- [web/shared-components/shared-component-wrapper-template.md](./web/shared-components/shared-component-wrapper-template.md)

## Workflow 2: Implement From Completed Specs

Use this workflow when the planning docs already exist and your job is to build the product surface they describe.

### Read Order

Read the docs in this order:

1. domain
2. web view
3. linked layout and shared components
4. bff
5. server

Suggested starting example:

- [example/domains/customer-identity.md](./example/domains/customer-identity.md)
- [example/web/views/profile.md](./example/web/views/profile.md)
- [example/web/layouts/account-shell.md](./example/web/layouts/account-shell.md)
- [example/web/shared-components/profile-card.md](./example/web/shared-components/profile-card.md)
- [example/bff/profile.md](./example/bff/profile.md)
- [example/server/get-user-profile.md](./example/server/get-user-profile.md)

### Implementation Checklist

- Start from the domain doc to normalize names and business rules before writing code.
- Use the view, BFF, and server purposes together to understand scope and expected behavior.
- Build the web layer against the BFF contract, not directly against the server contract.
- Use each view doc as the canonical source for domain-specific layout choice, shared-component composition, and the value mapping from BFF/route/domain data into shared-component inputs.
- Use the view doc for web entry and route-guard policy instead of looking for those rules elsewhere.
- Use each layout doc as the canonical source for shell structure, slot ownership, responsive layout behavior, and any layout-owned shared components.
- Use each shared-component doc as the canonical source for pure non-domain UI libraries, public interface, internal areas, and per-element base components, inputs, states, and interactions that must be composed in the implementation. Treat named areas and named elements as the target component breakdown unless the spec explicitly says they are optional or removed.
- Build the BFF against the server contracts, applying any mapping, aggregation, redaction, or failure translation described there.
- Respect the implementation boundary described in the BFF and server docs. Do not collapse transport, application, domain, integrations, contracts, and tests into one layer unless the plan explicitly says so.

## Validation

After changing validated docs, run:

```bash
make validate
make test
```

Use `.sbw-template/` only if your task is to maintain the validator or the validated schema itself.
