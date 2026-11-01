import pytest

import renpy
from renpy.display import im
from renpy.display.displayable import Displayable
from renpy.display.image import DynamicImage
from renpy.display.layout import Null
from renpy.display.model import Model
from renpy.gl2.gl2uniform import SamplerSetter
from renpy.uguu import GL_CLAMP_TO_EDGE, GL_REPEAT, GL_TEXTURE_2D


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


@pytest.mark.parametrize("premultiply", [True, False])
def test_texture_wraps_image_with_premultiply(premultiply: bool) -> None:
    """
    Model.texture wraps an image in a RawTexture that carries the premultiply setting and the mipmap=True
    that model textures get by default, and records the setting on the texture.
    """

    texture = Model().texture("normal.png", premultiply=premultiply).textures[0]

    assert isinstance(texture.displayable, im.UnoptimizedTexture)
    assert texture.displayable.image.filename == "normal.png"
    assert texture.displayable.premultiply == premultiply
    assert texture.displayable.mipmap is True
    assert texture.premultiply == premultiply


def test_texture_reuses_raw_texture_with_matching_premultiply():
    """
    A RawTexture whose premultiply setting matches the one passed to Model.texture is used as-is, so its
    own options (here mipmap=False) are kept rather than replaced by the model defaults.
    """

    raw = renpy.store.RawTexture(im.Null(), mipmap=False)
    texture = Model().texture(raw).textures[0]

    assert texture.displayable is raw


def test_texture_rewraps_raw_texture_with_different_premultiply():
    """
    A RawTexture whose premultiply setting differs from the one passed to Model.texture is wrapped again,
    so the setting passed to Model.texture is the one used when the texture is loaded.
    """

    raw = renpy.store.RawTexture(im.Null(), premultiply=False)
    texture = Model().texture(raw).textures[0]

    assert texture.displayable is not raw
    assert isinstance(texture.displayable, im.UnoptimizedTexture)
    assert texture.displayable.premultiply is True


@pytest.mark.parametrize(
    "displayable",
    [
        "[normal].png",
        "normal",
        "#fff",
        ["normal.png", "fallback.png"],
        DynamicImage("[normal].png"),
        im.Image("normal.png"),
        im.UnoptimizedTexture(im.Image("normal.png"), premultiply=False),
        Null(),
    ],
    ids=["dynamic-filename", "image-name", "color", "filename-list", "dynamic-image", "image", "raw-texture", "null"],
)
def test_texture_rejects_non_filename_without_premultiplication(displayable: str | list[str] | Displayable) -> None:
    """Only literal filename strings support premultiply=False, and rejected calls leave the model unchanged."""

    model = Model()

    with pytest.raises(ValueError, match="premultiply=False requires a literal image filename"):
        model.texture(displayable, premultiply=False)

    assert model.textures == []


def test_mixed_texture_copy_preserves_premultiply() -> None:
    """Copying a model for a dynamic texture preserves a separate file texture's premultiply=False setting."""

    model = Model().texture("normal.png", premultiply=False).texture(DynamicImage("[image]"))
    copied = model._in_current_store()

    assert copied is not model
    assert copied.textures[0] is model.textures[0]
    assert copied.textures[0].premultiply is False


def test_texture_from_old_save_copies_with_default_premultiply():
    """
    A texture saved before premultiply existed has no premultiply attribute in its state. Copying it in
    _in_current_store must fall back to premultiply=True instead of raising AttributeError. The missing
    attribute is simulated by removing it from the instance dict, as unpickling old state would leave it.
    """

    model = Model().texture(DynamicImage("[image]"))
    del model.textures[0].__dict__["premultiply"]

    copied = model._in_current_store()

    assert copied.textures[0].premultiply is True


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
