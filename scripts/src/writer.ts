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
      // No longer need Optional since we use | None syntax
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

  if (imports.hasTypeVar) {
    typingImports.add("TypeVar");
    typingImports.add("Generic");
  }
  if (imports.hasAny) typingImports.add("Any");
  // No longer need Dict and List - using built-in dict and list
  if (imports.hasLiteral) typingImports.add("Literal");
  // No longer need Optional - using | None syntax
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
    typeAnnotation = `${typeAnnotation} | None`;
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

  const isGeneric = parsed.fields.some((f) => f.pythonType === "T");
  const parentClass = isGeneric ? `${BASE_CLASS}, Generic[T]` : BASE_CLASS;
  lines.push(`class ${parsed.name}(${parentClass}):`);

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

  // TYPE_CHECKING imports for IDE/type checker support
  // These imports have zero runtime cost but make IDEs happy
  if (externalImports.length > 0) {
    lines.push("");
    lines.push("if TYPE_CHECKING:");
    externalImports.forEach((imp) => {
      lines.push(`    from pymedplum.fhir.${imp.toLowerCase()} import ${imp}`);
    });
  }

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
  const externalTypes = new Set<string>(externalImports);
  const hasExternalImports = externalImports.length > 0;
  const typingImports = buildTypingImports(typingImportFlags, hasExternalImports);

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

  lines.push("");

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
    '"""FHIR Resource models with lazy loading support.',
    '',
    'This module provides ~300 FHIR resource type definitions. To avoid massive',
    'startup costs, models are loaded on-demand via __getattr__.',
    '',
    'For static type checking: Use stub file (pymedplum/fhir/__init__.pyi)',
    'For IDE autocompletion: All types appear in autocomplete via __dir__()',
    'For runtime usage: Import normally, models load transparently',
    '',
    'Examples:',
    '    Direct import (lazy loads on access):',
    '    >>> from pymedplum.fhir import Patient',
    '',
    '    Type annotations (work with stub file):',
    '    >>> from pymedplum.fhir import Resource',
    '    >>> def process(r: Resource) -> str: ...',
    '',
    'Performance:',
    '    - First import: ~50ms (loads model + dependencies)',
    '    - Cached access: ~1µs (dict lookup)',
    '    - Type checking: Instant (stub file, no code execution)',
    '"""',
    "",
    "import importlib",
    "import re",
    "import threading",
    "from typing import TYPE_CHECKING, Any",
    "",
    "from .base import MedplumFHIRBase",
    "",
    "# ============================================================================",
    "# Public API",
    "# ============================================================================",
    "",
    "# Lightweight runtime alias; a more specific union is used for type checking",
    "Resource = MedplumFHIRBase",
    "",
    '# ============================================================================',
    '# Thread-Safe Lazy Loading Infrastructure',
    '# ============================================================================',
    '',
    '# Per-model loading lock to prevent redundant concurrent imports',
    '_MODEL_LOCKS: dict[str, threading.RLock] = {}',
    '_MODEL_LOCKS_LOCK = threading.Lock()',
    '',
    '# Shared types namespace for Pydantic model_rebuild() forward reference resolution',
    '_TYPES_NS: dict[str, Any] = {',
    '    "ResourceType": str,',
    '}',
    '',
    '# Global rebuild coordination',
    '_REBUILD_LOCK = threading.RLock()',
    '_TYPES_NS_VERSION = 0',
    '_LAST_REBUILT_VERSION = -1',
    '',
    '# Track which models are currently being loaded to detect circular dependencies',
    '_LOADING_STACK: set[str] = set()',
    '_LOADING_STACK_LOCK = threading.Lock()',
    '',
    "# Registry mapping class names to their module paths",
    "REGISTRY: dict[str, str] = {",
  ];

  // Create the registry dictionary
  resourceNames
    .sort()
    .forEach((className) => {
      const fileName = classesToFiles.get(className) || className.toLowerCase();
      lines.push(`    "${className}": "pymedplum.fhir.${fileName}:${className}",`);
    });

  lines.push("}");
  lines.push("");

	   lines.push(
	     ...[
	       "",
	       "# ============================================================================",
	       "# Introspection Support",
	       "# ============================================================================",
	       "",
	       "def __dir__() -> list[str]:",
	       '    """Return all available resource names for IDE autocompletion.',
	       "",
	       '    IDEs use this to populate autocomplete suggestions. We return:',
	       "    - All registered resource names (REGISTRY.keys())",
	       "    - Already-cached imports (globals())",
	       '    """',
	       "    return sorted(",
	       "        set(",
	       "            list(REGISTRY.keys()) +  # All available resources",
	       "            list(globals().keys())    # Already-cached imports",
	       "        )",
	       "    )",
	       "",
	       "",
	       "# Type names to skip during dependency extraction",
	       "_TYPING_SKIP = {",
	       '    "Optional", "Union", "List", "Dict", "Any", "Literal", "Type",',
	       '    "ForwardRef", "Annotated", "Callable", "Tuple", "Set",',
	       '    "ResourceType",  # TypeScript type alias, not a real Python class',
	       "}",
	       "",
	       "def _get_model_lock(name: str) -> threading.RLock:",
	       '    """Get or create a per-model lock to serialize loading of the same model.',
	       "",
	       "    This prevents multiple threads from simultaneously importing the same model,",
	       "    which could cause import-time state corruption.",
	       '    """',
	       "    with _MODEL_LOCKS_LOCK:",
	       "        if name not in _MODEL_LOCKS:",
	       "            _MODEL_LOCKS[name] = threading.RLock()",
	       "        return _MODEL_LOCKS[name]",
	       "",
	       "",
	       "# ============================================================================",
	       "# Dependency Resolution",
	       "# ============================================================================",
	       "",
	       "def _extract_referenced_types(model_class: type[MedplumFHIRBase]) -> set[str]:",
	       '    """Extract all type references from a model including parent classes via MRO.',
	       "",
	       "    No locks needed here as we're only reading class annotations.",
	       '    """',
	       "    out: set[str] = set()",
	       "    try:",
	       "        for base_class in model_class.__mro__:",
	       "            if (",
	       "                base_class is object",
	       '                or not hasattr(base_class, "__annotations__")',
	       '                or not hasattr(base_class, "__module__")',
	       '                or not base_class.__module__.startswith("pymedplum.fhir")',
	       "            ):",
	       "                continue",
	       "",
	       "            for ann in base_class.__annotations__.values():",
	       '                for m in re.findall(r"\\b([A-Z][a-zA-Z0-9_]*)\\b", str(ann)):',
	       "                    if m in REGISTRY and m not in _TYPING_SKIP:",
	       "                        out.add(m)",
	       "    except Exception:",
	       "        pass",
	       "    return out",
	       "",
	       "",
	       "def _load_model_and_dependencies(",
	       "    name: str, visited: set[str] | None = None, newly_loaded: set[str] | None = None",
	       ") -> None:",
	       '    """Recursively load a model class and all its dependencies with per-model locking.',
	       "",
	       "    Args:",
	       "        name: Name of the model to load",
	       "        visited: Set of already-visited models (prevents infinite recursion)",
	       "        newly_loaded: Set to track which models were loaded in this call",
	       '    """',
	       "    if visited is None:",
	       "        visited = set()",
	       "    if newly_loaded is None:",
	       "        newly_loaded = set()",
	       "",
	       "    if name in visited or name not in REGISTRY:",
	       "        return",
	       "",
	       "    # Detect circular dependencies",
	       "    with _LOADING_STACK_LOCK:",
	       "        if name in _LOADING_STACK:",
	       "            return  # Already being loaded by this or another thread",
	       "        _LOADING_STACK.add(name)",
	       "",
	       "    try:",
	       "        # Acquire per-model lock to serialize loading of this specific model",
	       "        model_lock = _get_model_lock(name)",
	       "        with model_lock:",
	       "            visited.add(name)",
	       "            ",
	       "            # Double-check within the lock: another thread may have loaded this while we waited",
	       "            if name in _TYPES_NS:",
	       "                return",
	       "",
	       "            try:",
	       '                modpath, clsname = REGISTRY[name].split(":")',
	       "                mod = importlib.import_module(modpath)",
	       "                cls = getattr(mod, clsname)",
	       "            except Exception:",
	       "                return",
	       "",
	       "            # Load safely under lock",
	       "            _TYPES_NS[name] = cls",
	       "            newly_loaded.add(name)",
	       "",
	       "            # Load dependencies recursively",
	       "            for dep in _extract_referenced_types(cls):",
	       "                if dep not in _TYPES_NS:",
	       "                    _load_model_and_dependencies(dep, visited, newly_loaded)",
	       "    finally:",
	       "        with _LOADING_STACK_LOCK:",
	       "            _LOADING_STACK.discard(name)",
	       "",
	       "",
	       "# ============================================================================",
	       "# Base Class Preloading",
	       "# ============================================================================",
	       "",
	       "_FHIR_BASE_CLASSES = [",
	       '    "Element",',
	       '    "Extension",',
	       '    "BackboneElement",',
	       '    "Meta",',
	       '    "Narrative",',
	       '    "Identifier",',
	       '    "HumanName",',
	       '    "Address",',
	       '    "ContactPoint",',
	       '    "CodeableConcept",',
	       '    "Coding",',
	       '    "Reference",',
	       '    "Period",',
	       '    "Quantity",',
	       "]",
	       "_BASE_CLASSES_LOADED = False",
	       '_BASE_CLASSES_LOCK = threading.Lock()',
	       "",
	       "",
	       "# ============================================================================",
	       "# Lazy Loading Entry Point",
	       "# ============================================================================",
	       "",
	       "",
	       "def __getattr__(name: str) -> Any:",
	       '    """Lazy load FHIR models on first access with proper thread synchronization.',
	       "",
	       "    This implementation is safe for:",
	       "    - CPython with GIL (Python < 3.13)",
	       "    - CPython without GIL (Python 3.13+)",
	       "    - Other Python implementations (PyPy, Jython, etc.)",
	       "",
	       "    Uses multiple layers of locking:",
	       "    1. Per-model locks: Prevent concurrent imports of the same model",
	       "    2. Rebuild lock: Serialize Pydantic model_rebuild() operations",
	       "    3. Base classes lock: Serialize one-time base class initialization",
	       '    """',
	       "    global _BASE_CLASSES_LOADED, _TYPES_NS_VERSION, _LAST_REBUILT_VERSION  # noqa: PLW0603",
	       "",
	       '    if name.startswith("_"):',
	       "        raise AttributeError(name)",
	       "    if name not in REGISTRY:",
	       "        raise AttributeError(name)",
	       "",
	       "    # First, check if already cached (fast path, no lock needed after first access)",
	       "    if name in _TYPES_NS:",
	       "        # Ensure it's in globals() for subsequent accesses",
	       "        if name not in globals():",
	       "            globals()[name] = _TYPES_NS[name]",
	       "        return _TYPES_NS[name]",
	       "",
	       "    with _REBUILD_LOCK:",
	       "        # Re-check after acquiring lock (another thread may have loaded it)",
	       "        if name in _TYPES_NS:",
	       "            if name not in globals():",
	       "                globals()[name] = _TYPES_NS[name]",
	       "            return _TYPES_NS[name]",
	       "",
	       "        newly_loaded: set[str] = set()",
	       "",
	       "        # One-time initialization of base classes (serialized across all threads)",
	       "        if not _BASE_CLASSES_LOADED:",
	       "            with _BASE_CLASSES_LOCK:",
	       "                # Triple-check pattern: verify again after acquiring lock",
	       "                if not _BASE_CLASSES_LOADED:",
	       "                    for base_name in _FHIR_BASE_CLASSES:",
	       "                        if base_name in REGISTRY and base_name not in _TYPES_NS:",
	       "                            _load_model_and_dependencies(",
	       "                                base_name, newly_loaded=newly_loaded",
	       "                            )",
	       "                    _BASE_CLASSES_LOADED = True",
	       "",
	       "        # Load requested class and its dependencies",
	       "        _load_model_and_dependencies(name, newly_loaded=newly_loaded)",
	       "",
	       "        # Update version if new classes were loaded",
	       "        if newly_loaded:",
	       "            _TYPES_NS_VERSION += 1",
	       "",
	       "        # Rebuild all loaded models when namespace changes",
	       "        # This is expensive but necessary for forward reference resolution",
	       "        if _LAST_REBUILT_VERSION != _TYPES_NS_VERSION:",
	       "            loaded_models = list(_TYPES_NS.values())",
	       "            for model in loaded_models:",
	       '                if hasattr(model, "model_rebuild"):',
	       "                    try:",
	       "                        model.model_rebuild(",
	       "                            _types_namespace=_TYPES_NS, raise_errors=True",
	       "                        )",
	       "                    except Exception as e:",
	       "                        import sys",
	       "                        print(",
	       '                            f"Warning: Failed to rebuild {model.__name__}: {e}",',
	       "                            file=sys.stderr,",
	       "                        )",
	       "            _LAST_REBUILT_VERSION = _TYPES_NS_VERSION",
	       "",
	       "        obj = _TYPES_NS[name]",
	       "        globals()[name] = obj  # Cache to avoid future __getattr__ calls",
	       "        return obj",
	     ]
	   );
	 lines.push("");

  lines.push("# ============================================================================");
  lines.push("# Type Checking Support");
  lines.push("# ============================================================================");
  lines.push("");
  lines.push("if TYPE_CHECKING:");
  lines.push("    # Type checkers get the full union for better inference.");
  lines.push("    # These imports are ONLY used by type checkers, not at runtime.");

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
  lines.push("    # Full type union for static analysis");
  const resourceTypesForUnion = resourceNames.sort().join(" | ");
  lines.push(`    Resource = ${resourceTypesForUnion}`);
  lines.push("");
  lines.push("");
  lines.push("# ============================================================================");
  lines.push("# Module Exports");
  lines.push("# ============================================================================");
  lines.push("");
  lines.push("if TYPE_CHECKING:");
  lines.push("    # For type checkers: export all resource names");
  const allResourceNames = resourceNames.sort();
  lines.push(`    __all__ = [`);
  lines.push(`        "Resource",`);
  // Add resource names in groups of 5 for readability
  for (let i = 0; i < allResourceNames.length; i += 5) {
    const chunk = allResourceNames.slice(i, i + 5);
    lines.push(`        ${chunk.map(n => `"${n}"`).join(", ")},`);
  }
  lines.push(`    ]`);
  lines.push("else:");
  lines.push("    # At runtime: minimal exports (lazy loading handles the rest)");
  lines.push("    __all__ = [\"Resource\"]");

  return lines.join("\n") + "\n";
}

