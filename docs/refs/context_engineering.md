# Continuous Context Engineering – Curated References

> This bibliography collects **validated, public sources** on long-term context, LLM memory design, and Cursor-specific memory tooling. Each entry includes a short annotation with key takeaways relevant to this project.

---

## 1. Foundational Articles & Guides

1. **Why Context Engineering Matters More Than Prompt Engineering** – *Towards AI*, 27 Jun 2025.  
   URL: <https://pub.towardsai.net/why-context-engineering-matters-more-than-prompt-engineering-8fd01cd2d0b6>  
   *Takeaways*: Defines context engineering as a discipline; stresses compression, memory isolation, and tool-call awareness.

2. **Context Engineering in the Age of LLMs: A Developer’s Definitive Guide** – Medium, 07 Jul 2025.  
   URL: <https://medium.com/data-and-beyond/context-engineering-in-the-age-of-llms-a-developers-definitive-guide-3b0e0d05612d>  
   *Takeaways*: Breaks down storage vs retrieval layers; recommends hierarchical memory (short / mid / long-term).

3. **Mastering LLM Memory: A Comprehensive Guide** – *Strongly.ai* blog, 08 Oct 2024.  
   URL: <https://www.strongly.ai/blog/mastering-llm-memory-a-comprehensive-guide.html>  
   *Takeaways*: Compares sequential, sliding-window, summary-based, and retrieval-based strategies; highlights compression & vector DBs.

4. **Short-Term vs Long-Term LLM Memory: When to Use Prompts vs Recall?** – RandomTrees blog, 16 Oct 2023.  
   URL: <https://randomtrees.com/blog/short-term-vs-long-term-llm-memory-prompts-vs-recall/>  
   *Takeaways*: Clarifies distinction between ephemeral prompt context and persistent knowledge base.

5. **Making LLMs Remember Using this Prompting Technique** – *Generative AI* (Medium), 23 Feb 2025.  
   URL: <https://generativeai.pub/making-llms-remember-using-this-prompting-technique-5ea97a53fc07>  
   *Takeaways*: Showcases prompt-only memory cues; useful for fallback when external storage unavailable.

---

## 2. Cursor-Specific Memory Solutions

1. **AI Memory Extension** – VS Marketplace / GitHub `Ipenywis/aimemory`  
   Marketplace: <https://marketplace.visualstudio.com/items?itemName=CoderOne.aimemory>  
   GitHub: <https://github.com/Ipenywis/aimemory>  
   *Takeaways*: Implements Memory-Bank (markdown files) + MCP server for Cursor integration; good reference implementation.

2. **Cursor Forum – Persistent, Intelligent Project Memory (Thread)**, Jan–Apr 2025.  
   URL: <https://forum.cursor.com/t/persistent-intelligent-project-memory/39109>  
   *Takeaways*: Community pain points & proposed features; confirms `.cursor-rules.md` as interim solution.

3. **Memory Bank Feature for your Cursor (Showcase)** – Cursor Forum thread, Mar 2025.  
   URL: <https://forum.cursor.com/t/memory-bank-feature-for-your-cursor/71979>  
   *Takeaways*: Walk-through of `npx cursor-bank init`; outlines required markdown files.

4. **cursor.directory Repository** – GitHub `pontusab/cursor.directory`  
   URL: <https://github.com/pontusab/cursor.directory>  
   *Takeaways*: Large catalogue of community-maintained `.cursor-rules` and MCPs; reusable patterns.

---

## 3. Standards & Protocols

1. **Model Context Protocol (MCP) Servers**  
   GitHub: <https://github.com/modelcontextprotocol/servers>  
   *Takeaways*: Defines protocol for external context graphs; Cursor can connect to MCP servers for automatic memory ingestion.

---

## 4. Observed Best Practices (Cross-referenced)

| Practice | Supported By |
|----------|--------------|
| Summary-based compression of long chats | [1], [3] |
| Retrieval / vector search for relevance | [3], MCP Servers |
| Hierarchical memory (short/mid/long) | [2], [3] |
| Memory-Bank markdown files + automation | AI Memory ext., Cursor Forum |
| `.cursor-rules.md` enforcement | Cursor Forum |

---

*Last updated: <!--date-->* 