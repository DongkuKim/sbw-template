#!/usr/bin/env python3
"""Validate docs-first planning specs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_ROOT = SCRIPT_DIR.parent
DEFAULT_SCHEMA_DIR = TEMPLATE_ROOT / "schemas"
MODULE_BOUNDARIES = [
    "transport",
    "application",
    "domain",
    "integrations",
    "contracts",
    "tests",
]


class ValidationError(Exception):
    """Raised when a document cannot be parsed."""


@dataclass
class SpecDoc:
    doc_type: str
    path: Path
    relative_path: str
    schema: dict[str, Any]
    front_matter: dict[str, Any]
    sections: dict[str, str]

    @property
    def doc_id(self) -> str:
        return str(self.front_matter.get("id", ""))


def normalize_heading(value: str) -> str:
    value = value.strip().lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar_list(raw: str) -> list[str]:
    inner = raw[1:-1].strip()
    if not inner:
        return []
    return [strip_quotes(part.strip()) for part in inner.split(",") if part.strip()]


def parse_front_matter(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].rstrip()
        index += 1

        if not line.strip():
            continue

        if line.startswith(" ") or line.startswith("\t"):
            raise ValidationError(f"Unsupported front matter indentation: {line}")

        if ":" not in line:
            raise ValidationError(f"Invalid front matter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value == "":
            items: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if not next_line.strip():
                    index += 1
                    continue
                if next_line.startswith("  - "):
                    items.append(strip_quotes(next_line[4:].strip()))
                    index += 1
                    continue
                break
            result[key] = items
            continue

        if raw_value == "[]":
            result[key] = []
            continue

        if raw_value.startswith("[") and raw_value.endswith("]"):
            result[key] = parse_scalar_list(raw_value)
            continue

        result[key] = strip_quotes(raw_value)

    return result


def parse_markdown(path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("File must start with YAML front matter")

    closing_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        raise ValidationError("Front matter must be closed with ---")

    front_block = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])
    front_matter = parse_front_matter(front_block)

    sections: dict[str, list[str]] = {}
    current: str | None = None
    buffer: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = normalize_heading(line[3:])
            buffer = []
            continue
        if current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()

    return front_matter, sections


def load_schemas(schema_dir: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(schema_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        schemas[data["doc_type"]] = data
    return schemas


def resolve_schema_dir(root: Path) -> Path:
    repo_schema_dir = root / ".sbw-template" / "schemas"
    if repo_schema_dir.exists():
        return repo_schema_dir
    return DEFAULT_SCHEMA_DIR


def collect_docs(root: Path, schemas: dict[str, dict[str, Any]]) -> tuple[list[SpecDoc], list[str]]:
    docs: list[SpecDoc] = []
    errors: list[str] = []
    for doc_type, schema in schemas.items():
        directory = root / schema["directory"]
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name.endswith("-template.md"):
                continue
            relative_path = path.relative_to(root).as_posix()
            try:
                front_matter, sections = parse_markdown(path)
            except ValidationError as exc:
                errors.append(f"{relative_path}: {exc}")
                continue
            docs.append(
                SpecDoc(
                    doc_type=doc_type,
                    path=path,
                    relative_path=relative_path,
                    schema=schema,
                    front_matter=front_matter,
                    sections=sections,
                )
            )
    return docs, errors


def validate_doc(doc: SpecDoc) -> list[str]:
    errors: list[str] = []
    schema = doc.schema
    front_matter = doc.front_matter

    allowed_fields = set(schema.get("allowed_front_matter", []))
    required_fields = set(schema.get("required_front_matter", []))

    for field in required_fields:
        if field not in front_matter:
            errors.append(f"{doc.relative_path}: missing front matter field `{field}`")

    for field in front_matter:
        if allowed_fields and field not in allowed_fields:
            errors.append(f"{doc.relative_path}: unexpected front matter field `{field}`")

    if "id" in front_matter:
        file_stem = doc.path.stem
        if file_stem != front_matter["id"]:
            errors.append(
                f"{doc.relative_path}: file name `{file_stem}` must match id `{front_matter['id']}`"
            )

    layer = front_matter.get("layer")
    allowed_layers = set(schema.get("allowed_layers", []))
    if layer not in allowed_layers:
        errors.append(f"{doc.relative_path}: invalid layer `{layer}`")

    for field in schema.get("list_fields", []):
        if field in front_matter and not isinstance(front_matter[field], list):
            errors.append(f"{doc.relative_path}: field `{field}` must be a list")

    for section in schema.get("required_sections", []):
        normalized = normalize_heading(section)
        if normalized not in doc.sections:
            errors.append(f"{doc.relative_path}: missing section `## {section}`")

    for section in schema.get("forbidden_sections", []):
        normalized = normalize_heading(section)
        if normalized in doc.sections:
            errors.append(f"{doc.relative_path}: unexpected section `## {section}`")

    if schema.get("requires_implementation_boundary"):
        body = doc.sections.get("implementation boundary", "").lower()
        for name in MODULE_BOUNDARIES:
            if f"{name}:" not in body:
                errors.append(
                    f"{doc.relative_path}: implementation boundary must define `{name}`"
                )

    for field in schema.get("self_ref_fields", []):
        if front_matter.get(field) != front_matter.get("id"):
            errors.append(f"{doc.relative_path}: `{field}` must match `id`")

    return errors


def build_index(
    docs: list[SpecDoc],
) -> tuple[dict[tuple[str, str], SpecDoc], dict[str, list[SpecDoc]], list[str]]:
    typed_index: dict[tuple[str, str], SpecDoc] = {}
    generic_index: dict[str, list[SpecDoc]] = defaultdict(list)
    errors: list[str] = []

    for doc in docs:
        if not doc.doc_id:
            errors.append(f"{doc.relative_path}: missing id")
            continue
        key = (doc.doc_type, doc.doc_id)
        if key in typed_index:
            errors.append(
                f"{doc.relative_path}: duplicate id `{doc.doc_id}` for type `{doc.doc_type}` "
                f"also used by {typed_index[key].relative_path}"
            )
            continue
        typed_index[key] = doc
        generic_index[doc.doc_id].append(doc)

    return typed_index, generic_index, errors


def validate_reference(
    doc: SpecDoc,
    field: str,
    target_type: str | None,
    many: bool,
    typed_index: dict[tuple[str, str], SpecDoc],
    generic_index: dict[str, list[SpecDoc]],
    errors: list[str],
) -> None:
    if field not in doc.front_matter:
        return

    values = doc.front_matter[field]
    if many:
        if not isinstance(values, list):
            errors.append(f"{doc.relative_path}: field `{field}` must be a list")
            return
        candidates = values
    else:
        candidates = [values]

    for value in candidates:
        if target_type:
            target = typed_index.get((target_type, value))
            if target is None:
                errors.append(
                    f"{doc.relative_path}: `{field}` references missing id `{value}`"
                )
            continue

        matches = generic_index.get(value, [])
        if not matches:
            errors.append(f"{doc.relative_path}: `{field}` references missing id `{value}`")
        elif len(matches) > 1:
            errors.append(
                f"{doc.relative_path}: `{field}` references ambiguous id `{value}`"
            )


def validate_graph(
    docs: list[SpecDoc],
    typed_index: dict[tuple[str, str], SpecDoc],
    generic_index: dict[str, list[SpecDoc]],
) -> list[str]:
    errors: list[str] = []

    for doc in docs:
        schema = doc.schema
        for reference in schema.get("references", []):
            validate_reference(
                doc=doc,
                field=reference["field"],
                target_type=reference.get("doc_type"),
                many=reference.get("many", False),
                typed_index=typed_index,
                generic_index=generic_index,
                errors=errors,
            )

    for doc in docs:
        if doc.doc_type == "bff":
            view = typed_index.get(("web-view", doc.front_matter.get("view", "")))
            if view and view.front_matter.get("bff") != doc.doc_id:
                errors.append(
                    f"{doc.relative_path}: linked view `{view.doc_id}` must point back to this BFF"
                )

    return errors


def validate_repository(root: Path) -> list[str]:
    schemas = load_schemas(resolve_schema_dir(root))
    docs, errors = collect_docs(root, schemas)

    for doc in docs:
        errors.extend(validate_doc(doc))

    typed_index, generic_index, index_errors = build_index(docs)
    errors.extend(index_errors)
    errors.extend(validate_graph(docs, typed_index, generic_index))

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate planning specs")
    parser.add_argument("root", nargs="?", default=".", help="repository root to validate")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Validated planning specs in {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
