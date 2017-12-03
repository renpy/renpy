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
interaction is restarted.

**Screens must not cause side effects that are visible from
outside the screen.** Ren'Py will run a screen multiple times, as
it deems necessary. It runs a screen as part of the image
prediction process, before the screen is first shown. As a result, if
running a screen has side effects, those side effects may occur at
unpredictable times.

A screen has a scope associated with it, giving values to some
variables. When a variable is accessed by a screen, it's first looked
up in the scope, and then looked up as a global variable.

Screen Language
===============

The screen language is a mostly-declarative way of displaying
screens. It consists of a statement that declares a new screen,
statements that add displayables to that screen, and control
statements.

Here's an example of a screen.::

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
that box is 10 pixels. It contains two text fields, one of the name of
the speaker, and the other with the speaker's id.

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

If a statement ends with a colon (:), then it takes a block. Each line
in a block may be one of two things:

* A property list.
* A screen language statement.


Screen Statement
----------------

The `screen` statement is a Ren'Py script language statement that is
used to declare a new screen. It is parsed using the screen language
common syntax.

It takes one parameter, the name of the screen. This is a name, not an
expression. It takes the following properties:

`modal`
    If True, the screen is modal. A modal screen prevents the user
    from interacting with displayables below it, except
    for the default keymap.

`tag`
    Parsed as a name, not an expression. This specifies a tag
    associated with this screen. Showing a screen replaces other
    screens with the same tag. This can be used to ensure that only
    one screen of a menu is shown at a time, in the same context.

`zorder`
    This controls how close to the user a screen is displayed. The
    larger the number, the closer the screen is displayed to the
    user. It defaults to 0.

`variant`
    If present, this should be a string or list of strings giving the
    variant of screen to be defined. See :ref:`screen-variants`.

`style_prefix`
    A string that's used to provide a prefix for the style for the
    children of this screen, as :ref:`described below <style-prefix>`.

::

   screen hello_world():
        tag example
        zorder 1
        modal False

        text "Hello, World."

A screen can take a parameter list::

   screen center_text(s, size=42):
        text s size size


User Interface Statements
=========================

The user interface statements create displayables and add them either
to the screen, or to an enclosing displayable. They allow the user to
display information, allow the user to interact with the game, or
allow the game to react to various events.

.. _common-properties:

All user interface statements take the following common properties:

`at`
    A transform, or list of transforms, that are used to wrap this
    displayable. The show, hide, replace, and replaced external events
    are delivered to a transform if and only if it is added directly
    to the screen.

    For example, if a vbox is wrapped in a transform, and added directly
    to the screen, then events are delivered to that transform. But if
    a transform wraps a textbutton that is added to the vbox, this
    second transform is not given events.

`default`
    If given and true, the displayable is focused by default. Only one
    displayable should have this.

`id`
    An identifier for the user-interface statement. When a screen is
    shown, property values can be supplied for the displayables with a
    given identifier. Some screens will require that a displayable
    with a given identifier is created.

    By default, the id is automatically-generated.

`style`
    The name of the style applied to this displayable. This may be a
    string name, or a style object. The style gives default
    values for style properties.

`style_prefix`
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

`style_group`
    An alias for `style_prefix`, used in older version of Ren'Py.

`style_suffix`
    Specifies the suffix that is combined with the `style_prefix` to
    generate a style name. If this is ``"small_button"`` and the
    style prefix is ``"pref"``, the style ``"pref_small_button"`` is
    used.

    If no style prefix is in use, this is used directly as the name of
    the style. A style suffix applies to a single displayable only, not
    a displayable and all children.

`focus`
    Takes a string or integer, and gives a name to the displayable
    for focus purposes. Ren'Py looks for structural similarity between
    focus names when deciding with displayable to give focus to at the
    start of an interaction. If a box is given a focus name, and the
    third button in that box is focused at the end of an interaction,
    the third button of a box with the same will be highlighted at
    the start of the next interaction.

