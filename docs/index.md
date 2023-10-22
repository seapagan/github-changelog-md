# Markdown Changelog Generator

**Generate a Markdown changelog from your Github repository.**

[![PyPI
version](https://badge.fury.io/py/github-changelog-md.svg)](https://badge.fury.io/py/github-changelog-md)&nbsp;
![PyPI - License](https://img.shields.io/pypi/l/github-changelog-md)&nbsp;
[![Ruff](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/linting.yml)&nbsp;
[![Tests](https://github.com/seapagan/github-changelog-md/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/github-changelog-md/actions/workflows/tests.yml)&nbsp;
[![codecov](https://codecov.io/gh/seapagan/github-changelog-md/graph/badge.svg?token=27D8PGNX0E)](https://codecov.io/gh/seapagan/github-changelog-md)

This project will automatically generate a Markdown-formatted changelog from a
Github repository. It will automatically detect the latest release and generate
a changelog based on the **merged** Pull Requests since that release along with
a section for **unmerged** PRs at the top. It will also include a list of all
Issues closed for each release.

The PRs and issues are grouped by type (bug, enhancement, etc.) and sorted by
latest to oldest in this release.

There is an option to tag all the Unreleased PRs with an upcoming release number
to ease the process of creating a new release by having the changelog already up
to date.

While the project is written in Python, it is not limited to generating a
changelog for Python projects. It will work with **any Github repository** and
therefore **any coding language**. In this case a
[global](installation.md#globally)
installation is recommended. Most linux-based systems will already have Python
installed, but if not it is easy to install. Windows and the latest releases of
MacOS will need Python to be installed, see the [Python
documentation](https://www.python.org/downloads/){:target="_blank"} for details.

For an example of the output, see the [Changelog](changelog.md) for this
project.
