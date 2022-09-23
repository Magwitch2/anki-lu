"""Top-level configuration for anki-lu program."""

from pathlib import Path

from pydantic import BaseModel

from anki_lu.anki import conf

config_file_path: Path = Path("/Users/terry/anki-lu/src/anki_lu/config.json")
data_dir_name: Path = Path("data")


class Configuration(BaseModel, allow_mutation=False):
    """Read-only object containing application-wide configuration.

    Attr:
        data_root (Path): location of data resources
        anki (dict): kwargs for anki module config
    """

    # data_root: Path = Path(__file__).parents[2].joinpath(data_dir_name)
    data_root: Path = Path(".")
    anki: conf.Configuration


config = Configuration.parse_file(config_file_path)
