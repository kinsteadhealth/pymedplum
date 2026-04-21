# Welcome to pymedplum!

`pymedplum` is an unofficial Python SDK for [Medplum](https://www.medplum.com), providing a convenient interface for interacting with a Medplum server's FHIR API. It is designed to be intuitive, robust, and fully typed.

This library allows you to:

- Authenticate with a Medplum server.
- Perform CRUD (Create, Read, Update, Delete) operations on FHIR resources.
- Search for FHIR resources using powerful query parameters.
- Execute GraphQL queries for complex data retrieval.
- Work with fully-typed Pydantic models for all FHIR resources, providing excellent editor support and data validation.
- Run an optional MCP server for agent-based workflows.

---

## Start here

- [Installation](installation.md)
- [Quickstart](quickstart.md)
- [MCP Server](mcp.md)

## Core concepts

- [FHIR Models](fhir_models.md)
- [Client Design](client_design.md)

## Advanced

- [Advanced Usage (overview)](advanced_usage.md)
- [On-Behalf-Of](advanced/on_behalf_of.md)
- [Audit Logging](advanced/audit_logging.md)
- [MCP Server](mcp.md)

## Reference

- [Client API Reference](api_reference.md)
- [Utility Functions](utils.md)

## Help

- [FAQ & Troubleshooting](faq.md)

---

_PyMedplum is an independent Python client and is **not affiliated with, endorsed by, or sponsored by Orangebot, Inc.**, the makers of [Medplum](https://www.medplum.com) ([upstream repo](https://github.com/medplum/medplum)). "Medplum" is a product and trademark of Orangebot, Inc. "FHIR" is a registered trademark of Health Level Seven International. Use of these names here is purely descriptive._

Built and maintained by [Kinstead Health](https://www.kinsteadhealth.com).
