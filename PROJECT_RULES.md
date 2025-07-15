# Project Rules

## 1. No Deletion Policy
- Never delete files.
- Move outdated or unused files to `archive-cursor_memory_project/` for future reference.

## 2. Data Integrity
- Keep all original/raw data in `data/raw/` and never modify it.
- All data cleaning, merging, or transformation outputs go in `data/processed/`.

## 3. Documentation
- Every major step (data collection, cleaning, analysis, script creation) must be documented in `docs/` or in a `README.md`.
- All scripts and notebooks must have clear comments and explanations.

## 4. Reproducibility
- Use scripts or notebooks for all data transformations, **never** manual edits.
- Save all code in `scripts/` or `notebooks/`.

## 5. Inspiration & References
- Save all inspiration (profiles, reels, ideas) in `inspiration/`, organised by type.

## 6. Script Library
- Store finalised, reusable scripts/templates for your own content in `scripts_library/`.

## 7. Naming Conventions
- Use clear, descriptive, and consistent names (e.g. `YYYYMMDD_description.csv`).
- Avoid spaces; use underscores `_` or hyphens `-`.

## 8. Version Control
- Use version numbers or dates in filenames for iterative work (e.g. `analysis_v2.ipynb`).

## 9. Archiving
- When moving files out of the main workflow, place them in `archive-cursor_memory_project/` with a note in a log file if needed.

## 10. Simplicity & Scalability
- Keep folder depth to three levels or less.
- Regularly review and update the structure as the project evolves.

---

These rules are mandatory for **all** contributors and are enforced by `.cursor-rules.md`. 