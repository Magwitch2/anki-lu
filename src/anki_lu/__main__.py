"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Anki for Luxembourgish."""


if __name__ == "__main__":
    main(prog_name="anki-lu")  # pragma: no cover
