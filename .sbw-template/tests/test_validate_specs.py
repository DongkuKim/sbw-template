from __future__ import annotations

import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = TEMPLATE_ROOT.parent
EXAMPLE_ROOT = REPO_ROOT / "example"
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
        "domains/customer-identity.md",
        f"""
        ---
        id: customer-identity
        name: Customer Identity
        layer: domain
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
domain: customer-identity
view: profile
server_apis:
{server_list}
---
# Profile BFF

## Purpose

Purpose.

## BFF Path

/profile

## View Inputs

Inputs.

## BFF API (Web-facing)

API.

## Orchestration Flow

Flow.

## Server API Usage

Usage.

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
        "web/shared-components/profile-card.md",
        f"""
        ---
        id: profile-card
        name: Profile Card
        layer: web-shared-component
        component_kind: custom
        libraries:
          - shadcn
        ---
        # Profile Card

        ## Intent

        Intent.

        ## Purpose

        Purpose.

        ## UX Contract

        UX.

        ## Public Interface

        Interface.

        ## State & Data

        State.

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
        domain: customer-identity
        route: /profile
        layout: account-shell
        bff: profile
        shared_components:
          - profile-card
        ---
        # Profile View

        ## Purpose

        Purpose.

        ## Layout Usage

        - `Layout`: `account-shell`
        - `Header slot`: page title content
        - `Body slot`: `profile-card`
        - `Aside slot`: none

        ## Shared Component Usage

        ### `profile-card`

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

    def test_example_workspace_passes(self) -> None:
        errors = validate_repository(EXAMPLE_ROOT)
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

    def test_non_schema_docs_are_ignored_by_validation(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "notes/reference/auth-and-observability.md",
                """
                # Shared Auth And Observability

                This file is intentionally free-form and is outside the validated doc directories.
                """,
            )
            self.assertEqual(validate_repository(root), [])

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
                domain: customer-identity
                route: /profile
                layout: account-shell
                bff: profile
                shared_components:
                  - profile-card
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
                - `Body slot`: `profile-card`
                - `Aside slot`: none

                ## Shared Component Usage

                ### `profile-card`

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
                domain: customer-identity
                route: /profile
                layout: account-shell
                bff: profile
                shared_components:
                  - profile-card
                ---
                # Profile View

                ## Purpose

                Purpose.

                ## Route and Guards

                Guards.

                ## Layout Usage

                - `Layout`: `account-shell`
                - `Header slot`: page title content
                - `Body slot`: `profile-card`
                - `Aside slot`: none

                ## BFF Contract

                Contract.

                ## Shared Component Usage

                ### `profile-card`

                - `Placement`: `account-shell` `body` slot
                - `When used`: rendered when profile data is available
                - `Inputs filled by view`:
                  - `display name`: `profile.profileSummary.displayName`

                ## View States

                States.
                """,
            )
            self.assert_fixture_errors(root, "unexpected section `## Route and Guards`")

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

    def test_missing_shared_component_public_interface_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/profile-card.md",
                """
                ---
                id: profile-card
                name: Profile Card
                layer: web-shared-component
                component_kind: custom
                libraries:
                  - shadcn
                ---
                # Profile Card

                ## Intent

                Intent.

                ## Purpose

                Purpose.

                ## UX Contract

                UX.

                ## State & Data

                State.

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
            self.assert_fixture_errors(root, "missing section `## Public Interface`")

    def test_missing_shared_component_elements_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/profile-card.md",
                """
                ---
                id: profile-card
                name: Profile Card
                layer: web-shared-component
                component_kind: custom
                libraries:
                  - shadcn
                ---
                # Profile Card

                ## Intent

                Intent.

                ## Purpose

                Purpose.

                ## UX Contract

                UX.

                ## Public Interface

                Interface.

                ## State & Data

                State.

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
                "web/shared-components/profile-card.md",
                """
                ---
                id: profile-card
                name: Profile Card
                layer: web-shared-component
                component_kind: custom
                libraries:
                  - shadcn
                ---
                # Profile Card

                ## Intent

                Intent.

                ## Purpose

                Purpose.

                ## UX Contract

                UX.

                ## Public Interface

                Interface.

                ## State & Data

                State.

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

    def test_invalid_shared_component_kind_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/profile-card.md",
                """
                ---
                id: profile-card
                name: Profile Card
                layer: web-shared-component
                component_kind: domain
                libraries:
                  - shadcn
                ---
                # Profile Card

                ## Purpose

                Purpose.

                ## Public Interface

                Interface.

                ## Structure

                Structure.

                ## Elements

                Elements.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(
                root,
                "field `component_kind` must be one of `custom`, `wrapper`",
            )

    def test_missing_custom_shared_component_intent_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/profile-card.md",
                """
                ---
                id: profile-card
                name: Profile Card
                layer: web-shared-component
                component_kind: custom
                libraries:
                  - shadcn
                ---
                # Profile Card

                ## Purpose

                Purpose.

                ## UX Contract

                UX.

                ## Public Interface

                Interface.

                ## State & Data

                State.

                ## Structure

                Structure.

                ## Elements

                Elements.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(
                root,
                "missing section `## Intent` when `component_kind` is `custom`",
            )

    def test_missing_wrapper_wraps_fixture_fails(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/icon-button.md",
                """
                ---
                id: icon-button
                name: Icon Button
                layer: web-shared-component
                component_kind: wrapper
                libraries:
                  - shadcn
                ---
                # Icon Button

                ## Purpose

                Purpose.

                ## Wrapped Component

                Wrapped.

                ## Public Interface

                Interface.

                ## Wrapper Contract

                Contract.

                ## Structure

                Structure.

                ## Elements

                Elements.

                ## Usage Rules

                Rules.
                """,
            )
            self.assert_fixture_errors(
                root,
                "missing front matter field `wraps` when `component_kind` is `wrapper`",
            )

    def test_wrapper_shared_component_fixture_passes(self) -> None:
        temp_dir, root = self.with_fixture()
        with temp_dir:
            build_base_valid_fixture(root)
            write(
                root,
                "web/shared-components/icon-button.md",
                """
                ---
                id: icon-button
                name: Icon Button
                layer: web-shared-component
                component_kind: wrapper
                libraries:
                  - shadcn
                wraps: shadcn/button
                ---
                # Icon Button

                ## Purpose

                Purpose.

                ## Wrapped Component

                Wrapped.

                ## Public Interface

                Interface.

                ## Wrapper Contract

                Contract.

                ## Structure

                Structure.

                ## Elements

                Elements.

                ## Usage Rules

                Rules.
                """,
            )
            self.assertEqual(validate_repository(root), [])

    def test_unexpected_feature_field_fixture_fails(self) -> None:
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
                feature: profile-experience
                domain: customer-identity
                view: profile
                server_apis:
                  - get-user-profile
                ---
                # Profile BFF

                ## Purpose

                Purpose.

                ## BFF Path

                /profile

                ## View Inputs

                Inputs.

                ## BFF API (Web-facing)

                API.

                ## Orchestration Flow

                Flow.

                ## Server API Usage

                Usage.

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
            self.assert_fixture_errors(root, "unexpected front matter field `feature`")

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
                domain: customer-identity
                route: /profile
                layout: account-shell
                bff: another-bff
                shared_components:
                  - profile-card
                ---
                # Profile View

                ## Purpose

                Purpose.

                ## Layout Usage

                - `Layout`: `account-shell`
                - `Header slot`: page title content
                - `Body slot`: `profile-card`
                - `Aside slot`: none

                ## Shared Component Usage

                ### `profile-card`

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
