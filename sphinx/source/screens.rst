.. _screens:

===========================
Screens and Screen Language
===========================

The things that a user sees when looking at a Ren'Py game can be
broken divided into images and user interface. Images are displayed to
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

A screen has a scope associated with it, giving values to some
variables. When a variable is accessed by a screen, it's first looked
up in the scope, and then looked up as a global variable.

Screen Language
===============

The screen language is a mostly-declarative way of displaying
screens. It consists of a statement that declares a new screen,
statements that add displayables to that screen, and control
statements.

Here's an example of a screen. ::

    screen say:
        window id "window":
            vbox:
                spacing 10
             
                text who id "who"
                text what id "what"

The first line of this is a screen statement, a Ren'Py language
statement that's used to declare a screen. The name of the screen is
`say`, so this is the screen that's used to display dialogue.

The screen contains a window, which has been given the id of
"window". This window contains a vertical box, and the spacing inside
that box is 10 pixels. It contains two text fields, one of the name of
the speaker, and the other with the speaker's id.

Screen Language Syntax
-----------------------

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
    If present, this should be a string giving the variant of screen
    to be defined. See :ref:`screen-variants`. 
    
::

   screen hello_world:
        tag example
        zorder 1
        modal False
   
        text "Hello, World."


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

`style_group`
    Style_group is used to provide a prefix to the style of a displayable,
    for this displayable and all of its children (unless they have a
    more specific group set).

    For example, if a vbox has a group of ``"pref"``, then the vbox will
    have the style ``"pref_vbox"``, unless a more specific style is
    supplied to it. A button inside that vbox would default to the
    style ``"pref_button"``.

    Styles accessed in this way are automatically created, if they do
    not exist. This prevents an error from being signalled.
    
    Setting a group of ``None`` disables this behavior for a
    displayable and all of its children.

`focus`
    Takes a string or integer, and gives a name to the displayable
    for focus purposes. Ren'Py looks for structural similarity between
    focus names when deciding with displayable to give focus to at the
    start of an interaction. If a box is given a focus name, and the
    third button in that box is focused at the end of an interaction,
    the third button of a box with the same will be highlighted at
    the start of the next interaction.
    
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

This does not take any children.

::

    screen add_test:
        add "logo.png" xalign 1.0 yalign 0.0


.. _sl-bar:
        
Bar
---

Creates a horizontally-oriented bar that can be used to view or adjust
data. It takes the following properties:

`value`
    The current value of the bar. This can be either a BarValue object,
    or a number.

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

    screen volume_controls:
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
    The action to run when the button is activated. This also controls
    if the button is sensitive, and if the button is selected.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

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

    screen test_frame:
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

`spacing`
    The spacing between the rows and columns of the grid.
    
It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

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

   screen hbox_text:
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
    idle defaults to "button_idle.png".

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
    The action to run when the button is activated. This also controls
    if the button is sensitive, and if the button is selected.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

This takes no children.

::

    screen gui_game_menu:
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
interaction. This takes no parameters, and the following properties:

`default`
    The default text in this input.

`length`
    The maximum length of the text in this input.

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

    screen input_screen:
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
bind. See the `Keymap`_ section for a description of available
keysyms. It takes one property:

`action`
    This gives an action that is run when the key is pressed. This
    property is mandatory.

It takes no children.

::

    screen keymap_screen:
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
    
It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`

It does not take children.

::

    screen display_preference:
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

    screen text_box:
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
The mousearea statement takes not parameters, and the following properties:

`hovered`
    An action to run when the mouse enters the mouse area.

`unhovered`
    An action to run when the mouse leaves the mouse area.

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

    screen button_overlay:
        mousearea:
            area (0, 0, 1.0, 100)
            hovered Show("buttons", transition=dissolve)
            unhovered Hide("buttons", transition=dissolve)

    screen buttons:
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

A side taks the following properties:

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

    screen side_test:
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

    screen hello_world:
        text "Hello, World." size 40

.. _sl-textbutton:
        
Textbutton
----------

Creates a button containing a text label. The button takes a single
parameter, the text to include as part of the button. It takes the
following properties:

`action`
    The action to run when the button is activated. This also controls
    if the button is sensitive, and if the button is selected.

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

`text_style`
    The name of the style to use for the button text. If not supplied,
    and the `style` property is a string, then ``"_text"`` is appended
    to that string to give the default text style.
    
It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`
* :ref:`window-style-properties`
* :ref:`button-style-properties`

It does not take children.

::

    screen textbutton_screen:
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

    screen timer_test:
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

    screen volume_controls:
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

    screen vbox_test:
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
    If True, the mouse wheel can be used to scroll the viewport.
`draggable`
    If True, dragging the mouse will scroll the viewport.
`xadjustment`
    The :func:`ui.adjustment` used for the x-axis of the
    viewport. When omitted, a new adjustment is created.
`yadjustment`
    The :func:`ui.adjustment` used for the y-axis of the
    viewport. When omitted, a new adjustment is created.

In addition, it takes the following groups of style properties:

* :ref:`Common Properties <common-properties>`
* :ref:`position-style-properties`

It takes one child. If zero, two, or more children are supplied, then
a fixed is created to contain them.

To make a viewport scrollable, it's often best to assign an id to it,
and then use :func:`XScrollValue` and :func:`YScrollValue` with that
id.

