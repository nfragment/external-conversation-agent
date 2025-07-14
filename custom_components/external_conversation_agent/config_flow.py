import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "external_conversation_agent"

DATA_SCHEMA = vol.Schema({
    vol.Required("endpoint_url"): str,
    vol.Optional("api_key"): str,
})

class ExternalConversationAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for External Conversation Agent."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Use some default name as the config entry title
            return self.async_create_entry(
                title="External Agent",
                data=user_input,
            )

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
