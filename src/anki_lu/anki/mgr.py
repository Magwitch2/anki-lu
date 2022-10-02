"""This module manages os-specific access and operations to Anki artifacts."""
import os
import shutil
from pathlib import Path
from tempfile import mkdtemp
from time import time
from zipfile import ZIP_DEFLATED, ZipFile

from anki_lu.anki.conf import Configuration as AnkiConf

_work_deck_prefix: str = "anki_temp"
_work_deck_loc: Path = Path(__file__).parent
#  original anki export file copied instead of over-written
_orig_pkg_flag: str = "(old)"


class Handler:
    """Creates object to manage access and manipulations on Anki artifacts."""

    def __init__(self, conf: AnkiConf) -> None:
        """Includes file & dir changes to manage import/export workflow."""
        self._conf: AnkiConf = conf
        self._work_dir: Path = Path(
            mkdtemp(prefix=_work_deck_prefix, dir=_work_deck_loc)
        )
        self._anki_export_file: Path = conf.zip_path
        self._work_zip: Path = self._work_dir / conf.zip_path.name
        self._zip_comp_lvl: int = 8  # re-zipping compression (deflate mode)
        self.deck: Path = Path("not found")
        self._deck_cr_time: float = 0
        self._new_zip: Path = self._work_dir / "new_zip"
        self._set_up()

    def _set_up(self) -> None:
        """Prepare Anki export object for modification."""
        shutil.copy(self._anki_export_file, self._work_zip)
        with ZipFile(self._work_zip) as w_zip:
            for file in w_zip.infolist():
                w_zip.extract(file.filename, self._work_dir)
                file_suffix: str = file.filename.split(".")[-1]
                if file_suffix == self._conf.deck_suffix:
                    self.deck = self._work_dir / file.filename
                    self._deck_cr_time = time()
                    self._zip_comp_lvl = file.compress_type
        self._work_zip.unlink()
        if self.deck == Path("not found"):
            self._clean_up()
            raise FileNotFoundError(
                f"No {self._conf.deck_suffix} file found in "
                "{self._work_zip.name} file"
            )

    def _clean_up(self) -> None:
        """Cleans up all dirs and files created by instance."""
        shutil.rmtree(self._work_dir)

    def __del__(self) -> None:
        """Cleans-up temp files, and (if needed) exports updated Anki file."""
        if os.stat(self.deck).st_mtime > self._deck_cr_time:
            archived_stem: str = self._anki_export_file.stem + _orig_pkg_flag
            os.rename(
                self._anki_export_file,
                self._anki_export_file.with_stem(archived_stem),
            )

            with ZipFile(
                self._anki_export_file,
                mode="w",
                compression=ZIP_DEFLATED,
                compresslevel=self._zip_comp_lvl,
            ) as new_archive:
                for file_path in self._work_dir.iterdir():
                    new_archive.write(file_path, arcname=file_path.name)

        self._clean_up()
