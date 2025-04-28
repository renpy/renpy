.. _screens:

===========================
Screens and Screen Language
===========================

The things that a user sees when looking at a Ren'Py game can be
divided into images and user interface. Images are displayed to
the user using the scene, show, and hide statements, and are generally
part of the story being told. Everything else the user sees is part of
the user interface, which is customized using screens.

Screens can be displayed in four ways:

* Implicitly, when script statements execute. For example,
  the say statement will cause the `say` screen to be displayed.
* Automatically. For example, Ren'Py will display the `main_menu`
  screen when it starts running, or when the user returns to the
  main menu.
* As an action, associated with a button, mouse button, or keyboard
  key. By default, the `save` screen is shown when the user
  right-clicks or presses escape. It's also possible to define an
  on-screen button that shows the `save` screen.
* Explicitly, using statements that cause screens to be shown.

More than one screen can be shown at a time.

Screens have two main functions. The first is to display information
to the user. Information can be displayed using text, bars, and
images. Some of the information displayed in this manner is vital to
gameplay. The `say` screen, for example, is used to display dialogue
to the user, including the character's name and what she is saying.

The other thing a screen can do is to allow the user to interact with
the game. Buttons and bars allow the user to invoke actions and adjust
values. Ren'Py includes a pool of pre-defined actions, allowing the
user to advance the game, control preferences, load and save games,
and invoke many other actions. A game-maker can also write new actions
in Python.

Screens are updated at the start of each interaction, and each time an
interaction is restarted. Note that a ``with None`` statement does not
cause an interaction to happen, and hence won't update a screen. A
``with Pause(0)`` will be enough to trigger one, if necessary.

A screen has a scope associated with it, giving values to some variables. There are different kinds
of variables, in screens, which are resolved as shown in the following list:

- First are local variables. These only exist in a screen that is being included in another with
  the :ref:`use <sl-use>` statement instead of being shown (or called) on its own. They are very
  similar with screen variables (see below), and created the same way, except that local variables
  can only be accessed by the used screen. Those are set using :class:`SetLocalVariable`, among
  other actions, or by a python block or line in the used screen. Actions such as
  :class:`SetScreenVariable` will *not work* on local variables.

  - Local parameters are the parameters taken by the used screen. They live in the same scope as
    local variables, and follow the same behavior and constraints as screen parameters - see
    below.

- If a name cannot be resolved among local variables - or if we are not in a screen being
  :ref:`used <sl-use>` by another - the name is searched for in screen variables. These are
  variables created with the in-screen :ref:`sl-default` or :ref:`sl-python` statements, in the
  top-level screen. Screen variables can be set through the :class:`SetScreenVariable` action,
  among others, or by a python block or line in the top-level screen, or any used screen if no
  local variable has the same name.

  - Screen parameters (that is, values defined and passed through the parentheses of the screen
    statement) live in the same scope as screen variables (that is, they can't have the same
    name), but they can't be set or edited through actions, since they will be reset to their
    original value at arbitrary times, including every time an action is executed. So, if their
    value were edited through the :class:`SetScreenVariable` action (or any other action really),
    it would be reset immediately afterwards. This is also the case for variables defined in
    in-screen python blocks, since these blocks are executed at arbitrary times, as opposed to
    the in-screen :ref:`default <sl-default>` statement which executes only at the time the
    screen gets shown.

- In last resort, a variable name is looked for in the general store, where all of Ren'Py's global
  variables are. Such variables can be set through the :class:`SetVariable` action, among others.

.. note::

    If you want an action to set a variable inside a screen, and you want that screen to be
    sometimes shown directly and sometimes used inside another, use :class:`SetLocalVariable`. It
    will be far less efficient, but it will work in both cases.

**Screens must not cause side effects that are visible from
outside the screen.** Ren'Py will run a screen multiple times, as
it deems necessary. It runs a screen as part of the image
prediction process, before the screen is first shown. As a result, if
running a screen has side effects, those side effects may occur at
unpredictable times.

**Using Python generators in screens may cause unpredictable results.**
This traces back to an issue with the way the Python interpreter compiles
Python source code that will be used in a screen context. Generators
can be used in Python functions called from a screen, but not in the
screen itself.



Screen Language
===============

The screen language is a mostly-declarative way of displaying
screens. It consists of a statement that declares a new screen,
statements that add displayables to that screen, and control
statements.

Here's an example of a screen::

    screen say(who, what):
        window id "window":
            vbox:
                spacing 10

                text who id "who"
                text what id "what"

The first line of this is a screen statement, a Ren'Py language
statement that's used to declare a screen. The name of the screen is
`say`, so this is the screen that's used to display dialogue. It takes
two parameters, `who` and `what`.

The screen contains a window, which has been given the id of
"window". This window contains a vertical box, and the spacing inside
that box is 10 pixels. It contains two text fields, one displaying the name of
the speaker, and the displaying what is being spoken.

Screen Language Syntax
----------------------

Most screen language statements share a common syntax. (Some of the
control statements have other syntaxes.)  A statement starts at the
beginning of a line, with a keyword that introduces the statement.

If a statement takes parameters, they immediately follow the
keyword. The parameters are space-separated simple expressions, unless
otherwise noted.

The positional parameters are followed by a property list. A property
consists of the property name, followed by the value of that
property. Property values are simple expressions, unless otherwise
noted. A property list is a space-separated list of these properties.

If a statement ends with a colon ``:``, then it takes a block. Each line
in a block may be one of two things:

* A property list.
* A screen language statement.

.. _screen-statement:

Screen Statement
----------------

The ``screen`` statement is a Ren'Py script language statement that is
used to declare a new screen. It is parsed using the screen language
common syntax.

It takes one parameter, the name of the screen. This is a name, not an
expression. It takes the following properties:

.. screen-property:: modal

    If True, the screen is modal. A modal screen prevents the user
    from interacting with displayables below it, except
    for the default keymap. This is evaluated once, when the
    game starts.

.. screen-property:: sensitive

    An expression that determines whether the screen is sensitive or not.
    This expression is evaluated at least once per interaction.

.. screen-property:: tag

    Parsed as a name, not an expression. This specifies a tag
    associated with this screen. Showing a screen replaces other
    screens with the same tag. This can be used to ensure that only
    one screen of a menu is shown at a time, in the same context.

.. screen-property:: zorder

    This controls how close to the user a screen is displayed. The
    larger the number, the closer the screen is displayed to the
    user. It defaults to 0.

.. screen-property:: variant

    If present, this should be a string or list of strings giving the
    variant of screen to be defined. See :ref:`screen-variants`.

.. screen-property:: style_prefix

    A string that's used to provide a prefix for the style for the
    children of this screen, as :ref:`described below <style-prefix>`.

.. screen-property:: layer

    A string giving the name of the layer the screen is shown on by
    default.

.. screen-property:: roll_forward

    If true, roll forward will be enabled when the screen is used in a
    ``call screen`` statement. If false, roll forward is disabled, and
    if None or not given, the value of :var:`config.call_screen_roll_forward`
    is used.

    When roll forwarding from a ``call screen`` statement, return values
    and terminal jumps are preserved, but other side effects will not
    occur. This means that if the screen only contains :func:`Jump`
    and :func:`Return` actions, it's safe to enable `roll_forward`. Other
    actions may have side-effects that will not occur during the roll_forward.

If the first line of a screen is a Python string, it is used as the docstring for
the screen. The docstring can be retrieved with :func:`renpy.get_screen_docstring`.

::

   screen hello_world():
        """
        Displays a hello world message.
        """

        tag example
        zorder 1
        modal False

        text "Hello, World."

A screen can take a parameter list::

   screen center_text(s, size=42):
        text s size size

If a screen has no parameters, it still should be given empty
parentheses. If any other screen ``use``\ s a screen with no
parentheses, the difference in behavior are described in the section
concerning :ref:`the use statement <sl-use>`. If no other screen
``use`` a given screen, not giving parentheses to that screen leads to
pure inefficiency in the way Ren'py works internally, see the
:doc:`screen optimization section <screen_optimization>` concerning
parameters.


User Interface Statements
=========================

The user interface statements create displayables and add them either
to the screen, or to an enclosing displayable. They allow the user to
display information, allow the user to interact with the game, or
allow the game to react to various events.

.. _common-properties:

All user interface statements take the following common properties:

