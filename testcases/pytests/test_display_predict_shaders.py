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


"""Tests for how shaders are predicted from displayables and from renpy.start_predict_shader."""

from types import SimpleNamespace

import pytest

import renpy
import renpy.exports
from renpy.display import predict
from renpy.gl2 import gl2shadercache as shadercache


@pytest.fixture
def prediction_cache(mocker, tmp_path):
    """
    Installs a ShaderCache as the draw object's shader cache, with empty prediction state, and returns it.

    Prediction reads renpy.display.draw.shader_cache, and the pytest engine has no renderer, so a stand-in
    draw object holds the cache. The predict module's queues are replaced for the test, as is the set of
    registered shader parts, so the shaders registered here don't outlive it. The cache only records which
    shaders were predicted; nothing is compiled, so no GL context is needed.
    """

    cache = shadercache.ShaderCache(str(tmp_path / "shaders.txt"), True, 300)

    mocker.patch.object(renpy.display, "draw", SimpleNamespace(shader_cache=cache))
    mocker.patch.object(predict, "predicted", set())
    mocker.patch.object(predict, "predicted_displayables", [])
    mocker.patch.object(predict, "pending", [])
    mocker.patch.dict(shadercache.shader_part)

    renpy.exports.register_shader(
        "test_predict_shaders.modern",
        glsl=300,
        variables="uniform float u__amount;",
        fragment_600="fragment_color.rgb *= u__amount;\n",
    )

    renpy.exports.register_shader(
        "test_predict_shaders.legacy",
        glsl=100,
        variables="uniform float u__amount;",
        fragment_600="gl_FragColor.rgb *= u__amount;\n",
    )

    return cache


def prediction_key(*parts: str) -> tuple[str, ...]:
    """
    Returns the key the cache records for a shader built from `parts` and the default shader.
    """

    return tuple(sorted((renpy.config.default_shader,) + parts))


def test_displayable_prediction_composes_shaders_across_render_boundaries(prediction_cache) -> None:
    """
    Predicting a displayable predicts the shader of every render in its tree, with each render
    contributing the shaders of the displayables that draw into it.

    A transform around an AlphaMask around a model that has its own shaders produces three renders: the
    mask's, the model's texture, and the model itself. The shaders the transform adds apply to the mask
    render only, and the mask adds its own parts.
    """

    texture = renpy.display.imagelike.Solid("#fff")
    model = renpy.display.model.Model()
    model.texture(texture)
    model.shader("renpy.texture")
    model.shader("test_predict_shaders.legacy")

    mask = renpy.display.imagelike.Solid("#000")
    masked = renpy.display.layout.AlphaMask(model, mask)
    transform = renpy.display.transform.Transform(masked, alpha=0.5, shader="test_predict_shaders.modern")

    predict.displayable(transform)
    renpy.asynctask.run_sync(predict.predict_pending())

    assert list(prediction_cache.predicted) == [
        prediction_key("renpy.alpha", "renpy.mask", "test_predict_shaders.modern"),
        prediction_key("renpy.texture"),
        prediction_key("renpy.texture", "test_predict_shaders.legacy"),
    ]


def test_shader_prediction_can_be_started_and_stopped(mocker, prediction_cache) -> None:
    """
    renpy.start_predict_shader adds shader combinations to the set that is predicted every interaction,
    renpy.stop_predict_shader removes one, and predict_registered_shaders predicts what remains.

    A combination can be given as separate names or as one tuple. The store variable is replaced with an
    empty set so the test does not leave shaders registered for prediction. The API builds revertable
    sets, which record their mutations in the game's rollback log, so a real log is installed.
    """

    mocker.patch.object(renpy.store, "_predict_shader", set(), create=True)
    mocker.patch.object(renpy.game, "log", renpy.rollback.RollbackLog())

    legacy = ("renpy.texture", "test_predict_shaders.legacy")
    modern = ("renpy.texture", "test_predict_shaders.modern")

    renpy.exports.start_predict_shader(*legacy)
    renpy.exports.start_predict_shader(modern)
    assert renpy.store._predict_shader == {legacy, modern}

    renpy.exports.stop_predict_shader(legacy)
    assert renpy.store._predict_shader == {modern}

    renpy.asynctask.run_sync(predict.predict_registered_shaders())

    assert list(prediction_cache.predicted) == [prediction_key(*modern)]
