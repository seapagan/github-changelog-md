# Changelog

## [Unreleased](https://github.com/seapagan/github-changelog-md/tree/HEAD)

**Enhancements**

- Capitalize PR and Issues ([#59](https://github.com/seapagan/github-changelog-md/pull/59)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.3...HEAD)

## [0.2.3](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.3) (2023-10-24)

**Merged Pull Requests**

- Stop splitting the individual PR/Issue lines ([#57](https://github.com/seapagan/github-changelog-md/pull/57)) by [seapagan](https://github.com/seapagan)
- Trim PR and Issue titles in changelog ([#56](https://github.com/seapagan/github-changelog-md/pull/56)) by [seapagan](https://github.com/seapagan)
- Minor code refactoring ([#54](https://github.com/seapagan/github-changelog-md/pull/54)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Docs: fix wrong project links in README and index ([#52](https://github.com/seapagan/github-changelog-md/pull/52)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump black from 23.10.0 to 23.10.1 ([#55](https://github.com/seapagan/github-changelog-md/pull/55)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump actions/checkout from 3 to 4 ([#53](https://github.com/seapagan/github-changelog-md/pull/53)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.2...0.2.3)

## [0.2.2](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.2) (2023-10-22)

**Bug Fixes**

- Fix another bug with 'next-release' links ([#50](https://github.com/seapagan/github-changelog-md/pull/50)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.1...0.2.2)

## [0.2.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.1) (2023-10-22)

**Merged Pull Requests**

- Add a credit link to the end of the file ([#46](https://github.com/seapagan/github-changelog-md/pull/46)) by [seapagan](https://github.com/seapagan)
- Set schema to version 1 ([#45](https://github.com/seapagan/github-changelog-md/pull/45)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix bug in release links when 'next release' is specified ([#47](https://github.com/seapagan/github-changelog-md/pull/47)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump pytest-mock from 3.11.1 to 3.12.0 ([#44](https://github.com/seapagan/github-changelog-md/pull/44)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.0...0.2.1)

## [0.2.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.0) (2023-10-21)

**Closed Issues**

- Add a '--next-release' flag which will create a virtual release containing all PRs that have been merged since the last release. ([#35](https://github.com/seapagan/github-changelog-md/issues/35)) by [seapagan](https://github.com/seapagan)
- Try to take repo name from the current folder if it is a git repo ([#34](https://github.com/seapagan/github-changelog-md/issues/34)) by [seapagan](https://github.com/seapagan)
- Include closed issues in the changelog, linked to the PR that closed them. ([#31](https://github.com/seapagan/github-changelog-md/issues/31)) by [seapagan](https://github.com/seapagan)
- Finish Documentation ([#30](https://github.com/seapagan/github-changelog-md/issues/30)) by [seapagan](https://github.com/seapagan)
- Add testing with Pytest ([#29](https://github.com/seapagan/github-changelog-md/issues/29)) by [seapagan](https://github.com/seapagan)
- Any PR with a dunder string in the title will have that formatted as Bold instead of printed as is. ([#22](https://github.com/seapagan/github-changelog-md/issues/22)) by [seapagan](https://github.com/seapagan)

**Merged Pull Requests**

- Add Unit testing with pytest ([#42](https://github.com/seapagan/github-changelog-md/pull/42)) by [seapagan](https://github.com/seapagan)

**Enhancements**

- List closed issues ([#38](https://github.com/seapagan/github-changelog-md/pull/38)) by [seapagan](https://github.com/seapagan)
- Add the '--next-release' option ([#37](https://github.com/seapagan/github-changelog-md/pull/37)) by [seapagan](https://github.com/seapagan)
- Get repo name from local if possible ([#36](https://github.com/seapagan/github-changelog-md/pull/36)) by [seapagan](https://github.com/seapagan)
- Prompt for PAT if config file is missing ([#33](https://github.com/seapagan/github-changelog-md/pull/33)) by [seapagan](https://github.com/seapagan)
- Sort prs into sections based on their labels ([#23](https://github.com/seapagan/github-changelog-md/pull/23)) by [seapagan](https://github.com/seapagan)
- Tweak release layout ([#21](https://github.com/seapagan/github-changelog-md/pull/21)) by [seapagan](https://github.com/seapagan)
- Use local config file ([#20](https://github.com/seapagan/github-changelog-md/pull/20)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix bug #22 ([#24](https://github.com/seapagan/github-changelog-md/pull/24)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Create release docs ([#32](https://github.com/seapagan/github-changelog-md/pull/32)) by [seapagan](https://github.com/seapagan)
- Start working on docs ([#17](https://github.com/seapagan/github-changelog-md/pull/17)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump pymdown-extensions from 10.3 to 10.3.1 ([#43](https://github.com/seapagan/github-changelog-md/pull/43)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump faker from 19.10.0 to 19.11.0 ([#41](https://github.com/seapagan/github-changelog-md/pull/41)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump mypy from 1.6.0 to 1.6.1 ([#40](https://github.com/seapagan/github-changelog-md/pull/40)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump gitpython from 3.1.37 to 3.1.38 ([#28](https://github.com/seapagan/github-changelog-md/pull/28)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump flake8-type-checking from 2.4.2 to 2.5.1 ([#27](https://github.com/seapagan/github-changelog-md/pull/27)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump black from 23.9.1 to 23.10.0 ([#26](https://github.com/seapagan/github-changelog-md/pull/26)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump urllib3 from 2.0.6 to 2.0.7 ([#25](https://github.com/seapagan/github-changelog-md/pull/25)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump mkdocs-git-revision-date-localized-plugin from 1.2.0 to 1.2.1 ([#19](https://github.com/seapagan/github-changelog-md/pull/19)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump simple-toml-settings from 0.2.0 to 0.2.2 ([#18](https://github.com/seapagan/github-changelog-md/pull/18)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump pylint from 2.17.7 to 3.0.1 ([#16](https://github.com/seapagan/github-changelog-md/pull/16)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump faker from 19.9.0 to 19.10.0 ([#15](https://github.com/seapagan/github-changelog-md/pull/15)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump pygithub from 1.59.1 to 2.1.1 ([#14](https://github.com/seapagan/github-changelog-md/pull/14)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump pylint-pydantic from 0.2.4 to 0.3.0 ([#13](https://github.com/seapagan/github-changelog-md/pull/13)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump faker from 19.8.0 to 19.9.0 ([#12](https://github.com/seapagan/github-changelog-md/pull/12)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump mypy from 1.5.1 to 1.6.0 ([#11](https://github.com/seapagan/github-changelog-md/pull/11)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump flake8-type-checking from 2.4.1 to 2.4.2 ([#9](https://github.com/seapagan/github-changelog-md/pull/9)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump mkdocs-material from 9.4.1 to 9.4.4 ([#8](https://github.com/seapagan/github-changelog-md/pull/8)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump urllib3 from 2.0.5 to 2.0.6 ([#6](https://github.com/seapagan/github-changelog-md/pull/6)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump pylint from 2.17.5 to 2.17.7 ([#5](https://github.com/seapagan/github-changelog-md/pull/5)) by [dependabot[bot]](https://github.com/apps/dependabot)

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
