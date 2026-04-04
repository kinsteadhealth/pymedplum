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

Add the server with `claude mcp add`:

```bash
claude mcp add --transport stdio \
  --env MEDPLUM_CLIENT_ID=your-client-id \
  --env MEDPLUM_CLIENT_SECRET=your-client-secret \
  --env MEDPLUM_BASE_URL=https://api.medplum.com/ \
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

Add the server with `codex mcp add`:

```bash
codex mcp add \
  pymedplum \
  --env MEDPLUM_CLIENT_ID=your-client-id \
  --env MEDPLUM_CLIENT_SECRET=your-client-secret \
  --env MEDPLUM_BASE_URL=https://api.medplum.com/ \
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

The MCP keeps a relatively compact tool surface:

- Generic FHIR CRUD and search
- Resource schema and server capability discovery
- Generic FHIR operation execution
- GraphQL queries
- Terminology helpers
- Agent-oriented helpers such as conditional create, full-result search,
  CodeSystem validation, C-CDA export, and Medplum bot workflows

Use the higher-level tools first when they exist:

- `create_resource_if_none_exist`
- `search_all_resources`
- `create_bot`
- `execute_bot`
- `save_and_deploy_bot`

Use `execute_operation` as the escape hatch for uncommon FHIR or
Medplum-specific operations.
