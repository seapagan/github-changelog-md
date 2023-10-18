# Markdown Changelog Generator <!-- omit in toc -->

**Generate a Markdown changelog from a Github repository.**

    Note: This is pre-release documentation for the next version of this
    project which will be released soon. It is not yet available in the current
    PyPI release, though you can install it from the `main` branch on Github.

    Once unit tests are added, the documentation will be updated and a new
    release will be made.

This project will automatically generate a Markdown-formatted changelog from a
Github repository. It will automatically detect the latest release and generate
a changelog based on the **merged** Pull Requests since that release along with
a section for **unmerged** PRs at the top. It will also include a list of all
Issues closed for each release.

The PRs and issues are grouped by type (bug, enhancement, etc.) and sorted by
latest to oldest in this release.

For an example of the output, see the [Changelog](CHANGELOG.md) for this
project.

**Full documentation is available at:** <https://changelog.seapagan.net>

- [Install Locally for a project](#install-locally-for-a-project)
- [Install Globally](#install-globally)
- [Setup a GitHub PAT](#setup-a-github-pat)
  - [PAT Permissions](#pat-permissions)
- [Create a config file](#create-a-config-file)
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

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay](https://github.com/seapagan)
