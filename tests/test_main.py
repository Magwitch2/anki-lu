"""Module covering main.py (main control path)."""
# from click.testing import CliRunner
from pathlib import Path

import pytest

from anki_lu.__main__ import Configuration


def test_basic() -> None:
    """Confirm tests are running."""
    assert 3 == 3


# def test_correct_config_creation -- tests not needed due to pydantic validation


def test_missing_config_file() -> None:
    """Ensure that a missing file raises an exception.

    GIVEN a non-existent path name
    WHEN config object is tried to be created
    THEN an exception is raised
    """
    with pytest.raises(FileNotFoundError):
        test_config: Configuration = Configuration.parse_file(Path("ardakl;n"))  # noqa


# @pytest.fixture
# def runner() -> CliRunner:
#     """Fixture for invoking command-line interfaces."""
#     return CliRunner()

# def test_main_succeeds(runner: CliRunner) -> None:
#     """It exits with a status code of zero."""
#     result = runner.invoke('poetry anki-lu')
#     assert result.exit_code == 0
