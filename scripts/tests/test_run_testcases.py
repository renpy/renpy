# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Regression tests for the functional test runner's classification, failure reporting, and Wine cleanup."""

import os
import shlex
import shutil
import subprocess
import sys
import threading
from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from scripts import run_testcases

# Run a project with simulated child output and an exit code, without executing a command.
SimulatedProject = Callable[[str, int], run_testcases.Result]

# ConsoleReporter suppresses expected-failure diagnostics, but arbitrary prints still reach the log. Both kinds
# of output are represented here, alongside failed assertions, multiline exceptions, screenshot errors, and hooks.
FAILED_OUTPUT = """\
[rpytest] Starting test run
[rpytest] Platform: test-platform
[rpytest] [exc] + global
[rpytest] [exc]   + example
[rpytest] [exc]     - passing
PASS-NOISE
[rpytest] [exc]     - passing (0.1 s)
[rpytest] [exc]     - expected_failure
XFAIL-NOISE
[rpytest] [exc]     - expected_failure (0.1 s)
[rpytest] [exc]     - assertion_failure
FAILURE-NOISE
File "game/script.rpy", line 20, in global.example.assertion_failure
AssertionError: assert eval 3 == 4

Full traceback:
  File "game/script.rpy", line 20, in assertion_failure
    assert eval 3 == 4
RenpyTestAssertionError: failed assertion
During testcase execution:
  File "game/script.rpy", line 18, in testcase assertion_failure
    testcase assertion_failure:
====================
[rpytest] [exc]     - assertion_failure (0.1 s)
[rpytest] [exc]     - screenshot_failure
Full traceback:
RenpyTestScreenshotError: screenshot.png (pixel difference: 12 > 0)
Current image saved to screenshots/screenshot.new.png
Difference image saved to screenshots/screenshot.diff.png
During testcase execution:
  File "game/script.rpy", line 25, in testcase screenshot_failure
    screenshot "screenshot.png"
====================
[rpytest] [exc]     - screenshot_failure (0.1 s)
[rpytest] [exc]   + failed_setup
HOOK-NOISE
Full traceback:
ValueError: setup error line one
setup error line two
During testcase execution:
  File "game/script.rpy", line 30, in hook setup(0)
    raise ValueError("setup error line one\\nsetup error line two")
====================
[rpytest] Test outcomes (Detailed)
[rpytest] FAILED global
[rpytest]   FAILED example
[rpytest]     PASSED passing
[rpytest]     XFAILED expected_failure
[rpytest]     FAILED assertion_failure
[rpytest]     FAILED screenshot_failure
[rpytest]   FAILED failed_setup
[rpytest]     NOT RUN never_started
====================
[rpytest] Test outcomes (Summary)
[rpytest] Test cases : 5 | 1 passed | 1 xfailed | 2 failed | 0 xpassed | 0 skipped | 1 not run
[rpytest] Test hooks : 1 | 0 passed | 0 xfailed | 1 failed | 0 xpassed | 0 skipped | 0 not run
[rpytest] Test suites: 3 | 0 passed | 0 xfailed | 3 failed | 0 xpassed | 0 skipped | 0 not run
[rpytest] Status: FAILED
TRAILING-NOISE
"""


@pytest.mark.parametrize(
    ("status", "returncode", "cases", "expected"),
    [
        ("PASSED", 0, run_testcases.Counts(total=1, passed=1), "PASS"),
        ("XFAILED", 0, run_testcases.Counts(total=1, xfailed=1), "PASS"),
        ("XFAILED", 1, run_testcases.Counts(total=1, xfailed=1), "FAIL"),
        ("FAILED", 1, run_testcases.Counts(total=1, failed=1), "FAIL"),
        ("XPASSED", 1, run_testcases.Counts(total=1, xpassed=1), "FAIL"),
        ("SKIPPED", 0, run_testcases.Counts(total=1, skipped=1), "FAIL"),
        ("PASSED", 0, run_testcases.Counts(), "FAIL"),
    ],
)
def test_classify_completed_run(status: str, returncode: int, cases: run_testcases.Counts, expected: str) -> None:
    """Expected failures are successful outcomes, while process errors and runs with no tests still fail."""

    report = run_testcases.Report(cases, run_testcases.Counts(), run_testcases.Counts(), status=status)

    assert run_testcases.classify(returncode, report) == expected


