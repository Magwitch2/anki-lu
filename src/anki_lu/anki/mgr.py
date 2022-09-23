"""This module manages os-specific access and operations to Anki artifacts."""
import os
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from anki_lu.conf import config


class Handler:
    """Creates object to manage access and manipulations on Anki artifacts."""

    def __init__(self) -> None:
        """Includes file & dir changes to manage import/export workflow."""
        self.working_deck: Path = Path("")

        self._anki_export_file: Path = config.anki.zip_path
        self._anki_export_compress_level: int = 0
        self._working_dir: Path = config.data_root / "anki_resources"
        self._working_deck_create_time: float = 0.0
        self._working_zip: Path = self._working_dir / config.anki.zip_path.name
        self._new_zip: Path = self._working_dir / "new_zip"
        self._set_up()

    def _set_up(self) -> None:
        """Prepare Anki export object for modification."""
        try:
            self._working_dir.mkdir()
        except FileExistsError:
            shutil.rmtree(self._working_dir)
            self._working_dir.mkdir()

        shutil.copy(self._anki_export_file, self._working_zip)
        with ZipFile(self._working_zip) as w_zip:
            for file in w_zip.infolist():
                w_zip.extract(file.filename, self._working_dir)
                file_ext: str = "." + file.filename.split(".")[-1]
                if file_ext == config.anki.deck_suffix:
                    self.working_deck = self._working_dir / file.filename
                    self._working_deck_create_time = os.stat(self.working_deck).st_mtime
                    self._anki_export_compress_level = file.compress_type
        self._working_zip.unlink()
        if self.working_deck == Path(""):
            self._clean_up()
            raise FileNotFoundError(f"No {config.anki.deck_suffix} file found in " "{self._working_zip.name} file")

    def _clean_up(self) -> None:
        """Cleans up all dirs and files created by instance"""
        shutil.rmtree(self._working_dir)

    def __del__(self) -> None:
        """Cleans-up temp files, and (if needed) exports updated Anki file."""
        if os.stat(self.working_deck).st_mtime > self._working_deck_create_time:
            archived_stem: str = self._anki_export_file.stem + " (old)"
            os.rename(
                self._anki_export_file,
                self._anki_export_file.with_stem(archived_stem),
            )

            with ZipFile(
                self._anki_export_file,
                mode="w",
                compression=ZIP_DEFLATED,
                compresslevel=self._anki_export_compress_level,
            ) as new_archive:
                for file_path in self._working_dir.iterdir():
                    new_archive.write(file_path, arcname=file_path.name)

        self._clean_up()
