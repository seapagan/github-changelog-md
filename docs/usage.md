# Usage

## Basic Usage

Simply run the tool in the folder of a git repository and it will generate a
`CHANGELOG.md` file in the current folder. You can specify the name of the
repository you want to generate the changelog for using the `--repo` or `-r`
option:

```console
$ github-changelog-md --repo <repo-name>
```

!!! note "Automatic repository name detection"

    If you do not specify a repository name, the tool will try to determine the
    repository name from the current folder if it is a git repository. Failing
    that it will exit.

    Just run the command from the root of the repository you want to generate
    the changelog for, with no options:

    ```console
    $ github-changelog-md
    ```

This works for any repository that is linked to your username (determined from
the PAT), however if you want to generate a changelog for a repository that is
**not** linked to your username, you can specify the repository owner using the
`--user` or `-u` option.

```console
$ github-changelog-md --user <repo-owner> --repo <repo-name>
```

As mentioned in the [Installation](installation.md) section, you will be
prompted for your GitHub PAT the first time you run the tool, and a config
file will be created in the current folder if it does not already exist.

## Release Section Headers

There are a few different section headers defined, which are used to group the
PRs in the changelog for each release. These are taken from the GitHub `labels`
applied to the PR. The default section headers are:

| **Title**            | **Label**       | **Notes**             |
|----------------------|-----------------|-----------------------|
| Breaking Changes     |      _breaking_ |                       |
| Merged Pull Requests |                 | Any PR with NO labels |
| Enhancements         |   _enhancement_ |                       |
| Bug Fixes            |           _bug_ |                       |
| Refactoring          |      _refactor_ |                       |
| Documentation        | _documentation_ |                       |
| Dependency Updates   |  _dependencies_ |                       |

You can tag each of your PRs with any of these labels to group them in the
changelog - If you are using `Dependabot`, by default it will add the
`dependencies` label.

Labels are case-insensitive, so `bug` or `BUG` will both
match "Bug Fixes". The above order is also the order that the sections will
appear in the changelog.

!!! tip

    For the moment, limit your PRs to a single label, as the tool will only
    include the PR in the first section it finds a label for. This will be
    improved in future versions, and you will also be able to customize the
    section headers and add your own. I also plan to add the ability to use
    multiple labels for the same section, eg `enhancement` and `enhancements`

## Ignored Labels

There are a few labels that are ignored by default, as they should not be
included in the changelog. These are:

- `duplicate`
- `invalid`
- `question`
- `wontfix`

These are ignored for both PRs and Issues.

!!! tip

    This list of ignored labels will be customizable in future versions.

## Advanced Usage

There are some options you can use to customize the output of the tool.

### `--output` / `-o`

By default the tool will create a `CHANGELOG.md` file in the current folder. You
can specify a different filename using the `--output` or `-o` option.

```console
$ github-changelog-md --output HISTORY.md
```

### `--next-release` / `-n`

This option allows you to specify the name of the next release. By default, any
PRs that are merged after the last existing release will be added to the
`Unreleased` section of the changelog. If you specify a value for this option,
the tool will create a new section with the specified name and add the PRs to
that section instead.

Useful to prep for a release before it is actually released.

```console
$ github-changelog-md --next-release 1.2.3
```

### `--unreleased` / `--no-unreleased`

Choose whether to include the `Unreleased` section in the changelog. By default
the `Unreleased` section is included (`--unreleased`), but you can use the
`--no-unreleased` option to exclude it

### `--depends` / `--no-depends`

Choose whether to include the `Dependency Updates` section in the changelog. By
default this will be shown (`--depends`), but you can use the `--no-depends` to
hide them. Some releases have a lot of dependency updates, so this can be useful
to keep the changelog more readable.

## Hide PR from the Changelog

If there is a PR that you do **NOT** wish to include in the changelog for some
reason, you can add `[no changelog]` anywhere in the PR title, and it will be
excluded from the changelog. This is case-insensitive, so `[No Changelog]` or
`[NO CHANGELOG]` will also work.

## Future plans

See the [Todo List](todo_list.md) for planned features. There are quite a few
more options and customizations to come.