.. screen-property:: at

    This can be a transform, or a list of transforms, or an anonymous
    transform (a transform that is defined directly in at) ::

        transform hello_t:
            align (0.7, 0.5) alpha 0.0
            linear 0.5 alpha 1.0

        screen hello_title():
            text "Hello." at hello_t
            text "Hello." at transform:
                align (0.2, 0.5) alpha 0.0
                linear 0.5 alpha 1.0

    This transforms are used to wrap this displayable. The show, hide,
    replace, and replaced external events are delivered to a transform
    if and only if it is added directly to the screen.

    For example, if a vbox is wrapped in a transform, and added directly
    to the screen, then events are delivered to that transform. But if
    a transform wraps a textbutton that is added to the vbox, this
    second transform is not given events.

    It's possible for a single statement to have both an `at` property
    and an ``at transform``. The property must come first, and is
    applied first. ::

        screen title():
            add "title background":
                at sepia

            text "The Title of the Game":
                at sepia, truecenter
                at transform:
                    alpha 0.0
                    linear 0.5 alpha 1.0

.. screen-property:: default_focus

    If given and true, the displayable is focused by default. When
    multiple displayables have this, the values are compared and the
    displayable with the greatest default focus becomes the default.

    The default focus is only used when the last interaction was not
    a mouse click, mouse movement, or touch.

.. screen-property:: extra_alt

    This is used to specify extra alt text for :doc:`self_voicing`.
    If defined, the extra alt text is spoken to the player when the
    '?' key is pressed, and self-voicing ie enabled.

    The ``extra_alt`` is inherited by all children of the displayable,
    unless they have a more specific ``extra_alt`` set.

    Extra alt text is intended to provide vision-impaired players with
    additional information about groups of displayables.

.. screen-property:: focus

    Takes a string or integer, and gives a name to the displayable
    for focus purposes. Ren'Py looks for structural similarity between
    focus names when deciding with displayable to give focus to at the
    start of an interaction. If a box is given a focus name, and the
    third button in that box is focused at the end of an interaction,
    the third button of a box with the same will be highlighted at
    the start of the next interaction.

.. screen-property:: group_alt

    This is used to specify a group prefix for :doc:`self_voicing`.
    When self-voicing is enabled, a group prefix is spoken the first time a displayable
    with the same group prefix is focused, but will not be spoken again until a
    displayable with a different group prefix is focused.

    The ``group_alt`` is inherited by all children of the displayable,
    unless they have a more specific ``group_alt`` set.

.. screen-property:: id

    An identifier for the user-interface statement. When a screen is
    shown, property values can be supplied for the displayables with a
    given identifier. Some screens will require that a displayable
    with a given identifier is created.

    When a displayable is created with an id, the id is stored as a
    string ion a attribute named id on the Displayable object.

.. screen-property:: prefer_screen_to_id

    If true, when a property is provided by both the screen and a
    displayable identifier, the screen property is used. If false, the
    default, the displayable property is used. (This can be used to
    decide if the screen overrides properties set by a Character.)

.. screen-property:: style

    A string giving the name of the style applied to this displayable. The
    style gives default values for style properties.

.. screen-property:: style_prefix

    .. _style-prefix:

    Provides a prefix to the style of this displayable and all of its
    children, unless those children have a more specific style or
    style prefix set.

    The style name is created by concatenating a style prefix, underscore,
    and a style suffix. The style suffix is either specified using
    `style_suffix`, or determined by the displayable.

    For example, if a vbox has a style prefix of ``"pref"``, the vbox
    will be given the style ``"pref_vbox"``. Unless a more specific style
    or style prefix is set, a button inside the vbox will have the style
    ``"pref_button"``.

    Styles accessed in this way are automatically created, if the style
    does not exist. Setting a prefix of ``None`` removes the prefix from
    this displayable and its children.

.. screen-property:: style_group

    An alias for `style_prefix`, used in older versions of Ren'Py.

.. screen-property:: style_suffix

    Specifies the suffix that is combined with the `style_prefix` to
    generate a style name. If this is ``"small_button"`` and the
    style prefix is ``"pref"``, the style ``"pref_small_button"`` is
    used.

    If no style prefix is in use, this is used directly as the name of
    the style. A style suffix applies to a single displayable only, not
    a displayable and all children.

.. screen-property:: tooltip

    Assigns a tooltip to this displayable. When the displayable gains
    focus, the value of this property will be made available from the
    :func:`GetTooltip` function. See the :ref:`tooltips` section for
    more details.

    Objects passed to tooltip must support equality. If equality is
    not supported, an infinite loop may occur.

.. screen-property:: arguments

    A tuple or list containing additional positional arguments that
    are given to the displayable.

.. screen-property:: properties

    A dictionary containing additional properties given to the
    displayable.

Many user interface statements take classes of style properties, or
transform properties. These properties can have a style prefix
associated with them, that determines when they apply. For example, if
text is given the ``hover_size`` property, it sets the text size when the
text is hovered.

User interface statements take an ``as`` clause, which takes a variable
name, without any quotes. The displayable that the statement creates is
assigned to the variable. (An example can be found in :ref:`the drag and drop
documentation <as-example>`.)

.. _sl-bar:

Bar
---

Creates a horizontally-oriented bar that can be used to view or adjust
data. It takes the following properties:

.. screen-property:: value

    The current value of the bar. This can be either a :ref:`bar value <bar-values>`
    object, or a number.

.. screen-property:: range

    The maximum value of the bar. This is required if `value` is a
    number.

.. screen-property:: adjustment

    A :func:`ui.adjustment` object that this bar adjusts.

.. screen-property:: changed

    If given, this should be a Python function. The function is called
    with the value of the adjustment when the adjustment is changed.

.. screen-property:: hovered

    An action to run when the bar gains focus.

.. screen-property:: unhovered

    An action to run when the bar loses focus.

.. screen-property:: released

    An action to run when the bar button is released. This will be invoked
    even if the bar has not changed its value.

.. screen-property:: thumb_align

    The alignment of the bar thumb, relative to the bar. If the bar and
    thumb are different sizes - for example, the thumb is taller than the
    height of a horizontal bar - thumb_align can be set to 0.5 so the centers
    of the bar and thumb are aligned.

One of `value` or `adjustment` must be given. In addition, this
function takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`bar-style-properties`

This does not take children.

::

    screen volume_controls():
        frame:
            has vbox

            bar value Preference("sound volume") released Play("sound", "audio/sample_sound.ogg")
            bar value Preference("music volume")
            bar value Preference("voice volume")

.. _sl-button:

Button
------

Creates an area of the screen that can be activated to run an
action. A button takes no parameters, and the following properties.

.. screen-property:: action

    The action to run when the button is activated. A button is activated
    when it is clicked, or when the player selects it and hits enter on the
    keyboard. This also controls if the button is sensitive if `sensitive`
    is not provided or None, and if the button is selected if `selected` is not
    provided or None.

.. screen-property:: alternate

    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

.. screen-property:: hovered

    An action to run when the button gains focus.

.. screen-property:: unhovered

    An action to run when the button loses focus.

.. screen-property:: selected

    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine selectedness.

.. screen-property:: sensitive

    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine sensitivity.

.. screen-property:: keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

.. screen-property:: alternate_keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

It takes one child. If zero, two, or more children are supplied,
they are implicitly added to a fixed, which is added to the button.


.. _sl-dismiss:

Dismiss
-------

The dismiss statement creates the highly specialized dismiss displayable,
which gains focus when no other displayable has focus,
and runs an action when it's activated. In this regard, it works
very similarly to the behavior of the say statement.

This is rarely used, and mostly to allow a modal frame to be
dismissed when the player clicks outside it, as might be the case
with a popup window.

This takes the following properties:

.. screen-property:: action

    The action performed when the dismiss is activated. This property is
    required.

.. screen-property:: keysym

    A string giving a :doc:`keysym <keymap>` describing a key that,
    when pressed, invokes the action of this dismiss. This replaces the default
    "dismiss" keysym.

.. screen-property:: modal

    By default, the dismiss is modal, preventing events from being processed
    by displayables "behind" it.


It also takes:

* :ref:`Common Properties <common-properties>`
* The :propref:`hover_sound` and :propref:`activate_sound` style properties.

Here's an example of dismiss being used::

    screen dismiss_test():

        dismiss action Return()

        frame:
            modal True

            align (.5, .3)
            padding (20, 20)

            has vbox

            text "This is a very important message.":
                xalign 0.5
                textalign 0.5

            # Dismiss can be confusing on its own, so we'll add a button as well.
            textbutton "Dismiss":
                xalign 0.5
                action Return()

