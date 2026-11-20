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


"""Tests for shader dialects, emitted source, and fallback in renpy.gl2.gl2shadercache."""

import pytest

import renpy
from renpy.gl2 import gl2shader
from renpy.gl2 import gl2shadercache as shadercache


@pytest.fixture
def shader_parts(mocker):
    """
    Restores the set of registered shader parts when the test ends, so parts a test creates don't leak.
    """

    mocker.patch.dict(shadercache.shader_part)


def test_undeclared_legacy_syntax_is_inferred_as_oldest_dialect(shader_parts) -> None:
    """
    A part that declares no dialect but uses gl_FragColor is treated as GLSL ES 1.00, so games written
    before dialects existed keep working.
    """

    part = shadercache.ShaderPart(
        "test_gl2_shadercache.undeclared",
        variables="uniform float u__amount;",
        fragment_600="gl_FragColor.rgb *= u__amount;\n",
    )

    assert part.glsl == shadercache.DIALECTS[0]


@pytest.mark.parametrize("gles, version", [(True, 300), (False, 330)])
def test_modern_fragment_output_has_explicit_location(gles: bool, version: int) -> None:
    """
    Fragment shaders emitted in the modern dialect declare their output with an explicit location, for
    both the GLES and desktop profiles.
    """

    text = shadercache.source([], [], [], True, gles, version)

    assert "layout(location = 0) out vec4 fragment_color;" in text


@pytest.mark.parametrize(
    "gles, version, expected",
    [(True, 100, True), (False, 120, False), (True, 300, False), (False, 330, False)],
)
def test_derivatives_enable_extension_in_gles_100(gles: bool, version: int, expected: bool) -> None:
    """
    A fragment shader using dFdx enables GL_OES_standard_derivatives when emitted as GLSL ES 1.00, where
    derivatives need it, and not in the other dialects, where they're built in. The blur shader uses
    derivatives to measure how small its texture is drawn.
    """

    parts = [(0, "test", "fragment_color = vec4(dFdx(v_tex_coord), 0.0, 1.0);\n", 300)]
    text = shadercache.source([], parts, [], True, gles, version)

    assert ("#extension GL_OES_standard_derivatives : require" in text) == expected


@pytest.mark.parametrize("interpolation", ["flat", "noperspective"])
def test_interpolation_requires_modern_dialect(shader_parts, interpolation: str) -> None:
    """
    A part that uses flat or noperspective interpolation can't run in the oldest dialect, even when it
    is written in it, and says which feature requires the newer one.
    """

    part = shadercache.ShaderPart(
        "test_gl2_shadercache.minimum_" + interpolation,
        glsl=100,
        variables=f"{interpolation} varying vec2 v_test;",
        vertex_100="v_test = vec2(0.0);",
        fragment_100="gl_FragColor = vec4(v_test, 0.0, 1.0);",
    )

    assert part.minimum_dialect == 300
    assert part.minimum_feature == f"{interpolation} interpolation on v_test"


def test_failed_fallback_preserves_version(mocker, shader_parts, tmp_path) -> None:
    """
    When a shader fails to build and the fallback build fails too, the error is raised and the cache keeps
    the version it started with, rather than staying lowered by the failed fallback.

    Program is replaced with a class whose load always fails, as the real one needs a GL context.
    """

    class FailingProgram:
        def __init__(self, *args) -> None:
            pass

        def load(self) -> None:
            raise gl2shader.ShaderError("test shader failure")

    name = "test_gl2_shadercache.fallback_failure"
    shadercache.ShaderPart(name, glsl=100)
    shadercache.ShaderPart(renpy.config.default_shader, glsl=100)  # The cache always adds the default shader.
    mocker.patch.object(gl2shader, "Program", FailingProgram)

    cache = shadercache.ShaderCache(str(tmp_path / "shaders.txt"), True, 300)

    with pytest.raises(gl2shader.ShaderError):
        cache.get((name,))

    assert cache.version == 300


@pytest.mark.parametrize(
    ("written", "expanded"),
    [("tex1__to_crop", "tex1_OP_to_crop"), ("tex0__res", "tex0_OP_res"), ("u_markup__res", "u_markup_OP_res")],
)
def test_operation_suffix_expands_for_tex_and_u_names(shader_parts, written: str, expanded: str) -> None:
    """
    A double-underscore operation suffix on a texN sampler expands like one on a u_ uniform, so shaders can
    write tex1__to_crop to get the transform into a cropped texture's coordinates. The expanded name is what
    the uniform setter parses the operation from.
    """

    part = shadercache.ShaderPart(
        "test_gl2_shadercache.operation_" + written,
        glsl=300,
        variables=f"uniform sampler2D tex0;\nuniform sampler2D tex1;\nuniform vec4 {written};",
        vertex_200=f"gl_Position.xy += {written}.xy;",
    )

    assert expanded in part.uniforms
    assert written not in part.uniforms
    assert any(expanded in text for _priority, _name, text in part.vertex_parts)
