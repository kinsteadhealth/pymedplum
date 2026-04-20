/**
 * TypeScript AST parser for Medplum FHIR type definitions.
 *
 * Parses .d.ts files and extracts interface definitions, fields, types,
 * and documentation to prepare for Pydantic model generation.
 */

import * as ts from "typescript";
import * as fs from "fs";

// ============================================================================
// Type Definitions
// ============================================================================

export interface ParsedField {
  name: string;
  pythonName: string;
  type: string;
  pythonType: string;
  optional: boolean;
  description: string;
  isArray: boolean;
  isReadonly: boolean;
}

export interface ParsedInterface {
  name: string;
  description: string;
  fields: ParsedField[];
  imports: Set<string>;
  isResource: boolean;
}

export interface ParsedFile {
  interfaces: ParsedInterface[];
  allImports: Set<string>;
  localTypes: Set<string>;
}

// ============================================================================
// Constants
// ============================================================================

const TYPE_MAP: Record<string, string> = {
  string: "str",
  number: "Union[int, float]",
  boolean: "bool",
  any: "Any",
  unknown: "Any",
  object: "Dict[str, Any]",
  null: "None",
  undefined: "None",
};

const PYTHON_KEYWORDS = new Set([
  "and",
  "as",
  "assert",
  "break",
  "class",
  "continue",
  "def",
  "del",
  "elif",
  "else",
  "except",
  "False",
  "finally",
  "for",
  "from",
  "global",
  "if",
  "import",
  "in",
  "is",
  "lambda",
  "None",
  "nonlocal",
  "not",
  "or",
  "pass",
  "raise",
  "return",
  "True",
  "try",
  "while",
  "with",
  "yield",
]);

const GENERIC_REGEX = /^([A-Z][a-zA-Z]*)<(.+)>$/;
const UNION_SEPARATOR = " | ";

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Converts camelCase to snake_case and handles Python keywords.
 */
function camelToSnake(str: string): string {
  let result = str
    .replace(/([A-Z])/g, "_$1")
    .toLowerCase()
    .replace(/^_/, "");

  if (PYTHON_KEYWORDS.has(result)) {
    result += "_";
  }

  return result;
}

/**
 * Checks if a type string is a string literal (wrapped in quotes).
 */
function isStringLiteral(type: string): boolean {
  return type.startsWith("'") || type.startsWith('"');
}

/**
 * Maps TypeScript generic types to Python equivalents.
 */
function mapGenericType(container: string, inner: string): string {
  if (container === "Array") {
    return `list[${mapTypeScriptTypeToPython(inner)}]`;
  }
  // For Reference<T> or other generics, use container alone
  // Type parameters are TypeScript-only
  return container;
}

/**
 * Maps TypeScript union types to Python Union or Literal.
 */
function mapUnionType(parts: string[]): string {
  // All string literals -> use Literal instead of Union
  if (parts.every(isStringLiteral)) {
    return `Literal[${parts.join(", ")}]`;
  }

  // Mixed or non-literal union
  const mappedParts = parts.map((t) => mapTypeScriptTypeToPython(t));
  return `Union[${mappedParts.join(", ")}]`;
}

/**
 * Converts TypeScript type to Python type annotation.
 */
function mapTypeScriptTypeToPython(tsType: string): string {
  // Direct primitive type mapping
  if (TYPE_MAP[tsType]) {
    return TYPE_MAP[tsType];
  }

  // Generic types (e.g., "Array<string>", "Reference<Patient | Practitioner>")
  // Handle BEFORE union splitting to avoid breaking on | inside <>
  const genericMatch = tsType.match(GENERIC_REGEX);
  if (genericMatch) {
    const [, container, inner] = genericMatch;
    // Special case: Array<Resource> should become list[dict[str, Any]]
    // to avoid Pydantic rebuild issues with Resource type alias
    if (container === "Array" && inner === "Resource") {
      return "list[dict[str, Any]]";
    }
    return mapGenericType(container, inner);
  }

  // Array types with [] notation
  if (tsType.endsWith("[]")) {
    const elementType = tsType.slice(0, -2);
    // Special case: Resource[] should become list[dict[str, Any]]
    if (elementType === "Resource") {
      return "list[dict[str, Any]]";
    }
    return `list[${mapTypeScriptTypeToPython(elementType)}]`;
  }

  // Union types (e.g., "string | number" or "'a' | 'b'")
  // Handle both " | " and "|" (in case of line breaks or formatting)
  if (tsType.includes("|")) {
    const parts = tsType
      .split("|")
      .map((t) => t.trim())
      .filter((t) => t.length > 0);
    return mapUnionType(parts);
  }

  // Single string literal - must be wrapped in Literal for Python
  if (isStringLiteral(tsType)) {
    return `Literal[${tsType}]`;
  }

  // FHIR types - keep as-is (will be imported)
  return tsType;
}

/**
 * Narrows a TypeScript `number` field to `int` or `float` based on the
 * FHIR polymorphic naming convention (`value[x]` fields).
 *
 * Upstream TypeScript collapses every FHIR numeric primitive (`integer`,
 * `positiveInt`, `unsignedInt`, `integer64`, `decimal`) to `number`, which
 * would otherwise force us to emit `int | float` everywhere. For the
 * ~108 polymorphic fields that encode the primitive in their name suffix
 * (e.g. `valueInteger`, `multipleBirthInteger`, `valueDecimal`,
 * `defaultValuePositiveInt`), we can recover the precise type.
 *
 * Non-polymorphic numeric fields like `sequence`, `rank`, `count` stay
 * as `int | float` because the upstream types don't preserve enough
 * information to distinguish them.
 *
 * Returns the narrowed Python type, or null if no narrowing applies.
 */
