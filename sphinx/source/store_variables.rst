Store Variables
===============

Ren'Py has a number of store variables that control its function. Store
variables may be changed at any time. If a store variable is changed after
the game has started, it will be be saved and loaded by the save system,
and rolled-back when rollback occurs.

.. var:: adv = Character(...)

    This is a template ADV-mode character, and the default character kind
    that is used when :func:`Character` is called.

.. var:: _confirm_quit = True

    This determines if quitting the game asks for confirmation. It is
    set to False during the splashscreen, and is ignored when in the main
    menu.

.. var:: _dismiss_pause = True

    If True, the player can dismiss pauses and transitions.

.. var:: _game_menu_screen = "save"

    This is the screen that is displayed when entering the game menu with no
    more specific screen selected. (For example, when right-clicking, pressing
    escape, or when :func:`ShowMenu` is not given an argument.) If None, entry
    to the game menu is disallowed.

    This is set to None at the start of the splashscreen, and restored to its
    original value when the splashscreen ends.

.. var:: _history = True

    If true, Ren'Py will record dialogue history when a line is shown. (Note
    that :var:`config.history_list_length` must be set as well.)

.. var:: _history_list = [ ]

    This is a list of history objects, corresponding to each line of history
    from oldest to newest. See the :ref:`History <history>` section for more
    information.

.. var:: main_menu = False

    Ren'Py sets this variable to True while in the main menu. This can be used
    to have screens display differently while in the main menu.

.. var:: _menu = False

    Ren'Py sets this variable to True when entering a main menu or game menu
    context.

.. var:: menu = renpy.display_menu

    The function that's called to display the in-gamemenu. It should take the same
    arguments as :func`renpy.display_menu`. Assigning :func:`nvl_menu` to this
    will display an nvl-mode menu.

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

    except that the temp_char variable is not used.

.. var:: narrator = Character(...)

    This is the character that speaks narration (say statements that do not
    give a character or character name). This::

        "Hello, world."

    is equivalent to::

        narrator "Hello, world."

.. var:: _rollback = True

    Controls if rollback is allowed.

.. var:: say = ...

    A function that is called by Ren'Py to display dialogue. This is called
    with three arguments. The first argument (`who`) is the character saying the
    dialogue (or None for the narrator). The second argument(`what`) is what dialogue
    is being said.

    The third argument must be a keyword argument named `interact` and defaulting
    to True. If true, the say function will wait for a click. If false, it will
    immediately return with the dialogue displayed on the screen.

    It's rare to call this function directly, as one can simply call a character
    with dialogue. This variable mostly exists to be redefined, as a way of
    hooking the say statement.

.. var:: save_name = ""

    A save name that is included with saves.

.. var:: _skipping = True

    Controls of if skipping is allowed.

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

