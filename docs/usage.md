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
not linked to your username, you can specify the repository owner using the
`--user` or `-u` option.

```console
$ github-changelog-md --user <repo-owner> --repo <repo-name>
```

As mentioned in the [Installation](installation.md) section, you will be
prompted for your GitHub PAT the first time you run the tool, and a config
file will be created in the current folder if it does not already exist.

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
