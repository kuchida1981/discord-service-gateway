"""Application configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    DISCORD_PUBLIC_KEY: str = "00" * 32
    DISCORD_TOKEN: str = "dummy_token"
    DISCORD_APPLICATION_ID: str = "dummy_app_id"
    DISCORD_GUILD_ID: str | None = None

    NGROK_AUTHTOKEN: str | None = None
    NGROK_DOMAIN: str | None = None

    N8N_HEALTH_URL: str

    # Cloud Run Proxy Settings
    MODE: str = "prod"  # prod, dev, local
    FORWARD_URL: str | None = None  # ngrok URL for dev mode
    PROXY_SECRET: str | None = None  # Optional secret for proxy authentication

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
