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

"""Tests for the updater test runner's choices, its wait for the restarted Ren'Py, and how it judges an update."""

import os
import subprocess
import time
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from scripts import run_testcases, run_updater_test

# The versions being developed, in the form renpy/versions.py gives them.
SERIES: dict[str, tuple[int, int, int]] = {"main": (8, 7, 0), "fix": (8, 6, 2)}

# What the testcase reports for an update that worked.
EXPECTED: dict[str, object] = {"channel": {"channel": "Nightly Fix", "split_version": [8, 6, 2, 26111801]}}
RESULT: dict[str, object] = {
    "version": "8.6.2.26111801+nightly",
    "version_tuple": [8, 6, 2, 26111801],
    "installed": {"sdk": "8.6.2.26111801+nightly"},
}
FINISHED: dict[str, object] = {"failed": False}


################################################################################
# Choosing what to update, and what to update it to.


@pytest.mark.parametrize(
    "branch, expected",
    [
        ("fix", "8.6.2"),
        ("main", "8.7.0"),
        ("work/someone/feature", "8.7.0"),
        ("", "8.7.0"),
    ],
)
def test_choose_version_follows_branch(branch: str, expected: str) -> None:
    """
    The default version is the one the current branch develops. A branch without a version of its own, or a
    detached head, develops the main version, as it does in renpy/versions.py.
    """

    assert run_updater_test.choose_version(branch, SERIES) == expected


@pytest.mark.parametrize(
    "version, expected",
    [
        ("8.6.2", "Nightly Fix"),
        ("8.6.1", "Nightly Fix"),
        ("8.7.0", "Nightly"),
        ("8.5.3", "Nightly"),
        ("not-a-version", "Nightly"),
    ],
)
def test_choose_channel_matches_release_series(version: str, expected: str) -> None:
    """
    A version in the series that's getting fixes updates to the nightly of those fixes, and any other version to the
    main nightly, as there are no fixes for it to get.
    """

    assert run_updater_test.choose_channel(version, SERIES) == expected


