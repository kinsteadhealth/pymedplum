import json
from base64 import urlsafe_b64decode
from datetime import datetime, timezone
from typing import Optional


def decode_jwt_exp(token: str) -> Optional[datetime]:
    """Decode a JWT and extract its expiration time ('exp') claim.

    Args:
        token: The JWT string.

    Returns:
        A datetime object representing the expiration time in UTC, or None if
        the token cannot be decoded or the 'exp' claim is missing.
    """
    try:
        _, payload_b64, _ = token.split(".")
        payload_json = urlsafe_b64decode(payload_b64 + "==").decode("utf-8")
        payload = json.loads(payload_json)

        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

    except (ValueError, IndexError, TypeError):
        return None

    return None
