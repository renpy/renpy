import subprocess
import sys
import tempfile
from collections.abc import Callable, Generator
from pathlib import Path

import pytest

import setup as renpy_setup
from scripts.setuplib import _build_lock

ROOT: Path = Path(__file__).resolve().parents[2]
"The repository root, which holds setup.py and the tmp/ directory."

CHILD_CODE: str = (
    "import sys\n"
    "from pathlib import Path\n"
    "from scripts.setuplib import _build_lock\n"
    "print('ready', flush=True)\n"
    "with _build_lock(Path(sys.argv[1])):\n"
    "    print('acquired', flush=True)\n"
)
"A child process that waits for the build lock at the path in argv[1], and prints 'acquired' once it has it."


@pytest.fixture
def start_waiter() -> Generator[Callable[[Path], subprocess.Popen[str]]]:
    """
    Factory that starts a child process trying to take the build lock at a path, waits until the child is about to,
    and returns it. Children still running at teardown are killed.
    """

    children = []

    def start(lock_path: Path) -> subprocess.Popen[str]:
        child = subprocess.Popen(
            [sys.executable, "-c", CHILD_CODE, str(lock_path)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        children.append(child)

        assert child.stdout is not None
        assert child.stdout.readline() == "ready\n"
        return child

    yield start

    for child in children:
        if child.poll() is None:
            child.kill()
            child.communicate()


def assert_blocked(child: subprocess.Popen[str]) -> None:
    """
    Asserts that `child` is still waiting for the lock, by checking that it keeps running for 0.2 seconds without
    exiting. communicate() keeps the partial output after a timeout, so a later call still collects all of it.
    """

    with pytest.raises(subprocess.TimeoutExpired):
        child.communicate(timeout=0.2)


def assert_acquires(child: subprocess.Popen[str]) -> None:
    """Asserts that `child` takes the lock and exits successfully, once the lock is released."""

    stdout, stderr = child.communicate(timeout=10)
    assert child.returncode == 0, stderr
    assert "acquired\n" in stdout


def test_other_process_waits_for_build(start_waiter):
    """
    A second process that calls _build_lock on the same file blocks until the first releases the lock.

    The parent holds the real file lock while a child process tries to take it. The timeout in assert_blocked is used
    as a check that the child is blocked, not as a deadline for the lock itself.
    """

    with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
        lock_path = Path(directory) / ".cython.lock"

        with _build_lock(lock_path):
            child = start_waiter(lock_path)
            assert_blocked(child)

        assert_acquires(child)


def test_setup_holds_lock_through_build(start_waiter, mocker, monkeypatch):
    """
    setup.main() holds the real build lock at tmp/.cython.lock while the build runs, and releases it afterwards, so
    a concurrent ./run.sh --build waits rather than compiling the same extensions at the same time.

    _build is replaced because it compiles every extension. The replacement starts a child process that tries to take
    the lock and checks that the child stays blocked. The lock file is the repository's own, so the test waits if a
    real build is running. main() changes the working directory to the repository root, and monkeypatch.chdir restores
    it at teardown.
    """

    lock_path = ROOT / "tmp" / ".cython.lock"
    children = []

    def build():
        child = start_waiter(lock_path)
        children.append(child)
        assert_blocked(child)

    monkeypatch.chdir(Path.cwd())
    mocker.patch.object(renpy_setup, "_build", build)

    renpy_setup.main()

    assert len(children) == 1
    assert_acquires(children[0])
