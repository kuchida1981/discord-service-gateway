from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DISCORD_PUBLIC_KEY: str = "00" * 32
    DISCORD_TOKEN: str = "dummy_token"
    DISCORD_APPLICATION_ID: str = "dummy_app_id"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
