import threading

import pytest

from renpy import savelocation


@pytest.fixture
def location():
    """A bare FileLocation that already holds persistent data with mtime 1, without scanning the disk."""

    location = savelocation.FileLocation.__new__(savelocation.FileLocation)
    location.persistent_mtime = 1
    location.persistent_data = "old data"
    return location


@pytest.mark.parametrize("consume", [False, True])
def test_load_waits_for_scan_publication(location, consume):
    """
    load_persistent waits for disk_lock, so it returns the data the scan thread publishes rather than
    the stale data visible before.

    The test holds disk_lock as the scan thread does while it updates the mtime and data, and checks
    that the loader has started but has not finished within 20 ms. With consume=True the loaded data is
    also cleared from the location; otherwise it stays.
    """

    started = threading.Event()
    finished = threading.Event()
    results = []

    def load():
        started.set()
        try:
            results.extend(location.load_persistent(consume=consume))
        finally:
            finished.set()

    worker = threading.Thread(target=load)
    try:
        with savelocation.disk_lock:
            worker.start()
            assert started.wait(2)
            assert not finished.wait(0.02)
            location.persistent_mtime = 2
            location.persistent_data = "new data"
    finally:
        worker.join(2)

    assert not worker.is_alive()
    assert results == [(2, "new data")]
    assert location.persistent_data == (None if consume else "new data")


def test_consume_is_once_and_lock_is_reentrant(location):
    """
    Data loaded with consume=True is returned only once, and load_persistent works while the caller
    already holds disk_lock.

    disk_lock must be reentrant, or the nested acquisition inside load_persistent would deadlock. The
    mtime is left alone when the data is consumed.
    """

    with savelocation.disk_lock:
        assert location.load_persistent() == [(1, "old data")]
        assert location.load_persistent(consume=True) == [(1, "old data")]
        assert location.load_persistent(consume=True) == []

    assert location.persistent_mtime == 1
