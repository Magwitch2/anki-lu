"""Command-line interface."""
from pathlib import Path

import click

from anki_lu.conf import Configuration
from anki_lu.conf_mgr import get_config_obj

_config_path: Path = Path("config.json")
conf: Configuration


@click.command()
@click.version_option()
def main() -> None:
    """Anki for Luxembourgish."""
    conf = get_config_obj()
    print(conf)
    exit()  # pragma: no cover


if __name__ == "__main__":
    main(prog_name="anki-lu")  # pragma: no cover
