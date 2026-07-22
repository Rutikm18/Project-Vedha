# Learning Notes

Use this file to add core technical concepts that need to be learned.
Keep each note direct, practical, append-only, and detailed only where useful.

## Writing Rules

- Add only core technical concepts: software engineering, architecture, security, backend, frontend, databases, infrastructure, algorithms, protocols, testing, or production operations.
- Do not add meta workflow notes such as Codex usage, prompt setup, file maintenance, or command mechanics unless explicitly requested as a technical topic.
- Think like an expert software engineer before writing: capture the real concept, the practical problem, and the correct usage.
- Keep each field short but useful. Prefer one or two focused sentences over vague one-liners or long explanations.

## Format

```md
## Concept Headline

**What:** Clear meaning of the concept.

**Problem:** The practical issue, risk, or confusion it solves.

**Solution:** The core idea or pattern that fixes the problem.

**When Use:** Where this concept should be applied.

**Why Use:** Why it matters in real engineering work.
```

## Notes

Add new concepts below this line. Do not delete previous notes.

---

## Append-Only Learning Notes

**What:** A notes file where new concepts are added without removing old ones.

**Problem:** Important learning points can be lost if old notes are overwritten.

**Solution:** Always append each new concept below the existing notes.

**When Use:** Use when building a personal learning history.

**Why Use:** It keeps all previous learning available for review.

## AGENTS.md Project Guidance

**What:** A repo instruction file that tells Codex how to behave in this project.

**Problem:** Repeating the same workflow rules in every prompt is slow and error-prone.

**Solution:** Store durable project rules in `AGENTS.md`.

**When Use:** Use for project-specific habits, formats, checks, and workflows.

**Why Use:** Codex reads it automatically and follows consistent rules.

## Codex Custom Prompt

**What:** A Markdown prompt saved in `~/.codex/prompts` for reuse.

**Problem:** Common tasks need the same instructions again and again.

**Solution:** Save the task as a reusable prompt file.

**When Use:** Use for repeated workflows like adding learning notes.

**Why Use:** It turns repeated instructions into a quick command.

## Slash Command Prompt

**What:** A command-style shortcut that invokes a saved Codex prompt.

**Problem:** Typing full instructions each time wastes time.

**Solution:** Use `/prompts:learning` with the concept name.

**When Use:** Use when adding a new concept to `learning.md`.

**Why Use:** It makes the learning workflow fast and consistent.

## Prompt Arguments

**What:** Extra text passed into a custom prompt.

**Problem:** A reusable prompt still needs the specific topic each time.

**Solution:** Pass the concept after the command, such as `/prompts:learning JWT`.

**When Use:** Use when the same prompt needs different input.

**Why Use:** It keeps the command reusable while changing only the topic.
