/**
 * Main generator script.
 *
 * Converts Medplum's TypeScript FHIR types to Pydantic models.
 */

import * as fs from "fs";
import * as path from "path";
import { parseTypeScriptFile } from "./parser";
import { generatePydanticFile, generateInitFile, generateRebuildModule } from "./writer";

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
): { success: boolean; interfaceCount: number } {
  try {
    const parsedFile = parseTypeScriptFile(tsPath);

    if (parsedFile.interfaces.length === 0) {
      console.log(`   ⚠️  No interfaces found, skipping`);
      return { success: false, interfaceCount: 0 };
    }

    // Generate and write Pydantic code
    const pythonCode = generatePydanticFile(parsedFile);
    const outputPath = path.join(outputDir, `${resourceName.toLowerCase()}.py`);
    fs.writeFileSync(outputPath, pythonCode, "utf-8");

    console.log(
      `   ✅ Generated ${resourceName.toLowerCase()}.py (${parsedFile.interfaces.length} class${parsedFile.interfaces.length > 1 ? "es" : ""})`,
    );

    return { success: true, interfaceCount: parsedFile.interfaces.length };
  } catch (error) {
    console.error(`   ❌ Error: ${error}`);
    return { success: false, interfaceCount: 0 };
  }
}

/**
 * Generates the __init__.py and _rebuild.py files for the module.
 */
function generateModuleInit(
  resourceNames: string[],
  classesToFiles: Map<string, string>,
  outputDir: string
): void {
  console.log("\n📦 Generating module exports...");
  
  // Generate _rebuild.py for centralized model rebuilding
  const rebuildCode = generateRebuildModule();
  fs.writeFileSync(path.join(outputDir, "_rebuild.py"), rebuildCode, "utf-8");
  
  // Generate __init__.py
  const initCode = generateInitFile(resourceNames, classesToFiles);
  fs.writeFileSync(path.join(outputDir, "__init__.py"), initCode, "utf-8");
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

    if (result.success) {
      stats.generated++;
      // Collect all interface names from the parsed file and map to their file
      const parsedFile = parseTypeScriptFile(tsPath);
      const pythonFileName = resourceName.toLowerCase();
      parsedFile.interfaces.forEach((iface) => {
        resourceNames.push(iface.name);
        classesToFiles.set(iface.name, pythonFileName);
      });
    } else if (result.interfaceCount === 0) {
      stats.skipped++;
    } else {
      stats.errors++;
    }
  }

  generateModuleInit(resourceNames, classesToFiles, OUTPUT_DIR);
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
