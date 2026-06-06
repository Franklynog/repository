---
name: test-driven-development
description: Use when implementing or changing a behavior in code that can be
  tested (bug fix, new function, new endpoint, edge-case handling). Drives the
  change with a failing test first (red), then minimal code to pass (green), then
  refactor — so the behavior is pinned down and regressions are caught.
---

# Test-Driven Development

Write the test before the code. The test defines "done", forces you to think about
the interface before the implementation, and leaves a regression guard behind.

## The loop

1. **Red.** Write the smallest test that captures the next bit of desired
   behavior. Run it. Confirm it fails — and fails for the *right* reason (the
   behavior is missing, not a typo or import error).
2. **Green.** Write the minimal code to make that test pass. Resist adding
   anything the test doesn't require yet.
3. **Refactor.** With the test green, clean up names, duplication, and structure.
   Re-run the test; it must stay green.
4. **Repeat** for the next behavior.

## Rules

- **One behavior at a time.** Don't write five tests then five implementations.
- **Watch it fail first.** A test that passes before you write the code tests
  nothing. Seeing red proves the test exercises the new behavior.
- **Minimal green.** Don't gold-plate. New requirements get new tests.
- **Test behavior, not implementation.** Assert on observable outcomes, not
  private internals, so refactors don't break tests.

## For bug fixes

1. Write a test that reproduces the bug — it should fail, demonstrating the bug.
2. Fix the code until that test passes.
3. The failing-then-passing test is your proof the bug is actually fixed and
   won't silently return.

## When to relax

Exploratory spikes and throwaway prototypes don't need TDD. But once the design
is settled and the code is meant to stay, drive it with tests.
