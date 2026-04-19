# Security Policy

## Reporting a Vulnerability

PyMedplum is a Python SDK used to interact with Medplum FHIR servers,
which typically hold protected health information (PHI). Security issues
in this library can have direct implications for clinical data handling.

If you believe you have found a security vulnerability — whether a bug,
a misconfiguration, a dependency issue, or a design flaw — please report
it privately rather than opening a public GitHub issue.

**Contact:** [security@kinsteadhealth.com](mailto:security@kinsteadhealth.com)

When reporting, it's helpful to include:

- A description of the issue and the impact you believe it has
- Steps to reproduce (a minimal script or failing test is ideal)
- The version of `pymedplum` you tested against
- Whether you are aware of any active exploitation

You should expect an acknowledgement within a few business days. We will
work with you on disclosure timing and credit.

## Scope

- Bugs or design issues in `pymedplum` itself (client, MCP server,
  generated FHIR models).
- Vulnerable dependencies where the exposure is specific to how this
  package uses them.

Issues in the Medplum server, the `@medplum/fhirtypes` upstream, or the
HL7 FHIR specification itself are out of scope — please report those to
the relevant upstream project.

## Please Do Not

- Include protected health information (PHI), real patient data, or
  production credentials in reports. Use synthetic data for
  reproduction steps.
- Publicly disclose the issue before we have had a chance to respond
  and, if needed, ship a fix.
