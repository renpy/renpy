Store Variables
===============

Ren'Py has a number of store variables that control its function. Store
variables may be changed at any time. If a store variable is changed after
the game has started, it will be be saved and loaded by the save system,
and rolled-back when rollback occurs.

.. var:: adv = Character(...)

    This is a template ADV-mode character, and the default character kind
    that is used when :func:`Character` is called.

.. var:: _autosave = True

    This variable can be set to False to disable autosave.

.. var:: _confirm_quit = True

    This determines if quitting the game asks for confirmation. It is
    set to False during the splashscreen, and is ignored when in the main
    menu.

.. var:: _constant

    If set to true in a store, indicates the store is constant.
    See :ref:`constant-stores`.

.. var:: default_mouse

    This is undefined by default. If defined, and if :var:`config.mouse` is
    set at game startup, this is a key that is used to look up a mouse cursor
    when the current cursor does not exist, or is the default. This is used by
    :var:`config.mouse` and :func:`MouseDisplayable`.

    See :doc:`mouse` for more information.

.. var:: _dismiss_pause = True

    If True, the player can dismiss pauses and transitions.

.. var:: _game_menu_screen = "save"

    This is the screen that is displayed when entering the game menu with no
    more specific screen selected. (For example, when right-clicking, pressing
    escape, or when :func:`ShowMenu` is not given an argument.) If None, entry
    to the game menu is disallowed.

    This is set to None at the start of the splashscreen, and restored to its
    original value when the splashscreen ends.

.. var:: _greedy_rollback = True

    Determines if the game performs a greedy rollback after a load. A greedy
    rollback will rollback to just after the last statement that interacted,
    rather than to just before the statement that the game was in during
    the load.

.. var:: _history = True

    If true, Ren'Py will record dialogue history when a line is shown. (Note
    that :var:`config.history_length` must be set as well.)

.. var:: _history_list = [ ]

    This is a list of history objects, corresponding to each line of history
    from oldest to newest. See the :doc:`History <history>` section for more
    information.

.. var:: _ignore_action = None

    When this is not None, it's an action that is run after clicking Ignore
    on the error handling screen. The action is usually :func:`Jump`, to jump
    the game to a place that can recover from an error. If None, control
    continues with the next Ren'Py statement.

.. var:: main_menu = False

    Ren'Py sets this variable to True while in the main menu. This can be used
    to have screens display differently while in the main menu.

.. var:: _menu = False

    Ren'Py sets this variable to True when entering a main menu or game menu
    context.

.. var:: menu = renpy.display_menu

    The function that's called to display the in-game menu. It should take the same
    arguments as :func:`renpy.display_menu`, and pass unknown keyword arguments
    unchanged. Assigning :func:`nvl_menu` to this will display an nvl-mode menu.

.. var:: mouse_visible = True

    Controls if the mouse is visible. This is automatically set to true when
    entering the standard game menus.

.. var:: name_only = Character(...)

    This is a template character that is used when a string is given as the
    character name in a say statement. This::

        "Eileen" "Hello, world."

    is equivalent to::

        $ temp_char = Character("Eileen", kind=name_only)
        temp_char "Hello, world."

    except that the ``temp_char`` variable is not used.

.. var:: narrator = Character(...)

    This is the character that speaks narration (say statements that do not
    give a character or character name). This::

        "Hello, world."

    is equivalent to::

        narrator "Hello, world."

.. var:: _quit_slot = None

    If not None, this should be a string giving the name of a file slot.
    When Ren'Py quits, the game will be saved in this slot.

.. var:: _rollback = True

    Controls if rollback is allowed.

.. var:: say : Callable

    A function that is called by Ren'Py to display dialogue, when a string is
    used in place of the speaking character::

        define e = Character("Eileen", who_color="#0f0")

        label start:
            "Eileen" "My name is Eileen." # will call the say function
            e "I like trains !" # will not call the say function

    This function should have the same signature as :func:`renpy.say`.
    It should not call :func:`renpy.say` but rather use the other
    :doc:`say statement equivalents <statement_equivalents>`.

    It's rare to call this function directly, as one can simply call a character
    with dialogue. This variable mostly exists to be redefined, as a way of
    hooking the say statement.

.. var:: save_name = ""

    A save name that is included with saves. This is also used by the steam timeline if
    :var:`config.automatic_steam_timeline` is true, and is best considered to be a chapter
    name.

.. var:: _scene_show_hide_transition = None

    If not None, this is a transition that will be performed using the
    with statement after a series of scene, show, and hide statements
    that are not followed by a with statement, or by a window transition.

    .. seealso:: :ref:`scene-show-hide-transition`

.. var:: _screenshot_pattern = None

    If not None, this string is used in preference to :var:`config.screenshot_pattern`
    to determine the filename of a screenshot. Please see the documentation for
    that variable for the format of the string.

.. var:: _skipping = True

    Controls if skipping is allowed.

.. var:: _version = ...

    This is set to :var:`config.version` when a new game is started. It can be
    used by the ``after_load`` label or :var:`config.after_load_callbacks` to
    determine which upgrades need to be done.

    This is only set once, upon the initial start. After that, the game is
    responsible for updating _version as necessary.

.. var:: _window = False

    This set by the ``window show`` and ``window hide`` statements, and indirectly
    by ``window auto``. If true, the dialogue window is shown during non-dialogue
    statements.

.. var:: _window_auto = False

    This is set to true by ``window auto`` and to false by ``window show`` and
    ``window hide``. If true, the window auto behavior occurs.

.. var:: _window_subtitle = ''

    This is appended to :var:`config.window_title` to produce the caption for the game
    window. This is automatically set to :var:`config.menu_window_subtitle` while in
    the game menu.
