# Markdown Changelog Generator <!-- omit in toc -->

[![PyPI
version](https://badge.fury.io/py/github-changelog-md.svg)](https://badge.fury.io/py/github-changelog-md)
![PyPI - License](https://img.shields.io/pypi/l/github-changelog-md)
[![Ruff](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml)
[![Tests](https://github.com/seapagan/github-changelog-md/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/seapagan/github-changelog-md/graph/badge.svg?token=27D8PGNX0E)](https://codecov.io/gh/seapagan/github-changelog-md)
[![Dependency Review](https://github.com/seapagan/github-changelog-md/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/dependency-review.yml)
[![CodeQL](https://github.com/seapagan/github-changelog-md/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/codeql.yml)
[![Weekly Downloads](https://static.pepy.tech/personalized-badge/github-changelog-md?period=week&units=international_system&left_color=black&right_color=green&left_text=Weekly%20Downloads)](https://pepy.tech/project/github-changelog-md)
[![Total Downloads](https://static.pepy.tech/personalized-badge/github-changelog-md?period=total&units=international_system&left_color=black&right_color=green&left_text=Total%20Downloads)](https://pepy.tech/project/github-changelog-md)

**Generate a Markdown changelog from a Github repository.**

This project will generate a Markdown-formatted changelog from a Github
repository. It will detect all GitHub releases and generate a changelog based on
the **merged** Pull Requests for each release along with a section for
**unreleased** PRs (those since the last release) at the top. It will also
include a list of all Issues closed for each release.

The PRs and issues are grouped by type (bug, enhancement, etc.) and sorted by
latest to oldest in this release.

For an example of the output, see the
[CHANGELOG](https://github.com/seapagan/github-changelog-md/blob/main/CHANGELOG.md)
for this project.

**Full documentation is available at:** <https://changelog.seapagan.net>

- [Install Locally for a project](#install-locally-for-a-project)
- [Install Globally](#install-globally)
- [Setup a GitHub PAT](#setup-a-github-pat)
  - [PAT Permissions](#pat-permissions)
- [Create a config file](#create-a-config-file)
- [Add the config file to your .gitignore](#add-the-config-file-to-your-gitignore)
- [Development setup](#development-setup)
- [License](#license)
- [Credits](#credits)

It is possible to install this package both locally within your projects and
globally so it can be used in every project. You also need to generate a GitHub
Personal Access Token (PAT) to use this tool or use an existing one. This should
be stored in a config file `.github-changelog-md.toml` in the directory you run
the tool from.

## Install Locally for a project

Change to your project directory and install the package using your preferred
package manager or plain `pip`.

I'd recommend using [Poetry](https://python-poetry.org/) for managing your
project dependencies if you don't already have a preference:

```console
$ poetry add github-changelog-md --group dev
```

or

```console
$ pip install github-changelog-md
```

## Install Globally

You could also install the package globally if you want to use it in every
project. See the [Documentation](http://127.0.0.1:8000/installation/#globally)
for more information.

## Setup a GitHub PAT

Since this tool uses the GitHub API, you will need to create a [Personal Access
Token](https://github.com/settings/tokens) (PAT) to use this tool without being
rate limited. You can create a PAT with the `repo` scope to access private
repositories, or just leave all the scopes unchecked to only access public
repositories. Generate a 'classic' token unless you need more fine-grained
control over the permissions.

Choose a descriptive name for your token, such as `github-changelog-md`, an
expiry time (or choose to not have it expire at all) and copy the token to your
clipboard.

### PAT Permissions

At this time the tool does not require any special permissions, but in the
future we plan to offer the ability to create an actual release from the command
line. To do this, the PAT will need either the `public_repo` scope (you only
plan to use this on public repositories) or the `repo` scope (you also plan to
use this on private repositories).

## Create a config file

This tool will look for a config file `.changelog-generator.toml` in the
location it is run from. The config file is a simple [TOML](https://toml.io/en/)
file with the following format:

```toml
[changelog_generator]
schema_version = 1
github_pat = "your_github_pat"
```

The easiest way to create this is run the app, you will be prompted for the
PAT and the config file will be created for you in the current folder then the
app will continue.

```console
$ github-changelog-md
```

This is only the barest **minimum** usable configuration! There are many more
options
available, see the
[Configuration](https://changelog.seapagan.net/usage/options/)
section in the documentation for a full list of the many available options.

## Add the config file to your .gitignore

Make sure you add the config file to your `.gitignore` file so you don't
accidentally commit your PAT to your repository. If this does happen, GitHub
will automatically revoke the PAT and you will need to create a new one anyway,
but there is a small chance someone could use it to access your repositories.

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

If you don't want to use Poetry, you can create a virtual environment yourself
then install the dependencies using pip:

```console
$ pip install -r requirements-dev.txt
```

Note however that Poetry will be installed anyway as a dependency of the
project, so you may as well take the time to learn and use it! :grin:

See the [Contributing](https://changelog.seapagan.net/contributing/) section in
the documentation for more information on how to contribute to this project.

## License

This project is released under the terms of the [MIT license](LICENSE.txt).

## Credits

This generator puts a small unobtrusive comment at the bottom of the changelog
to indicate that it was generated by this tool. This is to acknowledge the work
of the contributors and to help spread the word about this project. Please leave
this comment in place for others :pray:.

If you use this tool and like it, please consider giving it a :star: on Github,
which helps others find it. Thanks!

If you find this tool is useful, please consider
[sponsoring](https://github.com/sponsors/seapagan) the developer . All sponsors
will be listed on the documentation and README. All contributions are greatly
appreciated and will be directly used to support and improve the project.

The original Python boilerplate for this package was created using my
[Pymaker](https://github.com/seapagan/py-maker) tool.
