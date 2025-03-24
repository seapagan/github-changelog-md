# Installation

It is possible to install this package both locally within your projects and
globally so it can be used in every project. You also need to generate a GitHub
Personal Access Token (PAT) to use this tool or use an existing one. This should
be stored in a config file `.changelog-generator.toml` in the directory you run
the tool from.

## Locally for a project

Change to your project directory and install the package using your preferred
package manager or plain `pip`.

I'd recommend using [uv](https://docs.astral.sh/uv/){:target="_blank"} for
managing your project dependencies if you don't already have a preference:

```console
$ uv add --dev github-changelog-md
```

or (from inside a virtual environment)

```console
$ pip install github-changelog-md
```

## Globally

Install with [pipx](https://pypa.github.io/pipx/) (recommended)

```console
$ pipx install github-changelog-md
```

Or, install the package globally using pip:

```console
$ pip install github-changelog-md
```

If you cannot install globally due to permissions, you can install it to your
user install directory:

```console
$ pip install --user github-changelog-md
```

## Setup a GitHub PAT

Since this tool uses the GitHub API, you will need to create a [Personal Access
Token](https://github.com/settings/tokens){:target="_blank} (PAT) to use this
tool without being rate limited. You can create a PAT with the `repo` scope to
access private repositories, or just leave all the scopes unchecked to only
access public repositories. Generate a 'classic' token unless you need more
fine-grained control over the permissions.

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

!!! danger "Dont commit the config file to your project repository!"

    The config file contains your GitHub PAT, so you should not commit it to
    your repository. It is critical that you add it to your `.gitignore` file
    when you are using this tool in a project.

    If this does end up in a repository, GitHub will automatically revoke the
    PAT and you will need to create a new one anyway, but there is a small
    chance someone could use it to access your repositories.

This tool will look for a config file `.changelog-generator.toml` in the
location it is run from. The config file is a simple
[TOML](https://toml.io/en/){:target="_blank"} file with the following format:

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

!!! info "Note"

    Future versions of this tool may require a newer schema version, so it is
    recommended to always use the latest version. At this time, the schema
    version is not used for anything.

    It is also planned to have a global config file in the user's home folder,
    with the settings from the local config file being merged with the global
    config file. This will allow you to set the PAT once and use it for all
    projects.
