# The mask shaders can be checked without distributing a Cubism sample model.
# A white cropped mask deliberately touches every texture edge: clamping its
# coordinates outside the crop would incorrectly mask the entire canvas.

init python:
    def test_live2d_masks__render(inverted, origin):
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
        mask = renpy.display.draw.solid_texture(64, 32, Color("#fff"))
        result.blit(mask, (0, 0))
        return result

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
