import sys
import httpx
from src.core.config import settings

def register_commands():
    app_id = settings.DISCORD_APPLICATION_ID
    token = settings.DISCORD_TOKEN
    guild_id = settings.DISCORD_GUILD_ID

    if not token or token == "dummy_token":
        print("Error: DISCORD_TOKEN is not set.")
        sys.exit(1)

    if not app_id or app_id == "dummy_app_id":
        print("Error: DISCORD_APPLICATION_ID is not set.")
        sys.exit(1)

    # Define commands
    commands = [
        {
            "name": "ping",
            "description": "Replies with Pong!",
            "type": 1,  # CHAT_INPUT
        }
    ]

    # Registration URL
    if guild_id:
        url = f"https://discord.com/api/v10/applications/{app_id}/guilds/{guild_id}/commands"
        print(f"Registering commands to guild: {guild_id}")
    else:
        url = f"https://discord.com/api/v10/applications/{app_id}/commands"
        print("Registering global commands")

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.put(url, headers=headers, json=commands)
        response.raise_for_status()
        print(f"Successfully registered commands: {response.status_code}")
        print(response.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    register_commands()
