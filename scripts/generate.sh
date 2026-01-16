#!/bin/bash
#
# End-to-end FHIR model generator
#
# Handles:
#   1. Updating @medplum/fhirtypes from npm to latest
#   2. Running the TypeScript generator
#   3. Formatting the generated Python code with ruff
#
# Usage:
#   ./scripts/generate.sh              # Update to latest and regenerate
#   ./scripts/generate.sh --no-update  # Regenerate without npm update
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FHIR_OUTPUT_DIR="$PROJECT_ROOT/pymedplum/fhir"

cd "$SCRIPT_DIR"

echo "========================================"
echo "PyMedplum FHIR Model Generator"
echo "========================================"

# Parse args
NO_UPDATE=false
for arg in "$@"; do
    case $arg in
        --no-update)
            NO_UPDATE=true
            shift
            ;;
    esac
done

# Show current version
CURRENT_VERSION=$(node -p "require('./package.json').dependencies['@medplum/fhirtypes']" 2>/dev/null || echo "unknown")
echo ""
echo "Current package.json version: $CURRENT_VERSION"

# Step 1: Update to latest
echo ""
echo "[1/4] Updating @medplum/fhirtypes..."
if [ "$NO_UPDATE" = true ]; then
    echo "  Skipped (--no-update)"
else
    LATEST=$(npm view @medplum/fhirtypes version)
    echo "  Latest version: $LATEST"
    npm install "@medplum/fhirtypes@^$LATEST" --save
fi

# Step 2: Clean install dependencies
echo ""
echo "[2/4] Installing npm dependencies (clean)..."
rm -rf node_modules package-lock.json
npm install

# Step 3: Run generator
echo ""
echo "[3/4] Running TypeScript generator..."
npm run generate

# Step 4: Format with ruff (using uvx for isolation)
echo ""
echo "[4/4] Formatting with ruff..."
cd "$PROJECT_ROOT"
uvx ruff format "$FHIR_OUTPUT_DIR"
uvx ruff check --fix "$FHIR_OUTPUT_DIR" || true

# Summary
echo ""
echo "========================================"
echo "Generation complete!"
echo "========================================"
INSTALLED_VERSION=$(node -p "require('$SCRIPT_DIR/node_modules/@medplum/fhirtypes/package.json').version" 2>/dev/null || echo "unknown")
NUM_FILES=$(find "$FHIR_OUTPUT_DIR" -name "*.py" | wc -l | tr -d ' ')
echo "  Version: $INSTALLED_VERSION"
echo "  Files: $NUM_FILES"
echo "  Output: $FHIR_OUTPUT_DIR"
