=======================
Configuration Variables
=======================

Configuration variables control the behavior of Ren'Py's implementation,
allowing Ren'Py itself to be customized in a myriad of ways. These range from
the common (such as changing the screen size) to the obscure (adding new
kinds of archive files).

Ren'Py's implementation makes the assumption that, once the GUI system has
initialized, configuration variables will not change. Changing configuration
variables outside of init blocks can lead to undefined behavior.
Configuration variables are not part of the save data.

Configuration variables are often changed in init python blocks::

    init python:

        # Use a widescreen resolution.
        config.screen_width = 1024
        config.screen_height = 600


Commonly Used
-------------

.. var:: config.developer = False

    If set to True, developer mode is enabled. Developer mode gives
    access to the shift+D developer menu, shift+R reloading, and
    various other features that are not intended for end users.

    The default game template sets this to True. We suggest setting it
    to False before releasing a game.

.. var:: config.help = "README.html"

    This controls the functionality of the help system invoked by the
    help button on the main and game menus, or by pressing f1 or
    command-?.

    If None, the help system is disabled and does not show up on
    menus.  If a string corresponding to a label found in the script,
    that label is invoked in a new context. This allows you to define
    an in-game help-screen.  Otherwise, this is interpreted as a
    filename relative to the base directory, that is opened in a web
    browser.

.. var:: config.name = ""

    This should be a string giving the name of the game. This is included
    as part of tracebacks and other log files, helping to identify the
    version of the game being used.

.. var:: config.save_directory = "..."

   This is used to generate the directory in which games and
   persistent information are saved. The name generated depends on
   the platform:

   Windows
       %APPDATA%/RenPy/`save_directory`

   Mac OS X
       ~/Library/RenPy/`save_directory`

   Linux/Other
       ~/.renpy/`save_directory`

   Setting this to None creates a "saves" directory underneath the
   game directory. This is not recommended, as it prevents the game
   from being shared between multiple users on a system. It can also
   lead to problems when a game is installed as Administrator, but run
   as a user.

   This must be set in a python early block, so that persistent
   information can be loaded before init code is run.

   The user may change the directory. Code that needs to know the save
   directory should read :var:`config.savedir` instead of this
   variable.

.. var:: config.screen_height = 600

    The height of the screen.

.. var:: config.screen_width = 800

    The width of the screen.

.. var:: config.translations = dict(...)

    This is a map used to translate text in the game menu into your
    language. See Localizing Ren'Py for how to use it, and here for a
    list of available translations.

.. var:: config.window_icon = None

    If not None, this is expected to be the filename of an image
    giving an icon that is used for the window on Linux and Mac OS
    X. This should be a large image, with 8-bit alpha.

    This should generally be a PNG format file.

.. var:: config.windows_icon = None

    If not None, this is expected to be the filename of an image
    giving an icon that is used for the window on Windows. This should
    be a 32x32 image with 1-bit alpha. (Opaque images work the best.)

    This should be a PNG format file.

.. var:: config.window_title = "A Ren'Py Game"

    The static portion of the title of the window containing the
    Ren'Py game. :var:`_window_subtitle` is appended to this to get
    the full title of the window.

.. var:: config.version = ""

    This should be a string giving the version of the game. This is included
    as part of tracebacks and other log files, helping to identify the
    version of the game being used.

Transitions
-----------

These control transitions between various screens.

.. var:: config.adv_nvl_transition = None

    A transition that is used when showing NVL-mode text directly
    after ADV-mode text.

.. var:: config.after_load_transition = None

    A transition that is used after loading, when entering the loaded
    game.

.. var:: config.end_game_transition = None

    The transition that is used to display the main menu after the
    game ends normally, either by invoking return with no place to
    return to, or by calling :func:`renpy.full_restart`.

.. var:: config.end_splash_transition = None

    The transition that is used to display the main menu after the end
    of the splashscreen.

.. var:: config.enter_replay_transition = None

    If not None, a transition that is used when entering a replay.

.. var:: config.enter_transition = None

    If not None, this variable should give a transition that will be
    used when entering the game menu.

.. var:: config.enter_yesno_transition = None

    If not None, a transition that is used when entering the yes/no
    prompt screen.

