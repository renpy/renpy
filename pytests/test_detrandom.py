from types import SimpleNamespace

import pytest

import renpy
from renpy.revertable import DetRandom


@pytest.fixture
def recorded():
    """The current rollback log entry's list of random numbers, which DetRandom appends to."""

    return []


@pytest.fixture
def checkpoint_context():
    """A stand-in for the current context, used to observe whether DetRandom forces a checkpoint."""

    return SimpleNamespace(force_checkpoint=False)


@pytest.fixture(autouse=True)
def game_log(mocker, recorded, checkpoint_context):
    """Points renpy.game.log and renpy.game.context at the recorded list and checkpoint_context."""

    mocker.patch.object(renpy.game, "log", SimpleNamespace(current=SimpleNamespace(random=recorded)))
    mocker.patch.object(renpy.game, "context", lambda: checkpoint_context)


@pytest.fixture
def rng():
    """A DetRandom seeded with 12345."""

    rng = DetRandom()
    rng.seed(12345)
    return rng


def test_existing_seeded_sequences_are_unchanged(rng):
    """
    The seeded sequences from randint, choice, and randrange are unchanged.

    Games rely on seeded sequences being reproducible, so these values pin down the existing sequences
    and catch changes to DetRandom that would alter them.
    """

    assert [rng.randint(1, 100) for _ in range(10)] == [85, 42, 32, 31, 69, 29, 14, 99, 99, 62]
    assert [rng.choice("abcdefghij") for _ in range(10)] == list("giahdjfchd")
    assert [rng.randrange(3, 100, 7) for _ in range(10)] == [3, 66, 52, 80, 38, 31, 10, 3, 52, 10]


def test_getrandbits_records_and_replays(rng, recorded, checkpoint_context):
    """
    getrandbits records its randomness so rollback can replay it.

    Each call records one value per 32-bit chunk (widths straddle the 32 and 64 bit boundaries), forces
    a checkpoint, and returns a value in range. After pushing the recorded values back, the same calls
    return the same results, record the same values again, and drain the replay stack.
    """

    widths = (1, 31, 32, 33, 64, 127)
    values = [rng.getrandbits(k) for k in widths]
    old_recorded = recorded[:]

    assert len(old_recorded) == sum((k + 31) // 32 for k in widths)
    assert checkpoint_context.force_checkpoint

    for k, value in zip(widths, values):
        assert value >= 0
        assert value < 1 << k

    rng.pushback(old_recorded)
    recorded.clear()
    assert [rng.getrandbits(k) for k in widths] == values
    assert recorded == old_recorded
    assert rng.stack == []


def test_randbytes_records_and_replays(rng, recorded):
    """
    randbytes returns the requested number of bytes, records one value per 4 bytes, and replays the same
    bytes after the recorded values are pushed back. Includes a zero length, which records nothing.
    """

    lengths = (0, 1, 8, 17)
    values = [rng.randbytes(n) for n in lengths]
    old_recorded = recorded[:]

    assert [len(value) for value in values] == list(lengths)
    assert len(old_recorded) == sum((n + 3) // 4 for n in lengths)

    rng.pushback(old_recorded)
    recorded.clear()
    assert [rng.randbytes(n) for n in lengths] == values
    assert recorded == old_recorded


def test_zero_and_invalid_widths_do_not_consume_randomness(rng, recorded, checkpoint_context):
    """
    getrandbits(0) returns 0, and negative or non-integer widths raise like random.Random's.

    None of these may record a value or force a checkpoint. Otherwise a failed call would leave an extra
    value in the rollback log and shift every later replayed number.
    """

    assert rng.getrandbits(0) == 0

    for k in (-1, -32):
        with pytest.raises(ValueError):
            rng.getrandbits(k)

    with pytest.raises(TypeError):
        rng.getrandbits(1.5)

    assert recorded == []
    assert not checkpoint_context.force_checkpoint
