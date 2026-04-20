"""Shared string constants used by the client, auth, and base modules.

Placed in its own module so ``_auth`` can consume the same auth-header
vocabulary the request path uses without importing ``_base`` (which
would be a cycle).
"""

from __future__ import annotations

AUTHORIZATION_HEADER = "Authorization"
OBO_HEADER = "X-Medplum-On-Behalf-Of"
AUTH_HEADERS_LOWER: frozenset[str] = frozenset(
    {AUTHORIZATION_HEADER.lower(), OBO_HEADER.lower()}
)

MEDPLUM_EXTENDED_HEADER = "X-Medplum"
MEDPLUM_EXTENDED_VALUE = "extended"
