import logging
from datetime import timedelta

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

from .perfectdraft_api import PerfectDraftAPI

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = "x_api_key"
CONF_RECAPTCHA_TOKEN = "recaptcha_token"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_RECAPTCHA_TOKEN): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    x_api_key = config[CONF_API_KEY]
    recaptcha_token = config[CONF_RECAPTCHA_TOKEN]

    api = PerfectDraftAPI(email, password, x_api_key)
    if not api.authenticate(recaptcha_token):
        _LOGGER.error("Authentication failed")
        return

    sensors = []
    user_info = api.get_user_info()
    if user_info and 'machines' in user_info:
        for machine in user_info['machines']:
            sensors.append(PerfectDraftMachineSensor(api, machine['id'], machine['name']))
    add_entities(sensors, True)

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
    def update(self):
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

