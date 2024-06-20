from homeassistant.core import HomeAssistant

DOMAIN = "perfectdraft"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the PerfectDraft component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up PerfectDraft from a config entry."""
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
