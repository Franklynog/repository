---
name: systematic-debugging
description: Use when facing a bug, failing test, crash, or unexpected behavior
  that isn't obvious at a glance. Replaces guess-and-check with a disciplined
  loop: reproduce, isolate, form a hypothesis, test it, and fix the root cause.
---

# Systematic Debugging

Random edits "until it works" produce fragile fixes and hidden new bugs. Debug by
forming and testing hypotheses against evidence.

## Process

1. **Reproduce reliably.** Find the smallest, most consistent way to trigger the
   problem. A reliable repro is the foundation for everything else; if it's
   intermittent, work to make it deterministic first.
2. **Gather evidence.** Read the actual error message and stack trace fully.
   Check logs, inputs, and recent changes (`git log`, `git diff`). Don't theorize
   ahead of the data.
3. **Form one hypothesis.** State a specific, falsifiable guess: "X fails because
   Y is null when Z." 
4. **Test the hypothesis.** Add a log/assertion/breakpoint or a targeted check
   that would confirm or refute it. Run it. Let the result decide.
5. **Narrow.** If confirmed, zoom into the root cause. If refuted, discard it and
   form a new hypothesis — don't pile guesses on top of each other.
6. **Fix the root cause**, not the symptom. A patch that hides the symptom while
   leaving the cause will resurface.
7. **Verify.** Confirm the original repro now passes, and add/keep a test so the
   bug can't return.

## Principles

- **Read the error.** Most bugs are explained by the message you skimmed past.
- **Change one thing at a time.** Multiple simultaneous edits make it impossible
  to know what fixed (or broke) what.
- **Bisect.** When the cause is unclear, halve the search space repeatedly
  (`git bisect`, commenting out regions, narrowing inputs).
- **Question assumptions.** The bug lives where you're certain there's no bug.

## Anti-patterns

- Editing code before you can reproduce the problem.
- "Fixing" by adding try/catch that swallows the real error.
- Declaring it fixed without re-running the repro.
