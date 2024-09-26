# Planned features

Not all of these features/ideas will (or should!) be implemented but this is an
idea of where I want to take the project in the future.

Items marked with:

- :fire: Should be implemented as a priority before the next minor release
(patch or bug-fixes are ok as needed).
- :rocket: Has been already implemented in the main repo and will be included
in the next release.

## Features to Add
- If there are no releases, say that at the bottom. Allow the text for this to
  be customized in the config file.
- Add a list of releases that should be ignored.
- Allow ignoring all alpha/beta releases and merge their changes into the next
  full release of the same version (or just the next release).
- Allowing some sort of merging of releases, e.g. all beta releases PR are
  listed with the latest 'un merged' release. or, more simply, a list of
  releases to ignore so that their PR's are added to the next release up's
  notes.
- Allow setting a different last release to compare to for release links, in the
  case that releases are out of order.
- Allow the `extend_sections` option to use a regex on the PR title in addition
  to just matching on the label.
- Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, PDF, etc.) in addition to the default
  Markdown.
- Add ability to create a new draft release on GitHub with the latest
  changelog text as the body.
- For the `--contrib` option, allow to use an existing file with comment markers
  in the file to indicate where to add the names. Provide a default file with
  the comment markers in it or just document the process?
- If there is no local config file, check for a global config file in the
  user's home directory. This would allow a user to set their GitHub PAT once
  and use it for all projects. \[`Probably needs to be done in the settings
  package`\]
- Add settings to run this as a GitHub action, so it can be run automatically
  when a new release is created or a PR is merged. We should be able to use the
  `secrets.GITHUB_TOKEN` for this?
- Option to start at a specific release, ignoring all previous releases.
- Once the common config file functionality is implemented, add the ability to
  read the config from a `pyproject.toml` file if it exists in the current
  directory. This will allow one less config file. Note that the PAT will still
  need to be set manually in the local or global config file to aviod it getting
  added to the repo so this has limited usefulness. Can always get the PAT from
  a local secret file or environment variable.
- Add option to specify the GitHub PAT from the command line, eg `--token
  <PAT>`. This will override any PAT set in the config file. **Note that this
  can be a security risk if the PAT is visible in the command history, so it
  should be used with caution.** \[`This needs the settings logic to be
  refactored first, the way it is done at the moment it will still ask for the
  PAT if it is not set in the config file, even if it is set on the command
  line, since this is a side-effect of importing the settings library.`\]
- Offer to create any missing GitHub labels for the repo. This will prob require
  adding extra permissions to the PAT.
- Allow to use `Git TAGS` instead of `GitHub Releases` to generate the
  changelog. some projects don't use GitHub releases, but do use tags.

## Improve existing functionality

- Allow multiple labels to be used for the same section, eg 'enhancement'
  and 'new_feature' both map to the 'Enhancements' section.
- Perhaps rename the `Enhancements` section to `New Features` or similar? I do
  this in my own projects anyway.
- If the tool is run in a local repo, use that for the `--contrib` functionality
  instead of the GitHub API. This should be an order of magnitude faster. Have
  an opt-out option to use the GitHub API instead.
- Update the format for custom sections to allow each section to have it's own
  insertion index. This will be a breaking change in the config file format so
  require a `schema_version` bump. \[`This will not be needed if the option for
  custom ordering of sections is implemented, it can be folded into that.`\]
- Add option to use Markdown header levels for the section headings instead of
  the default **bold** text. This is more correct for Markdown and will pass
  linters.
- Add an option in the individual `changelog_generator.release_text`
  sections to hide the title for that release.

## Known Issues

- Some version numbers in PRs (especially dependabot) get mis-identified as
  emojis in the output, especially if the version number contains `<3` which
  gives :heart: in certain viewers (**though this does NOT happen in GitHub or
  MkDocs at least**). This is very obvious for 'pip' version numbers. It's not a
  priority to fix this for it's intended usage, but just for completeness.
- When using the Release body, we need to normalize any headings to Bold text
  instead so it does not grate so badly with the auto-generated headings.
- In some cases the `full-changelog` does not get removed from the existing body
  properly depending on how it is formatted.
- For closed issues, if there are no issues after filtering (for example if the
  only issue has the `ignore` label) the heading is still shown.

## Refactoring

- The whole code base needs a bit of refactoring to tidy the code and remove
  some of the duplication. This is a low priority but should be done at some
  point. Priority to the actual 'ChangeLog' class. **Preferably this should wait
  until we have full test coverage.**

## Documentation

- The table styling under mobile looks a bit squashed due to setting the width
  to 100% for better desktop display. Need to add a media query to set the width
  better for mobile, prob using overflow

## Testing

- Complete testing with `pytest` to 100% or as close as possible.
- The whole `test_changelog.py` file needs to be re-written and find a better
  way to deal with missing options.

## Back Burner

*These are ideas that I have had but are not really a priority at the moment,
were partially deprecated by other functionality, or I'm not sure if they are
even a good idea.*

Moving them here to prune the main list down to things that are more likely to
be implemented.

- Ability to only update changes and leave the rest of the file untouched (ie do
  not re-generate previous releases, only new ones or the unreleased section).
  (allows user customization to the CHANGELOG). \[`Since adding the ability to
  include arbitrary text, hide releases and PRs, this is probably not worth the
  effort it would take`\]
- Add support for generating changelogs for specific time periods (e.g. last
  week, last month, etc.) \[`More like something would be in a repo analysis
  tool not a changelog generator`\]
- Add support for generating changelogs for specific contributors, authors or
  teams. \[`As above`\]
- option to just have a flat list of PRs and Issues with no sections. \[`Would
  be ugly and limited usefulness`\]
- Add some form of text block to the oldest release that says something like
  "First release" or "Initial release" or "Initial commit" or something
  (configurable) to indicate that this is the first release and nothing to
  compare to. Optionally hide all PR, Issue and commit links in this release.
  \[`Easily done using the 'release_overrides' option.`\]
- Set up versioned documentation on GitHub pages using 'mike' in conjunction with
  MkDocs. I'd like to have an 'unreleased' branch to show ongoing docs for the
  upcoming versions if possible. See the
  [mkdocs-material versioning](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/){:target="_blank"}
  page on this subject. \[`Honestly, I can't be bothered with this. I don't see
  the point of versioned docs for a tool like this. Just use the latest version
  and docs`]
- Dump markdown code for a specific release to the terminal, so it can be copy /
  pasted into other docs.

## Other

- Break out the `--contrib` option into a separate standalone project that can
  be used to generate a list of contributors for any project directly from a
  local repository. This will be useful for projects that don't use GitHub. Can
  be made into a GitHub action too.
- Offer standalone binaries for Windows, MacOS and Linux. This will allow users
  to install the tool without having to install Python first. This will be
  especially useful for Windows users. This will require using `pyinstaller` or
  similar to create the binaries. Can probably be done with GitHub actions.
