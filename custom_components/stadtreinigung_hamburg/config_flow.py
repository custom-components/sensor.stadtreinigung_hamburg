from homeassistant import config_entries
import voluptuous as vol
from homeassistant.util import slugify
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback

from stadtreinigung_hamburg.StadtreinigungHamburg import *

DOMAIN = "stadtreinigung_hamburg"


@callback
def stadtreinigung_hamburg_names(hass: HomeAssistant):
    """Return configurations of Stadtreinigung Hamburg component."""
    return set(
        (slugify(entry.data[CONF_NAME]))
        for entry in hass.config_entries.async_entries(DOMAIN)
    )


@config_entries.HANDLERS.register(DOMAIN)
class StadtreinigungHamburgConfigFlow(config_entries.ConfigFlow):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._street = None
        self._number = None
        self._errors = {}

    async def async_step_user(self, user_input=None):
        self._errors = {}

        if user_input is not None:
            name = slugify(user_input[CONF_NAME])

            try:
                srh = StadtreinigungHamburg()
                srh.get_garbage_collections(user_input["street"], user_input["number"])
            except StreetNotFoundException as error:
                self._errors["street"] = "street_not_found"
            except StreetNumberNotFoundException as error:
                self._errors["number"] = "number_not_found"
                numbers = [x[0] for x in error.args[1]]
                print(numbers)
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                            vol.Required("street", default=user_input["street"]): str,
                            vol.Required(
                                "number", default=user_input["number"]
                            ): vol.In(numbers),
                        }
                    ),
                    errors=self._errors,
                )

            if not self._name_in_configuration_exists(name):
                if self._errors == {}:
                    print("CREATE ENTRY!")
                    return self.async_create_entry(
                        title=user_input[CONF_NAME], data=user_input
                    )
            else:
                self._errors[CONF_NAME] = "name_exists"
        else:
            user_input = {CONF_NAME: None, "street": None, "number": None}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                    vol.Required("street", default=user_input["street"]): str,
                    vol.Required("number", default=user_input["number"]): str,
                }
            ),
            errors=self._errors,
        )

    def _name_in_configuration_exists(self, name: str) -> bool:
        """Return True if name exists in configuration."""
        if name in stadtreinigung_hamburg_names(self.hass):
            return True
        return False
