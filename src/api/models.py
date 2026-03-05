"""Pydantic models for Discord interactions."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class CommandOption(BaseModel):
    """Base model for command options, supporting recursion."""

    name: str
    type: int
    value: str | int | float | bool | None = None
    options: list[CommandOption] | None = None


class HealthOption(BaseModel):
    """Option for the health subcommand."""

    name: Literal["health"]
    type: int


class N8nGroup(BaseModel):
    """Option group for n8n commands."""

    name: Literal["n8n"]
    type: int
    options: Annotated[list[HealthOption], Field(min_length=1)]


class PingCommandData(BaseModel):
    """Data for the /ping command."""

    name: Literal["ping"]
    id: str
    type: int


class DsgCommandData(BaseModel):
    """Data for the /dsg command."""

    name: Literal["dsg"]
    id: str
    type: int
    options: Annotated[list[N8nGroup], Field(min_length=1)]


CommandData = Annotated[
    PingCommandData | DsgCommandData,
    Field(discriminator="name"),
]

# Alias or Specific model if needed by schema
ApplicationCommandData = CommandData


class Interaction(BaseModel):
    """Top-level Discord interaction model."""

    type: int
    data: ApplicationCommandData | None = None
    token: str | None = None
    id: str | None = None
    application_id: str | None = None


# Rebuild models for recursive types if necessary
CommandOption.model_rebuild()
