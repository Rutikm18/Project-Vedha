# AGENTS.md

## Learning notes

- When the user starts a prompt with `/learning` or invokes the `learning` custom prompt, append exactly one new concept note to `learning.md`.
- Treat `/learning <concept>` as the command format: strip `/learning` and use the remaining text as the concept. If it is missing or unclear, ask one short clarification.
- Never delete, overwrite, reorder, or summarize previous notes in `learning.md`.
- Add only core technical concepts: software engineering, architecture, security, backend, frontend, databases, infrastructure, algorithms, protocols, testing, or production operations.
- Do not add meta workflow notes such as Codex usage, prompt setup, file maintenance, or command mechanics unless the user explicitly asks to learn that as a technical topic.
- Before writing, think like an expert software engineer: identify the real underlying concept, remove fluff, and explain only what is necessary.
- Add the new entry under `## Notes`; keep it concise but useful, with one or two short sentences per field when needed.
- Use this exact format for every new concept:

```md
## Concept Headline

**What:** Clear meaning of the concept.

**Problem:** The practical issue, risk, or confusion it solves.

**Solution:** The core idea or pattern that fixes the problem.

**When Use:** Where this concept should be applied.

**Why Use:** Why it matters in real engineering work.
```
