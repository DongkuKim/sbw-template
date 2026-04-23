# sbw-template

Docs-first template for planning and implementing a Server/BFF/Web product from Markdown specs before writing code.

## Layout

- `features/`: feature-level plan, scope, linked docs, and implementation boundary
- `domains/`: canonical terms, entities, invariants, and lifecycle rules
- `server/`: backend API contracts consumed by the BFF
- `bff/`: web-facing orchestration and contract shaping
- `web/`: views, layouts, and shared components
- `architecture/`: optional shared reference docs for cross-cutting concerns
- `.sbw-template/`: internal validation schemas, scripts, and tests

The editable planning surface is the top-level docs directories. `.sbw-template/` is internal enforcement machinery and should only be changed when maintaining the validator or schema contract. Docs in `features/`, `domains/`, `server/`, `bff/`, and `web/` are schema-validated. Docs in `architecture/` are intentionally free-form reference material.

For AI-agent workflows, read [AGENTS.md](/home/kimdongkudavid/develop/personal/sbw-template/AGENTS.md).

## Commands

```bash
make validate
make test
```
