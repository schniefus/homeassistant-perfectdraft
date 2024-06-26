import logging
from homeassistant.helpers.entity import Entity
from .api import PerfectDraftAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the PerfectDraft sensors."""
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    x_api_key = config_entry.data.get("x_api_key")
    recaptcha_token = config_entry.data.get("recaptcha_token")

    api = PerfectDraftAPI(email, password, x_api_key, recaptcha_token)
    api.authenticate()
    status = api.get_status()
    machine_id = status['machine_id']
    machine_details = api.get_machine_details(machine_id)

    sensors = [
        PerfectDraftSensor(api, "Temperature", machine_details['temperature']),
        PerfectDraftSensor(api, "Pressure", machine_details['pressure']),
        PerfectDraftSensor(api, "Door Status", machine_details['door_status'])
    ]

    async_add_entities(sensors, True)

class PerfectDraftSensor(Entity):
    def __init__(self, api, name, state):
        self._api = api
        self._name = name
        self._state = state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Re-authenticate if necessary
        if not self._api.access_token:
            self._api.authenticate()
        
        # Fetch the latest machine details
        status = self._api.get_status()
        machine_id = status['machine_id']
        machine_details = self._api.get_machine_details(machine_id)

        if self._name == "Temperature":
            self._state = machine_details['temperature']
        elif self._name == "Pressure":
            self._state = machine_details['pressure']
        elif self._name == "Door Status":
            self._state = machine_details['door_status']