def test_classify_missing_summary() -> None:
    """An exit code of zero alone cannot establish that tests ran to completion."""

    assert run_testcases.classify(0, None) == "CRASH"


@pytest.mark.parametrize("name", [".", ".."])
def test_parse_target_rejects_directory_names(name: str) -> None:
    """
    A target's name is a directory under the staging directory, which is deleted from. These two names are made of
    allowed characters, but name the staging directory or its parent, which hold every target's files.
    """

    with pytest.raises(run_testcases.ConfigError, match="isn't allowed"):
        run_testcases.parse_target(name, {"type": "local"}, {})


def test_updater_runs_by_default_and_takes_arguments() -> None:
    """
    The updater test is selected like a project, and runs last when nothing is selected. What follows -- is specific
    to one project, so it's refused when several are selected, and accepted for the updater test alone, where it
    holds that test's arguments rather than test filters.
    """

    assert run_testcases.select_projects(None, [])[-1] == run_testcases.UPDATER
    assert run_testcases.select_projects("updater,tutorial", []) == ["updater", "tutorial"]
    assert run_testcases.select_projects("updater", ["--version", "8.6.1"]) == ["updater"]

    with pytest.raises(run_testcases.ConfigError, match="exactly one"):
        run_testcases.select_projects("updater,tutorial", ["--version", "8.6.1"])


