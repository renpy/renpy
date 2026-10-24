import pytest

import renpy
from renpy.display import im
from renpy.display.render import Render

pytestmark = pytest.mark.usefixtures("surface_deallocation")


@pytest.fixture(autouse=True)
def draw(mocker):
    """
    A mock draw object that reports textures as not ready and returns the surface passed to load_texture
    unchanged, so the cache can be exercised without a graphics device. It is patched into every test.
    """

    draw = mocker.Mock()
    draw.ready_one_texture.return_value = False
    draw.load_texture.side_effect = lambda surface, **kwargs: surface
    mocker.patch.object(renpy.display, "draw", draw)
    return draw


@pytest.fixture
def cache(mocker):
    """
    An image cache built with renpy.emscripten set, which skips starting the preload thread. The flag is
    restored right after construction. Teardown clears the cache so no surfaces outlive the test.
    """

    emscripten = mocker.patch.object(renpy, "emscripten", True)
    cache = im.Cache()
    mocker.stop(emscripten)

    yield cache

    cache.cache.clear()


def assert_uncached(cache):
    """Checks that the cache holds no entries and reports zero total size."""

    assert cache.cache == {}
    assert cache.get_total_size() == 0


@pytest.mark.parametrize("cache_surfaces", [False, True])
def test_uncached_surface_reloads(mocker, cache, draw, cache_surfaces):
    """
    An image created with cache=False is reloaded on every get, returning a new surface each time, and
    leaves nothing in the cache. This holds whether or not config.cache_surfaces is set, since
    cache=False takes precedence.
    """

    mocker.patch.object(renpy.config, "cache_surfaces", cache_surfaces)
    image = im.Null(cache=False)
    first = cache.get(image)
    second = cache.get(image)
    assert isinstance(first, renpy.pygame.Surface)
    assert isinstance(second, renpy.pygame.Surface)
    assert first is not second
    assert_uncached(cache)
    draw.load_texture.assert_not_called()


def test_uncached_texture_and_image_render(mocker, cache, draw):
    """
    Requesting an uncached image as a texture loads it once and returns that texture. Rendering the same
    uncached image loads a second texture and returns a Render of the image's size, without retaining
    anything in the cache.
    """

    image = im.Null(cache=False)
    texture = cache.get(image, texture=True)
    draw.load_texture.assert_called_once()
    assert texture is draw.load_texture.call_args.args[0]

    cache_patch = mocker.patch.object(im, "cache", cache)
    render = image.render(100, 100, 0, 0)
    mocker.stop(cache_patch)

    assert isinstance(render, Render)
    assert render.get_size() == (1, 1)
    assert draw.load_texture.call_count == 2
    assert_uncached(cache)


def test_uncached_render_matches_cached_bounds_and_properties(mocker, cache, draw):
    """
    With texture bounds optimization on, an uncached render and a cached render of the same image produce
    the same size, child offset, child surface size, and pixel_perfect property. Only one entry lands in
    the cache, from the cached image. Texture loads from both use the mipmap property. The patches are
    removed after the renders are built.
    """

    surface = renpy.pygame.Surface((12, 8))
    surface.fill((0, 0, 0, 0))
    surface.fill((255, 255, 255, 255), (4, 2, 4, 4))
    patches = [
        mocker.patch.object(renpy.config, "optimize_texture_bounds", True),
        mocker.patch.object(renpy.config, "expand_texture_bounds", 0),
        mocker.patch.object(im.Null, "load", return_value=surface),
        mocker.patch.object(im.Null, "pixel_perfect", True),
    ]
    renders = [
        cache.get(im.Null(cache=use_cache, mipmap=True, oversample=2), render=True) for use_cache in (False, True)
    ]
    for patched in patches:
        mocker.stop(patched)

    assert [r.get_size() for r in renders] == [(6, 4), (6, 4)]
    assert [r.children[0][1:3] for r in renders] == [(2, 1), (2, 1)]
    assert [r.children[0][0].get_size() for r in renders] == [(4, 4), (4, 4)]
    assert [r.properties for r in renders] == [{"pixel_perfect": True}] * 2
    assert len(cache.cache) == 1
    for call in draw.load_texture.call_args_list:
        assert call.kwargs == {"properties": {"mipmap": True}}


def test_uncached_prediction_does_not_retain_texture(cache, draw):
    """
    Predicting an uncached image loads its texture each time but returns None and retains nothing, and
    it never consults ready_one_texture, which is only used for cached textures.
    """

    image = im.Null(cache=False)
    for _ in range(2):
        assert cache.get(image, predict=True, render=True) is None
        assert_uncached(cache)
    assert draw.load_texture.call_count == 2
    draw.ready_one_texture.assert_not_called()


def test_uncached_images_do_not_log_cache_changes(mocker, cache):
    """
    Uncached images, whether fetched, predicted, or rendered, don't write to the image cache debug log,
    even with config.debug_image_cache enabled, because they never enter the cache.
    """

    mocker.patch.object(renpy.config, "debug_image_cache", True)
    mocker.patch.object(renpy.config, "cache_surfaces", False)
    log = mocker.patch.object(renpy.display, "ic_log")

    image = im.Null(cache=False)
    cache.get(image)
    cache.get(image, predict=True, render=True)
    cache.get(image, render=True)
    log.write.assert_not_called()
    assert_uncached(cache)


def test_cached_prediction_is_reused_for_rendering(cache, draw):
    """
    Predicting a cached image loads its texture once, and later render requests reuse that texture and
    its entry instead of loading again. The cache holds one entry with a nonzero total size.
    """

    image = im.Null()
    assert cache.get(image, predict=True, render=True) is None
    first = cache.get(image, render=True)
    second = cache.get(image, render=True)
    assert isinstance(first, Render)
    assert isinstance(second, Render)
    assert first.children[0][0] is second.children[0][0]
    draw.load_texture.assert_called_once()
    assert len(cache.cache) == 1
    assert cache.get_total_size() > 0