`tooltip`
    Assigns a tooltip to this displayable. When the displayable gains
    focus, the value of this property will be made available from the
    :func:`GetTooltip` function. See the :ref:`tooltips` section for
    more details.

Many user interface statements take classes of style properties, or
transform properties. These properties can have a style prefix
associated with them, that determines when they apply. For example, if
text is given the hover_size property, it sets the text size when the
text is hovered.


.. _sl-add:

Add
---

Adds an image or other displayable to the screen. This optionally
takes :ref:`transform properties <transform-properties>`. If at least
one transform property is given, a Transform is created to wrap the
image, and the properties are given to the transform.

If the displayable is None, nothing is added to the screen.

This does not take any children.

::

    screen add_test():
        add "logo.png" xalign 1.0 yalign 0.0


.. _sl-bar:

Bar
---

Creates a horizontally-oriented bar that can be used to view or adjust
data. It takes the following properties:

`value`
    The current value of the bar. This can be either a :ref:`bar value <input-values>`
    object, or a number.

`range`
    The maximum value of the bar. This is required if `value` is a
    number.

`adjustment`
    A :func:`ui.adjustment` object that this bar adjusts.

`changed`
    If given, this should be a python function. The function is called
    with the value of the adjustment when the adjustment is changed.

`hovered`
    An action to run when the bar gains focus.

`unhovered`
    An action to run when the bar loses focus.

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

            bar value Preference("sound volume")
            bar value Preference("music volume")
            bar value Preference("voice volume")

.. _sl-button:

Button
------

Creates an area of the screen that can be activated to run an
action. A button takes no parameters, and the following properties.

`action`
    The action to run when the button is activated. A button is activated
    when it is clicked, or when the player selects it and hits enter on the
    keyboard. This also controls if the button is sensitive if `sensitive`
    is not provided, and if the button is selected if `selected` is not
    provided.

`alternate`
    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

`selected`
    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine selectedness.

`sensitive`
    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine sensitivity.

`keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

`alternate_keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

It takes one children. If zero, two, or more children are supplied,
they are implicitly added to a fixed, which is added to the button.


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
grid, and the second is the number of rows in the grid. It takes the
following property:

`transpose`
    If False (the default), rows are filled before columns. If True,
    then columns are filled before rows.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`grid-style-properties`

This must be given columns * rows children. Giving it a different
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

`auto`
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


`insensitive`
    The image used when the button is insensitive.

`idle`
    The image used when the button is not focused.

`hover`
    The image used when the button is focused.

`selected_idle`
    The image used when the button is selected and idle.

`selected_hover`
    The image used when the button is selected and hovered.

`action`
    The action to run when the button is activated. This also controls if
    the button is sensitive if `sensitive` is not provided, and if the button
    is selected if `selected` is not provided.

`alternate`
    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

`selected`
    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine selectedness.

`sensitive`
    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine sensitivity.

`keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

`alternate_keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
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

The input statement takes no parameters, and the following properties:

`value`
    An :ref:`input value <input-values>` object that this input uses.
    InputValue objects determine where the default value is taken from,
    what happens when the text is changed, what happens when enter is
    pressed, and if the text is editable by default.

    This should not be given at the same time as `default` and `changed`.

`default`
    The default text in this input.

`length`
    The maximum length of the text in this input.

`pixel_width`
    The maximum pixel width of the input. If typing a character would
    cause the input to exceed this width, the keypress is ignored.

`allow`
    A string containing characters that are allowed to be typed into
    this input. (By default, allow all characters.)

`exclude`
    A string containing characters that are disallowed from being
    typed into this input. (By default, "{}".)

`prefix`
    An immutable string to prepend to what the user has typed.

`suffix`
    An immutable string to append to what the user has typed.

`changed`
    A python function that is called with what the user has typed,
    when the string changes.


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

This creates a keybinding that runs an action when a key is
pressed. Key is used in a loose sense here, as it also allows joystick
and mouse events.

Key takes one positional parameter, a string giving the key to
bind. See the :ref:`keymap` section for a description of available
keysyms. It takes one property:

