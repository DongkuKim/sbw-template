---
id: account-shell
name: Account Shell
layer: web-layout
domain: customer-identity
slots:
  - header
  - body
  - aside
---

# Account Shell

## Purpose

Provide a reusable authenticated account page shell with navigation and a content slot for account views.

## Structure

### Composition

```tsx
export default function AccountShellLayout() {
  return (
    <ShellRoot>
      <HeaderRail>
        <HeaderSlotFrame>{/* slot: header */}</HeaderSlotFrame>
      </HeaderRail>
      <ContentGrid>
        <BodySlotFrame>{/* slot: body */}</BodySlotFrame>
        <AsideSlotFrame>{/* slot: aside (optional) */}</AsideSlotFrame>
      </ContentGrid>
    </ShellRoot>
  );
}
```

### Composition Notes

- `Shell root`: page-level container for the authenticated account experience.
- `Header rail`: persistent top region containing `Header slot frame`.
- `Content grid`: main region containing `Body slot frame` and optional `Aside slot frame`.

## Elements

### `Header slot frame`

- `Purpose`: anchor the page heading and top-of-page shell chrome.
- `Shared components`: none
- `Slot usage`: owns the `header` slot for page-level title, breadcrumbs, or view-specific actions.
- `Structure notes`: stays at the top of the shell and spans the full content width.
- `Responsive behavior`: remains first in document order across breakpoints.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onOpen>` / `<onClose>`: none.

### `Body slot frame`

- `Purpose`: provide the primary content container for the view.
- `Shared components`: none
- `Slot usage`: owns the `body` slot and renders the main content surface.
- `Structure notes`: takes the primary grid column and defines the reading flow for account pages.
- `Responsive behavior`: remains primary content on all breakpoints and stacks above the aside when the layout collapses to one column.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onOpen>` / `<onClose>`: none.

### `Aside slot frame`

- `Purpose`: host optional support or contextual secondary content.
- `Shared components`: none
- `Slot usage`: owns the optional `aside` slot.
- `Structure notes`: renders only when a view provides aside content.
- `Responsive behavior`: appears as a secondary column on larger screens and stacks below the body slot on smaller screens.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onOpen>` / `<onClose>`: none.

## Usage Rules

The layout remains presentational and structure-focused. Feature decisions, data loading, and server-facing behavior stay in the view and BFF layers.
