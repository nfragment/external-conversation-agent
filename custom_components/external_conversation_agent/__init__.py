"""Custom Conversation Agent for Home Assistant that can send all user inputs to any supported external API like Node-Red flows, N8N, LocalAI or custom endpoint"""

from homeassistant.core import HomeAssistant

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration."""
    return True
