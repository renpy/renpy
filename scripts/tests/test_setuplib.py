import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from scripts.setuplib import _build_lock


def test_other_process_waits_for_build():
    """
    A second process that calls _build_lock on the same file blocks until the first releases the lock.

    The parent holds the real file lock while a child process tries to take it. The child must print
    'ready' and then keep running (the 0.2 second communicate timeout) instead of printing 'acquired'.
    Only after the parent releases the lock does the child print 'acquired' and exit with status 0.
    The timeout is used as a check that the child is blocked, not as a deadline for the lock itself.
    """

    root = Path(__file__).resolve().parents[2]
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
