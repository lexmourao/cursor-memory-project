# Validation Report

This document records empirical evidence that the memory system improves Cursor responses.

## Scenario
1. Started MCP server (`make dev`).
2. Asked Cursor in a fresh chat: *"What is the project vision?"*  
   – Without memory: Cursor could not answer.
3. Same question after memory load: Cursor summarized `memory-bank/projectbrief.md` correctly.

## Key Observations
* Retrieval engine surfaced correct chunk (score 0.89).
* Response token count stayed within 500 tokens.

## Next Steps
* Automate this scenario into an integration test. 