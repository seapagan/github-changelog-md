# Markdown Changelog Generator

**Generate a Markdown changelog from your Github repository.**

[![PyPI
version](https://badge.fury.io/py/github-changelog-md.svg)](https://badge.fury.io/py/pyproject-maker)&nbsp;
![PyPI - License](https://img.shields.io/pypi/l/github-changelog-md)&nbsp;
[![Ruff](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml)

This project will automatically generate a Markdown-formatted changelog from a
Github repository. It will automatically detect the latest release and generate
a changelog based on the **merged** Pull Requests since that release along with
a section for **unmerged** PRs at the top. It will also include a list of all
Issues closed for each release.

The PRs and issues are grouped by type (bug, enhancement, etc.) and sorted by
latest to oldest in this release.

For an example of the output, see the [Changelog](changelog.md) for this
project.