::

    screen viewport_example:
        side "c b r":
             area (100, 100, 600, 400)
         
             viewport id "vp":
                 draggable True
                 
                 add "washington.jpg"

             bar value XScrollValue("vp")
             vbar value YScrollValue("vp")

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

    screen say:
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

    screen preferences:

        tag menu
        use navigation
    
        imagemap:
            auto "gui_set/gui_prefs_%s.png"
            
            hotspot (740, 232, 75, 73) clicked Preference("display", "fullscreen")
            hotspot (832, 232, 75, 73) clicked Preference("display", "window")
            hotspot (1074, 232, 75, 73) clicked Preference("transitions", "all")
            hotspot (1166, 232, 75, 73) clicked Preference("transitions", "none")

            hotbar (736, 415, 161, 20) value Preference("music volume")
            hotbar (1070, 415, 161, 20) value Preference("sound volume")
            hotbar (667, 535, 161, 20) value Preference("voice volume")
            hotbar (1001, 535, 161, 20) value Preference("text speed")

            
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
    idle defaults to "imagemap_idle.png".

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

`hovered`
    An action to run when the button gains focus.

`unhovered`
    An action to run when the button loses focus.

It also takes:

* :ref:`Common Properties <common-properties>`
* :ref:`button-style-properties`

A hotspot creates a fixed, allowing children to be added to it. The
fixed has an area that is the same size as the hotspot, meaning that
the children will be positioned relative to the hotpsot.


.. _sl-hotbar:

Hotbar
------

A hotbar is a bar that consists of a portion of the imagemap that
contains it. It takes a single parameter, a (x, y, width, height)
tuple giving the area of the imagemap that makes up the button. It
also takes the following properties:

`value`
    The current value of the bar. This can be either a Value object,
    or a number.

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
    and its focused variants.

``draggroup``
    Creates a :class:`DragGroup`. A drag group may have zero or more
    drags as its children.
    

.. _sl-has:
    
Has Statement
=============

The has statment allows you to specify a container to use, instead of
fixed, for statements that take only one child. The has statement
may only be used inside a statement that takes one child. The keyword
``has`` is followed (on the same line) by another statement, which
must be a statement that creates a container displayable, one that
takes more than one child.

The has statement changes the way in which the block that contains
it is parsed. Child displayables created in that block are added to
the container, rather than the parent displayable. Keyword arguments
to the parent displayable are not allowed after the has statement.

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

   screen volume_controls:
        frame:
            has vbox
        
            bar value Preference("sound volume")
            bar value Preference("music volume")
            bar value Preference("voice volume")


Control Statements
==================

The screen language includes control statements for conditional
execution, iteration, including other screens, executing actions when
events occur, and executing arbitrary python code.

.. _sl-default:

Default
-------

The default statement sets the default value of a variable, if it is not
passed as an argument to the screen, or inherited from a screen that calls
us using the use statement.

::

    screen message:
         default message = "No message defined."
         text message


.. _sl-for:
         
For
---

The for statement is similar to the Python for statment, except that
it does not support the else clause. It supports assignment to
(optionally nested) tuple patterns, as well as variables. 

::

    $ numerals = [ 'I', 'II', 'III', 'IV', 'V' ]

    screen five_buttons:
        vbox:
            for i, numeral in enumerate(numerals):
                textbutton numeral action Return(i + 1)


.. _sl-if:
                
If
--

The screen language if statement is the same as the Python/Ren'Py if
statement. It supports the if, elif, and else clauses.

::

    screen skipping_indicator:
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

    screen preferences:
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
followed by a keyword argument list, in parenthesis.

The scope of the included code includes the scope of the current
statement's code, updated by assinging the parameters their new
values.

::

    screen file_slot:
        button:
            action FileAction(slot)

            has hbox

            add FileScreenshot(slot)
            vbox:
                text FileTime(slot, empty="Empty Slot.")
                text FileSaveName(slot)
                    

     screen save:
         grid 2 5:
             for i in range(1, 11):
                  use file_slot(slot=i)

.. _sl-python:
                  
Python
------

The screen language also includes single-line and multiple-line python
statements, which can execute python code. This code runs in the scope
of the statement.

::

    screen python_screen:
        python:
            test_name = "Test %d" % test_number

        text test_name

        $ test_label = "test_%d" % test_label

        textbutton "Run Test" action Jump(test_label)
        
        
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
are used to intialize the scope of the screen.

Screens shown in this way are displayed until they are explicitly
hidden. This allows them to be used for overlay purposes.

::

    show screen overlay_screen
    show screen clock_screen(hour=11, minute=30)

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

::

   call screen my_imagemap


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
``"tablet touch"`` or ``"phone touch"`` allows screens intended for
Android devices to be tested on a PC.

If the environment variable is not present, a list of variants is
built up automatically, by going through the following list in order
and choosing the entries that apply to the current platform.

``"tablet"``
   Defined on touchscreen based devices where the screen has a
   diagonal size of 6 inches or more.

``"phone"``
   Defined on touchscren-based devices where the diagonal size of
   the screen is less than 6 inches. On such a small device, it's
   important to make buttons large enough a user can easily choose
   them.

``"touch"``
   Defined on touchscreen-based devices, such as those running the
   Android platform.

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
   screen hello_world:
        tag example
        zorder 1
        modal False
        variant "touch" 
        
        text "Hello, World." size 30
        
