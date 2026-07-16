"""Utilities for the AquaHawk integration."""

from urllib.parse import urlsplit


def normalize_hostname(hostname: str) -> str:
    """Normalize an AquaHawk hostname or URL to a bare host[:port] value."""
    normalized = hostname.strip()
    if not normalized:
        raise ValueError("Hostname is required")

    if "://" not in normalized:
        normalized = f"https://{normalized}"

    parsed = urlsplit(normalized)
    if parsed.hostname is None:
        raise ValueError("Hostname is invalid")

    if parsed.port is not None:
        return f"{parsed.hostname}:{parsed.port}"

    return parsed.hostname
