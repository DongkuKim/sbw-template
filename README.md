# sbw-template

Docs-first template for planning and implementing a Server/BFF/Web product from Markdown specs before writing code.

## Layout

- `domains/`: canonical terms, entities, invariants, and lifecycle rules
- `server/`: backend API contracts consumed by the BFF
- `bff/`: web-facing orchestration, BFF route shape, and typed request/response contracts
- `web/`: domain-specific views, reusable layouts, and non-domain shared components
- `example/`: worked example using the same planning structure
- `.sbw-template/`: internal validation schemas, scripts, and tests

The editable planning surface is the top-level docs directories. `.sbw-template/` is internal enforcement machinery and should only be changed when maintaining the validator or schema contract. The top-level `domains/`, `server/`, `bff/`, and `web/` directories hold starter templates, while `example/` holds the worked example in the same mirrored format. Docs in those mirrored planning directories are schema-validated.

Shared components use `component_kind: custom` for real reusable components and `component_kind: wrapper` with `wraps` for restricted wrappers around upstream primitives. Start from `web/shared-components/shared-component-template.md` to choose the right component template.

For AI-agent workflows, read [AGENTS.md](/home/kimdongkudavid/develop/personal/sbw-template/AGENTS.md).

## Commands

```bash
make validate
make test
```
