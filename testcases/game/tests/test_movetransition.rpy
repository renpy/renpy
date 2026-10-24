init python:
    define.move_transitions(
        "movetransition__slow_move", 1.0, in_time_warp=_warper.easein)

define movetransition__custom_right = MoveTransition(
    1.0, enter=Transform(xpos=1.0, xanchor=0.0), enter_time_warp=_warper.easein)

define movetransition__custom_left = MoveTransition(
    1.0, enter=Transform(xpos=0.0, xanchor=1.0), enter_time_warp=_warper.easein)

image movetransition__box:
    Solid("#fff", xysize=(100, 80))
    pos (0.46, 0.32)
    anchor (0.5, 0.25)

image movetransition__negative:
    Solid("#fff", xysize=(100, 80))
    pos (0.46, -0.16)
    anchor (0.5, 0.25)


init python:
    def movetransition__sample(transition, image, width, height, st):
        """
        Starts `transition` (a store name) entering `image` on an empty layer, renders the moving
        image at `st` inside a `width` x `height` frame, and returns the surface and the image's
        placed position.
        """

        from renpy.display.displayable import place
        from renpy.display.scenelists import SceneListEntry

        old = Fixed()
        old.layer_name = "master"
        old.append_scene_list([])
        new = Fixed()
        new.layer_name = "master"
        new.append_scene_list([
            SceneListEntry("box", 0, None, None, ImageReference(image), (image,))
        ])
        result = getattr(store, transition)(old_widget=old, new_widget=new)

        # Render the merged entry directly so sampled transition time
        # does not depend on the layer's wall-clock timebase.
        move = result.scene_list[0].displayable
        frame = Fixed(Solid("#000"), move, xysize=(width, height))
        surface = renpy.render_to_surface(frame, width, height, st=st, resize=True)
        x, y = place(width, height, 100, 80, move.get_placement())
        return surface, x, y

    def movetransition__expected(side, width, height, ypos, fraction):
        """
        Returns the expected position of the 100x80 test image when `fraction` of the way
        through an entrance from `side`.
        """

        start_x = -100 if side == "left" else width
        end_x = width * 0.46 - 50
        return start_x + fraction * (end_x - start_x), height * ypos - 20

    def movetransition__lit_rows(surface, x):
        return [ row for row in range(surface.get_height()) if surface.get_at((int(x), row))[0] > 128 ]

    def movetransition__lit_columns(surface, y):
        return [ column for column in range(surface.get_width()) if surface.get_at((column, int(y)))[0] > 128 ]


testsuite movetransition:
    testcase horizontal_entrance_positions:
        description "GH-7370: Directional entrances preserve explicitly positioned images' height."

        parameter (width, height) = [ (800, 600), (1280, 720) ]
        parameter (transition, side, delay, midpoint) = [
            ("moveinleft", "left", 0.5, 0.5),
            ("moveinright", "right", 0.5, 0.5),
            ("movetransition__slow_moveinleft", "left", 1.0, 2 ** -0.5),
            ("movetransition__slow_moveinright", "right", 1.0, 2 ** -0.5),
            ("movetransition__custom_left", "left", 1.0, 2 ** -0.5),
            ("movetransition__custom_right", "right", 1.0, 2 ** -0.5),
            ]
        parameter (image, ypos) = [ ("movetransition__box", 0.32), ("movetransition__negative", -0.16) ]
        parameter progress = [ 0.0, 0.5, 1.0 ]

        $ surface, x, y = movetransition__sample(transition, image, width, height, progress * delay)
        $ fraction = midpoint if progress == 0.5 else progress
        $ expected_x, expected_y = movetransition__expected(side, width, height, ypos, fraction)
        assert eval abs(x - expected_x) < 0.01
        assert eval abs(y - expected_y) < 0.01

    testcase horizontal_entrance_pixels:
        description "GH-7370: Directional entrances draw the whole image where it is placed."

        parameter (width, height) = [ (800, 600), (1280, 720) ]
        parameter (transition, delay) = [
            ("moveinleft", 0.5),
            ("moveinright", 0.5),
            ("movetransition__slow_moveinleft", 1.0),
            ("movetransition__slow_moveinright", 1.0),
            ("movetransition__custom_left", 1.0),
            ("movetransition__custom_right", 1.0),
            ]
        parameter progress = [ 0.5, 1.0 ]

        $ surface, x, y = movetransition__sample(transition, "movetransition__box", width, height, progress * delay)
        assert eval all(channel > 128 for channel in surface.get_at((int(x + 50), int(y + 40)))[:3])

        $ rows = movetransition__lit_rows(surface, x + 50)
        assert eval abs(rows[0] - y) <= 1
        assert eval len(rows) == 80

        $ columns = movetransition__lit_columns(surface, y + 40)
        assert eval abs(columns[0] - x) <= 1
        assert eval len(columns) == 100
