"""Client helpers for the AquaHawk integration."""

from aquahawk_client import AquaHawkClient
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .util import normalize_hostname


def create_aquahawk_client(
    hass: HomeAssistant,
    account_number: str,
    hostname: str,
    username: str,
    password: str,
) -> AquaHawkClient:
    """Create an AquaHawk client using Home Assistant's shared HTTP session.

    Existing config entries may still contain a full AquaHawk portal URL, so
    the hostname is normalized here in addition to config-flow validation.
    """
    return AquaHawkClient(
        account_number,
        normalize_hostname(hostname),
        username,
        password,
        session=async_get_clientsession(hass),
    )
