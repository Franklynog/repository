# Project Skills

This directory holds **project-scoped skills** for Claude Code. Because they live
in the repository, they are cloned with the project and are available in **web /
remote sessions** (Claude Code on the web), not just on a single developer's
machine.

## Layout

Each skill is a directory containing a `SKILL.md` file:

```
.claude/skills/
  <skill-name>/
    SKILL.md        # required: frontmatter + instructions
    ...             # optional supporting files (scripts, templates, references)
```

`SKILL.md` frontmatter must include:

```yaml
---
name: skill-name              # lowercase, hyphenated; matches the directory
description: One or two sentences describing WHAT the skill does and, crucially,
  WHEN to use it. Claude reads this to decide whether to invoke the skill, so
  lead with concrete trigger conditions.
---
```

Everything after the frontmatter is the instruction body Claude follows once the
skill is invoked.

## Skills in this directory

These are "Superpowers-style" workflow skills — disciplined defaults for how to
approach engineering work:

| Skill | Use when |
| --- | --- |
| `brainstorming` | A task is open-ended or underspecified and you should explore the problem before writing code. |
| `writing-plans` | A change is non-trivial and benefits from a written, reviewable plan before implementation. |
| `test-driven-development` | Implementing a behavior change — write the failing test first, then make it pass. |
| `systematic-debugging` | A bug or failing test needs root-cause analysis instead of guess-and-check. |
| `verification-before-completion` | About to claim a task is done — verify the change actually works first. |

## Long-form fanfiction skills

A curated set for writing **long, multi-chapter fanfiction**, where the hard
problems are continuity, characterization, and pacing across a big word count:

| Skill | Use when |
| --- | --- |
| `story-bible` | Maintaining the single source of truth for canon facts, OCs, world rules, timeline, and relationships in an ongoing story. |
| `character-voice` | Writing dialogue/POV and keeping characters distinct, consistent, and in-character (avoiding "OOC"). |
| `chapter-outlining` | Planning the overall arc and chapter-by-chapter beats, or breaking through the "muddy middle". |
| `continuity-tracking` | Revising or posting a new chapter and checking for contradictions in facts, timeline, knowledge state, and rules. |
| `prose-craft` | Drafting/revising scene prose — show-don't-tell, sensory grounding, dialogue, sentence rhythm. |
| `fanfic-conventions` | Preparing a fic for posting — ratings, tags, warnings, summary, POV/tense, trope handling, serialized-posting norms. |

## Adding a new skill

1. Create `.claude/skills/<name>/SKILL.md`.
2. Write a trigger-focused `description` (this is what makes the skill fire).
3. Keep the body actionable: numbered steps, checklists, do/don't.
4. Commit it so web sessions pick it up.
