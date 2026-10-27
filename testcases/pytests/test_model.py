import pytest

from renpy.display.image import DynamicImage
from renpy.display.layout import Null
from renpy.display.model import Model
from renpy.uguu import GL_CLAMP_TO_EDGE, GL_REPEAT


@pytest.mark.parametrize("texture_wrap", [None, (GL_REPEAT, GL_CLAMP_TO_EDGE)], ids=["default-wrap", "custom-wrap"])
def test_dynamic_texture_copy_preserves_options(texture_wrap):
    """
    Model._in_current_store copies a model whose texture is a DynamicImage, and the copy keeps the
    texture's focus, main, fit, and texture_wrap options.

    A DynamicImage locks to the current store's values, so the copy must hold a new, locked displayable
    while leaving the original unlocked, and must not share the texture with the original model.
    Parametrized over the default and an explicit texture_wrap.
    """

    model = Model().texture(DynamicImage("[image]"), focus=True, main=True, fit=True, texture_wrap=texture_wrap)
    original = model.textures[0]
    copied = model._in_current_store()
    texture = copied.textures[0]

    assert copied is not model
    assert texture.displayable is not original.displayable
    assert texture.displayable.locked
    assert not original.displayable.locked
    assert (texture.focus, texture.main, texture.fit) == (True, True, True)
    assert texture.texture_wrap == texture_wrap
    assert original.texture_wrap == texture_wrap


def test_static_texture_keeps_model():
    """A model whose textures don't depend on the store is returned unchanged rather than copied."""

    model = Model().texture(Null(), texture_wrap=(GL_CLAMP_TO_EDGE, GL_REPEAT))
    assert model._in_current_store() is model


def test_mixed_textures_copy_only_dynamic_texture():
    """
    In a model with a static and a dynamic texture, only the dynamic one is replaced.

    The static texture object is shared with the original model. The replacement dynamic texture keeps
    its own texture_wrap and its default (False) focus, main, and fit options.
    """

    model = Model().texture(Null(), texture_wrap=(GL_CLAMP_TO_EDGE, GL_REPEAT))
    model.texture(DynamicImage("[image]"), texture_wrap=(GL_REPEAT, GL_CLAMP_TO_EDGE))

    copied = model._in_current_store()

    assert copied.textures[0] is model.textures[0]
    assert copied.textures[1] is not model.textures[1]
    assert copied.textures[1].texture_wrap == (GL_REPEAT, GL_CLAMP_TO_EDGE)
    assert (copied.textures[1].focus, copied.textures[1].main, copied.textures[1].fit) == (False,) * 3
