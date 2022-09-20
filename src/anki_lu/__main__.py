"""Command-line interface."""
from pathlib import Path

import click
from pydantic import BaseModel

from anki_lu import anki_mgr


class Configuration(BaseModel, allow_mutation=False):
    """Read-only object containing application-wide configuration.

    This object is composed of module-specific config (defined locally per module)
    """

    anki: anki_mgr.Configuration


@click.command()
@click.version_option()
def main() -> None:
    """Anki for Luxembourgish."""
    print("I'm running!")
    config = Configuration.parse_file(Path("config.json"))
    print(config.anki.deck)
    exit()


if __name__ == "__main__":
    main(prog_name="anki-lu")  # pragma: no cover
