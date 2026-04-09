/**
 * Main generator script.
 *
 * Converts Medplum's TypeScript FHIR types to Pydantic models.
 */

import * as fs from "fs";
import * as path from "path";
import { parseTypeScriptFile } from "./parser";
import { generatePydanticFile, generateInitFile, generateStubFile } from "./writer";

// ============================================================================
// Version Detection
// ============================================================================

/**
 * Reads the installed @medplum/fhirtypes version from node_modules.
 */
function getInstalledFhirTypesVersion(): string {
  const candidates = [
    path.resolve(__dirname, "../node_modules/@medplum/fhirtypes/package.json"),
    path.resolve(__dirname, "../../node_modules/@medplum/fhirtypes/package.json"),
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      try {
        const pkg = JSON.parse(fs.readFileSync(candidate, "utf-8"));
        return pkg.version || "unknown";
      } catch {
        continue;
      }
    }
  }
  return "unknown";
}

// ============================================================================
// Configuration
// ============================================================================

const OUTPUT_DIR = path.resolve(__dirname, "../../pymedplum/fhir");

const SKIP_FILES = new Set([
  "index.d.ts", // Skip index
  "Resource.d.ts", // Skip union type
  "ResourceType.d.ts", // Skip string literal type
]);

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Finds the Medplum types directory by checking common node_modules locations.
 */
function findMedplumTypesDir(): string {
  const basePaths = [
    path.resolve(__dirname, "../../node_modules/@medplum/fhirtypes"),
    path.resolve(__dirname, "../node_modules/@medplum/fhirtypes"),
  ];

  const searchedPaths: string[] = [];

  for (const basePath of basePaths) {
    // Try /dist subdirectory first, then base path
    const candidates = [path.join(basePath, "dist"), basePath];

    for (const dir of candidates) {
      searchedPaths.push(dir);
      if (fs.existsSync(dir)) {
        const files = fs.readdirSync(dir);
        if (files.some((f) => f.endsWith(".d.ts"))) {
          return dir;
        }
      }
    }
  }

  console.error(
    "❌ Could not find @medplum/fhirtypes type definitions in any expected location",
  );
  console.error("Searched:");
  searchedPaths.forEach((d) => console.error(`  - ${d}`));
  process.exit(1);
}

/**
 * Gets all TypeScript definition files to process.
 */
function getDefinitionFiles(typesDir: string): string[] {
  return fs
    .readdirSync(typesDir)
    .filter((f) => f.endsWith(".d.ts") && !SKIP_FILES.has(f))
    .sort();
}

/**
 * Ensures the output directory exists.
 */
function ensureOutputDirectory(outputDir: string): void {
  fs.mkdirSync(outputDir, { recursive: true });
}

/**
 * Processes a single TypeScript definition file.
 */
function processDefinitionFile(
  tsPath: string,
  resourceName: string,
  outputDir: string,
): { success: boolean; parsedFile: ReturnType<typeof parseTypeScriptFile> | null } {
  try {
    const parsedFile = parseTypeScriptFile(tsPath);

    if (parsedFile.interfaces.length === 0) {
      console.log(`   ⚠️  No interfaces found, skipping`);
      return { success: false, parsedFile: null };
    }

    // Generate and write Pydantic code
    const pythonCode = generatePydanticFile(parsedFile);
    const outputPath = path.join(outputDir, `${resourceName.toLowerCase()}.py`);
    fs.writeFileSync(outputPath, pythonCode, "utf-8");

    console.log(
      `   ✅ Generated ${resourceName.toLowerCase()}.py (${parsedFile.interfaces.length} class${parsedFile.interfaces.length > 1 ? "es" : ""})`,
    );

    return { success: true, parsedFile };
  } catch (error) {
    console.error(`   ❌ Error: ${error}`);
    return { success: false, parsedFile: null };
  }
}

/**
 * Generates the __init__.py file and IDE support files for the module.
 */
