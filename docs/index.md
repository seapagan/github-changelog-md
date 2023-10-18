# Markdown Changelog Generator

!!! danger "Pre-release docs"

    This is **pre-release** documentation for the next version of this project
    which will be released soon. It is not yet available in the current PyPI
    release, though you can install it from the `main` branch on Github. Link
    is above in the header. Also, some features mentioned in these docs may not
    be fully implemented even in the development version.

**Generate a Markdown changelog from your Github repository.**

This project will automatically generate a Markdown-formatted changelog from a
Github repository. It will automatically detect the latest release and generate
a changelog based on the **merged** Pull Requests since that release along with
a section for **unmerged** PRs at the top. It will also include a list of all
issues and PRs closed since the last release.

The PRs and issues are grouped by type (bug, enhancement, etc.) and sorted by
latest to oldest in this release. Any Issues that were closed during this
release are also listed.

For an example of the output, see the [Changelog](changelog.md) for this
project.
