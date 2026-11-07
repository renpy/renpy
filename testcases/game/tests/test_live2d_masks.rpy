# The mask shaders can be checked without distributing a Cubism sample model.
# A white cropped mask deliberately touches every texture edge: clamping its
# coordinates outside the crop would incorrectly mask the entire canvas.

init python:
    def test_live2d_masks__render(inverted, origin, mask=None):
        """
        Rasterizes a rectangular mask with Live2D's model coordinates and a
        cropped texture. An off-center origin checks both axes independently.
        """

        from renpy.gl2.gl2mesh2 import Mesh2
        from renpy.display.matrix import Matrix

        x, y = origin
        result = renpy.Render(128, 128)
        result.reverse = Matrix.offset(x, y, 0.0) * Matrix.scale(1.0, -1.0, 1.0)
        result.forward = result.reverse.inverse()
        result.mesh = Mesh2.texture_rectangle(-x, y - 128, 128 - x, y, 0.0, 0.0, 1.0, 1.0)
        result.add_shader("live2d.inverted_mask" if inverted else "live2d.mask")
        result.add_uniform("u_live2d_ppu", 1.0)
        result.add_uniform("u_live2d_offset", origin)
        result.add_uniform("u_live2d_mask_bounds", (0.25, 0.125, 0.5, 0.25))
        result.blit(renpy.display.draw.solid_texture(128, 128, Color("#fff")), (0, 0))
        if mask is None:
            mask = renpy.display.draw.solid_texture(64, 32, Color("#fff"))
        result.blit(mask, (0, 0))
        return result

    def test_live2d_masks__cached_mask():
        """Constructs the same kind of cached mask as the native model renderer."""

        mask = renpy.gl2.live2dmodel.Live2DMask(64, 32)
        mask.add_property("live2d_mask", True)
        mask.blit(renpy.display.draw.solid_texture(64, 32, Color("#fff")), (0, 0))
        return mask

    def test_live2d_masks__scaled(mask, scale):
        """Draws a shared mask through a new parent transform, without changing its geometry."""

        from renpy.display.matrix import Matrix

        result = renpy.Render(128 * scale, 128 * scale)
        result.reverse = Matrix.scale(scale, scale, 1.0)
        result.forward = result.reverse.inverse()
        # Keep translation out of the renderer's oversample estimate, so
        # this fixture measures only the change in parent zoom.
        result.blit(test_live2d_masks__render(False, (0.0, 0.0), mask), (0, 0))
        renpy.render_to_surface(result)
        return mask.cached_texture

    def test_live2d_masks__zoom_textures(scale):
        """
        Samples the textures used by successive parent transforms in one frame.
        Unsaved Renders held only by test locals are swept between test steps.
        """

        mask = test_live2d_masks__cached_mask()
        original = test_live2d_masks__scaled(mask, 1.0)
        enlarged = test_live2d_masks__scaled(mask, scale)
        repeated = test_live2d_masks__scaled(mask, scale)
        smaller = test_live2d_masks__scaled(mask, 1.0)
        return original, enlarged, repeated, smaller

testsuite live2d_masks:
    enabled renpy.has_live2d()

    testcase cropped:
        description "Cropped normal and inverted masks remain transparent outside their geometry"
        parameter inverted = [ False, True ]
        parameter shifted = [ False, True ]
        $ origin = (48.0, 80.0) if shifted else (64.0, 64.0)
        $ surface = renpy.render_to_surface(test_live2d_masks__render(inverted, origin), resize=True)
        assert eval (surface.get_at((64, 32))[3] < 5) == inverted
        assert eval (surface.get_at((16, 32))[3] > 250) == inverted
        assert eval (surface.get_at((64, 80))[3] > 250) == inverted

    testcase parent_zoom:
        description "A shared mask gains resolution when only its parent zoom changes"
        enabled config.mesh_oversample >= 3.0
        parameter scale = [ 2.0, 3.0 ]
        $ original, enlarged, repeated, smaller = test_live2d_masks__zoom_textures(scale)
        assert eval enlarged is not original
        # Allow rounding to physical pixels at fractional display scales.
        assert eval abs(enlarged.texture_width - original.texture_width * scale) < scale
        assert eval abs(enlarged.texture_height - original.texture_height * scale) < scale
        # A repeated zoom and a smaller instance can share the larger texture.
        assert eval repeated is enlarged
        assert eval smaller is enlarged

    testcase context_generation:
        description "Reinitializing a texture loader invalidates its mask rasterization token"
        # This loader owns no textures, so reinitializing it leaves the
        # active renderer's textures intact while exercising a real context.
        $ loader = renpy.gl2.gl2texture.TextureLoader(renpy.display.draw)
        run Function(loader.init)
        $ before = loader.mask_cache_token()
        run Function(loader.init)
        assert eval before != loader.mask_cache_token()
