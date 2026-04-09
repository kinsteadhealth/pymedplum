# FHIR Model Generator

This directory contains the TypeScript-based code generator that converts Medplum's FHIR type definitions into Python Pydantic models.

## Quick Start

```bash
# From the project root:
make generate              # Update to latest @medplum/fhirtypes and regenerate
make generate-no-update    # Regenerate without updating npm

# Or run directly:
./scripts/generate.sh
./scripts/generate.sh --no-update
```

## Requirements

- **Node.js** / **npm** - for TypeScript generation
- **python3** - for validation smoke test
- **uvx** - for running ruff formatter (auto-downloads ruff on first run)

The script checks for all of these at startup and exits with a clear error if any are missing.

## What It Does

1. **Updates `@medplum/fhirtypes`** - fetches latest version from npm (skip with `--no-update`)
2. **Installs dependencies** - uses `npm ci` for reproducible installs (falls back to `npm install` if no lockfile)
3. **Runs TypeScript generator** - parses `.d.ts` files, generates Pydantic models, removes stale files
4. **Formats with ruff** - applies formatting and lint fixes
5. **Validates output** - smoke test imports key types and instantiates a Patient

## Safety Features

- **Stale file cleanup**: If an upstream type is removed, the corresponding `.py` file is automatically deleted. Cleanup is skipped if any files errored during generation to prevent accidental data loss.
- **Version stamp**: The generated `__init__.py` records which `@medplum/fhirtypes` version produced it.
- **Validation**: A Python smoke test runs after generation to catch import errors early.
- **Pre-flight checks**: The script validates that all required tools are on PATH before starting.

## Output

```
pymedplum/fhir/
├── __init__.py      # Lazy-loading module with 700+ class exports
├── __init__.pyi     # Type stubs for IDE support
├── py.typed         # PEP 561 marker
├── base.py          # MedplumFHIRBase class
├── patient.py       # Patient resource
├── observation.py   # Observation resource
└── ...              # 200+ more resource/datatype files
```

## Architecture

```
@medplum/fhirtypes (npm)
    ↓
src/parser.ts      → Parse TypeScript .d.ts AST
    ↓
src/writer.ts      → Generate Pydantic class code
    ↓
pymedplum/fhir/*.py
```

### Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Main orchestrator, stale file cleanup, version detection |
| `src/parser.ts` | TypeScript AST parser, type mapping |
| `src/writer.ts` | Pydantic code generator |
| `generate.sh` | End-to-end build script with validation |

## Manual Generation

If you need to run steps individually:

```bash
cd scripts

# Install/update dependencies
npm install "@medplum/fhirtypes@^5.0.0" --save
npm install

# Run generator
npm run generate

# Format output
cd ..
uvx ruff format pymedplum/fhir
uvx ruff check --fix pymedplum/fhir
```