function narrowFhirNumericType(
  fieldName: string,
  tsType: string,
): string | null {
  if (tsType !== "number") {
    return null;
  }
  if (/(?:Integer(?:64)?|PositiveInt|UnsignedInt)$/.test(fieldName)) {
    return "int";
  }
  if (/Decimal$/.test(fieldName)) {
    return "float";
  }
  return null;
}

/**
 * Extracts JSDoc comment from a TypeScript node.
 */
function extractJSDocComment(node: ts.Node): string {
  const jsDoc = (ts as any).getJSDocCommentsAndTags(node);
  if (jsDoc && jsDoc.length > 0) {
    const comment = jsDoc[0];
    if (ts.isJSDoc(comment) && comment.comment) {
      return comment.comment.toString();
    }
  }
  return "";
}

/**
 * Parses a TypeScript property signature into a ParsedField.
 */
function parsePropertySignature(
  member: ts.PropertySignature,
  interfaceData: ParsedInterface,
): ParsedField | null {
  const nameNode = member.name;
  if (!ts.isIdentifier(nameNode)) {
    return null;
  }

  const fieldName = nameNode.text;
  const typeNode = member.type;
  let typeText = typeNode?.getText() || "any";
  let isArray = false;

  // Check if array type
  if (typeNode && ts.isArrayTypeNode(typeNode)) {
    isArray = true;
    typeText = typeNode.elementType.getText();
  }

  // Track resourceType discriminators. A top-level FHIR resource in Medplum's
  // TypeScript definitions has its resourceType field typed as a string literal
  // matching the interface name (e.g. `readonly resourceType: 'Patient';`).
  // Backbone elements that happen to carry a resourceType field for metadata
  // purposes are typed as `string` or `ResourceType` — those are NOT resources
  // and must be excluded so downstream allowlist consumers don't accept
  // backbone names like `AccessPolicyResource` as FHIR route segments.
  if (fieldName === "resourceType") {
    const literalName = typeText.replace(/^['"]|['"]$/g, "");
    const isStringLiteral =
      (typeText.startsWith("'") && typeText.endsWith("'")) ||
      (typeText.startsWith('"') && typeText.endsWith('"'));
    if (isStringLiteral && literalName === interfaceData.name) {
      interfaceData.isResource = true;
    }
  }

  const narrowed = narrowFhirNumericType(fieldName, typeText);

  return {
    name: fieldName,
    pythonName: camelToSnake(fieldName),
    type: typeText,
    pythonType: narrowed ?? mapTypeScriptTypeToPython(typeText),
    optional: !!member.questionToken,
    description: extractJSDocComment(member),
    isArray,
    isReadonly:
      member.modifiers?.some((m) => m.kind === ts.SyntaxKind.ReadonlyKeyword) ||
      false,
  };
}

/**
 * Parses a TypeScript interface declaration.
 */
function parseInterfaceDeclaration(
  node: ts.InterfaceDeclaration,
  result: ParsedFile,
): void {
  const interfaceName = node.name.text;
  result.localTypes.add(interfaceName);

  const interfaceData: ParsedInterface = {
    name: interfaceName,
    description: extractJSDocComment(node),
    fields: [],
    imports: new Set(),
    isResource: false,
  };

  // Parse each member/field
  node.members.forEach((member) => {
    if (ts.isPropertySignature(member)) {
      const field = parsePropertySignature(member, interfaceData);
      if (field) {
        interfaceData.fields.push(field);
      }
    }
  });

  result.interfaces.push(interfaceData);
}

/**
 * Parses a TypeScript import declaration.
 */
function parseImportDeclaration(
  node: ts.ImportDeclaration,
  result: ParsedFile,
): void {
  const moduleSpecifier = node.moduleSpecifier;
  if (!ts.isStringLiteral(moduleSpecifier)) {
    return;
  }

  const importClause = node.importClause;
  if (
    importClause?.namedBindings &&
    ts.isNamedImports(importClause.namedBindings)
  ) {
    importClause.namedBindings.elements.forEach((element) => {
      result.allImports.add(element.name.text);
    });
  }
}

// ============================================================================
// Main Parser
// ============================================================================

/**
 * Parses a TypeScript declaration file and extracts all interface definitions.
 *
 * @param filePath - Path to the .d.ts file to parse
 * @returns ParsedFile containing all interfaces, imports, and type information
 */
export function parseTypeScriptFile(filePath: string): ParsedFile {
  const sourceCode = fs.readFileSync(filePath, "utf-8");
  const sourceFile = ts.createSourceFile(
    filePath,
    sourceCode,
    ts.ScriptTarget.Latest,
    true,
  );

  const result: ParsedFile = {
    interfaces: [],
    allImports: new Set(),
    localTypes: new Set(),
  };

  function visit(node: ts.Node): void {
    if (ts.isInterfaceDeclaration(node)) {
      parseInterfaceDeclaration(node, result);
    } else if (ts.isImportDeclaration(node)) {
      parseImportDeclaration(node, result);
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
  return result;
}
