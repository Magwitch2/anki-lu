"""Command-line interface."""

import click

from anki_lu.anki.mgr import Handler


@click.command()
@click.version_option()
def main() -> None:
    """Anki for Luxembourgish."""
    anki_handler: Handler = Handler()
    print("From __main__, here is anki deck:")
    print(anki_handler.working_deck)
    exit()


if __name__ == "__main__":
    main(prog_name="anki-lu")  # pragma: no cover
