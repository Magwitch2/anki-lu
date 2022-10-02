"""Configuration for anki_mgr."""
from pathlib import Path

from pydantic import BaseModel, validator


class Configuration(BaseModel):
    """Config data for managing local Anki artifacts."""

    zip_path: Path
    deck_suffix: str  # without leading '.'

    @validator("deck_suffix")
    def file_suffix_correct_formatting(
        cls, v: str  # noqa: B902,N805 (pydantic)
    ) -> str:
        """Consistent with output of Path.suffix methods."""
        if v.count(".") > 1:
            #  TODO: raise error and handle in UI
            pass
        v = v.replace(".", "")
        return v
