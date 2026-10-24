import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pytest

import setup as renpy_setup
from scripts.setuplib import _build_lock


def test_setup_holds_lock_through_build(mocker, monkeypatch):
    """
    main() takes the Cython build lock at tmp/.cython.lock and holds it for the whole of _build().

    The lock and build functions are replaced with recorders, so the test checks ordering only: locked,
    then build, then unlocked. main() changes the working directory to the repository base, so the test
    records the current directory with monkeypatch.chdir, which restores it at teardown.
    """

    events = []

    @contextmanager
    def record_lock(path):
        assert path == Path("tmp/.cython.lock")
        events.append("locked")
        try:
            yield
        finally:
            events.append("unlocked")

    def build():
        events.append("build")
        assert events == ["locked", "build"]

    monkeypatch.chdir(Path.cwd())
    lock_patch = mocker.patch.object(renpy_setup.setuplib, "_build_lock", record_lock)
    build_patch = mocker.patch.object(renpy_setup, "_build", build)
    renpy_setup.main()
    mocker.stop(build_patch)
    mocker.stop(lock_patch)

    assert events == ["locked", "build", "unlocked"]


def test_other_process_waits_for_build():
    """
    A second process that calls _build_lock on the same file blocks until the first releases the lock.

    The parent holds the real file lock while a child process tries to take it. The child must print
    'ready' and then keep running (the 0.2 second communicate timeout) instead of printing 'acquired'.
    Only after the parent releases the lock does the child print 'acquired' and exit with status 0.
    The timeout is used as a check that the child is blocked, not as a deadline for the lock itself.
    """

    root = Path(__file__).resolve().parents[1]
    child_code = (
        "import sys\n"
        "from pathlib import Path\n"
        "from scripts.setuplib import _build_lock\n"
        "print('ready', flush=True)\n"
        "with _build_lock(Path(sys.argv[1])):\n"
        "    print('acquired', flush=True)\n"
    )

    with tempfile.TemporaryDirectory(dir=root / "tmp") as directory:
        lock_path = Path(directory) / ".cython.lock"
        child = None
        try:
            with _build_lock(lock_path):
                child = subprocess.Popen(
                    [sys.executable, "-c", child_code, str(lock_path)],
                    cwd=root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                assert child.stdout is not None
                assert child.stdout.readline() == "ready\n"
                # communicate() keeps the partial state after a timeout, so the later call still collects output.
                with pytest.raises(subprocess.TimeoutExpired):
                    child.communicate(timeout=0.2)

            stdout, stderr = child.communicate(timeout=10)
            assert child.returncode == 0, stderr
            assert "acquired\n" in stdout
        finally:
            if child is not None and child.poll() is None:
                child.kill()
                child.communicate()
