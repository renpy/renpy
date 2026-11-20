import math
from types import SimpleNamespace

import pytest

import renpy
from renpy.display.matrix import Matrix, MatrixStack
from renpy.display.render import Render
from renpy.gl2.gl2draw import GL2Draw
from renpy.gl2.gl2model import GL2Model
from renpy.gl2.gl2texture import TextureLoader
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


class ResizeRecordingDraw(GL2Draw):
    """A GL2Draw that counts on_resize calls instead of rebuilding the OpenGL display."""

    resizes: int
    """The number of times on_resize was called."""

    def on_resize(self, first=False, full_reset=False):
        self.resizes += 1


@pytest.fixture
def update_environment(mocker, window_environment):
    """
    Returns a function that sets up GL2Draw.update to see a window of the given size, drawable size, SDL
    display scale and pixel density. The function returns a ResizeRecordingDraw whose stored state already
    matches that window, with a DPI scale of 1, and the mocked SDL window.
    """

    mocker.patch.object(testexecution, "get_test_window_size", return_value=None)
    window = mocker.patch.object(renpy.pygame.display, "get_window").return_value

    def setup(size, drawable_size, display_scale, pixel_density, fullscreen):
        window.get_window_flags.return_value = renpy.pygame.WINDOW_FULLSCREEN_DESKTOP if fullscreen else 0
        mocker.patch.object(renpy.display.core, "get_size", return_value=size)
        mocker.patch.object(renpy.pygame.display, "get_drawable_size", return_value=drawable_size)
        mocker.patch.object(renpy.pygame.display, "get_window_display_scale", return_value=display_scale)
        mocker.patch.object(renpy.pygame.display, "get_window_pixel_density", return_value=pixel_density)
        renpy.display.interface.fullscreen = fullscreen

        draw = ResizeRecordingDraw.__new__(ResizeRecordingDraw)
        draw.resizes = 0
        draw.dpi_scale = 1.0
        draw.physical_size = size
        draw.drawable_size = drawable_size
        draw.maximized = False
        return draw, window

    return setup


@pytest.mark.parametrize(
    "fullscreen, size, drawable_size",
    [(True, (1463, 914), (2560, 1600)), (False, (1361, 766), (2382, 1341))],
)
def test_update_ignores_pixel_density_rounding(update_environment, fullscreen, size, drawable_size):
    """
    With fractional scaling (Wayland at 175%), SDL computes the pixel density from the rounded window and
    drawable sizes, so it is slightly off from the display scale. That isn't a DPI change, so update must
    neither rebuild the display nor resize the window.

    The values are from issue #7529. Treating the difference as a change rebuilt the display every frame,
    leaving fullscreen black, and resized the window by a pixel each frame in windowed mode.
    """

    draw, window = update_environment(size, drawable_size, 1.75, 1.7501837015151978, fullscreen)

    assert draw.update() is False
    assert draw.resizes == 0
    window.resize.assert_not_called()
    assert draw.dpi_scale == 1.0


@pytest.mark.parametrize(
    "display_scale, pixel_density, expected_scale, expected_size",
    [
        (1.5, 1.0, 1.5, (1200, 900)),
        (3.5, 2.0002, 1.75, (1400, 1050)),
        (1.3, 1.0, 1.3, (1040, 780)),
    ],
)
def test_update_resizes_window_on_dpi_change(
    update_environment, display_scale, pixel_density, expected_scale, expected_size
):
    """
    When the window moves to a display with a different scale and the drawable doesn't scale to match,
    update resizes the window to keep its size on screen, records the new DPI scale, and rebuilds the display.

    A scale within rounding error of a multiple of 0.25 snaps to it (3.5 / 2.0002 becomes 1.75), so the
    window doesn't keep resizing as the rounding changes. Other scales, such as 1.3, are kept as they are.
    """

    draw, window = update_environment((800, 600), (800, 600), display_scale, pixel_density, False)

    assert draw.update() is True
    assert draw.dpi_scale == expected_scale
    window.resize.assert_called_once_with(expected_size, opengl=True, fullscreen=False, maximized=False)
    assert draw.resizes == 1


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


