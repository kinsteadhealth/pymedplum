# Installation

`pymedplum` is available on PyPI and can be installed with pip. A virtual environment is recommended.

## Install with pip

```bash
pip install pymedplum
```

This will install the core package and its dependencies, including `pydantic` and `httpx`.

## Install with MCP support

If you want to use the optional MCP server, the recommended launch pattern is:

```bash
uvx --from "pymedplum[mcp]" pymedplum-mcp
```

If you specifically want it installed into your environment, install the `mcp`
extra:

```bash
pip install "pymedplum[mcp]"
```

With `uv`:

```bash
uv add "pymedplum[mcp]"
```

For MCP clients, prefer the direct `uvx` command over a separate install step.

## For Developers

If you are contributing to `pymedplum`, you will need to install the package in editable mode along with development dependencies.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kinsteadhealth/pymedplum.git
    cd pymedplum
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install in editable mode with dev extras:**
    ```bash
    pip install -e ".[dev]"
    ```
This will install `pytest`, `ruff`, `mypy`, and other tools needed for testing and linting.
