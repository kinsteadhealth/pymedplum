/**
 * Pydantic class generator.
 *
 * Generates Python/Pydantic code from parsed TypeScript interfaces.
 */

import { ParsedInterface, ParsedField, ParsedFile } from "./parser";

// ============================================================================
// Constants
// ============================================================================

const PYTHON_HEADER = [
  "# This is a generated file",
  "# Do not edit manually.",
  "# Generated from Medplum TypeScript definitions",
  "# ruff: noqa: F821 - Forward references resolved via Pydantic model_rebuild()",
  "",
  "from __future__ import annotations",
  "",
];

const BASE_CLASS = "MedplumFHIRBase";
const PYDANTIC_IMPORT = "from pydantic import Field";
const BASE_IMPORT = "from pymedplum.fhir.base import MedplumFHIRBase";

const MAX_SINGLE_LINE_DOCSTRING = 84;
const MAX_DOCSTRING_LINE_WIDTH = 72;

// Unicode characters to normalize in Python strings
const UNICODE_REPLACEMENTS: Record<number, string> = {
  0x2011: "-", // Non-breaking hyphen
  0x2013: "-", // En dash
  0x2014: "-", // Em dash
};

// ============================================================================
// Type Import Management
// ============================================================================

interface TypingImports {
  hasOptional: boolean;
  hasUnion: boolean;
  hasLiteral: boolean;
  hasAny: boolean;
  hasTypeVar: boolean;
  hasList: boolean;
  hasDict: boolean;
}

/**
 * Analyzes parsed file to determine which typing imports are needed.
 */
function analyzeTypingImports(parsedFile: ParsedFile): TypingImports {
  const imports: TypingImports = {
    hasOptional: false,
    hasUnion: false,
    hasLiteral: false,
    hasAny: false,
    hasTypeVar: false,
    hasList: false,
    hasDict: false,
  };

  // Check if TypeVar is needed for generic classes
  imports.hasTypeVar = parsedFile.interfaces.some((iface) =>
    iface.fields.some(
      (f) =>
        f.pythonType === "T" ||
        f.pythonType.includes(" T ") ||
        f.pythonType.includes("[T]") ||
        f.pythonType.includes(" T,") ||
        f.pythonType.startsWith("T,"),
    ),
  );

  // Check which typing constructs are used
  parsedFile.interfaces.forEach((iface) => {
    iface.fields.forEach((field) => {
      if (field.optional) imports.hasOptional = true;
      if (field.pythonType === "Any" || field.pythonType.includes("[Any]"))
        imports.hasAny = true;
      if (field.pythonType.includes("Union[")) imports.hasUnion = true;
      if (field.pythonType.includes("Literal[")) imports.hasLiteral = true;
      if (field.pythonType.includes("List[") || field.isArray) imports.hasList = true;
      if (field.pythonType.includes("Dict[")) imports.hasDict = true;
      // Check if field will be converted to dict[str, Any] for Resource arrays
      if (field.isArray && field.pythonType === "Resource") imports.hasAny = true;
    });
  });

  return imports;
}

/**
 * Builds sorted typing imports following isort rules.
 */
function buildTypingImports(
  imports: TypingImports,
  hasExternalImports: boolean,
): string[] {
  const typingImports = new Set<string>();

  if (imports.hasTypeVar) typingImports.add("TypeVar");
  if (imports.hasAny) typingImports.add("Any");
  // No longer need Dict and List - using built-in dict and list
  if (imports.hasLiteral) typingImports.add("Literal");
  if (imports.hasOptional) typingImports.add("Optional");
  if (imports.hasUnion) typingImports.add("Union");
  if (hasExternalImports) typingImports.add("TYPE_CHECKING");

  // Sort: SCREAMING_CASE first, then TitleCase
  return Array.from(typingImports).sort((a, b) => {
    const aIsUpper = a === a.toUpperCase();
    const bIsUpper = b === b.toUpperCase();

    if (aIsUpper && !bIsUpper) return -1;
    if (!aIsUpper && bIsUpper) return 1;
    return a.localeCompare(b);
  });
}

/**
 * Extracts external type references from parsed interfaces.
 */
