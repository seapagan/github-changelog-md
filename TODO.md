# Planned features

Not all of these features/ideas will (or should!) be implemented but this is an
idea of where I want to take the project in the future.

Items marked with:

- ':fire:' Should be implemented as a priority before the next minor release
(patch or bug-fixes are ok as needed).
- ':rocket:` Have been already implemented in the main repo and will be included
in the next release.

## Features to Add

- allow the `extend_sections` option to use a regex on the PR title in addition
  to just matching on the label.
- :fire: Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, Markdown, PDF, LaTeX, etc.).
- Ability to only update changes and leave the rest of the file untouched (ie do
  not re-generate previous releases, only new ones or the unreleased section).
  (allows user customization to the CHANGELOG).
- Ability to specify a custom template layout.
- Allow filtering of commits based on commit message or other criteria.
- Allow customization of the commit message format in the changelog.
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
- Allow to add a text block to the 'Breaking Changes' section. Can be added to
  the config file, or more usefully to a dedicated file linking releases to a
  text block.
- Use the above secondary config file for every release to add a custom text
  block to the release?
- Add an option to add a custom text block to the top of the changelog, eg to
  explain the version numbering scheme or other important information.
- investigate adding caching of the GitHub API calls to speed up the process.
- for the `--contrib` option, allow to use an existing file with comment markers
  in the file to indicate where to add the names. Provide a default file with
  the comment markers in it or just document the process?
- :fire: If there is no local config file, check for a global config file in the
  user's home directory. This would allow a user to set their GitHub PAT once
  and use it for all projects.
- dump markdown code for a specific release to the terminal, so it can be copy /
  pasted into other docs.
- option to hide certain headers, or remove all headers and just have a list of
  PRs.
- :fire: change the order of PRs in the output - current is newest first, but we
  could have oldest first or alphabetical by title or something.
- Add settings to run this as a GitHub action, so it can be run automatically
  when a new release is created or a PR is merged. We should be able to use the
  `secrets.GITHUB_TOKEN` for this?
- option to start at a specific release, ignoring all previous releases.
- :fire: add `extend_ignored_labels` option to add to the default list of
  ignored labels.
- :fire: add `ignored_labels` option to override the default list of ignored
  labels.
- :fire: add `allowed_labels` option to specify which of the default ignored
  labels you want to include in the changelog.
- once the common config file functionality is implemented, add the ability to
  read the config from a `pyproject.toml` file if it exists in the current
  directory. This will allow one less config file. Note that the PAT will still
  need to be set manually in the local or global config file.
- add option to specify the GitHub PAT from the command line, eg `--token
  <PAT>`. This will override any PAT set in the config file. **Note that this
  can be a security risk if the PAT is visible in the command history, so it
  should be used with caution.** `This needs the settings logic to be refactored
  first, the way it is done at the moment it will still ask for the PAT if it is
  not set in the config file, even if it is set on the command line, since this
  is a side-effect of importing the settings library.`

## Improve existing functionality

- :fire: if there are no PR for a specific release then say something to that
  effect instead of just leaving the section empty. We already use the Release
  'body' for this, but if that is missing too we need to say something.
- add link targets to the release headers so they can be linked to directly.
- allow multiple labels to be used for the same section, eg 'enhancement'
  and 'enhancements' both map to the 'Enhancements' section.
- :fire: hide the closed issues section on demand.
- :fire: allow to hide PR's from the output by their number.
- :fire: if the tool is run in a local repo, use that for the `--contrib` functionality
  instead of the GitHub API. This should be an order of magnitude faster. Have
  an opt-out option to use the GitHub API instead.

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

## Other

- break out the `--contrib` option into a separate standalone project that can
  be used to generate a list of contributors for any project directly from a
  local repository. This will be useful for projects that don't use GitHub. Can
  be made into a GitHub action too.