See also how dismiss is used in conjunction with :ref:`nearrect <sl-nearrect>`.

.. _sl-fixed:

Fixed
-----

This creates an area to which children can be added. By default, the
fixed expands to fill the available area, but the :propref:`xmaximum`
and :propref:`ymaximum` properties can change this.

The children are laid out according to their position style
properties. They can overlap if not positioned properly.

The fixed statement takes no parameters, and the following groups of
properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`fixed-style-properties`

This takes any number of children, which are added to the fixed.

It's often unnecessary to explicitly create a fixed displayable. Each
screen is contained within a fixed displayable, and many screen
language statements automatically create a fixed displayable if they
have two or more children.

::

    screen ask_are_you_sure:
        fixed:
             text "Are you sure?" xalign 0.5 yalign 0.3
             textbutton "Yes" xalign 0.33 yalign 0.5 action Return(True)
             textbutton "No" xalign 0.66 yalign 0.5 action Return(False)


.. _sl-frame:

Frame
-----

A frame is a window that contains a background that is intended for
displaying user-interface elements like buttons, bars, and text. It
takes the following groups of properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`

It takes one child. If zero, two, or more children are supplied, then
a fixed is created to contain them.

::

    screen test_frame():
        frame:
            xpadding 10
            ypadding 10
            xalign 0.5
            yalign 0.5

            vbox:
                text "Display"
                null height 10
                textbutton "Fullscreen" action Preference("display", "fullscreen")
                textbutton "Window" action Preference("display", "window")

.. _sl-grid:

Grid
----

This displays its children in a grid. Each child is given an area of
the same size, the size of the largest child.

It takes two parameters. The first is the number of columns in the
grid, and the second is the number of rows in the grid. If the grid
is not full, the remaining cells are filled with the ``null`` displayable.

Grid takes several properties related to the way its children are placed:

.. screen-property:: transpose

    If False (the default), rows are filled before columns. If True,
    then columns are filled before rows.

.. screen-property:: right_to_left

    If True, cells are filled from right to left, instead of the default
    left to right.

.. screen-property:: bottom_to_top

    If True, cells are filled from bottom to top, instead of the default
    top to bottom.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`grid-style-properties`

This must be given (columns * rows) children. Giving it a different
number of children is an error.

::

    screen grid_test:
         grid 2 3:
             text "Top-Left"
             text "Top-Right"

             text "Center-Left"
             text "Center-Right"

             text "Bottom-Left"
             text "Bottom-Right"

.. _sl-hbox:

Hbox
----

This displays its children side by side, in an invisible horizontal
box. It takes no parameters, and the following groups of properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`box-style-properties`

UI displayable children are added to the box.

::

   screen hbox_text():
       hbox:
            text "Left"
            text "Right"


.. _sl-imagebutton:

Imagebutton
-----------

Creates a button consisting of images, that change state when the user
hovers over them. This takes no parameters, and the following
properties:

.. screen-property:: auto

    Used to automatically define the images used by this button. This
    should be a string that contains %s in it. If it is, and one of
    the image properties is omitted, %s is replaced with the name of
    that property, and the value is used as the default for that
    property.

    For example, if `auto` is "button_%s.png", and `idle` is omitted, then
    idle defaults to "button_idle.png". Similarly, if `auto` is "button %s",
    the ``button idle`` image is used.

    The behavior of `auto` can be customized by changing
    :var:`config.imagemap_auto_function`.


.. screen-property:: insensitive

    The image used when the button is insensitive.

.. screen-property:: idle

    The image used when the button is not focused.

.. screen-property:: hover

    The image used when the button is focused.

.. screen-property:: selected_idle

    The image used when the button is selected and idle.

.. screen-property:: selected_hover

    The image used when the button is selected and hovered.

.. screen-property:: action

    The action to run when the button is activated. This also controls if
    the button is sensitive if `sensitive` is not provided or None, and if the button
    is selected if `selected` is not provided or None.

.. screen-property:: alternate

    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

.. screen-property:: hovered

    An action to run when the button gains focus.

.. screen-property:: unhovered

    An action to run when the button loses focus.

.. screen-property:: selected

    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine selectedness.

.. screen-property:: sensitive

    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine sensitivity.

.. screen-property:: keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

.. screen-property:: alternate_keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

This takes no children.

::

    screen gui_game_menu():
         vbox xalign 1.0 yalign 1.0:
              imagebutton auto "save_%s.png" action ShowMenu('save')
              imagebutton auto "prefs_%s.png" action ShowMenu('preferences')
              imagebutton auto "skip_%s.png" action Skip()
              imagebutton auto "afm_%s.png" action Preference("auto-forward mode", "toggle")


.. _sl-input:

Input
-----

Creates a text input area, which allows the user to enter text. When
the user presses return, the text will be returned by the
interaction. (When the screen is invoked through ``call screen``, the result
will be placed in the ``_return`` variable.)

Due to limitations in supporting libraries, on Android and the web platform
the input displayable is limited to alphabetic characters.

The input statement takes no parameters, and the following properties:

.. screen-property:: value

    An :ref:`input value <input-values>` object that this input uses.
    InputValue objects determine where the default value is taken from,
    what happens when the text is changed, what happens when enter is
    pressed, and if the text is editable by default.

    This should not be given at the same time as `default` and `changed`.

.. screen-property:: default

    The default text in this input.

.. screen-property:: length

    The maximum length of the text in this input.

.. screen-property:: pixel_width

    The maximum pixel width of the input. If typing a character would
    cause the input to exceed this width, the keypress is ignored.

.. screen-property:: allow

    A string containing characters that are allowed to be typed into
    this input. (By default, allow all characters.)

.. screen-property:: exclude

    A string containing characters that are disallowed from being
    typed into this input. (By default, "{}".)

.. screen-property:: copypaste

    If True, it becomes possible to copy and paste
    into this input. (By default, disabled.)

.. screen-property:: prefix

    An immutable string to prepend to what the user has typed.

.. screen-property:: suffix

    An immutable string to append to what the user has typed.

.. screen-property:: changed

    A Python function that is called with what the user has typed,
    when the string changes.

.. screen-property:: mask

    If given, a string that replaces each displayable character in
    the text. This can be used to mask out a password.

.. screen-property:: caret_blink

    If not False, the blinking period of the default caret.
    Overrides :var:`config.input_caret_blink`.

.. screen-property:: multiline

    If true, it becomes possible to move caret on the next line
    using keyboard (Shift+Enter by default,
    can be changed by modifying config.keymap['input_next_line']).

.. screen-property:: action

    If not None, an action that is run when enter is pressed and the
    input is active. This overrides the default action of returning
    the input value.

    Generally, this is is used with a `value` that stores the input into
    a variable, so the action can access it.

.. screen-property:: arrowkeys

    If True (the default), the arrow keys can be used to move the caret left and right
    within the input. If False, arrow keys are ignored, making them available for other uses,
    like changing focus.


It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`text-style-properties`

This does not take any children.

::

    screen input_screen():
        window:
            has vbox

            text "Enter your name."
            input default "Joseph P. Blow, ESQ."


.. _sl-key:

Key
---

This creates a keybinding that runs an action when a key is pressed,
or one of the keys in a given list. Key is used in a loose sense here,
as it also allows joystick and mouse events.

Key takes one positional parameter, a string giving the key to
bind. See the :doc:`keymap` section for a description of available
keysyms. It takes two properties:

.. screen-property:: action

    This gives an action that is run when the key is pressed. This
    property is mandatory.

.. screen-property:: capture

    If true, the default, the event will capture, and will not be
    processed by other displayables. If false and the action does
    not end the interaction, the event will be processed by other
    displayables.

It takes no children.

::

    screen keymap_screen():
        key "game_menu" action ShowMenu('save')
        key "p" action ShowMenu('preferences')
        key ["s", "w"] action Screenshot()


.. _sl-label:

Label
-----

Creates a window in the label style, and then places text inside that
window. Together, this combination is used to label things inside a
frame.

It takes one positional argument, the text of the label. It takes
the property:

.. screen-property:: text_style

    The name of the style to use for the button text. If not supplied,
    and the `style` property is a string, then ``"_text"`` is appended
    to that string to give the default text style.

.. screen-property:: text_-

   Other properties prefixed with text_ have this prefix stripped, and
   are then passed to the text displayable.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`

It does not take children.

