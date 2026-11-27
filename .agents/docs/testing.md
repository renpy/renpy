# Testing Ren'Py

Read this before writing, changing, or reviewing tests. [AGENTS.md](../../AGENTS.md#which-checks-to-run) lists which
checks each kind of change needs.

## When to add or update tests

- Add or extend behavior-focused tests for new or intentionally changed behavior, bug fixes with
  a plausible recurrence risk, and changes with a high likelihood or consequence of regression.
- Assess the actual change, not just the file it touches. Pay particular attention to
  save/compiled-script compatibility, rollback, persistent data, prediction, control flow, and
  shared engine logic.
- Existing tests suffice when they exercise the exact behavior or failure mode and assert the
  intended outcome. Extend them when needed; do not add redundant tests simply because code changed.
- For a bug fix, make the regression test fail before the fix and pass afterward where feasible.
  Assert observable behavior rather than incidental implementation details.
- Documentation-only edits, mechanical changes, and low-risk fixes already covered do not
  automatically require new tests. Still run the relevant existing checks.
- Choose coverage at the affected boundary: Python tests for anything that can run after
  engine initialization, runtime testcases only for behavior that needs the running game
  ([see below](#runtime-testcases-testcasesgametests)), and the save/load, rollback,
  persistent-restart, or schema checks [listed in AGENTS.md](../../AGENTS.md#which-checks-to-run) when applicable.
- If required automated coverage is impractical, report the specific reason, manual validation
  performed and its result, and the remaining regression risk. If manual validation is also
  unavailable, explicitly report the unverified path; do not present the change as validated.

## Test files and quality

Organization:

- One test file per source file, named `test_<path under renpy/, "/" replaced by "_">.py`:
  `renpy/bootstrap.py` → `test_bootstrap.py`, `renpy/gl2/live2d.py` → `test_gl2_live2d.py`. A
  package's `__init__.py` takes the package name (`renpy/translation/` → `test_translation.py`).
  Tests for tools in `scripts/` and for the build system (`setup.py`, `scripts/setuplib.py`) go in
  `scripts/tests/`, named by the same rule. Runtime testcases use the same name as their pytest
  counterpart.
- Before creating a test file, look for the existing one for that module and extend it.
- A test that spans several files goes in the file for the most important one. Split a large file
  by aspect with a suffix (`test_display_tts_prism_native.py`), keep shared harness code in
  `conftest.py` or a helper module, and add section comments to files over about 250 lines.

Quality:

- Assert behavior that games, saves, or callers depend on: results, state, exceptions, ordering.
  Do not assert constants, private attributes, mock call counts, log wording, or the internal
  layout of renders and AST nodes.
- Mock only a collaborator the code needs (clock, filesystem, threads, native libraries, network).
  If a test patches most of the code path it claims to cover, it is testing the mocks; move it to
  a runtime testcase or drive the real code instead.
- Do not write tests that pass whether or not the code works: asserting that nothing raised,
  restating a constant, or testing the test harness. Use `pytest.mark.parametrize` rather than
  near-duplicate functions.
- A test must fail or skip loudly when its required resource is missing; do not let it pass
  vacuously. Tests that need native libraries, a GPU driver, or non-redistributable assets skip
  with an explicit reason.
- Do not make checks pass by skipping, deleting, or weakening tests, loosening assertions, or
  special-casing test inputs, unless the task is to change the test. A test that checks
  implementation details rather than the intended contract may be changed; say so in the final
  response.
- Before reporting a task as done, run the relevant tests and report any that could not run.

## Python Tests

The Python tests use pytest and pytest-mock, installed by `uv sync` as dev dependencies. Engine tests live in
[testcases/pytests/](../../testcases/pytests/); tests for tools in `scripts/` and for the build system (`setup.py`,
`scripts/setuplib.py`) live in [scripts/tests/](../../scripts/tests/) and run without engine initialization or compiled
extensions. Default pytest discovery includes only engine tests; run the tool suite explicitly.

```sh
uv run pytest                                   # engine Python tests (default)
uv run pytest scripts/tests                      # script tools, without engine startup
uv run pytest testcases/pytests                   # engine Python tests
uv run pytest testcases/pytests/test_display_predict.py  # one module
uv run pytest -k <expression>                   # tests matching an expression
uv run pytest -m prism_native                   # native Prism TTS tests (opt-in, need libprism)
uv run ruff check <changed-files>
```

For engine tests, [testcases/pytests/conftest.py](../../testcases/pytests/conftest.py) starts the engine once, before test
modules are imported, so tests import engine names directly. Never call `renpy.import_all()` in a test: engine
startup runs once per process and records the reload backup. Keep that startup confined to the engine suite; do not
import its conftest from tool tests. Copy setup from the nearest existing test.

- Write plain `test_*` functions with bare `assert`, `pytest.raises`, and
  `@pytest.mark.parametrize`. Do not use `unittest.TestCase`.
- Patch with pytest-mock's `mocker` fixture and put setup in fixtures (teardown after `yield`), so
  patched globals are restored. Keep fixtures in the test module unless several modules
  share them; shared fixtures go in `conftest.py`.
- Give every test function a docstring that explains what it tests and anything non-obvious about
  it: why something is patched, why an input or edge case matters, timing or threading assumptions,
  what an unusual assertion guards against, and why it skips. Give fixtures and helpers a docstring
  when their purpose or teardown is not obvious.

## Runtime testcases ([testcases/game/tests/](../../testcases/game/tests/))

Ren'Py has its own test language (`testsuite`, `testcase`, `run`, `click`, `advance until`, ...),
documented in [testcases.rst](../../sphinx/source/testcases.rst). When adding coverage for user-visible
behavior (display, input, screens, statements), use runtime testcases rather than relying only
on Python tests.

- **Placement.** Use a testcase only when the behavior needs the running game: the interaction
  loop, rendering, input, script or screen execution, rollback, or save/load. Logic that can be
  exercised after engine initialization (parsers, data structures, task scheduling, engine
  internals with mocked collaborators) belongs in [testcases/pytests/](../../testcases/pytests/).
- **Write testcases in the test language.** Drive the game with test statements (`run`, `click`,
  `advance`, `pause`, `type`, ...) and check results with `assert` or `assert eval`. Keep `$` and
  `python` lines to small setup and state inspection. A testcase whose body is a single
  `$ helper()` call into Python that does the whole test is a Python test in disguise: move it to
  `testcases/pytests/`, or, if it needs the running game, split it into test-language steps. Replace
  loops over inputs with `parameter` properties ([parameterized tests](../../sphinx/source/testcases.rst)).

Tests are named `<suite>.<case>`:

```sh
./scripts/run-headless.sh testcases test                                    # all
./scripts/run-headless.sh testcases test particle.snowblossom_menu_return --report-detailed
```

A filter matching nothing is an error. Options are defined in
[renpy/test/testcli.py](../../renpy/test/testcli.py); do not guess flags. Success means the runner's
report shows passes and the process exited 0 — launching the game is not a pass.

After the last test, the game quits with status 1 if a test failed and 0 otherwise. `--persist` (or
`config.persist_after_tests = True`) keeps it open for a human instead; never pass it in unattended runs, where it
looks like a hang after `Status: PASSED`. An `exit` test statement quits immediately, overriding `--persist`.

To skip the main menu in a test game, define a `main_menu` label that returns, so the game goes straight to
`label start`:

```
label main_menu:
    return
```
