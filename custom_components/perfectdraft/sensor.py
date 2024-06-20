import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from .perfectdraft_api import PerfectDraftAPI

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the PerfectDraft sensors."""
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    x_api_key = config_entry.data.get("x_api_key")
    recaptcha_site_key = config_entry.data.get("recaptcha_site_key")
    recaptcha_secret_key = config_entry.data.get("recaptcha_secret_key")

    api = PerfectDraftAPI(email, password, x_api_key, recaptcha_site_key, recaptcha_secret_key)
    if not api.authenticate():
        _LOGGER.error("Authentication failed")
        return

    sensors = []
    user_info = api.get_user_info()
    if user_info and 'machines' in user_info:
        for machine in user_info['machines']:
            sensors.append(PerfectDraftMachineSensor(api, machine['id'], machine['name']))
    async_add_entities(sensors, True)

class PerfectDraftMachineSensor(Entity):
    def __init__(self, api, machine_id, name):
        self._api = api
        self._machine_id = machine_id
        self._name = name
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        machine_info = self._api.get_machine_info(self._machine_id)
        if machine_info:
            self._state = machine_info.get('temperature')
            self._attributes = {
                'pressure': machine_info.get('pressure'),
                'eco_mode': machine_info.get('eco_mode'),
                'door_open': machine_info.get('door_open'),
                'last_pour_duration': machine_info.get('last_pour_duration'),
                'pours_since_startup': machine_info.get('pours_since_startup'),
                'serial_number': machine_info.get('serial_number'),
            }
