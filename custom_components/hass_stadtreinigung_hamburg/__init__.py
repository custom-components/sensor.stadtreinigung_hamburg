"""The Stadtreinigung Hamburg integration"""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from stadtreinigung_hamburg.StadtreinigungHamburg import StadtreinigungHamburg

_LOGGER = logging.getLogger(__name__)

DOMAIN = "stadtreinigung_hamburg"
PLATFORMS = [Platform.SENSOR]
UPDATE_INTERVAL = timedelta(hours=1)


async def async_setup(hass, config):
    """Do not allow config via configuration.yaml"""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Stadtreinigung Hamburg as config entry."""

    # Create coordinator for this config entry
    coordinator = StadtreinigungHamburgCoordinator(
        hass,
        config_entry.data[CONF_NAME],
        config_entry.data["street"],
        config_entry.data["number"],
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


class StadtreinigungHamburgCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data fetching for Stadtreinigung Hamburg."""

    def __init__(self, hass: HomeAssistant, name: str, street: str, number: str):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Stadtreinigung Hamburg {name}",
            update_interval=UPDATE_INTERVAL,
        )
        self.street = street
        self.number = number
        self.location_name = name

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            srh = StadtreinigungHamburg()
            data = await self.hass.async_add_executor_job(
                srh.get_garbage_collections,
                self.street,
                self.number,
            )
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
