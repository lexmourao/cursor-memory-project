# System Patterns

Core patterns used in this repository:

1. Local-first by default  
   The project is designed to run locally without requiring hosted infrastructure.

2. Starter template plus worked example  
   Root `memory-bank/` stays sparse for new projects. This directory shows the methodology applied to this repo.

3. Active vs archived separation  
   Deprecated workflows, docs, and deployment scaffolding are preserved under `archive/` instead of deleted.

4. Fallback-first AI workflow  
   OpenAI-backed summarization and embedding paths have fallback behavior when API keys are absent.

5. Traceable retrieval  
   Retrieval results expose source and chunk metadata to support inspection and auditability.

6. PR-scoped cleanup  
   Each cleanup step is small, reviewed, verified, merged, and then followed by local cleanup.
