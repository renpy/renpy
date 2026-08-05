# This file tests camera transforms, interpolation, and replacement behavior.

# ==============
# == Fixtures ==
# ==============

label camera_transform__replacement_preserves_state__label:
    scene bg room
    show eileen happy
    camera at camera_transform__replacement_preserves_state__zoomin
    "Moving..."
    camera at camera_transform__replacement_preserves_state__zoomout
    "Moving back..."
    return

transform camera_transform__replacement_preserves_state__zoomin:
    linear 1.0 xoffset 100 yoffset 100 zoom 1.5

transform camera_transform__replacement_preserves_state__zoomout:
    linear 0.2 xoffset 0 yoffset 0 zoom 1.0


# ==============
# === Tests ====
# ==============

testsuite camera_transform:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)


    testcase replacement_preserves_state:
        description "Preserves interrupted camera-transform state"
        # GH-6994: When a camera transform is interrupted, the next transform continues from the
        # current state, rather than resetting unspecified properties to defaults.
        # https://github.com/renpy/renpy/issues/6994

        # Let the zoomin animation get partway through
        run Start("camera_transform__replacement_preserves_state__label")
        pause 0.3

        python:
            ct = renpy.game.context().scene_lists.camera_transform.get("master", None)
            old_zoom = ct.state.zoom if (ct is not None) else None
            old_xoffset = ct.state.xoffset if (ct is not None) else None
            assert old_zoom is not None and old_zoom > 1.0, f"Expected zoom > 1.0, got {old_zoom}"
            assert old_xoffset is not None and old_xoffset > 0, f"Expected offset > 0, got {old_xoffset}"

        # Interrupt the transform and replace the transform with zoomout.
        # The zoom should continue interpolation from the interrupted value
        # (not jumping straight to 1.0, and not stuck at old_zoom).
        advance
        pause 0.02

        python:
            ct = renpy.game.context().scene_lists.camera_transform.get("master", None)
            mid_zoom = ct.state.zoom if (ct is not None) else None
            assert mid_zoom is not None and mid_zoom > 1.0 and mid_zoom < old_zoom, \
                f"Expected zoom between {old_zoom} and 1.0, got {mid_zoom}"

        # Let the zoomout animation complete.
        pause 0.2

        python:
            ct = renpy.game.context().scene_lists.camera_transform.get("master", None)
            new_xoffset = ct.state.xoffset if (ct is not None) else None
            new_zoom = ct.state.zoom if (ct is not None) else None
            assert new_xoffset is not None and abs(new_xoffset - 0) < 0.01, f"Expected offset near 0.0, got {new_xoffset}"
            assert new_zoom is not None and abs(new_zoom - 1.0) < 0.01, f"Expected zoom near 1.0, got {new_zoom}"
