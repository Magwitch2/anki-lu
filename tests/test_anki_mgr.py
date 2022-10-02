"""Tests exercising anki_mgr, a module that manages Anki artifacts, import, export."""
import os
import shutil
from pathlib import Path
from tempfile import mkdtemp, mkstemp
from zipfile import ZipFile

import pytest

from anki_lu.anki import mgr
from anki_lu.anki.conf import Configuration

_m_deck_sfx: str = ".anki21"
_m_zip_name: str = "test.apkg"


@pytest.fixture()
def mock_artifacts() -> Configuration:  # type: ignore[misc]
    """Creates mock anki export artifact, and supporting conf object.

    Returns: conf object, which includes path to mocked artifacts.
    """
    w_dir: Path = Path(mkdtemp())
    deck: Path = Path(mkstemp(dir=w_dir, suffix=_m_deck_sfx)[-1])  # deck file
    other: Path = Path(mkstemp(dir=w_dir)[-1])  # random other resource
    zip_pkg: Path = w_dir.joinpath(_m_zip_name)
    with ZipFile(zip_pkg, mode="w") as z:
        for f in w_dir.iterdir():
            if f.suffix == Path(_m_zip_name).suffix:
                continue
            z.write(f, arcname=f.name)
    deck.unlink()
    other.unlink()

    conf: Configuration = Configuration.parse_obj(
        {
            "zip_path": zip_pkg,
            "deck_suffix": _m_deck_sfx,
        }
    )

    yield conf
    shutil.rmtree(w_dir)


def test_anki_mgr_clean_up(mock_artifacts: Configuration) -> None:
    """Ensures no temp files remain after clean-up function called."""
    test_handler = mgr.Handler(mock_artifacts)
    count: int = len(list(mgr._work_deck_loc.glob(f"{mgr._work_deck_prefix}*")))
    assert count > 0
    test_handler._clean_up()
    count = len(list(mgr._work_deck_loc.glob(f"{mgr._work_deck_prefix}*")))
    assert count == 0


def test_missing_deck_in_package(mock_artifacts: Configuration) -> None:
    """Raise correct error if file is missing."""
    mock_artifacts.deck_suffix = "wrong"
    with pytest.raises(Exception) as exc:
        test_handler: mgr.Handler = mgr.Handler(mock_artifacts)  # noqa: F841
    assert exc.type == FileNotFoundError


def test_export_of_changed_file(mock_artifacts: Configuration) -> None:
    """Ensure any modified anki files are exported before exit.

    GIVEN a changed Anki deck file,
    WHEN anki handler shuts down,
    THEN
        an updated anki archive is in original directory,
        the original anki archive is renamed and present in same directory,
        the same files, with the same names, are in both archives,
        the <deck> file is the only one that has been modified.
    """
    conf: Configuration = mock_artifacts
    handler: mgr.Handler = mgr.Handler(conf)
    pkg: Path = conf.zip_path
    timestamp: float = os.stat(pkg).st_mtime
    with open(handler.deck, mode="a") as f:
        f.write("Something changed.")
    handler.__del__()
    assert os.stat(pkg).st_mtime > timestamp

    old_pkg_name: str = str(conf.zip_path.stem) + mgr._orig_pkg_flag
    old_pkg: Path = conf.zip_path.with_stem(old_pkg_name)
    assert old_pkg.exists()

    with ZipFile(pkg, mode="r") as new, ZipFile(old_pkg, "r") as old:
        old_names: set[str] = set(old.namelist())
        assert old_names == set(new.namelist())
        for name in old_names:
            if name.split(".")[-1] == conf.deck_suffix:
                continue
            assert old.getinfo(name).date_time == new.getinfo(name).date_time
        print(old_names)


def test_unchanged_files_not_exported(mock_artifacts: Configuration) -> None:
    """Ensure that source anki artifacts unaltered if no changes.

    GIVEN no changes to Anki deck file,
    WHEN anki handler shuts down,
    THEN the source files are untouched.
    """
    timestamp: float = os.stat(mock_artifacts.zip_path).st_mtime
    handler: mgr.Handler = mgr.Handler(mock_artifacts)
    handler.__del__()
    assert os.stat(mock_artifacts.zip_path).st_mtime == timestamp
