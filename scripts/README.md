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
- **uv** - for running ruff formatter (auto-downloads ruff on first run)

## What It Does

1. **Updates `@medplum/fhirtypes`** - fetches latest version from npm
2. **Clean installs dependencies** - removes node_modules to avoid corruption
3. **Runs TypeScript generator** - parses `.d.ts` files → generates Pydantic models
4. **Formats with ruff** - applies formatting and lint fixes

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
| `src/index.ts` | Main orchestrator |
| `src/parser.ts` | TypeScript AST parser, type mapping |
| `src/writer.ts` | Pydantic code generator |
| `generate.sh` | End-to-end build script |

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
