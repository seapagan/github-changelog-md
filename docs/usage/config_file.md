# Configuration File

As mentioned in the [Installation](../installation.md) section, this tool uses a
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

    As already mentioned, the config file contains your GitHub PAT, so you
    should **NOT** commit this file to your repository. Add it to your
    `.gitignore` file to prevent it being committed.

## Options

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
| `max_depends`           | Max dependency updates per Release | `10`          |
| `show_diff`             | Show diff links for each Release   | `True`        |
| `show_patch`            | Show patch links for each Release  | `True`        |
| `intro_text`            | Introductory paragraph             | `""`          |
| `release_text`          | Add text to a release              | `[]`          |
| `release_text_before`   | Add text before a release          | `[]`          |
| `release_overrides`     | Replace all text for a release     | `[]`          |
| `yanked`                | Mark a release as Yanked           | `[]`          |
| _`schema_version`_      | _Configuration schema version_     | _`1`_         |

!!! tip "Config file schema version"

    The `schema_version` setting is used to determine if the config file needs
    to be updated. If you have an older version of the config file, it may have
    some settings that are renamed or no longer used. If this is the case, the
    tool will mention this and point to the documentation so you can update your
    config file.

    You should never change this setting manually unless you are
    updating the config file to an official newer version.

## Example Configuration File

This is a faked up example of a config file with many of the settings.

```toml hl_lines="1" title="changelog_generator.toml"
[changelog_generator]
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
max_depends = 15
show_patch = false
intro_text = """
This is a log of all the changes that have been made to the project since the
first release. It is automatically generated for each release.
"""
yanked = [
  { release = "1.3.0", reason = "Ooooh, nasty nasty bug - use 1.3.1 instead!!!" }
]

[[changelog_generator.release_text]]
release = "1.4.0"
text = "This is a paragraph for the 1.4.0 release."

[[changelog_generator.release_text]]
release = "unreleased"
text = """
These are the changes that have been made to the main repository since the last
release.
"""

[[changelog_generator.release_overrides]]
release = "1.3.5"
text = """
**Replacement Text**

This is **replacement text** for the release notes of version 1.3.5.

No autogenerated text will be included in the release notes for this version.
"""
```

1. :bulb: This is the only required setting, the others are optional.
2. :bulb: This setting uses the `strftime` format, see
   [Advanced Usage](options.md/#custom-date-format) for more details.
3. :bulb: You can also add `[no changelog]` anywhere in the PR or Issue title,
   and it will be excluded from the changelog. This is case-insensitive, so `[No
   Changelog]` or `[NO CHANGELOG]` will also work.

As mentioned above, the only required setting is the `github_pat` setting. The
other settings can be left out, and the tool will use the default values (or the
values specified on the command line).

[^1]:
    The default setting is to insert your custom sections just before the
    `Dependency Updates` section, but you can change this by setting the
    `extend_sections_index` value. See the
    [Custom Sections](options.md#custom-sections) section for more details.

## Real-world Example

The below is the exact configuration file used to create the changelog for this
project. It is a good example of how you can customize the changelog to suit
your needs.

````toml title="changelog_generator.toml"
[changelog_generator]
github_pat = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
schema_version = '1'
extend_sections = [
  { title = "Testing", label = "testing" },
  { title = "Security", label = "security" },
]
extend_sections_index = 3
date_format = "%B %d, %Y"
rename_sections = [{ old = "Enhancements", new = "New Features" }]
ignored_users = ["pre-commit-ci[bot]"]
intro_text = """
This is an auto-generated log of all the changes that have been made to the
project since the first release.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""
[[changelog_generator.yanked]]
release = "0.5.0"
reason = "Crashes on missing config file, use 0.5.1 or above instead."

[[changelog_generator.release_text]]
release = "0.5.1"
text = """
This release is a bug-fix for release 0.5.0, which was yanked due to crashing
when creating a missing config file.
"""

[[changelog_generator.release_text]]
release = "unreleased"
text = """
These are the changes that have been merged to the repository since the last
release. If you want to try out these changes, you can install the latest
version from the main branch by running:

```console
$ pip install git+https://github.com/seapagan/github-changelog-md
```

or, if using poetry:

```console
$ poetry add git+https://github.com/seapagan/github-changelog-md
```
Everything in this section will be included in the next official release.
"""

[[changelog_generator.release_overrides]]
release = "0.2.0"
text = """
**First Public Release**

This is the first release of this project that was uploaded to
[PyPI](https://pypi.org/) and released as a stable version.
"""
````
