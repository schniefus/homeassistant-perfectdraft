import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class PerfectDraftConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PerfectDraft."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="PerfectDraft", data=user_input)

        data_schema = vol.Schema({
            vol.Required("email"): cv.string,
            vol.Required("password"): cv.string,
            vol.Required("x_api_key"): cv.string,
            vol.Required("recaptcha_site_key"): cv.string,
            vol.Required("recaptcha_secret_key"): cv.string,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PerfectDraftOptionsFlow(config_entry)

class PerfectDraftOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for PerfectDraft."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required("email", default=self.config_entry.data.get("email")): cv.string,
            vol.Required("password", default=self.config_entry.data.get("password")): cv.string,
            vol.Required("x_api_key", default=self.config_entry.data.get("x_api_key")): cv.string,
            vol.Required("recaptcha_site_key", default=self.config_entry.data.get("recaptcha_site_key")): cv.string,
            vol.Required("recaptcha_secret_key", default=self.config_entry.data.get("recaptcha_secret_key")): cv.string,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
