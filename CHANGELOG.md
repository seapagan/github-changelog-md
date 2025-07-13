# Changelog

This is an auto-generated log of all the changes that have been made to the
project since the first release.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.9.6](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.6) (July 13, 2025)

**New Features**

- Migrate from `poetry` to `uv` ([#351](https://github.com/seapagan/github-changelog-md/pull/351)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Fix some security issues with dependencies and some compatibility with typer ([#363](https://github.com/seapagan/github-changelog-md/pull/363)) by [seapagan](https://github.com/seapagan)
- Build(deps-dev): bump h11 from 0.14.0 to 0.16.0 ([#358](https://github.com/seapagan/github-changelog-md/pull/358)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Chore(deps): update astral-sh/setup-uv action to v6 ([#357](https://github.com/seapagan/github-changelog-md/pull/357)) by [renovate[bot]](https://github.com/apps/renovate)
- Chore(deps): update astral-sh/setup-uv action to v5 ([#354](https://github.com/seapagan/github-changelog-md/pull/354)) by [renovate[bot]](https://github.com/apps/renovate)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.9.5...0.9.6) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.9.5...0.9.6.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.9.5...0.9.6.patch)

## [0.9.5](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.5) (August 17, 2024)

This release fixes some security issues in the project dependencies, and updates
some of the tooling.

**Merged Pull Requests**

- Relax dependency version constraints ([#335](https://github.com/seapagan/github-changelog-md/pull/335)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Perform some more refactoring ([#311](https://github.com/seapagan/github-changelog-md/pull/311)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps-dev): bump faker from 25.8.0 to 27.0.0 ([#334](https://github.com/seapagan/github-changelog-md/pull/334)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mypy from 1.10.0 to 1.11.1 ([#328](https://github.com/seapagan/github-changelog-md/pull/328)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump setuptools from 68.2.2 to 70.0.0 ([#324](https://github.com/seapagan/github-changelog-md/pull/324)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump zipp from 3.17.0 to 3.19.1 ([#322](https://github.com/seapagan/github-changelog-md/pull/322)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump certifi from 2023.7.22 to 2024.7.4 ([#320](https://github.com/seapagan/github-changelog-md/pull/320)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump poethepoet from 0.26.1 to 0.27.0 ([#319](https://github.com/seapagan/github-changelog-md/pull/319)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump rtoml from 0.10.0 to 0.11.0 ([#315](https://github.com/seapagan/github-changelog-md/pull/315)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.9.4...0.9.5) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.9.4...0.9.5.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.9.4...0.9.5.patch)

## [0.9.4](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.4) (June 18, 2024)

**Closed Issues**

- The `release_text` option does not work if the `--next-release` is specified and corresponds to that release_text version. ([#272](https://github.com/seapagan/github-changelog-md/issues/272)) by [seapagan](https://github.com/seapagan)

**Testing**

- Slightly improve test coverage ([#215](https://github.com/seapagan/github-changelog-md/pull/215)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Don't print the release title if it is the same as the tag ([#309](https://github.com/seapagan/github-changelog-md/pull/309)) by [seapagan](https://github.com/seapagan)
- Fix missing release text when using `--next-release` option ([#273](https://github.com/seapagan/github-changelog-md/pull/273)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Remove pydantic as a dependency ([#308](https://github.com/seapagan/github-changelog-md/pull/308)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Docs: fix bad README link to installation docs ([#307](https://github.com/seapagan/github-changelog-md/pull/307)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps): bump urllib3 from 2.0.7 to 2.2.2 ([#306](https://github.com/seapagan/github-changelog-md/pull/306)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-material from 9.5.26 to 9.5.27 ([#305](https://github.com/seapagan/github-changelog-md/pull/305)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump ruff from 0.4.2 to 0.4.9 ([#304](https://github.com/seapagan/github-changelog-md/pull/304)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump pydantic from 2.7.1 to 2.7.4 ([#303](https://github.com/seapagan/github-changelog-md/pull/303)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pre-commit from 3.7.0 to 3.7.1 ([#302](https://github.com/seapagan/github-changelog-md/pull/302)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pygments from 2.17.2 to 2.18.0 ([#300](https://github.com/seapagan/github-changelog-md/pull/300)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pyfakefs from 5.4.1 to 5.5.0 ([#299](https://github.com/seapagan/github-changelog-md/pull/299)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pymarkdownlnt from 0.9.19 to 0.9.20 ([#298](https://github.com/seapagan/github-changelog-md/pull/298)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-material from 9.5.20 to 9.5.26 ([#297](https://github.com/seapagan/github-changelog-md/pull/297)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump faker from 25.0.0 to 25.8.0 ([#296](https://github.com/seapagan/github-changelog-md/pull/296)) by [dependabot[bot]](https://github.com/apps/dependabot)
- *and 6 more dependency updates*

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.9.3...0.9.4) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.9.3...0.9.4.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.9.3...0.9.4.patch)

## [0.9.3](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.3) (May 02, 2024)

**Dependency Updates**

- Build(deps-dev): bump mypy from 1.9.0 to 1.10.0 ([#278](https://github.com/seapagan/github-changelog-md/pull/278)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pytest-xdist from 3.5.0 to 3.6.1 ([#277](https://github.com/seapagan/github-changelog-md/pull/277)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump pydantic from 2.6.4 to 2.7.1 ([#276](https://github.com/seapagan/github-changelog-md/pull/276)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump poethepoet from 0.25.0 to 0.26.1 ([#275](https://github.com/seapagan/github-changelog-md/pull/275)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pymarkdownlnt from 0.9.18 to 0.9.19 ([#274](https://github.com/seapagan/github-changelog-md/pull/274)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump faker from 24.4.0 to 25.0.0 ([#271](https://github.com/seapagan/github-changelog-md/pull/271)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-material from 9.5.15 to 9.5.20 ([#270](https://github.com/seapagan/github-changelog-md/pull/270)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump ruff from 0.3.4 to 0.4.2 ([#267](https://github.com/seapagan/github-changelog-md/pull/267)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pyfakefs from 5.3.5 to 5.4.1 ([#258](https://github.com/seapagan/github-changelog-md/pull/258)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump idna from 3.4 to 3.7 ([#257](https://github.com/seapagan/github-changelog-md/pull/257)) by [dependabot[bot]](https://github.com/apps/dependabot)
- *and 21 more dependency updates*

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.9.2...0.9.3) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.9.2...0.9.3.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.9.2...0.9.3.patch)

## [0.9.2](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.2) (March 07, 2024)

This release relaxes the version criteria for `simple-toml-settings`, there are no further changes.
[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.9.1...0.9.2) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.9.1...0.9.2.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.9.1...0.9.2.patch)

## [0.9.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.9.1) (February 27, 2024)

**New Features**

- For a closed issue, show the name who closed it not who opened it ([#210](https://github.com/seapagan/github-changelog-md/pull/210)) by [seapagan](https://github.com/seapagan)
- Stop with error if the config file schema is wrong ([#198](https://github.com/seapagan/github-changelog-md/pull/198)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix error causing crash if issue is converted to discussion ([#216](https://github.com/seapagan/github-changelog-md/pull/216)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps-dev): bump pre-commit from 3.6.1 to 3.6.2 ([#214](https://github.com/seapagan/github-changelog-md/pull/214)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump pydantic from 2.6.1 to 2.6.2 ([#213](https://github.com/seapagan/github-changelog-md/pull/213)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump poethepoet from 0.24.4 to 0.25.0 ([#212](https://github.com/seapagan/github-changelog-md/pull/212)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pytest from 7.4.3 to 8.0.2 ([#209](https://github.com/seapagan/github-changelog-md/pull/209)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-material from 9.5.8 to 9.5.11 ([#208](https://github.com/seapagan/github-changelog-md/pull/208)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump cryptography from 42.0.0 to 42.0.4 ([#207](https://github.com/seapagan/github-changelog-md/pull/207)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump faker from 23.1.0 to 23.2.1 ([#204](https://github.com/seapagan/github-changelog-md/pull/204)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump ruff from 0.2.1 to 0.2.2 ([#203](https://github.com/seapagan/github-changelog-md/pull/203)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump pygithub from 2.1.1 to 2.2.0 ([#197](https://github.com/seapagan/github-changelog-md/pull/197)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump faker from 20.1.0 to 23.1.0 ([#196](https://github.com/seapagan/github-changelog-md/pull/196)) by [dependabot[bot]](https://github.com/apps/dependabot)
- *and 8 more dependency updates*

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.8.1...0.9.1) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.8.1...0.9.1.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.8.1...0.9.1.patch)

## [0.8.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.8.1) (February 08, 2024)

This release is to fix security issues in some of the project dependencies.

These are: `cryptography`, `jinja2` and `gitpython`.

Several other dependencies have been updated to their latest versions as well.

**Dependency Updates**

- Build(deps-dev): bump mkdocs-material from 9.5.1 to 9.5.8 ([#186](https://github.com/seapagan/github-changelog-md/pull/186)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump cryptography from 41.0.6 to 42.0.0 ([#185](https://github.com/seapagan/github-changelog-md/pull/185)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-git-revision-date-localized-plugin from 1.2.1 to 1.2.4 ([#184](https://github.com/seapagan/github-changelog-md/pull/184)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump codecov/codecov-action from 3 to 4 ([#182](https://github.com/seapagan/github-changelog-md/pull/182)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-minify-plugin from 0.7.1 to 0.8.0 ([#181](https://github.com/seapagan/github-changelog-md/pull/181)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump actions/dependency-review-action from 3 to 4 ([#177](https://github.com/seapagan/github-changelog-md/pull/177)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump actions/cache from 3 to 4 ([#176](https://github.com/seapagan/github-changelog-md/pull/176)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump jinja2 from 3.1.2 to 3.1.3 ([#174](https://github.com/seapagan/github-changelog-md/pull/174)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump gitpython from 3.1.40 to 3.1.41 ([#173](https://github.com/seapagan/github-changelog-md/pull/173)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pre-commit from 3.5.0 to 3.6.0 ([#166](https://github.com/seapagan/github-changelog-md/pull/166)) by [dependabot[bot]](https://github.com/apps/dependabot)
- *and 17 more dependency updates*

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.8.0...0.8.1) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.8.0...0.8.1.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.8.0...0.8.1.patch)

## [0.8.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.8.0) (November 19, 2023)

**New Features**

- Allow totally replacing the text for a specific release (`release_overrides` option) ([#142](https://github.com/seapagan/github-changelog-md/pull/142)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps-dev): bump pyfakefs from 5.3.0 to 5.3.1 ([#141](https://github.com/seapagan/github-changelog-md/pull/141)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump pydantic from 2.5.0 to 2.5.1 ([#140](https://github.com/seapagan/github-changelog-md/pull/140)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps): bump rich from 13.6.0 to 13.7.0 ([#139](https://github.com/seapagan/github-changelog-md/pull/139)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump faker from 20.0.0 to 20.0.3 ([#138](https://github.com/seapagan/github-changelog-md/pull/138)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.7.2...0.8.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.7.2...0.8.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.7.2...0.8.0.patch)

## [0.7.2](https://github.com/seapagan/github-changelog-md/releases/tag/0.7.2) (November 14, 2023)

**Closed Issues**

- If `ignored_users` is not specified, all users are ignored which results in using the release text instead of the generated changelog ([#135](https://github.com/seapagan/github-changelog-md/issues/135)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix bug where without `ignored_users` specified, all users are ignored ([#136](https://github.com/seapagan/github-changelog-md/pull/136)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps): bump pydantic from 2.4.2 to 2.5.0 ([#134](https://github.com/seapagan/github-changelog-md/pull/134)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.7.1...0.7.2) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.7.1...0.7.2.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.7.1...0.7.2.patch)

## [0.7.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.7.1) (November 13, 2023)

**Bug Fixes**

- Fix spacing issues caused by extra line when deps are truncated ([#133](https://github.com/seapagan/github-changelog-md/pull/133)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Refactor and clarify documentation site ([#127](https://github.com/seapagan/github-changelog-md/pull/127)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps-dev): bump faker from 19.13.0 to 20.0.0 ([#132](https://github.com/seapagan/github-changelog-md/pull/132)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump poethepoet from 0.24.2 to 0.24.3 ([#131](https://github.com/seapagan/github-changelog-md/pull/131)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mypy from 1.6.1 to 1.7.0 ([#130](https://github.com/seapagan/github-changelog-md/pull/130)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pymdown-extensions from 10.3.1 to 10.4 ([#129](https://github.com/seapagan/github-changelog-md/pull/129)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump pytest-xdist from 3.3.1 to 3.4.0 ([#128](https://github.com/seapagan/github-changelog-md/pull/128)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump ruff from 0.1.4 to 0.1.5 ([#126](https://github.com/seapagan/github-changelog-md/pull/126)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.7.0...0.7.1) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.7.0...0.7.1.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.7.0...0.7.1.patch)

## [0.7.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.7.0) (November 08, 2023)

**New Features**

- Add an optional text block between releases ([#124](https://github.com/seapagan/github-changelog-md/pull/124)) by [seapagan](https://github.com/seapagan)
- Implement a `release_text` option to add arbitrary text to any release ([#121](https://github.com/seapagan/github-changelog-md/pull/121)) by [seapagan](https://github.com/seapagan)
- Allow marking a release as 'yanked' (or removed) for some reason ([#120](https://github.com/seapagan/github-changelog-md/pull/120)) by [seapagan](https://github.com/seapagan)
- Add `intro_text` option to display a block of text at the top of the Changelog ([#118](https://github.com/seapagan/github-changelog-md/pull/118)) by [seapagan](https://github.com/seapagan)
- Add diff and patch links for each Release ([#117](https://github.com/seapagan/github-changelog-md/pull/117)) by [seapagan](https://github.com/seapagan)
- Allow to only show `max_depends` number of dependency updates for each release ([#116](https://github.com/seapagan/github-changelog-md/pull/116)) by [seapagan](https://github.com/seapagan)
- Implement the `ignore_users` setting. Users listed in this will not have any PRs or Issues in the Changelog ([#115](https://github.com/seapagan/github-changelog-md/pull/115)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Hide custom text from 'unreleased' if we are also using `--next-release` ([#122](https://github.com/seapagan/github-changelog-md/pull/122)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Add mypy to pre-commit and update tool versions ([#119](https://github.com/seapagan/github-changelog-md/pull/119)) by [seapagan](https://github.com/seapagan)
- Refactor settings class, change default values ([#114](https://github.com/seapagan/github-changelog-md/pull/114)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Refactor the documentation layout, splitting the long documentation section into multiple sections ([#123](https://github.com/seapagan/github-changelog-md/pull/123)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Build(deps-dev): bump poethepoet from 0.22.1 to 0.24.2 ([#113](https://github.com/seapagan/github-changelog-md/pull/113)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump mkdocs-material from 9.4.7 to 9.4.8 ([#112](https://github.com/seapagan/github-changelog-md/pull/112)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Build(deps-dev): bump ruff from 0.1.3 to 0.1.4 ([#111](https://github.com/seapagan/github-changelog-md/pull/111)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.6.0...0.7.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.6.0...0.7.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.6.0...0.7.0.patch)

## [0.6.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.6.0) (November 04, 2023)

**New Features**

- Make the list of ignored labels customizable ([#109](https://github.com/seapagan/github-changelog-md/pull/109)) by [seapagan](https://github.com/seapagan)
- Implement renaming default section headers ([#108](https://github.com/seapagan/github-changelog-md/pull/108)) by [seapagan](https://github.com/seapagan)
- Handle missing release body ([#106](https://github.com/seapagan/github-changelog-md/pull/106)) by [seapagan](https://github.com/seapagan)
- Hide PRs or Issues by their GitHub number ([#105](https://github.com/seapagan/github-changelog-md/pull/105)) by [seapagan](https://github.com/seapagan)
- Allow sorting PRs and Issues within each section of a release ([#104](https://github.com/seapagan/github-changelog-md/pull/104)) by [seapagan](https://github.com/seapagan)
- Implement '--no-issues' flag to hide closed issues from the generated changelog ([#102](https://github.com/seapagan/github-changelog-md/pull/102)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Don't add all settings to auto-generated config file ([#103](https://github.com/seapagan/github-changelog-md/pull/103)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.5.1...0.6.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.5.1...0.6.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.5.1...0.6.0.patch)

## [0.5.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.5.1) (November 02, 2023)

This release is a bug-fix for release 0.5.0, which was yanked due to crashing
when creating a missing config file.

**Closed Issues**

- Crash with `TypeError` when new config created ([#99](https://github.com/seapagan/github-changelog-md/issues/99)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix Crash with writing/reading `None` values ([#100](https://github.com/seapagan/github-changelog-md/pull/100)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump faker from 19.12.1 to 19.13.0 ([#98](https://github.com/seapagan/github-changelog-md/pull/98)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.5.0...0.5.1) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.5.0...0.5.1.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.5.0...0.5.1.patch)

## [0.5.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.5.0) (November 01, 2023) **[`YANKED`]**

**This release has been removed for the following reason and should not be used:**

- Crashes on missing config file, use 0.5.1 or above instead.

**New Features**

- Change the default position of custom sections and allow custom position ([#94](https://github.com/seapagan/github-changelog-md/pull/94)) by [seapagan](https://github.com/seapagan)
- Allow a custom date format ([#92](https://github.com/seapagan/github-changelog-md/pull/92)) by [seapagan](https://github.com/seapagan)
- Implement custom sections in a release ([#91](https://github.com/seapagan/github-changelog-md/pull/91)) by [seapagan](https://github.com/seapagan)
- Skip release(s) through CLI option or in settings ([#88](https://github.com/seapagan/github-changelog-md/pull/88)) by [seapagan](https://github.com/seapagan)
- Implement getting settings from the config file ([#87](https://github.com/seapagan/github-changelog-md/pull/87)) by [seapagan](https://github.com/seapagan)
- Implement quiet mode ([#86](https://github.com/seapagan/github-changelog-md/pull/86)) by [seapagan](https://github.com/seapagan)
- Implement creating a CONTRIBUTORS file ([#85](https://github.com/seapagan/github-changelog-md/pull/85)) by [seapagan](https://github.com/seapagan)
- Add list of ignored labels ([#83](https://github.com/seapagan/github-changelog-md/pull/83)) by [seapagan](https://github.com/seapagan)
- Add a 'breaking changes' section ([#81](https://github.com/seapagan/github-changelog-md/pull/81)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Bug: unreleased section not using date format when `--next-release` specified ([#95](https://github.com/seapagan/github-changelog-md/pull/95)) by [seapagan](https://github.com/seapagan)
- Bug - missing GitHub PAT causes crash ([#93](https://github.com/seapagan/github-changelog-md/pull/93)) by [seapagan](https://github.com/seapagan)
- Label matching should be case insensitive ([#84](https://github.com/seapagan/github-changelog-md/pull/84)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Split requirements file into prod and dev ([#82](https://github.com/seapagan/github-changelog-md/pull/82)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Fix bad wording in front page and readme ([#79](https://github.com/seapagan/github-changelog-md/pull/79)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump faker from 19.12.0 to 19.12.1 ([#90](https://github.com/seapagan/github-changelog-md/pull/90)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump pymarkdownlnt from 0.9.13.4 to 0.9.14 ([#89](https://github.com/seapagan/github-changelog-md/pull/89)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump mkdocs-material from 9.4.6 to 9.4.7 ([#80](https://github.com/seapagan/github-changelog-md/pull/80)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.4.0...0.5.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.4.0...0.5.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.4.0...0.5.0.patch)

## [0.4.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.4.0) (October 28, 2023)

**New Features**

- Don't list any PRs with specific flag in the PR title ([#74](https://github.com/seapagan/github-changelog-md/pull/74)) by [seapagan](https://github.com/seapagan)
- Allow a custom output file name ([#72](https://github.com/seapagan/github-changelog-md/pull/72)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Use Ruff for import sorting ([#77](https://github.com/seapagan/github-changelog-md/pull/77)) by [seapagan](https://github.com/seapagan)
- Update simple-toml-settings library to latest ([#76](https://github.com/seapagan/github-changelog-md/pull/76)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Change the docs logo and favicon ([#73](https://github.com/seapagan/github-changelog-md/pull/73)) by [seapagan](https://github.com/seapagan)
- Tweak the contributing info in docs a little ([#71](https://github.com/seapagan/github-changelog-md/pull/71)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump ruff from 0.1.2 to 0.1.3 ([#75](https://github.com/seapagan/github-changelog-md/pull/75)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump actions/checkout from 3 to 4 ([#70](https://github.com/seapagan/github-changelog-md/pull/70)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.3.0...0.4.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.3.0...0.4.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.3.0...0.4.0.patch)

## [0.3.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.3.0) (October 25, 2023)

**New Features**

- Hide dependency PRs if requested ([#68](https://github.com/seapagan/github-changelog-md/pull/68)) by [seapagan](https://github.com/seapagan)
- Add and implement '--unreleased' option ([#60](https://github.com/seapagan/github-changelog-md/pull/60)) by [seapagan](https://github.com/seapagan)
- Capitalize PR and Issues ([#59](https://github.com/seapagan/github-changelog-md/pull/59)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Migrate to 'ruff format' from 'black' ([#65](https://github.com/seapagan/github-changelog-md/pull/65)) by [seapagan](https://github.com/seapagan)
- Refactor the handling of options ([#64](https://github.com/seapagan/github-changelog-md/pull/64)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Docs: add more badges to docs ([#67](https://github.com/seapagan/github-changelog-md/pull/67)) by [seapagan](https://github.com/seapagan)
- Clarify some areas in the docs and update linting options, list tasks ([#66](https://github.com/seapagan/github-changelog-md/pull/66)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.3...0.3.0) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.2.3...0.3.0.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.2.3...0.3.0.patch)

## [0.2.3](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.3) (October 24, 2023)

**Merged Pull Requests**

- Stop splitting the individual PR/Issue lines ([#57](https://github.com/seapagan/github-changelog-md/pull/57)) by [seapagan](https://github.com/seapagan)
- Trim PR and Issue titles in changelog ([#56](https://github.com/seapagan/github-changelog-md/pull/56)) by [seapagan](https://github.com/seapagan)

**Refactoring**

- Minor code refactoring ([#54](https://github.com/seapagan/github-changelog-md/pull/54)) by [seapagan](https://github.com/seapagan)

**Documentation**

- Docs: fix wrong project links in README and index ([#52](https://github.com/seapagan/github-changelog-md/pull/52)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump black from 23.10.0 to 23.10.1 ([#55](https://github.com/seapagan/github-changelog-md/pull/55)) by [dependabot[bot]](https://github.com/apps/dependabot)
- Bump actions/checkout from 3 to 4 ([#53](https://github.com/seapagan/github-changelog-md/pull/53)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.2...0.2.3) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.2.2...0.2.3.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.2.2...0.2.3.patch)

## [0.2.2](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.2) (October 22, 2023)

**Bug Fixes**

- Fix another bug with 'next-release' links ([#50](https://github.com/seapagan/github-changelog-md/pull/50)) by [seapagan](https://github.com/seapagan)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.1...0.2.2) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.2.1...0.2.2.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.2.1...0.2.2.patch)

## [0.2.1](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.1) (October 22, 2023)

**Merged Pull Requests**

- Add a credit link to the end of the file ([#46](https://github.com/seapagan/github-changelog-md/pull/46)) by [seapagan](https://github.com/seapagan)
- Set schema to version 1 ([#45](https://github.com/seapagan/github-changelog-md/pull/45)) by [seapagan](https://github.com/seapagan)

**Bug Fixes**

- Fix bug in release links when 'next release' is specified ([#47](https://github.com/seapagan/github-changelog-md/pull/47)) by [seapagan](https://github.com/seapagan)

**Dependency Updates**

- Bump pytest-mock from 3.11.1 to 3.12.0 ([#44](https://github.com/seapagan/github-changelog-md/pull/44)) by [dependabot[bot]](https://github.com/apps/dependabot)

[`Full Changelog`](https://github.com/seapagan/github-changelog-md/compare/0.2.0...0.2.1) | [`Diff`](https://github.com/seapagan/github-changelog-md/compare/0.2.0...0.2.1.diff) | [`Patch`](https://github.com/seapagan/github-changelog-md/compare/0.2.0...0.2.1.patch)

## [0.2.0](https://github.com/seapagan/github-changelog-md/releases/tag/0.2.0) (October 21, 2023)

**First Public Release**

This is the first release of this project that was uploaded to
[PyPI](https://pypi.org/) and released as a stable version.

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
