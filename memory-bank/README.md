# Memory Bank

> This folder is the starter memory layer for the Cursor Memory Project.

The `memory-bank/` directory is intentionally initialized as a template. It is designed to be populated when a real project starts, not filled with fake project knowledge in advance.

This repository is a reusable setup system for Cursor-based AI-assisted development. When a new project begins, these files become the long-term memory layer used by Cursor, ChatGPT, Codex, and related AI-assisted workflows.

## Why This Starts Mostly Empty

At project kickoff, the memory system should begin with structured placeholders. Real project knowledge should be added only after actual discovery, implementation, decisions, errors, and milestones occur.

This prevents:

- fake context from contaminating future work
- hallucinated project assumptions
- outdated starter information being treated as truth
- confusion between template setup and active project memory

## File Roles

| File | Purpose |
|---|---|
| `projectbrief.md` | High-level project vision, goals, non-goals, and stakeholders |
| `productContext.md` | User problems, personas, motivations, and real-world context |
| `activeContext.md` | Rolling generated summary of recent project interactions |
| `systemPatterns.md` | Architecture patterns, design decisions, and implementation logic |
| `techContext.md` | Technology stack, environment constraints, and setup details |
| `progress.md` | Current status, blockers, next steps, and operational progress |

## Active Context

`activeContext.md` may be overwritten by:

```bash
python scripts/summarize_chat.py
```

Do not treat placeholder content in `activeContext.md` as final project knowledge. It becomes meaningful after the first real project session is summarized.

## Security Rule

Do not store the following in memory-bank files:

- API keys
- passwords
- private credentials
- personal data
- protected health information
- client-confidential information
- secrets or tokens
- proprietary data without authorization

Use environment variables, secret files, or approved secure storage for sensitive values.

## How to Use This Folder

For a new project:

1. Start with the template files.
2. Fill `projectbrief.md` during project kickoff.
3. Update `productContext.md` after user/persona discovery.
4. Use `activeContext.md` for rolling summaries.
5. Record architecture decisions in `systemPatterns.md`.
6. Keep `techContext.md` aligned with the real stack.
7. Update `progress.md` after significant milestones.

The purpose of this folder is not to replace human judgment. It gives AI-assisted development tools a structured memory layer so work can continue across sessions with less context loss.
