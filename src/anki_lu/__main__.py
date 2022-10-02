"""Command-line interface."""

import click

from anki_lu.anki.mgr import Handler
from anki_lu.conf import Configuration
from anki_lu.conf_mgr import get_config_obj


@click.command()
@click.version_option()
def main() -> None:
    """Anki for Luxembourgish."""
    # TODO refactor conf_mgr to simplify, also avoid assignment flag
    conf: Configuration = get_config_obj()  # type: ignore[assignment]
    deck: Handler = Handler(conf.anki)
    print(deck)


if __name__ == "__main__":
    main(prog_name="anki-lu")  # pragma: no cover
