# Vertical Slice BFF Planning Baseline

## Context

The template needs to force clean boundaries before implementation and prevent teams from defaulting to horizontal controller or service buckets that mix business rules, transport details, and downstream integration concerns.

## Decision

The default planning model is a vertical slice BFF architecture. Each feature must describe the future `transport`, `application`, `domain`, `integrations`, `contracts`, and `tests` boundaries before code is written.

## Consequences

Implementation plans now need to be explicit about where orchestration, business rules, adapters, and schemas will live. Teams gain cleaner implementation guidance and faster onboarding, but they must do more design work up front.