::

    screen display_preference():
        frame:
            has vbox

            label "Display"
            textbutton "Fullscreen" action Preference("display", "fullscreen")
            textbutton "Window" action Preference("display", "window")


.. _mousearea:
.. _sl-mousearea:

Mousearea
---------

A mouse area is an area of the screen that can react to the mouse
entering or leaving it. Unlike a button, a mouse area does not take
focus, so it's possible to have a mouse area with buttons inside it.
The ``mousearea`` statement takes no parameters, and the following properties:

.. screen-property:: hovered

    An action to run when the mouse enters the mouse area.

.. screen-property:: unhovered

    An action to run when the mouse leaves the mouse area.

.. screen-property:: focus_mask

    The :propref:`focus_mask` style property, which may be a Displayable
    or None. If a displayable, the mousearea will only be hovered if the
    mouse is over an opaque portion of the displayable. (The displayable
    is not shown to the user.)

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

It does not take children.

Usually, a mousearea statement is given the :propref:`area` style
property, which controls the size and position of the mouse
area. Without some way of controlling its size, the mouse area would
take up the entire screen, a less useful behavior.

.. note::

    Since Ren'Py games can be played using the keyboard and joystick, it
    often makes sense to duplicate mousearea functionality by some other
    means.

::

    screen button_overlay():
        mousearea:
            area (0, 0, 1.0, 100)
            hovered Show("buttons", transition=dissolve)
            unhovered Hide("buttons", transition=dissolve)

    screen buttons():
        hbox:
            textbutton "Save" action ShowMenu("save")
            textbutton "Prefs" action ShowMenu("preferences")
            textbutton "Skip" action Skip()
            textbutton "Auto" action Preference("auto-forward", "toggle")

    label start:
        show screen button_overlay

.. _sl-nearrect:

Nearrect
--------

The ``nearrect`` statement takes a single child, and lays that child out
at a location near a rectangle. Usually, this is a rectangle focus captured using
the :func:`CaptureFocus` action. This can be used for tooltips and dropdown or
pulldown menus.

Nearrect takes the following properties:

.. screen-property:: rect

    If given, this should be an (x, y, w, h) rectangle that the child is
    positioned relative to, as described below.

.. screen-property:: focus

    If given, this should be a string. This string is passed to the equivalent of
    :func:`GetFocusRect` to find the rectangle. If a focus rectangle with that
    name is found, the child is rendered.

    Passing "tooltip" to this uses the location of the last displayable that
    was focused while displaying a tooltip.

    If present, overrides `rect`

.. screen-property:: preferred_side

    One of ``"left"``, ``"top"``, ``"right"``, ``"bottom"`` to prefer that
    position for the nearrect. If there is not room on one side, the opposite
    side is used. By default, the preferred side is "bottom".

.. screen-property:: prefer_top

    Deprecated. Equivalent to ``preferred_side "top"``

