"""Application configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    DISCORD_PUBLIC_KEY: str = "00" * 32
    DISCORD_TOKEN: str = "dummy_token"  # noqa: S105
    DISCORD_APPLICATION_ID: str = "dummy_app_id"
    DISCORD_GUILD_ID: str | None = None

    NGROK_AUTHTOKEN: str | None = None
    NGROK_DOMAIN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
