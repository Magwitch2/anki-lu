"""This module manages os-specific access and operations to Anki artifacts."""

from pathlib import Path

from pydantic import BaseModel


class Configuration(BaseModel, allow_mutation=False):
    """Config data for managing local Anki artifacts."""

    deck: Path
