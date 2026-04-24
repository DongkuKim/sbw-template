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

Describe the layout as code-level composition (layout primitives + shared components), including where slots and persistent shell elements live.

Recommended shape:

### Composition

```tsx
export default function YourPageLayout() {
  return (
    <PageShell direction="col" height="100vh">
      <TopBar height={64} />

      <Main direction="col" topOffset={64} height="calc(100vh - 64px)">
        <FilterRow height={56} direction="row" wrapOnMobile />

        <Body direction="col" flex={1}>
          <PrimaryArea flex={1} />
          <SecondaryArea width={360} hiddenBelow="lg" />
          <PaginationRow height={48} align="end" />
        </Body>
      </Main>

      <ModalHost />
      <DrawerHost />
      <ToastHost />
    </PageShell>
  );
}
```

### Composition Notes

- `Element name`: list each important structural element from the composition.
- `Slot or condition`: note the slot it owns, whether it is persistent layout chrome, and any optional or responsive conditions.

## Elements

Document each important layout element as its own subsection.

Recommended shape:

### `Element name`

- `Purpose`: what structural responsibility the element has in the layout.
- `Shared components`: list the shared components used by this element, or say `none`.
- `Slot usage`: describe which slot this element owns, wraps, or exposes and what kind of content belongs there.
- `Structure notes`: describe positioning, containment, sticky behavior, ordering, or other structure-specific rules.
- `Responsive behavior`: describe how the element moves, stacks, hides, or changes across breakpoints.
- `Interaction events`: list layout-owned events only using explicit notation:
  - `<onHover>`: ...
  - `<onClick>`: ...
  - `<onOpen>` / `<onClose>`: ...

If the layout does not own interactions for this element, say so explicitly, for example `<onClick>: none.`

## Usage Rules

Describe reuse constraints and what logic must stay out of the layout.
