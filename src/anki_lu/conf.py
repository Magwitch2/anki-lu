"""Top-level configuration for anki-lu program."""

from pathlib import Path

from pydantic import BaseModel

from anki import conf as anki_conf


class Configuration(BaseModel, allow_mutation=False):
    """Read-only object containing application-wide configuration.

    Attr:
        data_root (Path): location of data resources
        anki (dict): kwargs for anki module config
    """

    data_root: Path = Path(".")
    anki: anki_conf.Configuration
