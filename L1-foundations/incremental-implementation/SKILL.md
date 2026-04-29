---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
source: addyosmani/agent-skills
imported: 2026-04-29
---

# Incremental Implementation

## Overview

Build in thin vertical slices — implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state.

## When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

## The Increment Cycle

1. **Implement** the smallest complete piece of functionality
2. **Test** — run the test suite
3. **Verify** — confirm the slice works as expected
4. **Commit** — save progress with a descriptive message
5. **Move to the next slice**

## Core Rules

- **Rule 0: Simplicity First** — what is the simplest thing that could work?
- **Rule 0.5: Scope Discipline** — touch only what the task requires
- **Rule 1: One Thing at a Time** — each increment changes one logical thing
- **Rule 2: Keep It Compilable** — project must build after each increment
- **Rule 3: Feature Flags** — for incomplete features that need merging
- **Rule 4: Safe Defaults** — new code defaults to conservative behavior
- **Rule 5: Rollback-Friendly** — each increment independently revertable

## Red Flags

- More than 100 lines written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping test/verify step to move faster
- Building abstractions before the third use case

## Increment Checklist

- [ ] Change does one thing completely
- [ ] All existing tests pass
- [ ] Build succeeds
- [ ] New functionality works as expected
- [ ] Change is committed with descriptive message

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
