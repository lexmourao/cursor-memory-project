"""Summarization service for active context workflows."""

from datetime import datetime
import os
from pathlib import Path
from typing import Any

from app.models.summarization import SummarizationResponse
from scripts.retrieve_context import add_chunk

OpenAIClient: Any
try:
    from openai import OpenAI as OpenAIClient
except ImportError:
    OpenAIClient = None


MEMORY_BANK_PATH = Path("memory-bank/activeContext.md")


class SummarizationService:
    """Summarize text and optionally update active memory context."""

    def summarize(
        self,
        text: str,
        model: str = "gpt-4o",
        manual: bool = False,
        embed: bool = True,
    ) -> SummarizationResponse:
        """Summarize text, write active context, and optionally embed the result."""
        if manual:
            summary = text.strip()
            used_fallback = False
        else:
            summary, used_fallback = self._summarize_with_model(text, model=model)

        wrote_active_context = self._write_active_context(summary)

        embedded = False
        if embed:
            embedded = self._embed_summary(summary)

        return SummarizationResponse(
            summary=summary,
            word_count=len(summary.split()),
            model=model,
            used_fallback=used_fallback,
            wrote_active_context=wrote_active_context,
            embedded=embedded,
        )

    def _summarize_with_model(self, text: str, model: str) -> tuple[str, bool]:
        """Summarize with OpenAI when configured, otherwise use fallback."""
        if OpenAIClient is None or os.getenv("OPENAI_API_KEY") is None:
            return self._fallback_summary(text), True

        prompt_system = (
            "You are an expert summarization engine. Produce a concise markdown "
            "summary capturing key decisions, open questions, and next steps. "
            "Emphasize technical details needed for future context."
        )

        try:
            client = OpenAIClient()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
                max_tokens=400,
            )
            content = response.choices[0].message.content or ""
            return content.strip(), False
        except Exception:
            return self._fallback_summary(text), True

    def _fallback_summary(self, text: str) -> str:
        """Return a simple fallback summary from the last non-empty lines."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines[-10:])

    def _write_active_context(self, summary: str) -> bool:
        """Write summary to activeContext.md."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        header = "# Active Context (Auto-Generated)\n\n"
        header += f"> **Generated:** {timestamp}\n\n---\n\n"

        MEMORY_BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
        MEMORY_BANK_PATH.write_text(header + summary, encoding="utf-8")
        return True

    def _embed_summary(self, summary: str) -> bool:
        """Embed summary into the retrieval index."""
        add_chunk(summary, source="activeContext")
        return True
