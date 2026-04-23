---
id: your-layout-id
name: Your Layout Name
layer: web-layout
domain: your-domain-id
slots:
  - body
---

# Your Layout Name

> Copy and rename this file to define one reusable layout.

## Purpose

Describe the shell or structure this layout provides.

## Structure

Describe the area hierarchy of the layout and where slots or persistent shell elements live.

Recommended shape:

### Areas

- `Area name`: describe each major region such as a top bar, content grid, side rail, or footer shell.

### Elements

- `Element name`: name each important structural element and note which area it belongs to.
- `Slot or condition`: note the slot it owns, whether it is persistent layout chrome, and any optional or responsive conditions.

## Elements

Document each important layout element as its own subsection.

Recommended shape:

### `Element name`

- `Parent area`: where the element lives.
- `Purpose`: what structural responsibility the element has in the layout.
- `Shared components`: list the shared components used by this element, or say `none`.
- `Slot usage`: describe which slot this element owns, wraps, or exposes and what kind of content belongs there.
- `Structure notes`: describe positioning, containment, sticky behavior, ordering, or other structure-specific rules.
- `Responsive behavior`: describe how the element moves, stacks, hides, or changes across breakpoints.

Interaction events:
`<onHover>`: describe behavior only when the layout owns it.
`<onClick>`: describe behavior only when the layout owns it.
`<onOpen>` or `<onClose>`: describe layout-owned disclosure behavior when relevant.

If the layout does not own any interaction for this element, say so explicitly, for example `<onClick>: none.`

## Usage Rules

Describe reuse constraints and what logic must stay out of the layout.
