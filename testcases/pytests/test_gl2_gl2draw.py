from types import SimpleNamespace

import pytest

import renpy
from renpy.display.matrix import MatrixStack
from renpy.display.render import Render
from renpy.gl2.gl2draw import GL2Draw
from renpy.gl2.gl2model import GL2Model
from renpy.test import testexecution


def make_draw(dpi_scale, info):
    """Creates a GL2Draw with an 800x600 virtual size without initializing OpenGL."""

    draw = GL2Draw.__new__(GL2Draw)
    draw.virtual_size = (800, 600)
    draw.dpi_scale = dpi_scale
    draw.info = info
    return draw


@pytest.fixture
def window_environment(mocker):
    """
    Replaces the player's preferences, the interface, and display logging, so window sizing can run
    without a game. Returns the mocked preferences.
    """

    preferences = mocker.patch.object(renpy.game, "preferences")
    mocker.patch.object(renpy.display, "interface")
    mocker.patch.object(renpy.display.log, "write")
    return preferences


def test_resize_ignores_saved_size_dpi_and_fullscreen(mocker, window_environment):
    """
    With a test window size, resize uses exactly that size in a plain window.

    The player's saved size, fullscreen, and maximized preferences are ignored, the DPI scale is reset
    to 1, and a maximum window size smaller than the test size doesn't shrink it. Otherwise click
    coordinates in tests would depend on the machine running them.
    """

    draw = make_draw(2.0, {"max_window_size": (640, 480)})
    mocker.patch.object(testexecution, "get_test_window_size", return_value=(800, 600))
    get_window = mocker.patch.object(renpy.pygame.display, "get_window")
    window_environment.fullscreen = True
    window_environment.maximized = True
    window_environment.physical_size = (1920, 1080)

    draw.resize()

    assert draw.dpi_scale == 1.0
    get_window.return_value.resize.assert_called_once_with((800, 600), opengl=True, fullscreen=False, maximized=False)


def test_initial_size_ignores_display_limits_and_dpi(mocker, window_environment):
    """
    With a test window size, the initial physical size is the test size even when the display is
    smaller (640x480) and a larger size was requested.

    The DPI scale is reset to 1, and the maximum window size is raised to the test size so later
    resizes are not clamped.
    """

    draw = make_draw(2.0, {})
    mocker.patch.object(testexecution, "get_test_window_size", return_value=(800, 600))
    mocker.patch.object(renpy.game, "interface")
    mocker.patch.object(renpy.display, "get_info", return_value=SimpleNamespace(current_w=640, current_h=480))
    mocker.patch.object(renpy.pygame.display, "get_surface", return_value=None)
    mocker.patch.object(renpy.pygame.display, "get_display_bounds", return_value=[(0, 0, 640, 480)])
    window_environment.maximized = False

    assert draw.select_physical_size((1920, 1080)) == (800, 600)
    assert draw.dpi_scale == 1.0
    assert draw.info["max_window_size"] == (800, 600)


def test_normal_resize_keeps_existing_policy(mocker, window_environment):
    """
    Without a test window size, resize still follows the player's preferences: the saved size, and
    fullscreen when it is enabled. Maximized is not requested while fullscreen.
    """

    draw = make_draw(1.0, {"max_window_size": (1920, 1080)})
    mocker.patch.object(testexecution, "get_test_window_size", return_value=None)
    get_window = mocker.patch.object(renpy.pygame.display, "get_window")
    window_environment.fullscreen = True
    window_environment.maximized = True
    window_environment.physical_size = (1024, 768)

    draw.resize()

    get_window.return_value.resize.assert_called_once_with((1024, 768), opengl=True, fullscreen=True, maximized=False)


class RecordingDraw(GL2Draw):
    """A GL2Draw that records the oversample each render-to-texture asks for, as drawing needs OpenGL."""

    oversamples: list[float]
    """The oversample of each render-to-texture, in the order they were requested."""

    def render_to_texture(self, what, alpha=True, properties=None, oversample=1.0):
        self.oversamples.append(oversample)
        return GL2Model((what.width, what.height), None, ("renpy.texture",), None)


@pytest.mark.parametrize("mesh_oversample, expected", [(True, 2.0), (False, 1.0)])
def test_mesh_oversample_property_disables_oversampling(mocker, mesh_oversample, expected):
    """
    A mesh drawn at twice its size has its texture oversampled by 2, unless its mesh_oversample
    property is false.

    Blurred transforms set that property, as resizing the texture while the zoom animates makes
    the blur shake. config.mesh_oversample is patched so its limit is above the 2x scale.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    render = Render(100, 50)
    render.blit(Render(100, 50), (0, 0))
    render.mesh = True
    render.add_property("mesh_oversample", mesh_oversample)

    draw = RecordingDraw.__new__(RecordingDraw)
    draw.oversamples = []
    draw.load_all_textures(render, MatrixStack([2, 0, 0, 2]))

    assert draw.oversamples == [expected]