.. screen-property:: invert_offsets

    If True and there isn't enough space on the preferred side, multiply
    xoffset and yoffset by -1 since the child will be on the opposite side of
    the rectangle. False by default.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`


Nearrect differs from the other layouts in that it positions its child near the
given rectangle, rather than inside it. For a `preferred_side` of ``"top"`` or
``"bottom"`` (resp. ``"left"``, ``"right"``), the child is first rendered with
the full width (resp. height) available, and the maximum of the height
(resp. width) above and below the rectangle. The y position (resp. x position)
is then computed as followed.

* If the child will fit on the `preferred_side` of the rectangle, the child is
  positioned directly adjacent to the rectangle.
* Otherwise, if the child can fit opposite the `preferred_side` of the
  rectangle, it's positioned there.
* Otherwise, the child is positioned directly adjacent to the rectangles's
  `preferred_side`.

The x positioning (resp. y position) is computed using the normal rules, using
the :propref:`xpos` and :propref:`xanchor` properties (resp. :propref:`ypos`,
:propref:`yanchor`) of the child, and properties that set them, such as
:propref:`xalign`. The pos properties are relative to the x coordinate
(resp. y coordinate) of the rectangle, and in the case of a floating point
number, the width (resp. height).

At the end of positioning, the :propref:`xoffset` and :propref:`yoffset`
properties are applied as normal.

If the child of the nearrect is a transform, the transform is given ``show``
and ``hide`` events. However, the position will change instantly. Nearrect
works best on the top of a screen, with transforms and positioning applied
to its child, rather the nearrect.

One use of nearrect is for dropdown menus::

    default difficulty = "Easy"

    screen select_difficulty():

        # This frame can be a very complex layout, if required.
        frame:
            align (.5, .3)
            padding (20, 20)

            has vbox

            # This is the button that is clicked to enable the dropdown
            textbutton "Difficulty: [difficulty]":

                # This action captures the focus rectangle, and in doing so,
                # displays the dropdown.
                action CaptureFocus("diff_drop")

            textbutton "Done":
                action Return()

        # All sorts of other screen elements could be here, but the nearrect needs
        # to be at the top level, and the last thing shown, apart from its child.

        # Only if the focus has been captured, display the dropdown.
        # You could also use showif instead of basic if
        if GetFocusRect("diff_drop"):

            # If the player clicks outside the frame, dismiss the dropdown.
            # The ClearFocus action dismisses this dropdown.
            dismiss action ClearFocus("diff_drop")

            # This positions the displayable near (usually under) the button above.
            nearrect:
                focus "diff_drop"

                # Finally, this frame contains the choices in the dropdown, with
                # each using ClearFocus to dismiss the dropdown.
                frame:
                    modal True

                    has vbox

                    textbutton "Easy" action [ SetVariable("difficulty", "Easy"), ClearFocus("diff_drop") ]
                    textbutton "Medium" action [ SetVariable("difficulty", "Medium"), ClearFocus("diff_drop") ]
                    textbutton "Hard" action [ SetVariable("difficulty", "Hard"), ClearFocus("diff_drop") ]
                    textbutton "Nightmare" action [ SetVariable("difficulty", "Nightmare"), ClearFocus("diff_drop") ]

Dropdowns may benefit from improved styling, which isn't done here.


.. _sl-null:

Null
----

The null statement inserts an empty area on the screen. This can be
used to space things out. The null statement takes no parameters, and
the following properties:

.. screen-property:: width

    The width of the empty area, in pixels.

.. screen-property:: height

    The height of the empty area, in pixels.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

It does not take children.

::

    screen text_box():
        vbox:
             text "The title."
             null height 20
             text "This body text."


.. _sl-side:

Side
----

This positions displayables in the corners or center of a grid. It
takes a single parameter, string containing a space-separated list of
places to place its children. Each component of this list should be
one of:

    'c', 't', 'b', 'l', 'r', 'tl', 'tr', 'bl', 'br'

'c' means center, 't' top, 'tl' top left, 'br' bottom right, and so on.

A side takes the following properties:

.. screen-property:: spacing

    The spacing between the rows and columns of the grid.


A side takes the following property groups:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

When being rendered, this first sizes the corners, then the sides,
then the center. The corners and sides are rendered with an available
area of 0, so it may be necessary to supply them a minimum size (using
:propref:`xminimum` or :propref:`yminimum`) to ensure they render at
all.
The order of placing children is controlled from top to bottom when
adding them (i.e. also in the order of substrings in the argument),
the latter will be the highest. This is may be disabled by
:var:`config.keep_side_render_order`.

Children correspond to entries in the places list, so this must have
the same number of children as there are entries in the places list.

::

    screen side_test():
         side "c tl br":
              text "Center"
              text "Top-Left"
              text "Bottom-Right"

.. _sl-text:

Text
----

The text statement displays text. It takes a single parameter, the
text to display. It also takes the following groups of properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`text-style-properties`

It does not take children.

::

    screen hello_world():
        text "Hello, World." size 40

.. _sl-textbutton:

Textbutton
----------

Creates a button containing a text label. The button takes a single
parameter, the text to include as part of the button. It takes the
following properties:

.. screen-property:: action

    The action to run when the button is activated. This also controls if
    the button is sensitive if `sensitive` is not provided or None, and if the button
    is selected if `selected` is not provided or None.

.. screen-property:: alternate

    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

.. screen-property:: hovered

    An action to run when the button gains focus.

.. screen-property:: unhovered

    An action to run when the button loses focus.

.. screen-property:: selected

    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine selectedness.

.. screen-property:: sensitive

    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine sensitivity.

.. screen-property:: keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

.. screen-property:: alternate_keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

.. screen-property:: text_style

    The name of the style to use for the button text. If not supplied,
    and the `style` property is a string, then ``"_text"`` is appended
    to that string to give the default text style.

.. screen-property:: text_-

    Other properties prefixed with text_ have this prefix stripped, and are
    then passed to the text displayable.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

It does not take children.

::

    screen textbutton_screen():
        vbox:
            textbutton "Wine" action Jump("wine")
            textbutton "Women" action Jump("women")
            textbutton "Song" action Jump("song")

.. _sl-timer:

Timer
-----

This creates a timer that runs an action when time runs out. It takes
one positional parameter, giving the timeout time, in seconds. It
takes the properties:

.. screen-property:: action

    This gives an action that is run when the timer expires. This
    property is mandatory.

.. screen-property:: repeat

    If True, the timer repeats after it times out.

.. screen-property:: modal

    If True, the timer will not fire if it is blocked by a modal
    screen. If false or not given, the timer will fire even if it
    is blocked by a modal screen.


Timer takes no children.

::

    screen timer_test():
        vbox:
             textbutton "Yes." action Jump("yes")
             textbutton "No." action Jump("no")

        timer 3.0 action Jump("too_slow")

.. _sl-transform:

Transform
---------

Applies a transform to its child. This takes no parameters, and the
following property groups:

* :ref:`Common Properties <common-properties>`
* :ref:`Transform Properties <transform-properties>`

This should take a single child.


.. _sl-vbar:

Vbar
----

The vertically oriented equivalent of `bar`_. Properties are the same
as `bar`.

::

    screen volume_controls():
         frame:
             has hbox

             vbar value Preference("sound volume")
             vbar value Preference("music volume")
             vbar value Preference("voice volume")


.. _sl-vbox:

Vbox
----

This displays its children one above the other, in an invisible
vertical box. It takes no parameters, and the following groups of
properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`box-style-properties`

UI displayable children are added to the box.

::

    screen vbox_test():
        vbox:
             text "Top."
             text "Bottom."


.. _sl-viewport:

Viewport
--------

A viewport is area of the screen that can be scrolled by dragging,
with the mouse wheel, or with scrollbars. It can be used to display
part of something that is bigger than the screen. It takes the
following properties:

.. screen-property:: child_size

    The size that is offered to the child for rendering. An (`xsize`,
    `ysize`) tuple. This can usually be omitted, when the child can
    compute it's own size. If either component is None, the child's
    size is used.

.. screen-property:: mousewheel

    This should be one of:

    False
        To ignore the mousewheel. (The default.)
    True
        To scroll vertically.
    "horizontal"
        To scroll horizontally.
    "change"
        To scroll the viewport vertically, only if doing so would cause the
        viewport to move. If not, the mousewheel event is passed to the rest
        of the interface. (For example, if change is given, placing
        ``key "viewport_wheeldown" action Return()`` before the viewport
        will cause the screen to return if the viewport scrolls past the
        bottom.)
    "horizontal-change"
        Combines horizontal scrolling with change mode.

.. screen-property:: draggable

    If True, dragging the mouse will scroll the viewport. This can also be
    a :ref:`variant <screen-variants>`, in which case the viewport will be draggable
    if the variant is in place. (For example, ``draggable "touch"``.)

.. screen-property:: edgescroll

    Controlls scrolling when the mouse reaches the edge of the
    viewport. If not None, this should be a two- or three-element
    tuple:

    * The first element in the tuple is the distance from
      the edge of the viewport that edgescrolling begins to take
      effect, in pixels.

    * The second element is the maximum scrolling rate, in pixels per
      second.

    * If present, the third element is a function that adjusts the
      scrolling speed, based on how close to the pointer is to an
      edge. The function should take a number between -1.0 and 1.0, and
      return a number in the same range. The default function returns
      its input, and implements proportional scrolling.  A function
      that returned -1.0 or 1.0 based on the sign of its input would
      implement constant-speed scrolling.

.. screen-property:: xadjustment

    The :func:`ui.adjustment` used for the x-axis of the
    viewport. When omitted, a new adjustment is created.

.. screen-property:: yadjustment

    The :func:`ui.adjustment` used for the y-axis of the
    viewport. When omitted, a new adjustment is created.

.. screen-property:: xinitial

    The initial horizontal offset of the viewport. This may be an integer
    giving the number of pixels, or a float giving a fraction of the
    possible offset.

.. screen-property:: yinitial

    The initial vertical offset of the viewport. This may be an integer
    giving the number of pixels, or a float giving a fraction of the
    possible offset.

.. screen-property:: scrollbars

    If not None, scrollbars are added along with this viewport.
    This works by creating a side layout, and placing the created
    viewport in the center of the side. If `scrollbars` is "horizontal",
    a horizontal scrollbar is placed beneath the viewport. If `scrollbars`
    is "vertical", a vertical scrollbar is placed to the right of the
    viewport. If `scrollbars` is "both", both horizontal and vertical
    scrollbars are created.

    When `scrollbars` is not None, the `viewport` takes prefixed properties:

    * Properties beginning with ``viewport_`` are passed to the viewport.
    * Properties beginning with ``side_`` are passed to the side.
    * Properties beginning with ``scrollbar_`` are passed to the horizontal scrollbar, if it exists.
    * Properties beginning with ``vscrollbar_`` are passed to the vertical scrollbar, if it exists.

    Unprefixed properties are also accepted. :ref:`position-style-properties` are
    passed to the side, while other unprefixed properties are supplied to the
    viewport.

.. screen-property:: arrowkeys

    If true, the viewport can be scrolled with the left, right, up, and down
    arrow keys. This takes precedence over the usual function of these keys,
    which is changing focus. However, the arrow keys will change focus when the
    viewport reaches its limits.

.. screen-property:: pagekeys

    If true, the viewport can be scrolled up and down by the pageup and
    pagedown keys. This disables the usual functionality of these keys,
    which is to cause rollback and rollforward.

In addition, it takes the following groups of style properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

It takes one child. If zero, two, or more children are supplied, then
a fixed is created to contain them.

To make a viewport scrollable, it's often best to assign an id to it,
and then use :func:`XScrollValue` and :func:`YScrollValue` with that
id.

::

    screen viewport_example():
        side "c b r":
             area (100, 100, 600, 400)

             viewport id "vp":
                 draggable True

                 add "washington.jpg"

             bar value XScrollValue("vp")
             vbar value YScrollValue("vp")


.. _sl-vpgrid:

Vpgrid
------

A vpgrid (viewport grid) combines a viewport and grid into a single
displayable. The vpgrid takes multiple children (like a grid) and is
optimized so that only the children being displayed within the viewport
are rendered.

A vpgrid assumes that all children are the same size, the size being taken
from the dimensions of the first child. If a vpgrid appears to be rendering
incorrectly, please ensure that all children are of the same size.

A vpgrid must be given at least one of the `cols` and `rows` properties.
If one is omitted or None, the other is automatically determined from the
size, spacing, and number of children. If a row or column would be underfull,
``null`` displayable are used to fill the remaining space.

Vpgrids take the following properties:

.. screen-property:: cols

    The number of columns in the grid.

.. screen-property:: rows

    The number of rows in the grid.

.. screen-property:: transpose

    If true, columns are filled before rows. The default of this depends
    on the `cols` and `rows` properties. If `cols` is given, columns
    are filled before rows, otherwise rows are filled before columns.

In addition, a vpgrid takes all properties a :ref:`viewport <sl-viewport>` can,
and the following groups of style properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`grid-style-properties`

When the `scrollbar` property is given, prefixed properties are passed to
the vpgrid in the same way as they are with viewports. (Properties prefixed
with ``viewport_`` are passed to the vpgrid itself.)

::

    screen vpgrid_test():

        vpgrid:

            cols 2
            spacing 5
            draggable True
            mousewheel True

            scrollbars "vertical"

            # Since we have scrollbars, this positions the side, rather than
            # the vpgrid.
            xalign 0.5

            for i in range(1, 101):

                textbutton "Button [i]":
                    xysize (200, 50)
                    action Return(i)



.. _sl-window:

Window
------

A window is a window that contains a background that is intended for
displaying in-game dialogue. It takes the following groups of
properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`

It takes one child. If zero, two, or more children are supplied, then
a fixed is created to contain them.

::

    screen say(who, what):
        window id "window"
            vbox:
                spacing 10

                text who id "who"
                text what id "what"


Imagemap Statements
===================

