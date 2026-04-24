---
id: your-shared-component-id
name: Your Shared Component Name
layer: web-shared-component
component_kind: custom
libraries:
  - library1
  - library2
---

# Your Shared Component Name

> Copy and rename this file to define a custom shared presentational component.

## Intent

- `Problem`: what this component solves.
- `Target users`: who benefits from this component.
- `Non-goals`: what this component intentionally does not solve.

## Purpose

Describe the reusable UI responsibility for this component.

## UX Contract

- `User actions`: what users can do with this component.
- `Expected outcomes`: what happens when those actions succeed.
- `Constraints`: key UX or product limits this component must respect.

## Public Interface

Document the component API in a practical, code-facing shape.

```tsx
<YourSharedComponent
  title="Profile"
  variant="default"
  onAction={(id) => {}}
/>
```

```ts
type YourSharedComponentProps = {
  title: string;
  variant?: "default" | "compact";
  onAction?: (id: string) => void;
};
```

- `Props`: rendering inputs and variants.
- `Events`: interaction callbacks.

## State & Data

- `Core state`: key internal state the component owns.
- `Input data`: required/optional input data shape.
- `Output data`: emitted values/events and their meaning.
- `Persistence expectations`: whether state is ephemeral, URL-backed, or server-backed.

## Structure

Describe the component as code-level composition (primitives + shared components).

### Composition

```tsx
export function YourSharedComponent(props: YourSharedComponentProps) {
  return (
    <Root>
      <Header />
      <Content />
      <Actions />
    </Root>
  );
}
```

### Composition Notes

- `Element name`: list each important element from the composition.
- `Variant or condition`: note optional rendering variants or feature-flag/conditional branches.
- `Slot`: if this component exposes any slot-like insertion points, name them and allowed content.

## Elements

Document each important element as its own subsection.

### `Element name`

- `Purpose`: what responsibility this element has.
- `Base components`: primitives used.
- `Inputs`: element-level inputs.
- `States`: key UI states.
- `Responsive behaviors`: how this element changes across breakpoints.
- `Interaction events`:
  - `<onHover>`: ...
  - `<onClick>`: ...
  - `<onChange>`: ...
  - `<onFocus>` / `<onOpen>`: ...

If no interaction is owned here, state it explicitly, for example `<onClick>: none.`

## Usage Rules

Describe where the component is used and how to apply its interface consistently.

- `Use when`: contexts where this component is the default choice.
- `Do not use when`: contexts that require a different component.
- `Extension boundary`: what can be customized without changing core behavior.
- `Acceptance criteria`: minimum conditions for implementation to be considered complete.
