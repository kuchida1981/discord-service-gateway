"""Project-wide custom exception classes."""


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""


class MissingTokenError(ConfigurationError):
    """Raised when DISCORD_TOKEN is missing or has the default dummy value."""

    def __init__(self) -> None:
        """Initialize with a descriptive message."""
        super().__init__("DISCORD_TOKEN is not set.")


class MissingApplicationIdError(ConfigurationError):
    """Raised when DISCORD_APPLICATION_ID is missing or has the default dummy value."""

    def __init__(self) -> None:
        """Initialize with a descriptive message."""
        super().__init__("DISCORD_APPLICATION_ID is not set.")