A convenient way of creating a screen, especially for those who think
visually, is to create an imagemap. When creating an imagemap, the
imagemap statement is used to specify up to six images. The hotspot
and hotbar images are used to carve rectangular areas out of the
image, and apply actions and values to those areas.

Here's an example of a preferences screen that uses imagemaps.

::

    screen preferences():

        tag menu
        use navigation

        imagemap:
            auto "gui_set/gui_prefs_%s.png"

            hotspot (740, 232, 75, 73) action Preference("display", "fullscreen") alt _("Display Fullscreen")
            hotspot (832, 232, 75, 73) action Preference("display", "window") alt _("Display Window")
            hotspot (1074, 232, 75, 73) action Preference("transitions", "all") alt _("Transitions All")
            hotspot (1166, 232, 75, 73) action  Preference("transitions", "none") alt _("Transitions None")

            hotbar (736, 415, 161, 20) value Preference("music volume") alt _("Music Volume")
            hotbar (1070, 415, 161, 20) value Preference("sound volume") alt _("Sound Volume")
            hotbar (667, 535, 161, 20) value Preference("voice volume") alt _("Voice Volume")
            hotbar (1001, 535, 161, 20) value Preference("text speed") alt _("Text Speed")


.. _sl-imagemap:

Imagemap
--------

The imagemap statement is used to specify an imagemap. It takes no
parameters, and the following properties:

.. screen-property:: auto

    Used to automatically define the images used by this imagemap. This
    should be a string that contains %s in it. If it is, and one of
    the image properties is omitted, %s is replaced with the name of
    that property, and the value is used as the default for that
    property.

    For example, if `auto` is "imagemap_%s.png", and `idle` is omitted, then
    idle defaults to "imagemap_idle.png". If `auto` is "imagemap %s", the
    ``imagemap idle`` image is used.

    The behavior of `auto` can be customized by changing
    :var:`config.imagemap_auto_function`.

.. screen-property:: ground

    The image used for portions of the imagemap that are not part of a
    hotspot or hotbar.

.. screen-property:: insensitive

    The image used when a hotspot or hotbar is insensitive.

.. screen-property:: idle

    The image used when a hotspot is not selected and not focused, and
    for the empty portion of unfocused hotbars.

.. screen-property:: hover

    The image used when a hotspot is not selected and focused, and
    for the empty portion of focused hotbars.

.. screen-property:: selected_idle

    The image used when a hotspot is selected and not focused, and
    for the full portion of unfocused hotbars.

.. screen-property:: selected_hover

    The image used when a hotspot is selected and focused, and
    for the full portion of focused hotbars.

.. screen-property:: alpha

    If true, the default, a hotspot only gains focus when the mouse is
    in an area of the hover image that is opaque. If false, the hotspot
    gains focus whenever the mouse is within its rectangular boundary.

.. screen-property:: cache

    If true, the default, hotspot data is cached in to improve performance
    at the cost of some additional disk space.

It takes the following groups of properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`fixed-style-properties`

An imagemap creates a fixed, allowing any child to be added to it (not
just hotspots and hotbars).


.. _sl-hotspot:

Hotspot
-------

A hotspot is a button consisting of a portion of the imagemap that
contains it. It takes a single parameter, a (x, y, width, height)
tuple giving the area of the imagemap that makes up the button. It
also takes the following properties:

.. screen-property:: action

    The action to run when the button is activated. This also controls
    if the button is sensitive, and if the button is selected.

.. screen-property:: alternate

    An action that is run if the hotspot is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the hotspot
    on a mouse-based platform, or when the player long presses the hotspot
    on a touch-based platform.

.. screen-property:: hovered

    An action to run when the button gains focus.

.. screen-property:: unhovered

    An action to run when the button loses focus.

.. screen-property:: selected

    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine selectedness.

.. screen-property:: sensitive

    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided or None, the action will be used to determine sensitivity.

.. screen-property:: keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

.. screen-property:: alternate_keysym

    A string giving a :doc:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`button-style-properties`

A hotspot creates a fixed, allowing children to be added to it. The
fixed has an area that is the same size as the hotspot, meaning that
the children will be positioned relative to the hotspot.

Hotspots should be given the ``alt`` style property to allow Ren'Py's
self-voicing feature to work.

.. _sl-hotbar:

Hotbar
------

A hotbar is a bar that consists of a portion of the imagemap that
contains it. It takes a single parameter, a (x, y, width, height)
tuple giving the area of the imagemap that makes up the button. It
also takes the following properties:

.. screen-property:: value

    The current value of the bar. This can be either a :ref:`bar value <input-values>`
    object, or a number.

.. screen-property:: range

    The maximum value of the bar. This is required if `value` is a
    number.

.. screen-property:: adjustment

    A :func:`ui.adjustment` object that this bar adjusts.

One of `value` or `adjustment` must be given. In addition, this
function takes:

* :ref:`Common Properties <common-properties>`
* :ref:`bar-style-properties`

This does not take children.

Hotbars should be given the ``alt`` style property to allow Ren'Py's
self-voicing feature to work.

Add Statement
=============

The add statement is a bit special, as it adds an already-existing displayble
to the screen. As a result, it doesn't take the properties common to the
user interface statements.

.. _sl-add:

Add
---

Adds an image or other displayable to the screen. This optionally
takes :ref:`transform properties <transform-properties>`. If at least
one transform property is given, a :class:`Transform` is created to wrap the
image, and the properties are given to the transform.

If the displayable is None, nothing is added to the screen.

This does not take any children.

::

    screen add_test():
        add "logo.png" xalign 1.0 yalign 0.0




Advanced Displayables
=====================

In addition to the commonly-used statements, the screen language has
statements that correspond to advanced displayables. The mapping from
displayable to statement is simple. Positional parameters of the
displayables become positional parameters of the statement. Keyword
arguments and the relevant style properties become screen language
properties.

The advanced displayable statements are:

.. _sl-areapicker:

Areapicker
----------

Intended for use in development tools, this lets the user select a
rectangular area on the screen. It takes the following properties:

.. screen-property:: cols

    If not None, the default, this divides the screen up into a grid
    with this many columns.

.. screen-property:: rows

    If not None, the default, this divides the screen up into a grid
    with this many rows.

.. screen-property:: position

    If not None, the default, this is a function called with the
    x and y coordinates of the location the user first clicked,
    rounded to the grid.

.. screen-property:: changed

    This is called with the rectangle, an (x, y, width, height) tuple,
    whenever the user changes the selected area.

.. screen-property:: finished

    This is called with the rectangle, an (x, y, width, height) tuple,
    when the user finishes selecting an area.

.. screen-property:: persist

    If true, the child will be shown in the selected area when the
    selection is complete. If false, the default, the child will be
    hidden once the selection is complete.

It takes the following group of properties:

* :ref:`Common Properties <common-properties>`

An areapicker takes one child. The child is displayed on the screen in the
selected area.

Drag
----

Creates a :class:`Drag` that can be dragged around the screen. With the
exception of `d`, which is supplied by the screen language, this takes
all properties defined in that class.

It also takes the following properties:

* :ref:`Common Properties <common-properties>`
* The :propref:`hover_sound` and :propref:`activate_sound` style
  properties
* The :propref:`focus_mask` style_property.

A drag takes one child, or the :propref:`child` style property can be
used to supply the child and its focused variants.

Draggroup
---------

Creates a :class:`DragGroup`.  This takes the same properties as :class:`DragGroup`,
and also takes the following properties:

* :ref:`Common Properties <common-properties>`

A drag group may have zero or more drags as its children. It may also have
non-drags as children, in which case it functions like fixed.


.. _sl-has:

Has Statement
=============

The has statement allows you to specify a container to use, instead of
fixed, for statements that take only one child. The has statement
may only be used inside a statement that takes one child. The keyword
``has`` is followed (on the same line) by another statement, which
must be a statement that creates a container displayable, one that
takes more than one child.

The has statement changes the way in which the block that contains it
is parsed. Child displayables created in that block are added to the
container, rather than the parent displayable. Keyword arguments to
the parent displayable are not allowed after the has
statement. Multiple has statements can be used in the same block.

The has statement can be supplied as a child of the following
statements:

* button
* frame
* window

The has statement can be given the following statements as a
container.

* fixed
* grid
* hbox
* side
* vbox

::

   screen volume_controls():
        frame:
            has vbox

            bar value Preference("sound volume")
            bar value Preference("music volume")
            bar value Preference("voice volume")


