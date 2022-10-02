"""Top-level configuration for anki-lu program."""

from pydantic import BaseModel

from anki_lu.anki import conf as anki_conf


class Configuration(BaseModel, allow_mutation=False):
    """Read-only object containing application-wide configuration.

    Attr:
        data_root (Path): location of data resources
        anki (dict): kwargs for anki module config
    """

    anki: anki_conf.Configuration
