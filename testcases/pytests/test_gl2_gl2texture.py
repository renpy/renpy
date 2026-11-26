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

import pytest

import renpy
from renpy.gl2.gl2draw import GL2Draw
from renpy.gl2.gl2texture import Texture, TextureLoader


@pytest.fixture
def loader():
    """Returns a TextureLoader that hasn't touched OpenGL, as freeing a texture only queues its number."""

    return TextureLoader(GL2Draw.__new__(GL2Draw))


def make_loaded_texture(loader, number):
    """
    Returns a 10x10 texture that is loaded as texture `number` in the loader's current generation, as loading it
    for real would create the texture in OpenGL.
    """

    rv = Texture((10, 10), loader)
    rv.number = number
    rv.generation = loader.generation
    rv.loaded = True
    rv.properties = {"mipmap": False}
    loader.allocated.add(number)

    return rv


def test_freed_texture_is_queued_for_deletion(loader):
    """
    A texture from the current context that is freed is queued to be deleted, and stops counting toward the size.
    The helper doesn't add the texture's size, so the total goes negative by it.
    """

    texture = make_loaded_texture(loader, 7)
    del texture

    assert loader.free_list == [7]
    assert loader.total_texture_size == -10 * 10 * 4


def test_texture_from_old_context_is_never_deleted(loader):
    """
    A texture that outlives a context reset isn't queued when it's freed, since its number may name a texture in the
    new context. Deleting it would make an unrelated image vanish.
    """

    old = make_loaded_texture(loader, 7)

    loader.new_context()
    new = make_loaded_texture(loader, 7)

    del old

    assert loader.free_list == []
    assert loader.allocated == {7}
    assert loader.total_texture_size == 0

    del new

    assert loader.free_list == [7]


def test_cleanup_without_context_keeps_queue(loader):
    """
    With no OpenGL context current, as when a reset starts after the context was lost, cleanup can't delete textures,
    so it keeps them queued for when the context is current again. Dropping them would leak them if the same context
    then came back. The engine under pytest has no context, which is the case being tested.
    """

    texture = make_loaded_texture(loader, 7)
    del texture

    loader.cleanup()

    assert loader.free_list == [7]
    assert loader.allocated == {7}

    loader.new_context()

    assert loader.free_list == []


@pytest.mark.parametrize("reset", ["new_context", "kill_textures"])
def test_reset_dequeues_textures(loader, reset):
    """
    A replaced context, or emptying the texture caches, stops textures queued to load ahead of time from being
    loaded. A texture still waiting is loaded when it's drawn instead. ready_one_texture would load a queued texture,
    which needs OpenGL, so returning False shows nothing was left to load.
    """

    texture = Texture((10, 10), loader)
    texture.from_surface(renpy.display.pgrender.surface((10, 10), True), {"mipmap": False})

    if reset == "new_context":
        loader.new_context()
    else:
        draw = GL2Draw.__new__(GL2Draw)
        draw.texture_loader = loader
        draw.kill_textures()

    assert loader.ready_one_texture() is False
    assert not texture.loaded
