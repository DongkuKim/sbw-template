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

## Layout Usage

- `Layout`: `account-shell`
- `Header slot`: page title content for `Profile`
- `Body slot`: `user-summary-card` when profile summary data is available, otherwise lightweight inline fallback messaging owned by the view
- `Aside slot`: none

Route path is defined in front matter as `/profile`. Route protection follows the [standard web-product NFR profile](../../architecture/nfr-profiles/standard-web-product.md) instead of repeating guard rules here.

## Shared Component Usage

### `user-summary-card`

- `Placement`: `account-shell` `body` slot
- `When used`: rendered when the view has profile summary data to present; the view keeps empty and retryable error messaging outside this shared component
- `Inputs filled by view`:
  - `display name`: `profile.profileSummary.displayName`
  - `primary email`: `profile.profileSummary.primaryEmail`
  - `membership tier`: `profile.profileSummary.membershipTier`
  - `loading`: `profile.viewState == "loading"`
