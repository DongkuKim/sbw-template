---
id: profile
name: Profile View
layer: web-view
feature: profile-experience
domain: customer-identity
route: /profile
layout: account-shell
bff: profile
shared_components:
  - user-summary-card
---

# Profile View

## Purpose

Render the signed-in user's profile summary inside the account experience.

## Route and Guards

The route is `/profile` and requires an authenticated user session before the BFF call is made.

## Layout Usage

- `Layout`: `account-shell`
- `Header slot`: page title content for `Profile`
- `Body slot`: `user-summary-card` when profile summary data is available, otherwise lightweight inline fallback messaging owned by the view
- `Aside slot`: none

## Shared Component Usage

### `user-summary-card`

- `Placement`: `account-shell` `body` slot
- `When used`: rendered when the view has profile summary data to present; the view keeps empty and retryable error messaging outside this shared component
- `Inputs filled by view`:
  - `display name`: `profile.profileSummary.displayName`
  - `primary email`: `profile.profileSummary.primaryEmail`
  - `membership tier`: `profile.profileSummary.membershipTier`
  - `loading`: `profile.viewState == "loading"`
