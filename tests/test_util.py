"""Tests for AquaHawk hostname normalization."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "aquahawk"
    / "util.py"
)

SPEC = spec_from_file_location("aquahawk_util", MODULE_PATH)
UTIL = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(UTIL)


def test_normalize_hostname_leaves_plain_hostname_unchanged():
    """A plain hostname should be preserved."""
    assert UTIL.normalize_hostname("city.aquahawk.us") == "city.aquahawk.us"


def test_normalize_hostname_strips_scheme_and_path():
    """A full portal URL should be converted to a hostname."""
    assert (
        UTIL.normalize_hostname("https://city.aquahawk.us/customers/login")
        == "city.aquahawk.us"
    )


def test_normalize_hostname_preserves_port():
    """Non-default ports should be preserved."""
    assert UTIL.normalize_hostname("https://city.aquahawk.us:8443") == (
        "city.aquahawk.us:8443"
    )
