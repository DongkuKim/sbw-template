---
id: your-shared-component-id
name: Your Shared Component Name
layer: web-shared-component
feature: your-feature-id
domain: your-domain-id
libraries:
  - shadcn
  - radix-ui
---

# Your Shared Component Name

> Copy and rename this file to define one shared presentational component.

## Purpose

Describe the reusable UI responsibility for this component.

## Composition

Describe how this shared component composes the listed libraries. Explain only the important top-level composition choices here. Put element-specific base components under each element in `## Elements`.

## Structure

Describe the internal area hierarchy of the component and where elements live. Include important regions, nested elements, and conditional variants such as alternate breadcrumb shapes, optional actions, or explicitly removed elements.

Recommended shape:

### Areas

- `Area name`: describe the purpose of each major region such as a top bar, content block, metadata rail, or action row.

### Elements

- `Element name`: name the element and note which area it belongs to.
- `Variant or condition`: note alternate cases such as `Domain > asset name` versus `Area > Domain > asset name`, or controls that are intentionally omitted.

## Elements

Document each element as its own subsection.

Recommended shape:

### `Element name`

- `Parent area`: where the element lives.
- `Purpose`: what the element is responsible for.
- `Base components`: list the primitives or library components used to build this element, such as `shadcn/typography` or `radix-ui/avatar`.
- `Inputs`: props, data dependencies, and rendering assumptions for this element.
- `States`: loading, empty, error, success, disabled, hidden, or variant-specific states for this element.
Interaction events:

`<onHover>`: describe the visual or behavioral change.
`<onClick>`: describe the navigation, save, pop-up, or other action.
`<onChange>`: describe input or value-change behavior when relevant.
`<onFocus>` or `<onOpen>`: describe keyboard or expanded-state behavior when relevant.

If an event does nothing, say so explicitly, for example `<onClick>: none.`

Repeat for every important element that another agent would need to implement or reuse correctly.

## Usage Rules

Describe where the component can be used and what logic must stay out of it.
