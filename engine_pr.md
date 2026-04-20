# Engine PR Guide

Use this for engine bugfix PRs.

## Rule

If a code change fixes an engine bug, add a regression test when practical.

If a regression test is not practical, say why in the PR. That should be an exception.

## Before Opening The PR

- reproduce the bug
- fix the bug
- add or update the regression test
- run the relevant engine tests before opening the PR
- run the relevant unit tests if Python-side logic changed

## Test Commands

```bash
./scripts/run_engine_tests.sh
./scripts/run_unit_tests.sh
```

## PR Notes

Keep the PR note short and direct:

- what broke
- what changed
- what test covers it

If the fix changes behavior without a regression test, explain why the test is missing.
