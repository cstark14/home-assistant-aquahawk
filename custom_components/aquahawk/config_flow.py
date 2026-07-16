import logging
from typing import Dict, Optional

import aiohttp
from aquahawk_client import AuthenticationError
from homeassistant import config_entries, core
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .client import create_aquahawk_client
from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)
from .util import normalize_hostname

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCOUNT_NUMBER): cv.string,
        vol.Required(CONF_HOSTNAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


async def validate_auth(
    account_number: str,
    hostname: str,
    username: str,
    password: str,
    hass: core.HomeAssistant,
) -> None:
    """Validate AquaHawk credentials."""
    aquahawk = create_aquahawk_client(
        hass, account_number, hostname, username, password
    )
    try:
        await aquahawk.authenticate()
    except AuthenticationError as err:
        raise ValueError from err


class AquahawkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """AquaHawk Custom config flow."""

    async def async_step_user(self, user_input: Optional[Dict[str, str]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                normalized_hostname = normalize_hostname(user_input[CONF_HOSTNAME])
            except ValueError:
                errors["base"] = "invalid_hostname"
            else:
                normalized_input = {
                    **user_input,
                    CONF_HOSTNAME: normalized_hostname,
                }
                try:
                    await validate_auth(
                        normalized_input[CONF_ACCOUNT_NUMBER],
                        normalized_input[CONF_HOSTNAME],
                        normalized_input[CONF_USERNAME],
                        normalized_input[CONF_PASSWORD],
                        self.hass,
                    )
                except ValueError:
                    errors["base"] = "auth"
                except (aiohttp.ClientError, TimeoutError):
                    errors["base"] = "cannot_connect"
                if not errors:
                    return self.async_create_entry(
                        title="AquaHawk", data=normalized_input
                    )

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )
