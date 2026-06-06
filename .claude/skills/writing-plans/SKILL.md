---
name: writing-plans
description: Use when a change is non-trivial (touches multiple files, has ordering
  dependencies, or carries risk) and benefits from a written, reviewable plan
  before implementation. Produces a concrete step-by-step plan with affected
  files, sequencing, and a verification strategy.
---

# Writing Plans

A good plan turns a fuzzy task into a sequence of small, verifiable steps. It lets
the user catch a wrong direction before code is written and gives you a checklist
to execute against.

## When to use

- The work spans several files or systems.
- Steps have ordering dependencies or migration concerns.
- The change is risky or hard to reverse.

For one-file, low-risk edits, skip the plan and just make the change.

## What a plan contains

1. **Goal** — one sentence: what will be true when this is done.
2. **Affected areas** — the files/modules/services you expect to touch, with a
   word on each.
3. **Steps** — an ordered list of small, individually verifiable actions. Each
   step should be something you can complete and check before moving on.
4. **Verification** — how you'll prove it works: which tests, commands, or manual
   checks. Prefer something runnable.
5. **Risks / open questions** — anything that could derail the plan or needs a
   decision.

## Principles

- **Small steps.** If a step can't be verified on its own, split it.
- **Sequence deliberately.** Do the thing that de-risks the rest first.
- **Make it executable.** Reference real file paths and real commands.
- **Keep it current.** As you execute, update the plan if reality diverges.

## After writing

Share the plan and get agreement before implementing anything substantial. Then
work the steps in order, verifying as you go.
