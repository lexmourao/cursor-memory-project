# Project Makefile

.PHONY: help dev summarize rebuild test clean install

help:
	@echo "Available targets:"
	@echo "  install    Install dependencies via pip"
	@echo "  dev        Start MCP server (background) and tail logs"
	@echo "  summarize  Run summarize_chat (manual stdin) then rebuild index"
	@echo "  rebuild    Rebuild FAISS index from memory-bank"
	@echo "  test       Run pytest"
	@echo "  clean      Remove generated index, logs, __pycache__"

install:
	pip install -r requirements.txt

# Runs MCP server detached (Ctrl-C to stop foreground one)
dev:
	python scripts/run_mcp_server.py &
	@echo "MCP server running at http://localhost:7331 (PID $$!)"

summarize:
	@echo "Paste chat content, then Ctrl-D:";
	cat | python scripts/summarize_chat.py --stdin --manual
	python scripts/retrieve_context.py rebuild

rebuild:
	python scripts/retrieve_context.py rebuild

test:
	pytest -q

clean:
	rm -f memory-bank/embeddings.faiss memory-bank/embeddings_meta.pkl
	rm -rf logs/errors/* logs/solutions/*
	find . -name '__pycache__' -type d -exec rm -rf {} + 