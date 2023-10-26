# Planned features

Not all of these features/ideas will (or should!) be implemented but this is an
idea of where I want to take the project in the future.

## Features to Add

- Allow custom sections in the output, set by `label` or a regex.
- Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, Markdown, PDF, LaTeX, etc.).
- Ability to only update changes and leave the rest of the file untouched (ie do
  not re-generate previous releases, only new ones or the unreleased section).
  (allows user customization to the CHANGELOG).
- Ability to specify a custom CHANGELOG file (e.g. `HISTORY.md` or
  `CHANGES.md`).
- Ability to specify a custom template layout.
- Ability to upload the CHANGELOG to a remote server.
- Allow filtering of commits based on commit message or other criteria.
- Allow customization of the commit message format in the changelog.
- Allow customization of the date format in the changelog.
- Add support for generating changelogs for specific time periods (e.g. last
  week, last month, etc.)
- Add support for generating changelogs for specific contributors, authors or
  teams.
- add ability to create a new release on GitHub with the latest changelog text
  as the body.
- add some form of text or even block to the oldest release that says something
  like "First release" or "Initial release" or "Initial commit" or something
  (configurable) to indicate that this is the first release and nothing to
  compare to. Optionally hide all PR, Issue and commit links in this release.
- add ability to place a section between releases with custom markdown, eg to
  explain changes in the version numbering scheme or other important
  information.
- option to change PR/Issue/Commit links to use the GitHub autolink syntax
  instead of explicitly linking to the GitHub page.
- add a flag eg \[no changelog\] to PR titles to allow skipping of PRs that
  don't need to be in the changelog.
- For using the tool in a CI/CD pipeline, allow setting the `GITHUB_PAT`
  environment variable instead of creating a config file.
- Add a 'breaking changes' section to the release, with an optional flag to only
  show this section if there are breaking changes. This will need a specific
  GitHub label to be set on the PRs that are breaking changes. Allow to add a
  text block to this release section. Can be added to the config file, or more
  usefully to a dedicated file linking releases to a text block.
- Use the above secondary config file for every release to add a custom text
  block to the release?
- Add an option to add a custom text block to the top of the changelog, eg to
  explain the version numbering scheme or other important information.
- investigate adding caching of the GitHub API calls to speed up the process.

## Improve existing functionality

- if there are no PR for a specific release then say something to that effect
  instead of just leaving the section empty. We already use the Release 'body'
  for this, but if that is missing too we need to say something.
- check the closed issues logic - we don't want to list issues that were closed
  unless it is linked to a merged PR. Some issues will be closed as wrong or not
  relevant to a release etc, and we don't want to list those.

## Known Issues

- some version numbers in PRs (especially dependabot) get mis-identified as
  emojis in the output, especially if the version number contains `<3` which
  gives <3. This is very obvious for 'pip' version numbers. We need to escape
  this particular pattern in the PR title.

## Documentation

- set up versioned documentation on GitHub pages using 'mike' in conjunction with
  MkDocs. I'd like to have an 'unreleased' branch to show ongoing docs for the
  upcoming versions if possible. See the
  [mkdocs-material versioning](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/){:target="_blank"}
  page on this subject.

## Testing

- complete testing with `pytest` to 100% or as close as possible.
