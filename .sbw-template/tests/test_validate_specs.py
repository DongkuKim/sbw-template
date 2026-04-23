from __future__ import annotations

import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = TEMPLATE_ROOT.parent
sys.path.insert(0, str(TEMPLATE_ROOT))

from scripts.validate_specs import validate_repository


def write(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def copy_support_files(root: Path) -> None:
    shutil.copytree(TEMPLATE_ROOT / "schemas", root / ".sbw-template" / "schemas")


def build_base_valid_fixture(root: Path, *, server_ids: list[str] | None = None) -> None:
    if server_ids is None:
        server_ids = ["get-user-profile"]

    copy_support_files(root)
    server_list = "\n".join(f"  - {server_id}" for server_id in server_ids)

    write(
        root,
        "features/profile-experience.md",
        f"""---
id: profile-experience
name: Profile Experience
layer: feature
feature: profile-experience
domain: customer-identity
views:
  - profile
bffs:
  - profile
server_apis:
{server_list}
---
# Profile Experience

## Goal

Goal.

## Scope

Scope.

## Actors

Actors.

## User Flows

Flows.

## Linked Specs

Links.

## Implementation Boundary

- Transport: transport.
- Application: application.
- Domain: domain.
- Integrations: integrations.
- Contracts: contracts.
- Tests: tests.

## Acceptance Scenarios

Acceptance.

## Rollout and Backout

Rollout.
""",
    )

    write(
        root,
        "domains/customer-identity.md",
        f"""
        ---
        id: customer-identity
        name: Customer Identity
        layer: domain
        feature: profile-experience
        domain: customer-identity
        bounded_context: account
        ---
        # Customer Identity

        ## Purpose

        Purpose.

        ## Entities and Value Objects

        Entities.

        ## Invariants

        Invariants.

        ## Ownership and Lifecycle

        Ownership.

        ## Shared Language

        Language.
        """,
    )

    server_api_blocks = []
    for server_id in server_ids:
        server_api_blocks.append(
            f"""
            ---
            id: {server_id}
            name: {server_id}
            layer: server
            feature: profile-experience
            domain: customer-identity
            method: GET
            path: /{server_id}
            ---
            # {server_id}

            ## Purpose

            Purpose.

            ## Request Contract

            Request.

            ## Response Contract

            Response.

            ## Auth and Authorization

            Auth.

            ## Error Model

            Errors.

            ## Operational Policy

            Ops.

            ## Implementation Boundary

            - Transport: transport.
            - Application: application.
            - Domain: domain.
            - Integrations: integrations.
            - Contracts: contracts.
            - Tests: tests.
            """
        )

    for server_id, server_doc in zip(server_ids, server_api_blocks):
        write(root, f"server/{server_id}.md", server_doc)

    write(
        root,
        "bff/profile.md",
        f"""---
id: profile
name: Profile BFF
layer: bff
feature: profile-experience
domain: customer-identity
view: profile
server_apis:
{server_list}
---
# Profile BFF

## Purpose

Purpose.

## View Inputs

Inputs.

## Orchestration Flow

Flow.

## Server API Usage

Usage.

## View Contract

Contract.

## Failure Handling

Failure.

## Data Protection

Protection.

## Implementation Boundary

- Transport: transport.
- Application: application.
- Domain: domain.
- Integrations: integrations.
- Contracts: contracts.
- Tests: tests.
""",
    )

    write(
        root,
        "web/layouts/account-shell.md",
        f"""
        ---
        id: account-shell
        name: Account Shell
        layer: web-layout
        feature: profile-experience
        domain: customer-identity
        slots:
          - body
        ---
        # Account Shell

        ## Purpose

        Purpose.

        ## Structure

        - `Shell root`: outer shell.
        - `Header rail`: top shell region.
        - `Content grid`: body and aside arrangement.

        ## Elements

        ### `Body slot frame`

        - `Parent area`: `Content grid`
        - `Purpose`: host the main view content.
        - `Shared components`: none
        - `Slot usage`: owns the `body` slot.
        - `Structure notes`: primary content container.
        - `Responsive behavior`: stays first when stacked.

        Interaction events:
        `<onHover>`: none.
        `<onClick>`: none.

        ## Usage Rules

        Rules.
        """,
    )

    write(
        root,
        "web/shared-components/user-summary-card.md",
        f"""
        ---
        id: user-summary-card
        name: User Summary Card
        layer: web-shared-component
        feature: profile-experience
        domain: customer-identity
        libraries:
          - shadcn
        ---
        # User Summary Card

        ## Purpose

        Purpose.

        ## Composition

        Composition.

        ## Structure

        - `Card container`: outer shell.
        - `Header text block`: name and email group.

        ## Elements

        ### `Display name`

        - `Parent area`: `Header text block`
        - `Purpose`: show the name.
        - `Base components`: `shadcn/typography`
        - `Inputs`: display name string.
        - `States`: hidden while loading.
        Interaction events:
        `<onHover>`: none.
        `<onClick>`: none.

        ## Usage Rules

        Rules.
        """,
    )

    write(
        root,
        "web/views/profile.md",
        f"""
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

        Purpose.

        ## Route and Guards

        Guards.

        ## Layout Usage

        - `Layout`: `account-shell`
        - `Header slot`: page title content
        - `Body slot`: `user-summary-card`
        - `Aside slot`: none

        ## Shared Component Usage

        ### `user-summary-card`

        - `Placement`: `account-shell` `body` slot
        - `When used`: rendered when profile data is available
        - `Inputs filled by view`:
          - `display name`: `profile.profileSummary.displayName`
          - `primary email`: `profile.profileSummary.primaryEmail`
          - `membership tier`: `profile.profileSummary.membershipTier`
          - `loading`: `profile.viewState == "loading"`
        """,
    )


class ValidateSpecsTests(unittest.TestCase):
    def with_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        return temp_dir, root

    def assert_fixture_errors(self, root: Path, expected_text: str) -> None:
        errors = validate_repository(root)
        self.assertTrue(errors, "fixture should fail validation")
        joined = "\n".join(errors)
        self.assertIn(expected_text, joined)

    def test_repository_example_passes(self) -> None:
        errors = validate_repository(REPO_ROOT)
        self.assertEqual(errors, [])

    def test_minimal_valid_fixture_passes(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            self.assertEqual(validate_repository(root), [])

    def test_multi_api_valid_fixture_passes(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(
                root,
                server_ids=["get-user-profile", "get-membership-benefits"],
            )
            self.assertEqual(validate_repository(root), [])

    def test_architecture_docs_are_ignored_by_validation(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "architecture/reference/auth-and-observability.md",
                """
                # Shared Auth And Observability

                This file is intentionally free-form and should be linked from feature or runtime docs
                instead of copied into multiple places.
                """,
            )
            self.assertEqual(validate_repository(root), [])

    def test_missing_feature_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            (root / "features" / "profile-experience.md").unlink()
            self.assert_fixture_errors(root, "references missing id `profile-experience`")

    def test_missing_domain_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            (root / "domains" / "customer-identity.md").unlink()
            self.assert_fixture_errors(root, "references missing id `customer-identity`")

    def test_direct_view_to_server_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/views/profile.md",
                """
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
                server_apis:
                  - get-user-profile
                ---
                # Profile View

                ## Purpose

                Purpose.

                ## Route and Guards

                Guards.

                ## Layout Usage

                - `Layout`: `account-shell`
                - `Header slot`: page title content
                - `Body slot`: `user-summary-card`
                - `Aside slot`: none

                ## Shared Component Usage

                ### `user-summary-card`

                - `Placement`: `account-shell` `body` slot
                - `When used`: rendered when profile data is available
                - `Inputs filled by view`:
                  - `display name`: `profile.profileSummary.displayName`
                  - `primary email`: `profile.profileSummary.primaryEmail`
                  - `membership tier`: `profile.profileSummary.membershipTier`
                  - `loading`: `profile.viewState == "loading"`
                """,
            )
            self.assert_fixture_errors(root, "unexpected front matter field `server_apis`")

    def test_legacy_view_sections_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/views/profile.md",
                """
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

                Purpose.

                ## Route and Guards

                Guards.

                ## Layout Usage

                - `Layout`: `account-shell`
                - `Header slot`: page title content
                - `Body slot`: `user-summary-card`
                - `Aside slot`: none

                ## BFF Contract

                Contract.

                ## Shared Component Usage

                ### `user-summary-card`

                - `Placement`: `account-shell` `body` slot
                - `When used`: rendered when profile data is available
                - `Inputs filled by view`:
                  - `display name`: `profile.profileSummary.displayName`

                ## View States

                States.
                """,
            )
            self.assert_fixture_errors(root, "unexpected section `## BFF Contract`")

    def test_missing_implementation_boundary_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "server/get-user-profile.md",
                """
                ---
                id: get-user-profile
                name: get-user-profile
                layer: server
                feature: profile-experience
                domain: customer-identity
                method: GET
                path: /get-user-profile
                ---
                # get-user-profile

                ## Purpose

                Purpose.

                ## Request Contract

                Request.

                ## Response Contract

                Response.

                ## Auth and Authorization

                Auth.

                ## Error Model

                Errors.

                ## Operational Policy

                Ops.
                """,
            )
            self.assert_fixture_errors(root, "missing section `## Implementation Boundary`")

    def test_legacy_layout_sections_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/layouts/account-shell.md",
                """
                ---
                id: account-shell
                name: Account Shell
                layer: web-layout
                feature: profile-experience
                domain: customer-identity
                slots:
                  - body
                ---
                # Account Shell

                ## Purpose

                Purpose.

                ## Structure

                Structure.

                ## Slots

                Slots.

                ## Interaction Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(root, "unexpected section `## Slots`")

    def test_missing_shared_component_composition_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/user-summary-card.md",
                """
                ---
                id: user-summary-card
                name: User Summary Card
                layer: web-shared-component
                feature: profile-experience
                domain: customer-identity
                libraries:
                  - shadcn
                ---
                # User Summary Card

                ## Purpose

                Purpose.

                ## Structure

                - `Card container`: outer shell.

                ## Elements

                ### `Display name`

                - `Parent area`: `Header text block`
                - `Purpose`: show the name.
                - `Base components`: `shadcn/typography`
                - `Inputs`: display name string.
                - `States`: hidden while loading.
                Interaction events:
                `<onHover>`: none.
                `<onClick>`: none.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(root, "missing section `## Composition`")

    def test_missing_shared_component_elements_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/user-summary-card.md",
                """
                ---
                id: user-summary-card
                name: User Summary Card
                layer: web-shared-component
                feature: profile-experience
                domain: customer-identity
                libraries:
                  - shadcn
                ---
                # User Summary Card

                ## Purpose

                Purpose.

                ## Composition

                Composition.

                ## Structure

                Structure.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(root, "missing section `## Elements`")

    def test_legacy_shared_component_sections_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/user-summary-card.md",
                """
                ---
                id: user-summary-card
                name: User Summary Card
                layer: web-shared-component
                feature: profile-experience
                domain: customer-identity
                libraries:
                  - shadcn
                ---
                # User Summary Card

                ## Purpose

                Purpose.

                ## Composition

                Composition.

                ## Structure

                Structure.

                ## Elements

                ### `Display name`

                - `Parent area`: `Header text block`
                - `Purpose`: show the name.
                - `Base components`: `shadcn/typography`
                - `Inputs`: display name string.
                - `States`: hidden while loading.
                Interaction events:
                `<onHover>`: none.
                `<onClick>`: none.

                ## Inputs

                Inputs.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(root, "unexpected section `## Inputs`")

    def test_feature_back_link_mismatch_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "bff/profile.md",
                """
                ---
                id: profile
                name: Profile BFF
                layer: bff
                feature: another-feature
                domain: customer-identity
                view: profile
                server_apis:
                  - get-user-profile
                ---
                # Profile BFF

                ## Purpose

                Purpose.

                ## View Inputs

                Inputs.

                ## Orchestration Flow

                Flow.

                ## Server API Usage

                Usage.

                ## View Contract

                Contract.

                ## Failure Handling

                Failure.

                ## Data Protection

                Protection.

                ## Implementation Boundary

                - Transport: transport.
                - Application: application.
                - Domain: domain.
                - Integrations: integrations.
                - Contracts: contracts.
                - Tests: tests.
                """,
            )
            self.assert_fixture_errors(root, "`bffs` entry `profile` must point back to this feature")

    def test_bff_view_link_mismatch_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/views/profile.md",
                """
                ---
                id: profile
                name: Profile View
                layer: web-view
                feature: profile-experience
                domain: customer-identity
                route: /profile
                layout: account-shell
                bff: another-bff
                shared_components:
                  - user-summary-card
                ---
                # Profile View

                ## Purpose

                Purpose.

                ## Route and Guards

                Guards.

                ## Layout Usage

                - `Layout`: `account-shell`
                - `Header slot`: page title content
                - `Body slot`: `user-summary-card`
                - `Aside slot`: none

                ## Shared Component Usage

                ### `user-summary-card`

                - `Placement`: `account-shell` `body` slot
                - `When used`: rendered when profile data is available
                - `Inputs filled by view`:
                  - `display name`: `profile.profileSummary.displayName`
                  - `primary email`: `profile.profileSummary.primaryEmail`
                  - `membership tier`: `profile.profileSummary.membershipTier`
                  - `loading`: `profile.viewState == "loading"`
                """,
            )
            self.assert_fixture_errors(root, "linked view `profile` must point back to this BFF")

    def test_missing_linked_server_api_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            (root / "server" / "get-user-profile.md").unlink()
            self.assert_fixture_errors(root, "references missing id `get-user-profile`")


if __name__ == "__main__":
    unittest.main()