`action`
    This gives an action that is run when the key is pressed. This
    property is mandatory.

It takes no children.

::

    screen keymap_screen():
        key "game_menu" action ShowMenu('save')
        key "p" action ShowMenu('preferences')
        key "s" action Screenshot()


.. _sl-label:

Label
-----

Creates a window in the label style, and then places text inside that
window. Together, this combination is used to label things inside a
frame.

It takes one positional argument, the text of the label. It takes
the property:

`text_style`
    The name of the style to use for the button text. If not supplied,
    and the `style` property is a string, then ``"_text"`` is appended
    to that string to give the default text style.

`text_`-
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


.. _sl-null:

Null
----

The null statement inserts an empty area on the screen. This can be
used to space things out. The null statement takes no parameters, and
the following properties:

`width`
    The width of the empty area, in pixels.

`height`
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

.. _mousearea:
.. _sl-mousearea:

Mousearea
---------

A mouse area is an area of the screen that can react to the mouse
entering or leaving it. Unlike a button, a mouse area does not take
focus, so it's possible to have a mouse area with buttons inside it.
The mousearea statement takes no parameters, and the following properties:

`hovered`
    An action to run when the mouse enters the mouse area.

`unhovered`
    An action to run when the mouse leaves the mouse area.

`focus_mask`
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

`spacing`
    The spacing between the rows and columns of the grid.


A side takes the following property groups:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

When being rendered, this first sizes the corners, then the sides,
then the center. The corners and sides are rendered with an available
area of 0, so it may be necessary to supply them a minimum size (using
:propref:`xminimum` or :propref:`yminimum`) to ensure they render at
all.

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

`action`
    The action to run when the button is activated. This also controls if
    the button is sensitive if `sensitive` is not provided, and if the button
    is selected if `selected` is not provided.

`alternate`
    An action that is run if the button is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the button
    on a mouse-based platform, or when the player long presses the button
    on a touch-based platform.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

`selected`
    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine selectedness.

`sensitive`
    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine sensitivity.

`keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

`alternate_keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the alternate action of this button.

`text_style`
    The name of the style to use for the button text. If not supplied,
    and the `style` property is a string, then ``"_text"`` is appended
    to that string to give the default text style.

`text_`-
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

`action`
    This gives an action that is run when the timer expires. This
    property is mandatory.

`repeat`
    If True, the timer repeats after it times out.

It takes no children.

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
following property groups :

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

`child_size`
    The size that is offered to the child for rendering. An (`xsize`,
    `ysize`) tuple. This can usually be omitted, when the child can
    compute it's own size. If either component is None, the child's
    size is used.
`mousewheel`
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
`draggable`
    If True, dragging the mouse will scroll the viewport.
`edgescroll`
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

`xadjustment`
    The :func:`ui.adjustment` used for the x-axis of the
    viewport. When omitted, a new adjustment is created.
`yadjustment`
    The :func:`ui.adjustment` used for the y-axis of the
    viewport. When omitted, a new adjustment is created.
`xinitial`
    The initial horizontal offset of the viewport. This may be an integer
    giving the number of pixels, or a float giving a fraction of the
    possible offset.
`yinitial`
    The initial vertical offset of the viewport. This may be an integer
    giving the number of pixels, or a float giving a fraction of the
    possible offset.
`scrollbars`
    If not None, scrollbars are added along with this viewport.
    This works by creating a side layout, and placing the created
    viewport in the center of the side. If `scrollbars` is "horizontal",
    a horizontal scrollbar is placed beneath the viewport. If `scrollbars`
    is "vertical", a vertical scrollbar is placed to the right of the
    viewport. If `scrollbars` is "both", both horizontal and vertical
    scrollbars are created.

    If `scrollbars` is not None, the viewport takes properties prefixed
    with "side_". These are passed to the created side layout.


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
size, spacing, and number of children. If there are not enough children to
fill all cells, any empty cells will not be rendered.

Vpgrids take the the following properties:

`cols`
    The number of columns in the grid.

