# Dependency Direction Rules

## Purpose

Make dependency direction an explicit planning concern so implementation does not drift into cyclical or convenience-based coupling.

## Rules

- `transport -> application -> domain` is the only allowed inward dependency direction.
- `integrations` implement application ports and may depend on contracts but never on web layers.
- `web/views` may consume a BFF contract only and may not consume `server/` contracts directly.
- `web/layouts` and `web/shared-components` stay reusable and must not own business rules.

## Build Notes

- Does every dependency point inward toward policy?
- Is every downstream API call initiated from BFF or server integration boundaries only?
- Would removing a web layout or shared component leave business rules intact?