def test_mesh_oversample_ignores_translation(mocker):
    """
    A mesh drawn at twice its size is oversampled by 2 wherever it is drawn.

    The matrix here also moves the mesh by (300, 200). If the offset counted towards the scale,
    a mesh would be oversampled more the further it is moved, and would be rendered again each
    frame while it moves.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    render = Render(100, 50)
    render.blit(Render(100, 50), (0, 0))
    render.mesh = True

    matrix = [2, 0, 0, 300, 0, 2, 0, 200, 0, 0, 1, 0, 0, 0, 0, 1]

    draw = RecordingDraw.__new__(RecordingDraw)
    draw.oversamples = []
    draw.load_all_textures(render, MatrixStack(matrix))

    assert draw.oversamples == [2.0]


def perspective_stack(matrix):
    """Returns a MatrixStack holding `matrix`, viewed through the default perspective camera on a 1920x1080 screen."""

    stack = MatrixStack(None)
    stack.take(Matrix.perspective(1920, 1080, 100.0, 1000.0, 100000.0) * matrix)
    return stack


def projected_scale(matrix, x, y):
    """
    Returns how much `matrix` magnifies the diagonal at (x, y), found by projecting points on either side of it and
    dividing by w, in double precision. This is independent of how load_all_textures computes the scale.
    """

    columns = [matrix.transform(*basis, components=4) for basis in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1))]

    def project(u, v):
        point = [u * cu + v * cv + cw for cu, cv, cw in zip(*columns)]
        return point[0] / point[3], point[1] / point[3]

    h = 1e-3
    x0, y0 = project(x - h, y - h)
    x1, y1 = project(x + h, y + h)

    return math.hypot(x1 - x0, y1 - y0) / math.hypot(2 * h, 2 * h)


def record_oversamples(render, stack):
    """Loads the textures of `render` through `stack`, and returns the oversample each render-to-texture asked for."""

    draw = RecordingDraw.__new__(RecordingDraw)
    draw.oversamples = []
    draw.load_all_textures(render, stack)
    return draw.oversamples


def mesh_render(width, height):
    """Returns a mesh render with a child to render to a texture."""

    rv = Render(width, height)
    rv.blit(Render(width, height), (0, 0))
    rv.mesh = True
    return rv


@pytest.mark.parametrize(
    "z, scale, expected",
    [
        (0.0, 1.0, 1.0),
        (500.0, 1.0, 2.0),
        (0.0, 2.0, 2.0),
        (-1000.0, 4.0, 2.0),
        (2000.0, 1.0, 8.0),
    ],
)
def test_mesh_oversample_under_perspective(mocker, z, scale, expected):
    """
    A mesh seen through a perspective camera is oversampled by how much it's scaled on screen.

    With the 1:1 plane 1000 units from the camera, a mesh moved 500 units towards the camera is drawn twice as
    large, and one moved 1000 units away is drawn at half size. Without dividing by w, the camera's distance
    counts towards the scale, and every mesh is oversampled by config.mesh_oversample. A mesh behind the camera
    (z = 2000) can't be measured, and is oversampled as much as config.mesh_oversample allows.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    stack = perspective_stack(Matrix.offset(300, 200, z) * Matrix.scale(scale, scale, 1.0))

    assert record_oversamples(mesh_render(100, 50), stack) == [pytest.approx(expected, rel=1e-4)]


def test_mesh_oversample_uses_most_magnified_corner(mocker):
    """
    A mesh tilted towards a perspective camera is oversampled by the scale of its most magnified part.

    The mesh is turned about its left edge, so its right edge comes towards the camera and is drawn larger. The
    assertion that the corners differ guards against a rotation that leaves the scale the same everywhere.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    matrix = Matrix.offset(960, 540, 0) * Matrix.rotate(0, -60, 0)
    corners = [(0, 0), (400, 0), (0, 400), (400, 400)]
    scales = [projected_scale(perspective_stack(matrix), x, y) for x, y in corners]

    assert max(scales) > 1.2 * min(scales)

    oversamples = record_oversamples(mesh_render(400, 400), perspective_stack(matrix))

    assert oversamples == [pytest.approx(max(scales), rel=1e-3)]


def test_mesh_oversample_includes_blit_offset(mocker):
    """
    A mesh blitted away from its parent's origin is oversampled by the scale at the place it's drawn.

    The parent is tilted, so the mesh's blit offset moves it towards the camera. If the offset were ignored, the
    mesh would be measured at the parent's origin, where it would be drawn smaller.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    matrix = Matrix.offset(960, 540, 0) * Matrix.rotate(0, -60, 0)

    parent = Render(1000, 100)
    parent.blit(mesh_render(100, 100), (600, 0))

    placed = perspective_stack(matrix * Matrix.offset(600, 0, 0))
    expected = max(projected_scale(placed, x, y) for x in (0, 100) for y in (0, 100))
    unplaced = max(projected_scale(perspective_stack(matrix), x, y) for x in (0, 100) for y in (0, 100))

    assert expected > 1.2 * unplaced

    assert record_oversamples(parent, perspective_stack(matrix)) == [pytest.approx(expected, rel=1e-3)]


