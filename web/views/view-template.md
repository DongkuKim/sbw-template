---
id: your-view-id
name: Your View Name
layer: web-view
domain: your-domain-id
route: /your-route
layout: your-layout-id
bff: your-bff-id
shared_components:
  - your-shared-component-id
---

# Your View Name

> Copy and rename this file to define one web view contract.

## Purpose

Describe the user goal and responsibility of this view.

## Layout Usage

Describe the referenced layout and how the view fills its slots.

The route path belongs in front matter under `route`. Route guards and entry policy should be documented here when they affect the view.

Recommended shape:

- `Layout`: name the layout used by this view.
- `Route guard`: describe auth or entry requirements, or say `none`.
- `Header slot`: describe what the view places here, or say `none`.
- `Body slot`: describe the primary content or shared components placed here.
- `Aside slot`: describe optional secondary content, or say `none`.

## Shared Component Usage

Document each shared component the view uses and exactly how the view fills its inputs.

Recommended shape:

### `shared-component-id`

- `Placement`: which layout slot or view region this component appears in.
- `When used`: when the view renders this component, including important conditions if needed.
- `Inputs filled by view`:
  - `input name`: where the value comes from, such as a BFF field, route param, derived view value, or constant.
  - `input name`: note any transformation, fallback, or omission the view applies before passing the value.

If a shared component is not used for a state, document that in the `When used` line instead of repeating a separate view-state section.
