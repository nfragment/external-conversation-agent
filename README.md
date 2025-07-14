# External-Conversation-Agent
A custom conversation agent for Home Assistant that allows to send user input to an external API ( like Node-Red flow, N8N, LocalAI or any other custom api endpoint )

## Devlog

### 14 July 2025
- Latest release of Home Assistant (2025.7.1) is a big step towards standardization of voice related features and has a lot of improvements.
- Now that custom ESPHome voice assistants have feature parity with official Voice PE features, we hope development will be much easier moving forward.
- Voice and conversation features have seen a lot of development in the past year, hence there were a lot of changes happening to the code structure of both Home Assistant and ESPHome.
- Keeping up with everything was not easy and any development that we made would break with the next release.
- In this release some of the important structures related to Voice and AI features are almost standardized (eg conversation, config_entries) so this is a good time to start developing a custom conversation agent and hopefully add all the features that we want.
#### v0.0.1-alpha
- Initialized the repo and added basic files.
#### v0.0.2-alpha
- Starting with reverse engineering official ollama integration
- Looks like async_setup, async_setup_entry and async_unload_entry are needed. Don't know what the function of migrate is.
- Devs also introduced subentry in this release. So yet to figure out how to use it. Skipping for now.
#### v0.0.3-alpha
- Added HACS support
#### v0.0.4-alpha
- Adding config_flow and config_entries for setting up the integration from the UI.
- Forward the config entry setup to the 'conversation' platform only as the ai_task platform is not required for our current usecase.
- Config entry is loading when integration is added, but errors out because of missing conversation platform.
### 15 July 2025
#### v0.0.5-alpha
- Looks like in the new structure the conversation agent must be defined as an entity and then added to home assistant asynchronously using async_add_entities
- When these entities are added or removed, the agents will be set and unset in the conversation platform.
- supported_languages property is very important, without this the agent will not load.
- Added dummy response text for testing before implementing the api call
- Tested by adding integration and the conversation agent shows up as a new entity in the ui.
- Chatting with the agent gives the predefined static response as expected.
#### v0.0.6-alpha
- Using aiohttp for communicating with external api/server.
- Implemented api call.
- Added basic error handling using try except.
- Created a Node-Red flow that will send back the user input along with a predefined text. 
- Tested the conversation using Node-Red as endpoint (basic http without any authentication).
- The component is ready for beta release.