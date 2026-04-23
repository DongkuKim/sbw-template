---
id: account-shell
name: Account Shell
layer: web-layout
feature: profile-experience
domain: customer-identity
slots:
  - header
  - body
  - aside
---

# Account Shell

## Purpose

Provide a reusable authenticated account page shell with navigation and a content slot for account features.

## Structure

### Areas

- `Shell root`: page-level container for the authenticated account experience.
- `Header rail`: persistent top region for shell chrome and page heading content.
- `Content grid`: main structural region that arranges body content with an optional aside.

### Elements

- `Header slot frame`: structural wrapper for the `header` slot inside the `Header rail`.
- `Body slot frame`: primary content wrapper for the `body` slot inside the `Content grid`.
- `Aside slot frame`: optional support-content wrapper for the `aside` slot inside the `Content grid`.

## Elements

### `Header slot frame`

- `Parent area`: `Header rail`
- `Purpose`: anchor the page heading and top-of-page shell chrome.
- `Shared components`: none
- `Slot usage`: owns the `header` slot for page-level title, breadcrumbs, or view-specific actions.
- `Structure notes`: stays at the top of the shell and spans the full content width.
- `Responsive behavior`: remains first in document order across breakpoints.

Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Body slot frame`

- `Parent area`: `Content grid`
- `Purpose`: provide the primary feature-content container for the view.
- `Shared components`: none
- `Slot usage`: owns the `body` slot and renders the main feature surface.
- `Structure notes`: takes the primary grid column and defines the reading flow for account pages.
- `Responsive behavior`: remains primary content on all breakpoints and stacks above the aside when the layout collapses to one column.

Interaction events:
`<onHover>`: none.
`<onClick>`: none.

### `Aside slot frame`

- `Parent area`: `Content grid`
- `Purpose`: host optional support or contextual secondary content.
- `Shared components`: none
- `Slot usage`: owns the optional `aside` slot.
- `Structure notes`: renders only when a view provides aside content.
- `Responsive behavior`: appears as a secondary column on larger screens and stacks below the body slot on smaller screens.

Interaction events:
`<onHover>`: none.
`<onClick>`: none.

## Usage Rules

The layout remains presentational and structure-focused. Feature decisions, data loading, and server-facing behavior stay in the view and BFF layers.
