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

Describe the referenced layout and how this view inherits it and fills its slots.

The route path belongs in front matter under `route`. Route guards and entry policy should be documented here when they affect the view.

Recommended shape:

- `Layout`: name the layout used by this view.
- `Route guard`: describe auth or entry requirements, or say `none`.
- `Entry policy`: describe preconditions or redirects needed before render, or say `none`.
- `Slots filled by view`: list each layout slot this view fills and what it places there.

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

## Structure

Describe the view as code-level composition (layout primitives + shared components), including explicit slot filling for the inherited layout.

Recommended shape:

### Composition

```tsx
export default function YourView() {
  return (
    <YourLayout
      header={
        <HeaderRegion>
          <SharedHeroBanner />
        </HeaderRegion>
      }
      body={
        <ViewRoot direction="col" gap={16}>
          <ContentRegion direction="row" gap={16}>
            <PrimaryColumn flex={1}>
              <SharedPrimaryPanel />
            </PrimaryColumn>

            <SecondaryColumn width={320} hiddenBelow="lg">
              <SharedSecondaryPanel />
            </SecondaryColumn>
          </ContentRegion>
        </ViewRoot>
      }
      aside={
        <AsideRegion>
          <SharedSecondaryPanel />
        </AsideRegion>
      }
    />
  );
}
```

Alternative slot API style:

```tsx
export default function YourView() {
  return (
    <YourLayout>
      <LayoutSlotHeader>
        <HeaderRegion>
          <SharedHeroBanner />
        </HeaderRegion>
      </LayoutSlotHeader>

      <LayoutSlotBody>
        <ViewRoot direction="col" gap={16}>
          <SharedPrimaryPanel />
        </ViewRoot>
      </LayoutSlotBody>

      <LayoutSlotAside>
        <AsideRegion>
          <SharedSecondaryPanel />
        </AsideRegion>
      </LayoutSlotAside>
    </YourLayout>
  );
}
```

### Composition Notes

- `Slot name`: list each layout slot filled by the view.
- `Element name`: list each important structural element inside each slot.
- `Condition`: note optional, loading, empty, error, or responsive conditions.

## Elements

Document each important view-owned element as its own subsection.

Recommended shape:

### `Element name`

- `Purpose`: what responsibility this element has in the view.
- `Shared components`: list shared components this element composes, or say `none`.
- `Structure notes`: describe containment, ordering, or visibility rules.
- `Inputs mapped by view`: list input mappings from route params, BFF fields, derived values, or constants.
- `State conditions`: describe loading, empty, error, and success behavior for this element.
- `Interaction events`: list view-owned events only using explicit notation:
  - `<onClick>`: ...
  - `<onChange>`: ...
  - `<onSubmit>`: ...

If the view does not own interactions for this element, say so explicitly, for example `<onClick>: none.`
