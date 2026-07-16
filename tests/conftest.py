"""Test configuration for AquaHawk unit tests."""

import sys
import types


homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")
const = types.ModuleType("homeassistant.const")

config_entries.ConfigEntry = type("ConfigEntry", (), {})
core.HomeAssistant = type("HomeAssistant", (), {})
const.Platform = type("Platform", (), {"SENSOR": "sensor"})

homeassistant.config_entries = config_entries
homeassistant.core = core
homeassistant.const = const

sys.modules.setdefault("homeassistant", homeassistant)
sys.modules.setdefault("homeassistant.config_entries", config_entries)
sys.modules.setdefault("homeassistant.core", core)
sys.modules.setdefault("homeassistant.const", const)
