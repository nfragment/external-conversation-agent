from typing import Literal
import aiohttp

from homeassistant.components import conversation
from homeassistant.components.conversation import (
    ConversationEntity,
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
    ChatLog,
    AssistantContent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import MATCH_ALL
from homeassistant.helpers import intent

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the External conversation platform from a config entry."""
    
    endpoint_url = entry.data["endpoint_url"]

    async_add_entities([ExternalConversationAgent(hass, entry, endpoint_url)])


class ExternalConversationAgent(ConversationEntity, AbstractConversationAgent):
    """External conversation agent entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        endpoint_url: str,
    ):
        """Initialize the agent."""
        super().__init__()
        self.hass = hass
        self.entry = entry
        self._endpoint_url = endpoint_url

    async def async_added_to_hass(self) -> None:
        """Register agent when entity is added."""
        await super().async_added_to_hass()
        conversation.async_set_agent(self.hass, self.entry, self)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister agent when entity is removed."""
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

    @property
    def name(self) -> str:
        return "External Conversation Agent"

    @property
    def unique_id(self) -> str:
        return f"external_conversation_agent_{self.entry.entry_id}"

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def _async_handle_message(
        self,
        user_input: ConversationInput,
        chat_log: ChatLog,
    ) -> ConversationResult:
        """Handle incoming message by sending it to external API."""

        text = user_input.text

        headers = {"Content-Type": "application/json"}

        payload = {
            "text": text,
            "context": user_input.context.as_dict() if user_input.context else {},
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._endpoint_url, json=payload, headers=headers, timeout=10
                ) as response:
                    if response.status != 200:
                        response_text = "Error, External server couldn't process your request right now."
                    else:
                        data = await response.json()
                        response_text = data.get("response", "Sorry, I didn't understand that.")
        except Exception as exc:
            response_text = "Error, unable to communicate with external server."

        # Add assistant content to chat log
        chat_log.async_add_assistant_content_without_tools(
            AssistantContent(agent_id=user_input.agent_id, content=response_text)
        )

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response_text)

        return ConversationResult(
            conversation_id=None,
            response=intent_response,
            continue_conversation=False,
        )