def test_find_archive_returns_built_sdk(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    The SDK to update is the tar.bz2 of the chosen variant in the version's directory. DL_DIR is patched so this
    doesn't depend on what has been built.
    """

    mocker.patch.object(run_updater_test, "DL_DIR", tmp_path)
    archive = tmp_path / "8.6.2" / "renpy-8.6.2-sdkarm.tar.bz2"
    archive.parent.mkdir()
    archive.touch()

    assert run_updater_test.find_archive("8.6.2", "sdkarm") == archive


def test_find_archive_rejects_missing_version(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    A version that hasn't been built is a configuration error that names the missing archive, rather than a failure
    part way through a run.
    """

    mocker.patch.object(run_updater_test, "DL_DIR", tmp_path)

    with pytest.raises(run_testcases.ConfigError, match="renpy-8.6.2-sdk.tar.bz2"):
        run_updater_test.find_archive("8.6.2", "sdk")


################################################################################
# Targets.


def test_select_targets_leaves_out_source_targets() -> None:
    """
    A source target runs in the repository, which must never be updated, so it isn't run by default.
    """

    targets = [run_testcases.Target("source", "source"), run_testcases.Target("linux", "local")]

    assert [t.name for t in run_updater_test.select_targets(targets, None)] == ["linux"]


def test_select_targets_rejects_named_source_target() -> None:
    """
    Naming a source target is an error, rather than being ignored, so the user knows it didn't run.
    """

    targets = [run_testcases.Target("source", "source"), run_testcases.Target("linux", "local")]

    with pytest.raises(run_testcases.ConfigError, match="source"):
        run_updater_test.select_targets(targets, "linux,source")


def test_run_target_uses_own_directory_on_ssh_target(tmp_path: Path) -> None:
    """
    An ssh target is updated in a subdirectory of its destination, so that the tree run_testcases.py keeps there
    isn't the one that gets replaced, and the copy to it deletes only inside that subdirectory.
    """

    target = run_testcases.Target("mac", "ssh", host="tom@mac", path="/Users/tom/renpy-test")
    options = run_updater_test.Options("8.6.2", "sdk", "Nightly Fix")

    run_target = run_updater_test.make_run_target(target, tmp_path, options)
    argvs = run_updater_test.build_deliver_argvs(run_target, tmp_path)

    assert run_target.workdir == "/Users/tom/renpy-test/updater-test"
    assert target.workdir == "/Users/tom/renpy-test"
    assert argvs[-1][-2:] == [f"{tmp_path}/", "tom@mac:/Users/tom/renpy-test/updater-test/"]
    assert "--delete" in argvs[-1]


def test_run_target_passes_channel_to_testcase(tmp_path: Path) -> None:
    """
    A local target runs where the SDK was unpacked, needing no copy, and the testcase is told which channel to pick
    through the environment, alongside what the target's configuration sets.
    """

    target = run_testcases.Target("linux", "local", env={"KEEP": "1"})
    options = run_updater_test.Options("8.6.2", "sdk", "Nightly")

    run_target = run_updater_test.make_run_target(target, tmp_path, options)

    assert run_target.workdir == str(tmp_path)
    assert run_target.env["RENPY_UPDATER_TEST_CHANNEL"] == "Nightly"
    assert run_target.env["KEEP"] == "1"
    assert run_updater_test.build_deliver_argvs(run_target, tmp_path) == []


def test_parse_options_reads_updater_arguments(mocker: MockerFixture) -> None:
    """
    The arguments run_testcases.py passes on choose the SDK, package, and channel. A version given without a channel
    gets the channel that suits that version, rather than the one that suits the repository. The versions being
    developed are patched, so this doesn't change when renpy/versions.py does.
    """

    mocker.patch.object(run_updater_test, "read_series", return_value=SERIES)

    assert run_updater_test.parse_options(["--version", "8.6.1"]) == run_updater_test.Options(
        "8.6.1", "sdk", "Nightly Fix"
    )
    assert run_updater_test.parse_options([
        "--version",
        "8.5.3",
        "--variant",
        "sdkarm",
        "--channel",
        "Release",
    ]) == run_updater_test.Options("8.5.3", "sdkarm", "Release")


@pytest.mark.parametrize(
    "arguments",
    [["some_test"], ["--variant", "source"], ["--version"], ["--headless"]],
    ids=["test_filter", "unknown_variant", "missing_value", "runner_option"],
)
def test_parse_options_rejects_other_arguments(mocker: MockerFixture, arguments: list[str]) -> None:
    """
    Anything that isn't one of the updater test's arguments is a configuration error, including a test filter, since
    the updater test can't be filtered. argparse would exit the process, which would end run_testcases.py without
    its usual message.
    """

    mocker.patch.object(run_updater_test, "read_series", return_value=SERIES)

    with pytest.raises(run_testcases.ConfigError):
        run_updater_test.parse_options(arguments)


def test_requested_sdk_must_exist(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    An SDK that was asked for by version and hasn't been built is an error, both before the run starts and as the
    result of a target, unlike the default SDK, whose absence is expected. DL_DIR is patched to an empty directory.
    """

    mocker.patch.object(run_updater_test, "DL_DIR", tmp_path)
    arguments = ["--version", "8.6.1"]

    with pytest.raises(run_testcases.ConfigError, match="renpy-8.6.1-sdk.tar.bz2"):
        run_updater_test.check_arguments(arguments)

    run_updater_test.check_arguments([])

    results = run_updater_test.run_default(run_testcases.Target("linux", "local"), 0, tmp_path / "results", arguments)

    assert [(r.project, r.status) for r in results] == [("updater", "ERROR")]


def test_run_default_skips_source_target(tmp_path: Path) -> None:
    """
    When run by run_testcases.py, a source target gets no updater result at all, rather than a failure, since the
    repository is never updated.
    """

    assert run_updater_test.run_default(run_testcases.Target("source", "source"), 0, tmp_path) == []


def test_run_default_expects_failure_without_built_sdk(mocker: MockerFixture, tmp_path: Path) -> None:
    """
    When run by run_testcases.py and the SDK of this repository's version hasn't been built, the result is an
    expected failure that names the missing archive, and nothing is run. DL_DIR is patched to an empty directory.
    """

    mocker.patch.object(run_updater_test, "DL_DIR", tmp_path)
    run = mocker.patch.object(run_updater_test, "run_target")

    results = run_updater_test.run_default(run_testcases.Target("linux", "local"), 0, tmp_path / "results")

    assert [(r.project, r.status) for r in results] == [("updater", "XFAIL")]
    assert "-sdk.tar.bz2 doesn't exist" in results[0].detail
    run.assert_not_called()


################################################################################
# Running the update, and waiting for the Ren'Py that the launcher restarts.


def run_update_script(tmp_path: Path, launcher: str, mocker: MockerFixture) -> subprocess.CompletedProcess[str]:
    """
    Runs the real update script in `tmp_path`, with the shell script `launcher` standing in for Ren'Py. The waits are
    shortened, so a restart that never reports is noticed in about a second. The script gets a session of its own, as
    it does when the runner starts it, because it signals its process group, which would otherwise be pytest's.
    """

    mocker.patch.object(run_updater_test, "RELAUNCH_WAIT", 1)
    mocker.patch.object(run_updater_test, "SETTLE", 0)

    fake = tmp_path / "fake-renpy.sh"
    fake.write_text(f'#!/bin/sh\necho "$@" > arguments.txt\n{launcher}\n')
    fake.chmod(0o755)

    target = run_testcases.Target("linux", "local", command="./fake-renpy.sh", root=str(tmp_path))
    argv = run_updater_test.build_update_argv(target, 0)

    return subprocess.run(argv, check=False, capture_output=True, text=True, timeout=60, start_new_session=True)


def test_update_script_waits_for_restarted_renpy(tmp_path: Path, mocker: MockerFixture) -> None:
    """
    The launcher exits as soon as it has started the Ren'Py it installed, so the script has to keep running until
    that Ren'Py reports that it's quitting. Here that's written by a background process, after the fake launcher has
    exited.
    The launcher is also run with Ren'Py itself as its base directory, as it only offers updates there.
    """

    state = run_updater_test.STATE_DIR
    launcher = (
        f"mkdir -p {state}; touch {state}/expected.json; (sleep 0.3; touch {state}/finished.json) > /dev/null 2>&1 &"
    )

    completed = run_update_script(tmp_path, launcher, mocker)

    assert completed.returncode == 0
    assert (tmp_path / state / "finished.json").exists()
    assert (tmp_path / "arguments.txt").read_text().split()[0] == "."


@pytest.mark.parametrize(
    "launcher",
    [
        "exit 0",
        f"mkdir -p {run_updater_test.STATE_DIR}; touch {run_updater_test.STATE_DIR}/expected.json",
    ],
    ids=["update_not_installed", "restart_never_reports"],
)
def test_update_script_fails_without_report(tmp_path: Path, mocker: MockerFixture, launcher: str) -> None:
    """
    The script fails if the launcher exits without having installed the update, even with a zero exit status, and
    if the update was installed but nothing reports afterwards, which is what a Ren'Py that can't start looks like.
    """

    assert run_update_script(tmp_path, launcher, mocker).returncode != 0


def test_update_script_stops_restart_that_never_quits(tmp_path: Path, mocker: MockerFixture) -> None:
    """
    A restarted Ren'Py that hangs without reporting is stopped when the wait for it runs out, rather than being left
    running on the target, where it would get in the way of later tests. Here it's a background sleep that records
    its process id, and signal 0 is used to see if that process still exists.
    """

    state = run_updater_test.STATE_DIR
    launcher = (
        f"mkdir -p {state}; touch {state}/expected.json; "
        "sh -c 'echo $$ > restarted.pid; exec sleep 60' > /dev/null 2>&1 &"
    )

    # The status is that of a failed test. A script that was itself killed by the signal would have a negative one
    # here, and over ssh that would be reported as ssh having failed.
    assert run_update_script(tmp_path, launcher, mocker).returncode == 1

    pid = int((tmp_path / "restarted.pid").read_text())
    time.sleep(0.5)

    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


def test_update_script_keeps_launcher_exit_status(tmp_path: Path, mocker: MockerFixture) -> None:
    """
    The script exits with the status of the launcher that did the update, which is nonzero if its tests failed, even
    when the Ren'Py it installed goes on to report. Otherwise that failure would be lost, as only the reports of the
    restarted Ren'Py are read.
    """

    state = run_updater_test.STATE_DIR
    launcher = f"mkdir -p {state}; touch {state}/expected.json {state}/finished.json; exit 7"

    assert run_update_script(tmp_path, launcher, mocker).returncode == 7


def test_update_script_removes_previous_report(tmp_path: Path, mocker: MockerFixture) -> None:
    """
    Reports left by a previous run are removed before the launcher starts. Otherwise the testcase would take a stale
    expected.json to mean the update had already happened, and the script would accept a stale result.
    """

    state = tmp_path / run_updater_test.STATE_DIR
    state.mkdir()
    (state / "expected.json").touch()
    (state / "result.json").touch()
    (state / "finished.json").touch()

    assert run_update_script(tmp_path, "exit 0", mocker).returncode != 0
    assert not state.exists()


def test_headless_display_outlives_launcher() -> None:
    """
    On a headless target, the virtual display has to wrap the wait as well as the launcher, since xvfb-run stops the
    display when its command exits, and the restarted Ren'Py still needs it. So xvfb-run runs the waiting shell, and
    the launcher is started inside that.
    """

    target = run_testcases.Target("linux", "local", headless=True, root="/stage")
    script = run_updater_test.build_update_script(target, 0)

    display = script.index("xvfb-run")
    shell = script.index("/bin/sh -c")

    assert display < shell < script.index("./renpy.sh")
    assert shell < script.index("finished.json")


def test_update_runs_over_ssh_with_pty() -> None:
    """
    An ssh target runs the same script on the other computer, with a pty, so that stopping the client also stops
    the Ren'Py processes there.
    """

    target = run_testcases.Target("mac", "ssh", host="tom@mac", path="renpy-test", root="renpy-test/updater-test")
    argv = run_updater_test.build_update_argv(target, 0)

    assert argv[:2] == ["ssh", "-tt"]
    assert argv[-2] == "tom@mac"
    assert argv[-1] == run_updater_test.build_update_script(target, 0)


################################################################################
# Judging the update.


def test_judge_update_accepts_matching_versions() -> None:
    """
    An update worked when the Ren'Py that ran after it is the version the channel offered, the updater recorded
    that version as installed, and that Ren'Py quit without its tests failing.
    """

    assert run_updater_test.judge_update(EXPECTED, RESULT, FINISHED, "sdk") is None


@pytest.mark.parametrize(
    "expected, result, finished, variant, problem",
    [
        (None, None, None, "sdk", "did not install"),
        (None, RESULT, FINISHED, "sdk", "did not install"),
        (EXPECTED, None, None, "sdk", "did not report"),
        (EXPECTED, RESULT, None, "sdk", "did not quit"),
        (EXPECTED, RESULT, {"failed": True}, "sdk", "tests failed"),
        (EXPECTED, RESULT, {}, "sdk", "tests failed"),
        (EXPECTED, {**RESULT, "version_tuple": [8, 6, 1, 26111705]}, FINISHED, "sdk", "offered version"),
        (EXPECTED, {**RESULT, "installed": {"sdk": "8.6.1.26111705"}}, FINISHED, "sdk", "current.json"),
        (EXPECTED, RESULT, FINISHED, "sdkarm", "current.json"),
        ({"channel": "Nightly Fix"}, RESULT, FINISHED, "sdk", "don't give the versions"),
        ({}, {}, FINISHED, "sdk", "don't give the versions"),
    ],
    ids=[
        "nothing_reported",
        "stale_result_only",
        "restart_did_not_report",
        "restart_did_not_quit",
        "restart_tests_failed",
        "quit_report_without_outcome",
        "old_version_still_runs",
        "install_not_recorded",
        "other_variant_installed",
        "malformed_expected",
        "empty_reports",
    ],
)
def test_judge_update_reports_problem(
    expected: dict[str, object] | None,
    result: dict[str, object] | None,
    finished: dict[str, object] | None,
    variant: str,
    problem: str,
) -> None:
    """
    Each way an update can go wrong is reported as its own problem: the launcher not finishing, the restarted Ren'Py
    not reporting, not quitting, or failing its tests, the old version still running, and the updater's record of
    what's installed not matching, including for the variant that was asked for. Reports that lack the versions are a
    failure, rather than two missing values comparing as equal, or an exception.
    """

    assert problem in (run_updater_test.judge_update(expected, result, finished, variant) or "")


def test_read_json_ignores_unusable_reports(tmp_path: Path) -> None:
    """
    A report that's missing, isn't JSON, or isn't an object reads as None, which judge_update treats as the step not
    having happened. A valid one is returned as is.
    """

    (tmp_path / "broken.json").write_text("{")
    (tmp_path / "list.json").write_text("[1]")
    (tmp_path / "good.json").write_text('{"version": "8.6.2"}')

    assert run_updater_test.read_json(tmp_path / "missing.json") is None
    assert run_updater_test.read_json(tmp_path / "broken.json") is None
    assert run_updater_test.read_json(tmp_path / "list.json") is None
    assert run_updater_test.read_json(tmp_path / "good.json") == {"version": "8.6.2"}
