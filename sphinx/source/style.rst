.. _styles:

======
Styles
======

Styles allow the look of displayables to be customized. This is done by
changing the value of style properties for displayables. For example,
changing the :propref:`background` property allows the background of a window
or button to be customized.

Style properties consist of two parts, a prefix that
specifies when the property is used, and the property itself. For example, a
button's ``hover_background`` property is used when a button is focused,
while its ``idle_background`` property is used when the button is unfocused.
(Setting the ``background`` property sets the ``idle_background`` and
``hover_background``, among others.)

While Ren'Py has over 100 style properties, only a few properties are
used in this section. Along with ``background``, we use ``color``, ``font``,
``outlines`` and ``size`` as style properties. For a full list of style
properties, please read the :ref:`style properties <style-properties>`
documentation.


Using Styles and Style Inheritance
==================================

Each displayable has a style built-into it. When the displayable is created,
either directly or using the screen system, style properties can be supplied
to it, and these styles are used to update the look of the displayable. In
the following example::

    image big hello world = Text("Hello, World", size=40)

the :propref:`size` property is supplied to a Text displayable, allowing us to
change its text size. This will customize the look of the text displayable by
displaying the text 40 pixels high.

Similarly, when using Screen Language, each user interface statement takes
relevant style properties::

    screen big_hello_world:
        text "Hello, World" size 40

Ren'Py supports style inheritance, with each style having a single
parent. If a style property is not defined in a style, the value of the
property is inherited from the closest parent, grandparent, or other
ancestor.

Each displayable takes a property named ``style``, which gives the parent
of the displayable's style::

    image big hello world = Text("Hello World", style="big")

    screen hello_world:
        text "Hello, World" style "big"

When no ``style`` property is given, a parent is chosen based on the kind of
displayable be that has been supplied. The parent chosen can be influenced
by the :ref:`style_prefix <style-prefix>` property of user interface statements
in the screen language.

When a style is defined without a parent being specified, a default
parent is chosen for the style. If the style contains an underscore (_)
in its name, the parent is named by removing everything up to and
including the first underscore. For example, a style named ``my_button``
will inherit from ``button``. This inheritance can be changed using the
style statement or by calling a method on a style object.  When a style that
does not exist is used, and the style has an underscore in its name, Ren'Py will create
it using the default parent.

Style names beginning with an underscore are reserved for Ren'Py use.

As Ren'Py builds styles on startup, named styles should not be changed
outside of a style statement or init block.


Style Inspector
===============

When :var:`config.developer` is true, the style inspector can be used to
see which styles are being used by a displayable.

To activate the style inspector, place the mouse over a displayable, and
press shift+I. Ren'Py will display a list of displayables that include
the mouse position, in the order they are drawn to the screen. (That is,
the last displayable is the one on top of the others.)

Click the name of a style to display the styles the displayable inherits
from, and the properties each style contributes the to the final displayable.


Defining Styles: Style Statement
================================

The preferred way to define styles is through the style statement::

    style my_text is text:
        size 40
        font "gentium.ttf"

If a style does not exist, the style statement creates it. Otherwise,
the existing style is modified by the style statement.

A style statement begins with the keyword ``style`` and the name of the
style to define. This is followed on the first line by zero or more
clauses, and an optional colon.

If the colon is present, a block must follow. Each line of the block should
contain one ore more clauses. Otherwise, the statement is complete.

The style statement accepts the following clauses:

`style-property` `simple-expression`
    Assigns the value of the simple expression to the given style
    property.

``is`` `parent`
    Sets the parent of this style. The parent must be a word giving the
    name of a style.

``clear``
    Removes all properties of this style that were assigned before
    this style statement was run. This does not prevent the style
    from inheriting property values from its parents.

``take`` `style-name`
    Removes all properties of this style that were assigned before
    this style statement was run, and replaces them with the properties
    of the named style. This does not change the parent of this style.

``variant`` `simple-expression`
    Evaluates the simple expression, to yield a string or list of strings,
    which are interpreted as :ref:`screen variants <screen-variants>`. If at
    least one of the variants given is active, the style statement is run,
    otherwise it is ignored.

