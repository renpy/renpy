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
import subprocess
import sys
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
