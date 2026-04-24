---
id: profile
name: Profile View
layer: web-view
domain: customer-identity
route: /profile
layout: account-shell
bff: profile
shared_components:
  - profile-card
---

# Profile View

## Purpose

Render a profile-oriented card inside the account experience.

## Layout Usage

- `Layout`: `account-shell`
- `Route guard`: signed-in session required before the view calls the BFF
- `Entry policy`: redirect to sign-in when session is missing
- `Slots filled by view`:
  - `header`: page title content for `Profile`
  - `body`: profile content states and `profile-card` success surface
  - `aside`: none

## Shared Component Usage

### `profile-card`

- `Placement`: `account-shell` `body` slot success surface.
- `When used`: rendered only when `viewState` is `success`.
- `Inputs filled by view`:
  - `icon`: derived from view-owned initials/avatar fallback mapping.
  - `name`: `profile.profileSummary.displayName`.
  - `description`: view-owned text mapping from available summary fields.

## Structure

### Composition

```tsx
export default function ProfileView() {
  return (
    <AccountShellLayout
      header={<ProfileHeaderTitle title="Profile" />}
      body={
        <ProfileBodyRegion>
          <LoadingNotice />
          <ErrorNotice />
          <EmptyNotice />
          <ProfileCardSurface />
        </ProfileBodyRegion>
      }
      aside={null}
    />
  );
}
```

### Composition Notes

- `header`: `ProfileHeaderTitle` renders static heading chrome for this route.
- `body`: `ProfileBodyRegion` renders one state surface at a time from BFF `viewState`.
- `aside`: intentionally unfilled.

## Elements

### `ProfileHeaderTitle`

- `Purpose`: provide page-level heading content for the layout `header` slot.
- `Shared components`: none
- `Structure notes`: renders static `Profile` title text.
- `Inputs mapped by view`: constant `"Profile"`.
- `State conditions`: always shown.
- `Interaction events`:
  - `<onClick>`: none.
  - `<onChange>`: none.
  - `<onSubmit>`: none.

### `ProfileBodyRegion`

- `Purpose`: own slot-level state selection and success content composition.
- `Shared components`: `profile-card` (success only)
- `Structure notes`: exactly one child surface shown per `viewState`.
- `Inputs mapped by view`:
  - `profile-card.icon`: derived from view-owned initials/avatar fallback mapping.
  - `profile-card.name`: `profile.profileSummary.displayName`.
  - `profile-card.description`: derived from `primaryEmail` and optional `membershipTier`.
- `State conditions`:
  - `loading`: lightweight inline loading message.
  - `retryable-error`: retryable inline error message owned by the view.
  - `not-found`: inline empty/not-found message.
  - `access-denied`: inline access-denied message.
  - `success`: render `profile-card`.
- `Interaction events`:
  - `<onClick>`: retry button triggers BFF refetch in `retryable-error`.
  - `<onChange>`: none.
  - `<onSubmit>`: none.
