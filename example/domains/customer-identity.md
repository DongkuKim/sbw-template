---
id: customer-identity
name: Customer Identity
layer: domain
domain: customer-identity
bounded_context: account
---

# Customer Identity

## Purpose

Define the canonical profile concepts used across the profile experience and any adjacent identity-facing surfaces.

## Entities and Value Objects

The primary entity is `CustomerProfile`. Key value objects include `DisplayName`, `PrimaryEmail`, and `MembershipTier`.

## Invariants

A customer profile must always have a stable user id, a verified primary email for authenticated account access, and a membership tier that maps to known product entitlements.

## Ownership and Lifecycle

Account Platform owns the source profile record. The BFF may reshape data for presentation but does not redefine identity semantics.

## Shared Language

Use `customer profile` for the full identity record, `primary email` for the user-facing email field, and `membership tier` for the normalized benefits classification.
