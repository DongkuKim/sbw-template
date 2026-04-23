# Auth Model Standard

## Purpose

Make authentication and authorization requirements explicit during planning so protected flows do not rely on implementation-time guesswork.

## Rules

- Web views state route guards and entry requirements.
- BFF specs define session inputs, authorization checks, and data redaction responsibilities.
- Server specs declare caller identity, permission checks, and sensitive field handling.

## Build Notes

- Can an implementer identify who is allowed to invoke the flow?
- Is sensitive data filtered at the earliest safe boundary?
- Are authorization checks assigned to a concrete runtime boundary?
