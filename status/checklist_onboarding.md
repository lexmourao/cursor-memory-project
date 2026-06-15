# Onboarding Checklist

> Starter onboarding checklist for contributors or AI-assisted tools working with projects created from the Cursor Memory Project template.

## Repository Setup

- [ ] Clone the repository
- [ ] Review `README.md`
- [ ] Review `PROJECT_RULES.md`
- [ ] Review `.cursor-rules.md`
- [ ] Review `memory-bank/README.md`
- [ ] Review `docs/ARCHITECTURE.md`
- [ ] Review `docs/CONTEXT_ENGINEERING_GUIDE.md`

## Local Environment

- [ ] Install dependencies from `requirements.txt`
- [ ] Copy `env.template` to `.env` if local environment variables are needed
- [ ] Add `OPENAI_API_KEY` only if automated summarization or embeddings are required
- [ ] Add `GPG_KEY_ID` only if encrypted backups are required
- [ ] Confirm `.env` is ignored by Git
- [ ] Confirm no secrets are committed

## Memory-Bank Usage

- [ ] Understand that `memory-bank/` starts as a template
- [ ] Do not add fake project knowledge to memory-bank files
- [ ] Fill `projectbrief.md` only after real project kickoff
- [ ] Update `productContext.md` only after real user/persona discovery
- [ ] Treat `activeContext.md` as generated or summary-driven context
- [ ] Record design decisions in `systemPatterns.md`
- [ ] Keep `techContext.md` aligned with the real stack
- [ ] Keep `progress.md` aligned with actual milestones and blockers

## Local Workflow

- [ ] Run the MCP server locally if context loading is needed
- [ ] Confirm `/health` endpoint responds
- [ ] Confirm `/memory` endpoint returns memory records
- [ ] Run retrieval rebuild if memory files changed
- [ ] Use `scripts/log_action.py` for errors and solutions
- [ ] Use `scripts/update_status.py` when status files need updating

## Quality Checks

- [ ] Run relevant tests before committing code changes
- [ ] Run `ruff check .` for linting when editing Python
- [ ] Run `mypy app scripts tests` when editing typed Python code
- [ ] Review public CI results after each commit
- [ ] Review CodeQL results after relevant commits

## Security

- [ ] Do not store API keys, passwords, credentials, PII, PHI, or client-confidential data in `memory-bank/`
- [ ] Use `.env`, Docker secrets, or approved secure storage for sensitive local configuration
- [ ] Keep generated retrieval files out of version control
- [ ] Treat Nginx and Docker files as starter local/single-VM examples unless hardened for production

## Handoff

- [ ] Update `diary/project_log.md` after significant milestones
- [ ] Update `status/roadmap.md` when priorities change
- [ ] Update relevant docs when architecture or workflow assumptions change
- [ ] Leave clear notes for the next human or AI-assisted session