`rows`
    The number of rows in the grid.

`transpose`
    If true, columns are filled before rows. The default of this depends
    on the `cols` and `rows` properties. If `cols` is given, columns
    are filled before rows, otherwise rows are filled before columns.

In addition, a vpgrid takes all properties a :ref:`viewport <sl-viewport>` can,
and the following groups of style properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`00
* :ref:`grid-style-properties`

::

    screen vpgrid_test():

        vpgrid:

            cols 2
            spacing 5
            draggable True
            mousewheel True

            scrollbars "vertical"

            # Since we have scrollbars, we have to position the side, rather
            # than the vpgrid proper.
            side_xalign 0.5

            for i in range(1, 100):

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
visually is to create an imagemap. When creating an imagemap, the
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

`auto`
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

`ground`
    The image used for portions of the imagemap that are not part of a
    hotspot or hotbar.

`insensitive`
    The image used when a hotspot or hotbar is insensitive.

`idle`
    The image used when a hotspot is not selected and not focused, and
    for the empty portion of unfocused hotbars.

`hover`
    The image used when a hotspot is not selected and focused, and
    for the empty portion of focused hotbars.

`selected_idle`
    The image used when a hotspot is selected and not focused, and
    for the full portion of unfocused hotbars.

`selected_hover`
    The image used when a hotspot is selected and focused, and
    for the full portion of focused hotbars.

`alpha`
    If true, the default, a hotspot only gains focus when the mouse is
    in an area of the hover image that is opaque. If false, the hotspot
    gains focus whenever the mouse is within its rectangular boundary.

`cache`
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

`action`
    The action to run when the button is activated. This also controls
    if the button is sensitive, and if the button is selected.

`alternate`
    An action that is run if the hotspot is activated in an alternate manner.
    Alternate activation occurs when the player right-clicks on the hotspot
    on a mouse-based platform, or when the player long presses the hotspot
    on a touch-based platform.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

`selected`
    An expression that determines whether the button is selected or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine selectedness.

`sensitive`
    An expression that determines whether the button is sensitive or not.
    This expression is evaluated at least once per interaction.
    If not provided, the action will be used to determine sensitivity.

`keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
    when pressed, invokes the action of this button.

`alternate_keysym`
    A string giving a :ref:`keysym <keymap>` describing a keyboard key that,
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

`value`
    The current value of the bar. This can be either a :ref:`bar value <input-values>`
    object, or a number.

`range`
    The maximum value of the bar. This is required if `value` is a
    number.

`adjustment`
    A :func:`ui.adjustment` object that this bar adjusts.

One of `value` or `adjustment` must be given. In addition, this
function takes:

* :ref:`Common Properties <common-properties>`
* :ref:`bar-style-properties`

This does not take children.

Hotbars should be given the ``alt`` style property to allow Ren'Py's
self-voicing feature to work.


Advanced Displayables
=====================

In addition to the commonly-used statements, the screen language has
statements that correspond to advanced displayables. The mapping from
displayable to statement is simple. Positional parameters of the
displayables become positional parameters of the statement. Keyword
arguments and the relevant style properties become screen language
properties.

The advanced displayable statements are:

``drag``
    Creates a :class:`Drag`. A drag can be given an optional child,
    or the :propref:`child` style property can be used to supply the child,
    and its focused variants. Drags also take the :propref:`focus_mask`
    style property.

``draggroup``
    Creates a :class:`DragGroup`. A drag group may have zero or more
    drags as its children.


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

The default statement sets the default value of a variable when the
screen is first one. :func:`SetScreenVariable`

The default statement sets the default value of a variable, if it is not
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

The for statement is similar to the Python for statement, except that
it does not support the else clause. It supports assignment to
(optionally nested) tuple patterns, as well as variables.

::

    $ numerals = [ 'I', 'II', 'III', 'IV', 'V' ]

    screen five_buttons():
        vbox:
            for i, numeral in enumerate(numerals):
                textbutton numeral action Return(i + 1)


.. _sl-if:

