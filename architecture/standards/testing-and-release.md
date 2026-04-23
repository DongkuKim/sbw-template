# Testing and Release Standard

## Purpose

Keep implementation plans honest by requiring the expected test and release strategy before any code is started.

## Rules

- Every feature, BFF, and server spec includes a `tests` boundary entry.
- Features define acceptance scenarios, rollout gates, and backout steps.
- Contract changes require explicit contract-test coverage and compatibility notes.

## Build Notes

- Are the required test layers named before implementation?
- Does the rollout plan say how to stop or reverse the change?
- Would another engineer know what must be verified in CI and staging?