``properties`` `simple-expression`
    Evaluates the simple expression to get a dictionary. The dictionary is
    expected to map style properties to values, and the values are assigned
    as if they were provided to the style statement.

Examples of style statements are::

    # Creates a new style, inheriting from default.
    style big_red:
        size 40

    # Updates the style.
    style big_red color "#f00"

    # Takes the properties of label_text from big_red, but only if we're
    # on a touch system.

    style label_text:
        variant "touch"
        take big_red

Style statements are always run at init-time. If a style statement is not
in an init block, it is automatically placed init an init 0 block.


Defining Styles: Python
=======================

Named styles exists as fields on the global ``style`` object. To create a new
style, create an instance of the Style class, and assign it to a field on the
``style`` object.::

    init python:
         style.big_red = Style(style.default)

Style properties can be set by assigning to field-like properties of the
Styles. ::

    init python:
         style.big_red.color = "#f00"
         style.big_red.size = 42

.. class:: Style(parent)

    Creates a new style object. Style properties can be assigned to
    the fields of this object.

    `parent`
        The styles parent. This can be another style object, or a
        string.

    .. method:: clear()

        This removes all style properties from this object. Values will be
        inherited from this object's parent.

    .. method:: set_parent(parent)

        Sets the parent of this style object to `parent`.

    .. method:: take(other)

        This takes all style properties from `other`. `other` must be a
        style object.


..

    Indexed Styles

    Indexed styles are lightweight styles that can be used to customize the look
    of a displayable based on the data supplied to that displayable. An index
    style is created by indexing a style object with a string or integer. If an
    indexed style does not exist, indexing creates it.::

        init python:
            style.button['Foo'].background = "#f00"
            style.button['Bar'].background = "#00f"

    An index style is used by supplying the indexed style to a displayable.::

        screen indexed_style_test:
            vbox:
                textbutton "Foo" style style.button["Foo"]
                textbutton "Bar" style style.button["Bar"]


.. _style-preferences:

Style Preferences
-----------------

.. note::

    :ref:`gui-preferences` may often provide a better way of accomplishing
    the same thing, as a gui preference can change a variable used in multiple
    styles.

It's often desirable to allow the user to customize aspects of the user
interface that are best expressed as styles. For example, a creator may want
to give players of his game the ability to adjust the look, color, and size
of the text. Style preferences allow for this customization.

A style preference is a preference that controls one or more style properties.
A style preference has a name and one or more alternatives. At any given
time, one of the alternatives is the selected alternative for the style
preference. The selected alternative is saved in the persistent data, and
defaults to the first alternative registered for a style property.

An alternative has one or more associations of style, property, and value
associated with it, and represents a promise that when the alternative
becomes the selected alternative for the style preference, the property on
the style will be assigned the given value. This occurs when Ren'Py first
initializes, and then whenever a new alternative is selected.

One should ensure that every alternative for a given style preference updates
the same set of styles and properties. Otherwise, some styles may not be
assigned values, and the result will not be deterministic.

The style preference functions are:

.. include:: inc/style_preferences

Here's an example of registering a style property that allows the user to
choose between large, simple text and smaller outlined text.

::

    init python:
        renpy.register_style_preference("text", "decorated", style.say_dialogue, "outlines", [ (1, "#000", 0, 0) ])
        renpy.register_style_preference("text", "decorated", style.say_dialogue, "size", 22)

        renpy.register_style_preference("text", "large", style.say_dialogue, "outlines", [ ])
        renpy.register_style_preference("text", "large", style.say_dialogue, "size", 24)

The following will allow the user to select these alternatives using
buttons::

    textbutton "Decorated" action StylePreference("text", "decorated")
    textbutton "Large" action StylePreference("text", "large")

Other Style Functions
---------------------

.. function:: style.rebuild()

   This causes named styles to be rebuilt, allowing styles to be
   changed after the init phase has finished.

   .. warning::

      Named styles are not saved as part of the per-game data. This
      means that changes to them will not be persisted through a save
      and load cycle.
