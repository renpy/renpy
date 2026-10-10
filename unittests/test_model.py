import unittest

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.image import DynamicImage
from renpy.display.layout import Null
from renpy.display.model import Model


class TestModelTextures(unittest.TestCase):
    def test_dynamic_texture_copy_preserves_options(self):
        for texture_wrap in (None, (True, False)):
            with self.subTest(texture_wrap=texture_wrap):
                model = Model().texture(
                    DynamicImage("[image]"), focus=True, main=True, fit=True, texture_wrap=texture_wrap
                )
                copied = model._in_current_store()
                original = model.textures[0]
                texture = copied.textures[0]

                self.assertIsNot(copied, model)
                self.assertIsNot(texture.displayable, original.displayable)
                self.assertTrue(texture.displayable.locked)
                self.assertEqual((texture.focus, texture.main, texture.fit), (True, True, True))
                self.assertEqual(texture.texture_wrap, texture_wrap)
                self.assertEqual(original.texture_wrap, texture_wrap)

    def test_static_texture_keeps_model(self):
        model = Model().texture(Null(), texture_wrap=(False, True))
        self.assertIs(model._in_current_store(), model)
