#!/bin/bash
#
# End-to-end FHIR model generator
#
# Handles:
#   1. Updating @medplum/fhirtypes from npm to latest
#   2. Running the TypeScript generator (stale file cleanup included)
#   3. Formatting the generated Python code with ruff
#   4. Validating that generated models import correctly
#
# Usage:
#   ./scripts/generate.sh              # Update to latest and regenerate
#   ./scripts/generate.sh --no-update  # Regenerate without npm update
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FHIR_OUTPUT_DIR="$PROJECT_ROOT/pymedplum/fhir"

cd "$SCRIPT_DIR"

echo "========================================"
echo "PyMedplum FHIR Model Generator"
echo "========================================"

# ── Pre-flight checks ──────────────────────────────────────────────────

for cmd in node npm python3 uvx; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: $cmd is not installed or not on PATH" >&2
        exit 1
    fi
done

# ── Parse args ─────────────────────────────────────────────────────────

NO_UPDATE=false
for arg in "$@"; do
    case $arg in
        --no-update)
            NO_UPDATE=true
            shift
            ;;
        *)
            echo "Unknown argument: $arg" >&2
            echo "Usage: $0 [--no-update]" >&2
            exit 1
            ;;
    esac
done

# Show current version
CURRENT_VERSION=$(node -p "require('./package.json').dependencies['@medplum/fhirtypes']" 2>/dev/null || echo "unknown")
echo ""
echo "Current package.json version: $CURRENT_VERSION"

# ── Step 1: Update to latest ──────────────────────────────────────────

echo ""
echo "[1/4] Updating @medplum/fhirtypes..."
if [ "$NO_UPDATE" = true ]; then
    echo "  Skipped (--no-update)"
else
    LATEST=$(npm view @medplum/fhirtypes version)
    echo "  Latest version: $LATEST"
    npm install "@medplum/fhirtypes@^$LATEST" --save
fi

# ── Step 2: Install dependencies ──────────────────────────────────────

echo ""
echo "[2/4] Installing npm dependencies..."
npm ci || npm install

# ── Step 3: Run generator ─────────────────────────────────────────────

echo ""
echo "[3/4] Running TypeScript generator..."
npm run generate

# ── Step 4: Format with ruff ──────────────────────────────────────────

echo ""
echo "[4/4] Formatting with ruff..."
cd "$PROJECT_ROOT"
uvx ruff format "$FHIR_OUTPUT_DIR"
# Fix auto-fixable lint issues; fail on errors that can't be auto-fixed
uvx ruff check --fix "$FHIR_OUTPUT_DIR" || {
    echo ""
    echo "WARNING: ruff check found unfixable lint issues (see above)."
    echo "         The models are generated but may need manual attention."
}

# ── Validation ─────────────────────────────────────────────────────────

echo ""
echo "Validating generated models..."
cd "$PROJECT_ROOT"

VALIDATION_FAILED=false

# Quick smoke test: import the module and a few common types
python3 -c "
from pymedplum.fhir import Patient, Observation, Practitioner, Encounter
from pymedplum.fhir import List, Parameters, FHIR_TYPES
print(f'  Registry: {len(FHIR_TYPES)} classes')
p = Patient(resource_type='Patient')
assert p.resource_type == 'Patient', 'Patient resourceType mismatch'
# Regression: these used to crash the loader / fail Pydantic rebuild
List(status='current', mode='working')
Parameters(parameter=[{'name': 'patient', 'resource': p}])
print('  Smoke test: PASSED')
" || {
    echo "  WARNING: Smoke test failed. Generated models may have issues."
    VALIDATION_FAILED=true
}

# ── Summary ────────────────────────────────────────────────────────────

echo ""
echo "========================================"
echo "Generation complete!"
echo "========================================"
cd "$SCRIPT_DIR"
INSTALLED_VERSION=$(node -p "require('./node_modules/@medplum/fhirtypes/package.json').version" 2>/dev/null || echo "unknown")
NUM_FILES=$(find "$FHIR_OUTPUT_DIR" -name "*.py" -not -name "__init__*" | wc -l | tr -d ' ')
echo "  @medplum/fhirtypes: $INSTALLED_VERSION"
echo "  Resource files:     $NUM_FILES"
echo "  Output:             $FHIR_OUTPUT_DIR"

if [ "$VALIDATION_FAILED" = true ]; then
    echo ""
    echo "  ⚠️  Validation had warnings — review the output above."
    exit 1
fi
