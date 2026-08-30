# Continuous Integration

GitHub Actions checks pushes and pull requests for code quality, typing,
tests, documentation, dependencies, and workflow security. The test workflow
runs the supported Python versions and uploads coverage when the Codacy token
is configured. The `ty` workflow is a separate beta check and retains its
documented temporary-disable switch.

## Run checks locally

Use the corresponding Poe tasks while developing:

```console
$ poe lint
$ poe test
$ poe docs:build
$ poe pre
```

`poe lint` runs Ruff formatting, Ruff linting, both `ty` and `mypy`, Markdown
linting, and Zizmor. The individual tasks, including `poe format`, `poe ruff`,
`poe type`, `poe ty`, `poe mypy`, `poe markdown`, and `poe zizmor`, remain
available for focused checks. `poe docs:build` writes the MkDocs site to
`site`. The Prek configuration also runs Zizmor when checking workflow and
action files.

CodeQL analysis and dependency review are primarily hosted checks because they
depend on GitHub's analysis and pull-request context.

## Audit GitHub Actions with Zizmor

[Zizmor](https://docs.zizmor.sh/){:target="_blank"} audits GitHub Actions
workflows and action definitions. Run the repository's pedantic audit with:

```console
$ poe zizmor
```

Zizmor is pinned as a development dependency, a Prek hook, and in the dedicated
hosted workflow. Keep all three versions synchronized when updating it. The Poe
task and hosted workflow restrict collection to `workflows,actions` because the
repository's native `prek.toml` is Prek-specific and uses the `builtin`
repository. The Prek hook receives only matching workflow and action files
directly, so it does not parse the Prek configuration.

Local audits run offline unless a suitable GitHub token is already available
through `ZIZMOR_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN`. A read-only token
is sufficient. Keep credentials out of repository files. Set
`ZIZMOR_OFFLINE=1` to force offline operation, or
`ZIZMOR_NO_ONLINE_AUDITS=1` to allow remote input fetching without online
audits.

The hosted workflow enables online audits and annotations. SARIF upload is
disabled, so it needs only `contents: read`; it does not receive security-event
or write permissions.
