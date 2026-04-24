---
id: your-shared-wrapper-id
name: Your Shared Wrapper Name
layer: web-shared-component
component_kind: wrapper
libraries:
  - shadcn
wraps: shadcn/<component-name>
---

# Your Shared Wrapper Name

> Copy and rename this file to define a restricted wrapper around an upstream primitive.

## Purpose

Describe the unified behavior this wrapper enforces across the project.

## Wrapped Component

- `Source`: upstream primitive path and name.

## Public Interface

Document the exposed API in a practical, code-facing shape.

```tsx
<YourWrapper size="md" intent="default" onAction={() => {}}>
  Label
</YourWrapper>
```

```ts
type YourWrapperProps = {
  size?: "sm" | "md" | "lg";
  intent?: "default" | "danger";
  onAction?: () => void;
};
```

- `Props`: only project-approved inputs.
- `Events`: only project-approved callbacks.

## Wrapper Contract

- `Allowed props`: list props accepted by wrapper.
- `Blocked props`: list omitted/forbidden upstream props.
- `Enforced defaults`: tokens, variant defaults, a11y defaults.
- `Project invariants`: required behavior this wrapper guarantees.

## Structure

If this wrapper only forwards to one primitive without structural changes, state `No additional structure`.

### Composition

```tsx
export function YourWrapper(props: YourWrapperProps) {
  return (
    <Root>
      <WrappedPrimitive />
      <Affordance />
    </Root>
  );
}
```

### Composition Notes

- `Element name`: list each wrapper-owned element.
- `Condition`: note optional rendering conditions.

## Elements

Document each important wrapper-owned element as its own subsection.

### `Element name`

- `Purpose`: structural responsibility.
- `Base components`: wrapped primitive(s) and helper primitives.
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

Describe where this wrapper must be used and direct-primitive usage limits.