/**
 * Generates simplified .pyi stub file for IDE and type checker support.
 * Uses __all__ list for Pylance autocomplete without complex imports.
 */
export function generateStubFile(
  resourceNames: string[],
  classesToFiles: Map<string, string>
): string {
  const sortedResources = resourceNames.sort();
  
  const lines: string[] = [
    '"""Type stubs for pymedplum.fhir module.',
    'This is a generated file.',
    'Do not edit it manually',
    '',
    "Pylance uses imports to provide autocomplete for all FHIR resources.",
    "The lazy loader (__getattr__) handles actual imports at runtime.",
    '"""',
    "",
    "# ruff: noqa: F822",
    "",
    "from typing import Any",
    "",
  ];
  
  // Group classes by file for organized imports
  const fileToClasses = new Map<string, string[]>();
  sortedResources.forEach((className) => {
    const fileName = classesToFiles.get(className) || className.toLowerCase();
    if (!fileToClasses.has(fileName)) {
      fileToClasses.set(fileName, []);
    }
    fileToClasses.get(fileName)!.push(className);
  });

  // Add all imports at module level for Pylance autocomplete
  lines.push("# Type imports for IDE autocomplete");
  Array.from(fileToClasses.keys())
    .sort()
    .forEach((fileName) => {
      const classes = fileToClasses.get(fileName)!.sort();
      lines.push(`from .${fileName} import ${classes.join(", ")}`);
    });

  lines.push("");
  lines.push("# Stub for runtime lazy loader");
  lines.push("def __getattr__(name: str) -> Any: ...");
  lines.push("");
  lines.push("# Introspection support");
  lines.push("def __dir__() -> list[str]: ...");
  lines.push("");
  lines.push("# Explicit exports for IDE autocomplete");
  lines.push("__all__ = [");
  lines.push('    "Resource",');
  
  // Add all resource names to __all__ for autocomplete
  sortedResources.forEach((name) => {
    lines.push(`    "${name}",`);
  });
  
  lines.push("]");

  return lines.join("\n") + "\n";
}
