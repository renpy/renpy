## This file tests the shaders in renpy/common/_shaders.rpym in the running game.

# ==============
# == Fixtures ==
# ==============

screen blur_zoom_comparison(blur, zoom):
    add Solid("#000")

    # The same blurred square is shown twice, once drawn at its own size, and once built at 1 / zoom times the
    # size and zoomed to the same size on screen. The padding keeps the blur from reaching the edge of the
    # displayable.
    add Transform(Fixed(Solid("#fff", xysize=(100, 100), align=(.5, .5)), xysize=(200, 200)), blur=blur):
        pos (100, 100)

    add Transform(
        Fixed(Solid("#fff", xysize=(int(100 / zoom), int(100 / zoom)), align=(.5, .5)), xysize=(int(200 / zoom), int(200 / zoom))),
        blur=blur,
        zoom=zoom,
    ):
        pos (400, 100)

screen blur_in_oversampled_mesh(blur):
    add Solid("#000")

    # On the left, the blur is drawn into the texture of a mesh zoomed by 2, which has 2 texels per unit, and is
    # measured in that mesh's units. On the right, twice the blur is drawn directly at the same zoom, and is
    # measured on screen, so both should be the same width.
    add Transform(Transform(Fixed(Solid("#fff", xysize=(100, 100), align=(.5, .5)), xysize=(200, 200)), blur=blur), mesh=True, zoom=2.0):
        pos (0, 100)

    add Transform(Fixed(Solid("#fff", xysize=(100, 100), align=(.5, .5)), xysize=(200, 200)), blur=blur * 2, zoom=2.0):
        pos (400, 100)

init python:
    def blur_edge_width(left, right, y):
        """
        Returns how many virtual pixels it takes for the screen to go from 10% to 90% of its brightest value,
        moving right from `left` towards `right` along row `y`.
        """

        surf = renpy.display.draw.screenshot(renpy.game.interface.surftree)
        w, h = surf.get_size()
        scale = w / config.screen_width

        row = [ surf.get_at((int(x * scale), int(y * scale)))[0] / 255.0 for x in range(left, right) ]
        peak = max(row)

        def crossing(level):
            for i in range(1, len(row)):
                if row[i] >= level:
                    return i - 1 + (level - row[i - 1]) / max(row[i] - row[i - 1], 1e-6)

            raise Exception("The brightness never reached {}.".format(level))

        return crossing(0.9 * peak) - crossing(0.1 * peak)

# ==============
# === Tests ====
# ==============

testsuite blur_shader:

    testcase zoomed_blur_keeps_its_size_on_screen:
        description "A blur is about as many pixels wide on screen when its displayable is zoomed, as in Ren'Py 8.5, rather than shrinking or growing with the zoom."
        parameter blur = [ 4.0, 8.0 ]
        parameter zoom = [ 0.25, 2.0 ]

        run Show("blur_zoom_comparison", blur=blur, zoom=zoom)
        pause 0.1

        $ blur_unzoomed = blur_edge_width(100, 200, 200)
        $ blur_zoomed = blur_edge_width(400, 500, 200)

        assert eval (blur_unzoomed > 2.0)
        assert eval (0.7 < blur_zoomed / blur_unzoomed < 1.4)

        run Hide("blur_zoom_comparison")

    testcase blur_in_texture_uses_its_units:
        description "A blur drawn into a mesh's oversampled texture is measured in the units of that mesh, using the pixels per unit of the texture, rather than in its texels."
        parameter blur = [ 2.0, 4.0 ]

        run Show("blur_in_oversampled_mesh", blur=blur)
        pause 0.1

        $ blur_in_mesh = blur_edge_width(0, 200, 300)
        $ blur_direct = blur_edge_width(400, 600, 300)

        assert eval (blur_direct > 2.0)
        assert eval (0.7 < blur_in_mesh / blur_direct < 1.4)

        run Hide("blur_in_oversampled_mesh")
