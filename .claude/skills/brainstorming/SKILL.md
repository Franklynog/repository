---
name: brainstorming
description: Use BEFORE writing code when a request is open-ended, ambiguous, or
  could be solved several ways (e.g. "add a feature", "improve X", "how should we
  do Y"). Explores the problem space, surfaces options and trade-offs, and
  converges on an approach with the user before any implementation begins.
---

# Brainstorming

Jumping straight to code on an underspecified task wastes effort and produces the
wrong thing. Spend a short, focused phase understanding the problem and agreeing
on direction first.

## When to use

- The request is vague ("make it better", "add search").
- There are multiple plausible designs with real trade-offs.
- The cost of building the wrong thing is high.

Skip this for trivial, unambiguous changes — go straight to doing them.

## Process

1. **Restate the goal.** In one or two sentences, say what you understand the
   user actually wants and why. Confirm or correct.
2. **Surface unknowns.** List the open questions that would change the design.
   Ask the 2–4 that matter most; don't interrogate.
3. **Generate options.** Propose 2–3 distinct approaches. For each, give a
   one-line summary, the main benefit, and the main cost or risk.
4. **Recommend.** State which option you'd pick and why, in one or two sentences.
5. **Converge.** Get explicit agreement on the approach (and scope) before
   moving to a plan or to code.

## Output shape

Keep it tight — a short bulleted comparison, not an essay. The deliverable is a
chosen direction the user has signed off on, not a design document.

## Anti-patterns

- Presenting one option as if it were the only choice.
- Asking a long list of low-value clarifying questions.
- Sliding into implementation before the direction is agreed.
