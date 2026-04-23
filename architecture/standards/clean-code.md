# Clean Code Baseline

## Purpose

Define the default code organization expectations that every plan should respect before implementation begins.

## Rules

- Business rules live in `domain`, not in transport handlers or UI composition code.
- Application orchestration belongs in `application` use cases and ports.
- Integrations translate external concerns into internal contracts without leaking vendor details upward.
- Shared web components stay presentational and do not own feature decisions.

## Build Notes

- Can an implementer point to where business rules will live before code exists?
- Does the plan separate orchestration from transport and integration work?
- Are shared web artifacts free of product-specific branching logic?
