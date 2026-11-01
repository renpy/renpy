#!/usr/bin/env python3
#
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
Runs Ren'Py's functional testcases on several platforms at once, and prints one synopsis.

Targets are defined in ~/.renpy/dev/testcases.toml; scripts/run_testcases.example.toml documents the format. A target
is a place to run: in the repository, in a private copy of the tree (natively or under wine), or in a copy rsynced to
another computer and run over ssh. Targets run in parallel, and each one runs the test suites of the projects in
PROJECTS, one project at a time, with a process for each.

Progress goes to stderr and the final synopsis to stdout. Logs and failure artifacts are kept in
tmp/run-testcases/<timestamp>/<target>/<project>/, with tmp/run-testcases/latest pointing at the newest run. The exit
status is 0 if every project passed on every target, 1 if any did not, and 2 for a configuration or usage error.
"""

from __future__ import annotations

import argparse
import dataclasses
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import tomllib
from pathlib import Path

# The root of the Ren'Py checkout this script belongs to.
REPO: Path = Path(__file__).resolve().parent.parent

# The configuration file used when --config is not given.
DEFAULT_CONFIG: Path = Path("~/.renpy/dev/testcases.toml")

# The directory, under the repository, that holds private trees and results. tmp/ is gitignored.
WORK_DIR: Path = REPO / "tmp" / "run-testcases"

# The saves and persistent directory of a target, relative to its tree. Without this, every run on a computer would
# share the directory named by config.save_directory. Each project has a directory of its own inside this one.
STAGED_SAVEDIR: str = ".test-saves"

# The projects with test suites, in the order they run. These are top-level directories of the repository.
PROJECTS: tuple[str, ...] = ("testcases", "tutorial", "the_question", "launcher")

# The kinds of target, which determine where a target runs and how it starts.
TARGET_TYPES: frozenset[str] = frozenset({"source", "local", "wine", "ssh"})

# The keys a target's table may contain. Others are rejected, so a misspelled key isn't silently ignored.
TARGET_KEYS: frozenset[str] = frozenset({
    "type",
    "enabled",
    "headless",
    "timeout",
    "env",
    "command",
    "sync",
    "prepare",
    "destination",
    "wineprefix",
})

# The timeout of each project's tests, in seconds, when the configuration does not give one.
DEFAULT_TIMEOUT: float = 900

# What gets copied to a target. This is the part of test_mac.sh's list that's needed to run testcases, the projects, and
# what the launcher's tests use: gui is the template for new projects, LICENSE.txt is put into the distributions they
# build, and sphinx holds the license they compare it to.
DEFAULT_SYNC: tuple[str, ...] = (
    "lib",
    "renpy",
    "renpy.py",
    "renpy.sh",
    "renpy.app",
    "sdk-fonts",
    "LICENSE.txt",
    "gui",
    "sphinx",
    *PROJECTS,
)

# Rsync filters for files a project generates, or that shouldn't leave this computer, like the_question's keystores.
PROJECT_FILTERS: tuple[str, ...] = (
    "--exclude=/screenshots/",
    "--exclude=/tmp/",
    "--exclude=*.rpyc",
    "--exclude=*.rpymc",
    "--exclude=*.rpyb",
    "--exclude=__pycache__/",
    "--exclude=*.pyc",
    "--exclude=*.keystore",
    "--exclude=/game/cache/",
    "--exclude=/game/saves/",
    "--exclude=log.txt",
    "--exclude=traceback.txt",
    "--exclude=errors.txt",
    "--exclude=lint.txt",
    "--exclude=image_cache.txt",
)

# Rsync filters for each item. They can't be global, as lib/ needs the .so and .pyc files excluded from renpy/. Excluded
# files are left alone on the destination, which keeps the per-target screenshot baselines. --delete-excluded can't be
# used, since it hangs the openrsync that comes with macOS, so CLEAN_GENERATED removes generated files instead.
SYNC_FILTERS: dict[str, tuple[str, ...]] = {
    # A Linux build in the source tree must not shadow the runtime in lib/.
    "renpy": ("--exclude=*.cpython-*.so", "--exclude=__pycache__/", "--exclude=*.pyc", "--exclude=*.pyo"),
    "testcases": ("--exclude=/pytests/", *PROJECT_FILTERS),
    "tutorial": PROJECT_FILTERS,
    "the_question": PROJECT_FILTERS,
    "launcher": PROJECT_FILTERS,
    "gui": PROJECT_FILTERS,
    # The documentation is large, and the launcher's tests only need this file.
    "sphinx": ("--include=/source/", "--include=/source/license.rst", "--exclude=*"),
}

# A shell command, run in a private tree before syncing, that removes what a previous run generated. Ren'Py would still
# load the .rpyc of a test whose .rpy has been deleted, and these files could also keep rsync from removing a directory.
CLEAN_GENERATED: str = (
    f"find {' '.join(PROJECTS)} gui "
    r"\( -name '*.rpyc' -o -name '*.rpymc' -o -name '*.rpyb' \) -delete 2>/dev/null; "
    "rm -rf " + " ".join(f"{i}/game/cache {i}/game/saves" for i in (*PROJECTS, "gui"))
)

# Rsync's exit status when source files vanished during the transfer, which doesn't hurt the files that matter.
RSYNC_VANISHED: int = 24

# The exit status of the ssh client when the connection, rather than the remote command, failed.
SSH_FAILED: int = 255

# Options that keep ssh from waiting forever on a prompt, an unreachable computer, or a connection that has died.
SSH_OPTIONS: tuple[str, ...] = (
    "-o",
    "BatchMode=yes",
    "-o",
    "ConnectTimeout=15",
    "-o",
    "ServerAliveInterval=15",
    "-o",
    "ServerAliveCountMax=4",
)

# How long to let a process group exit after SIGTERM, before using SIGKILL.
TERMINATE_GRACE: float = 5

# How many lines of output to show for a target that ended without a summary.
TAIL_LINES: int = 5

ANSI_RE: re.Pattern[str] = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
LINE_RE: re.Pattern[str] = re.compile(r"[\r\n]+")
COUNTS_RE: re.Pattern[str] = re.compile(
    r"^\[rpytest\] Test (?P<kind>cases|hooks|suites)\s*:\s*(?P<total>\d+)\s*\|\s*(?P<passed>\d+) passed\s*\|"
    r"\s*(?P<xfailed>\d+) xfailed\s*\|\s*(?P<failed>\d+) failed\s*\|\s*(?P<xpassed>\d+) xpassed\s*\|"
    r"\s*(?P<skipped>\d+) skipped\s*\|\s*(?P<not_run>\d+) not run"
)
PLATFORM_RE: re.Pattern[str] = re.compile(r"^\[rpytest\] Platform:\s*(.*?)\s*$")
STATUS_RE: re.Pattern[str] = re.compile(r"^\[rpytest\] Status:\s*(.*?)\s*$")
DETAILED_RE: re.Pattern[str] = re.compile(
    r"^\[rpytest\] (?P<indent> *)(?P<status>PASSED|XFAILED|FAILED|XPASSED|SKIPPED|NOT RUN|PENDING)\s+"
    r"(?P<name>.+?)(?:\s+- \(.*\))?\s*$"
)

# Set to abandon the run. Commands that are running are terminated.
cancelled: threading.Event = threading.Event()


class ConfigError(Exception):
    """
    The configuration or the command line is unusable. The message is meant to be shown to the user.
    """


class CommandTimeout(Exception):
    """
    A command ran past its timeout, and has been terminated.
    """


class Cancelled(Exception):
    """
    The user interrupted the run while a command was running, and the command has been terminated.
    """


@dataclasses.dataclass
class Target:
    """
    One place to run the testcases, as defined by a [target.<name>] table in the configuration.
    """

    name: str
    type: str
    headless: bool = False
    timeout: float = DEFAULT_TIMEOUT
    enabled: bool = True
    env: dict[str, str] = dataclasses.field(default_factory=dict)

    command: str | None = None
    "A shell command that replaces the default launch. Ren'Py's arguments are appended to it."

    sync: tuple[str, ...] = DEFAULT_SYNC
    prepare: str | None = None

    host: str | None = None
    "For ssh targets, the [user@]host part of the destination."

    path: str | None = None
    "For ssh targets, the path part of the destination, which is absolute or relative to the remote home directory."

    wineprefix: str | None = None

    @property
    def workdir(self) -> str:
        """
        The root of the tree this target runs in, on the computer it runs on.
        """

        if self.type == "source":
            return str(REPO)
        elif self.type == "ssh":
            return str(self.path)
        else:
            return str(WORK_DIR / "stage" / self.name)

    @property
    def savedir(self) -> str:
        """
        This target's saves and persistent directory, relative to its tree.
        """

        if self.type == "source":
            return f"tmp/run-testcases/saves/{self.name}"

        return STAGED_SAVEDIR

    def project_savedir(self, project: str) -> str:
        """
        The saves and persistent directory of a project on this target, relative to its tree. The projects must not
        share one, as the persistent data of each would overwrite the others'.
        """

        return f"{self.savedir}/{project}"


@dataclasses.dataclass
class Counts:
    """
    The figures from one row of the reporter's summary.
    """

    total: int = 0
    passed: int = 0
    xfailed: int = 0
    failed: int = 0
    xpassed: int = 0
    skipped: int = 0
    not_run: int = 0


@dataclasses.dataclass
class Report:
    """
    What could be learned from the output of a test run. This is None for runs that never printed a summary.
    """

    cases: Counts
    hooks: Counts
    suites: Counts
    status: str = ""
    platform: str = ""
    problems: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Result:
    """
    The outcome of one project on one target, which is a row of the synopsis.
    """

    name: str
    project: str
    status: str
    report: Report | None = None
    duration: float = 0
    detail: str = ""
    log: Path | None = None

    target_wide: bool = False
    "True if the target failed before it could run this project, so that the detail applies to all of its projects."


def strip_terminal_codes(text: str) -> str:
    """
    Removes the color and cursor codes that the console reporter emits, which a pty may also deliver with CRs.
    """

    return ANSI_RE.sub("", text)


def output_lines(text: str) -> list[str]:
    """
    Splits raw test output into clean lines, treating a CR as a line ending since ssh -tt adds them.
    """

    return LINE_RE.split(strip_terminal_codes(text))


def parse_output(text: str) -> Report | None:
    """
    Parses the output of `test --report-detailed`, returning None if the summary is missing, or a Report.

    The summary is printed when a run finishes, so a missing one means that the run died part way through.
    """

    counts: dict[str, Counts] = {}
    status = ""
    platform = ""
    problems: list[str] = []

    # The (depth, name, status) of the line in the detailed tree. A suite only has its own line, so only the leaves
    # are reported, using the suite.case form that test filters take.
    tree: list[tuple[int, str, str]] = []
    in_tree = False

    for line in output_lines(text):
        if line.startswith("[rpytest] Test outcomes (Detailed)"):
            in_tree = True
            tree = []
            continue

        if line.startswith("[rpytest] Test outcomes (Summary)"):
            in_tree = False
            continue

        if in_tree:
            m = DETAILED_RE.match(line)
            if m:
                tree.append((len(m["indent"]) // 2, m["name"], m["status"]))
            continue

        m = COUNTS_RE.match(line)
        if m:
            fields = {f.name: int(m[f.name]) for f in dataclasses.fields(Counts)}
            counts[m["kind"]] = Counts(**fields)
            continue

        m = STATUS_RE.match(line)
        if m:
            status = m[1]
            continue

        m = PLATFORM_RE.match(line)
        if m:
            platform = m[1]

    if "cases" not in counts:
        return None

    path: list[str] = []

    for i, (depth, name, line_status) in enumerate(tree):
        path[depth:] = [name]

        if line_status not in ("FAILED", "XPASSED"):
            continue

        is_leaf = i + 1 == len(tree) or tree[i + 1][0] <= depth
        if is_leaf:
            suffix = " (unexpected pass)" if line_status == "XPASSED" else ""
            # The root suite isn't part of the name that a filter uses.
            names = path[1:] if path[0] == "global" and len(path) > 1 else path
            problems.append(".".join(names) + suffix)

    return Report(
        cases=counts["cases"],
        hooks=counts.get("hooks", Counts()),
        suites=counts.get("suites", Counts()),
        status=status,
        platform=platform,
        problems=problems,
    )


def classify(returncode: int, report: Report | None) -> str:
    """
    Decides a finished run's status from its exit status and its parsed output.

    A run only passes if it says so as well as exiting with 0, because launching the game isn't a pass.
    """

    if report is None:
        return "CRASH"

    if returncode != 0 or report.status.upper() != "PASSED":
        return "FAIL"

    if report.cases.total == 0 or report.cases.failed or report.cases.xpassed or report.hooks.failed:
        return "FAIL"

    return "PASS"


def split_destination(name: str, destination: object) -> tuple[str, str]:
    """
    Splits an ssh target's <host>:<path> destination, refusing paths that rsync --delete must never be pointed at.
    """

    if not isinstance(destination, str) or ":" not in destination:
        raise ConfigError(f"Target {name}: destination must look like <user>@<host>:<path>.")

    host, _, path = destination.partition(":")
    path = path.rstrip("/")

    if path == "~" or path.startswith("~/"):
        path = path[2:]

    if not host or path in ("", "."):
        raise ConfigError(f"Target {name}: destination must name a dedicated directory, not {destination!r}.")

    if path == str(REPO):
        raise ConfigError(f"Target {name}: destination must not be a Ren'Py checkout, as syncing deletes files.")

    return host, path


def parse_target(name: str, table: dict[str, object], defaults: dict[str, object]) -> Target:
    """
    Turns a [target.<name>] table into a Target, raising ConfigError if it's not valid.
    """

    if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        raise ConfigError(f"Target name {name!r} may only contain letters, digits, '.', '_' and '-'.")

    unknown = set(table) - TARGET_KEYS
    if unknown:
        raise ConfigError(f"Target {name}: unknown key(s): {', '.join(sorted(unknown))}.")

    target_type = table.get("type")
    if target_type not in TARGET_TYPES:
        raise ConfigError(f"Target {name}: type must be one of: {', '.join(sorted(TARGET_TYPES))}.")

    def get(key: str, kind: type | tuple[type, ...], default: object = None) -> object:
        """
        Gets a value from the target or the defaults, checking its type.
        """

        value = table.get(key, defaults.get(key, default))

        if value is not None and (not isinstance(value, kind) or (kind is not bool and isinstance(value, bool))):
            raise ConfigError(f"Target {name}: {key} has the wrong type.")

        return value

    env = get("env", dict, {})
    if not all(isinstance(v, str) for v in env.values()):  # type: ignore
        raise ConfigError(f"Target {name}: the values of env must be strings.")

    sync = get("sync", list, list(DEFAULT_SYNC))
    if not all(isinstance(i, str) and i and "/" not in i and i != ".." for i in sync):  # type: ignore
        raise ConfigError(f"Target {name}: sync must list top-level files and directories of the repository.")

    target = Target(
        name=name,
        type=target_type,  # type: ignore
        enabled=get("enabled", bool, True),  # type: ignore
        headless=get("headless", bool, False),  # type: ignore
        timeout=get("timeout", (int, float), DEFAULT_TIMEOUT),  # type: ignore
        env=dict(env),  # type: ignore
        command=get("command", str),  # type: ignore
        sync=tuple(sync),  # type: ignore
        prepare=get("prepare", str),  # type: ignore
    )

    if target.timeout <= 0:
        raise ConfigError(f"Target {name}: timeout must be positive.")

    if target_type == "ssh":
        target.host, target.path = split_destination(name, table.get("destination"))
    elif "destination" in table:
        raise ConfigError(f"Target {name}: only ssh targets have a destination.")

    if target_type == "wine":
        wineprefix = get("wineprefix", str)
        if wineprefix is not None:
            target.wineprefix = str(Path(wineprefix).expanduser().absolute())  # type: ignore
    elif "wineprefix" in table:
        raise ConfigError(f"Target {name}: only wine targets have a wineprefix.")

    return target


def load_targets(path: Path) -> list[Target]:
    """
    Reads every target from the configuration file, raising ConfigError if it's missing or not valid.
    """

    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        example = REPO / "scripts" / "run_testcases.example.toml"
        raise ConfigError(f"{path} doesn't exist. To create it, copy and edit {example}.") from None
    except (OSError, tomllib.TOMLDecodeError) as e:
        raise ConfigError(f"Could not read {path}: {e}") from None

    unknown = set(data) - {"defaults", "target"}
    if unknown:
        raise ConfigError(f"{path}: unknown section(s): {', '.join(sorted(unknown))}.")

    defaults = data.get("defaults", {})
    unknown = set(defaults) - {"timeout", "headless"}
    if unknown:
        raise ConfigError(f"{path}: [defaults] may only set timeout and headless, not {', '.join(sorted(unknown))}.")

    return [parse_target(name, table, defaults) for name, table in data.get("target", {}).items()]


def select_targets(targets: list[Target], names: str | None) -> list[Target]:
    """
    Picks the targets to run: the comma-separated `names`, which may be disabled ones, or else all enabled targets.
    """

    if names:
        by_name = {t.name: t for t in targets}
        selected = []

        for name in names.split(","):
            if name not in by_name:
                raise ConfigError(f"Unknown target {name!r}. Known targets: {', '.join(by_name) or 'none'}.")
            selected.append(by_name[name])
    else:
        selected = [t for t in targets if t.enabled]

    if not selected:
        raise ConfigError("There are no targets to run.")

    if sum(t.type == "source" for t in selected) > 1:
        raise ConfigError("Only one source target can run at a time, since it runs in the repository itself.")

    return selected


def select_projects(names: str | None, filters: list[str]) -> list[str]:
    """
    Picks the projects to run: the comma-separated `names`, or else all of them. Test filters are specific to a
    project, and a filter that matches nothing fails the run, so they can only be used with a single project.
    """

    projects = list(dict.fromkeys(names.split(","))) if names else list(PROJECTS)

    for project in projects:
        if project not in PROJECTS:
            raise ConfigError(f"Unknown project {project!r}. Known projects: {', '.join(PROJECTS)}.")

    if filters and len(projects) != 1:
        raise ConfigError("Test filters are specific to a project, so use --project to name exactly one.")

    return projects


def build_launch(target: Target, index: int) -> str:
    """
    Returns the shell command that starts Ren'Py on a target, up to but not including Ren'Py's arguments.

    `index` is the target's position in this run, which keeps parallel virtual displays apart.
    """

    env = dict(target.env)

    if target.type == "wine":
        env.setdefault("WINEDEBUG", "-all")
        if target.wineprefix:
            env.setdefault("WINEPREFIX", target.wineprefix)

    if target.command:
        launch = target.command
    elif target.type == "source":
        launch = "./scripts/run-headless.sh" if target.headless else "./run.sh"
    elif target.type == "wine":
        launch = "wine lib/py3-windows-x86_64/python.exe renpy.py"
    else:
        launch = "./renpy.sh"

    unset = ""

    if target.headless and target.type != "source":
        # Without these, SDL prefers a Wayland session, and opens on the real desktop instead of the virtual display.
        # SDL under wine is a Windows build with no x11 driver, so it has to pick its own, which wine then runs on X11.
        # xvfb-run -a is racy when started in parallel, so each target searches from its own display number.
        unset = "-u WAYLAND_DISPLAY "

        if target.type == "wine":
            unset += "-u SDL_VIDEODRIVER -u SDL_VIDEO_DRIVER "
            env = {"SDL_AUDIODRIVER": "dummy", **env}
        else:
            env = {"SDL_AUDIODRIVER": "dummy", "SDL_VIDEODRIVER": "x11", "SDL_VIDEO_DRIVER": "x11", **env}

        launch = f"xvfb-run -a -n {100 + 10 * index} -s {shlex.quote('-screen 0 1920x1080x24')} {launch}"

    assignments = "".join(f"{k}={shlex.quote(v)} " for k, v in env.items())

    return f"env {unset}{assignments}{launch}"


def build_test_arguments(target: Target, project: str, filters: list[str]) -> list[str]:
    """
    Returns the arguments given to Ren'Py to run a project's testcases.
    """

    return [project, "--savedir", target.project_savedir(project), "test", "--report-detailed", *filters]


def build_run_script(target: Target, project: str, index: int, filters: list[str]) -> str:
    """
    Returns the POSIX shell script that clears the last run's leftovers and runs the tests, in place of the shell.

    The same script runs locally and over ssh. Leftovers are removed so that all artifacts come from this run.
    """

    arguments = " ".join(shlex.quote(i) for i in build_test_arguments(target, project, filters))

    return "; ".join([
        f"cd {shlex.quote(target.workdir)} || exit 125",
        f"rm -rf {shlex.quote(target.project_savedir(project))} {project}/traceback.txt {project}/errors.txt",
        f"find {project}/screenshots \\( -name '*.new.png' -o -name '*.diff.png' \\) -delete 2>/dev/null",
        f"exec {build_launch(target, index)} {arguments}",
    ])


def build_prepare_tree_script(target: Target) -> str:
    """
    Returns the POSIX shell script that creates a target's private tree, or clears what was generated in it last time.
    """

    workdir = shlex.quote(target.workdir)

    return f"mkdir -p {workdir} && cd {workdir} && {{ {CLEAN_GENERATED}; true; }}"


def build_run_argv(target: Target, project: str, index: int, filters: list[str]) -> list[str]:
    """
    Returns the local command line that runs a project's tests on a target.

    ssh gets a pty so that killing the client gives the remote process a SIGHUP, rather than leaving it running.
    """

    script = build_run_script(target, project, index, filters)

    if target.type == "ssh":
        return ["ssh", "-tt", *SSH_OPTIONS, str(target.host), script]

    return ["/bin/sh", "-c", script]


def rsync_base(target: Target) -> list[str]:
    """
    Returns the start of an rsync command line that talks to a target.

    Owners and groups mean nothing on another computer, and sending their names makes the openrsync that comes with
    macOS print a warning for each.
    """

    argv = ["rsync", "-a", "--no-owner", "--no-group", "--timeout=60"]

    if target.type == "ssh":
        argv += ["-e", shlex.join(["ssh", *SSH_OPTIONS])]

    return argv


def remote_path(target: Target, relative: str) -> str:
    """
    Returns the rsync spelling of a path inside a target's tree.
    """

    path = f"{target.workdir}/{relative}"

    if target.type == "ssh":
        return f"{target.host}:{path}"

    return path


def build_sync_argvs(target: Target) -> list[list[str]]:
    """
    Returns one rsync command per item that exists in the repository. A source target has nothing to sync.

    Removing from the destination is what keeps a deleted test from running again. It's why targets need a dedicated
    directory.
    """

    if target.type == "source":
        return []

    argvs = []

    for item in target.sync:
        source = REPO / item

        if not source.exists():
            continue

        argvs.append([
            *rsync_base(target),
            "--delete",
            *SYNC_FILTERS.get(item, ()),
            f"{source}/" if source.is_dir() else str(source),
            remote_path(target, item),
        ])

    return argvs


def build_collect_argvs(target: Target, project: str, directory: Path) -> list[list[str]]:
    """
    Returns the rsync commands that copy a project's logs and differing screenshots to the results directory.

    These commands fail harmlessly if there's nothing to collect. Each file gets its own command as
    --ignore-missing-args is too new for the rsync on some computers.
    """

    argvs = []

    for name in ("traceback.txt", "errors.txt", "log.txt"):
        argvs.append([*rsync_base(target), remote_path(target, f"{project}/{name}"), f"{directory}/"])

    argvs.append([
        *rsync_base(target),
        "--prune-empty-dirs",
        "--include=*/",
        "--include=*.new.png",
        "--include=*.diff.png",
        "--exclude=*",
        remote_path(target, f"{project}/screenshots/"),
        f"{directory}/screenshots/",
    ])

    return argvs


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    """
    Ends a command and everything it started, such as a game inside xvfb-run.
    """

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass

    try:
        process.wait(TERMINATE_GRACE)
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass

    process.wait()


def run_logged(
    argv: list[str],
    log: Path,
    timeout: float | None = None,
    env: dict[str, str] | None = None,
    cancellable: bool = True,
) -> int:
    """
    Runs a command in its own process group, appending its output to `log`, and returns its exit status.

    Raises CommandTimeout or Cancelled, once the command has been terminated, if it doesn't finish. If `cancellable`
    is False, the command keeps running after the run has been interrupted, which is what cleaning up needs.
    """

    deadline = None if timeout is None else time.monotonic() + timeout

    with log.open("ab") as output:
        process = subprocess.Popen(
            argv,
            cwd=REPO,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        while True:
            try:
                return process.wait(0.2)
            except subprocess.TimeoutExpired:
                pass

            if cancellable and cancelled.is_set():
                terminate_group(process)
                raise Cancelled

            if deadline is not None and time.monotonic() > deadline:
                terminate_group(process)
                raise CommandTimeout


def stop_wine(target: Target, log: Path) -> None:
    """
    Stops what remains of a wine target after it has been terminated, as wine processes outlive their process group.
    """

    if target.type != "wine":
        return

    env = dict(os.environ)
    if target.wineprefix:
        env["WINEPREFIX"] = target.wineprefix

    try:
        run_logged(["wineserver", "-k"], log, timeout=30, env=env, cancellable=False)
    except (CommandTimeout, OSError):
        pass


def report_progress(target: str, message: str) -> None:
    """
    Tells the user how a target is doing. This uses stderr, so that stdout holds just the synopsis.
    """

    print(f"[{target}] {message}", file=sys.stderr, flush=True)


def read_tail(log: Path) -> str:
    """
    Returns the last few non-empty lines of a log, which indicates why a run ended without a summary.
    """

    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

    lines = [i for i in output_lines(text) if i.strip()]

    return "\n".join(lines[-TAIL_LINES:])


def sync_target(target: Target, log: Path) -> str | None:
    """
    Copies the tree to a target, returning None if that succeeded, or a description of the failure.
    """

    if target.type == "source":
        WORK_DIR.mkdir(parents=True, exist_ok=True)
        return None

    if target.type == "ssh":
        status = run_logged(["ssh", *SSH_OPTIONS, str(target.host), build_prepare_tree_script(target)], log)
        if status != 0:
            return f"could not set up {target.workdir} on {target.host} (ssh exit status {status})"
    else:
        status = run_logged(["/bin/sh", "-c", build_prepare_tree_script(target)], log)
        if status != 0:
            return f"could not set up {target.workdir} (exit status {status})"

    for argv in build_sync_argvs(target):
        status = run_logged(argv, log)
        if status not in (0, RSYNC_VANISHED):
            return f"rsync of {argv[-2]} failed with exit status {status}"

    return None


def collect_artifacts(target: Target, project: str, directory: Path, log: Path) -> None:
    """
    Copies a project's logs and screenshots from a target's tree. Failing to do so doesn't change the project's result.
    """

    for argv in build_collect_argvs(target, project, directory):
        try:
            run_logged(argv, log, timeout=300)
        except (CommandTimeout, Cancelled, OSError):
            return


def make_target_errors(target: Target, projects: list[str], detail: str) -> list[Result]:
    """
    Makes the results of a target that failed before running any of its projects.
    """

    return [Result(target.name, project, "ERROR", detail=detail, target_wide=True) for project in projects]


def run_project(target: Target, project: str, index: int, filters: list[str], directory: Path, support: Path) -> Result:
    """
    Runs, collects from, and reports on a single project on a target that has been synced. This doesn't raise for
    anything that's the project's fault, so a broken project can't affect the others.
    """

    directory.mkdir(parents=True, exist_ok=True)

    label = f"{target.name}/{project}"
    output = directory / "output.txt"
    relative_output = output.relative_to(REPO) if output.is_relative_to(REPO) else output

    def error(detail: str, status: str = "ERROR", duration: float = 0) -> Result:
        """
        Makes the result of a run that has no test results.
        """

        return Result(target.name, project, status, duration=duration, detail=detail, log=relative_output)

    if cancelled.is_set():
        return error("interrupted")

    report_progress(label, "running tests")
    start = time.monotonic()

    try:
        returncode = run_logged(build_run_argv(target, project, index, filters), output, target.timeout)

    except CommandTimeout:
        stop_wine(target, support)
        collect_artifacts(target, project, directory, support)
        duration = time.monotonic() - start
        tail = read_tail(output)
        report_progress(label, "TIMEOUT")
        return error(f"timed out; see {relative_output}\n{tail}".rstrip(), "TIMEOUT", duration)

    except Cancelled:
        stop_wine(target, support)
        report_progress(label, "interrupted")
        return error("interrupted", duration=time.monotonic() - start)

    except OSError as e:
        report_progress(label, f"ERROR: {e}")
        return error(str(e), duration=time.monotonic() - start)

    duration = time.monotonic() - start

    if target.type == "ssh" and returncode == SSH_FAILED:
        report_progress(label, "ERROR: ssh failed")
        return error(f"ssh failed; see {relative_output}", duration=duration)

    collect_artifacts(target, project, directory, support)

    text = output.read_text(encoding="utf-8", errors="replace") if output.exists() else ""
    report = parse_output(text)
    status = classify(returncode, report)

    detail = ""
    if status == "CRASH":
        tail = read_tail(output)
        detail = f"exit status {returncode}, no test summary; see {relative_output}\n{tail}".rstrip()
    elif status == "FAIL":
        detail = f"exit status {returncode}; see {relative_output}"

    report_progress(label, f"{status} in {format_duration(duration)}")

    return Result(target.name, project, status, report, duration, detail, relative_output)


def run_target(target: Target, projects: list[str], index: int, filters: list[str], directory: Path) -> list[Result]:
    """
    Syncs a target and runs its projects one at a time, returning a result for each. Projects run on their own
    because their windows would take focus from each other. This doesn't raise for anything that's the target's fault,
    so a broken target can't affect the others.
    """

    directory.mkdir(parents=True, exist_ok=True)

    support = directory / "support.txt"

    try:
        if target.type != "source":
            report_progress(target.name, "syncing")

        failure = sync_target(target, support)

    except Cancelled:
        report_progress(target.name, "interrupted")
        return make_target_errors(target, projects, "interrupted")

    except OSError as e:
        report_progress(target.name, f"ERROR: {e}")
        return make_target_errors(target, projects, str(e))

    if failure:
        report_progress(target.name, f"ERROR: {failure}")
        return make_target_errors(target, projects, f"{failure}; see {support}")

    return [run_project(target, i, index, filters, directory / i, support) for i in projects]


def run_prepare_commands(targets: list[Target], directory: Path) -> dict[str, str]:
    """
    Runs the targets' prepare commands, one at a time, before anything is synced. Returns the targets that failed, as
    a mapping from target name to a description of the failure.

    These builds rewrite the lib/ that gets synced and can't share renpy-build, so they can't overlap. A command
    shared by several targets only runs once.
    """

    failures: dict[str, str] = {}
    outcomes: dict[str, str | None] = {}

    for target in targets:
        command = target.prepare
        if not command:
            continue

        if command not in outcomes:
            if cancelled.is_set():
                outcomes[command] = "interrupted"
                continue

            log = directory / f"prepare-{len(outcomes) + 1}.txt"
            report_progress("prepare", command)

            try:
                status = run_logged(["/bin/sh", "-c", command], log)
                outcomes[command] = None if status == 0 else f"`{command}` exited with {status}; see {log}"
            except Cancelled:
                outcomes[command] = "interrupted"
            except OSError as e:
                outcomes[command] = f"`{command}` failed: {e}"

        outcome = outcomes[command]
        if outcome:
            failures[target.name] = outcome

    return failures


def format_duration(seconds: float) -> str:
    """
    Formats a duration for the synopsis.
    """

    minutes, secs = divmod(round(seconds), 60)

    if minutes:
        return f"{minutes}m{secs:02d}s"

    return f"{secs}s"


def format_synopsis(results: list[Result]) -> str:
    """
    Formats the final report: a table with a row per project on each target, the problems found, and the overall
    result. A problem that stopped a whole target is only listed once.
    """

    rows = [("Target", "Project", "Status", "Passed", "Failed", "XFail", "Skip", "Time", "Platform")]

    for r in results:
        if r.report:
            cases = r.report.cases
            figures = [str(i) for i in (cases.passed, cases.failed + cases.xpassed, cases.xfailed, cases.skipped)]
        else:
            figures = ["-"] * 4

        platform = r.report.platform if r.report else ""
        rows.append((r.name, r.project, r.status, *figures, format_duration(r.duration), platform))

    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = []

    for row in rows:
        cells = [
            cell.rjust(width) if 3 <= i <= 6 else cell.ljust(width)
            for i, (cell, width) in enumerate(zip(row, widths))
        ]
        lines.append("  ".join(cells).rstrip())

    failures = []
    failed_targets = set()

    for r in results:
        if r.status == "PASS":
            continue

        if r.target_wide:
            if r.name in failed_targets:
                continue

            failed_targets.add(r.name)

        label = r.name if r.target_wide else f"{r.name}/{r.project}"

        if r.report:
            failures += [f"  {label}: {problem}" for problem in r.report.problems]

        first, *rest = (r.detail or r.status).split("\n")
        failures.append(f"  {label}: {first}")
        failures += [f"    {i}" for i in rest]

    if failures:
        lines += ["", "Failures:", *failures]

    passed = sum(r.status == "PASS" for r in results)
    overall = "PASS" if passed == len(results) else "FAIL"
    lines += ["", f"OVERALL: {overall} ({passed}/{len(results)} test runs passed)"]

    return "\n".join(lines)


def make_results_directory() -> Path:
    """
    Creates this run's results directory, and points the `latest` symlink at it.
    """

    stamp = time.strftime("%Y%m%d-%H%M%S")
    directory = WORK_DIR / stamp
    suffix = 1

    while directory.exists():
        suffix += 1
        directory = WORK_DIR / f"{stamp}-{suffix}"

    directory.mkdir(parents=True)

    latest = WORK_DIR / "latest"
    latest.unlink(missing_ok=True)
    latest.symlink_to(directory.name)

    return directory


def run_all(targets: list[Target], projects: list[str], filters: list[str], use_prepare: bool) -> list[Result]:
    """
    Prepares and then runs the given targets in parallel, returning a result for each project on each target, in the
    order they were given.

    If the run is cancelled, this stops every target and still returns a result for each of them.
    """

    directory = make_results_directory()
    report_progress("results", str(directory))

    results: dict[str, list[Result]] = {}
    threads = []

    def run_one(target: Target, index: int) -> None:
        """
        Runs one target on its own thread, reporting a bug in this script as that target's error.
        """

        try:
            results[target.name] = run_target(target, projects, index, filters, directory / target.name)
        except Exception as e:
            report_progress(target.name, f"ERROR: {e!r}")
            results[target.name] = make_target_errors(target, projects, repr(e))

    failures = run_prepare_commands(targets, directory) if use_prepare else {}

    for index, target in enumerate(targets):
        if target.name in failures:
            results[target.name] = make_target_errors(target, projects, failures[target.name])
            report_progress(target.name, "ERROR: prepare failed")
            continue

        if cancelled.is_set():
            results[target.name] = make_target_errors(target, projects, "interrupted")
            continue

        thread = threading.Thread(target=run_one, args=(target, index), name=target.name)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return [result for t in targets for result in results[t.name]]


def request_cancel(signum: int, frame: object) -> None:
    """
    Handles SIGINT and SIGTERM by asking the running commands to stop. Commands are in their own sessions, so they
    don't get a Ctrl-C from the terminal themselves.

    This must not raise KeyboardInterrupt. On Python 3.12, interrupting Thread.join() makes the thread look finished
    while it's still running, so the script would exit and leave the games running.
    """

    cancelled.set()


def main() -> int:
    """
    Runs the command line, returning the exit status.
    """

    ap = argparse.ArgumentParser(description="Run Ren'Py's functional testcases on several platforms at once.")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=f"The config file. Default: {DEFAULT_CONFIG}")
    ap.add_argument("-t", "--target", help="A comma-separated list of targets to run, which may be disabled ones.")
    ap.add_argument("-p", "--project", help=f"A comma-separated list of projects to run. Default: {','.join(PROJECTS)}")
    ap.add_argument("--list", action="store_true", help="List the configured targets, and exit.")
    ap.add_argument("--build", action="store_true", help="Run the targets' prepare commands before the tests.")
    ap.add_argument("--headless", action="store_true", help="Run every target on a virtual display with dummy audio.")
    ap.add_argument("--timeout", type=float, help="Override the timeout of each project's tests, in seconds.")
    ap.add_argument(
        "filters",
        nargs="*",
        help="Test filters, which require --project to name one project. Default: all tests. Use -- before them.",
    )
    args = ap.parse_args()

    try:
        targets = load_targets(args.config.expanduser())

        if args.list:
            for target in targets:
                suffix = "" if target.enabled else " (disabled)"
                print(f"{target.name}: {target.type}{' headless' if target.headless else ''}{suffix}")
            return 0

        if args.timeout is not None and args.timeout <= 0:
            raise ConfigError("--timeout must be positive.")

        selected = select_targets(targets, args.target)
        projects = select_projects(args.project, args.filters)

    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    for target in selected:
        target.headless = target.headless or args.headless
        if args.timeout is not None:
            target.timeout = args.timeout

    if not shutil.which("rsync") and any(t.type != "source" for t in selected):
        print("Error: rsync is required to run anything but a source target.", file=sys.stderr)
        return 2

    signal.signal(signal.SIGINT, request_cancel)
    signal.signal(signal.SIGTERM, request_cancel)

    results = run_all(selected, projects, args.filters, args.build)
    print(format_synopsis(results), flush=True)

    return 0 if all(r.status == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
