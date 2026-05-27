# ADR 0002: Retrieval Metadata Storage Strategy

## Status

Accepted

## Date

2026-05-27

## Context

The Cursor Memory Project now has a tested retrieval API and metadata-aware retrieval results.

Current retrieval results include:

```text
score
source
chunk_idx
text
```

The retrieval workflow currently stores FAISS metadata in:

```text
memory-bank/embeddings_meta.pkl
```

This metadata is used by:

```text
scripts/retrieve_context.py
app/services/retrieval_service.py
POST /retrieval/query
```

The repository has also introduced a formal chunk metadata schema in:

```text
app/models/chunk.py
```

Implemented models:

```text
ChunkMetadata
RetrievedChunk
```

The current implementation works and is tested, but the metadata storage format still needs a clear evolution path.

## Decision

For the current stage of the project:

```text
Keep pickle as the internal metadata storage format for the existing FAISS retrieval workflow.
```

This preserves the current CLI and backend behavior without introducing unnecessary migration risk.

However, the project should treat pickle as an internal implementation detail, not as the long-term inspection or dashboard format.

The recommended evolution path is:

```text
Current: pickle metadata for FAISS workflow compatibility
Next: JSON metadata export for inspection and review
Later: SQLite metadata storage if queryability, dashboards, migrations, or multi-project support become necessary
```

## Rationale

### Why keep pickle now

Pickle is already used by the retrieval workflow and works with the current scripts.

Keeping it avoids:

- breaking existing CLI behavior
- introducing an unnecessary migration during backend stabilization
- creating extra storage code before the retrieval model is fully stable
- adding complexity before there is a real dashboard or multi-project use case

This fits the current project principle:

```text
Improve through small, auditable, green steps.
```

### Why not rely on pickle forever

Pickle is not ideal as a long-term public or inspection-friendly metadata format.

Limitations:

- not human-readable
- not ideal for technical reviewers
- not safe for untrusted data
- not suitable for easy diffs
- not ideal for dashboards
- not ideal for schema evolution
- not ideal for future multi-project querying

Because this project is a public technical artifact, future metadata should become easier to inspect and reason about.

### Why JSON is the next likely step

JSON is the best next step for public readability and lightweight inspection.

A future JSON export could support:

- reviewer inspection
- dashboard prototypes
- debugging retrieval chunks
- comparing metadata changes
- validating chunk schemas
- safer handoff documentation

Possible future file:

```text
memory-bank/embeddings_meta.json
```

or:

```text
data/processed/retrieval_metadata.json
```

The JSON export should be generated, not manually edited.

### Why SQLite may be useful later

SQLite becomes useful if retrieval metadata needs:

- filtering
- querying
- multi-project support
- migrations
- dashboards
- indexed metadata fields
- richer source/chunk relationships
- audit or inspection workflows

SQLite is not necessary yet because the current project is still local-first and file-based.

## Consequences

### Positive consequences

- Preserves current working retrieval behavior
- Keeps existing CLI workflow stable
- Avoids risky migration during backend evolution
- Gives the project a clear metadata storage roadmap
- Supports future JSON/SQLite evolution without overengineering now
- Aligns metadata storage decisions with the formal chunk schema

### Negative consequences

- Metadata remains non-human-readable for now
- Pickle remains unsuitable for untrusted metadata input
- Dashboard-ready inspection still requires a later export or storage improvement
- JSON/SQLite migration remains future work

## Implementation Notes

Current metadata storage remains:

```text
memory-bank/embeddings_meta.pkl
```

Current vector index remains:

```text
memory-bank/embeddings.faiss
```

Current typed schema remains:

```text
app/models/chunk.py
```

The retrieval API should continue returning:

```text
score
source
chunk_idx
text
```

Future implementation options:

1. Add JSON metadata export while keeping pickle as the internal runtime format.
2. Add tests that validate JSON export shape against `ChunkMetadata` / `RetrievedChunk`.
3. Add optional SQLite metadata storage if the project adds dashboards or multi-project retrieval.
4. Keep public CI free from private secrets and environment-specific requirements.

## Current Decision Summary

```text
Keep pickle now.
Add JSON export later for inspectability.
Consider SQLite later for queryability and dashboards.
```

## Related Files

```text
scripts/retrieve_context.py
app/models/chunk.py
app/models/retrieval.py
app/services/retrieval_service.py
tests/test_api_retrieval.py
docs/BACKEND_DESIGN.md
status/roadmap.md
```

## Follow-Up Work

- [ ] Add JSON metadata export option.
- [ ] Add tests for exported metadata shape.
- [ ] Document generated metadata files.
- [ ] Consider SQLite only after dashboard or multi-project requirements become real.
- [ ] Keep generated FAISS, pickle, and future metadata exports out of version control unless explicitly intended as examples.