function extractExternalImports(parsedFile: ParsedFile): string[] {
  const usedTypes = new Set<string>();

  parsedFile.interfaces.forEach((iface) => {
    iface.fields.forEach((field) => {
      // Normalize to lowercase built-ins and remove generics
      let processedType = field.pythonType
        .replace(/\bList\[/g, "list[")
        .replace(/\bDict\[/g, "dict[")
        .replace(/\bType\[/g, "type[")
        .replace(/([A-Z][a-zA-Z0-9]*)<[^>]+>/g, "$1");

      // Extract capitalized type names (FHIR types)
      const typeMatches = processedType.match(/\b[A-Z][a-zA-Z0-9]*\b/g);
      if (typeMatches) {
        typeMatches.forEach((t) => usedTypes.add(t));
      }
    });
  });

  return Array.from(parsedFile.allImports)
    .filter((imp) => !parsedFile.localTypes.has(imp))
    .filter((imp) => usedTypes.has(imp))
    .sort();
}

// ============================================================================
// String Normalization
// ============================================================================

/**
 * Normalizes Unicode characters in strings to their ASCII equivalents.
 */
function normalizeUnicode(text: string): string {
  return Array.from(text)
    .map((char) => {
      const code = char.charCodeAt(0);
      return UNICODE_REPLACEMENTS[code] || char;
    })
    .join("");
}

/**
 * Normalizes and cleans description text for Python.
 */
function normalizeDescription(description: string): string {
  return normalizeUnicode(description)
    .replace(/\s+/g, " ")
    .replace(/"/g, '\\"')
    .replace(/\n/g, " ")
    .trim();
}

// ============================================================================
// Type Annotation Processing
// ============================================================================

/**
 * Flattens nested Literal types.
 * E.g., Literal['a', Literal['b'], Literal['c']] -> Literal['a', 'b', 'c']
 */
function flattenNestedLiterals(typeAnnotation: string): string {
  let result = typeAnnotation;

  while (result.includes("Literal[")) {
    const before = result;
    result = result.replace(
      /Literal\[((?:[^[\]]|(?:\[[^\]]*\]))*)\]/g,
      (match, inner) => {
        const flattened = inner.replace(/Literal\[/g, "").replace(/\]/g, "");
        return `Literal[${flattened}]`;
      },
    );
    if (before === result) break; // Avoid infinite loop
  }

  return result;
}

/**
 * Removes quotes from forward references but keeps them in Literal values.
 */
function cleanForwardReferences(typeAnnotation: string): string {
  return typeAnnotation.replace(/"([A-Z][a-zA-Z0-9_]*)"/g, (match, name) => {
    const beforeMatch = typeAnnotation.substring(
      0,
      typeAnnotation.indexOf(match),
    );
    const openBrackets = (beforeMatch.match(/\[/g) || []).length;
    const closeBrackets = (beforeMatch.match(/\]/g) || []).length;

    // Keep quotes inside brackets (Literal values)
    if (openBrackets > closeBrackets) {
      return match;
    }
    // Remove quotes for top-level type references
    return name;
  });
}

/**
 * Processes type annotation to Python format.
 * With `from __future__ import annotations`, all annotations are strings by default,
 * so no need to manually quote them.
 */
function processTypeAnnotation(field: ParsedField, externalTypes: Set<string>): string {
  let typeAnnotation = field.pythonType
    // Convert to lowercase built-ins (Python 3.9+ style)
    .replace(/\bType\[/g, "type[")
    .replace(/\bList\[/g, "list[")
    .replace(/\bDict\[/g, "dict[")
    .replace(/Union\[\(([^)]+)\)\]/g, "Literal[$1]")
    .replace(/([A-Z][a-zA-Z0-9]*)<[^>]+>/g, "$1");

  typeAnnotation = flattenNestedLiterals(typeAnnotation);
  typeAnnotation = cleanForwardReferences(typeAnnotation);

  if (field.isArray && !typeAnnotation.startsWith("list[")) {
    // Special case: Resource arrays should become list[dict[str, Any]]
    // to avoid Pydantic rebuild issues with Resource type alias
    if (typeAnnotation === "Resource") {
      typeAnnotation = "list[dict[str, Any]]";
    } else {
      typeAnnotation = `list[${typeAnnotation}]`;
    }
  }
  if (field.optional) {
    typeAnnotation = `Optional[${typeAnnotation}]`;
  }

  // With `from __future__ import annotations`, no need to quote annotations
  // Pydantic v2 handles forward references automatically
  return typeAnnotation;
}

// ============================================================================
// Docstring Generation
// ============================================================================

/**
 * Wraps long text into multiple lines at word boundaries.
 */
function wrapText(text: string, maxWidth: number): string[] {
  const words = text.split(" ");
  const lines: string[] = [];
  let currentLine = "";

  for (const word of words) {
    if (currentLine && currentLine.length + word.length + 1 > maxWidth) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine += (currentLine ? " " : "") + word;
    }
  }
  if (currentLine) lines.push(currentLine);

  return lines;
}

/**
 * Generates a class docstring (single or multi-line).
 */
function generateDocstring(description: string, defaultText: string): string[] {
  if (!description) {
    return [`    """${defaultText}"""`];
  }

  const normalizedDesc = normalizeDescription(description);

  // Single-line docstring
  if (normalizedDesc.length <= MAX_SINGLE_LINE_DOCSTRING) {
    return [`    """${normalizedDesc}"""`];
  }

  // Multi-line docstring
  const lines = wrapText(normalizedDesc, MAX_DOCSTRING_LINE_WIDTH);
  return [
    `    """${lines[0]}`,
    ...lines.slice(1).map((line) => `    ${line}`),
    `    """`,
  ];
}

// ============================================================================
// Field Generation
// ============================================================================

/**
 * Generates Field() arguments for a Pydantic field.
 */
function generateFieldArgs(field: ParsedField): string[] {
  const args: string[] = [`default=${field.optional ? "None" : "..."}`];

  if (field.pythonName !== field.name) {
    args.push(`alias="${field.name}"`);
  }

  if (field.description) {
    const safeDesc = normalizeDescription(field.description);
    args.push(`description="${safeDesc}"`);
  }

  return args;
}

/**
 * Generates a resourceType field declaration.
 */
function generateResourceTypeField(resourceName: string): string[] {
  return [
    `    resource_type: Literal["${resourceName}"] = Field(`,
    `        default="${resourceName}",`,
    `        alias="resourceType"`,
    `    )`,
  ];
}

/**
 * Generates a regular field declaration.
 */
function generateRegularField(
  field: ParsedField,
  externalTypes: Set<string>,
): string {
  const typeAnnotation = processTypeAnnotation(field, externalTypes);
  const fieldArgs = generateFieldArgs(field);
  
  // Add noqa comment if field references undefined forward types
  const hasForwardRef = /\b[A-Z][a-zA-Z0-9]+\b/.test(typeAnnotation) &&
    !typeAnnotation.match(/^(Optional|list|dict|Union|Literal)\[/);
  const noqaComment = hasForwardRef && !externalTypes.has(typeAnnotation.replace(/^Optional\[|\]$/g, ''))
    ? "  # noqa: F821"
    : "";
  
  return `    ${field.pythonName}: ${typeAnnotation} = Field(${fieldArgs.join(", ")})${noqaComment}`;
}

// ============================================================================
// Class Generation
// ============================================================================

/**
 * Generates a single Pydantic class from a parsed interface.
 */
function generateClass(
  parsed: ParsedInterface,
  externalTypes: Set<string>,
): string[] {
  const lines: string[] = [];

  lines.push(`class ${parsed.name}(${BASE_CLASS}):`);

  // Docstring
  lines.push(
    ...generateDocstring(parsed.description, `${parsed.name} FHIR resource`),
  );
  lines.push("");

  // resourceType field for FHIR resources
  if (parsed.isResource) {
    lines.push(...generateResourceTypeField(parsed.name));
    lines.push("");
  }

  // Regular fields
  const regularFields = parsed.fields.filter((f) => f.name !== "resourceType");

  if (regularFields.length === 0) {
    lines.push("    pass");
  } else {
    regularFields.forEach((field) => {
      lines.push(generateRegularField(field, externalTypes));
    });
  }

  return lines;
}

// ============================================================================
// File Generation
// ============================================================================

/**
 * Generates import section of the Python file.
 */
function generateImports(
  typingImports: string[],
  externalImports: string[],
  needsTypeVar: boolean,
): string[] {
  const lines: string[] = [];

  // Standard library imports
  lines.push(`from typing import ${typingImports.join(", ")}`);
  lines.push("");

  // Third-party imports
  lines.push(PYDANTIC_IMPORT);
  lines.push("");

  // Local imports
  lines.push(BASE_IMPORT);

  // TypeVar definition (must come after all imports)
  if (needsTypeVar) {
    lines.push("");
    lines.push('T = TypeVar("T")');
  }

  // No longer need TYPE_CHECKING imports - using string annotations instead
  return lines;
}

/**
 * Generates complete Pydantic file from parsed TypeScript interfaces.
 */
export function generatePydanticFile(parsedFile: ParsedFile): string {
  const lines: string[] = [...PYTHON_HEADER];

  // Analyze what imports are needed
  const typingImportFlags = analyzeTypingImports(parsedFile);
  const externalImports = extractExternalImports(parsedFile);
  const externalTypes = new Set(externalImports);
  const typingImports = buildTypingImports(typingImportFlags, false);

  // Generate imports
  lines.push(
    ...generateImports(
      typingImports,
      externalImports,
      typingImportFlags.hasTypeVar,
    ),
  );
  lines.push("");

  // Generate classes
  parsedFile.interfaces.forEach((parsed, index) => {
    if (index > 0) {
      lines.push("");
      lines.push(""); // Two blank lines between classes (PEP 8)
    }
    lines.push(...generateClass(parsed, externalTypes));
  });

  // Register models for centralized rebuilding to handle circular dependencies
  if (parsedFile.interfaces.length > 0) {
    lines.push("");
    lines.push("");
    lines.push("# Register models for forward reference resolution");
    lines.push("from typing import TYPE_CHECKING  # noqa: E402");
    lines.push("");
    lines.push("if not TYPE_CHECKING:");
    lines.push("    from pymedplum.fhir._rebuild import register_model  # noqa: E402");
    lines.push("");
    parsedFile.interfaces.forEach((parsed) => {
      lines.push(`    register_model("${parsed.name}", ${parsed.name})`);
    });
  }

  return lines.join("\n") + "\n";
}

// ============================================================================
// Legacy Support & Module Exports
// ============================================================================

/**
 * @deprecated Use generatePydanticFile instead
 */
export function generatePydanticClass(parsed: ParsedInterface): string {
  const parsedFile: ParsedFile = {
    interfaces: [parsed],
    allImports: parsed.imports,
    localTypes: new Set([parsed.name]),
  };
  return generatePydanticFile(parsedFile);
}

/**
 * Generates __init__.py file for the fhir module.
 */
export function generateInitFile(
  resourceNames: string[],
  classesToFiles: Map<string, string>
): string {
  const lines: string[] = [
    "# Generated FHIR module",
    "# Do not edit manually",
    "",
    "# Import classes directly from their respective modules, e.g.:",
    "# from pymedplum.fhir.patient import Patient",
    "# from pymedplum.fhir.organization import Organization",
    "",
    "import importlib",
    "from typing import TYPE_CHECKING, Any, Literal",
    "",
  ];

  // Create ResourceType as a Literal of all resource type strings
  const resourceTypeStrings = resourceNames.sort().map(name => `"${name}"`).join(", ");
  lines.push(`# ResourceType is a Literal of all FHIR resource type strings`);
  lines.push(`ResourceType = Literal[${resourceTypeStrings}]`);
  lines.push("");
  
  lines.push("if TYPE_CHECKING:");
  lines.push("    # Resource is a union of all FHIR resource types");
  lines.push("    # Import all resources for type checking");
  
  // Group classes by their file for TYPE_CHECKING imports
  const fileToClasses = new Map<string, string[]>();
  resourceNames.forEach((className) => {
    const fileName = classesToFiles.get(className) || className.toLowerCase();
    if (!fileToClasses.has(fileName)) {
      fileToClasses.set(fileName, []);
    }
    fileToClasses.get(fileName)!.push(className);
  });

  // Add imports inside TYPE_CHECKING block
  Array.from(fileToClasses.keys())
    .sort()
    .forEach((fileName) => {
      const classes = fileToClasses.get(fileName)!.sort();
      lines.push(
        `    from pymedplum.fhir.${fileName} import ${classes.join(", ")}`
      );
    });
  
  lines.push("");
  const resourceTypesForUnion = resourceNames.sort().join(" | ");
  lines.push(`    Resource = ${resourceTypesForUnion}`);
  lines.push("else:");
  lines.push("    # At runtime, use Any to avoid circular import issues");
  lines.push("    Resource = Any");
  lines.push("");
  lines.push("__all__ = [\"Resource\", \"ResourceType\"]");
  lines.push("");
  lines.push("# Import all modules to trigger model registration");
  
  // Import all modules at runtime to register models
  const fileNames = Array.from(fileToClasses.keys()).sort();
  fileNames.forEach((fileName) => {
    lines.push(`importlib.import_module("pymedplum.fhir.${fileName}")`);
  });
  
  lines.push("");
  lines.push("# Register special types for forward reference resolution");
  lines.push("from pymedplum.fhir._rebuild import register_model, rebuild_all_models  # noqa: E402");
  lines.push("register_model('ResourceType', ResourceType)");
  lines.push("register_model('Resource', Resource)  # Needed for type resolution even though it's Any at runtime");
  lines.push("");
  lines.push("# Rebuild all models to resolve forward references");
  lines.push("rebuild_all_models()");

  return lines.join("\n") + "\n";
}

/**
 * Generates _rebuild.py module for centralized model rebuilding.
 */
export function generateRebuildModule(): string {
  return `"""Central registry for handling model rebuilding with circular references.

This module provides a centralized approach to resolving forward references
in Pydantic models with circular dependencies. Models register themselves
upon module import, and are rebuilt after all modules are loaded.
"""

from typing import Any

# Global namespace that collects all models
_models_namespace: dict[str, Any] = {}


def register_model(name: str, model: Any) -> None:
    """Register a model to be available for forward reference resolution.

    Args:
        name: The name of the model class
        model: The model class itself
    """
    _models_namespace[name] = model


def rebuild_all_models() -> None:
    """Rebuild all registered models with the complete namespace.

    This resolves all forward references by providing each model with
    a namespace containing all registered models.
    """
    for model in _models_namespace.values():
        if hasattr(model, "model_rebuild"):
            # Pass the complete namespace for resolving forward references
            model.model_rebuild(_types_namespace=_models_namespace)
`;
}
