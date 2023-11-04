# Changelog

## [Unreleased](https://github.com/seapagan/github-changelog-md/tree/HEAD)

**Enhancements**

- Handle missing release body (#106) by @seapagan
- Hide PRs or Issues by their GitHub number (#105) by @seapagan
- Allow sorting PRs and Issues within each section of a release (#104) by @seapagan
- Implement '--no-issues' flag to hide closed issues from the generated changelog (#102) by @seapagan

**Refactoring**

- Don't add all settings to auto-generated config file (#103) by @seapagan

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.5.1...HEAD)

## [0.5.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.5.1) (November 02, 2023)

**Closed Issues**

- Crash with `TypeError` when new config created (#99) by @seapagan

**Bug Fixes**

- Fix Crash with writing/reading `None` values (#100) by @seapagan

**Dependency Updates**

- Bump faker from 19.12.1 to 19.13.0 (#98) by @dependabot[bot]

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.5.0...0.5.1)

## [0.5.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.5.0) (November 01, 2023)

**Enhancements**

- Change the default position of custom sections and allow custom position (#94) by @seapagan
- Allow a custom date format (#92) by @seapagan
- Implement custom sections in a release (#91) by @seapagan
- Skip release(s) through CLI option or in settings (#88) by @seapagan
- Implement getting settings from the config file (#87) by @seapagan
- Implement quiet mode (#86) by @seapagan
- Implement creating a CONTRIBUTORS file (#85) by @seapagan
- Add list of ignored labels (#83) by @seapagan
- Add a 'breaking changes' section (#81) by @seapagan

**Bug Fixes**

- Bug: unreleased section not using date format when `--next-release` specified (#95) by @seapagan
- Bug - missing GitHub PAT causes crash (#93) by @seapagan
- Label matching should be case insensitive (#84) by @seapagan

**Refactoring**

- Split requirements file into prod and dev (#82) by @seapagan

**Documentation**

- Fix bad wording in front page and readme (#79) by @seapagan

**Dependency Updates**

- Bump faker from 19.12.0 to 19.12.1 (#90) by @dependabot[bot]
- Bump pymarkdownlnt from 0.9.13.4 to 0.9.14 (#89) by @dependabot[bot]
- Bump mkdocs-material from 9.4.6 to 9.4.7 (#80) by @dependabot[bot]

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.4.0...0.5.0)

## [0.4.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.4.0) (October 28, 2023)

**Enhancements**

- Don't list any PRs with specific flag in the PR title (#74) by @seapagan
- Allow a custom output file name (#72) by @seapagan

**Refactoring**

- Use Ruff for import sorting (#77) by @seapagan
- Update simple-toml-settings library to latest (#76) by @seapagan

**Documentation**

- Change the docs logo and favicon (#73) by @seapagan
- Tweak the contributing info in docs a little (#71) by @seapagan

**Dependency Updates**

- Bump ruff from 0.1.2 to 0.1.3 (#75) by @dependabot[bot]
- Bump actions/checkout from 3 to 4 (#70) by @dependabot[bot]

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.3.0...0.4.0)

## [0.3.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.3.0) (October 25, 2023)

**Enhancements**

- Hide dependency PRs if requested (#68) by @seapagan
- Add and implement '--unreleased' option (#60) by @seapagan
- Capitalize PR and Issues (#59) by @seapagan

**Refactoring**

- Migrate to 'ruff format' from 'black' (#65) by @seapagan
- Refactor the handling of options (#64) by @seapagan

**Documentation**

- Docs: add more badges to docs (#67) by @seapagan
- Clarify some areas in the docs and update linting options, list tasks (#66) by @seapagan

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.3...0.3.0)

## [0.2.3](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.3) (October 24, 2023)

**Merged Pull Requests**

- Stop splitting the individual PR/Issue lines (#57) by @seapagan
- Trim PR and Issue titles in changelog (#56) by @seapagan

**Refactoring**

- Minor code refactoring (#54) by @seapagan

**Documentation**

- Docs: fix wrong project links in README and index (#52) by @seapagan

**Dependency Updates**

- Bump black from 23.10.0 to 23.10.1 (#55) by @dependabot[bot]
- Bump actions/checkout from 3 to 4 (#53) by @dependabot[bot]

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.2...0.2.3)

## [0.2.2](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.2) (October 22, 2023)

**Bug Fixes**

- Fix another bug with 'next-release' links (#50) by @seapagan

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.1...0.2.2)

## [0.2.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.1) (October 22, 2023)

**Merged Pull Requests**

- Add a credit link to the end of the file (#46) by @seapagan
- Set schema to version 1 (#45) by @seapagan

**Bug Fixes**

- Fix bug in release links when 'next release' is specified (#47) by @seapagan

**Dependency Updates**

- Bump pytest-mock from 3.11.1 to 3.12.0 (#44) by @dependabot[bot]

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.0...0.2.1)

## [0.2.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.0) (October 21, 2023)

**Closed Issues**

- Add a '--next-release' flag which will create a virtual release containing all PRs that have been merged since the last release. (#35) by @seapagan
- Try to take repo name from the current folder if it is a git repo (#34) by @seapagan
- Include closed issues in the changelog, linked to the PR that closed them. (#31) by @seapagan
- Finish Documentation (#30) by @seapagan
- Add testing with Pytest (#29) by @seapagan
- Any PR with a dunder string in the title will have that formatted as Bold instead of printed as is. (#22) by @seapagan

**Enhancements**

- List closed issues (#38) by @seapagan
- Add the '--next-release' option (#37) by @seapagan
- Get repo name from local if possible (#36) by @seapagan
- Prompt for PAT if config file is missing (#33) by @seapagan
- Sort prs into sections based on their labels (#23) by @seapagan
- Tweak release layout (#21) by @seapagan
- Use local config file (#20) by @seapagan

**Testing**

- Add Unit testing with pytest (#42) by @seapagan

**Bug Fixes**

- Fix bug #22 (#24) by @seapagan

**Documentation**

- Create release docs (#32) by @seapagan
- Start working on docs (#17) by @seapagan

**Dependency Updates**

- Bump pymdown-extensions from 10.3 to 10.3.1 (#43) by @dependabot[bot]
- Bump faker from 19.10.0 to 19.11.0 (#41) by @dependabot[bot]
- Bump mypy from 1.6.0 to 1.6.1 (#40) by @dependabot[bot]
- Bump gitpython from 3.1.37 to 3.1.38 (#28) by @dependabot[bot]
- Bump flake8-type-checking from 2.4.2 to 2.5.1 (#27) by @dependabot[bot]
- Bump black from 23.9.1 to 23.10.0 (#26) by @dependabot[bot]
- Bump urllib3 from 2.0.6 to 2.0.7 (#25) by @dependabot[bot]
- Bump mkdocs-git-revision-date-localized-plugin from 1.2.0 to 1.2.1 (#19) by @dependabot[bot]
- Bump simple-toml-settings from 0.2.0 to 0.2.2 (#18) by @dependabot[bot]
- Bump pylint from 2.17.7 to 3.0.1 (#16) by @dependabot[bot]
- Bump faker from 19.9.0 to 19.10.0 (#15) by @dependabot[bot]
- Bump pygithub from 1.59.1 to 2.1.1 (#14) by @dependabot[bot]
- Bump pylint-pydantic from 0.2.4 to 0.3.0 (#13) by @dependabot[bot]
- Bump faker from 19.8.0 to 19.9.0 (#12) by @dependabot[bot]
- Bump mypy from 1.5.1 to 1.6.0 (#11) by @dependabot[bot]
- Bump flake8-type-checking from 2.4.1 to 2.4.2 (#9) by @dependabot[bot]
- Bump mkdocs-material from 9.4.1 to 9.4.4 (#8) by @dependabot[bot]
- Bump urllib3 from 2.0.5 to 2.0.6 (#6) by @dependabot[bot]
- Bump pylint from 2.17.5 to 2.17.7 (#5) by @dependabot[bot]

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