def test_run_target_passes_arguments_to_updater(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    When the updater test is all that's selected, what followed -- on the command line reaches it, so that
    `-p updater -- --version 8.6.1` picks the SDK to update. The updater test is replaced, as it would download an
    update.
    """

    target = run_testcases.Target("linux", "local")
    run_default = mocker.patch.object(run_testcases.load_updater_test(), "run_default", return_value=[])

    run_testcases.run_target(target, ["updater"], 0, ["--version", "8.6.1"], tmp_path)

    assert run_default.call_args.args[3] == ["--version", "8.6.1"]


def test_synopsis_counts_expected_failure_as_success() -> None:
    """
    An expected failure, which is what the updater test reports when its SDK hasn't been built, is shown with its
    reason but doesn't fail the run. A real failure beside it still does.
    """

    passed = run_testcases.Result("linux", "tutorial", "PASS")
    expected = run_testcases.Result("linux", "updater", "XFAIL", detail="dl/8.6.2 doesn't exist.")
    failed = run_testcases.Result("linux", "launcher", "FAIL", detail="exit status 1")

    synopsis = run_testcases.format_synopsis([passed, expected])

    assert "OVERALL: PASS (1/2 test runs passed, 1 failed as expected)" in synopsis
    assert "Expected failures:\n  linux/updater: dl/8.6.2 doesn't exist." in synopsis
    assert "Failures:" not in synopsis.replace("Expected failures:", "")

    assert "OVERALL: FAIL" in run_testcases.format_synopsis([passed, expected, failed])


def test_updater_test_shares_this_module() -> None:
    """
    The updater test has to use the same run_testcases module that's running it. A second copy would have its own
    `cancelled` event, so interrupting the run wouldn't stop an update.
    """

    assert run_testcases.load_updater_test().run_testcases is run_testcases


def test_run_target_runs_updater_without_syncing(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    When only the updater test is selected, the target's tree isn't synced, as the updater test unpacks a Ren'Py of
    its own. sync_target is patched to fail the test if it's called, and the updater test itself is replaced, as it
    would download an update.
    """

    target = run_testcases.Target("linux", "local")
    result = run_testcases.Result("linux", "updater", "PASS")

    mocker.patch.object(run_testcases, "sync_target", side_effect=AssertionError("The target was synced."))
    mocker.patch.object(run_testcases.load_updater_test(), "run_default", return_value=[result])

    assert run_testcases.run_target(target, ["updater"], 0, [], tmp_path) == [result]


def test_project_target_pairs_overlap(mocker: MockerFixture, tmp_path: Path) -> None:
    """All four runs must reach the barrier before any finishes, with stable report order and separate displays."""
    barrier = threading.Barrier(4)

    def run_pair(
        target: run_testcases.Target, project: str, index: int, filters: list[str], directory: Path, support: Path
    ) -> run_testcases.Result:
        barrier.wait(timeout=5)
        return run_testcases.Result(target.name, project, "PASS", detail=str(index))

    targets = [run_testcases.Target(name, "local") for name in ("one", "two")]
    mocker.patch.object(run_testcases, "make_results_directory", return_value=tmp_path)
    mocker.patch.object(run_testcases, "sync_target", return_value=None)
    mocker.patch.object(run_testcases, "run_project", side_effect=run_pair)

    projects = ["tutorial", "launcher"]
    results = run_testcases.run_all(targets, projects, [], False)
    assert [(r.name, r.project, r.status) for r in results] == [(t.name, p, "PASS") for t in targets for p in projects]
    assert len({r.detail for r in results}) == 4


def test_run_target_keeps_project_results_when_updater_breaks(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    An unexpected exception from the updater test must not replace the results of concurrent projects,
    which may have taken a long time to get. It becomes an error of the updater test alone. The projects and the
    updater test are replaced, as this is about how their results are combined.
    """

    target = run_testcases.Target("linux", "local")
    passed = run_testcases.Result("linux", "tutorial", "PASS")

    mocker.patch.object(run_testcases, "sync_target", return_value=None)
    mocker.patch.object(run_testcases, "run_project", return_value=passed)
    mocker.patch.object(run_testcases.load_updater_test(), "run_default", side_effect=RuntimeError("broken"))

    results = run_testcases.run_target(target, ["tutorial", "updater"], 0, [], tmp_path)

    assert results[0] is passed
    assert [(r.project, r.status) for r in results[1:]] == [("updater", "ERROR")]
    assert "broken" in results[1].detail


@pytest.mark.skipif(os.name != "posix", reason="The source runner launches projects through POSIX shell scripts.")
def test_source_build_failure_stops_all_projects(mocker: MockerFixture, tmp_path: Path) -> None:
    """Both projects report a failed shared build, and a custom runtime can still skip this preparation."""
    mocker.patch.object(run_testcases, "REPO", tmp_path)
    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path)
    build = tmp_path / "run.sh"
    build.write_text("#!/bin/sh\necho build attempted\nexit 42\n")
    build.chmod(0o755)
    target = run_testcases.Target("source", "source")
    results_dir = tmp_path / "results"

    results = run_testcases.run_target(target, ["tutorial", "the_question"], 0, [], results_dir)

    assert [r.status for r in results] == ["ERROR", "ERROR"]
    assert all("build failed with exit status 42" in r.detail for r in results)
    assert (results_dir / "support.txt").read_text().splitlines() == ["build attempted"]
    target.command = "alternate-runtime"
    assert run_testcases.sync_target(target, tmp_path / "custom.txt") is None


@pytest.mark.parametrize("command", [None, "./scripts/run-headless.sh"])
@pytest.mark.skipif(os.name != "posix", reason="The source runner launches projects through POSIX shell scripts.")
def test_source_xvfb_displays_are_distinct(tmp_path: Path, command: str | None) -> None:
    """Run the real headless wrapper with an Xvfb probe to check the display chosen for each project."""
    for tool in ("bash", "dirname"):
        executable = shutil.which(tool)
        assert executable
        (tmp_path / tool).symlink_to(executable)
    xvfb = tmp_path / "xvfb-run"
    xvfb.write_text('#!/bin/sh\nwhile [ "$1" != "-n" ]; do shift; done\necho "$2"\n')
    xvfb.chmod(0o755)
    target = run_testcases.Target("source", "source", command=command, headless=True, env={"PATH": str(tmp_path)})

    displays = [
        subprocess.check_output(["/bin/sh", "-c", run_testcases.build_launch(target, index)], cwd=run_testcases.REPO)
        for index in (0, 1)
    ]
    assert all(display.strip().isdigit() for display in displays)
    assert displays[0] != displays[1]


@pytest.mark.skipif(os.name != "posix", reason="The source runner launches projects through POSIX shell scripts.")
def test_custom_run_sh_builds_do_not_overlap(tmp_path: Path) -> None:
    """Concurrent wrapper launches share a build tree. The simulated setup fails if another build is writing."""
    shutil.copy2(run_testcases.REPO / "run.sh", tmp_path)
    (tmp_path / "setup.py").write_text(
        "from pathlib import Path\nimport time\n"
        'build = Path("build-active")\nbuild.mkdir()\ntime.sleep(0.25)\nbuild.rmdir()\n'
    )
    (tmp_path / "renpy.py").write_text('print("game launched")\n')
    target = run_testcases.Target(
        "source", "source", command="bash ./run.sh", env={"VIRTUAL_ENV": sys.prefix, "RENPY_VIRTUAL_ENV": ""}
    )
    processes = [
        subprocess.Popen(
            ["/bin/sh", "-c", run_testcases.build_launch(target, index)], cwd=tmp_path, stdout=subprocess.PIPE
        )
        for index in (0, 1)
    ]
    for process in processes:
        output, _ = process.communicate(timeout=15)
        assert process.returncode == 0
        assert output.strip() == b"game launched"


@pytest.fixture
def wine_environment(mocker: MockerFixture) -> None:
    """Restore the inherited environment after each test, including direct changes to WINEPREFIX."""

    mocker.patch.dict(os.environ)
    os.environ.pop("WINEPREFIX", None)


@pytest.mark.usefixtures("wine_environment")
@pytest.mark.skipif(os.name != "posix", reason="The runner launches targets through a POSIX shell.")
@pytest.mark.parametrize(
    ("inherited_prefix", "configured_prefix", "environment_prefix"),
    [
        (None, None, None),
        ("inherited", None, None),
        ("inherited", "configured", None),
        ("inherited", None, "environment"),
        ("inherited", "configured", "environment"),
    ],
)
def test_wine_cleanup_uses_launch_prefix(
    mocker: MockerFixture,
    tmp_path: Path,
    inherited_prefix: str | None,
    configured_prefix: str | None,
    environment_prefix: str | None,
) -> None:
    """
    Launch and cleanup must select the same prefix, including env overrides and inherited defaults.

    The launch command probes its real shell environment using Python instead of Wine. Cleanup is mocked so no
    Wine processes are started or terminated. The shell probe is skipped on non-POSIX hosts, where the runner's
    launch commands cannot run.
    """

    if inherited_prefix is not None:
        os.environ["WINEPREFIX"] = str(tmp_path / inherited_prefix)

    env = {"WINEPREFIX": str(tmp_path / environment_prefix)} if environment_prefix is not None else {}
    target = run_testcases.Target(
        name="wine-test",
        type="wine",
        env=env,
        wineprefix=str(tmp_path / configured_prefix) if configured_prefix is not None else None,
        command=shlex.join([sys.executable, "-c", "import os; print(os.environ.get('WINEPREFIX', 'default'))"]),
    )
    launch = subprocess.run(
        ["/bin/sh", "-c", run_testcases.build_launch(target, 0)],
        capture_output=True,
        text=True,
        check=True,
    )
    cleanup = mocker.patch.object(run_testcases, "run_logged", return_value=0)

    run_testcases.stop_wine(target, tmp_path / "cleanup.txt")

    cleanup.assert_called_once()
    assert cleanup.call_args.args[0] == ["wineserver", "-k"]
    assert cleanup.call_args.kwargs["env"].get("WINEPREFIX", "default") == launch.stdout.strip()


def test_parallel_wine_cleanup_waits_for_games(mocker: MockerFixture, tmp_path: Path) -> None:
    """A failed Wine game requests cleanup without stopping other jobs that still need its prefix."""

    events: list[str] = []
    target = run_testcases.Target(name="windows", type="wine")
    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path)
    mocker.patch.object(run_testcases, "run_logged", side_effect=lambda *args, **kwargs: events.append("stop prefix"))

    def run_games(
        target: run_testcases.Target,
        projects: list[str],
        index: int,
        filters: list[str],
        directory: Path,
        games: list[run_testcases.Game] | None = None,
        exit_suite: Path | None = None,
    ) -> list[run_testcases.Result]:
        """Simulate one game timing out while another is finishing on the same target."""
        run_testcases.stop_wine(target, directory / "support.txt")
        events.append("last game finished")
        return []

    mocker.patch.object(run_testcases, "run_target", side_effect=run_games)
    run_testcases.run_all([target], ["testcases", "tutorial"], [], False)

    assert events == ["last game finished", "stop prefix"]


@pytest.fixture
def simulated_project(mocker: MockerFixture, tmp_path: Path) -> SimulatedProject:
    """Feed captured subprocess output through the real project runner without executing commands or collecting files."""

    def run_project(output: str, returncode: int) -> run_testcases.Result:
        """Return the result of a project whose process emitted `output` and exited with `returncode`."""

        def write_output(_argv: list[str], log: Path, _timeout: float) -> int:
            """Simulate a child process writing to its output log."""

            log.write_text(output, encoding="utf-8")
            return returncode

        mocker.patch.object(run_testcases, "run_logged", side_effect=write_output)
        mocker.patch.object(run_testcases, "collect_artifacts")

        return run_testcases.run_project(
            run_testcases.Target(name="linux", type="source"),
            "testcases",
            0,
            [],
            tmp_path / "testcases",
            tmp_path / "support.txt",
        )

    return run_project


@pytest.mark.parametrize("line_ending", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("hide_execution", [False, True])
def test_synopsis_includes_unexpected_failure_diagnostics(
    simulated_project: SimulatedProject, line_ending: str, hide_execution: bool
) -> None:
    """Show assertions, multiline errors, screenshot paths and hidden hook failures, excluding progress and xfail output.

    Colored output and all line endings accepted from SSH ptys must produce the same useful details. Execution
    progress may be disabled, so diagnostic extraction must also work without per-test start/end markers.
    """

    output = FAILED_OUTPUT
    if hide_execution:
        output = "\n".join(line for line in output.splitlines() if not line.startswith("[rpytest] [exc]"))
    output = output.replace("[rpytest]", "\x1b[36m[rpytest]\x1b[0m").replace("\n", line_ending)
    result = simulated_project(output, 1)

    synopsis = run_testcases.format_synopsis([result])

    assert result.status == "FAIL"
    assert "linux/testcases: example.assertion_failure" in synopsis
    assert 'File "game/script.rpy", line 20' in synopsis
    assert "AssertionError: assert eval 3 == 4" in synopsis
    assert "RenpyTestScreenshotError: screenshot.png (pixel difference: 12 > 0)" in synopsis
    assert "screenshots/screenshot.new.png" in synopsis
    assert "screenshots/screenshot.diff.png" in synopsis
    assert "ValueError: setup error line one\n    setup error line two" in synopsis
    assert "hook setup(0)" in synopsis
    assert "During testcase execution:" in synopsis
    assert "expected_failure" not in synopsis
    assert "NOISE" not in synopsis
    assert "[rpytest]" not in synopsis
    assert "\x1b" not in synopsis


def test_synopsis_includes_crash_traceback_without_summary(simulated_project: SimulatedProject) -> None:
    """A crash may have no summary, but its traceback should still be visible without opening the log."""

    result = simulated_project(
        '[rpytest] Starting test run\n'
        'Full traceback:\n'
        '  File "game/script.rpy", line 10, in startup\n'
        '    initialize_game()\n'
        '  File "game/script.rpy", line 50, in initialize_game\n'
        '    raise RuntimeError("startup failure")\n'
        'RuntimeError: startup failure\n'
        '====================\n',
        1,
    )

    synopsis = run_testcases.format_synopsis([result])

    assert result.status == "CRASH"
    assert "Full traceback:" in synopsis
    assert 'File "game/script.rpy", line 10, in startup' in synopsis
    assert "RuntimeError: startup failure" in synopsis


def test_synopsis_omits_expected_failure_output(simulated_project: SimulatedProject) -> None:
    """A run containing only expected failures is successful and must not print their output as failure details."""

    result = simulated_project(
        '[rpytest] [exc] - expected_failure\n'
        'XFAIL-NOISE\n'
        '[rpytest] Test outcomes (Summary)\n'
        '[rpytest] Test cases : 1 | 0 passed | 1 xfailed | 0 failed | 0 xpassed | 0 skipped | 0 not run\n'
        '[rpytest] Status: XFAILED\n',
        0,
    )

    synopsis = run_testcases.format_synopsis([result])

    assert result.status == "PASS"
    assert "Failures:" not in synopsis
    assert "expected_failure" not in synopsis
    assert "XFAIL-NOISE" not in synopsis


# Games given with --game


def make_game(root: Path, name: str, script: str = 'label start:\n    return\n') -> Path:
    """Creates a minimal game directory named `name` under `root`, with `script` as its only script."""
    game = root / name
    (game / "game").mkdir(parents=True)
    (game / "game" / "script.rpy").write_text(script)
    return game


def test_load_games_detects_global_suite(tmp_path: Path) -> None:
    """
    A game that defines testsuite global, even in a subdirectory, a linked directory, or a _ren.py file, keeps its own
    teardown. An indented definition is a nested suite, not the global one. One that
    doesn't gets the exit suite, as it would otherwise stay open until the timeout.
    """

    plain = make_game(tmp_path, "plain")
    nested = make_game(tmp_path, "nested")
    (nested / "game" / "tests").mkdir()
    (nested / "game" / "tests" / "global.rpy").write_text("testsuite global:\n    teardown:\n        exit\n")
    ren_py = make_game(tmp_path, "ren_py")
    (ren_py / "game" / "suite_ren.py").write_text('"""renpy\ntestsuite global:\n    teardown:\n        exit\n"""\n')

    linked = make_game(tmp_path, "linked")
    (linked / "game" / "tests").symlink_to(nested / "game" / "tests")
    indented = make_game(tmp_path, "indented", "testsuite outer:\n    testsuite global:\n        teardown:\n            exit\n")

    games = run_testcases.load_games([str(plain), str(nested), str(ren_py), str(linked), str(indented)])

    assert [(g.name, g.source, g.needs_exit_suite) for g in games] == [
        ("plain", plain, True),
        ("nested", nested, False),
        ("ren_py", ren_py, False),
        ("linked", linked, False),
        ("indented", indented, True),
    ]


def test_load_games_rejects_runner_copies(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    A copy the runner made is cleaned before it's synced, so running it as the source would delete files from the
    game being run. WORK_DIR is patched so the copy can be made in tmp_path.
    """

    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path)
    copy = make_game(tmp_path / "games", "probe")

    with pytest.raises(run_testcases.ConfigError, match="where the runner keeps its copies"):
        run_testcases.load_games([str(copy)])


@pytest.mark.parametrize(
    ("names", "message"),
    [
        (["one"], "has no game directory"),
        (["launcher"], "same name as the launcher project"),
        (["updater"], "same name as the updater project"),
        (["game", "elsewhere/game"], "more than one game named game"),
        (["has space"], "may only contain"),
    ],
)
def test_load_games_rejects_unusable_games(tmp_path: Path, names: list[str], message: str) -> None:
    """
    A game is reported under its directory name, which is also its directory and savedir on each target, so a name
    that matches a project or another game would mix their files and results. "one" is created without a game
    directory, to show that the path must be a game.
    """

    paths = []

    for name in names:
        path = tmp_path / name
        path.mkdir(parents=True)
        if name != "one":
            (path / "game").mkdir()
        paths.append(str(path))

    with pytest.raises(run_testcases.ConfigError, match=message):
        run_testcases.load_games(paths)


def test_select_projects_with_games() -> None:
    """Games replace the default projects, --project adds to them, and filters still need exactly one item."""
    games = [run_testcases.Game("probe", Path("/probe")), run_testcases.Game("other", Path("/other"))]

    assert run_testcases.select_projects(None, [], games) == ["probe", "other"]
    assert run_testcases.select_projects("tutorial", [], games[:1]) == ["tutorial", "probe"]
    assert run_testcases.select_projects(None, ["case"], games[:1]) == ["probe"]

    with pytest.raises(run_testcases.ConfigError):
        run_testcases.select_projects(None, ["case"], games)

    with pytest.raises(run_testcases.ConfigError):
        run_testcases.select_projects("tutorial", ["case"], games[:1])


@pytest.mark.parametrize("needs_exit_suite", [True, False])
def test_game_sync_copies_to_ssh_target(tmp_path: Path, needs_exit_suite: bool) -> None:
    """
    On an ssh target, the game is copied into the games directory of the target's tree, and the exit suite is added
    to its game directory only when the game needs it.
    """

    target = run_testcases.Target("mac", "ssh", host="tom@mac", path="/Users/tom/renpy-test")
    game = run_testcases.Game("probe", tmp_path / "probe", needs_exit_suite=needs_exit_suite)
    exit_suite = tmp_path / run_testcases.EXIT_SUITE_FILE

    prepare, *rsyncs = run_testcases.build_game_sync_argvs(target, game, exit_suite)

    assert prepare[0] == "ssh"
    assert [argv[-2:] for argv in rsyncs] == [
        [f"{game.source}/", "tom@mac:/Users/tom/renpy-test/games/probe"],
        [str(exit_suite), f"tom@mac:/Users/tom/renpy-test/games/probe/game/{run_testcases.EXIT_SUITE_FILE}"],
    ][: 2 if needs_exit_suite else 1]


@pytest.mark.skipif(os.name != "posix", reason="Games are copied with rsync and run through POSIX shell scripts.")
@pytest.mark.skipif(shutil.which("rsync") is None, reason="Games are copied with rsync.")
def test_source_target_runs_staged_game(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    A source target runs a copy of the game in the repository's tmp directory, with the exit suite added, and leaves
    the game's own directory alone. A copy left over from a previous run loses its compiled scripts and files that
    the game no longer has, so a deleted test can't run. REPO is patched so the copy goes to tmp_path, and the
    "game" is a shell script that prints its arguments.
    """

    repo = tmp_path / "repo"
    repo.mkdir()
    mocker.patch.object(run_testcases, "REPO", repo)
    mocker.patch.object(run_testcases, "WORK_DIR", repo / "tmp" / "run-testcases")

    # The game directory is a link, which must be copied rather than recreated, or the exit suite would be written
    # through it into the original scripts.
    original = make_game(tmp_path, "original")
    source = tmp_path / "probe"
    source.mkdir()
    (source / "game").symlink_to(original / "game")
    game = run_testcases.load_games([str(source)])[0]
    staged = repo / "tmp" / "run-testcases" / "games" / "probe" / "game"
    staged.mkdir(parents=True)
    (staged / "removed.rpy").write_text("")
    (staged / "script.rpyc").write_text("")

    exit_suite = tmp_path / run_testcases.EXIT_SUITE_FILE
    exit_suite.write_text(run_testcases.EXIT_SUITE)
    fake_renpy = tmp_path / "fake-renpy.sh"
    fake_renpy.write_text('#!/bin/sh\necho "$@" > args.txt\n')
    fake_renpy.chmod(0o755)
    target = run_testcases.Target("source", "source", command=str(fake_renpy))
    output = tmp_path / "results"

    results = run_testcases.run_target(target, ["probe"], 0, [], output, [game], exit_suite)

    assert [(r.project, r.status) for r in results] == [("probe", "CRASH")]
    assert sorted(i.name for i in staged.iterdir()) == ["script.rpy", run_testcases.EXIT_SUITE_FILE]
    assert sorted(i.name for i in (original / "game").iterdir()) == ["script.rpy"]
    assert not staged.is_symlink()
    assert (repo / "args.txt").read_text().split()[:3] == [
        "tmp/run-testcases/games/probe",
        "--savedir",
        "tmp/run-testcases/saves/source/probe",
    ]


def test_run_target_with_only_games_syncs_engine(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    When only games run, the bundled projects and what only they use aren't copied to the target, which saves a
    long sync. Commands are recorded rather than run, and every one succeeds.
    """

    commands: list[list[str]] = []

    def record(argv: list[str], *args: object, **kwargs: object) -> int:
        commands.append(argv)
        return 0

    mocker.patch.object(run_testcases, "run_logged", side_effect=record)
    mocker.patch.object(run_testcases, "run_project", return_value=run_testcases.Result("linux", "probe", "PASS"))
    target = run_testcases.Target("linux", "local")
    game = run_testcases.Game("probe", tmp_path / "probe")

    run_testcases.run_target(target, ["probe"], 0, [], tmp_path / "results", [game])

    synced = {Path(argv[-1]).name for argv in commands if argv[0] == "rsync"}
    assert "renpy" in synced
    assert "probe" in synced
    assert not synced & run_testcases.BUNDLED_ONLY


@pytest.mark.skipif(shutil.which("rsync") is None, reason="Games are copied with rsync.")
@pytest.mark.parametrize("screenshots", run_testcases.SCREENSHOT_DIRS)
def test_game_sync_keeps_baselines_game_lacks(mocker: MockerFixture, tmp_path: Path, screenshots: str) -> None:
    """
    In the usual case, the game has no screenshot directory, or tests directory, at all, and a target saves baselines
    on its first run. The next sync must keep them, rather than deleting the directory the game doesn't have.
    """

    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path / "work")
    source = make_game(tmp_path, "probe")
    target = run_testcases.Target("linux", "local")
    game = run_testcases.load_games([str(source)])[0]
    staged = Path(target.workdir) / target.game_path("probe") / screenshots
    log = tmp_path / "log.txt"

    assert run_testcases.sync_game(target, game, None, log) is None
    staged.mkdir(parents=True)
    (staged / "saved.png").write_text("target")
    assert run_testcases.sync_game(target, game, None, log) is None

    assert [i.name for i in staged.iterdir()] == ["saved.png"]


@pytest.mark.skipif(shutil.which("rsync") is None, reason="Games are copied with rsync.")
@pytest.mark.parametrize("screenshots", run_testcases.SCREENSHOT_DIRS)
def test_game_sync_keeps_target_baselines(mocker: MockerFixture, tmp_path: Path, screenshots: str) -> None:
    """
    A screenshot baseline that a target saved survives the next sync, or every run would save a new one and pass
    without comparing anything. A baseline in the game itself replaces the target's, while the mismatch images
    the game's directory may hold aren't copied. The runner's cleanup step is run as a real shell script, and the
    run's screenshots are collected from the same directory.
    """

    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path / "work")
    source = make_game(tmp_path, "probe")
    (source / screenshots).mkdir(parents=True)
    (source / screenshots / "shipped.png").write_text("source")
    (source / screenshots / "shipped.new.png").write_text("mismatch")

    target = run_testcases.Target("linux", "local")
    game = run_testcases.load_games([str(source)])[0]
    staged = Path(target.workdir) / target.game_path("probe") / screenshots
    log = tmp_path / "log.txt"

    assert run_testcases.sync_game(target, game, None, log) is None
    (staged / "saved.png").write_text("target")
    (staged / "shipped.png").write_text("target-made")
    assert run_testcases.sync_game(target, game, None, log) is None

    assert sorted(i.name for i in staged.iterdir()) == ["saved.png", "shipped.png"]
    assert (staged / "shipped.png").read_text() == "source"

    collected = [argv[-2] for argv in run_testcases.build_collect_argvs(target, "probe", tmp_path, "games/probe")]
    assert f"{target.workdir}/games/probe/{screenshots}/" in collected


@pytest.mark.skipif(shutil.which("rsync") is None, reason="Artifacts are collected with rsync.")
@pytest.mark.parametrize("screenshots", run_testcases.SCREENSHOT_DIRS)
def test_collect_artifacts_gets_mismatch_images(mocker: MockerFixture, tmp_path: Path, screenshots: str) -> None:
    """
    The images that explain a failed screenshot assert are collected from either screenshot directory, including
    tests/screenshots, whose parent doesn't exist in the results until it's made. Baselines aren't collected.
    """

    mocker.patch.object(run_testcases, "WORK_DIR", tmp_path / "work")
    target = run_testcases.Target("linux", "local")
    staged = Path(target.workdir) / "games" / "probe" / screenshots
    staged.mkdir(parents=True)
    for name in ("shot.png", "shot.new.png", "shot.diff.png"):
        (staged / name).write_text(name)

    results = tmp_path / "results"
    results.mkdir()
    run_testcases.collect_artifacts(target, "probe", results, tmp_path / "log.txt", "games/probe")

    assert sorted(i.name for i in (results / screenshots).iterdir()) == ["shot.diff.png", "shot.new.png"]
