# Planned features

Not all of these features/ideas will (or should!) be implemented but this is an
idea of where I want to take the project in the future.

Items marked with:

- ':fire:' Should be implemented as a priority before the next minor release
(patch or bug-fixes are ok as needed).
- ':rocket:` Have been already implemented in the main repo and will be included
in the next release.

## Features to Add

- :fire: Allow custom sections in the output, set by `label` or a regex.
- Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, Markdown, PDF, LaTeX, etc.).
- Ability to only update changes and leave the rest of the file untouched (ie do
  not re-generate previous releases, only new ones or the unreleased section).
  (allows user customization to the CHANGELOG).
- Ability to specify a custom template layout.
- Ability to upload the CHANGELOG to a remote server.
- Allow filtering of commits based on commit message or other criteria.
- Allow customization of the commit message format in the changelog.
- :fire: Allow customization of the date format in the changelog.
- Add support for generating changelogs for specific time periods (e.g. last
  week, last month, etc.)
- Add support for generating changelogs for specific contributors, authors or
  teams.
- :fire: add ability to create a new release on GitHub with the latest changelog
  text as the body.
- add some form of text or even block to the oldest release that says something
  like "First release" or "Initial release" or "Initial commit" or something
  (configurable) to indicate that this is the first release and nothing to
  compare to. Optionally hide all PR, Issue and commit links in this release.
- add ability to place a section between releases with custom markdown, eg to
  explain changes in the version numbering scheme or other important
  information.
- option to change PR/Issue/Commit links to use the GitHub autolink syntax
  instead of explicitly linking to the GitHub page.
- :rocket: implement a 'Breaking Changes' section that contains any PR with the
  'breaking' label. This should be the first section in the changelog.
- Allow to add a text block to the 'Breaking Changes' section. Can be added to
  the config file, or more usefully to a dedicated file linking releases to a
  text block.
- Use the above secondary config file for every release to add a custom text
  block to the release?
- Add an option to add a custom text block to the top of the changelog, eg to
  explain the version numbering scheme or other important information.
- investigate adding caching of the GitHub API calls to speed up the process.
- :rocket: Option to automatically add each contributor to a 'CONTRIBUTERS.md'
  file or similar. Can use comment markers in the file to indicate where to add
  the names. Provide a default file with the comment markers in it or just
  document the process?
- :fire: If there is no local config file, check for a global config file in the
  user's home directory. This would allow a user to set their GitHub PAT once
  and use it for all projects.
- dump markdown code for a specific release to the terminal, so it can be copy /
  pasted into other docs.
- option to hide certain headers, or remove all headers and just have a list of
  PRs.
- change the order of PRs in the output - current is newest first, but we
  could have oldest first or alphabetical by title or something.
- :rocket: add  a quiet mode so it doesn't print anything unless there are
  errors.
- :rocket: add more config file options to handle some of the existing command line
  options, eg `--unreleased` and `--output`.
- Add settings to run this as a GitHub action, so it can be run automatically
  when a new release is created or a PR is merged. We should be able to use the
  `secrets.GITHUB_TOKEN` for this?
- :rocket: option to skip certain releases, eg if there is a release that has been
  yanked, we can skip it and not include it in the output. This can be specified
  in the config file as a list of release tags, or on the command line,
  specified as many times as needed.
- option to start at a specific release, ignoring all previous releases.
- :rocket: add a default list of ignored labels, eg 'duplicate', 'invalid',
  'question', 'wontfix', etc.

## Improve existing functionality

- if there are no PR for a specific release then say something to that effect
  instead of just leaving the section empty. We already use the Release 'body'
  for this, but if that is missing too we need to say something.
- add link targets to the release headers so they can be linked to directly.
- :rocket: make labels case-insensitive, so 'enhancement' and 'Enhancement' are
  the same.
- allow multiple labels to be used for the same section, eg 'enhancement'
  and 'enhancements' both map to the 'Enhancements' section.

## Known Issues

- some version numbers in PRs (especially dependabot) get mis-identified as
  emojis in the output, especially if the version number contains `<3` which
  gives <3. This is very obvious for 'pip' version numbers. We need to escape
  this particular pattern in the PR title.
- The table styling under mobile looks a bit squashed due to setting the width
  to 100% for better desktop display. Need to add a media query to set the width
  better for mobile.

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
