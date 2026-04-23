---
id: user-summary-card
name: User Summary Card
layer: web-shared-component
domain: customer-identity
libraries:
  - shadcn
---

# User Summary Card

## Purpose

Render a concise summary of the signed-in user's profile information inside account surfaces.

## Composition

This component wraps shared `shadcn` building blocks into a stable product-level card. The component uses a card shell, a text hierarchy, loading placeholders, and a membership indicator, but the exact primitives are documented under each element.

## Structure

### Areas

- `Card container`: provides the outer shell, spacing, and border treatment.
- `Header text block`: groups the user's name and primary email.
- `Membership status area`: holds the membership tier badge.

### Elements

- `Display name`: primary text in the header block.
- `Primary email`: secondary text below the display name.
- `Membership tier badge`: compact status element inside the membership status area.
- `Loading skeletons`: replace the text and badge elements while preserving the same overall layout footprint.

## Elements

### `Display name`

- `Parent area`: `Header text block`
- `Purpose`: render the user's primary label in the card.
- `Base components`: `shadcn/typography`
- `Inputs`: display name string from the parent view.
- `States`: populated when profile data is available; hidden while loading skeletons are shown.
Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Primary email`

- `Parent area`: `Header text block`
- `Purpose`: render the user's secondary identifier below the display name.
- `Base components`: `shadcn/typography`
- `Inputs`: primary email string from the parent view.
- `States`: populated when profile data is available; hidden while loading skeletons are shown.
Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Membership tier badge`

- `Parent area`: `Membership status area`
- `Purpose`: show the current membership tier with compact emphasis.
- `Base components`: `shadcn/badge`
- `Inputs`: membership tier value from the parent view.
- `States`: shown on successful data load; hidden when the user has no tier or loading skeletons are active.
Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Loading skeletons`

- `Parent area`: `Header text block` and `Membership status area`
- `Purpose`: preserve layout footprint while profile content is loading.
- `Base components`: `shadcn/skeleton`
- `Inputs`: loading boolean from the parent view.
- `States`: shown only during loading; removed once content or an error placeholder is available.
Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Card container`

- `Parent area`: root container
- `Purpose`: provide the outer shell, spacing, and border treatment for the whole component.
- `Base components`: `shadcn/card`
- `Inputs`: optional class or layout props controlled by the parent view.
- `States`: always present in loading, success, and compact error rendering.
Interaction events:
`<onHover>`: none unless a parent view adds a wrapper affordance.
`<onClick>`: none inside the shared component. Parent views may wrap the component if they need navigation behavior.

## Usage Rules

The component is presentational only. It does not fetch data, inspect session state, or decide product behavior.
