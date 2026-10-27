# Ren'Py agent guide

This checkout is the Ren'Py **engine**, not a game. It contains the engine (`renpy/`), the
launcher (itself a Ren'Py game), and bundled games. Changes ship to thousands of existing games,
so compatibility with existing scripts, saves, and compiled files matters more than elegance.

Run commands from the repository root.

## Pull requests, issues, and commits

These rules apply when opening or updating upstream pull requests, issues, or commits (not to
implementing local changes requested by the user in an interactive session).

- **Require substantial human input before opening a pull request.** A human must have directed
  the design and reviewed and understood the code and its impact
  ([contribution policy](README.rst#efficiency-tools-including-language-models)). For changes
  developed without substantial human input, open an issue describing the problem and preferred
  solution instead of a pull request, and leave implementation to the maintainers.
- **Describe the human review.** In pull requests and issues, state what a human read, tested, or
  decided, and what the agent produced without review. Use the "Human Oversight" section of the
  [pull request template](.github/pull_request_template.md); do not imply review that did not occur.
- **Choose the correct target branch.** Fixes and documentation target `fix`; features and risky
  internal changes target `master`. Contribution branches are named `work/<username>/...`
  ([branch policy](README.rst#branches)).
- **Credit only humans in commits.** Never include a `Co-authored-by` trailer for an AI agent or
  other non-human entity, even if tooling adds one automatically.

## Code map

| What | Where |
| --- | --- |
| Startup | [renpy.py](renpy.py) → [renpy/bootstrap.py](renpy/bootstrap.py) → [renpy/main.py](renpy/main.py); module import order and reload in [renpy/\_\_init\_\_.py](renpy/__init__.py) |
| Script language | [lexer.py](renpy/lexer.py), [parser.py](renpy/parser.py) → [ast.py](renpy/ast.py) nodes; loading/`.rpyc` in [script.py](renpy/script.py); running in [execution.py](renpy/execution.py) |
| User-defined statements (CDS) | [renpy/statements.py](renpy/statements.py); many "built-in" statements are CDS in [renpy/common/000statements.rpy](renpy/common/000statements.rpy) |
| Python in scripts, stores | [renpy/python.py](renpy/python.py), [renpy/defaultstore.py](renpy/defaultstore.py), [renpy/pyanalysis.py](renpy/pyanalysis.py) |
| Public `renpy.*` API | [renpy/exports/](renpy/exports/) (`*exports.py` modules, re-exported by name in `__init__.py`) |
| Config variables | [renpy/config.py](renpy/config.py), documented in [config.rst](sphinx/source/config.rst) |
| Engine code written in Ren'Py | [renpy/common/](renpy/common/) `.rpy`/`_ren.py` (actions, preferences, compat, GUI defaults, statements) |
| ATL | [renpy/atl.py](renpy/atl.py), [renpy/display/transform.py](renpy/display/transform.py) |
| Screen language | [renpy/sl2/](renpy/sl2/) (`slparser`, `slast`, `sldisplayables`), runtime in [renpy/display/screen.py](renpy/display/screen.py) |
| Displayables, interaction loop | [renpy/display/](renpy/display/) (`displayable.py`, `core.py`, `layout.py`, `behavior.py`, `render.pyx`, `predict.py`) |
| GPU renderer, text, audio | [renpy/gl2/](renpy/gl2/), [renpy/text/](renpy/text/), [renpy/audio/](renpy/audio/) |
| Saves, persistent, rollback | [loadsave.py](renpy/loadsave.py), [persistent.py](renpy/persistent.py), [rollback.py](renpy/rollback.py), [revertable.py](renpy/revertable.py), [compat/pickle.py](renpy/compat/pickle.py) |
| SDL3 bindings, C code | [renpy/pygame/](renpy/pygame/) (Cython, imported as `renpy.pygame`), [src/](src/) |
| Native build | [setup.py](setup.py), [scripts/setuplib.py](scripts/setuplib.py), [run.sh](run.sh) |
| Launcher | [launcher/game/](launcher/game/) |
| New-project template | [gui/](gui/) (copied into new games; edits do not reach existing games) |
| Bundled games | [tutorial/](tutorial/), [the_question/](the_question/) |
| Tests | [testcases/pytests/](testcases/pytests/) (pytest), [testcases/](testcases/) (Ren'Py testcase project), runner in [renpy/test/](renpy/test/) |
| Docs | [sphinx/source/](sphinx/source/) |

Untracked local directories such as `lib/`, `web/`, `vscode/`, `tmp/`, `scratch/`, `c/`, `cg/`, and
`*-dists/` are build or personal artifacts; do not edit or search them for engine code. Ignore
stray `.pyc`/`.pyo`/`.rpyc` files.

## How Ren'Py runs

Read this before changing engine behavior; most Ren'Py bugs come from violating one of these.

1. **Loading.** Every `.rpy` and `_ren.py` file in the game and in `renpy/common/` is parsed into
   AST nodes and pickled to `.rpyc` (with [renpy/compat/pickle.py](renpy/compat/pickle.py)). Later
   runs load `.rpyc` when the source is unchanged, and released games may ship only `.rpyc`.
   So **AST classes are a persisted file format**.

   A `_ren.py` file (e.g. [renpy/common/00db_ren.py](renpy/common/00db_ren.py)) is Ren'Py script
   written as Python ([ren_py.rst](sphinx/source/ren_py.rst)). Everything before the first `"""renpy`
   block is ignored by Ren'Py and only exists for editors and type checkers (imports, stub
   assignments). Each `"""renpy` … `"""` block holds Ren'Py statements, usually `init python:`, and
   the Python after it becomes that statement's indented body. So the code runs in a Ren'Py store,
   not as an importable module, and gets the same revertable rewriting as other script Python.
   Both delimiters must start at column 0, and `x_ren.py` conflicts with `x.rpy` in the same
   directory.
2. **Init phase.** `init` blocks, `define`, `image`, `screen`, `transform`, `style`, and `init python`
   run once, ordered by init priority (engine common files use negative priorities such as
   `init -1500`). `default` values are set when a game starts or a save loads. Displayables may not
   be rendered during init.
3. **Config locks after init.** `config.*` is a proxy ([defaultstore.py](renpy/defaultstore.py));
   after init, setting an unknown name raises. Treat config as init-time unless its docs say it can
   change at runtime. Engine code must not change config variables after the end of the init
   phase (resolving defaults in `renpy.config.post_init()` is part of it), even temporarily. When
   engine code needs to override or update a setting at runtime, copy it into module-level or
   thread-local state at the end of init (e.g. `renpy.display.im.thread_local`) and change that.
4. **Stores.** Script Python runs in `store` (`renpy.store`) or named stores such as `store.gui`.
   Engine variables visible to games use a leading `_` (e.g. `_window`, `_rollback`) so they do not
   collide with game names. Variables set with `define`, and stores with `_constant = True`, are
   constants: not saved and not rolled back, so they must not be mutated after init. Script code
   sees `renpy` as `renpy.exports`.
5. **Game phase.** A [Context](renpy/execution.py) (`renpy.game.context()`) walks AST nodes by
   calling `Node.execute()`. Statements that wait for the player call `renpy.ui.interact()`, which
   runs `Interface.interact` in [core.py](renpy/display/core.py): show screens, render, handle
   events, loop until a displayable returns a value. The game menu and `renpy.call_in_new_context`
   run in a new context pushed on top of the current one.
6. **Rollback.** Say and menu statements create checkpoints (`renpy.exports.checkpoint`). Rollback
   restores store variables and objects derived from [revertable.py](renpy/revertable.py) types.
   Script Python is rewritten by `WrapNode` in [python.py](renpy/python.py) so list/dict/set
   literals and classes become revertable;
   **engine `.py` code is not rewritten**, so engine objects stored in the store must use revertable
   types explicitly (or be immutable).
7. **Saves** pickle the store, rollback log, contexts, and the shown scene lists — which include
   displayable and transform objects. **Displayable classes are therefore save-format classes.**
8. **Rendering.** `Displayable.render(width, height, st, at)` returns a `Render`; `event()` handles
   input; `visit()` lists children (used by prediction and by `visit_all`, which calls
   `per_interact()` on every displayable each interaction).
   `renpy.display.render.render()` caches renders, so `render` may not be called each frame and a
   returned `Render` must not be modified. Request redraws with `renpy.display.render.redraw(d, delay)`
   and use `renpy.display.render.invalidate(d)` when cached output is stale.
9. **Prediction.** Ren'Py predicts upcoming statements (`Node.predict`) and screens
   (`renpy.display.predict.predicting` is True) to preload images. Screen code, displayable
   constructors, and `visit()` can run during prediction, repeatedly, or for screens never shown.
10. **Screens.** sl2 parses screens into `slast` nodes, analyzes which expressions are constant
    ([pyanalysis.py](renpy/pyanalysis.py)), and reuses displayables between updates. Screen
    expressions are re-evaluated often; state changes belong in actions (`renpy/common/00action_*.rpy`).
11. **Reload (Shift+R).** [renpy/\_\_init\_\_.py](renpy/__init__.py) `Backup` pickles every `renpy.*`
    module's globals after import and restores them on reload. New module-level globals must be
    picklable, or the module/name must be added to the blacklists there. Do not keep state that
    must survive reload in module globals; `renpy.session` exists for that.

## Compatibility rules

These are the changes that break real games. Check each one that applies.

- **Assess compatibility for every behavior change.** Add a compat switch when existing games
  reasonably depend on the old behavior; ordinary bug fixes do not automatically need one.
  If a switch is needed, add a variable to [renpy/config.py](renpy/config.py) with the new behavior
  as default, restore the old value for older games in `_set_script_version` in
  [renpy/common/00compat.rpy](renpy/common/00compat.rpy) (`if version <= (X, Y, 99):` or a point
  release tuple, newest first — use the latest release series at the top of that function, not the
  `8.99.99` placeholder in `pyproject.toml`), and document it in [config.rst](sphinx/source/config.rst).
  Document incompatible changes in
  [incompatible.rst](sphinx/source/incompatible.rst), and mention features in
  [changelog.rst](sphinx/source/changelog.rst). Follow existing entries as templates.
- **AST/`.rpyc` format.** Nodes in [ast.py](renpy/ast.py), [atl.py](renpy/atl.py), and
  [sl2/slast.py](renpy/sl2/slast.py) are pickled. `ast.py` nodes use [cslots](renpy/cslots.pyx): an
  annotated class attribute is a slot whose class value is its default. In every case, give a new
  field a class-level default that reproduces old behavior so old `.rpyc` files load. Do not rename
  or move node classes or their modules. Do not change how statements are named; saves refer to the
  current statement by node name.
- **Saved objects.** Classes in saves (displayables, transforms, characters, actions, store
  objects, anything in `renpy.revertable`) must stay importable under the same module and class
  name. For a new attribute, add a class-level default so old saves load. For larger changes,
  [renpy.object.Object](renpy/object.py) provides `__version__` + `after_upgrade`, `nosave`, and
  `after_setstate`. Never store open files, threads, surfaces/textures, generators, lambdas, or local
  functions on saved objects. `renpy.compat.pickle.find_bad_reduction` locates unpicklable values.
- **Rollback.** `NoRollback`/`SlottedNoRollback` ([rollback.py](renpy/rollback.py)) only opt out
  of rollback; such objects are still saved and must still pickle. Persistent data
  ([persistent.py](renpy/persistent.py)) detects changes via equality and deepcopy, so persistent
  values need sane `__eq__`.
- **Public API.** A new `renpy.*` function goes in a `renpy/exports/*exports.py` module **and** in
  the explicit import list in [renpy/exports/\_\_init\_\_.py](renpy/exports/__init__.py). Do not
  rename, remove, or reorder positional arguments of `renpy.*` functions, config variables, actions,
  screen properties, statement syntax, or `store` names; add keyword arguments instead. Unused-looking
  imports in `renpy/exports/` and `renpy/defaultstore.py` are often public on purpose.
- **Control-flow exceptions.** Jump, call, quit, restart, and replay end are `Exception` subclasses
  listed in `renpy.game.CONTROL_EXCEPTIONS`. Any `except Exception` that can surround script,
  Python, or interaction code must re-raise them first: `except renpy.game.CONTROL_EXCEPTIONS: raise`.
  Rollback uses `RollbackException`/`UnfreezeException` (`BaseException`), so never use bare
  `except:` or `except BaseException` there either.
- **Engine `.rpy` files** in `renpy/common/` run in every game. Prefix new store names with `_` (or
  use a named store), give new init blocks a priority consistent with the file, and remember games
  may override screens, styles, and `config` values they define.

## Conventions

- Python 3.12 only ([pyproject.toml](pyproject.toml)); Ruff line length 120;
  Many files still start with `from __future__ ...` and `from renpy.compat import ...` lines; keep
  them in files that have them and match the file's existing style. Do not reformat files.
- Engine modules mostly `import renpy` and call fully qualified names
  (`renpy.display.render.render(...)`). Prefer this for engine modules: it avoids import cycles, and
  module import order is fixed in `import_all` in [renpy/\_\_init\_\_.py](renpy/__init__.py). A new
  module must be imported there, and then registered in the `TYPE_CHECKING` blocks of
  [renpy/\_\_init\_\_.py](renpy/__init__.py) and package `__init__.py` files by running
  `uv run python scripts/relative_imports.py`.
- Keep the MIT copyright header on source files; copy it from a neighboring file for new files.
- API reference docs are generated from docstrings tagged `:doc: <section>` (format in
  [README.rst](README.rst#format)). When changing a documented function, update its docstring; when
  adding one, tag it so it appears in the docs.
- `.pyx`/`.pxd` are Cython. Changing a `.pxd` or a `cdef` signature requires rebuilding all
  dependent extensions (`./run.sh --build` handles it; use `./run.sh --clean --build` if modules
  were removed or stale `.so`/`tmp/gen` artifacts persist). When changing Cython signatures or
  classes, regenerate git-ignored `.pyi` stubs after building with
  `uv run python scripts/generate_pyi.py`.

## Generated or vendored: do not hand-edit

| Path | Source of truth |
| --- | --- |
| `sphinx/source/inc/` | Docstrings with `:doc:` tags; regenerated by the docs build |
| `doc/`, `doc-web/` | Sphinx output |
| `renpy/styledata/style_*functions.pyx`, `styleclass.pyx`, `stylesets.py`, `styleconstants.pxd` | [scripts/generate_styles.py](scripts/generate_styles.py), run by `setup.py` |
| `.pyi` files starting with `# Generated by scripts/generate_pyi.py` | [scripts/generate_pyi.py](scripts/generate_pyi.py) (git-ignored; run after `./run.sh --build`; hand-written `.pyi` exist too, so check the header) |
| `renpy/display/matrix_functions.pxi` | [scripts/generate_matrix_functions.py](scripts/generate_matrix_functions.py) |
| `renpy/uguu/gl.pyx`, `renpy/uguu/gl.pxd`, `renpy/uguu/uguu.pyx` | `scripts/uguu/*.in` via [scripts/uguu/xml_to_pyx.py](scripts/uguu/xml_to_pyx.py) |
| `renpy/gl2/gl2functions.py` | [scripts/uguu/generate_required_functions.py](scripts/uguu/generate_required_functions.py) |
| `renpy/pygame/sdl.pxd`, `renpy/pygame/sdl_image.pxd` | [scripts/sdl3/main.py](scripts/sdl3/main.py) ([scripts/sdl3/generate.sh](scripts/sdl3/generate.sh)) |
| `renpy/text/emoji_trie.py`, `renpy/text/linebreak.pxi` | [scripts/unicode/make_emoji_trie.py](scripts/unicode/make_emoji_trie.py), [scripts/unicode/generate_linebreak.py](scripts/unicode/generate_linebreak.py) |
| `src/Setup`, `src/Setup.tfd` | `generate_setup_files()` in [scripts/setuplib.py](scripts/setuplib.py), run by `setup.py` |
| Text below `# Generated by scripts/relative_imports.py` in `__init__.py` files | [scripts/relative_imports.py](scripts/relative_imports.py) |
| `cubism/`, `src/libhydrogen/`, `src/tinyfiledialogs/` | Vendored third-party code |
| `*.rpyc`, `*.so`, `tmp/` | Build output |
| `launcher/game/tl/`, `*/game/tl/` | Translations, maintained by translators; leave them unless the task is about translations |

## Build, run, and test

The project uses `uv`. `uv sync` creates `.venv`; `run.sh` uses `$RENPY_VIRTUAL_ENV`, else an active
virtualenv, else `.venv`, and fails if none exists. Native builds need the `sdl3` and `sdl3-image`
pkg-config packages plus the libraries in [setup.py](setup.py); the SDL2 list in README.rst is out
of date.

```sh
./run.sh --build                      # rebuild changed Cython/C extensions, don't launch
./run.sh --clean --build              # delete compiled .so files and tmp/gen, then rebuild
./run.sh                              # rebuild, then open the launcher
./run.sh <project-dir>                # rebuild, then run a game (e.g. tutorial, the_question, testcases)
./run.sh <project-dir> lint --error-code  # Ren'Py's script linter; nonzero exit on lint errors
./run.sh <project-dir> compile        # compile scripts to .rpyc without running
./scripts/run-headless.sh <args>      # same arguments as run.sh, on a virtual display with dummy audio
```

`run.sh` rebuilds stale extensions before every launch; Python-only edits need no build step.
`run-headless.sh` needs Weston, `xvfb-run`, or `Xvfb`; read the script if it fails.

Lint the affected project (e.g. `launcher`, `tutorial`, or `the_question`), not always `testcases`.
Lint skips common-script nodes in its main statement checks, so linting a game does not replace
runtime coverage of changes in `renpy/common/`.

### When to add or update tests

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
  persistent-restart, or schema checks [listed below](#which-checks-to-run) when applicable.
- If required automated coverage is impractical, report the specific reason, manual validation
  performed and its result, and the remaining regression risk. If manual validation is also
  unavailable, explicitly report the unverified path; do not present the change as validated.

### Python Tests ([testcases/pytests/](testcases/pytests/))

The Python tests use pytest and pytest-mock, installed by `uv sync` as dev dependencies.

```sh
uv run pytest                                   # all
uv run pytest testcases/pytests/test_prediction.py  # one module
uv run pytest -k <expression>                   # tests matching an expression
uv run ruff check <changed-files>
```

[testcases/pytests/conftest.py](testcases/pytests/conftest.py) starts the engine once, before test
modules are imported, so tests import engine names directly. Never call `renpy.import_all()` in a
test: engine startup runs once per process and records the reload backup. Copy setup from the nearest
existing test.

- Write plain `test_*` functions with bare `assert`, `pytest.raises`, and
  `@pytest.mark.parametrize`. Do not use `unittest.TestCase`.
- Patch with pytest-mock's `mocker` fixture and put setup in fixtures (teardown after `yield`), so
  patched engine globals are restored. Keep fixtures in the test module unless several modules
  share them; shared fixtures go in `conftest.py`.
- Give every test function a docstring that explains what it tests and anything non-obvious about
  it: why something is patched, why an input or edge case matters, timing or threading assumptions,
  what an unusual assertion guards against, and why it skips. Give fixtures and helpers a docstring
  when their purpose or teardown is not obvious.

### Runtime testcases ([testcases/game/tests/](testcases/game/tests/))

Ren'Py has its own test language (`testsuite`, `testcase`, `run`, `click`, `advance until`, ...),
documented in [testcases.rst](sphinx/source/testcases.rst). When adding coverage for user-visible
behavior (display, input, screens, statements), use runtime testcases rather than relying only
on Python tests.

- **Placement.** Use a testcase only when the behavior needs the running game: the interaction
  loop, rendering, input, script or screen execution, rollback, or save/load. Logic that can be
  exercised after engine initialization (parsers, data structures, task scheduling, engine
  internals with mocked collaborators) belongs in [testcases/pytests/](testcases/pytests/).
- **Write testcases in the test language.** Drive the game with test statements (`run`, `click`,
  `advance`, `pause`, `type`, ...) and check results with `assert` or `assert eval`. Keep `$` and
  `python` lines to small setup and state inspection. A testcase whose body is a single
  `$ helper()` call into Python that does the whole test is a Python test in disguise: move it to
  `testcases/pytests/`, or, if it needs the running game, split it into test-language steps. Replace
  loops over inputs with `parameter` properties ([parameterized tests](sphinx/source/testcases.rst)).

Tests are named `<suite>.<case>`:

```sh
./scripts/run-headless.sh testcases test                                    # all
./scripts/run-headless.sh testcases test particle.snowblossom_menu_return --report-detailed
```

A filter matching nothing is an error. Options are defined in
[renpy/test/testcli.py](renpy/test/testcli.py); do not guess flags. Success means the runner's
report shows passes and the process exited 0 — launching the game is not a pass.

### Which checks to run

Run the applicable checks below. Decide whether missing coverage requires a new or extended test
using [When to add or update tests](#when-to-add-or-update-tests); report unavailable validation.

| Change | Run |
| --- | --- |
| Engine Python | Related Python tests, full `uv run pytest`, `ruff check` on changed files |
| Statements, screens, display, input, ATL | The above plus relevant runtime testcases |
| Project `.rpy` or `_ren.py` | `./run.sh <affected-project-dir> lint --error-code` plus related runtime testcases |
| Scripts in `renpy/common/` | Relevant runtime testcases; lint an affected project with `--error-code` for integration issues, not coverage of common-script nodes |
| Cython/C | `./run.sh --build` (and `uv run python scripts/generate_pyi.py` if signatures changed), then the above |
| Saves | Save and load the affected state through Ren'Py; verify restored values and behavior |
| Rollback | Mutate the affected state across a checkpoint, roll back, and verify restoration and subsequent execution |
| Persistent data | Change the affected value, save persistent data, restart, and verify that the change survives |
| Saved-object or AST/`.rpyc` schema | In addition to affected runtime checks, save/pickle with the old shape and load with the new; verify compatibility defaults or migration |
| RST or `:doc:` docstrings | `(cd sphinx && ./build.sh)` when the engine runs; it rewrites `sphinx/source/inc/`, `doc/`, and `doc-web/` |

## Pitfalls

| Symptom | Likely cause |
| --- | --- |
| `config.x is not a known configuration variable` | Variable not defined in [renpy/config.py](renpy/config.py) |
| Old saves or `.rpyc` fail to load, `AttributeError` on load | New attribute without a class-level/slot default |
| A change works until the player rolls back | Engine code stored a plain `list`/`dict`/object in the store instead of a revertable type |
| `Cannot pickle renpy.x = ...` printed at startup | Unpicklable module global; see reload backup in [renpy/\_\_init\_\_.py](renpy/__init__.py) |
| Jump/call/quit silently ignored | A broad `except` swallowed a control-flow exception |
| Displayable shows stale content | Cached render; call `renpy.display.render.redraw` or `invalidate` |
| Side effect happens at odd times or twice | Code ran during prediction or screen re-evaluation |
| Edit to `sphinx/source/inc/` or `doc/` disappeared | Generated file; edit the docstring or `sphinx/source/*.rst` instead |
| `ImportError` for a `.so` module, or Cython signature mismatch | Extensions out of date; run `./run.sh --build` (or `./run.sh --clean --build` if stale `.so`/`tmp/gen` files remain) |
| `run.sh`: "Please use 'uv sync'" | No virtualenv; run `uv sync` |

## Maintaining this file

This file is loaded automatically by agents of varying capability. Keep it Ren'Py-specific (no
generic coding advice), literal, and verified against the code; update it when a path, command, or
rule here changes. [CLAUDE.md](CLAUDE.md) only imports this file.
