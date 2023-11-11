# Command Line Options

Many (though not all) of the options that can be set in the config file can also
be set on the command line. This allows you to override the config file settings
on a per-run basis.

## `--output` / `-o`

By default the tool will create a `CHANGELOG.md` file in the current folder. You
can specify a different filename using the `--output` or `-o` option.

```terminal
$ github-changelog-md --output HISTORY.md
```

!!! tip ""

    :sparkles: Equivalent to the `output_file` setting in the config file.
---

## `--next-release` / `-n`

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

## `--unreleased` / `--no-unreleased`

Choose whether to include the `Unreleased` section in the changelog. By default
the `Unreleased` section is included (`--unreleased`), but you can use the
`--no-unreleased` option to exclude it

!!! tip ""

    :sparkles: Equivalent to the `unreleased` setting in the config file.
---

## `--depends` / `--no-depends`

Choose whether to include the `Dependency Updates` section in the changelog. By
default this will be shown (`--depends`), but you can use the `--no-depends` to
hide them. Some releases have a lot of dependency updates, so this can be useful
to keep the changelog more readable.

!!! tip ""

    :sparkles: Equivalent to the `depends` setting in the config file.
---

## `--issues` / `--no-issues`

Hide the `Closed Issues` section. By default this section is shown, but you can
use the `--no-issues` option to hide it.

!!! tip ""

    :sparkles: Equivalent to the `show_issues` setting in the config file.
---

## `--contrib` / `--no-contrib`

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

## `--quiet` / `-q`

By default the tool will output some information about what it is doing, and
some stats about the PRs and Issues it has found. You can use the `--quiet` or
`-q` option to suppress this output.

!!! tip ""

    :sparkles: Equivalent to the `quiet` setting in the config file.
---

## `--skip` / `-s`

This option allows you to skip a release. You can specify this option multiple
times to skip multiple releases. This is useful if you have a release that you
do not want to include in the changelog for some reason.

```terminal
$ github-changelog-md --skip 1.2.3 --skip 1.3-beta1
```

The string specified here is the actual release **`tag`** for that release, not
the release **`name`**.

## `--ignore` / `-e`

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

## `--item-order` / `-i`

This option allows you to specify the order of the PRs and Issues in each
section. By default the order is `newest_first`, but you can use the
`--item-order` or `-i` option to change this to `oldest_first`.

!!! tip ""

    :sparkles: Equivalent to the `item_order` setting in the config file.

## `--max-depends` / `-m`

This option allows you to specify the maximum number of dependency updates to
show for each release. By default this is set to `10`, but you can use the
`--max-depends` or `-m` option to change this.

If you use [Dependabot](https://github.com/apps/dependabot){:target="_blank"} to
handle your dependency updates, this setting can be useful to limit the noise in
the changelog.

!!! tip ""

    :sparkles: Equivalent to the `max_depends` setting in the config file.

## `--show-diff` / `--no-show-diff`

Choose whether to show the diff links for each release. By default this will be
shown (`--show-diff`), but you can use the `--no-show-diff` option to hide them.

!!! tip ""

    :sparkles: Equivalent to the `show_diff` setting in the config file.

## `--show-patch` / `--no-show-patch`

Choose whether to show the patch links for each release. By default this will be
shown (`--show-patch`), but you can use the `--no-show-patch` option to hide
them.

!!! tip ""

    :sparkles: Equivalent to the `show_patch` setting in the config file.`
