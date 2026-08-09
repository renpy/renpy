"""Move local branches to the Ren'Py archive repository.

Usage:
    python scripts/archive_branch.py BRANCH [BRANCH ...]

For each branch, this script verifies that the local branch contains any
matching archive or origin branch. It pushes the local branch to archive, then
deletes the local and origin branches after the archive push succeeds.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass

ARCHIVE_REMOTE = "archive"
ARCHIVE_URL = "git@github.com:renpy/archive.git"
ORIGIN_REMOTE = "origin"


class GitError(RuntimeError):
    """A Git command failed unexpectedly."""


@dataclass(frozen=True)
class Branch:
    name: str
    archive_exists: bool
    origin_exists: bool

    @property
    def local_ref(self) -> str:
        return f"refs/heads/{self.name}"

    def remote_ref(self, remote: str) -> str:
        return f"refs/remotes/{remote}/{self.name}"


def run_git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run Git without invoking a platform-specific shell."""

    result = subprocess.run(
        ["git", *arguments],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if check and result.returncode:
        command = " ".join(["git", *arguments])
        message = result.stderr.strip() or result.stdout.strip() or "Git command failed"
        raise GitError(f"{command}: {message}")

    return result


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("branches", nargs="+", metavar="BRANCH", help="Local branch to move to the archive")
    return parser.parse_args()


def ensure_archive_remote() -> None:
    """Configure the archive remote when it has not already been configured."""

    result = run_git("remote", "get-url", ARCHIVE_REMOTE, check=False)

    if result.returncode == 0:
        print(f"Using existing {ARCHIVE_REMOTE} remote: {result.stdout.strip()}")
        return

    run_git("remote", "add", ARCHIVE_REMOTE, ARCHIVE_URL)
    print(f"Added {ARCHIVE_REMOTE} remote: {ARCHIVE_URL}")


def remote_branch_exists(remote: str, branch: Branch) -> bool:
    """Return whether `branch` currently exists on `remote`."""

    result = run_git("ls-remote", "--exit-code", "--heads", remote, branch.local_ref, check=False)

    if result.returncode == 0:
        return True
    if result.returncode == 2:
        return False

    command = f"git ls-remote --exit-code --heads {remote} {branch.local_ref}"
    message = result.stderr.strip() or result.stdout.strip() or "Git command failed"
    raise GitError(f"{command}: {message}")


def fetch_branch(remote: str, branch: Branch) -> None:
    """Fetch one remote branch into its remote-tracking reference."""

    run_git("fetch", remote, f"+{branch.local_ref}:{branch.remote_ref(remote)}")


def fetch_local_branch(branch: Branch) -> None:
    """Fetch an origin branch into the matching local branch."""

    run_git("fetch", ORIGIN_REMOTE, f"{branch.local_ref}:{branch.local_ref}")


def local_branch_exists(branch: Branch) -> bool:
    """Return whether `branch` exists as a local branch."""

    return run_git("show-ref", "--verify", "--quiet", branch.local_ref, check=False).returncode == 0


def local_contains_remote(remote: str, branch: Branch) -> bool:
    """Return whether the local branch contains the remote branch."""

    result = run_git("merge-base", "--is-ancestor", branch.remote_ref(remote), branch.local_ref, check=False)

    if result.returncode in (0, 1):
        return result.returncode == 0

    command = f"git merge-base --is-ancestor {branch.remote_ref(remote)} {branch.local_ref}"
    message = result.stderr.strip() or result.stdout.strip() or "Git command failed"
    raise GitError(f"{command}: {message}")


def current_branch() -> str | None:
    """Return the checked-out branch name, or None for a detached HEAD."""

    result = run_git("symbolic-ref", "--quiet", "--short", "HEAD", check=False)

    if result.returncode == 0:
        return result.stdout.strip()
    if result.returncode == 1:
        return None

    message = result.stderr.strip() or result.stdout.strip() or "Git command failed"
    raise GitError(f"git symbolic-ref --quiet --short HEAD: {message}")


def preflight(branch_names: list[str]) -> list[Branch]:
    """Validate all branches before any archive push or deletion occurs."""

    if len(branch_names) != len(set(branch_names)):
        raise ValueError("A branch was specified more than once")

    checked_out = current_branch()
    branches = []

    for name in branch_names:
        branch = Branch(name, archive_exists=False, origin_exists=False)

        if name == checked_out:
            raise ValueError(f"Cannot archive the checked-out branch: {name}")

        archive_exists = remote_branch_exists(ARCHIVE_REMOTE, branch)
        origin_exists = remote_branch_exists(ORIGIN_REMOTE, branch)
        branch = Branch(name, archive_exists, origin_exists)

        if not origin_exists:
            raise ValueError(f"Branch does not exist on {ORIGIN_REMOTE}: {name}")

        if not local_branch_exists(branch):
            print(f"FETCH: {ORIGIN_REMOTE}/{name} -> local {name}")
            fetch_local_branch(branch)

        for remote, exists in ((ARCHIVE_REMOTE, archive_exists), (ORIGIN_REMOTE, origin_exists)):
            if not exists:
                print(f"CHECK: {name} does not exist on {remote}")
                continue

            fetch_branch(remote, branch)
            if not local_contains_remote(remote, branch):
                raise ValueError(f"Local branch {name} does not contain {remote}/{name}")

            print(f"CHECK: {name} contains {remote}/{name}")

        branches.append(branch)

    return branches


def archive_branch(branch: Branch) -> None:
    """Push one branch to archive and remove its local and origin copies."""

    print(f"PUSH: {branch.name} -> {ARCHIVE_REMOTE}/{branch.name}")
    run_git("push", ARCHIVE_REMOTE, f"{branch.local_ref}:{branch.local_ref}")

    print(f"DELETE: local {branch.name}")
    run_git("branch", "--delete", "--force", "--", branch.name)

    if branch.origin_exists:
        print(f"DELETE: {ORIGIN_REMOTE}/{branch.name}")
        run_git("push", ORIGIN_REMOTE, f":{branch.local_ref}")


def main() -> int:
    """Archive the requested branches."""

    arguments = parse_arguments()
    ensure_archive_remote()

    for branch in preflight(arguments.branches):
        archive_branch(branch)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GitError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
