"""
Tests for IOPath read buffering, and IOSubFile reading through a buffered IOPath.

Buffering is on by default only on Windows, so these tests pass `buffering` explicitly to exercise the
buffered stream on every platform. Each test compares the stream against an io.BytesIO holding the same data.
"""

import io
import random

import pytest

from renpy.pygame import iostream
from renpy.pygame.iostream import IOPath, IOSubFile

BUFFERINGS = [0, 1, 7, 16, 8192]


@pytest.fixture
def data():
    return random.Random(1234).randbytes(5000)


@pytest.fixture
def data_file(tmp_path, data):
    path = tmp_path / "data.bin"
    path.write_bytes(data)
    return path


@pytest.mark.parametrize("buffering", BUFFERINGS)
def test_read_chunks(data_file, data, buffering):
    """
    Reads of sizes smaller than, equal to, and larger than the buffer return the file's bytes in order.
    """

    rng = random.Random(buffering)

    with IOPath(data_file, buffering=buffering) as f:
        chunks = []

        while chunk := f.read(rng.choice([1, 3, 7, 16, 100, 4096])):
            chunks.append(chunk)

        assert b"".join(chunks) == data
        assert f.readinto(bytearray(10)) == 0
        assert f.read() == b""


@pytest.mark.parametrize("buffering", BUFFERINGS)
def test_read_seek_tell(data_file, data, buffering):
    """
    Seeks inside and outside the buffer, from every whence, interleaved with reads, match BytesIO.
    """

    rng = random.Random(buffering)
    model = io.BytesIO(data)

    with IOPath(data_file, buffering=buffering) as f:
        for _ in range(500):
            op = rng.randrange(4)

            if op == 0:
                size = rng.choice([1, 5, 16, 50, 3000])
                assert f.read(size) == model.read(size)
            elif op == 1:
                offset = rng.randrange(len(data) + 1)
                assert f.seek(offset) == model.seek(offset)
            elif op == 2:
                offset = rng.randrange(-20, 20)
                offset = max(offset, -model.tell())
                assert f.seek(offset, io.SEEK_CUR) == model.seek(offset, io.SEEK_CUR)
            else:
                offset = -rng.randrange(len(data) + 1)
                assert f.seek(offset, io.SEEK_END) == model.seek(offset, io.SEEK_END)

            assert f.tell() == model.tell()


def test_write_ignores_buffering(tmp_path, data):
    """
    Writes are not buffered by IOPath, so buffering is ignored in "wb" mode.
    """

    path = tmp_path / "out.bin"

    with IOPath(path, "wb", buffering=16) as f:
        assert f.buffering == 0
        assert f.write(data[:10]) == 10
        assert f.write(data[10:]) == len(data) - 10

    assert path.read_bytes() == data


@pytest.mark.parametrize("buffering", BUFFERINGS)
def test_subfile_from_iopath(data_file, data, buffering):
    """
    An IOSubFile over a buffered IOPath reads and seeks within its window, clamping at both ends.
    """

    base = 1000
    length = 2000
    model = io.BytesIO(data[base:base + length])

    with IOSubFile(IOPath(data_file, buffering=buffering), base=base, length=length) as f:
        assert f.read(10) == model.read(10)
        assert f.seek(-50, io.SEEK_END) == model.seek(-50, io.SEEK_END)
        assert f.read(100) == model.read(100)
        assert f.read(1) == b""

        assert f.seek(-100000, io.SEEK_CUR) == 0
        assert f.read() == data[base:base + length]


def test_subfile_from_path(data_file, data):
    """
    An IOSubFile opened from a path, which goes through IOPath, reads its window.
    """

    with IOSubFile(data_file, base=4000, length=2000) as f:
        assert f.read() == data[4000:]
        assert f.seek(10) == 10
        assert f.read(5) == data[4010:4015]


def test_buffering_argument(data_file):
    """
    The default buffering is the platform default, and negative buffering is rejected.
    """

    with IOPath(data_file) as f:
        assert f.buffering == iostream.IOPATH_DEFAULT_BUFFERING

    with IOPath(data_file, buffering=16) as f:
        assert f.buffering == 16
        assert "buffering=16" in repr(f)

    with pytest.raises(ValueError):
        IOPath(data_file, buffering=-1)


def test_buffered_refuses_write(data_file):
    """
    A buffered read stream refuses writes.
    """

    with IOPath(data_file, buffering=16) as f:
        with pytest.raises(io.UnsupportedOperation):
            f.write(b"x")
