"""Configuration for anki_mgr."""
from pathlib import Path

from pydantic import BaseModel, validator


class Configuration(BaseModel, allow_mutation=False):
    """Config data for managing local Anki artifacts."""

    zip_path: Path
    deck_suffix: str

    @validator("deck_suffix")
    def file_suffix_must_start_with_period(
        cls, v: str  # noqa: B902,N805 (pydantic)
    ) -> str:
        """Consistent with output of Path.suffix methods."""
        if v[0] != ".":
            v = "." + v
        return v
