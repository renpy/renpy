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


"""Tests for how shader variable declarations are validated and emitted in renpy.gl2.gl2shader."""

import pytest

import renpy
from renpy.gl2.gl2shader import ShaderError, Variable


def test_shader_parts_may_not_declare_layout_qualifiers() -> None:
    """
    A shader part can't declare its own layout-qualified output, as Ren'Py emits the one fragment output
    (with an explicit location) itself.
    """

    with pytest.raises(ShaderError, match="additional fragment output"):
        Variable("test_gl2_shader.output", "layout(location = 1) out vec4 user_output;")


@pytest.mark.parametrize(
    "fragment, gles, version, expected",
    [
        (False, True, 300, "invariant out vec2 v_test"),
        (True, True, 300, "in vec2 v_test"),
        (False, False, 330, "invariant out vec2 v_test"),
        (True, False, 330, "invariant in vec2 v_test"),
    ],
)
def test_invariant_varying_declaration(fragment: bool, gles: bool, version: int, expected: str) -> None:
    """
    An invariant varying is emitted for each profile and stage. GLSL ES 3.00 allows invariant only on the
    vertex output, so its fragment input is plain; desktop GLSL requires the matching input to be invariant.
    """

    variable = Variable("test_gl2_shader.invariant", "invariant out vec2 v_test;")

    assert variable.declaration(fragment, gles, version) == expected


def test_invariant_requires_a_varying() -> None:
    """
    Qualifying anything other than a varying as invariant is a clear ShaderError.
    """

    with pytest.raises(ShaderError, match="only qualify a varying"):
        Variable("test_gl2_shader.invariant", "invariant uniform float u_test;")


@pytest.fixture
def messages(mocker) -> list[str]:
    """
    Collects what the shader code writes to the display log, instead of writing it to log.txt.
    """

    rv: list[str] = []

    def write(message: str, *args) -> None:
        rv.append(message % args if args else message)

    mocker.patch.object(renpy.display.log, "write", write)

    return rv


def test_unsupported_interpolation_is_dropped_and_logged_once(mocker, messages: list[str]) -> None:
    """
    Outside developer mode, an interpolation qualifier the dialect doesn't support is dropped from the
    declaration, and logged once for each variable and not on every emission.

    flat needs GLSL 3.00 and noperspective needs desktop GL, so each is unsupported somewhere.
    """

    mocker.patch.object(renpy.config, "developer", False)

    flat = Variable("test_gl2_shader.interpolation", "flat out vec2 v_flat;")
    assert flat.declaration(False, True, 300) == "flat out vec2 v_flat"
    assert flat.declaration(False, True, 100) == "varying vec2 v_flat"
    assert len(messages) == 1
    assert "flat interpolation" in messages[0]

    assert flat.declaration(False, True, 100) == "varying vec2 v_flat"
    assert len(messages) == 1

    noperspective = Variable("test_gl2_shader.interpolation", "noperspective out vec2 v_noperspective;")
    assert noperspective.declaration(False, False, 330) == "noperspective out vec2 v_noperspective"
    assert noperspective.declaration(False, True, 300) == "out vec2 v_noperspective"
    assert len(messages) == 2
    assert "noperspective interpolation" in messages[1]


@pytest.mark.parametrize(
    "interpolation, gles, version",
    [
        ("flat", True, 100),
        ("noperspective", True, 300),
    ],
)
def test_unsupported_interpolation_fails_in_developer_mode(
    mocker, interpolation: str, gles: bool, version: int
) -> None:
    """
    In developer mode, an interpolation qualifier the dialect doesn't support raises a ShaderError that
    names it, so the problem is found during development rather than silently changing the rendering.
    """

    mocker.patch.object(renpy.config, "developer", True)

    variable = Variable("test_gl2_shader.interpolation", f"{interpolation} out vec2 v_test;")

    with pytest.raises(ShaderError, match=f"{interpolation} interpolation"):
        variable.declaration(False, gles, version)