.. var:: config.exit_replay_transition = None

    If not None, a transition that is used when exiting a replay.

.. var:: config.exit_transition = None

    If not None, this variable should give a transition that will be
    performed when exiting the game menu.

.. var:: config.exit_yesno_transition = None

    If not None, a transition that is used when exiting the yes/no
    prompt screen.

.. var:: config.game_main_transition = None

    The transition that is used to display the main menu after leaving
    the game menu. This is used when the load and preferences screens
    are invoked from the main menu, and it's also used when the user
    picks "Main Menu" from the game menu.

.. var:: config.main_game_transition = None

    The transition used when entering the game menu from the main
    menu, as is done when clicking "Load Game" or "Preferences".

.. var:: config.nvl_adv_transition = None

    A transition that is used when showing ADV-mode text directly
    after NVL-mode text.

.. var:: config.say_attribute_transition = None

    If not None, a transition to use when the image is changed by a
    say statement with image attributes.

.. var:: config.window_hide_transition = None

    The transition used by the window hide statement when no
    transition has been explicitly specified.

.. var:: config.window_show_transition = None

    The transition used by the window show statement when no
    transition has been explicitly specified.


Occasionally Used
-----------------

.. var:: config.auto_load = None

    If not None, the name of a save file to automatically load when
    Ren'Py starts up. This is intended for developer use, rather than
    for end users. Setting this to "1" will automatically load the
    game in save slot 1.

.. var:: config.automatic_images = None

    If not None, this causes Ren'Py to automatically define
    images.

    When not set to None, this should be set to a list of
    separators. (For example, ``[ ' ', '_', '/' ]``.)

    Ren'Py will scan through the list of files on disk and in
    archives. When it finds a file ending with .png or .jpg, it will
    strip the extension, then break the name at separators, to creatge
    an image name. If the name consists of at least two components,
    and no image with that name already is defined, Ren'Py will define
    that image to refer to a filename.

    With the example list of separators, if your game directory
    contains:

    * eileen_happy.png, Ren'Py will define the image "eileen happy".
    * lucy/mad.png, Ren'Py will define the image "lucy mad".
    * mary.png, Ren'Py will do nothing. (As the image does not have two components.)

.. var:: config.automatic_images_strip = []

    A list of strings giving prefixes that are stripped out when
    defining automatic images. This can be used to remove directory
    names, when directories contain images.

.. var:: config.debug = False

    Enables debugging functionality (mostly by turning some missing
    files into errors.) This should always be turned off in a release.

.. var:: config.debug_image_cache = False

    If True, Ren'Py will print the contents of the :ref:`image cache <images>`
    to standard output (wherever that goes) whenever the contents of the
    image cache change.

.. var:: config.debug_sound = False

    Enables debugging of sound functionality. This disables the
    supression of errors when generating sound. However, if a sound
    card is missing or flawed, then such errors are normal, and
    enabling this may prevent Ren'Py from functioning normally. This
    should always be False in a released game.

.. var:: config.debug_text_overflow = False

    When true, Ren'Py will log text overflows to text_overflow.txt. A text
    overflow occurs when a :class:`Text` displayable renders to a size
    larger than that allocated to it. By setting this to True and setting
    the :propref:`xmaximum` and :propref:`ymaximum` style properties of the dialogue
    window to the window size, this can be used to report cases where the
    dialogue is too large for its window.

.. var:: config.default_afm_time = None

    If not None, this sets the default auto-forward-mode timeout. If
    not None, then this is the time in seconds we should delay when
    showing 250 characters. 0 is special-cased to be infinite time,
    disabling auto-forward mode.

    Persistent data must be deleted for this to take effect.

.. var:: config.default_afm_enable = None

    If not None, this should be a boolean that controls if
    auto-forward-mode is enabled by default. When it's False,
    auto-forwarding will not occur. Set this to False with caution, as
    the default Ren'Py UI does not provide a way of changing it's
    setting. (But one can use Preference action in a screen to create
    such a UI.)

    Persistent data must be deleted for this to take effect.

.. var:: config.default_fullscreen = None

    This sets the default value of the fullscreen preference. This
    should be True or False. If None, this is ignored, allowing other
    code to set the default value. (It's usually set to False in
    options.rpy.)

