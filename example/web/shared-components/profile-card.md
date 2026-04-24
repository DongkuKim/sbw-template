---
id: profile-card
name: Profile Card
layer: web-shared-component
component_kind: custom
libraries:
  - shadcn
---

# Profile Card

## Intent

- `Problem`: reusable surfaces need a compact identity card with minimal content.
- `Target users`: end users scanning profile-related content blocks.
- `Non-goals`: data fetching, auth/session checks, navigation decisions.

## Purpose

Render a generic profile card with icon, name, and description.

## UX Contract

- `User actions`: view icon, name, and description content.
- `Expected outcomes`: users quickly understand who or what the card represents.
- `Constraints`: presentational only; no domain-specific logic.

## Public Interface

```tsx
<ProfileCard
  icon={<UserIcon />}
  name="Jane Doe"
  description="Product designer focused on growth."
/>
```

```ts
type ProfileCardProps = {
  icon?: React.ReactNode;
  name: string;
  description?: string;
};
```

- `Props`: `icon`, `name`, `description`.
- `Events`: none.

## State & Data

- `Core state`: no internal state.
- `Input data`: `icon`, `name`, `description` from parent.
- `Output data`: none.
- `Persistence expectations`: ephemeral render-only state.

## Structure

### Composition

```tsx
export function ProfileCard(props: ProfileCardProps) {
  return (
    <CardContainer>
      <IconArea>
        <IconSlot />
      </IconArea>
      <TextArea>
        <NameText />
        <DescriptionText />
      </TextArea>
    </CardContainer>
  );
}
```

### Composition Notes

- `Card container`: outer shell and spacing.
- `Icon area`: leading visual marker.
- `Text area`: name and description text stack.

## Elements

### `Card container`

- `Purpose`: provide outer shell and spacing.
- `Base components`: `shadcn/card`
- `Inputs`: optional class/layout props from parent.
- `States`: always present.
- `Responsive behaviors`: keeps spacing and layout consistency across breakpoints.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onChange>`: none.
  - `<onFocus>` / `<onOpen>`: none.

### `Icon slot`

- `Purpose`: render leading icon/avatar-like visual.
- `Base components`: `shadcn/avatar`
- `Inputs`: `icon` node.
- `States`: fallback placeholder when icon is absent.
- `Responsive behaviors`: fixed visual size, aligned with text block.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onChange>`: none.
  - `<onFocus>` / `<onOpen>`: none.

### `Name text`

- `Purpose`: render primary label.
- `Base components`: `shadcn/typography`
- `Inputs`: `name` string.
- `States`: always shown.
- `Responsive behaviors`: truncates or wraps per container rule.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onChange>`: none.
  - `<onFocus>` / `<onOpen>`: none.

### `Description text`

- `Purpose`: render secondary descriptive text.
- `Base components`: `shadcn/typography`
- `Inputs`: optional `description` string.
- `States`: hidden when description is absent.
- `Responsive behaviors`: wraps to available width.
- `Interaction events`:
  - `<onHover>`: none.
  - `<onClick>`: none.
  - `<onChange>`: none.
  - `<onFocus>` / `<onOpen>`: none.

## Usage Rules

- `Use when`: showing compact identity-style content with icon, name, and description.
- `Do not use when`: editing, actions, or status workflows are required.
- `Extension boundary`: parent can style placement, not component contract.
- `Acceptance criteria`: renders correctly with and without icon/description; no business logic.
