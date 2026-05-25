#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from pathlib import Path


PATH_IGNORE_RE = re.compile(r"(^|/)__pycache__(/|$)|(^|/)game/(saves|cache)(/|$)")
FILE_EXT_IGNORE_RE = re.compile(r"\.(pyc|pyo|rpyc|rpymc|so|pyi)$")
FILE_NAME_IGNORE_RE = re.compile(r"(^|/)(log\.txt|errors\.txt|errors\.text|traceback\.txt)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="compare_tree_with_git.py",
        description=(
            "Compares paths present in the working tree with paths tracked in git, "
            "and prints differences for both directories and files."
        ),
    )
    parser.add_argument("--repo", default=".", help="Repository path (defaults to current working directory)")
    parser.add_argument("--ref", default="HEAD", help="Git ref to compare against (defaults to HEAD)")
    return parser.parse_args()


def git_lines(repo: Path, *args: str) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in proc.stdout.splitlines() if line]


def is_repo(repo: Path) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def ignored_path(path: str) -> bool:
    return PATH_IGNORE_RE.search(path) is not None


def ignored_file(path: str) -> bool:
    return FILE_EXT_IGNORE_RE.search(path) is not None or FILE_NAME_IGNORE_RE.search(path) is not None


def top_level_only(paths: list[str]) -> list[str]:
    kept: list[str] = []

    for path in paths:
        if any(path.startswith(parent + "/") for parent in kept):
            continue

        kept.append(path)

    return kept


def list_working_tree(repo: Path) -> tuple[list[str], list[str]]:
    work_dirs: set[str] = set()
    work_files: set[str] = set()

    for p in repo.rglob("*"):
        rel = p.relative_to(repo).as_posix()

        if not rel:
            continue

        if rel == ".git" or rel.startswith(".git/"):
            continue

        if ignored_path(rel):
            continue

        if p.is_dir():
            work_dirs.add(rel)
            continue

        if p.is_file() and not ignored_file(rel):
            work_files.add(rel)

    return sorted(work_dirs), sorted(work_files)


def list_git_tree(repo: Path, ref: str) -> tuple[list[str], list[str]]:
    git_dirs = [p for p in git_lines(repo, "ls-tree", "-rd", "--name-only", ref) if not ignored_path(p)]
    git_files = [p for p in git_lines(repo, "ls-tree", "-r", "--name-only", ref) if not ignored_path(p) and not ignored_file(p)]
    return sorted(set(git_dirs)), sorted(set(git_files))


def set_diff(left: list[str], right: list[str]) -> list[str]:
    return sorted(set(left) - set(right))


def format_items(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    ref = args.ref

    if not is_repo(repo):
        print(f"Not a git repository: {repo}", file=sys.stderr)
        return 1

    try:
        work_dirs, work_files = list_working_tree(repo)
        git_dirs, git_files = list_git_tree(repo, ref)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr)
        return e.returncode

    dirs_only_work = top_level_only(set_diff(work_dirs, git_dirs))
    dirs_only_git = top_level_only(set_diff(git_dirs, work_dirs))

    files_only_work = set_diff(work_files, git_files)
    git_dir_set = set(git_dirs)
    files_only_work = [
        p
        for p in files_only_work
        if "/" not in p or p.rsplit("/", 1)[0] in git_dir_set
    ]
    files_only_git = set_diff(git_files, work_files)

    print("Comparing working tree with git tree")
    print(f"  repo: {repo}")
    print(f"  ref : {ref}")
    print()

    print("Directories only in working tree:")
    if dirs_only_work:
        print(format_items(dirs_only_work))

    print()
    print(f"Directories only in git ({ref}):")
    if dirs_only_git:
        print(format_items(dirs_only_git))

    print()
    print("Files only in working tree:")
    if files_only_work:
        print(format_items(files_only_work))

    print()
    print(f"Files only in git ({ref}):")
    if files_only_git:
        print(format_items(files_only_git))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
