# Contributing to GitHub Changelog Generator

Thank you for your interest in contributing to `github-changelog-md`! We welcome
all contributions, big or small.

If you are not sure where to start, please take a look at the [open
issues](https://github.com/seapagan/github-changelog-md/issues). If you have an
idea for a new feature or would like to report a bug, please open a new issue.

We also welcome contributions to the documentation. If you find any errors or
would like to suggest improvements, please open a new issue or submit a pull

## Prerequisites

- Since this is a [Python](https://www.python.org/) project, you will need to have
Python installed on your machine. You can download the latest version of Python
from the [official website](https://www.python.org/downloads/) or using your
Operating system's package manager.

- I'd recommend using [pyenv](https://github.com/pyenv/pyenv) to manage your
Python installations, the
[pyenv-installer](https://github.com/pyenv/pyenv-installer) works for Linux and
Mac OS X. For Windows, you can use the
[pyenv-win](https://github.com/pyenv-win/pyenv-win) port. See
[here](https://github.com/pyenv-win/pyenv-win#installation ) for installation
instructions.

- This project requires **Python 3.9** or higher.

- We also use [Poetry](https://python-poetry.org/) to manage our dependencies. You
should have this installed as well. You can install Poetry by following the
instructions on the [Poetry
website](https://python-poetry.org/docs/#installation).

## Getting Started

Before you start contributing, please make sure you have read and understood our
[Code of
Conduct](https://github.com/seapagan/github-changelog-md/blob/main/CODE_OF_CONDUCT.md)
and
[License](https://github.com/seapagan/github-changelog-md/blob/main/LICENSE.txt).

To get started, follow these steps:

1. Fork the repository and clone it to your local machine.
2. Install the required dependencies (see [next section](#install-dependencies)).
3. Create a new branch for your changes: `git checkout -b my-new-feature`.
4. Make your changes and commit them: `git commit -am 'Add some feature'`.
5. Push your changes to your fork: `git push origin my-new-feature`.
6. Create a new pull request.

## Install Dependencies

Run the following command to install the required dependencies:

```console
$ poetry install
```

You then need to activate the virtual environment:

```console
$ poetry shell
```

From here you can start working on the project. If you are using an IDE such as
VSCode or PyCharm, you can set the use their Python interpreter setting to use
the virtual environment that has just been created.

## Install Git Pre-Commit hooks

Please do this if you are intending to submit a PR. It will check commits
locally before they are pushed up to the Repo.

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

This will ensure that all code meets the required linting standard before being
committed.

## Run pre-commit manually

You can run these checks manually on all staged files using the below command :

```console
poe pre
```

## Testing

We are using [pytest](https://docs.pytest.org/) for testing.

At the moment the test framework is set up but we only have about 50% coverage.
We will be adding more tests as we go along - and most definitely welcome any
contributions to this area!

If you add any new features, please add tests for them. This will help us to
ensure that the code is working as expected and will prevent any regressions.
*Currently we are not enforcing this until we have better coverage of the code.*

There is a task set up to run tests:

```console
$ poe test
```

You can also run the tests manually using the following command:

```console
$ pytest
```

The task is set up so we can automatically add other options in the future.

## Changelog

The changelog is automatically generated, using this project, so please do not
edit it manually.

For maintaniers, there is a POE task that will run this and update the changelog
file.

```console
$ poe changelog
```

You also need to add a GitHub Personal Access Token to the config file. See the
section in the
[Documentation](https://changelog.seapagan.net/installation/#setup-a-github-pat)
for information.

**However, you should NOT include a change to the `CHANGELOG.md` file in your
Pull Requests. This will be handled by the maintainers when a new release is
made.**

## Convenience Tasks

There are a few other convenience tasks that can be run using the `poe` command.
These are defined in the `pyproject.toml` file.

Each of these tasks can have extra options added which will be passed to the
underlying tool.

Run **`mypy`** on the code base inb strict mode:

```console
$ poe mypy
```

Format the code using **`ruff format`**:

```console
$ poe format
```

Lint the code using **`ruff`**:

```console
$ poe ruff
```

Check the **Markdown**:

```console
$ poe markdown
```

Run `ruff`, `mypy` and `format` at the same time:

```console
$ poe lint
```

## Documentation Tasks

These are to help with developing and updating the documentation.

- `poe docs:serve` - Serve the MkDocs locally for testing and development
- `poe docs:serve:all` - Same as above, but opens to all interfaces so you can
  view it on other devices on your network
- `poe docs:build` - Build the MkDocs site into the `dist` folder
- `poe docs:publish` - Publish the docs to your GitHub pages. **Note that only
  those with write-access to this repo can do this**.

## Guidelines

Here are some guidelines to follow when contributing to `github-changelog-md`:

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. The
  pre-commit hooks will check for this. We are using the [Ruff
  Formatter](https://docs.astral.sh/ruff/formatter/).
- Try to have no linting errors or warnings. The pre-commit hooks will check for
  this also. [Ruff](https://docs.astral.sh/ruff/) is installed and set to pretty
  strict settings. Ruff now replaces all the original linters that were
  installed. There is also a Markdown linter.
- [MyPy](https://mypy.readthedocs.io/en/stable/) is installed and we are using
  type hints. Please try to add type hints to your code. If you see any areas of
  the code that are missing type hints, please feel free to open a PR and add
  them 😁!
- Write clear and concise commit messages.
- Write tests for your code.
- Make sure your code passes all existing and new tests before submitting a pull
  request.
- Document your code using
  [docstrings](https://www.python.org/dev/peps/pep-0257/).
- If you add or change any functionality, please update the documentation
  accordingly.
- Use [GitHub issues](https://github.com/seapagan/py-maker/issues) to report
  bugs or suggest new features.

If you are using VSCode, there is a config file in the `.vscode` folder that
will help you to follow these guidelines. You may need to install some
extensions to get the most out of it. I'll add a list of recommended extensions
here soon. The `Python` one is a must though.

## Contact

If you have any questions or need help with contributing, please contact me
**@seapagan** on GitHub. You can also use the [GitHub
Discussions](https://github.com/seapagan/github-changelog-md/discussions) feature.

Happy contributing!