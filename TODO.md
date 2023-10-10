# Planned features

For now, just some notes to myself. Not all of these will (or should!) be
implemented but it's good to have a list of ideas.

- Implement the basic functionality!
- Use a TOML file for configuration. Use my `simple-toml-settings` library.
- Get repo information from the current directory, read from the `.git` folder.
  If this is missing (e.g. because the current directory is not a git repo),
  then the user should be able to specify the repo information manually.
- Allow custom sections in the output, set by `label` or a regex
- Allow custom ordering of sections
- Allow custom output formats (e.g. HTML, Markdown, PDF, LaTeX, etc.)
- Ability to only update changes and leave the rest of the file untouched
  (allows user customization to the CHANGELOG)
- Ability to specify a custom CHANGELOG file (e.g. `HISTORY.md` or `CHANGES.md`)
- Ability to specify a custom template file (e.g. `changelog.jinja`)
- Ability to upload the CHANGELOG to a remote server
- Edit a GitHub release text with the generated CHANGELOG for that release
- Allow filtering of commits based on commit message or other criteria
- Allow customization of the commit message format in the changelog
- Allow customization of the date format in the changelog
- Add support for generating changelogs for specific time periods (e.g. last
  week, last month, etc.)
- Add support for generating changelogs for specific contributors, authors or
  teams
