from logging import getLogger
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir
from git import Repo
from git.exc import InvalidGitRepositoryError

from deckz import app_name
from deckz.exceptions import DeckzException


_logger = getLogger(__name__)


class Paths:
    def __init__(self, working_dir: str, check_depth: bool = True) -> None:
        self.working_dir = Path(working_dir).resolve()

        if check_depth and not self.working_dir.relative_to(self.git_dir).match("*/*"):
            raise DeckzException(
                f"Not deep enough from root {self.git_dir}. "
                "Please follow the directory hierarchy root > company > deck and "
                "invoke this tool from the deck directory."
            )

        self.build_dir = self.working_dir / "build"
        self.pdf_dir = self.working_dir / "pdf"
        self.shared_dir = self.git_dir / "shared"
        self.shared_img_dir = self.shared_dir / "img"
        self.shared_code_dir = self.shared_dir / "code"
        self.shared_latex_dir = self.shared_dir / "latex"
        self.templates_dir = self.git_dir / "templates"
        self.template_latex = self.templates_dir / "subsection.tex"
        self.template_targets = self.templates_dir / "targets.yml"
        self.jinja2_dir = self.git_dir / "jinja2"
        self.jinja2_main_template = self.jinja2_dir / "main.tex.jinja2"
        self.jinja2_print_template = self.jinja2_dir / "print.tex.jinja2"
        self.user_config_dir = Path(user_config_dir(app_name))
        self.global_config = self.git_dir / "global-config.yml"
        self.user_config = self.user_config_dir / "user-config.yml"
        self.company_config = (
            self.git_dir
            / self.working_dir.relative_to(self.git_dir).parts[0]
            / "company-config.yml"
        )
        self.deck_config = self.working_dir / "deck-config.yml"
        self.session_config = self.working_dir / "session-config.yml"
        self.targets = self.working_dir / "targets.yml"

        self.user_config_dir.mkdir(parents=True, exist_ok=True)

    @property
    def git_dir(self) -> Optional[Path]:
        if not hasattr(self, "_git_dir"):
            try:
                repository = Repo(str(self.working_dir), search_parent_directories=True)
            except InvalidGitRepositoryError as e:
                raise DeckzException(
                    "Could not find the path of the current git working directory. "
                    "Are you in one?"
                ) from e
            self._git_dir = Path(repository.git.rev_parse("--show-toplevel")).resolve()
        return self._git_dir
