# AGENTS.md

Canonical guide for AI agents using this template.

This repository has two primary uses:

1. Write or update the planning docs that define a product or feature.
2. Implement a product or feature from completed planning docs.

Use this file as the operational guide. Use the Markdown files in the repo as the actual planning source of truth.

## What This Template Is For

This template describes a product through linked Markdown specs before implementation starts.

- `features/` defines the feature slice and links the rest of the plan together.
- `domains/` defines canonical terminology, entities, invariants, and lifecycle rules.
- `server/` defines backend API contracts.
- `bff/` defines web-facing orchestration and response shaping.
- `web/views/` defines routes, layout usage, shared-component composition, and view-owned input mapping.
- `web/layouts/` defines reusable page shells.
- `web/shared-components/` defines reusable presentational building blocks.
- `example/` contains a worked example that mirrors the same planning structure, including `example/architecture/` for concrete example reference docs.
- `architecture/` contains reusable templates and shared reference docs for cross-cutting concerns.
- `.sbw-template/` contains the validator, schemas, and tests for the template itself.

Editable planning input lives in `features/`, `domains/`, `server/`, `bff/`, `web/`, and sometimes `architecture/`. The `example/` tree is a worked reference that uses the same format but should not be treated as the primary planning surface for a new product.

Do not edit `.sbw-template/` unless your task is to maintain the template contract, validator, or validator tests.

## Source Of Truth Rules

Treat each doc type as authoritative for a specific concern.

- `feature` is authoritative for product goal, scope, slice membership, linked docs, and the implementation boundary at slice level.
- `domain` is authoritative for canonical names, entities, invariants, and lifecycle rules.
- `web-view` is authoritative for route identity, which layout and shared components are used, and how the view maps route or BFF values into shared-component inputs.
- `web-layout` is authoritative for shell structure, slot behavior, and the per-element shared-component composition owned by the layout.
- `web-shared-component` is authoritative for reusable presentational behavior, internal structure, and the per-element base components, inputs, states, and interactions it composes from the listed UI libraries.
- `bff` is authoritative for the web-facing contract, orchestration flow, failure handling, and data protection at the web boundary.
- `server` is authoritative for backend request and response contracts, auth/authz behavior, error model, and operational policy.
- `architecture` docs are shared reference material. Use them when linked from a feature or runtime doc, or when they express a repo-wide default that is not overridden by a more specific doc.

When docs appear to overlap, prefer the more specific owning doc type over a broader one.

- `domain` beats `feature` for terminology and invariants.
- `server` beats `bff` for backend wire contract details.
- `bff` beats `web-view` for the web-facing data contract.
- `web-view` beats `feature` for route-specific UI behavior.
- A feature-specific exception stated in a runtime doc beats a generic architecture reference.

If two docs truly conflict and the conflict is not obviously “default vs exception,” stop and resolve the discrepancy before implementation.

## Link Instead Of Repeat

This template is optimized for linked canonical docs, not duplicated prose.

- Use front matter ids for machine-readable links required by the schema.
- Use Markdown links in body sections like `Linked Specs` when an agent should open the referenced file directly.
- Put shared rules such as auth, error handling, observability, or clean-architecture defaults in one architecture doc and link to it instead of re-explaining it in every feature.
- Only repeat information when a layer-specific transformation, narrowing, or exception must be explicit.

Prefer canonical link direction:

- `feature` links to the docs that make up the slice.
- `web/views` links to `web/layouts`, `web/shared-components`, and `bff`.
- `bff` links to `server`.

Do not invent reverse links or duplicate mapping tables unless the schema requires them.

## Workflow 1: Author Or Update Specs

Use this workflow when the task is to create, refine, or correct the planning docs.

### Authoring Order

1. Start with the feature.
2. Define or refine the domain.
3. Define the runtime docs:
   - `server/`
   - `bff/`
   - `web/views/`
   - `web/layouts/`
   - `web/shared-components/`
4. Add or link optional `architecture/` reference docs only when they provide reusable cross-cutting context.
5. Run validation.

### Authoring Checklist