.. var:: config.default_text_cps = None

    If not None, this sets the default number of characters per second
    to show. 0 is special cased to mean an infinite number of
    characters per second. (It's usually set to 0 in options.rpy.)

    Persistent data must be deleted for this to take effect.

.. var:: config.default_transform = ...

    When a displayable is shown using the show or scene statements,
    the transform properties are taken from this transform and used to
    initialize the values of the displayable's transform.

    The default default transform is :var:`center`.

.. var:: config.empty_window = ...

    This is called when _window is True, and no window has been shown
    on the screen. (That is, no call to :func:`renpy.shown_window` has
    occurred.) It's expected to show an empty window on the screen, and
    return without causing an interaction.

    The default implementation of this uses the narrator character to
    display a blank line without interacting.

.. var:: config.enter_sound = None

    If not None, this is a sound file that is played when entering the
    game menu.

.. var:: config.exit_sound = None

    If not None, this is a sound file that is played when exiting the
    game menu.

.. var:: config.fix_rollback_without_choice = False

    This option determines how the built in menus or imagemaps behave
    during fixed rollback. The default value is False, which means that
    menu only the previously selected option remains clickable. If set
    to True, the selected option is marked but no options are clickable.
    The user can progress forward through the rollback buffer by
    clicking.


.. var:: config.font_replacement_map = { }

    This is a map from (font, bold, italics) to (font, bold, italics),
    used to replace a font with one that's specialized as having bold
    and/or italics. For example, if you wanted to have everything
    using an italic version of "Vera.ttf" use "VeraIt.ttf" instead,
    you could write::

        init python:
            config.font_replacement_map["Vera.ttf", False, True] = ("VeraIt.ttf", False, False).

    Please note that these mappings only apply to specific variants of
    a font. In this case, requests for a bold italic version of vera
    will get a bold italic version of vera, rather than a bold version
    of the italic vera.

.. var:: config.framerate = 100

    If not None, this is the upper limit on the number of frames
    Ren'Py will attempt to display per second. This is only respected
    by the software renderer. The GL renderer will synchronize to
    vertical blank instead.

.. var:: config.game_menu = [ ... ]

    This is used to customize the choices on the game menu. Please
    read Main and Game Menus for more details on the contents of this
    variable.

    This is not used when the game menu is defined using screens.

.. var:: config.game_menu_music = None

    If not None, a music file to play when at the game menu.

.. var:: config.gl_test_image = "black"

    The name of the image that is used when running the OpenGL
    performance test. This image will be shown for 5 frames or .25
    seconds, on startup. It will then be automatically hidden.

.. var:: config.has_autosave = True

    If true, the game will autosave. If false, no autosaving will
    occur.

.. var:: config.image_cache_size = 8

    This is used to set the size of the :ref:`image cache <images>`, as a
    multiple of the screen size. This number is multiplied by the size of
    the screen, in pixels, to get the size of the image cache in pixels.

    If set too large, this can waste memory. If set too small, images
    can be repeatedly loaded, hurting performance.

.. var:: config.key_repeat = (.3, .03)

    Controls the rate of keyboard repeat. When key repeat is enabled, this
    should be a tuple. The first item in the tuple is the delay before the
    first repeat, and the second item is the delay between repeats. Both
    are in seconds. If None, keyboard repeat is disabled.

.. var:: config.language = None

    If not None, this should be a string giving the default language
    that the game is translated into by the translation framework.

.. var:: config.main_menu = [ ... ]

    The default main menu, when not using screens. For more details,
    see Main and Game Menus.

.. var:: config.main_menu_music = None

    If not None, a music file to play when at the main menu.

.. var:: config.menu_clear_layers = []

    A list of layer names (as strings) that are cleared when entering
    the game menu.

.. var:: config.menu_window_subtitle = ""

    The :var:`_window_subtitle` variable is set to this value when entering
    the main or game menus.

.. var:: config.missing_background = "black"

    This is the background that is used when :var:`config.developer` is True
    and an undefined image is used in a :ref:`scene statement
    <scene-statement>`. This should be an image name (a string), not a
    displayable.

.. var:: config.mode_callbacks = [ ... ]

    A list of callbacks called when entering a mode. For more documentation,
    see the section on :ref:`Modes`.

    The default value includes a callback that implements :var:`config.adv_nvl_transition`
    and :var:`config.nvl_adv_transition`.

.. var:: config.mouse = None

    This variable controls the use of user-defined mouse cursors. If
    None, the system mouse is used, which is usually a black-and-white
    mouse cursor.

    Otherwise, this should be a dictionary giving the
    mouse animations for various mouse types. Keys used by the default
    library include "default", "say", "with", "menu", "prompt",
    "imagemap", "pause", "mainmenu", and "gamemenu". The "default" key
    should always be present, as it is used when a more specific key
    is absent.

    Each value in the dictionary should be a list of (`image`,
    `xoffset`, `offset`) tuples, representing frames.

    `image`
        The mouse cursor image.

    `xoffset`
        The offset of the hotspot pixel from the left side of the
        cursor.

    `yoffset`
        The offset of the hotspot pixel from the top of the cursor.

    The frames are played back at 20hz, and the animation loops after
    all frames have been shown.

.. var:: config.narrator_menu = False

    (This is set to True by the default screens.rpy file.) If true,
    then narration inside a menu is displayed using the narrator
    character. Otherwise, narration is displayed as captions
    within the menu itself.

.. var:: config.overlay_functions = [ ]

    A list of functions. When called, each function is expected to
    use ui functions to add displayables to the overlay layer.

.. var:: config.python_callbacks = [ ]

    A list of functions. The functions in this list are called, without
    any arguments, whenever a python block is run outside of the init
    phase.

    One possible use of this would be to have a function limit a variable
    to within a range each time it is adjusted.

    The functions may be called during internal Ren'Py code, before the
    start of the game proper, and potentially before the variables the
    function depends on are intialized. The functions are required to deal
    with this, perhaps by using ``hasattr(store, 'varname')`` to check if
    a variable is defined.

.. var:: config.quit_action = ...

    The action that is called when the user clicks the quit button on
    a window. The default action prompts the user to see if he wants
    to quit the game.

.. var:: config.thumbnail_height = 75

    The height of the thumbnails that are taken when the game is
    saved. These thumbnails are shown when the game is loaded. Please
    note that the thumbnail is shown at the size it was taken at,
    rather than the value of this setting when the thumbnail is shown
    to the user.

    When using a load_save layout, a different default may be used.

.. var:: config.thumbnail_width = 100

    The width of the thumbnails that are taken when the game is
    saved. These thumbnails are shown when the game is loaded. Please
    note that the thumbnail is shown at the size it was taken at,
    rather than the value of this setting when the thumbnail is shown
    to the user.

    When using a load_save layout, a different default may be used.

.. var:: config.window_overlay_functions = []

    A list of overlay functions that are only called when the window
    is shown.


Rarely or Internally Used
-------------------------

.. var:: config.afm_bonus = 25

    The number of bonus characters added to every string when
    auto-forward mode is in effect.

.. var:: config.afm_callback = None

    If not None, a python function that is called to determine if it
    is safe to auto-forward. The intent is that this can be used by a
    voice system to disable auto-forwarding when a voice is playing.

.. var:: config.afm_characters = 250

    The number of characters in a string it takes to cause the amount
    of time specified in the auto forward mode preference to be
    delayed before auto-forward mode takes effect.

.. var:: config.all_character_callbacks = [ ]

    A list of callbacks that are called by all characters. This list
    is prepended to the list of character-specific callbacks.

.. var:: config.allow_skipping = True

    If set to False, the user is not able to skip over the text of the
    game.

.. var:: config.archives = [ ]

    A list of archive files that will be searched for images and other
    data. The entries in this should consist of strings giving the
    base names of archive files, without the .rpa extension.

    The archives are searched in the order they are found in this list.
    A file is taken from the first archive it is found in.

    At startup, Ren'Py will automatically populate this variable with
    the names of all archives found in the game directory, sorted in
    reverse ascii order. For example, if Ren'Py finds the files
    data.rpa, patch01.rpa, and patch02.rpa, this variable will be
    populated with ``['patch02', 'patch01', 'data']``.

.. var:: config.auto_choice_delay = None

    If not None, this variable gives a number of seconds that Ren'Py
    will pause at an in-game menu before picking a random choice from
    that menu. We'd expect this variable to always be set to None in
    released games, but setting it to a number will allow for
    automated demonstrations of games without much human interaction.

.. var:: config.autosave_frequency = 200

    Roughly, the number of interactions that will occur before an
    autosave occurs. To disable autosaving, set :var:`config.has_autosave` to
    False, don't change this variable.

.. var:: config.character_callback = None

    The default value of the callback parameter of Character.

.. var:: config.clear_layers = []

    A list of names of layers to clear when entering the main and game
    menus.

.. var:: config.context_clear_layers = [ 'screens' ]

    A list of layers that are cleared when entering a new context.

.. var:: config.fade_music = 0.0

    This is the amount of time in seconds to spend fading the old
    track out before a new music track starts. This should probably be
    fairly short, so the wrong music doesn't play for too long.

.. var:: config.fast_skipping = False

    Set this to True to allow fast skipping outside of developer mode.

.. var:: config.file_open_callback = None

    If not None, this is a function that is called with the file name
    when a file needs to be opened. It should return a file-like
    object, or None to load the file using the usual Ren'Py
    mechanisms. Your file-like object must implement at least the
    read, seek, tell, and close methods.

.. var:: config.focus_crossrange_penalty = 1024

    This is the amount of penalty to apply to moves perpendicular to
    the selected direction of motion, when moving focus with the
    keyboard.

.. var:: config.gl_enable = True

    Set this to False to disable OpenGL acceleration. OpenGL acceleration
    will automatically be disabled if it's determined that the system
    cannot support it, so it usually isn't necessary to set this.

    OpenGL can also be disabled by holding down shift at startup.

.. var:: config.gl_resize = True

    Determines if the user is allowed to resize an OpenGL-drawn window.

.. var:: config.hard_rollback_limit = 100

    This is the number of steps that Ren'Py will let the user
    interactively rollback. Set this to 0 to disable rollback
    entirely, although we don't recommend that, as rollback is useful
    to let the user see text he skipped by mistake.

.. var:: config.hide = renpy.hide

    A function that is called when the :ref:`hide statement <hide-statement>`
    is executed. This should take the same arguments as renpy.hide.

.. var:: config.imagemap_auto_function = ...

    A function that expands the `auto` property of a screen language
    :ref:`imagebutton <sl-imagebutton>` or :ref:`imagemap <sl-imagemap>`
    statement into a displayable. It takes the value of the auto property,
    and the desired image, one of: "insensitive", "idle", "hover",
    "selected_idle", "selected_hover", or "ground". It should return a
    displayable or None.

    The default implementation formats the `auto` property with
    the desired image, and then checks if the computed filename exists.

.. var:: config.imagemap_cache = True

    If true, imagemap hotspots will be cached to PNG files,
    reducing time and memory usage, but increasing the size of
    the game on disk. Set this to false to disable this behavior.

.. var:: config.implicit_with_none = True

    If True, then by default the equivalent of a :ref:`with None <with-none>`
    statement will be performed after interactions caused by dialogue, menus
    input, and imagemaps. This ensures that old screens will not show
    up in transitions.

.. var:: config.interact_callbacks = ...

    A list of functions that are called (without any arguments) when
    an interaction is started or restarted.

.. var:: config.joystick = True

    If True, joystick support is enabled.

.. var:: config.keep_running_transform = True

    If true, showing an image without supplying a transform or ATL
    block will cause the image to continue the previous transform
    an image with that tag was using, if any. If false, the transform
    is stopped.

.. var:: config.keymap = dict(...)

    This variable contains a keymap giving the keys and mouse buttons
    assigned to each possible operation. Please see the section on
    Keymaps for more information.

.. var:: config.label_callback = None

    If not None, this is a function that is called whenever a label is
    reached. It is called with two parameters. The first is the name
    of the label. The second is true if the label was reached through
    jumping, calling, or creating a new context, and false
    otherwise.

.. var:: config.label_overrides = { }

    This variable gives a way of causing jumps and calls of labels in
    Ren'Py code to be redirected to other labels. For example, if you
    add a mapping from "start" to "mystart", all jumps and calls to
    "start" will go to "mystart" instead.

.. var:: config.layer_clipping = { }

    Controls layer clipping. This is a map from layer names to (x, y,
    height, width) tuples, where x and y are the coordinates of the
    upper-left corner of the layer, with height and width giving the
    layer size.

    If a layer is not mentioned in config.layer_clipping, then it is
    assumed to take up the full screen.

.. var:: config.layers = [ 'master', 'transient', 'screens', 'overlay' ]

    This variable gives a list of all of the layers that Ren'Py knows
    about, in the order that they will be displayed to the
    screen. (The lowest layer is the first entry in the list.) Ren'Py
    uses the layers "master", "transient", "screens", and "overlay"
    internally, so they should always be in this list.

.. var:: config.lint_hooks = ...

    This is a list of functions that are called, with no arguments,
    when lint is run. The functions are expected to check the script
    data for errors, and print any they find to standard output (using
    the python print statement is fine in this case).

.. var:: config.load_before_transition = True

    If True, the start of an interaction will be delayed until all
    images used by that interaction have loaded. (Yeah, it's a lousy
    name.)

.. var:: config.log = None

    If not None, this is expected to be a filename. Much of the text
    shown to the user by :ref:`say <say-statement>` or :ref:`menu
    <menu-statement>` statements will be logged to this file.

.. var:: config.missing_image_callback = None

    If not None, this function is called when an attempt to load an
    image fails. It may return None, or it may return an image
    manipulator. If an image manipulator is returned, that image
    manipulator is loaded in the place of the missing image.

.. var:: config.mouse_hide_time = 30

    The mouse is hidden after this number of seconds has elapsed
    without any mouse input. This should be set to longer than the
    expected time it will take to read a single screen, so mouse users
    will not experience the mouse appearing then disappearing between
    clicks.

.. var:: config.new_substitutions = True

    If true, Ren'Py will apply new-style (square-bracket)
    substitutions to all text displayed.

.. var:: config.old_substitutions = False

    If true, Ren'Py will apply old-style (percent) substitutions to
    text displayed by the :ref:`say <say-statement>` and :ref:`menu
    <menu-statement>` statements.

.. var:: config.overlay_during_with = True

    True if we want overlays to be shown during :ref:`with statements
    <with-statement>`, or False if we'd prefer that they be hidden during
    the with statements.

.. var:: config.overlay_layers = [ 'overlay' ]

    This is a list of all of the overlay layers. Overlay layers are
    cleared before the overlay functions are called. "overlay" should
    always be in this list.

.. var:: config.periodic_callback = None

    If not None, this should be a function. The function is called,
    with no arguments, at around 20hz.

.. var:: config.predict_statements = 10

    This is the number of statements, including the current one, to
    consider when doing predictive image loading. A breadth-first
    search from the current statement is performed until this number
    of statements is considered, and any image referenced in those
    statements is potentially predictively loaded. Setting this to 0
    will disable predictive loading of images.

.. var:: config.profile = False

    If set to True, some profiling information will be output to
    stdout.

.. var:: config.rollback_enabled = True

    Should the user be allowed to rollback the game? If set to False,
    the user cannot interactively rollback.

.. var:: config.rollback_length = 128

    When there are more than this many statements in the rollback log,
    Ren'Py will consider trimming the log.

.. var:: config.say_allow_dismiss = None

    If not None, this should be a function. The function is called
    with no arguments when the user attempts to dismiss a :ref:`say
    statement <say-statement>`. If this function returns true, the
    dismissal is allowed, otherwise it is ignored.

.. var:: config.say_menu_text_filter = None

    If not None, then this is a function that is given the text found
    in strings in the :ref:`say <say-statement>` and :ref:`menu
    <menu-statement>` statements. It is expected to return new
    (or the same) strings to replace them.

.. var:: config.say_sustain_callbacks = ...

    A list of functions that are called, without arguments, before the
    second and later interactions caused by a line of dialogue with
    pauses in it. Used to sustain voice through pauses.

.. var:: config.save_dump = False

   If set to true, Ren'Py will create the file save_dump.txt whenever it
   saves a game. This file contains information about the objects contained
   in the save file. Each line consists of a relative size estimate, the path
   to the object, information about if the object is an alias, and a
   representation of the object.

.. var:: config.save_physical_size = True

    If true, the physical size of the window will be saved in the
    preferences, and restored when the game resumes.

.. var:: config.savedir = ...

    The complete path to the directory in which the game is
    saved. This should only be set in a python early block. See also
    config.save_directory, which generates the default value for this
    if it is not set during a python early block.

.. var:: config.scene = renpy.scene

    A function that's used in place of renpy.scene by the :ref:`scene
    statement <scene-statement>`. Note that this is used to clear the screen,
    and config.show is used to show a new image. This should have the same
    signature as renpy.scene.

.. var:: config.screenshot_callback = ...

    A function that is called when a screenshot is taken. The function
    is called with a single parameter, the full filename the screenshot
    was saved as.

.. var:: config.screenshot_crop = None

    If not None, this should be a (`x`, `y`, `height`, `width`)
    tuple. Screenshots are cropped to this rectangle before being
    saved.

.. var:: config.screenshot_pattern = "screenshot%04d.png"

    The pattern used to create screenshot files. This pattern is applied (using
    python's %-formatting rules) to the natural numbers to generate a sequence
    of filenames. The filenames may be absolute, or relative to
    config.renpy_base. The first filename that does not exist is used as the
    name of the screenshot.

.. var:: config.script_version = None

    If not None, this is interpreted as a script version. The library
    will use this script version to enable some compatibility
    features, if necessary. If None, we assume this is a
    latest-version script.

    This is normally set in a file added by the Ren'Py launcher when
    distributions are built.

.. var:: config.searchpath = [ 'common', 'game' ]

    A list of directories that are searched for images, music,
    archives, and other media, but not scripts. This is initialized to
    a list containing "common" and the name of the game directory.

.. var:: config.show = renpy.show

    A function that is used in place of renpy.show by the :ref:`show
    <show-statement>` and :ref:`scene <scene-statement>` statements. This
    should have the same signature as renpy.show.

.. var:: config.skip_delay = 75

    The amount of time that dialogue will be shown for, when skipping
    statements using ctrl, in milliseconds. (Although it's nowhere
    near that precise in practice.)

.. var:: config.skip_indicator = True

    If True, the library will display a skip indicator when skipping
    through the script.

.. var:: config.sound = True

    If True, sound works. If False, the sound/mixer subsystem is
    completely disabled.

.. var:: config.sound_sample_rate = 44100

    The sample rate that the sound card will be run at. If all of your
    wav files are of a lower rate, changing this to that rate may make
    things more efficent.

.. var:: config.start_callbacks = [ ... ]

    A list of callbacks functions that are called with no arguments
    after the init phase, but before the game (including the
    splashscreen) starts. This is intended to be used by frameworks
    to initialize variables that will be saved.

    The default value of this variable includes callbacks that Ren'Py
    uses internally to implement features such as nvl-mode. New
    callbacks can be appended to this list, but the existing callbacks
    should not be removed.

.. var:: config.start_interact_callbacks = ...

    A list of functions that are called (without any arguments) when
    an interaction is started. These callbacks are not called when an
    interaction is restarted.

.. var:: config.top_layers = [ ]

    This is a list of names of layers that are displayed above all
    other layers, and do not participate in a transition that is
    applied to all layers. If a layer name is listed here, it should
    not be listed in config.layers.

.. var:: config.transient_layers = [ 'transient' ]

    This variable gives a list of all of the transient
    layers. Transient layers are layers that are cleared after each
    interaction. "transient" should always be in this list.

.. var:: config.transform_uses_child_position = True

    If True, transforms will inherit :ref:`position properties
    <position-style-properties>` from their child. If not, they won't.

.. var:: config.variants = [ ... ]

    A list of screen variants that are searched when choosing a screen to
    display to the user. This should always end with None, to ensure
    that the default screens are chosen. See :ref:`screen-variants`.

.. var:: config.voice_filename_format = "{filename}"

    A string that is formatted with the string argument to the voice
    statement to produce the filename that is played to the user. For
    example, if this is "{filename}.ogg", the ``voice "test"`` statement
    will play test.ogg.

.. var:: config.with_callback = None

    If not None, this should be a function that is called when a :ref:`with
    statement <with-statement>` occurs. This function can be responsible for
    putting up transient things on the screen during the transition. The
    function is called with a single argument, which is the transition that
    is occurring. It is expected to return a transition, which may or may not
    be the transition supplied as its argument.