Control Statements
==================

The screen language includes control statements for conditional
execution, iteration, including other screens, executing actions when
events occur, and executing arbitrary Python.

.. _sl-default:

Default
-------

The ``default`` statement sets the default value of a variable, if it is not
passed as an argument to the screen, or inherited from a screen that calls
us using the use statement.

::

    screen scheduler():
        default club = None
        vbox:
             text "What would you like to do?"
             textbutton "Art Club" action SetScreenVariable("club", "art")
             textbutton "Writing Club" action SetScreenVariable("club", "writing")

             if club:
                 textbutton "Select" action Return(club)


.. _sl-for:

For
---

The ``for`` statement is similar to the Python ``for`` statement, except that
it does not support the ``else`` clause (it does, however, support the
``continue`` and ``break`` statements). It supports assignment to
(optionally nested) tuple patterns, as well as variables.

::

    $ numerals = [ 'I', 'II', 'III', 'IV', 'V' ]

    screen five_buttons():
        vbox:
            for i, numeral in enumerate(numerals):
                textbutton numeral action Return(i + 1)


The for statement takes an index clause::


    screen five_buttons():
        vbox:
            for i, numeral index numeral in enumerate(numerals):
                textbutton numeral action Return(i + 1)

If given, the ``index`` clause should consist of an expression that returns
a hashable and comparable value that is unique for each row in the list.
Ren'Py uses this value to make sure that transforms and other state wind
up associated with the correct iteration. If you're seeing weird behavior
when elements are added to or removed from a list you're iterating over,
you might want to use an index clause.


.. _sl-if:

If
--

The screen language ``if`` statement is the same as the Python/Ren'Py ``if``
statement. It supports the ``if``, ``elif``, and ``else`` clauses.

::

    screen skipping_indicator():
        if renpy.is_skipping():
             text "Skipping."
        else:
             text "Not Skipping."

.. _sl-on:

On
--

The ``on`` statement allows the screen to execute an action when an event
occurs. It takes one parameter, a string giving the name of an
event. This should be one of:

* ``"show"``
* ``"hide"``
* ``"replace"``
* ``"replaced"``

It then takes an action property, giving an action to run if the event
occurs.

::

    screen preferences():
        frame:
            has hbox

            text "Display"
            textbutton "Fullscreen" action Preferences("display", "fullscreen")
            textbutton "Window" action Preferences("display", "window")

        on "show" action Show("navigation")
        on "hide" action Hide("navigation")


.. _sl-use:

Use
---

The ``use`` statement allows a screen to include another. The use
statement takes the name of the screen to use. This can optionally be
followed by an argument list, in parenthesis.

If the used screen has no parentheses, it has read and write access
to the scope of the current screen, updated with any keyword arguments
passed via the ``use`` statement. Otherwise, its scope is initialized
to the result of assigning the arguments to those parameters. ::

    screen file_slot(slot):
        button:
            action FileAction(slot)

            has hbox

            add FileScreenshot(slot)
            vbox:
                text FileTime(slot, empty="Empty Slot.")
                text FileSaveName(slot)


     screen save():
         grid 2 5:
             for i in range(1, 11):
                  use file_slot(i)


The use statement may take clauses properties, ``id`` and ``as``. These properties must be placed
after the parameter list, if present, and must be on the first line of the statement, not in
th block.

The ``id`` clause is only useful when
two screens with the same tag use the same screen. In this case,
when one screen replaces the other, the state of the used screen
is transfered from old to new.

::

    transform t1():
        xpos 150
        linear 1.0 xpos 0

    screen common():
        text "Test" at t1

    screen s1():
        tag s
        use common id "common"
        text "s1" ypos 100

    screen s2():
        tag s
        use common id "common"
        text "s2" ypos 100

    label start:
        show screen s1
        pause
        show screen s2
        pause
        return

The ``as`` clause should be followed by a variable name. When the used screen finishes, the binding of the `main`
variable in the screen is assigned to the given variable. For example::

    screen child():
        add MyCreatorDefinedDisplayable() as main

    screen parent():
        use child as mycdd

        # Here, the MyCreatorDefinedDisplaybale instance is assigned to cdd.


Instead of the name of the screen, the keyword ``expression`` can be
given, followed by an expression giving the name of the screen to use.
If parameters are required, the ``pass`` keyword must be given to separate
them from the expression.

::

    screen ed(num):
        text "Ed"
        text "Captain"

    screen kelly(num):
        text "Kelly"
        text "First Officer"

    screen bortus(num):
        text "Bortus"
        text "Second Officer"

    screen crew():
        hbox:
            for i, member in enumerate(party):
                vbox:
                    use expression member.screen pass (i + 1)


Use and Transclude
^^^^^^^^^^^^^^^^^^

A use statement may also take a block containing screen language statements.
When a block is given, the screen that is used may contain the ``transclude``
statement. The ``transclude`` statement is replaced with the statements
contained within the use statement's block.

This makes it possible to define reusable layouts using screens. For example,
the screen::

    screen movable_frame(pos):
        drag:
            pos pos

            frame:
                background Frame("movable_frame.png", 10, 10)
                top_padding 20

                transclude

is meant to be a reusable component that wraps other components. Here's
an example of how it can be used::

    screen test:
        use movable_frame((0, 0)):
            text "You can drag me."

        use movable_frame((0, 100)):
            vbox:
                text "You can drag me too."
                textbutton "Got it!" action Return(True)

The use and transclude constructs form the basis of
:ref:`creator-defined screen language statements <creator-defined-sl>`.

.. _sl-python:

Python
------

The screen language also includes single-line and multiple-line Python
statements, which can execute Python. The Python runs in the scope
of the screen.

**Python must not cause side effects that are visible from
outside the screen.** Ren'Py will run a screen multiple times, as it
deems necessary. It runs a screen as part of the image prediction
process, before the screen is first shown. As a result, if a screen
has side effects, those side effects may occur at unpredictable times.

::

    screen python_screen:
        python:
            test_name = "Test %d" % test_number

        text test_name

        $ test_label = "test_%d" % test_label

        textbutton "Run Test" action Jump(test_label)


.. _sl-showif:

Showif Statement
================

The ``showif`` statement takes a condition. It shows its children when the
condition is true, and hides the children when the condition is false.
When showif's children have transforms, it will supply them with ATL
events to manage the show and hide process, so that Ren'Py can animate
the show and hide process.

The ``showif`` statement wraps its children in a displayable that manages
the show and hide process.

Multiple showif statements can be grouped together into a single
``showif``/``elif``/``else`` construct, similar to an if statement.
**Unlike the if statement, showif executes all of its blocks, including Python, even if the condition is false.**
This is because the showif statement needs to create the children that it is
hiding.

Showif delivers three events to its children:

``appear``
    Is delivered if the condition is true when the screen is first shown,
    to instantly show the child.
``show``
    Is delivered when the condition changes from false to true.
``hide``
    Is delivered when the condition changes from true to false.

For these purposes, the condition of an ``elif`` clause is always false if any
prior condition is true, while the condition of an else clause is only true
when all prior conditions are false.

For example::

    transform cd_transform:
        # This is run before appear, show, or hide.
        xalign 0.5 yalign 0.5 alpha 0.0

        on appear:
            alpha 1.0
        on show:
            zoom .75
            linear .25 zoom 1.0 alpha 1.0
        on hide:
            linear .25 zoom 1.25 alpha 0.0

    screen countdown():
        default n = 3

        vbox:
            textbutton "3" action SetScreenVariable("n", 3)
            textbutton "2" action SetScreenVariable("n", 2)
            textbutton "1" action SetScreenVariable("n", 1)
            textbutton "0" action SetScreenVariable("n", 0)

        showif n == 3:
            text "Three" size 100 at cd_transform
        elif n == 2:
            text "Two" size 100 at cd_transform
        elif n == 1:
            text "One" size 100 at cd_transform
        else:
            text "Liftoff!" size 100 at cd_transform

    label start:
        call screen countdown


Screen Statements
=================

In addition to the screen statement, there are three Ren'Py script
language statements that involve screens.

.. _show-screen-statement:

Show Screen
-----------

The ``show screen`` statement causes a screen to be shown. It takes an
screen name, a series of optional clauses, and optional Python arguments
which are passed to the screen. :func:`renpy.show_screen` and
:func:`renpy.call_screen` take additional specific keywords.