class StandInTexture(GL2Model):
    """A model standing in for the texture a render is rendered to, recording the oversample requested."""

    render_oversample: float
    texture_width: int
    texture_height: int

    def __init__(self, what, oversample):
        super().__init__((what.width, what.height), None, ("renpy.texture",), None)

        self.render_oversample = oversample
        self.texture_width = round(what.width * oversample)
        self.texture_height = round(what.height * oversample)


class StandInLoader(TextureLoader):
    """A TextureLoader that returns a stand-in for the texture it would render, as rendering needs OpenGL."""

    def render_to_texture(self, what, properties, oversample=1.0):
        return StandInTexture(what, oversample)


@pytest.fixture
def texture_draw():
    """Returns a GL2Draw that renders to stand-in textures, without initializing OpenGL."""

    draw = GL2Draw.__new__(GL2Draw)
    draw.texture_loader = StandInLoader.__new__(StandInLoader)
    return draw


@pytest.mark.parametrize("again", [2.0, 1.9999998909512358])
def test_render_to_texture_reuses_texture_at_same_oversample(texture_draw, again):
    """
    Rendering a render to a texture twice at the same oversample returns the first texture again.

    The second value is what a mesh at twice its size computes while it rotates, as the oversample
    comes from single-precision matrices. It must not cause the child to be rendered again each frame.
    """

    render = Render(100, 50)

    first = texture_draw.render_to_texture(render, oversample=2.0)

    assert texture_draw.render_to_texture(render, oversample=again) is first


def test_render_to_texture_replaces_texture_at_other_oversample(texture_draw):
    """
    A request at a different oversample gets a new texture at that oversample, which becomes the
    cached one.

    A mesh's child render can outlive the mesh, so without this a mesh that is zoomed in keeps the
    low resolution texture made when it was small.
    """

    render = Render(100, 50)

    first = texture_draw.render_to_texture(render, oversample=1.0)
    second = texture_draw.render_to_texture(render, oversample=2.0)

    assert second is not first
    assert second.render_oversample == 2.0
    assert texture_draw.render_to_texture(render, oversample=2.0) is second


def test_render_to_texture_keeps_texture_without_oversample(texture_draw):
    """
    A cached texture that was not rendered from the render, such as the loaded image that
    renpy.display.im assigns, is used at every oversample. Rendering it again would add no detail.
    """

    render = Render(100, 50)
    render.cached_texture = image = SimpleNamespace(render_oversample=None)

    assert texture_draw.render_to_texture(render, oversample=2.0) is image


def test_render_to_texture_without_oversample_shares_cached_texture(texture_draw):
    """
    A request with no oversample, as made for a render passed as a uniform, returns the cached
    texture whatever it was rendered at, and renders without oversampling when nothing is cached.

    Live2D passes the same render as the child of a mesh and as a uniform of another, and the
    uniform must get the mesh's oversampled texture instead of replacing it with a smaller one.
    """

    render = Render(100, 50)
    oversampled = texture_draw.render_to_texture(render, oversample=3.0)

    assert texture_draw.render_to_texture(render, oversample=None) is oversampled
    assert texture_draw.render_to_texture(Render(100, 50), oversample=None).render_oversample == 1.0


def test_render_used_as_child_and_uniform_shares_texture(mocker, texture_draw):
    """
    When a mesh drawn at twice its size uses one render as both its child and a uniform, the
    uniform gets the same oversampled texture as the child, so a shader sampling both sees the
    same pixels.
    """

    mocker.patch.object(renpy.config, "mesh_oversample", 8.0)

    child = Render(100, 50)
    render = Render(100, 50)
    render.blit(child, (0, 0))
    render.mesh = True
    render.add_uniform("u_other", child)

    texture_draw.load_all_textures(render, MatrixStack([2, 0, 0, 2]))

    model = render.cached_model

    assert model.get_texture(0).render_oversample == 2.0
    assert model.uniforms["u_other"] is model.get_texture(0)
