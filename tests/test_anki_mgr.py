"""Tests exercising anki_mgr, a module that manages Anki artifacts, import, export."""

import pytest

from anki_lu.anki.conf import Configuration


@pytest.fixture()
def mock_config() -> dict[str, str]:
    """Generates a well-formed dict object modeled after anki config."""
    conf_dict: dict[str, str] = {
        "zip_path": "random_path.apkg",
        "deck_suffix": ".anki21",
    }
    return conf_dict


def test_config_anki_pkg_validator(mock_config: dict[str, str]) -> None:
    """Tests Anki pkg validation is working.

    GIVEN an Anki export file path that isn't the expected file format
    WHEN config object is created
    THEN an exception is raised
    """
    mock_config["deck_suffix"] = "no-period"
    config = Configuration.parse_obj(mock_config)
    assert config.deck_suffix[0] == "."
