# Planned features

For now, just some notes to myself. Not all of these will (or should!) be
implemented but it's good to have a list of ideas.

- Get repo information from the current directory, read from the `.git` folder.
  If this is missing (e.g. because the current directory is not a git repo),
  then the user should be able to specify the repo information manually.
- Allow custom sections in the output, set by `label` or a regex.
- Allow custom ordering of sections.
- Allow custom output formats (e.g. HTML, Markdown, PDF, LaTeX, etc.).
- Ability to only update changes and leave the rest of the file untouched
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
- include closed issues in the changelog, linked to the PR that closed them.
- add ability to create a new release on GitHub with the latest changelog text
  as the body.
- add some form of text or even block to the oldest release that says something
  like "First release" or "Initial release" or "Initial commit" or something
  (configurable) to indicate that this is the first release and nothing to
  compare to. Optionally hide all PR, Issue and commit links in this release.
- add ability to place a section between releases with custom markdown, eg to
  explain changes in the version numbering scheme or other important
  information.
- if there are no PR for a specific release then say something to that effect
  instead of just leaving the section empty. We already use the Release 'body'
  for this, but if that is missing too we need to say something.
- option to change PR/Issue/Commit links to use the GitHub autolink syntax
  instead of explicitly linking to the GitHub page.
- delete extra line-breaks from end of generated file.
- put the 'dependency'-tagged PR's in a collapsable list at the bottom of the
  release, to avoid cluttering the changelog with a bunch of Dependabot PRs.
  _**[`This would be very useful however it breaks loading the CHANGELOG directly
  into MkDocs as it marks this up as a collapsable boxed section and mangles the
  formatting.`]**_
- offer the ability to collapse other sections (or all sections) too. _**[`See
  Above`]**_
- escape any 'dunder' strings in the PR title, e.g. `__init__` or `__main__` as
  otherwise they will be interpreted as markdown and made BOLD.
