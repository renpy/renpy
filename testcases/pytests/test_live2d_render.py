# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Live2D render caching with an optional, locally installed Cubism Core and model."""

import os
import sys
import weakref
from pathlib import Path
from types import SimpleNamespace

import pytest

import renpy
from renpy.display.render import Render

live2dmodel = pytest.importorskip("renpy.gl2.live2dmodel")


@pytest.fixture
def model(mocker):
    """
    Load a local model without a graphics context. Cubism and its sample models are not distributed
    with Ren'Py. RENPY_TEST_LIVE2D_CORE and RENPY_TEST_LIVE2D_MODEL can select an installed Core and
    .moc3 file; otherwise use the Core next to Python and the usual Mao sample location.
    """

    core_name = "Live2DCubismCore.dll" if renpy.windows else (
        "libLive2DCubismCore.dylib" if renpy.macintosh else "libLive2DCubismCore.so"
    )
    core = Path(os.environ.get("RENPY_TEST_LIVE2D_CORE", Path(sys.executable).parent / core_name))
    moc = Path(os.environ.get("RENPY_TEST_LIVE2D_MODEL", "testcases/game/live2d/Mao/Mao.moc3"))
    if not core.is_file() or not moc.is_file():
        pytest.skip("Requires a locally installed Cubism Core and model; see the model fixture.")

    assert live2dmodel.load(os.fsencode(core))
    mocker.patch.object(renpy.loader, "load", side_effect=lambda *args, **kwargs: moc.open("rb"))
    # Render construction needs the rasterization identity, but no OpenGL calls. Alter this token
    # below to simulate a window/context change independently of model parameters.
    loader = SimpleNamespace(token=object())
    loader.mask_cache_token = lambda: loader.token
    mocker.patch.object(renpy.display, "draw", SimpleNamespace(texture_loader=loader))
    result = live2dmodel.Live2DModel(moc.name)
    yield result, [Render(64, 64) for _ in range(32)], loader


def layers(render):
    """Collect mesh renders without following shared mask children more than once."""

    pending = [render]
    seen = set()
    result = []
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if current.mesh is not None and current.mesh is not True:
            result.append(current)
        pending.extend(child for child, *_ in current.children if isinstance(child, Render))
    return result


def masks(render):
    """Return the cropped mask used by each masked layer, including shared masks."""

    result = [layer.children[-1][0] for layer in layers(render)
              if layer.uniforms and "u_live2d_mask_bounds" in layer.uniforms]
    assert result, "The fixture model must contain visible masked drawables."
    return result


def test_mask_supports_weak_references():
    """Render itself cannot be weakly referenced; cached masks must use the weak-referenceable subclass."""

    mask = live2dmodel.Live2DMask(32, 32)
    assert weakref.ref(mask)() is mask


def test_unchanged_model_reuses_meshes_and_masks(model):
    """An unchanged Core evaluation must preserve mesh and mask identity to reuse uploaded GPU data."""

    native, textures, _ = model
    first = native.render(textures, 1.0)
    second = native.render(textures, 1.0)
    assert [layer.mesh for layer in layers(first)] == [layer.mesh for layer in layers(second)]
    assert masks(first) == masks(second)


def test_masks_are_cropped_to_geometry(model):
    """Small masks must not allocate another full-canvas texture; their shader bounds match the crop."""

    native, textures, _ = model
    render = native.render(textures, 1.0)
    cropped = masks(render)
    assert any(mask.width * mask.height < render.width * render.height / 4 for mask in cropped)
    for layer in layers(render):
        if not layer.uniforms or "u_live2d_mask_bounds" not in layer.uniforms:
            continue
        x, y, width, height = layer.uniforms["u_live2d_mask_bounds"]
        mask = layer.children[-1][0]
        assert 0 <= x <= 1 and 0 <= y <= 1
        assert mask.width == pytest.approx(width * render.width)
        assert mask.height == pytest.approx(height * render.height)


@pytest.mark.parametrize("change", ["textures", "zoom", "context", "killed"])
def test_mask_cache_invalidates(model, change):
    """Texture, zoom, rasterization and render-lifetime changes must not reuse stale mask textures."""

    native, textures, loader = model
    first = native.render(textures, 1.0)
    previous = masks(first)
    zoom = 1.0
    if change == "textures":
        textures = [Render(64, 64) for _ in textures]
    elif change == "zoom":
        zoom = 0.5
    elif change == "context":
        loader.token = object()
    else:
        for mask in previous:
            mask.kill()
    second = native.render(textures, zoom)
    assert not set(previous).intersection(masks(second))


def test_parameter_changes_preserve_old_renders(model):
    """Evaluating another instance of a shared Core model cannot mutate geometry in an existing Render."""

    native, textures, _ = model
    if "ParamAngleZ" not in native.parameters:
        pytest.skip("The fixture model has no ParamAngleZ parameter to deform its geometry.")
    first = native.render(textures, 1.0)
    old_meshes = [layer.mesh for layer in layers(first)]
    old_points = [mesh.get_points() for mesh in old_meshes]
    native.blend_parameter("ParamAngleZ", "Overwrite", native.parameters["ParamAngleZ"].maximum)
    second = native.render(textures, 1.0)
    assert set(old_meshes) != {layer.mesh for layer in layers(second)}
    assert [mesh.get_points() for mesh in old_meshes] == old_points
