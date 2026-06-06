---
name: verification-before-completion
description: Use right before claiming a task is done or reporting success. Forces
  actually verifying the change works — running tests, builds, linters, or the app
  — instead of asserting completion from inspection alone.
---

# Verification Before Completion

"It should work" is not "it works." Before you tell the user a task is complete,
prove it with evidence.

## Checklist before claiming done

1. **Re-read the request.** Did you address every part of what was asked, not
   just the easy part? Check scope and acceptance criteria.
2. **Run the tests.** Execute the relevant test suite (or the specific tests for
   the change). They must pass. If there were no tests, consider adding one.
3. **Build / typecheck / lint.** Run whatever the project uses. A change that
   breaks the build isn't done.
4. **Exercise the behavior.** Where practical, actually run the code path you
   changed — invoke the function, hit the endpoint, run the CLI, load the page —
   and observe the expected result.
5. **Check for collateral damage.** Did you leave debug prints, commented-out
   code, or unintended edits? Review the diff (`git diff`).

## Reporting honestly

- If tests pass, say so and name what you ran.
- If something fails, **say that** with the actual output — don't paper over it.
- If you skipped a step (couldn't run X), state it plainly rather than implying
  full verification.
- Only state "done and verified" when you have actually verified.

## Principle

The deliverable is working software plus evidence it works — not a confident
claim. When in doubt, run it.
