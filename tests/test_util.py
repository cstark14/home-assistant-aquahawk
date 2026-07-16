"""Tests for AquaHawk hostname normalization."""

import pytest

from custom_components.aquahawk.util import normalize_hostname


def test_normalize_hostname_leaves_plain_hostname_unchanged():
    """A plain hostname should be preserved."""
    assert normalize_hostname("city.aquahawk.us") == "city.aquahawk.us"


def test_normalize_hostname_strips_scheme_and_path():
    """A full portal URL should be converted to a hostname."""
    assert (
        normalize_hostname("https://city.aquahawk.us/customers/login")
        == "city.aquahawk.us"
    )


def test_normalize_hostname_preserves_port():
    """Non-default ports should be preserved."""
    assert normalize_hostname("https://city.aquahawk.us:8443") == (
        "city.aquahawk.us:8443"
    )


@pytest.mark.parametrize("hostname", ["", "   ", "https://"])
def test_normalize_hostname_rejects_invalid_values(hostname):
    """Invalid hostname values should be rejected."""
    with pytest.raises(ValueError):
        normalize_hostname(hostname)