- Copy the appropriate starter template and rename the file to the final `id`.
- Keep filenames aligned with front matter `id`.
- Fill required front matter and required sections.
- For `web/views`, keep the body focused on layout usage and shared-component usage. Document which layout slots are filled and how the view maps values into each shared-component input. Keep route path in front matter and put route-guard policy in the linked NFR profile instead of the view body.
- For `web/layouts`, document the internal area tree in `## Structure`, then document each important layout element in `## Elements` with its shared components, slot usage, structure notes, and responsive behavior.
- For `web/shared-components`, document the machine-readable `libraries` list in front matter.
- For `web/shared-components`, document the internal area tree in `## Structure`, then document each important element in `## Elements` with its base components, inputs, states, and interactions. Write interactions using explicit event notation like `<onHover>: ...`, `<onClick>: ...`, and `<onChange>: ...`. Name major areas and then name the elements inside them so another agent can map the spec directly to component structure.
- Prefer links to existing canonical docs instead of copying shared constraints.
- Make implementation boundaries concrete enough that another agent could build from them without making architecture decisions.
- Ensure feature, domain, server, BFF, and web docs all point to the correct linked ids.

### Starter Templates

- [features/feature-template.md](./features/feature-template.md)
- [domains/domain-template.md](./domains/domain-template.md)
- [server/server-api-template.md](./server/server-api-template.md)
- [bff/view-bff-template.md](./bff/view-bff-template.md)
- [web/views/view-template.md](./web/views/view-template.md)
- [web/layouts/layout-template.md](./web/layouts/layout-template.md)
- [web/shared-components/shared-component-template.md](./web/shared-components/shared-component-template.md)

## Workflow 2: Implement From Completed Specs

Use this workflow when the planning docs already exist and your job is to build the product or feature they describe.

### Read Order

Read the docs in this order:

1. feature
2. domain
3. web view
4. linked layout and shared components
5. bff
6. server
7. linked architecture docs

Suggested starting example:

- [example/features/profile-experience.md](./example/features/profile-experience.md)
- [example/domains/customer-identity.md](./example/domains/customer-identity.md)
- [example/architecture/adrs/adr-001-vertical-slice-bff.md](./example/architecture/adrs/adr-001-vertical-slice-bff.md)
- [example/architecture/nfr-profiles/standard-web-product.md](./example/architecture/nfr-profiles/standard-web-product.md)
- [example/web/views/profile.md](./example/web/views/profile.md)
- [example/web/layouts/account-shell.md](./example/web/layouts/account-shell.md)
- [example/web/shared-components/user-summary-card.md](./example/web/shared-components/user-summary-card.md)
- [example/bff/profile.md](./example/bff/profile.md)
- [example/server/get-user-profile.md](./example/server/get-user-profile.md)

### Implementation Checklist

- Start from the feature goal and scope so you know what is in and out.
- Use the domain doc to normalize names and business rules before writing code.
- Build the web layer against the BFF contract, not directly against the server contract.
- Use each view doc as the canonical source for layout choice, shared-component composition, and the value mapping from BFF or route data into shared-component inputs.
- Use the linked NFR profile for web entry and route-guard policy instead of looking for those rules in the view body.
- Use each layout doc as the canonical source for shell structure, slot ownership, responsive layout behavior, and any layout-owned shared components.
- Use each shared-component doc as the canonical source for which UI libraries, internal areas, and per-element base components, inputs, states, and interactions must be composed in the implementation. Treat named areas and named elements as the target component breakdown unless the spec explicitly says they are optional or removed.
- Build the BFF against the server contracts, applying any mapping, aggregation, redaction, or failure translation described there.
- Use linked architecture docs for shared defaults like auth, error handling, or clean architecture when they are referenced by the feature or runtime docs.
- Respect the implementation boundary described in the feature, BFF, and server docs. Do not collapse transport, application, domain, integrations, contracts, and tests into one layer unless the plan explicitly says so.

## Optional Architecture References

Use these root docs when a feature or runtime doc links to them, or when you need the reusable repo default for a cross-cutting concern.

- [architecture/adrs/adr-template.md](./architecture/adrs/adr-template.md)
- [architecture/standards/clean-code.md](./architecture/standards/clean-code.md)
- [architecture/standards/dependency-rules.md](./architecture/standards/dependency-rules.md)
- [architecture/standards/auth-model.md](./architecture/standards/auth-model.md)
- [architecture/standards/error-model.md](./architecture/standards/error-model.md)
- [architecture/standards/observability.md](./architecture/standards/observability.md)
- [architecture/standards/testing-and-release.md](./architecture/standards/testing-and-release.md)
- [architecture/nfr-profiles/nfr-profile-template.md](./architecture/nfr-profiles/nfr-profile-template.md)

## Validation

After changing validated docs, run:

```bash
make validate
make test
```

Use `.sbw-template/` only if your task is to maintain the validator or the validated schema itself.
