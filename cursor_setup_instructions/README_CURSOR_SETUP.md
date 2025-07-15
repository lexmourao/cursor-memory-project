# 🚀 Cursor Project Setup Instructions (Copy-Paste Template)

This guide will help you set up a professional, automated, and context-aware Cursor project. Follow these steps to ensure robust documentation, error tracking, automation, and team collaboration from day one.

---

## 1. Create the Folder Structure

```
project_root/
│
├── data/                        # Raw and processed data
│   ├── raw/
│   ├── processed/
│   └── sources/
├── docs/                        # Documentation, context, architecture, security
│   ├── CONTEXT_VERIFICATION.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   └── data_dictionary.md
├── status/                      # Status, checklists, roadmap
│   ├── current_status.md
│   ├── checklist_onboarding.md
│   ├── checklist_data.md
│   ├── checklist_deployment.md
│   └── roadmap.md
├── dairy/                       # Project log and daily diary
│   ├── project_log.md
│   └── log_action.py
├── scripts/                     # Automation, backup, error logging
│   ├── update_status.py
│   ├── backup_data.sh
│   └── log_error.py
├── logs/                        # Error logs and solutions
│   ├── errors/
│   ├── solutions/
│   └── error_index.md
├── notebooks/                   # Jupyter/Colab notebooks
│   └── scripts_templates/
│       ├── template_analysis.ipynb
│       └── template_script.py
├── tests/                       # Data validation and unit tests
│   └── test_data_validation.py
├── scripts_library/             # Finalized scripts/templates for content
├── inspiration/                 # Notes, screenshots, docs about inspiring profiles
│   ├── profiles/
│   └── reels/
├── archive-<project_name>/      # Archived/old files (never delete)
├── backups/                     # Automated backups
├── .gitignore
├── requirements.txt
├── CONTRIBUTING.md
├── PROJECT_RULES.md
├── README.md
├── .cursor-rules.md
└── ...
```

---

## 2. Essential Files & Templates
- **PROJECT_RULES.md**: All project rules, no-deletion policy, naming conventions, archiving, and context checklist.
- **README.md**: Project overview, quickstart, structure, and contributing reference.
- **CONTRIBUTING.md**: Guidelines for onboarding, code style, PRs, and communication.
- **CONTEXT_VERIFICATION.md**: Checklist and context questions for onboarding and session tracking.
- **ARCHITECTURE.md**: System architecture, data flow, and workflow documentation.
- **DEPLOYMENT.md**: Deployment and maintenance guide.
- **SECURITY.md**: Security, compliance, and incident response guide.
- **data_dictionary.md**: Document all fields in your datasets.
- **current_status.md, checklists, roadmap**: Track project status, onboarding, data, deployment, and milestones.
- **project_log.md**: Daily log and milestone tracking.
- **log_action.py**: Script to automate project log updates.
- **update_status.py**: Script to automate status/checklist/roadmap updates.
- **backup_data.sh**: Script for regular backups.
- **log_error.py**: Script for error logging, solution tracking, and learning documentation.
- **error_index.md**: Index of all errors, solutions, and learnings.
- **template_analysis.ipynb, template_script.py**: Templates for new analyses/scripts.
- **test_data_validation.py**: Sample data validation script.

---

## 3. Cursor Rules (.cursor-rules.md)
- Always read and follow the rules in `PROJECT_RULES.md` before making changes.
- Never delete files; move them to `archive-<project_name>/` instead.
- Maintain the folder structure and naming conventions as described in `PROJECT_RULES.md`.
- Always update all relevant status, checklist, and roadmap files in the `status/` folder when making changes. Use `scripts/update_status.py` for automation.
- Always log errors, solutions, and learnings in the `logs/` folder using `scripts/log_error.py`.
- Always check `logs/error_index.md` and `logs/solutions/` for past solutions before suggesting new ones.
- All contributors must review `PROJECT_RULES.md` regularly.

---

## 4. Automation & Best Practices
- Use the provided scripts for logging, status updates, and backups.
- Log all significant actions, errors, and solutions.
- Keep all documentation up to date after every major change.
- Use version control (Git) and `.gitignore` to avoid tracking data, archives, and secrets.
- Onboard new contributors with the onboarding checklist and context verification.
- Schedule regular reviews of checklists, roadmap, and documentation.

