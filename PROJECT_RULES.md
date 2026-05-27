# Project Rules

These rules define how contributors and AI-assisted coding tools should work inside this repository.

## 1. No-Deletion Policy

- Do not delete project knowledge, documentation, source files, or user-provided data.
- Move outdated or unused project artifacts to `archive-cursor_memory_project/` for future reference when preservation is required.
- Generated caches, local indexes, temporary files, test artifacts, and local runtime artifacts may be removed by maintenance commands.
- Examples of removable generated artifacts include `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, `.coverage`, generated FAISS indexes, generated pickle metadata, temporary files, and local backup test outputs.
- When in doubt, archive instead of deleting.

## 2. Data Integrity

- Keep all original/raw data in `data/raw/` and never modify it directly.
- All data cleaning, merging, or transformation outputs go in `data/processed/`.
- Do not store API keys, passwords, credentials, personal data, protected health information, client-confidential information, or secrets in `memory-bank/`.

## 3. Documentation

- Every major step, decision, script, workflow, or architectural change should be documented in `docs/`, `diary/`, `logs/solutions/`, or a relevant `README.md`.
- All scripts and notebooks should have clear comments or docstrings explaining their role.
- Documentation should distinguish between template mode, local development mode, and production-evolution ideas.

## 4. Reproducibility

- Use scripts or notebooks for repeatable data transformations.
- Save reusable automation in `scripts/`.
- Keep manual operational steps documented in `docs/`, `status/`, or the relevant README.
- Prefer small, auditable commits over large untracked changes.

## 5. Inspiration & References

- Save inspiration, references, profiles, articles, and examples in the appropriate reference folder.
- Keep external references separated from project memory unless they are part of the active project context.

## 6. Script Library

- Store finalized reusable scripts/templates in the appropriate reusable script location when they are stable.
- Keep experimental scripts clearly labeled or documented.

## 7. Naming Conventions

- Use clear, descriptive, and consistent names.
- Avoid spaces in file names.
- Prefer underscores `_` or hyphens `-`.
- Use version numbers or dates for iterative files when useful.

## 8. Version Control

- Keep commits small and descriptive.
- Use conventional-style commit messages when practical, such as `docs:`, `fix:`, `chore:`, `test:`, or `refactor:`.
- Do not commit local secrets, private credentials, generated indexes, or environment files.

## 9. Archiving

- When moving files out of the main workflow, place them in `archive-cursor_memory_project/` when preservation is required.
- Add a short note in a log file if the archived file affects project history or decision-making.

## 10. Template Mode

- This repository is a reusable Cursor memory setup template.
- `memory-bank/` starts mostly empty by design.
- Do not fill memory-bank files with fake project knowledge.
- Populate memory-bank files only after real project kickoff, discovery, decisions, errors, implementation work, or milestones.

## 11. Simplicity & Scalability

- Keep folder depth manageable.
- Regularly review and update the structure as the project evolves.
- Prefer clear, auditable workflows over complex hidden automation.

---

These rules are mandatory for contributors and AI-assisted tools working in this repository. They are reinforced by `.cursor-rules.md`.
