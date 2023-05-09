"""The Stadtreinigung Hamburg integration"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

DOMAIN = "stadtreinigung_hamburg"


async def async_setup(hass, config):
    """Do not allow config via configuration.yaml"""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Stadtreinigung Hamburg as config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True
