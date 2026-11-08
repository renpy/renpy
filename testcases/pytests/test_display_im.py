import threading

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


def visible_rects(render, xo=0, yo=0):
    """
    Returns the (x, y, width, height) of every surface blitted anywhere under a render, in the render's
    own coordinates, so tests can check where an image is drawn without depending on how the render tree
    is nested.
    """

    rects = []
    for child, x, y, _focus, _main in render.children:
        if isinstance(child, Render):
            rects.extend(visible_rects(child, xo + x, yo + y))
        else:
            rects.append((xo + x, yo + y, *child.get_size()))
    return rects


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


def test_uncached_texture_render_and_prediction_retain_nothing(mocker, cache, draw):
    """
    An uncached image is loaded afresh by every request and nothing is retained in the cache. Requesting
    it as a texture returns the texture that was loaded, rendering it returns a Render of the image's
    size, and predicting it returns None. Prediction never consults ready_one_texture, which is only used
    for cached textures, so the mock's earlier calls are cleared before predicting.
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

    draw.ready_one_texture.reset_mock()
    for _ in range(2):
        assert cache.get(image, predict=True, render=True) is None
    assert draw.load_texture.call_count == 4
    draw.ready_one_texture.assert_not_called()
    assert_uncached(cache)


def test_uncached_render_matches_cached_bounds_and_properties(mocker, cache):
    """
    With texture bounds optimization on, an uncached render and a cached render of the same image have the
    same size, draw the same visible rectangle, and have the same pixel_perfect property. The image has a
    transparent border, so the rectangle is the trimmed texture rather than the whole surface. Only the
    cached image leaves an entry in the cache. The patches are removed after the renders are built.
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
    assert [visible_rects(r) for r in renders] == [[(2, 1, 4, 4)], [(2, 1, 4, 4)]]
    assert [r.properties for r in renders] == [{"pixel_perfect": True}] * 2
    assert len(cache.cache) == 1


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


@pytest.mark.parametrize(
    ("premultiply", "mipmap", "properties"),
    [
        (True, None, {}),
        (False, None, {"premultiplied": True}),
        (True, False, {"mipmap": False}),
        (False, True, {"premultiplied": True, "mipmap": True}),
    ],
    ids=["default", "no-premultiply", "mipmap-false", "both"],
)
@pytest.mark.parametrize("raw", [False, True], ids=["image", "raw-texture"])
def test_texture_load_properties(cache, draw, raw, premultiply, mipmap, properties):
    """
    Loading an image as a texture passes premultiply and mipmap to load_texture as texture properties.

    premultiply=False is sent as premultiplied=True, which tells the loader the surface needs no
    premultiplication. mipmap=False must be sent explicitly rather than dropped, since leaving it out
    would fall back to config.mipmap. Runs on both a plain image and a RawTexture wrapping one.
    """

    if raw:
        image = im.UnoptimizedTexture(im.Null(), premultiply=premultiply, mipmap=mipmap)
    else:
        image = im.Null(premultiply=premultiply, mipmap=mipmap)

    cache.get(image, texture=True)
    assert draw.load_texture.call_args.kwargs == {"properties": properties}


def test_premultiply_setting_gets_separate_cache_entry(cache, draw):
    """
    RawTextures of the same image that differ only in premultiply are cached as separate entries with
    separate texture loads, so one never reuses a texture loaded with the other's setting.
    """

    premultiplied = im.UnoptimizedTexture(im.Null())
    raw = im.UnoptimizedTexture(im.Null(), premultiply=False)
    assert premultiplied.identity != raw.identity

    cache.get(premultiplied, texture=True)
    cache.get(raw, texture=True)
    assert len(cache.cache) == 2
    assert [call.kwargs for call in draw.load_texture.call_args_list] == [
        {"properties": {}},
        {"properties": {"premultiplied": True}},
    ]


def test_decode_pool_auto_size_without_cpu_count(mocker, cache):
    """
    With preload_threads set to 0 (auto), get_decode_pool must not raise when os.cpu_count() returns None, which the
    platform may do when the CPU count cannot be determined. It falls back to a single thread, so no pool is created.
    """

    mocker.patch.object(renpy.config, "preload_threads", 0)
    mocker.patch.object(im.os, "cpu_count", return_value=None)

    assert cache.get_decode_pool() is None


def test_new_thread_starts_from_config(mocker) -> None:
    """A new thread sees the current config value of raise_image_load_exceptions as its thread-local default."""
    values = []

    mocker.patch.object(renpy.config, "raise_image_load_exceptions", True)
    thread = threading.Thread(target=lambda: values.append(renpy.display.im.thread_local.raise_image_load_exceptions))
    thread.start()
    thread.join()

    assert values == [True]


################################################################################
# Preload pass
################################################################################


class TestPreloadPass:
    """Tests for when the image preload pass yields to the event loop, which only happens on the web."""

    @pytest.fixture
    def cache(self) -> im.Cache:
        """Provide a Cache without running its constructor, with no preloads and no decode pool."""
        cache = im.Cache.__new__(im.Cache)
        cache.preloads = []
        cache.keep_preloading = False
        cache.get_decode_pool = lambda: None
        cache.cleanout = lambda: True
        return cache

    @pytest.fixture
    def pauses(self, mocker) -> list[bool]:
        """Replace the predict sleep with a generator that records each pause, and return the record list."""
        pauses: list[bool] = []

        def pause():
            pauses.append(True)
            yield

        mocker.patch.object(renpy.display.predict, "predict_sleep", pause)
        return pauses

    def test_preload_yields_on_web(self, cache, pauses, mocker) -> None:
        """On the web, the preload pass pauses at least once so the browser's event loop keeps running."""
        mocker.patch.object(renpy, "emscripten", True)
        renpy.asynctask.run_sync(cache.preload_thread_pass())

        assert pauses

    def test_preload_does_not_yield_off_web(self, cache, pauses, mocker) -> None:
        """Off the web, the preload pass runs to completion without pausing."""
        mocker.patch.object(renpy, "emscripten", False)
        renpy.asynctask.run_sync(cache.preload_thread_pass())

        assert not pauses
