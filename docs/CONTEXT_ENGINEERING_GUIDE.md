# Continuous Context Engineering Guide

> **Purpose**: Provide actionable, opinionated guidance for implementing long-term memory and context management in this repository. Draws exclusively from validated sources listed in `docs/refs/context_engineering.md`.

---

## 1. Core Principles

| # | Principle | Source(s) |
|---|-----------|-----------|
| 1 | Treat *context* as a first-class engineering concern, distinct from prompt design. | TowardsAI (2025) |
| 2 | Use *hierarchical memory* layers (short / mid / long-term) to balance recency and relevance. | Medium Dev Guide (2025), Strongly.ai (2024) |
| 3 | Compress aggressively via summarization to stay within model token limits. | Strongly.ai, TowardsAI |
| 4 | Retrieve older context with semantic search rather than brute-force concatenation. | Strongly.ai |
| 5 | Automate logging & memory updates to avoid human error. | Cursor Forum, AI Memory ext. |

---

## 2. Memory Architecture for This Project

```mermaid
flowchart TD
    subgraph ShortTerm
        A[Rolling Window (last N turns)]
    end
    subgraph MidTerm
        B[activeContext.md  \n(summarized rolling context)]
    end
    subgraph LongTerm
        C[Memory Bank files \n(projectbrief, techContext, systemPatterns, progress)]
    end
    A -->|periodic summary| B
    B --> C
```

1. **Rolling Window (Short-Term)**: Cursor default window (~3–4 k tokens) + recent chat.
2. **activeContext.md (Mid-Term)**: Script-generated summaries; updated every *N* exchanges or when token budget > threshold.
3. **Memory Bank (Long-Term)**: Persistent markdown docs, loaded via MCP at session start.

---

## 3. Implementation Roadmap

| Step | Component | Owner Script / File |
|------|-----------|---------------------|
| 1 | Create Memory Bank directory structure | `memory-bank/` (Task `memory_bank_setup`) |
| 2 | Summarization engine (summary-based method) | `scripts/summarize_chat.py` |
| 3 | Vector retrieval engine | `scripts/retrieve_context.py` |
| 4 | MCP integration for auto-load | Part of `mcp_integration` task |
| 5 | Extend `log_action.py` and `update_status.py` to trigger summaries & retrieval | `automation_and_logging` task |

---

## 4. Token Budget & Chunking Rules

* Maximum file read chunk: **200 lines** (per `.cursor-rules.md`).
* Aim for ≤ **1 k tokens** in `activeContext.md` after each summary.
* Retrieval engine should return **top-K ≤ 5** most relevant chunks to stay within budget.

---

## 5. Quality Checks

1. **Recall Accuracy** ≥ 80% (unit tests will verify the assistant answers questions that require info > N turns ago).
2. **Token Usage** remains within model limits on stress-test dataset.
3. **Latency** acceptable (< 1 s added by retrieval per request on local machine).

---

## 6. Maintenance

* Update references quarterly; review architecture when OpenAI / Cursor extends context windows.
* Keep `.cursor-rules.md` in sync with any process changes.

---

*Last updated: <!--date-->* 