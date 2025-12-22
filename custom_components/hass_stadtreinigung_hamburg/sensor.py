import logging
from typing import Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import slugify

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_STREET = "street"
CONF_NUMBER = "number"
CONF_ASID = "asid"
CONF_HNID = "hnid"

ATTR_LAST_UPDATE = "Last update"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STREET): cv.string,
        vol.Required(CONF_NUMBER): cv.string,
        vol.Optional(CONF_ASID): cv.string,
        vol.Optional(CONF_HNID): cv.string,
    }
)

sensors = [
    "Grüne Biotonne",
    "Schwarze Restmülltonne",
    "Gelbe Wertstofftonne/-sack",
    "Blaue Papiertonne",
    "Weihnachtsbäume",
    "Laubsäcke",
]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up components.

    Can only be called when a user accidentally mentions stadtreinigung_hamburg in the
    config. In that case it will be ignored.
    """
    pass


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for sensor_type in sensors:
        entities.append(StadtreinigungHamburgSensor(coordinator, sensor_type))

    async_add_entities(entities)


class StadtreinigungHamburgSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Stadtreinigung Hamburg sensor."""

    def __init__(self, coordinator, container: str):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.container = container
        self._attr_name = container
        self._attr_icon = "mdi:recycle"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

        # Home Assistant automatically generates entity_id from unique_id and name.
        # Manual entity_id assignment is deprecated and can cause issues with entity registry.
        self._attr_unique_id = (
            f"stadtreinigung_hamburg_{coordinator.location_name}_{container}"
        )
        
        # Group all sensors under a single device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.location_name)},
            name=f"Stadtreinigung Hamburg {coordinator.location_name}",
            manufacturer="Stadtreinigung Hamburg",
            model="Waste Collection Schedule",
        )

    @property
    def native_value(self) -> Optional[str]:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        collections = sorted(self.coordinator.data, key=lambda x: x.date)

        if collections:
            collection = next(
                (c for c in collections if c.container == self.container), None
            )

            if collection:
                return collection.date.isoformat()

        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        # Coordinator automatically handles update timing
        return {}
