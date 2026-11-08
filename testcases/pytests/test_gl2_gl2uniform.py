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


"""
Tests for renpy.gl2.gl2uniform, the code that sets shader uniforms.
"""

import pytest

from renpy.gl2.gl2uniform import SamplerSetter
from renpy.uguu import GL_TEXTURE_2D


@pytest.mark.parametrize(
    ("uniform_name", "suffix"),
    [("tex0", "tex0"), ("tex3", "tex3"), ("u_myuniform", "myuniform"), ("user_tex", "user_tex")],
)
def test_sampler_property_keys(uniform_name: str, suffix: str) -> None:
    """
    Per-sampler texture_wrap and texture_scaling properties are named after the sampler uniform, with the
    u_ prefix removed only when present. Model.texture(texture_wrap=...) sets texture_wrap_tex0 and friends,
    so the built-in tex samplers must keep their full names (#7486). A name like user_tex starts with "u"
    but not "u_", and must also be left alone. Constructing the setter makes no GL calls, so the getter and
    location can be placeholders.
    """

    setter = SamplerSetter(uniform_name, "sampler2D", 0, None, 0, GL_TEXTURE_2D)

    assert setter.texture_wrap_key == "texture_wrap_" + suffix
    assert setter.texture_scaling_key == "texture_scaling_" + suffix
