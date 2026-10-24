import unittest

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.image import DynamicImage
from renpy.display.layout import Null
from renpy.display.model import Model
from renpy.uguu import GL_CLAMP_TO_EDGE, GL_REPEAT


class TestModelTextures(unittest.TestCase):
    def test_dynamic_texture_copy_preserves_options(self):
        for texture_wrap in (None, (GL_REPEAT, GL_CLAMP_TO_EDGE)):
            with self.subTest(texture_wrap=texture_wrap):
                model = Model().texture(
                    DynamicImage("[image]"), focus=True, main=True, fit=True, texture_wrap=texture_wrap
                )
                original = model.textures[0]
                copied = model._in_current_store()
                texture = copied.textures[0]

                self.assertIsNot(copied, model)
                self.assertIsNot(texture.displayable, original.displayable)
                self.assertTrue(texture.displayable.locked)
                self.assertFalse(original.displayable.locked)
                self.assertEqual((texture.focus, texture.main, texture.fit), (True, True, True))
                self.assertEqual(texture.texture_wrap, texture_wrap)
                self.assertEqual(original.texture_wrap, texture_wrap)

    def test_static_texture_keeps_model(self):
        model = Model().texture(Null(), texture_wrap=(GL_CLAMP_TO_EDGE, GL_REPEAT))
        self.assertIs(model._in_current_store(), model)

    def test_mixed_textures_copy_only_dynamic_texture(self):
        model = Model().texture(Null(), texture_wrap=(GL_CLAMP_TO_EDGE, GL_REPEAT))
        model.texture(DynamicImage("[image]"), texture_wrap=(GL_REPEAT, GL_CLAMP_TO_EDGE))

        copied = model._in_current_store()

        self.assertIs(copied.textures[0], model.textures[0])
        self.assertIsNot(copied.textures[1], model.textures[1])
        self.assertEqual(copied.textures[1].texture_wrap, (GL_REPEAT, GL_CLAMP_TO_EDGE))
        self.assertEqual((copied.textures[1].focus, copied.textures[1].main, copied.textures[1].fit), (False,) * 3)
