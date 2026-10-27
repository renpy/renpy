import pytest

import renpy
from renpy.display.layout import Null
from renpy.display.particle import SnowBlossom, SnowBlossomFactory


def midpoint(a, b):
    return (a + b) / 2


@pytest.fixture
def image():
    """The image each snow blossom is built from."""

    return Null()


def blossom(image, **kwargs):
    """Builds a four-particle blossom that falls straight down at 100 pixels per second."""

    return SnowBlossom(image, count=4, xspeed=0, yspeed=100, distribution=midpoint, **kwargs)


def assert_filled(blossom, st):
    """Checks that the blossom has all four particles started at time `st`, centered horizontally at the top."""

    assert len(blossom.particles) == 4
    for sprite, particle in blossom.particles:
        assert particle.start == st
        assert sprite.y == renpy.config.screen_height // 2


@pytest.mark.parametrize("animation", [False, True])
def test_fast_initializes_at_nonzero_time(image, animation):
    """
    With fast=True, the first update at a nonzero time starts all particles at that time, whether or not
    the blossom is animated.
    """

    snow = blossom(image, fast=True, animation=animation)
    snow.update_callback(5.0)
    assert_filled(snow, 5.0)


def test_fast_initializes_each_duplicate(image):
    """
    A duplicated blossom initializes its own particles at its own time, so a later duplicate started at
    a different time doesn't change the particles of the earlier one.
    """

    original = blossom(image, fast=True, animation=True)
    first = original._duplicate(None)
    first.update_callback(0.0)
    assert_filled(first, 0.0)

    second = original._duplicate(None)
    second.update_callback(5.0)
    assert_filled(second, 5.0)
    assert_filled(first, 0.0)


def test_fast_initializes_after_load(image):
    """
    After a save is loaded (after_setstate), the next update at a nonzero time reinitializes the
    particles, so loading doesn't leave the blossom in a stale state.
    """

    snow = blossom(image, fast=True, animation=True)
    snow.update_callback(0.0)
    snow.after_setstate()
    snow.update_callback(5.0)
    assert_filled(snow, 5.0)
    assert len(snow.sm.children) == 4


def test_fast_initializes_when_time_resets(image):
    """
    When the effect's time goes back to zero, as it does when the effect restarts, the particles are
    reinitialized at zero rather than continuing from the earlier time.
    """

    snow = blossom(image, fast=True)
    snow.update_callback(5.0)
    snow.update_callback(0.0)
    assert_filled(snow, 0.0)
    assert len(snow.sm.children) == 4


def test_fast_replacements_still_start_at_edge(image):
    """
    After the initial particles leave the screen, fast mode replaces them one at a time, and each
    replacement starts at the top edge (y == -50) at the current time rather than being filled all at once.
    """

    snow = blossom(image, fast=True)
    snow.update_callback(0.0)
    snow.update_callback(100.0)
    assert snow.particles == []

    snow.update_callback(101.0)
    assert len(snow.particles) == 1
    sprite, particle = snow.particles[0]
    assert particle.start == 101.0
    assert sprite.y == -50


def test_nonfast_preserves_gradual_start(image, mocker):
    """
    Without fast mode, particles start one at a time at the times given by the start offsets, so the
    particle count grows gradually. The random start offset is patched to the midpoint so the schedule is
    deterministic, and the patch is removed once the blossom is built.
    """

    uniform = mocker.patch("renpy.display.particle.random.uniform", side_effect=midpoint)
    snow = blossom(image, fast=False, start=10)
    mocker.stop(uniform)

    snow.update_callback(0.0)
    assert len(snow.particles) == 1
    assert snow.particles[0][0].y == -50
    snow.update_callback(1.0)
    assert len(snow.particles) == 1
    snow.update_callback(5.0)
    assert len(snow.particles) == 2


def test_factory_preserves_zero_time_initialization(image):
    """
    A SnowBlossomFactory in fast mode creates the full set of particles when asked to start at time zero
    with no existing particles.
    """

    factory = SnowBlossomFactory(image, 4, 0, 100, 50, 0, True, distribution=midpoint)
    assert len(factory.create([], 0.0)) == 4