If
--

The screen language if statement is the same as the Python/Ren'Py if
statement. It supports the if, elif, and else clauses.

::

    screen skipping_indicator():
        if config.skipping:
             text "Skipping."
        else:
             text "Not Skipping."

.. _sl-on:

On
--

The on statement allows the screen to execute an action when an event
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

The use statement allows a screen to include another. The use
statement takes the name of the screen to use. This can optionally be
followed by an argument list, in parenthesis.

If the used screen include parameters, its scope is initialized to the
result of assigning the arguments to those parameters. Otherwise, it
is passed the scope of the current screen, updated with any keyword
arguments passed to the screen.

::

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


The use statement may take one property, ``id``, which must be placed
after the parameter list if present. This screen is only useful when
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

Use and Transclude
^^^^^^^^^^^^^^^^^^

A use statement may also take a block containing screen language statements.
When a block is given, the screen that is used may contain the ``transclude``
statement. The ``transclude`` statement is replaces with the statements
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

The screen language also includes single-line and multiple-line python
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

The showif statement takes a condition. It shows its children when the
condition is true, and hides the children when the condition is false.
When showif's children have transforms, it will supply them with ATL
events to manage the show and hide process, so that Ren'Py can animate
the show and hide process.

Multiple showif statements can be grouped together into a single
showif/elif/else construct, similiar to an if statement.
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

For these purposes, the condition of an elif clause is always false if any
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

Two of these statements take a keyword argument list. This is a python
argument list, in parenthesis, consisting of only keyword
arguments. Positional arguments, extra positional arguments (*), and
extra keyword arguments (**) are not allowed.

Show Screen
-----------

The show screen statement causes a screen to be shown. It takes an
screen name, and an optional argument list. If present, the arguments
are used to initialize the scope of the screen.

The show screen statement takes an optional nopredict keyword, that
prevents screen prediction from occurring. During screen prediction,
arguments to the screen are evaluated. Please ensure that evaluating
the screen arguments does not cause unexpected side-effects to occur.

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


Hide Screen
-----------

The hide screen statement is used to hide a screen that is currently
being shown. If the screen is not being shown, nothing happens.

::

    hide screen overlay_screen
    hide screen clock


Call Screen
-----------

The call screen statement shows a screen, and then hides it again at
the end of the current interaction. If the screen returns a value,
then the value is placed in `_return`.

This can be used to display an imagemap. The imagemap can place a
value into the `_return` variable using the :func:`Return` action,
or can jump to a label using the :func:`Jump` action.

The call screen statement takes an optional ``nopredict`` keyword, that
prevents screen prediction from occurring. During screen prediction,
arguments to the screen are evaluated. Please ensure that evaluating
the screen arguments does not cause unexpected side-effects to occur.

The call screen statement takes an optional ``with`` keyword, followed
by a transition. The transition takes place when the screen is first
displayed. A with statement after the transition runs after the screen
is hidden, provided control is not transferred.

.. warning::

    If evaluating the arguments to a screen causes side-effects to occur,
    your game may behave in unexpected ways.

::

    call screen my_imagemap

    call screen my_screen(side_effect_function()) nopredict

    # Shows the screen with dissolve and hides it with fade.
    call screen my_other_screen with dissolve
    with fade

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

``"ouya"``
   Defined on the OUYA console. (``"tv"`` and ``"small"`` are also defined.)

``"firetv"``
   Defined on the Amazon Fire TV console. (``"tv"`` and ``"small"`` are also defined.)

``"android"``
   Defined on all Android devices.

``"ios"``
   Defined on iOS devices, like the iPad (where ``"tablet"`` and ``"medium"``
   are also defined) and the iPhone (where ``"phone"`` and ``"small"`` are
   also defined).

``"mobile"``
   Defined on mobile platforms, such as Android and iOS.

``"pc"``
   Defined on Windows, Mac OS X, and Linux. A PC is expected to have
   a mouse and keyboard present, to allow buttons to be hovered, and
   to allow precise pointing.

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

