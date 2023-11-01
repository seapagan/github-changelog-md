# Usage

!!! tip

    Read this section through to the end to learn how to configure and use the
    tool, and to see what configuration options are available.

    There are several ways to customize the output of the tool using command
    line options, the configuration file, and by using labels or naming on your
    PRs.

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

Labels are **case-insensitive**, so `bug` or `BUG` will both match "Bug Fixes".
The above order is also the order that the sections will appear in the
changelog, again this order will be customizable in future versions.

### Custom Sections

You can also **add** your own custom section headers, by adding a `label` to
your PRs that matches the `label` you specify in the config file. For example,
if you add the following to your config file:

```toml
extend_sections = [
  { title = "Automatic Testing", label = "testing" },
  { title = "Security", label = "security" },
]
```

Now, any PRs that have the `testing` label will be added to a section called
`Automatic Testing`, and `security` will be in `Security`. At the moment these
are added at the end of the release section, future versions will allow you to
specify the order of the sections. There is no limit to the number of custom
sections you can add.

The format for this option is an [array of
tables](https://toml.io/en/v1.0.0#array-of-tables){:target="_blank}, with each
table containing a `title` and a `label`. The above example uses an `inline TOML
array of tables` but the normal fomat will also work:

```toml
[[extend_sections]]
title = "Automatic Testing"
label = "testing"

[[extend_sections]]
title = "Security"
label = "security"
```

Inline arrays as in the first example are just a bit easier to read.

!!! tip

    For the moment, limit your PRs to a single label, as otherwise the tool will
    include the PR in each section it finds a label for. This will be improved
    in future versions. I also plan to add the ability to use
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

    This list of ignored labels will be customizable in future versions using a
    combination of `extend_ignored_labels` and `ignored_labels`. There will
    probably also be an `allowed_labels` option, so you can specify which of the
    default ignored labels you want to include in the changelog.

## Configuration File

As mentioned in the [Installation](installation.md) section, this tool uses a
configuration file to store your GitHub PAT and other settings. This file is
created in the current folder the first time you run the tool, and is named
`.changelog-generator.toml`. The only required setting is the **`github_pat`**
setting. The other settings are optional, and can be set on the command line
(see the next section) instead of in the config file. Any settings in the
config file will be overridden by the command line options.

The config file is in [TOML](https://toml.io/en/){:target="_blank"} format, and
can be edited manually. All settings are under the `[changelog_generator]`
section, and any other sections will be ignored.

Current available options are:

| **Setting**       | **Description**                    | **Default** |
|-------------------|------------------------------------|-------------|
| **`github_pat`**  | Your GitHub PAT                    |             |
| `output_file`     | Output filename                    |CHANGELOG.md |
| `unreleased`      | Include unreleased section         | `True`      |
| `depends`         | Include dependency updates section | `True`      |
| `contrib`         | Create CONTRIBUTORS.md file        | `False`     |
| `quiet`           | Suppress output                    | `False`     |
| `skip_releases`   | List of releases to skip           | `[]`        |
| `extend_sections` | Add custom sections                | `[]`        |
| `date_format`     | Date format for release dates      | `%Y-%m-%d`  |
| _`schema_version`_| _Configuration schema version_     | _`1`_       |

!!! tip "Config file schema version"

    The `schema_version` setting is used to determine if the config file needs
    to be updated. If you have an older version of the config file, it may have
    some settings that are renamed or no longer used. If this is the case, the
    tool will mention this and point to the documentation so you can update your
    config file.

    You should never change this setting manually unless you are
    updating the config file to an official newer version.

### Example Configuration File

```toml
[changelog_generator]
github_pat = "123456"
schema_version = "1"
unreleased = true
quiet = false
depends = true
contrib = false
skip_releases = ["1.2.3", "1.2.4"]
extend_sections = [
  { title = "Automatic Testing", label = "testing" },
]
date_format = "%d %B %Y"
```

As mentioned above, the only required setting is the `github_pat` setting. The
other settings can be left out, and the tool will use the default values (or the
values specified on the command line).

!!! info "Custom Date Format"

    The `date_format` setting allows you to specify a custom date format for the
    release dates. The default is "`%Y-%m-%d`" (`Year-month-day`) which will
    give you dates like `2023-10-01`. You can use any of the normal Python
    [strftime](https://strftime.org/){:target="_blank"} options to customize the
    date format. This is a full timestamp, so you can include the time as well
    if you want (though that is probably a bit overkill for a changelog).

    I quite like "`%B %d, %Y`" (`month day, year`) which will give you dates like
    `November 01, 2023`.

    There is no CLI option for this setting, so you will need to edit the config
    file manually if you want to change it.

## Command Line Options

There are some options you can use to customize the output of the tool.

### `--output` / `-o`

By default the tool will create a `CHANGELOG.md` file in the current folder. You
can specify a different filename using the `--output` or `-o` option.

```terminal
$ github-changelog-md --output HISTORY.md
```

### `--next-release` / `-n`

This option allows you to specify the name of the next release. By default, any
PRs that are merged after the last existing release will be added to the
`Unreleased` section of the changelog. If you specify a value for this option,
the tool will create a new section with the specified name and add the PRs to
that section instead.

Useful to prep for a release before it is actually released.

```terminal
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

### `--contrib` / `--no-contrib`

Choose whether to create the `CONTRIBUTORS.md` file. By default this will be
`False` (`--no-contrib`), but you can use the `--contrib` option to enable it.

!!! warning "Possibly LONG operation"

    This can take a while to run, as it has to query the GitHub API for each
    contributor. If you have a lot of contributors or many PR's, it can take a
    few minutes to complete.

    In this case it is recommended to only run this option when you are ready to
    release a new version, and not every time you run the tool.

    In future versions I will add the ability to cache the contributors list,
    which should speed things up a lot

### `--quiet` / `-q`

By default the tool will output some information about what it is doing, and
some stats about the PRs and Issues it has found. You can use the `--quiet` or
`-q` option to suppress this output.

### `--skip` / `-s`

This option allows you to skip a release. You can specify this option multiple
times to skip multiple releases. This is useful if you have a release that you
do not want to include in the changelog for some reason.

```terminal
$ github-changelog-md --skip 1.2.3 --skip 1.3-beta1
```

The string specified here is the actual release **`tag`** for that release, not
the release **`name`**.

## Hide PR from the Changelog

If there is a PR that you do **NOT** wish to include in the changelog for some
reason, you can add `[no changelog]` anywhere in the PR title, and it will be
excluded from the changelog. This is case-insensitive, so `[No Changelog]` or
`[NO CHANGELOG]` will also work.

## Future plans

See the [Todo List](todo_list.md) for planned features. There are quite a few
more options and customizations to come.
