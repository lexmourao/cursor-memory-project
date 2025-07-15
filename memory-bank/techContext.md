# Technical Context

> **Purpose**: Describe the technology stack, constraints, and environment details.

## Stack Overview

| Layer | Tech | Version |
|-------|------|---------|
| Language | Python | 3.11 |
| Vector DB | FAISS |  | 
| Embeddings API | OpenAI `text-embedding-3-small` |  | 
| Scheduler | cron |  |

## Constraints

* Example: Must run offline / air-gapped.
* …

## Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

<!-- Last updated: YYYY-MM-DD --> 