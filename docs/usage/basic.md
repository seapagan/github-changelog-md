# Using the Changelog Generator

This tool is designed to be run from the root of a project, and will generate a
`CHANGELOG.md` file in the current folder using the GitHub Release and PR
history. It can also create a `CONTRIBUTORS.md` file if you want it to.

Note that this tool is designed to be run **after** you have merged your PRs,
and just **before** you create a new release. It will use the GitHub release
tags to determine each release.

!!! tip  "Get the most out of this tool"
    Since it also lists unreleased PRs, you can run it at any time and push the
    `CHANGELOG.md` file up to GitHub, to give users an idea of what is coming
    in the next release.

    The generated CHANGELOG uses the **Pull Request or Issue Title** for each
    item, it is recommended that you use clear and descriptive titles for your
    PRs. This will make the changelog much more useful and readable. It is
    always possible to edit the titles of your PRs after they have been merged,
    so if you have a PR with a vague title, you can edit it to be more
    descriptive before you run the tool.

## Basic Usage

This tool is designed to produce a usable clean `CHANGELOG.md` without any extra
configuration. Simply run the tool in the folder of a git repository and it will
generate a
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

As mentioned in the [Installation](../installation.md) section, you will be
prompted for your GitHub PAT the first time you run the tool, and a config
file will be created in the current folder if it does not already exist.

## Advanced Usage

There are many options available to customize the output of the tool (both on
the command-line and through a configuration file), see the following sections
for full details.
