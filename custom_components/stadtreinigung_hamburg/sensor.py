import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle, slugify
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, DEVICE_CLASS_TIMESTAMP
from homeassistant.helpers.entity import Entity
import logging
from datetime import datetime
from datetime import timedelta
from homeassistant.core import HomeAssistant
from typing import Optional

from stadtreinigung_hamburg.StadtreinigungHamburg import StadtreinigungHamburg

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)

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
    "grüne Biotonne",
    "schwarze Restmülltonne",
    "gelbe Wertstofftonne/-sack",
    "blaue Papiertonne",
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
    hass: HomeAssistant, config_entry: ConfigEntry, config_entries
) -> bool:
    """Add a weather entity from map location."""
    config = config_entry.data
    name = slugify(config[CONF_NAME])

    data = StadtreinigungHamburgData(
        config[CONF_NAME], config["street"], config["number"]
    )

    entries = []
    for sensor in sensors:
        entity = StadtreinigungHamburgSensor(sensor, data)
        entity.entity_id = "sensor.stadtreinigung_hamburg_{}_{}".format(name, sensor)
        entries.append(entity)

    config_entries(entries, True)
    return True


class StadtreinigungHamburgSensor(Entity):
    def __init__(self, container, data):
        self.container = container
        self.data = data
        self._state = None
        self._last_update = None
        self._uuid = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.container

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ""

    @property
    def device_class(self) -> Optional[str]:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_TIMESTAMP

    @property
    def device_state_attributes(self):
        return {ATTR_LAST_UPDATE: self._last_update}

    @property
    def unique_id(self):
        return "stadtreinigung_hamburg" + self.data.name + self.container

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:recycle"

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self.data.update()
        collections = sorted(self.data.data, key=lambda x: x.date)

        if collections:
            collection = next(
                (c for c in collections if c.container == self.container), None
            )

            if collection:
                self._state = collection.date
                self._uuid = collection.uuid
                self._last_update = self.data.last_update

                _LOGGER.debug(collection)
            else:
                self._state = None
        else:
            self._state = None


class StadtreinigungHamburgData:
    """Get the latest data and update the states."""

    def __init__(self, name, street, number, use_asid=False, use_hnid=False):
        self.name = name
        self.street = street
        self.number = number
        self.use_asid = use_asid
        self.use_hnid = use_hnid
        self.last_update = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug("Updating garbage collection dates")

        try:
            self.data = StadtreinigungHamburg().get_garbage_collections(
                self.street, self.number, self.use_asid, self.use_hnid
            )
            self.last_update = datetime.today().strftime("%Y-%m-%d %H:%M")
        except Exception as error:
            _LOGGER.error("Error occurred while fetching data: %r", error)
            self.data = None
            return False
