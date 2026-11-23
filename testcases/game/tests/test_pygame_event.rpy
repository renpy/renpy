# Tests for pygame events that need the running game: the main window, and the common gamepad calibration code.

# ==============
# == Fixtures ==
# ==============

init python:

    def pygame_event__convert(event_type, **fields):
        """
        Returns the single event the event queue would produce for an SDL event of `event_type` with these SDL
        fields.
        """

        (ev,) = renpy.pygame.event._make_event(event_type, **fields)
        return ev

    def pygame_event__calibration_binding(mask):
        """
        Returns the binding the gamepad calibration screen records when hat 0 of a joystick moves to the position SDL
        reports as `mask`, or None if it records nothing.
        """

        ev = pygame_event__convert(renpy.pygame.JOYHATMOTION, which=0, hat=0, value=mask)
        watcher = _gamepad.EventWatcher({ "a" : "b0" })

        return watcher.event(ev, 0, 0, 0)


# ==============
# === Tests ====
# ==============

testsuite pygame_event:

    testcase main_window_attribute:
        description "An event from the main window carries the main window as its window attribute."

        assert eval renpy.pygame.event._get_main_window_id() != 0
        assert eval pygame_event__convert(renpy.pygame.WINDOWMOVED, windowID=renpy.pygame.event._get_main_window_id()).window is renpy.pygame.display.get_window()
        assert eval pygame_event__convert(renpy.pygame.KEYDOWN, windowID=renpy.pygame.event._get_main_window_id()).window is renpy.pygame.display.get_window()

    testcase main_window_event_pickles:
        description "An event carrying the main window can be pickled, as when a displayable that stored it is saved, and unpickles with the main window."

        $ import pickle
        $ pygame_event__pickled = pickle.loads(pickle.dumps(pygame_event__convert(renpy.pygame.KEYDOWN, key=renpy.pygame.K_a, windowID=renpy.pygame.event._get_main_window_id())))
        assert eval pygame_event__pickled.window is renpy.pygame.display.get_window()
        assert eval pygame_event__pickled.key == renpy.pygame.K_a

    testcase hat_calibration_binding:
        description "Gamepad calibration records a hat position as the SDL hat mask, from the (x, y) value of the event."
        # SDL hat masks: up 1, right 2, down 4, left 8. The mapping strings written to gamecontrollerdb.txt use them.

        parameter mask = [1, 2, 4, 8, 3, 6, 12, 9]
        assert eval pygame_event__calibration_binding(mask) == "h0.{}".format(mask)

    testcase hat_calibration_ignores_center:
        description "Gamepad calibration ignores a hat returning to the center."

        assert eval pygame_event__calibration_binding(0) is None