The ``show screen`` statement takes the following clauses, some of them similar
to the clauses of the :ref:`show-statement`:

``as``
    The ``as`` clause takes a name. If not specified, it defaults to the
    tag associated with the screen (see the :ref:`screen-statement`).
    If that's not specified, it defaults to the name of the screen.

``onlayer``
    The layer to show the screen on.

``zorder``
    The zorder to show the screen on. If not specified, defaults to
    the zorder associated with the screen. If that's not specified,
    it is 0 by default.

``expression``
    If the ``expression`` keyword is given, the expression following it will be evaluated
    as the screen name. To pass arguments to the screen with the expression keyword,
    separate the expression and arguments with the ``pass`` keyword::

        $ screen_name = "my_screen"
        show screen expression screen_name
        # Or if you need to pass some arguments
        show screen expression screen_name pass ("Foo", message="Bar")

``with``
    This is interpreted in the same way that the with clause of a ``show``
    statement is::

        show screen clock_screen with dissolve

``nopredict``
    The ``nopredict`` keyword doesn't take a value. It prevents screen prediction
    from occurring. During screen prediction, arguments to the screen are evaluated.
    Please ensure that evaluating the screen arguments does not cause unexpected
    side-effects to occur.

    .. warning::

        If evaluating the arguments to a screen causes side-effects to occur,
        your game may behave in unexpected ways.

Screens shown in this way are displayed until they are explicitly
hidden. This allows them to be used for overlay purposes.

::

    show screen overlay_screen
    show screen clock_screen(hour=11, minute=30)

    if rare_case:
        show rare_screen nopredict

.. _hide-screen-statement:

Hide Screen
-----------

The ``hide screen`` statement is used to hide a screen that is currently
being shown. It takes a screen tag. It first tries to find a screen with
the given tag on the given layer (see the ``onlayer`` clause). If none is
found, it looks for a screen with that name on the layer, regardless of
the tag the screen is shown as. If none is found, nothing happens::

    show screen A
    show screen B as A # B replaces A (which hides it)
    hide screen A # hides B, tagged as A

::

    show screen A as B
    show screen B as C

    hide screen B
    # hides the A screen, shown as B
    # the B screen, shown as C, stays shown

    hide screen B
    # hides the B screen

It also takes the ``onlayer`` clause, which defaults to the ``screens``
layer.

The with clause is interpreted the same way the ``with`` clause of a
:ref:`show-statement` is.

Similar to the ``show screen`` statement, ``hide screen`` also takes the
``expression`` keyword, allowing to use an arbitrary expression as the screen name.

::

    hide screen rare_screen
    hide screen clock_screen with dissolve
    hide screen overlay_screen
    $ screen_name = "some_screen"
    hide screen expression screen_name

.. _call-screen-statement:

Call Screen
-----------

The ``call screen`` statement shows a screen, and then hides it again at
the end of the current interaction. If the screen returns a value,
then the value is placed in the global ``_return`` variable.

This can be used to display an imagemap. The imagemap can place a
value into the ``_return`` variable using the :func:`Return` action,
or can jump to a label using the :func:`Jump` action.

The call screen statement takes various optional clauses, most of them similar to
those of the :ref:`show-screen-statement`:

``as``
    The ``as`` clause takes a name. If not specified, it defaults to the
    tag associated with the screen (see the :ref:`screen-statement`).
    If that's not specified, it defaults to the name of the screen.

``onlayer``
    The layer to show the screen on.

``zorder``
    The zorder to show the screen on. If not specified, defaults to
    the zorder associated with the screen. If that's not specified,
    it is 0 by default.

``nopredict``
    This keyword prevents screen prediction from occurring. During screen prediction,
    arguments to the screen are evaluated. Please ensure that evaluating
    the screen arguments does not cause unexpected side-effects to occur.

    .. warning::

        If evaluating the arguments to a screen causes side-effects to occur,
        your game may behave in unexpected ways.

``expression``
    Similar to the ``show screen`` statement, ``call screen`` also takes the
    ``expression`` keyword, allowing to use an arbitrary expression as the screen
    name. This also comes with the ``pass`` keyword, allowing arguments to be
    passed to the screen.

``with``
    In a call screen statement, the ``with`` clause causes a transition
    to occur when the screen is shown.

    This does **not** cause a ``with None`` occur before the screen is shown, so all show and hide statements before
    the screen will run. If you need a ``with None``, add one.

Since calling a screen is an interaction, and interactions trigger
an implicit ``with None``, using a ``with`` statement after the
``call screen`` instruction won't make the screen disappear using the
transition, as the screen will already will be gone. To disable the
implicit ``with None`` transition, pass the ``_with_none=False``
special keyword argument to the screen, as in the example below.

Other ways of triggering transitions also work, such as the
``[ With(dissolve), Return() ]`` action list.

::

    call screen my_imagemap

    call screen my_screen(side_effect_function()) nopredict

    # Shows the screen with dissolve
    call screen my_other_screen with dissolve
    # The screens instantly hides with None, then the pixellate transition executes
    with pixellate

    # Shows the screen with dissolve and hides it with pixellate.
    call screen my_other_screen(_with_none=False) with dissolve
    with pixellate

    $ screen_name = "my_screen"
    call screen expression screen_name pass (foo="bar")

.. _screen-variants:

Screen Variants
===============

Ren'Py runs both on traditional mouse-oriented devices such as Windows,
Mac, and Linux PCs, and newer touch-oriented devices such as Android-based
smartphones and tablets. Screen variants allow a game to supply
multiple versions of a screen, and use the version that best matches
the hardware it is running on.

Ren'Py chooses a screen variant to use by searching variants in the
order they are listed in :var:`config.variants`. The first variant
that exists is used.

If the RENPY_VARIANT environment variable is present, config.variants
is initialized by splitting the value of the variable on whitespace,
and then appending ``None``. Setting RENPY_VARIANT to a value such as
``"medium tablet touch"`` or ``"small phone touch"`` allows screens intended for
Android devices to be tested on a PC.

If the environment variable is not present, a list of variants is
built up automatically, by going through the following list in order
and choosing the entries that apply to the current platform.

``"steam_deck"``
    True if running on a Steam Deck or equivalent hardware.

``"steam_big_picture"``
    True if running in Steam Big Picture mode.

``"large"``
    A screen large enough that relatively small text can be
    comfortably read, and buttons can be easily clicked. This
    is used for computer screens.

``"medium"``
    A screen where smallish text can be read, but buttons may
    need to grow in size so they can be comfortably pressed.
    This is used for tablets.

``"small"``
    A screen where text must be expanded in order to be read. This
    is used for phones and televisions. (A television might be
    physically large, but it's often far away, making it hard
    to read.)

``"tablet"``
    Defined on touchscreen based devices where the screen has a
    diagonal size of 6 inches or more. (In general, ``"medium"`` should
    be used instead of ``"tablet"``.)

``"phone"``
    Defined on touchscreen-based devices where the diagonal size of
    the screen is less than 6 inches. On such a small device, it's
    important to make buttons large enough a user can easily choose
    them. (In general, ``"small"`` should be used instead of ``"phone"``.)

``"touch"``
    Defined on touchscreen-based devices.

``"tv"``
    Defined on television-based devices.

``"firetv"``
    Defined on the Amazon Fire TV console. (``"tv"`` and ``"small"`` are also defined.)

``"chromeos"``
    Defined when running as an Android app on a Chromebook.

``"android"``
    Defined on all Android devices.

``"ios"``
    Defined on iOS devices, like the iPad (where ``"tablet"`` and ``"medium"``
    are also defined) and the iPhone (where ``"phone"`` and ``"small"`` are
    also defined).

``"mobile"``
    Defined on mobile platforms, such as Android, iOS and mobile web browsers.

``"pc"``
    Defined on Windows, Mac OS X, and Linux. A PC is expected to have
    a mouse and keyboard present, to allow buttons to be hovered, and
    to allow precise pointing.

``"web"``
    Defined when running inside a web browser.

``None``
    Always defined.

An example of defining a screen variant is:

::

   # A variant hello_world screen, used on small touch-based
   # devices.
   screen hello_world():
        tag example
        zorder 1
        modal False
        variant "small"

        text "Hello, World." size 30

See also
========

:doc:`screen_actions` : a comprehensive list of actions and other tools
to be used with screens.

:doc:`screen_optimization` : some useful ways of making screens as
efficient as possible.

:doc:`screen_python` : go from using Ren'Py's predefined tools, to
extending Ren'Py.
