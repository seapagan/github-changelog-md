"""Entry point for the main application loop."""
from github import Auth, Github

from .config.settings import settings


class App:  # pylint: disable=too-few-public-methods
    """Main application class."""

    def __init__(self) -> None:
        """Initialize the application."""

    def __call__(self) -> None:
        """Call the application."""
        print("Welcome to Github Changelog Md!")
        auth = Auth.Token(settings.github_pat)
        git = Github(auth=auth)

        for repo in git.get_user().get_repos():
            print(repo.name)


app = App()

if __name__ == "__main__":
    app()
