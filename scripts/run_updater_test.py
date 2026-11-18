#!/usr/bin/env python3

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

"""
Tests the Ren'Py updater, by updating a copy of Ren'Py to a nightly build and checking that the result runs.

This uses the targets of scripts/run_testcases.py, defined in ~/.renpy/dev/testcases.toml, apart from source targets,
as the repository must not be updated. On each target, this:

1. Creates the Ren'Py to update, by unpacking the SDK that was built into dl/<version>.
2. Copies scripts/updater_testcase.rpy into its launcher, and runs it. The testcase uses the launcher to pick an update
   channel and update, and the launcher then restarts itself, which runs the testcase again in the Ren'Py that was
   installed.
3. Checks that the Ren'Py that restarted is the version the channel offered, and that it can run the tests of
   SMOKE_PROJECT.

The update comes from the real update servers, so the targets need to be able to reach them.

Progress goes to stderr and the final synopsis to stdout. Logs are kept in tmp/run-updater-test/<timestamp>/<target>/,
with tmp/run-updater-test/latest pointing at the newest run. The exit status is 0 if every target passed, 1 if any
did not, and 2 for a configuration or usage error.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    # When this or run_testcases.py is run as a script, the scripts directory is on the path. This comes first so that
    # the module run_testcases.py registered is used, rather than a second copy of it.
    import run_testcases
    from run_testcases import ConfigError, Result, Target
except ImportError:
    from scripts import run_testcases
    from scripts.run_testcases import ConfigError, Result, Target

# The root of the Ren'Py checkout this script belongs to.
REPO: Path = run_testcases.REPO

# The directory, under the repository, that holds the copies of Ren'Py being updated and the results.
WORK_DIR: Path = REPO / "tmp" / "run-updater-test"

# The directory that holds the SDKs that have been built, one directory per version.
DL_DIR: Path = REPO / "dl"

# The testcase that's copied into the launcher, and the name it's run by.
TESTCASE: Path = REPO / "scripts" / "updater_testcase.rpy"
TESTCASE_NAME: str = "updater_test"

# The directory, relative to the Ren'Py being updated, the testcase reports in. This matches UPDATER_TEST_STATE in
# the testcase.
STATE_DIR: str = "updater-test-state"

# The directory inside an ssh target's destination that holds the Ren'Py being updated. run_testcases.py only deletes
# from the items it syncs, so it leaves this alone.
REMOTE_SUBDIR: str = "updater-test"

# The project whose tests show that the Ren'Py that was installed runs.
SMOKE_PROJECT: str = "the_question"

# The names the update, and the tests run after it, are reported under.
UPDATE_NAME: str = run_testcases.UPDATER
SMOKE_NAME: str = f"{run_testcases.UPDATER}:{SMOKE_PROJECT}"

# The SDK packages that can be updated, which are the suffixes of their archives and their names in update files.
VARIANTS: tuple[str, ...] = ("sdk", "sdkarm")

# The update channels that are used when --channel isn't given.
FIX_CHANNEL: str = "Nightly Fix"
MAIN_CHANNEL: str = "Nightly"

# How long, in seconds, the Ren'Py that was installed has to start and report, once the launcher has exited.
RELAUNCH_WAIT: int = 300

# How long, in seconds, the Ren'Py that reported it was quitting is given to exit, so it isn't running during the
# next test.
SETTLE: int = 2

# The base directory the launcher is run with. This is Ren'Py itself, as it is when Ren'Py is started without naming a
# project, rather than the launcher project. The launcher only offers to update the Ren'Py in its base directory.
LAUNCHER_BASE: str = "."

# The files that are copied to the results, as a map from the path relative to the Ren'Py being updated to the name
# it's given. update/log.txt is the updater's own log, and the launcher writes the last three to its base directory.
ARTIFACTS: dict[str, str] = {
    f"{STATE_DIR}/expected.json": "expected.json",
    f"{STATE_DIR}/result.json": "result.json",
    f"{STATE_DIR}/finished.json": "finished.json",
    "update/log.txt": "updater-log.txt",
    "log.txt": "log.txt",
    "traceback.txt": "traceback.txt",
    "errors.txt": "errors.txt",
}


@dataclasses.dataclass
class Options:
    """
    What the command line asked for, which is the same for every target.
    """

    version: str
    "The major.minor.patch version of the Ren'Py being updated, which names the directory in dl/ that has its SDK."

    variant: str
    "The package to update, one of VARIANTS."

    channel: str
    "The name of the update channel to select in the launcher."


def read_series() -> dict[str, tuple[int, int, int]]:
    """
    Returns the version being developed on each branch, as given by renpy/versions.py. That file is loaded on its
    own, since importing the renpy package would start the engine.
    """

    spec = importlib.util.spec_from_file_location("_renpy_versions", REPO / "renpy" / "versions.py")

    if spec is None or spec.loader is None:
        raise ConfigError("Could not load renpy/versions.py.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return {branch: version.semver for branch, version in module.branch_to_version.items()}


def read_branch() -> str:
    """
    Returns the branch the repository is on, or "" if that can't be determined.
    """

    try:
        return subprocess.check_output(["git", "-C", str(REPO), "branch", "--show-current"], encoding="utf-8").strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def choose_version(branch: str, series: dict[str, tuple[int, int, int]]) -> str:
    """
    Returns the version of this repository, which is how distribute.py names the directory in dl/ it builds a
    release into. As in renpy/versions.py, a branch that has no version of its own is developing the main one.
    """

    return ".".join(str(i) for i in series.get(branch, series["main"]))


def choose_channel(version: str, series: dict[str, tuple[int, int, int]]) -> str:
    """
    Returns the nightly channel that suits a Ren'Py of the given version: the fixes to its own release series if it
    is in the series that's getting fixes, and the main nightly otherwise.
    """

    try:
        parts = tuple(int(i) for i in version.split(".")[:2])
    except ValueError:
        parts = ()

    if "fix" in series and parts == series["fix"][:2]:
        return FIX_CHANNEL

    return MAIN_CHANNEL


def find_archive(version: str, variant: str) -> Path:
    """
    Returns the archive of the SDK that was built for `version`, raising ConfigError if it hasn't been built.
    """

    archive = DL_DIR / version / f"renpy-{version}-{variant}.tar.bz2"

    if not archive.is_file():
        raise ConfigError(
            f"{archive} doesn't exist. Build that version, or use --version to name one that has been built."
        )

    return archive


def make_run_target(target: Target, stage: Path, options: Options) -> Target:
    """
    Returns a copy of a target that runs the Ren'Py being updated, rather than the tree run_testcases.py gives it,
    with the environment the testcase needs.
    """

    if target.type == "ssh":
        root = f"{target.path}/{REMOTE_SUBDIR}"
    else:
        root = str(stage)

    env = {
        **target.env,
        "RENPY_UPDATER_TEST_CHANNEL": options.channel,
        "RENPY_UPDATER_TEST_TIMEOUT": str(int(target.timeout)),
    }

    return dataclasses.replace(target, root=root, env=env)


def build_stage_argv(stage: Path, options: Options) -> list[str]:
    """
    Returns the command that fills the empty directory `stage` with the Ren'Py to update, by unpacking its SDK without
    the directory the archive keeps it in.
    """

    archive = find_archive(options.version, options.variant)

    return ["tar", "-xjf", str(archive), "-C", str(stage), "--strip-components=1"]


def build_deliver_argvs(target: Target, stage: Path) -> list[list[str]]:
    """
    Returns the commands that copy the Ren'Py in `stage` to where `target`, made by make_run_target, runs it. Only
    ssh targets run somewhere else. Removing what's there is what makes each run start from the same Ren'Py.
    """

    if target.type != "ssh":
        return []

    return [
        ["ssh", *run_testcases.SSH_OPTIONS, str(target.host), f"mkdir -p {shlex.quote(target.workdir)}"],
        [*run_testcases.rsync_base(target), "--delete", f"{stage}/", f"{target.host}:{target.workdir}/"],
    ]


def build_update_script(target: Target, index: int) -> str:
    """
    Returns the POSIX shell script that runs the testcase on a target made by make_run_target, and then waits for
    the Ren'Py the launcher started to report.

    The launcher's restart is a new process that outlives the one this starts. Waiting here keeps what it needs
    alive until it's done: the ssh session, and the virtual display, which is why the display wraps the whole wait
    rather than only the launcher.

    The script must be run as the leader of its own process group, as run_logged and sshd do, since it signals that
    group to stop a Ren'Py that never finishes.
    """

    savedir = target.project_savedir("launcher")
    arguments = shlex.join([LAUNCHER_BASE, "--savedir", savedir, "test", "--report-detailed", TESTCASE_NAME])
    expected = f"{STATE_DIR}/expected.json"
    finished = f"{STATE_DIR}/finished.json"

    inner = "; ".join([
        f"{run_testcases.choose_command(target)} {arguments}",
        # This is the status of the launcher that installed the update, which is what this script exits with.
        "status=$?",
        # Without this file, the launcher didn't finish updating, so it didn't restart.
        f"[ -e {expected} ] || exit 1",
        # The Ren'Py that was installed writes this last, as it quits.
        f"waited=0; while [ ! -e {finished} ] && [ $waited -lt {RELAUNCH_WAIT} ]; do sleep 1; waited=$((waited + 1)); done",
        # A Ren'Py that hasn't quit by now is stuck. This stops it, along with this shell and the virtual display, as
        # they share a process group, so that it isn't left running on the target.
        f"[ -e {finished} ] || {{ kill -TERM 0; exit 1; }}",
        f"sleep {SETTLE}",
        "exit $status",
    ])

    launch = run_testcases.build_launch(target, index, command=f"/bin/sh -c {shlex.quote(inner)}")

    return "; ".join([
        f"cd {shlex.quote(target.workdir)} || exit 125",
        f"rm -rf {STATE_DIR} {shlex.quote(savedir)} traceback.txt errors.txt",
        # This shell is the leader of the group that's signalled when the restarted Ren'Py is stuck. Handling the
        # signal lets it exit with a status, which over ssh is what tells a failure of the test from one of ssh. The
        # commands it runs don't inherit a handler, so they still stop.
        "trap 'exit 1' TERM",
        launch,
        "exit $?",
    ])


def build_update_argv(target: Target, index: int) -> list[str]:
    """
    Returns the local command line that runs the update on a target made by make_run_target. As in run_testcases.py,
    ssh gets a pty so that killing the client stops the remote processes.
    """

    script = build_update_script(target, index)

    if target.type == "ssh":
        return ["ssh", "-tt", *run_testcases.SSH_OPTIONS, str(target.host), script]

    return ["/bin/sh", "-c", script]


def build_collect_argvs(target: Target, directory: Path) -> list[list[str]]:
    """
    Returns the rsync commands that copy what the update left behind to the results directory. Those for files that
    don't exist fail harmlessly.
    """

    return [
        [*run_testcases.rsync_base(target), run_testcases.remote_path(target, source), f"{directory}/{name}"]
        for source, name in ARTIFACTS.items()
    ]


def read_json(path: Path) -> dict[str, object] | None:
    """
    Returns the object in a JSON file the testcase wrote, or None if the file is missing or isn't one.
    """

    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None

    return data if isinstance(data, dict) else None


def judge_update(
    expected: dict[str, object] | None,
    result: dict[str, object] | None,
    finished: dict[str, object] | None,
    variant: str,
) -> str | None:
    """
    Decides if an update worked, returning None if it did, or a description of what went wrong.

    `expected`
        What the testcase wrote once the launcher had installed the update: the channel it chose, as the launcher
        was offered it. None if it didn't get that far.

    `result`
        What the testcase wrote when it ran again after the launcher restarted: the version that ran, and the versions
        the updater recorded as installed. None if that didn't happen.

    `finished`
        What the testcase wrote as that Ren'Py quit: if its tests failed. None if it didn't quit.
    """

    if expected is None:
        return "the launcher did not install the update"

    if result is None:
        return "the update was installed, but the Ren'Py that the launcher restarted did not report"

    if finished is None:
        return "the Ren'Py that the launcher restarted reported, but did not quit"

    if finished.get("failed") is not False:
        return "the tests failed in the Ren'Py that the launcher restarted"

    channel = expected.get("channel")
    offered = channel.get("split_version") if isinstance(channel, dict) else None

    if offered is None or result.get("version") is None:
        return "the testcase's reports don't give the versions that were offered and that ran"

    if result.get("version_tuple") != offered:
        return f"the channel offered version {offered}, but version {result.get('version_tuple')} ran after the update"

    installed = result.get("installed")
    recorded = installed.get(variant) if isinstance(installed, dict) else None

    if recorded != result.get("version"):
        return f"update/current.json records {recorded!r} as installed, but {result.get('version')!r} ran"

    return None


def stage_target(run_target: Target, stage: Path, options: Options, log: Path) -> str | None:
    """
    Creates the Ren'Py to update, with the testcase in its launcher, where the target will run it. Returns None if
    that worked, or a description of the failure.

    This removes the Ren'Py a previous run left in `stage`, which that run updated.
    """

    if stage.exists():
        shutil.rmtree(stage)

    stage.mkdir(parents=True)

    status = run_testcases.run_logged(build_stage_argv(stage, options), log)
    if status != 0:
        return f"unpacking the SDK failed with exit status {status}"

    launcher = stage / "launcher" / "game"
    if not launcher.is_dir():
        return f"{stage} has no launcher, so it isn't a Ren'Py that can be updated"

    shutil.copy(TESTCASE, launcher / TESTCASE.name)

    for argv in build_deliver_argvs(run_target, stage):
        status = run_testcases.run_logged(argv, log)
        if status not in (0, run_testcases.RSYNC_VANISHED):
            return f"copying to {run_target.host} failed with exit status {status}"

    return None


def run_update(target: Target, index: int, options: Options, directory: Path, support: Path) -> Result:
    """
    Runs the update on a target made by make_run_target that has been staged, and reports on it. This doesn't raise
    for anything that's the update's fault.
    """

    directory.mkdir(parents=True, exist_ok=True)

    output = directory / "output.txt"
    relative_output = output.relative_to(REPO) if output.is_relative_to(REPO) else output

    def finish(status: str, detail: str = "") -> Result:
        """
        Makes the result of the update, and tells the user about it.
        """

        duration = time.monotonic() - start
        first = detail.split("\n")[0]
        run_testcases.report_progress(f"{target.name}/{UPDATE_NAME}", f"{status}{': ' if first else ''}{first}")

        return Result(target.name, UPDATE_NAME, status, duration=duration, detail=detail, log=relative_output)

    start = time.monotonic()
    run_testcases.report_progress(f"{target.name}/{UPDATE_NAME}", f"updating using the {options.channel} channel")

    # The testcase gives the update the target's timeout, and the rest is for starting, restarting, and reporting.
    timeout = target.timeout + RELAUNCH_WAIT + 120
    timed_out = False

    try:
        returncode = run_testcases.run_logged(build_update_argv(target, index), output, timeout)

    except run_testcases.CommandTimeout:
        run_testcases.stop_wine(target, support)
        returncode = None
        timed_out = True

    except run_testcases.Cancelled:
        run_testcases.stop_wine(target, support)
        return finish("ERROR", "interrupted")

    except OSError as e:
        return finish("ERROR", str(e))

    if target.type == "ssh" and returncode == run_testcases.SSH_FAILED:
        return finish("ERROR", f"ssh failed; see {relative_output}")

    for argv in build_collect_argvs(target, directory):
        try:
            run_testcases.run_logged(argv, support, timeout=300)
        except (run_testcases.CommandTimeout, run_testcases.Cancelled, OSError):
            break

    expected = read_json(directory / "expected.json")
    result = read_json(directory / "result.json")
    finished = read_json(directory / "finished.json")
    problem = judge_update(expected, result, finished, options.variant)

    if problem is None and returncode not in (0, None):
        problem = (
            f"the update was installed and runs, but the launcher that installed it exited with status {returncode}"
        )

    if problem is None and not timed_out:
        assert expected is not None and result is not None
        return finish("PASS", f"updated {expected.get('updated_from')} to {result.get('version')}")

    # A wine process outlives the process group that the script stops when the restarted Ren'Py doesn't quit.
    run_testcases.stop_wine(target, support)

    text = output.read_text(encoding="utf-8", errors="replace") if output.exists() else ""
    diagnostics = "\n\n".join(run_testcases.extract_failure_details(text)) or run_testcases.read_tail(output)

    if timed_out:
        problem = f"timed out; {problem}" if problem else "timed out"

    return finish("TIMEOUT" if timed_out else "FAIL", f"{problem}; see {relative_output}\n{diagnostics}".rstrip())


def run_target(target: Target, index: int, options: Options, directory: Path) -> list[Result]:
    """
    Tests the updater on one target: stages the Ren'Py to update, updates it, and if that worked, runs the tests of
    SMOKE_PROJECT in what was installed. Returns a result for each of those that ran.
    """

    directory.mkdir(parents=True, exist_ok=True)

    support = directory / "support.txt"
    stage = WORK_DIR / "stage" / target.name
    run_target = make_run_target(target, stage, options)

    def error(detail: str) -> list[Result]:
        """
        Makes the result of a target that couldn't be updated at all.
        """

        run_testcases.report_progress(target.name, f"ERROR: {detail}")
        return [Result(target.name, UPDATE_NAME, "ERROR", detail=detail)]

    try:
        run_testcases.report_progress(target.name, "staging")
        failure = stage_target(run_target, stage, options, support)

    except run_testcases.Cancelled:
        return error("interrupted")

    except OSError as e:
        return error(str(e))

    if failure:
        return error(f"{failure}; see {support}")

    results = [run_update(run_target, index, options, directory / "update", support)]

    if results[0].status == "PASS":
        project_directory = directory / SMOKE_PROJECT
        smoke = run_testcases.run_project(run_target, SMOKE_PROJECT, index, [], project_directory, support)
        results.append(dataclasses.replace(smoke, project=SMOKE_NAME))

    return results


def add_option_arguments(ap: argparse.ArgumentParser) -> None:
    """
    Adds the arguments that choose what's updated, and what it's updated to, to an argument parser. These are the
    arguments of this script that run_testcases.py also takes, after --.
    """

    ap.add_argument("--version", help="The version in dl/ to update. Default: the version of this repository.")
    ap.add_argument("--variant", choices=VARIANTS, default=VARIANTS[0], help="The SDK package to update. Default: sdk")
    ap.add_argument(
        "--channel",
        help=f"The update channel to select in the launcher. Default: {FIX_CHANNEL!r} if the version being updated is "
        f"in the release series that's getting fixes, {MAIN_CHANNEL!r} otherwise.",
    )


def make_options(version: str | None = None, variant: str = VARIANTS[0], channel: str | None = None) -> Options:
    """
    Returns the options for what was asked for. What wasn't asked for defaults to the SDK of this repository's
    version, and to the nightly channel that suits the version being updated.
    """

    series = read_series()
    version = version or choose_version(read_branch(), series)

    return Options(version, variant, channel or choose_channel(version, series))


def parse_options(arguments: list[str]) -> Options:
    """
    Returns the options given by `arguments`, which are the command line arguments that add_option_arguments defines.
    Raises ConfigError, rather than exiting as argparse would, if they aren't valid.
    """

    ap = argparse.ArgumentParser(prog="updater test", add_help=False, exit_on_error=False)
    add_option_arguments(ap)

    try:
        args, unknown = ap.parse_known_args(arguments)
    except argparse.ArgumentError as e:
        raise ConfigError(f"The updater test's arguments aren't valid: {e}") from None

    if unknown:
        raise ConfigError(
            f"The updater test doesn't take {' '.join(unknown)!r}. It takes --version, --variant, and --channel."
        )

    return make_options(args.version, args.variant, args.channel)


def check_arguments(arguments: list[str]) -> None:
    """
    Raises ConfigError if run_default can't use `arguments`: if they aren't valid, or if they name an SDK that hasn't
    been built. This lets run_testcases.py refuse them before it starts.
    """

    options = parse_options(arguments)

    if arguments:
        find_archive(options.version, options.variant)


def run_default(target: Target, index: int, directory: Path, arguments: list[str] | None = None) -> list[Result]:
    """
    Tests the updater on a target, for run_testcases.py. A source target has no results, as the repository can't be
    updated.

    `arguments`
        The command line arguments that choose what's updated, as parse_options takes them. Without any, the SDK of
        this repository's version is updated, and if it hasn't been built, the result is an expected failure, since
        that's the usual state of a repository between releases. An SDK that was asked for and is missing is an error.
    """

    if target.type == "source":
        return []

    if run_testcases.cancelled.is_set():
        return [Result(target.name, UPDATE_NAME, "ERROR", detail="interrupted")]

    try:
        options = parse_options(arguments or [])
        find_archive(options.version, options.variant)
    except ConfigError as e:
        status = "ERROR" if arguments else "XFAIL"
        run_testcases.report_progress(f"{target.name}/{UPDATE_NAME}", f"{status}: {e}")
        return [Result(target.name, UPDATE_NAME, status, detail=str(e))]

    return run_target(target, index, options, directory)


def run_all(targets: list[Target], options: Options) -> list[Result]:
    """
    Tests the updater on the given targets in parallel, returning their results in the order the targets were given.
    """

    directory = run_testcases.make_results_directory(WORK_DIR)
    run_testcases.report_progress("results", str(directory))

    results: dict[str, list[Result]] = {}
    threads = []

    def run_one(target: Target, index: int) -> None:
        """
        Runs one target on its own thread, reporting a bug in this script as that target's error.
        """

        try:
            results[target.name] = run_target(target, index, options, directory / target.name)
        except Exception as e:
            run_testcases.report_progress(target.name, f"ERROR: {e!r}")
            results[target.name] = [Result(target.name, UPDATE_NAME, "ERROR", detail=repr(e))]

    for index, target in enumerate(targets):
        thread = threading.Thread(target=run_one, args=(target, index), name=target.name)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return [result for t in targets for result in results[t.name]]


def select_targets(targets: list[Target], names: str | None) -> list[Target]:
    """
    Picks the targets to update, as run_testcases.py does, except that source targets are left out unless they are
    named, which is an error: a source target runs in the repository, which must not be updated.
    """

    if names:
        selected = run_testcases.select_targets(targets, names)

        for target in selected:
            if target.type == "source":
                raise ConfigError(f"Target {target.name}: a source target can't be updated, as it's the repository.")

        return selected

    return run_testcases.select_targets([t for t in targets if t.type != "source"], None)


def main() -> int:
    """
    Runs the command line, returning the exit status.
    """

    ap = argparse.ArgumentParser(description="Test the Ren'Py updater by updating a copy of Ren'Py to a nightly build.")
    add_option_arguments(ap)
    ap.add_argument(
        "--config",
        type=Path,
        default=run_testcases.DEFAULT_CONFIG,
        help=f"The config file. Default: {run_testcases.DEFAULT_CONFIG}",
    )
    ap.add_argument("-t", "--target", help="A comma-separated list of targets to run, which may be disabled ones.")
    ap.add_argument("--list", action="store_true", help="List the configured targets, and exit.")
    ap.add_argument("--headless", action="store_true", help="Run every target on a virtual display with dummy audio.")
    ap.add_argument("--timeout", type=float, help="Override how long the update, and the tests, may take, in seconds.")
    args = ap.parse_args()

    try:
        targets = run_testcases.load_targets(args.config.expanduser())

        if args.list:
            for target in targets:
                suffix = "" if target.enabled else " (disabled)"
                suffix += " (can't be updated)" if target.type == "source" else ""
                print(f"{target.name}: {target.type}{' headless' if target.headless else ''}{suffix}")
            return 0

        if args.timeout is not None and args.timeout <= 0:
            raise ConfigError("--timeout must be positive.")

        selected = select_targets(targets, args.target)

        options = make_options(args.version, args.variant, args.channel)
        find_archive(options.version, options.variant)

    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    for target in selected:
        target.headless = target.headless or args.headless
        if args.timeout is not None:
            target.timeout = args.timeout

    for tool in ("rsync", "tar"):
        if not shutil.which(tool):
            print(f"Error: {tool} is required.", file=sys.stderr)
            return 2

    signal.signal(signal.SIGINT, run_testcases.request_cancel)
    signal.signal(signal.SIGTERM, run_testcases.request_cancel)

    results = run_all(selected, options)
    print(run_testcases.format_synopsis(results), flush=True)

    return 0 if all(r.status in run_testcases.SUCCESSFUL for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
