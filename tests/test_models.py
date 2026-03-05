"""Unit tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from src.api.models import DsgCommandData, Interaction
from src.core.constants import InteractionType


def test_parse_ping_interaction() -> None:
    """Test parsing a PING interaction."""
    data = {
        "type": InteractionType.PING,
        "id": "123",
        "token": "abc",
    }
    interaction = Interaction.model_validate(data)
    assert interaction.type == InteractionType.PING
    assert interaction.id == "123"
    assert interaction.data is None


def test_parse_slash_command_ping() -> None:
    """Test parsing a /ping slash command."""
    data = {
        "type": InteractionType.APPLICATION_COMMAND,
        "id": "123",
        "data": {
            "name": "ping",
            "id": "456",
            "type": 1,
        },
    }
    interaction = Interaction.model_validate(data)
    assert interaction.type == InteractionType.APPLICATION_COMMAND
    assert interaction.data is not None
    assert interaction.data.name == "ping"


def test_parse_slash_command_dsg_health() -> None:
    """Test parsing a /dsg n8n health slash command."""
    data = {
        "type": InteractionType.APPLICATION_COMMAND,
        "id": "123",
        "data": {
            "name": "dsg",
            "id": "456",
            "type": 1,
            "options": [
                {
                    "name": "n8n",
                    "type": 2,
                    "options": [
                        {
                            "name": "health",
                            "type": 1,
                        }
                    ],
                }
            ],
        },
    }
    interaction = Interaction.model_validate(data)
    assert interaction.type == InteractionType.APPLICATION_COMMAND
    assert isinstance(interaction.data, DsgCommandData)
    assert interaction.data.name == "dsg"
    assert interaction.data.options[0].name == "n8n"
    assert interaction.data.options[0].options[0].name == "health"


def test_parse_invalid_command_name() -> None:
    """Test that an unknown command name raises ValidationError."""
    data = {
        "type": InteractionType.APPLICATION_COMMAND,
        "id": "123",
        "data": {
            "name": "unknown",
            "id": "456",
            "type": 1,
        },
    }
    with pytest.raises(ValidationError):
        Interaction.model_validate(data)


def test_parse_missing_options() -> None:
    """Test that missing required options raises ValidationError."""
    data = {
        "type": InteractionType.APPLICATION_COMMAND,
        "id": "123",
        "data": {
            "name": "dsg",
            "id": "456",
            "type": 1,
            # options is missing
        },
    }
    with pytest.raises(ValidationError):
        Interaction.model_validate(data)
