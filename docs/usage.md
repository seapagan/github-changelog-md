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

### `--next-release` \ `-n`

This option allows you to specify the name of the next release. By default, any
PRs that are merged after the last existing release will be added to the
`Unreleased` section of the changelog. If you specify a value for this option,
the tool will create a new section with the specified name and add the PRs to
that section instead.

Useful to prep for a release before it is actually released.

```console
$ github-changelog-md --next-release 1.2.3
```

## Future plans

At this time the tool does not have many options or configuration, but in the
future we plan to add a lot of options to customize the output. See the [Todo
List](todo_list.md) for planned features.