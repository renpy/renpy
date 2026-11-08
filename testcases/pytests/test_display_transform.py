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


"""Tests for how transform state is copied between transforms in renpy.display.transform."""

from renpy.display import transform
from renpy.display.transform import TransformState


def test_take_state_copies_only_uniforms_set_on_the_source(mocker) -> None:
    """
    Taking the state of a transform copies the shader uniforms that were explicitly set on it, and a
    later take from a state that never set the uniform removes it again, so unset uniforms keep the
    shader's default instead of being frozen at a value nobody asked for.

    State only copies the names in the module's set of uniforms, which registering a shader normally adds
    to, so the test adds its name to a patched copy of that set.
    """

    uniform_name = "u_test_transform_amount"
    mocker.patch.object(transform, "uniforms", transform.uniforms | {uniform_name})

    source = TransformState()
    copied = TransformState()

    assert uniform_name not in source.__dict__

    setattr(source, uniform_name, 0.5)
    copied.take_state(source)

    assert copied.__dict__[uniform_name] == 0.5

    copied.take_state(TransformState())

    assert uniform_name not in copied.__dict__
