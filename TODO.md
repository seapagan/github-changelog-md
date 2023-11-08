# Planned features

Not all of these features/ideas will (or should!) be implemented but this is an
idea of where I want to take the project in the future.

Items marked with:

- :fire: Should be implemented as a priority before the next minor release
(patch or bug-fixes are ok as needed).
- :rocket: Have been already implemented in the main repo and will be included
in the next release.

## Features to Add

- allow the `extend_sections` option to use a regex on the PR title in addition
  to just matching on the label.
- Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, Markdown, PDF, etc.).
- Ability to only update changes and leave the rest of the file untouched (ie do
  not re-generate previous releases, only new ones or the unreleased section).
  (allows user customization to the CHANGELOG).
- Add support for generating changelogs for specific time periods (e.g. last
  week, last month, etc.)
- Add support for generating changelogs for specific contributors, authors or
  teams.
- add ability to create a new draft release on GitHub with the latest
  changelog text as the body.
- add some form of text or even block to the oldest release that says something
  like "First release" or "Initial release" or "Initial commit" or something
  (configurable) to indicate that this is the first release and nothing to
  compare to. Optionally hide all PR, Issue and commit links in this release.
- :rocket: Add ability to place a text block **between** specific releases with
  custom markdown, eg to explain changes in the version numbering scheme or
  other important information. It is placed **before** the specified release and
  is not available for the 'Unreleased' section.
- :rocket: Add config option to add a custom text block to specfic releases. This
  is inside the release as opposed to the option above which is outside (before
  or after) the release.
- :rocket: Add an option to add a custom text block to the top of the changelog.
- investigate adding caching of the GitHub API calls to speed up the process.
- for the `--contrib` option, allow to use an existing file with comment markers
  in the file to indicate where to add the names. Provide a default file with
  the comment markers in it or just document the process?
- If there is no local config file, check for a global config file in the
  user's home directory. This would allow a user to set their GitHub PAT once
  and use it for all projects. \[`Probably needs to be done in the settings
  package`\]
- dump markdown code for a specific release to the terminal, so it can be copy /
  pasted into other docs.
- option to just have a flat list of PRs and Issues with no sections.
- Add settings to run this as a GitHub action, so it can be run automatically
  when a new release is created or a PR is merged. We should be able to use the
  `secrets.GITHUB_TOKEN` for this?
- option to start at a specific release, ignoring all previous releases.
- once the common config file functionality is implemented, add the ability to
  read the config from a `pyproject.toml` file if it exists in the current
  directory. This will allow one less config file. Note that the PAT will still
  need to be set manually in the local or global config file.
- add option to specify the GitHub PAT from the command line, eg `--token
  <PAT>`. This will override any PAT set in the config file. **Note that this
  can be a security risk if the PAT is visible in the command history, so it
  should be used with caution.** \[`This needs the settings logic to be
  refactored first, the way it is done at the moment it will still ask for the
  PAT if it is not set in the config file, even if it is set on the command
  line, since this is a side-effect of importing the settings library.`\]
- offer to create any missing GitHub labels for the repo. This will prob require
  adding extra permissions to the PAT.
- :rocket: add `patch` and `diff` links to each release. Its pretty easy to do
  this - just add `.patch` or `.diff` to the end of the '3-dot' url we generate
  for each release anyway. Optional.
- :rocket: option to mark a release as 'yanked', with a custom message.
- :rocket: list of usernames that should be ignored when generating the
  changelog. This will be useful for bots, particularly the `pre-commit` bot.
  `Dependabot` is not usually a problem, since it's PRs are usually labelled
  with `dependencies` and can be ignored by label or using the `--no-depends`
  flag.
- allow to use `Git TAGS` instead of `GitHub Releases` to generate the
  changelog. some projects don't use GitHub releases, but do use tags.
- :rocket: add option to limit how many 'depencency' PRs are shown for each
  release. Default to 10.

## Improve existing functionality

- allow multiple labels to be used for the same section, eg 'enhancement'
  and 'enhancements' both map to the 'Enhancements' section.
- if the tool is run in a local repo, use that for the `--contrib` functionality
  instead of the GitHub API. This should be an order of magnitude faster. Have
  an opt-out option to use the GitHub API instead.
- update the format for custom sections to allow each section to have it's own
  insertion index. This will be a breaking change in the config file format so
  require a `schema_version` bump. \[`This will not be needed if the option for
  custom ordering of sections is implemented, it can be folded into that.`\]

## Known Issues

- if using the `--next-release` option, while also having a `release_text` set for
  that virtual release, the `release_text` will not be shown for the virtual
  release.
- some version numbers in PRs (especially dependabot) get mis-identified as
  emojis in the output, especially if the version number contains `<3` which
  gives :heart: in certain viewers (**though this does NOT happen in GitHub or
  MkDocs at least**). This is very obvious for 'pip' version numbers. It's not a
  priority to fix this for it's intended usage, but just for completeness.
- The table styling under mobile looks a bit squashed due to setting the width
  to 100% for better desktop display. Need to add a media query to set the width
  better for mobile, prob using overflow
- when using the Release body, we need to normalize any headings to Bold text
  instead so it does not grate so badly with the auto-generated headings.
- in some cases the `full-changelog` does not get removed from the existing body
  properly depending on how it is formatted.

## Refactoring

- The whole code base needs a bit of refectoring to tidy the code and remove some
of the duplication. This is a low priority but should be done at some point.
Priority to the actual 'ChangeLog' class. **Preferably this should wait until we
have full test coverage.**

## Documentation

- set up versioned documentation on GitHub pages using 'mike' in conjunction with
  MkDocs. I'd like to have an 'unreleased' branch to show ongoing docs for the
  upcoming versions if possible. See the
  [mkdocs-material versioning](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/){:target="_blank"}
  page on this subject.

## Testing

- complete testing with `pytest` to 100% or as close as possible.
- the whole `test_changelog.py` file needs to be re-written and find a better
  way to deal with missing options.

## Other

- break out the `--contrib` option into a separate standalone project that can
  be used to generate a list of contributors for any project directly from a
  local repository. This will be useful for projects that don't use GitHub. Can
  be made into a GitHub action too.
- Offer standalone binaries for Windows, MacOS and Linux. This will allow users
  to install the tool without having to install Python first. This will be
  especially useful for Windows users. This will require using `pyinstaller` or
  similar to create the binaries. Can probably be done with GitHub actions.
