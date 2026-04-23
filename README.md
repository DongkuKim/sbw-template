# sbw-template

Docs-first template for planning and implementing a Server/BFF/Web product from Markdown specs before writing code.

## Layout

- `domains/`: canonical terms, entities, invariants, and lifecycle rules
- `server/`: backend API contracts consumed by the BFF
- `bff/`: web-facing orchestration and contract shaping
- `web/`: views, layouts, and shared components
- `example/`: worked example using the same planning structure
- `.sbw-template/`: internal validation schemas, scripts, and tests

The editable planning surface is the top-level docs directories. `.sbw-template/` is internal enforcement machinery and should only be changed when maintaining the validator or schema contract. The top-level `domains/`, `server/`, `bff/`, and `web/` directories hold starter templates, while `example/` holds the worked example in the same mirrored format. Docs in those mirrored planning directories are schema-validated.

For AI-agent workflows, read [AGENTS.md](/home/kimdongkudavid/develop/personal/sbw-template/AGENTS.md).

## Commands

```bash
make validate
make test
```
