import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class PerfectDraftConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="PerfectDraft", data=user_input)

        data_schema = vol.Schema({
            vol.Required("email"): str,
            vol.Required("password"): str,
            vol.Required("x_api_key"): str,
            vol.Required("recaptcha_site_key"): str,
            vol.Required("recaptcha_secret_key"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PerfectDraftOptionsFlowHandler(config_entry)

class PerfectDraftOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("email", default=self.config_entry.data.get("email")): str,
            vol.Optional("password", default=self.config_entry.data.get("password")): str,
            vol.Optional("x_api_key", default=self.config_entry.data.get("x_api_key")): str,
            vol.Optional("recaptcha_site_key", default=self.config_entry.data.get("recaptcha_site_key")): str,
            vol.Optional("recaptcha_secret_key", default=self.config_entry.data.get("recaptcha_secret_key")): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