function generateModuleInit(
  resourceNames: string[],
  classesToFiles: Map<string, string>,
  outputDir: string,
  fhirTypesVersion: string,
): void {
  console.log("\n📦 Generating module exports...");

  // Generate __init__.py
  const initCode = generateInitFile(resourceNames, classesToFiles, fhirTypesVersion);
  fs.writeFileSync(path.join(outputDir, "__init__.py"), initCode, "utf-8");

  // Generate __init__.pyi stub file for IDE/type checker support
  console.log("📝 Generating type stub file (__init__.pyi)...");
  const stubCode = generateStubFile(resourceNames, classesToFiles);
  fs.writeFileSync(path.join(outputDir, "__init__.pyi"), stubCode, "utf-8");

  // Create py.typed marker file
  console.log("🏷️  Creating py.typed marker...");
  const pyTypedPath = path.resolve(outputDir, "../py.typed");
  fs.writeFileSync(pyTypedPath, "", "utf-8");
}

/**
 * Prints generation summary.
 */
function printSummary(stats: {
  generated: number;
  skipped: number;
  errors: number;
}): void {
  console.log("\n" + "=".repeat(50));
  console.log(`✅ Generated: ${stats.generated} files`);
  console.log(`⚠️  Skipped:   ${stats.skipped} files`);
  console.log(`❌ Errors:    ${stats.errors} files`);
  console.log("=".repeat(50));

  if (stats.errors > 0) {
    console.log("\n⚠️  Some files had errors. Review above output.");
    return;
  }

  console.log("\n🎉 Generation complete!");
  console.log("\nNext steps:");
  console.log("1. Review generated files in pymedplum/fhir/");
  console.log("2. Run tests: pytest tests/");
  console.log("3. Commit changes");
}

// ============================================================================
// Main Generator
// ============================================================================

function main(): void {
  console.log("🚀 PyMedplum Type Generator");
  console.log("==========================\n");

  const typesDir = findMedplumTypesDir();
  console.log(`📂 Source: ${typesDir}`);
  console.log(`📝 Output: ${OUTPUT_DIR}\n`);

  ensureOutputDirectory(OUTPUT_DIR);

  // Track which .py files we generate so we can remove stale ones
  const generatedFiles = new Set<string>(["__init__.py", "__init__.pyi", "base.py", "py.typed"]);

  const files = getDefinitionFiles(typesDir);
  console.log(`📋 Found ${files.length} type definition files\n`);

  const resourceNames: string[] = [];
  const stats = {
    generated: 0,
    skipped: 0,
    errors: 0,
  };

  // Track classes by their file
  const classesToFiles = new Map<string, string>();

  // Process each file
  for (const file of files) {
    const tsPath = path.join(typesDir, file);
    const resourceName = path.basename(file, ".d.ts");

    console.log(`⚙️  Processing ${resourceName}...`);

    const result = processDefinitionFile(tsPath, resourceName, OUTPUT_DIR);

    if (result.success && result.parsedFile) {
      stats.generated++;
      const pythonFileName = resourceName.toLowerCase();
      generatedFiles.add(`${pythonFileName}.py`);
      result.parsedFile.interfaces.forEach((iface) => {
        resourceNames.push(iface.name);
        classesToFiles.set(iface.name, pythonFileName);
      });
    } else if (!result.parsedFile) {
      stats.skipped++;
    } else {
      stats.errors++;
    }
  }

  // Remove stale .py files that no longer correspond to upstream types
  const existingFiles = fs.readdirSync(OUTPUT_DIR).filter((f) => f.endsWith(".py") || f.endsWith(".pyi") || f === "py.typed");
  let staleCount = 0;
  for (const existing of existingFiles) {
    if (!generatedFiles.has(existing)) {
      const stalePath = path.join(OUTPUT_DIR, existing);
      fs.unlinkSync(stalePath);
      console.log(`   🗑️  Removed stale file: ${existing}`);
      staleCount++;
    }
  }
  if (staleCount > 0) {
    console.log(`\n🧹 Removed ${staleCount} stale file(s)`);
  }

  const fhirTypesVersion = getInstalledFhirTypesVersion();
  generateModuleInit(resourceNames, classesToFiles, OUTPUT_DIR, fhirTypesVersion);
  printSummary(stats);

  if (stats.errors > 0) {
    process.exit(1);
  }
}

// ============================================================================
// Entry Point
// ============================================================================

if (require.main === module) {
  main();
}