---

## 5. Quickstart for New Projects
1. Copy this folder and all template files into your new project.
2. Update `<project_name>` in folder names and documentation.
3. Run `pip install -r requirements.txt` to set up your environment.
4. Follow the onboarding checklist and context verification before starting work.
5. Use automation scripts for all logging, status, and error tracking.
6. Maintain all rules and best practices for a professional, scalable, and auditable project.

---

## 6. Full Project Rules

# Project Rules

## 1. No Deletion Policy
- Never delete files.
- Move outdated or unused files to `archive-<project_name>/` for future reference.

## 2. Data Integrity
- Keep all original/raw data in `data/raw/` and never modify it.
- All data cleaning, merging, or transformation outputs go in `data/processed/`.

## 3. Documentation
- Every major step (data collection, cleaning, analysis, script creation) must be documented in `docs/` or in a `README.md`.
- All scripts and notebooks must have clear comments and explanations.

## 4. Reproducibility
- Use scripts or notebooks for all data transformations, not manual edits.
- Save all code in `scripts/` or `notebooks/`.

## 5. Inspiration & References
- Save all inspiration (profiles, reels, ideas) in `inspiration/`, organized by type.

## 6. Script Library
- Store finalized, reusable scripts/templates for your own content in `scripts_library/`.

## 7. Naming Conventions
- Use clear, descriptive, and consistent names (e.g., `YYYYMMDD_description.csv`).
- Avoid spaces; use underscores `_` or hyphens `-`.

## 8. Version Control
- Use version numbers or dates in filenames for iterative work (e.g., `analysis_v2.ipynb`).

## 9. Archiving
- When moving files out of the main workflow, place them in `archive-<project_name>/` with a note in a log file if needed.

## 10. Simplicity & Scalability
- Keep folder depth to three levels or less.
- Regularly review and update the structure as the project evolves.

---

## 7. Security & Compliance Rules

# Security & Compliance Guide

## Data Protection
- Store all original data in data/raw and never modify it
- Processed data goes in data/processed
- Archive files instead of deleting
- Use strong passwords and access controls for sensitive data

## Access Control
- Only authorized contributors may edit scripts, data, or documentation
- All changes must be logged in dairy/project_log.md
- Use version control for all code and notebooks

## Compliance
- Follow all relevant data privacy laws (e.g., LGPD, GDPR if applicable)
- Document all data sources and processing steps
- Maintain audit trails via project logs and version control

## Incident Response
- If data integrity or privacy is compromised, log the incident in dairy/project_log.md and notify the project owner
- Archive affected files and document the response

---

## 8. Context Verification Checklist

# CONTEXT VERIFICATION CHECKLIST

## MANDATORY READING CHECKLIST
Before taking ANY action, all contributors MUST verify they have read and understood ALL of these files:

### Core Context Files (REQUIRED)
- [ ] PROJECT_RULES.md - Project rules and guidelines
- [ ] README.md - Project overview and structure
- [ ] docs/ARCHITECTURE.md - System architecture and data flow
- [ ] docs/DEPLOYMENT.md - Deployment and maintenance guide
- [ ] docs/SECURITY.md - Security and compliance
- [ ] dairy/project_log.md - Project log and daily diary

### Project Files (REFERENCE)
- [ ] data/raw/ - Original data
- [ ] data/processed/ - Processed data
- [ ] scripts/ - Data processing scripts
- [ ] notebooks/ - Analysis notebooks

## CONTEXT VERIFICATION QUESTIONS
1. What is the main goal of the project?
2. Where are the original and processed data stored?
3. What is the policy for deleting or archiving files?
4. Which files must be updated after every significant action?
5. What are the core folders and their purposes?
6. What are the main security and compliance requirements?

## CONTEXT CONFIRMATION STATEMENT
"I have read and understood all required context files for this project. I confirm understanding of the project rules, folder structure, data management, and documentation requirements. I will maintain consistency with all established decisions and focus on professional, reproducible, and well-documented work."

---

**You are now ready to start your Cursor project with world-class structure, automation, and documentation!** 