# Error Model Standard

## Purpose

Ensure planning docs describe failure states in a way that can be implemented consistently and observed reliably.

## Rules

- Server specs define canonical error categories, status mapping, and retry guidance.
- BFF specs define partial-failure behavior, user-safe error surfaces, and fallback rules.
- Web view specs define loading, empty, error, and success states with actionable recovery paths.

## Build Notes

- Are expected failures classified rather than described loosely?
- Does each layer document what it hides, maps, or exposes?
- Can support staff understand how a failure appears end to end?
