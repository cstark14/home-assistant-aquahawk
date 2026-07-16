"""Tests for AquaHawk hostname normalization."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


module_path = (
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "aquahawk"
    / "util.py"
)

spec = spec_from_file_location("aquahawk_util", module_path)
util_module = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(util_module)


def test_normalize_hostname_leaves_plain_hostname_unchanged():
    """A plain hostname should be preserved."""
    assert util_module.normalize_hostname("city.aquahawk.us") == "city.aquahawk.us"


def test_normalize_hostname_strips_scheme_and_path():
    """A full portal URL should be converted to a hostname."""
    assert (
        util_module.normalize_hostname("https://city.aquahawk.us/customers/login")
        == "city.aquahawk.us"
    )


def test_normalize_hostname_preserves_port():
    """Non-default ports should be preserved."""
    assert util_module.normalize_hostname("https://city.aquahawk.us:8443") == (
        "city.aquahawk.us:8443"
    )


@pytest.mark.parametrize("hostname", ["", "   ", "https://"])
def test_normalize_hostname_rejects_invalid_values(hostname):
    """Invalid hostname values should be rejected."""
    with pytest.raises(ValueError):
        util_module.normalize_hostname(hostname)
