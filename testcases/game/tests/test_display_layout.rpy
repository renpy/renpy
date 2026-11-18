## This file tests AlphaMask's placement of its child in the running game.

# ==============
# == Fixtures ==
# ==============

default alphamask_clicks = 0

screen alphamask_moved_button(**arguments):
    add AlphaMask(
        Button(Solid("#f00"), xysize=(100, 100), xoffset=200, action=IncrementVariable("alphamask_clicks")),
        Transform(Solid("#fff"), xysize=(400, 100)),
        **arguments
    ):
        pos (50, 50)

screen alphamask_cropped_button():
    add AlphaMask(
        Button(Solid("#f00"), xysize=(100, 100), xoffset=-50, action=IncrementVariable("alphamask_clicks")),
        Transform(Solid("#fff"), xysize=(100, 100)),
        place_child=True,
    ):
        pos (200, 50)

screen alphamask_perspective_child():
    add AlphaMask(
        Transform(Transform(Solid("#f00"), xysize=(100, 100)), perspective=True),
        Transform(Solid("#fff"), xysize=(100, 100)),
        place_child=True,
    ):
        pos (200, 50)

init python:
    def alphamask_pixel(x, y):
        """
        Returns the color drawn at a position on the virtual screen.
        """

        surf = renpy.display.draw.screenshot(renpy.game.interface.surftree)
        w, h = surf.get_size()

        return tuple(surf.get_at((x * w // config.screen_width, y * h // config.screen_height)))

# ==============
# === Tests ====
# ==============

testsuite alphamask:
    before testcase:
        $ alphamask_clicks = 0

    testcase moved_child_is_clicked_where_it_is_drawn:
        description "With place_child=True, a child is focused and clicked at its position in the AlphaMask."

        run Show("alphamask_moved_button", place_child=True)
        pause 0.1

        click pos (100, 100)
        assert eval (alphamask_clicks == 0)

        click pos (300, 100)
        assert eval (alphamask_clicks == 1)

        run Hide("alphamask_moved_button")

    testcase cropped_part_of_child_is_not_clickable:
        description "The part of a moved child outside the AlphaMask is cropped, so it can't be clicked."

        run Show("alphamask_cropped_button")
        pause 0.1

        click pos (175, 100)
        assert eval (alphamask_clicks == 0)

        click pos (225, 100)
        assert eval (alphamask_clicks == 1)

        run Hide("alphamask_cropped_button")

    testcase perspective_child_is_drawn:
        description "A child that uses perspective is drawn, as cropping must not clip it in screen coordinates."

        run Show("alphamask_perspective_child")
        pause 0.1

        assert eval (alphamask_pixel(250, 100) == (255, 0, 0, 255))

        run Hide("alphamask_perspective_child")

    testcase child_stays_at_the_corner_by_default:
        description "By default, the child's position properties are ignored."

        run Show("alphamask_moved_button")
        pause 0.1

        click pos (300, 100)
        assert eval (alphamask_clicks == 0)

        click pos (100, 100)
        assert eval (alphamask_clicks == 1)

        run Hide("alphamask_moved_button")
