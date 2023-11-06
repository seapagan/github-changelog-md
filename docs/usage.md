# Usage

!!! tip

    Read this section through to the end to learn how to configure and use the
    tool, and to see what configuration options are available.

    There are several ways to customize the output of the tool using command
    line options, the configuration file, and by using labels or naming on your
    PRs.

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

!!! tip "Custom GitHub Labels"

    GitHub provides a few default labels, but you can also create your own
    custom labels and then add them to the `extend_sections` option in the
    config file. See [Custom Sections](#custom-sections) for more details.

    For example, the `breaking` and `refactor` labels are not default GitHub
    labels, but are ones I add to all my projects personally.

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
`Automatic Testing`, and `security` labels will be in `Security`. By default
these are inserted just before the `Dependency Updates` section, but you can
specify the `extend_sections_index` value in the config file to change the index
at which they they are inserted.

!!! warning "Be Aware of the Index!"

    The value of `extend_sections_index` is the **index** of the section, not
    the **position**. The first section has an index of `0`, the second has an
    index of `1`, etc. So if you want your custom sections to appear after the
    `Enhancements` section, you would set the `extend_sections_index` to `3`
    (the index of the next section, `Bug Fixes`)

    **HOWEVER** this index is the index of the **default** sections (listed
    above) that you want to insert BEFORE, even if those sections are not
    displayed. So an index of 0 to 2 could still be before the `Enhancements`
    section, if the `Breaking Changes` or `Merged Pull Requests` sections are
    not displayed. Play with the value to get the desired result :grin:.

    Finally, the `Closed Issues` section is separate and always displayed first
    regardless of the `extend_sections_index` value.

The format for this option is an [array of
tables](https://toml.io/en/v1.0.0#array-of-tables){:target="_blank}, with each
table containing a `title` and a `label`. The above example uses an `inline TOML
array of tables` but the more verbose format will also work:

```toml
[[extend_sections]]
title = "Automatic Testing"
label = "testing"

[[extend_sections]]
title = "Security"
label = "security"
```

Note the **double square brackets!**. Inline arrays as in the first example are
just a bit easier to read and IMHO look nicer.

!!! tip

    For the moment, limit your PRs to a single label, as otherwise the tool will
    include the PR in each section it finds a label for. This will be improved
    in future versions. I also plan to add the ability to use
    multiple labels for the same section, eg `enhancement` and `enhancements`

### Renaming Default Sections

You can also **rename** the default section headers using the `rename_sections`
option in the config file. For example, if you want to rename the `Enhancements`
section to `New Features`, you would add the following to your config file:

```toml
rename_sections = [{ old = "Enhancements", new = "New Features" }]
```

You specify the original title of the section you want to rename as `old`
(**case sensitive!**), and the new title as `new`. You can rename as many
sections as you
want, just add more tables to the array.

The same notes apply to this option as to the `extend_sections` option above,
you can use the inline array format or the verbose format as you prefer.

## Ignored Labels

There are a few labels that are ignored by default and will not be included in
the changelog. These are:

- `duplicate`
- `invalid`
- `question`
- `wontfix`

These are ignored for both PRs and Issues.

### Customizing Ignored Labels

There are three ways to customize the ignored labels, all using settings in the
config file. There are no equivalent command line options for these settings.

#### `ignored_labels`

The `ignored_labels` setting is a definitive list of labels that should be
ignored. This totally replaces the default list. For example, if you only want
to ignore the `wontfix` label, but include every other label, you would add the
following to your config file:

```toml
ignored_labels = ["wontfix"]
```

!!! danger ""

    :sparkles: If this setting is present in your config file, the
    `extend_ignored` and `allowed_labels` settings will be silently ignored.

#### `extend_ignored`

The `extend_ignored` setting is a list of labels to add to the default list. For
example, if you don't want to list documentation changes in the changelog, you
could add the following to your config file:

```toml
extend_ignored = ["documentation"]
```

!!! danger ""

    :sparkles: This setting is ignored if you also have the `ignored_labels`
    setting in your config file.

#### `allowed_labels`

Finally, the `allowed_labels` setting is a list of labels that should be
included, even if they are in the default list. For example, if you want to
include the `question` label in the changelog, you could add the following to
your config file:

```toml
allowed_labels = ["question"]
```

!!! danger ""

    :sparkles: This setting is ignored if you also have the `ignored_labels`
    setting in your config file.

!!! Tip "Tip"

    You CAN combine the `extend_ignored` and `allowed_labels` settings if needed
    , but it is probably easier to just use the `ignored_labels` setting
    instead.

## Ignoring Specific Users

You can also ignore PRs and Issues from specific users, using the
`ignored_users` setting in the config file. For example, if you want to ignore
PRs and Issues from the `pre-commit-ci[bot]` user, you could add the following
to your config file:

```toml
ignored_users = ["pre-commit-ci[bot]"]
```

This is a list of strings and is optional. If you do not specify this setting,
all users will be included. This is NO command line equivalent for this setting.

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

!!! danger "Add to .gitignore"

    As mentioned in the [Installation](installation.md) section, the config file
    contains your GitHub PAT, so you should **NOT** commit this file to your
    repository. Add it to your `.gitignore` file to prevent it being committed.

Current available options are:

| **Setting**             | **Description**                    | **Default**   |
|-------------------------|------------------------------------|---------------|
| **`github_pat`**        | Your GitHub PAT                    |               |
| `output_file`           | Output filename                    |CHANGELOG.md   |
| `unreleased`            | Include unreleased section         | `True`        |
| `depends`               | Include dependency updates section | `True`        |
| `contrib`               | Create CONTRIBUTORS.md file        | `False`       |
| `quiet`                 | Suppress output                    | `False`       |
| `skip_releases`         | List of releases to skip           | `[]`          |
| `show_issues`           | Show closed issues                 | `True`        |
| `extend_sections`       | A list of custom sections          | `[]`          |
| `extend_sections_index` | Index to insert custom sections    | dynamic [^1]  |
| `rename_sections`       | Rename default section headers     | `[]`          |
| `date_format`           | Date format for release dates      | `%Y-%m-%d`    |
| `item_order`            | Order of PR/Issues in each section | `newest_first`|
| `ignore_items`          | List of PRs/Issues to ignore       | `[]`          |
| `ignored_labels`        | List of labels to ignore           | See above     |
| `extend_ignored`        | List of labels to add to ignored   | `[]`          |
| `allowed_labels`        | List of labels to allow            | `[]`          |
| `ignored_users`         | List of usernames to ignore        | `[]`          |
| _`schema_version`_      | _Configuration schema version_     | _`1`_         |

!!! tip "Config file schema version"

    The `schema_version` setting is used to determine if the config file needs
    to be updated. If you have an older version of the config file, it may have
    some settings that are renamed or no longer used. If this is the case, the
    tool will mention this and point to the documentation so you can update your
    config file.

    You should never change this setting manually unless you are
    updating the config file to an official newer version.

### Example Configuration File

```toml hl_lines="1" title="changelog_generator.toml"
github_pat = "1234567890" # (1)!
schema_version = "1"
unreleased = true
quiet = false
depends = true
contrib = false
skip_releases = ["1.2.3", "1.2.4"]
extend_sections = [
  { title = "Testing", label = "testing" },
  { title = "Security", label = "security" },
]
extend_sections_index = 3
rename_sections = [{ old = "Enhancements", new = "New Features" }]
date_format = "%d %B %Y" # (2)!
item_order = "oldest_first"
ignore_items = [123, 456] # (3)!
extend_ignored = ["testing"]
allowed_labels = ["question"]
ignored_users = ["pre-commit-ci[bot]"]
```

1. :bulb: This is the only required setting, the others are optional.
2. :bulb: This setting uses the `strftime` format, see the block below for more
   details.
3. :bulb: You can also add `[no changelog]` anywhere in the PR or Issue title,
   and it will be excluded from the changelog. This is case-insensitive, so `[No
   Changelog]` or `[NO CHANGELOG]` will also work.

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

!!! tip ""

    :sparkles: Equivalent to the `output_file` setting in the config file.
---

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

!!! tip ""

    :sparkles: There is no equivalent setting in the config file.
---

### `--unreleased` / `--no-unreleased`

Choose whether to include the `Unreleased` section in the changelog. By default
the `Unreleased` section is included (`--unreleased`), but you can use the
`--no-unreleased` option to exclude it

!!! tip ""

    :sparkles: Equivalent to the `unreleased` setting in the config file.
---

### `--depends` / `--no-depends`

Choose whether to include the `Dependency Updates` section in the changelog. By
default this will be shown (`--depends`), but you can use the `--no-depends` to
hide them. Some releases have a lot of dependency updates, so this can be useful
to keep the changelog more readable.

!!! tip ""

    :sparkles: Equivalent to the `depends` setting in the config file.
---

### `--issues` / `--no-issues`

Hide the `Closed Issues` section. By default this section is shown, but you can
use the `--no-issues` option to hide it.

!!! tip ""

    :sparkles: Equivalent to the `show_issues` setting in the config file.
---

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

!!! tip ""

    :sparkles: Equivalent to the `contrib` setting in the config file.
---

### `--quiet` / `-q`

By default the tool will output some information about what it is doing, and
some stats about the PRs and Issues it has found. You can use the `--quiet` or
`-q` option to suppress this output.

!!! tip ""

    :sparkles: Equivalent to the `quiet` setting in the config file.
---

### `--skip` / `-s`

This option allows you to skip a release. You can specify this option multiple
times to skip multiple releases. This is useful if you have a release that you
do not want to include in the changelog for some reason.

```terminal
$ github-changelog-md --skip 1.2.3 --skip 1.3-beta1
```

The string specified here is the actual release **`tag`** for that release, not
the release **`name`**.

### `--ignore` / `-e`

Ignore a PR or Issue. You can specify this option multiple times to ignore
multiple PRs or Issues. This is useful if you have a PR or Issue that you do not
want to include in the changelog for some reason.

The integer specified here is the actual PR or Issue **`number`** on GitHub.

```terminal
$ github-changelog-md --ignore 123 --ignore 456
```

!!! tip "Tip"

    You can also add `[no changelog]` anywhere in the PR title, and it will be
    excluded from the changelog. This is case-insensitive, so `[No Changelog]`
    or `[NO CHANGELOG]` will also work.

!!! tip ""

    :sparkles: Equivalent to the `ignore_items` setting in the config file.
---

### `--item-order` / `-i`

This option allows you to specify the order of the PRs and Issues in each
section. By default the order is `newest_first`, but you can use the
`--item-order` or `-i` option to change this to `oldest_first`.

!!! tip ""

    :sparkles: Equivalent to the `item_order` setting in the config file.

## Future plans

See the [Todo List](todo_list.md) for planned features. There are quite a few
more options and customizations to come.

[^1]:
    The default setting is to insert your custom sections just before the
    `Dependency Updates` section, but you can change this by setting the
    `extend_sections_index` value. See the [Custom Sections](#custom-sections)
    section for more details.
