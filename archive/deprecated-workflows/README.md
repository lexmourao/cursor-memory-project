# Deprecated GitHub Actions Workflows

This folder preserves GitHub Actions workflows that were moved out of the active `.github/workflows/` directory during the methodology-focused cleanup.

## Why these workflows were archived

The repository is being refocused as a local-first Cursor Memory / AI-assisted development methodology project, not as a production SaaS deployment.

Workflows in `.github/workflows/` run as active GitHub Actions. The archived workflows created scheduled automation, CI noise, or maintenance obligations that no longer fit the current scope.

## Archived workflows

- `backup.yml` — scheduled backup artifact workflow for `memory-bank`, `logs`, and `status`.
- `health.yml` — scheduled health-check workflow.
- `performance.yml` — scheduled/manual performance benchmark workflow.
- `security.yml` — pull-request security scan workflow using Bandit and TruffleHog.
- `nightly-integration.yml` — scheduled integration workflow that ran pytest, backup/restore validation, and Slack failure alerts.
- `weekly-openai.yml` — scheduled/manual OpenAI smoke workflow that used OPENAI_API_KEY to run a real summarization check.

## Future handling

These workflows are preserved for auditability and future reference. Any workflow restored from this archive should be reviewed, updated, and revalidated before being moved back into `.github/workflows/`.
