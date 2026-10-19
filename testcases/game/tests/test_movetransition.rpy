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
    def movetransition__check_entrances():
        """Exercise actual ATL and transition factories at deterministic times."""
        from renpy.display.displayable import place
        from renpy.display.scenelists import SceneListEntry

        transitions = (
            (moveinleft, "left", 0.5, 0.5),
            (moveinright, "right", 0.5, 0.5),
            (movetransition__slow_moveinleft, "left", 1.0, 2 ** -0.5),
            (movetransition__slow_moveinright, "right", 1.0, 2 ** -0.5),
            (movetransition__custom_left, "left", 1.0, 2 ** -0.5),
            (movetransition__custom_right, "right", 1.0, 2 ** -0.5),
        )

        for width, height in ((800, 600), (1280, 720)):
            for transition, side, delay, midpoint in transitions:
                for image, ypos in (
                    ("movetransition__box", 0.32),
                    ("movetransition__negative", -0.16),
                ):
                    old = Fixed()
                    old.layer_name = "master"
                    old.append_scene_list([])
                    new = Fixed()
                    new.layer_name = "master"
                    new.append_scene_list([
                        SceneListEntry("box", 0, None, None, ImageReference(image), (image,))
                    ])
                    result = transition(old_widget=old, new_widget=new)
                    # Render the merged entry directly so sampled transition time
                    # does not depend on the layer's wall-clock timebase.
                    move = result.scene_list[0].displayable
                    frame = Fixed(Solid("#000"), move, xysize=(width, height))
                    start_x = -100 if side == "left" else width
                    end_x = width * 0.46 - 50
                    expected_y = height * ypos - 20

                    for st, fraction in ((0.0, 0.0), (delay / 2, midpoint), (delay, 1.0)):
                        surface = renpy.render_to_surface(frame, width, height, st=st, resize=True)
                        x, y = place(width, height, 100, 80, move.get_placement())
                        expected_x = start_x + fraction * (end_x - start_x)
                        assert abs(x - expected_x) < 0.01, (image, side, st, x, expected_x)
                        assert abs(y - expected_y) < 0.01, (image, side, st, y, expected_y)

                        if ypos > 0 and st > 0:
                            cx, cy = int(x + 50), int(y + 40)
                            assert all(channel > 128 for channel in surface.get_at((cx, cy))[:3]), (
                                image, side, st, (x, y), surface.get_size(), surface.get_at((cx, cy))
                            )
                            rows = [
                                row for row in range(height)
                                if surface.get_at((cx, row))[0] > 128
                            ]
                            assert abs(rows[0] - expected_y) <= 1, (side, st, rows[0], expected_y)
                            assert len(rows) == 80, (side, st, len(rows))
                            columns = [
                                column for column in range(width)
                                if surface.get_at((column, cy))[0] > 128
                            ]
                            assert abs(columns[0] - expected_x) <= 1, (side, st, columns[0], expected_x)
                            assert len(columns) == 100, (side, st, len(columns))


testsuite movetransition:
    testcase horizontal_entrances:
        description "GH-7370: Directional entrances preserve explicitly positioned images' height."

        $ movetransition__check_entrances()
