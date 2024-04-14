from pathlib import Path

from typing_extensions import Annotated

from . import WorkdirOption, app


@app.command()
def upload(workdir: Annotated[Path, WorkdirOption] = Path(".")) -> None:
    """Upload pdfs to Google Drive."""
    from ..paths import Paths
    from ..uploading import Uploader

    paths = Paths.from_defaults(workdir)
    Uploader(paths)
