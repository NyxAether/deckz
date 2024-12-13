from pathlib import Path

from . import app


@app.command()
def print_config(*, workdir: Path = Path()) -> None:
    """Print the resolved configuration.

    Args:
        workdir: Path to move into before running the command

    """
    from rich import print as rich_print

    from ..configuring.settings import DeckSettings
    from ..configuring.variables import get_variables

    config = get_variables(DeckSettings.from_yaml(workdir))
    max_length = max(len(key) for key in config)
    rich_print(
        "\n".join((f"[green]{k:{max_length}}[/] {v}") for k, v in config.items())
    )
