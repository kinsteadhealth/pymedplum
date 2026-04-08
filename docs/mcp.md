# MCP Server

Use `pymedplum` as a local MCP server with an inline `uvx` launcher:

```bash
uvx --from "pymedplum[mcp]" pymedplum-mcp
```

## Required Environment

At minimum, set Medplum client credentials:

```bash
export MEDPLUM_CLIENT_ID="your-client-id"
export MEDPLUM_CLIENT_SECRET="your-client-secret"
```

Optional settings:

```bash
export MEDPLUM_BASE_URL="https://api.medplum.com/"
export MEDPLUM_FHIR_URL_PATH="fhir/R4/"
export MEDPLUM_ON_BEHALF_OF="ProjectMembership/00000000-0000-0000-0000-000000000000"
export MEDPLUM_READ_ONLY="true"
```

## Setup

### Claude Code CLI

```bash
claude mcp add \
  -e MEDPLUM_CLIENT_ID=your-client-id \
  -e MEDPLUM_CLIENT_SECRET=your-client-secret \
  -e MEDPLUM_BASE_URL=https://api.medplum.com/ \
  pymedplum -- \
  uvx --from "pymedplum[mcp]" pymedplum-mcp
```

For shared project config, use `.mcp.json`:

```json
{
  "mcpServers": {
    "pymedplum": {
      "command": "uvx",
      "args": ["--from", "pymedplum[mcp]", "pymedplum-mcp"],
      "env": {
        "MEDPLUM_CLIENT_ID": "${MEDPLUM_CLIENT_ID}",
        "MEDPLUM_CLIENT_SECRET": "${MEDPLUM_CLIENT_SECRET}",
        "MEDPLUM_BASE_URL": "${MEDPLUM_BASE_URL:-https://api.medplum.com/}"
      }
    }
  }
}
```

### Codex CLI

```bash
codex mcp add \
  pymedplum \
  -e MEDPLUM_CLIENT_ID=your-client-id \
  -e MEDPLUM_CLIENT_SECRET=your-client-secret \
  -e MEDPLUM_BASE_URL=https://api.medplum.com/ \
  -- \
  uvx --from "pymedplum[mcp]" pymedplum-mcp
```

### Codex `config.toml`

Add this to `~/.codex/config.toml` or project-scoped `.codex/config.toml`:

```toml
[mcp_servers.pymedplum]
command = "uvx"
args = ["--from", "pymedplum[mcp]", "pymedplum-mcp"]
env_vars = ["MEDPLUM_CLIENT_ID", "MEDPLUM_CLIENT_SECRET", "MEDPLUM_BASE_URL"]
```

If the config file is project-scoped or checked into git, do not hardcode
credentials in it. Prefer environment-variable forwarding like `env_vars`
above, or keep secrets only in your user-scoped `~/.codex/config.toml`.

### Standard `mcp.json`

For MCP hosts that use the standard JSON config shape:

```json
{
  "mcpServers": {
    "pymedplum": {
      "command": "uvx",
      "args": ["--from", "pymedplum[mcp]", "pymedplum-mcp"],
      "env": {
        "MEDPLUM_CLIENT_ID": "your-client-id",
        "MEDPLUM_CLIENT_SECRET": "your-client-secret",
        "MEDPLUM_BASE_URL": "https://api.medplum.com/"
      }
    }
  }
}
```

If the client supports project-scoped config, prefer sourcing secrets from
environment variables instead of checking credentials into the repo.

## What The Server Exposes

The MCP provides a compact tool surface:

- **Discovery**: resource schema lookup, server capability discovery
- **FHIR CRUD**: read, search (paginated, single, all-pages), create
  (with conditional create), update, patch (JSON Patch), delete
- **Patient**: `$everything` operation for full clinical picture
- **Terminology**: ValueSet validation/expansion, CodeSystem validation/lookup,
  ConceptMap translation
- **Operations**: generic FHIR `$operation` execution, GraphQL queries,
  batch/transaction bundles
- **Bots**: create, deploy, and execute Medplum bots
- **Escape hatch**: `raw_request` for any authenticated Medplum endpoint
  not covered by a dedicated tool

The server also exposes three MCP resources:

- `medplum://server-info` — connection info and read-only status
- `medplum://tool-guide` — quick-reference for which tool to use when
- `medplum://common-errors` — HTTP error codes and recovery steps

Use `execute_operation` for FHIR `$operations` not covered by a dedicated
tool, and `raw_request` as the last resort for arbitrary Medplum endpoints
(admin APIs, `$reindex`, `_history`, etc.).
