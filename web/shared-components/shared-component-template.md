---
id: your-shared-component-id
name: Your Shared Component Name
layer: web-shared-component
component_kind: custom
libraries:
  - shadcn
---

# Your Shared Component Name

> Use one of the two templates below based on component type.

## Choose Template

- Custom template:
  - [shared-component-custom-template.md](./shared-component-custom-template.md)
- Wrapper template:
  - [shared-component-wrapper-template.md](./shared-component-wrapper-template.md)

## Rule

Use exactly one template per shared component spec.

## Required Frontmatter Rule

- Always set `component_kind`:
  - `custom`: for fully custom shared components.
  - `wrapper`: for restricted wrappers around upstream primitives.
- When `component_kind` is `wrapper`, add `wraps` with the wrapped primitive or component id, for example `shadcn/button`.

## Shared Component Boundary

Shared components are reusable presentational building blocks. Keep route policy, domain decisions, data fetching, server calls, and BFF-specific mapping in the owning view/BFF docs.
