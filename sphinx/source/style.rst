======
Styles
======

Styles allow the look of :doc:`displayables` to be customized, by changing the
value of style properties. For example, changing the :propref:`background`
property to change the background of a window or button.

:doc:`Style properties <style_properties>` can be prefixed by identifiers
specifying when the property is used. For example, a button's
``hover_background`` property is used when it is focused, while its
``idle_background`` property is used when it is not. (Setting the
``background`` property sets both the ``idle_background`` and
``hover_background``, among others.)

While Ren'Py has over 100 style properties, only a few of them are
used in this section.


Using Styles and Style Inheritance
==================================

Each displayable has a style built into it. When the displayable is created,
either directly or using the screen system, style properties can be supplied,
which are used to update the look of the displayable. In the following example::

    image big hello world = Text("Hello, World", size=40)

the :propref:`size` property is supplied to a Text displayable, allowing us to
change its text size. This will customize the look of the text displayable by
displaying the text 40 pixels high (though this also depends on the font).

Similarly, when using Screen Language, each user interface statement takes
relevant style properties::

    screen big_hello_world:
        text "Hello, World" size 40

Individual styles exist to gather properties so they can be applied to
displayables together. For example, these two texts will appear the same::

    image big one = Text("Hello, World", size=40, color="#f00")
    image big two = Text("Hello, World", style="big_red")

    style big_red:
        size 40
        color "#f00"

Each style has a set of properties, and one parent. When a given style is applied
to a given displayable, each style property (among those taken by the
displayable) will be looked for among the style's properties. If it's not found,
it is searched in the parent style, and then in the parent's parent, and so on.

Each displayable takes a property named ``style``, which applies the said style
to the displayable::

    image big hello world = Text("Hello World", style="big")

    screen hello_world:
        text "Hello, World" style "big"

When no ``style`` property is given, a parent is chosen based on the kind of
displayable that has been supplied. For example, buttons (including imagebuttons
and textbuttons) default to the "button" style, grids to the "grid" style, and
so on. The parent choice can be influenced by the
:ref:`style_prefix <style-prefix>` property of user interface statements
in the screen language.

When a style is defined without a parent being specified, a default
parent is chosen for the style. If the style contains an underscore (_)
in its name, the parent is named by removing everything up to and
including the first underscore. When a style that does not exist is used, and
the style has an underscore in its name, Ren'Py will create it using the default
parent. For example, a style named ``my_button`` will inherit from ``button``.
This inheritance can be changed using the style statement or using methods of
the :class:`Style` class. Otherwise, the style named "default" is used.

Style names beginning with an underscore are reserved for Ren'Py use.

As Ren'Py builds styles on startup, named styles should not be changed
after the :ref:`init-phase`.

During development, the :ref:`style-inspector` can be very useful to check what
styles and style properties are being used by a displayable.


Defining Styles: Style Statement
================================

The preferred way to define styles is through the style statement::

    style my_text is text:
        size 40
        font "gentium.ttf"

If a style does not exist, the style statement creates it. Otherwise,
the existing style is modified by the style statement.

.. note::

    Unlike other statements such as :ref:`screen <screen-statement>`,
    :ref:`transform <transform-statement>` or :ref:`image <image-statement>`,
    the style statement is not unique for a given name: several statements can
    refer to the same style and alter it successively, sometimes in a
    concurrent or contradictory way. In such cases, the init times at which the
    different style statements occur greatly matter over the final result.

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
    Sets or replaces the parent of this style. The parent must be a word giving
    the name of a style.

``clear``
    Removes all properties of this style that were assigned before
    this style statement was run. This does not prevent the style
    from inheriting property values from its parents, and does not change its
    parent. To clear the parent of a style, use ``is default`` instead.

``take`` `style-name`
    Clears all properties of this style that were assigned before
    this style statement was run, and replaces them with the properties
    of the named style. This does not change the parent of this style.

``variant`` `simple-expression`
    Evaluates the simple expression, to yield a string or list of strings,
    which are interpreted as :ref:`screen variants <screen-variants>`. If at
    least one of the variants given is active, the style statement is run,
    otherwise the rest of the block is ignored.

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

    # Style a has all the properties of style c, except that when not present
    # in c, the properties are taken from b or b's parents.
    style a is b:
        take c

Style statements are always run at :ref:`init time <init-phase>`.


Defining Styles: Python
=======================

Named styles exists as fields on the global ``style`` object. To create a new
style, create an instance of the :class:`Style` class, and assign it to a field
on the ``style`` object::

    init python:
        style.big_red = Style(style.default)

Style properties can be set by assigning to properties-like fields of the Style
objects. ::

    init python:
        style.big_red.color = "#f00"
        style.big_red.size = 42

However, the value of a style property cannot be accessed this way, it can only
be written.

.. class:: Style(parent)

    `parent`
        The styles parent. This can be another Style object, or a string.

    .. method:: clear()

        This removes all style properties from this object. Values will be
        inherited from this object's parent.

        The equivalent of the ``clear`` clause in a style statement.

    .. method:: set_parent(parent)

        Sets the parent of this style object to `parent`, which can be another
        Style object or a string.

        The equivalent of the ``is`` clause in a style statement.

    .. method:: take(other)

        This takes all style properties from `other`, which can be another
        Style object or a string.

        The equivalent of the ``take`` clause in a style statement.


.. _indexed-styles:

Indexed Styles
--------------

Indexed styles are lightweight styles that can be used to customize the look
of a displayable based on the data supplied to that displayable. An index
style is created by indexing an existing Style object with a string or integer.
If the indexed style does not exist, indexing creates it as a child of the
original Style object. ::

    init python:
        style.button["Foo"].background = "#f00"
        style.button["Bar"].background = "#00f"

::

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
to give players the ability to adjust the look, color and size
of the text. Style preferences allow for this customization.

A style preference is a preference controlling one or more style properties.
A style preference has a name and one or more alternatives. At any given time,
one of the available alternatives is selected, and saved in the persistent data.
It defaults to the first registered alternative.

An alternative contains one or more associations of style, property, and value
for that property. It represents a promise that when the alternative gets
selected, that property on that style will be assigned that value. This occurs
when Ren'Py first initializes, and then whenever a new alternative is selected.

One should ensure that every alternative for a given style preference updates
the same set of styles and properties. Otherwise, the result will not be
deterministic as going from one alternative to another and going back to the
first one will leave some properties set as they are in the second alternative.

Here's an example of registering a style property that allows the user to
choose between large, simple text, and smaller outlined text.

::

    init python:
        # The "decorated" alternative of the "text" preference will set the size to 22 on the "say_dialogue" style.
        renpy.register_style_preference("text", "decorated", style.say_dialogue, "size", 22)
        renpy.register_style_preference("text", "decorated", style.say_dialogue, "outlines", [ (1, "#000", 0, 0) ])

        renpy.register_style_preference("text", "large", style.say_dialogue, "size", 24)
        renpy.register_style_preference("text", "large", style.say_dialogue, "outlines", [ ])

        # The "decorated" alternative will be the default one for the "text" preference since it was registered first.

The following allows the user to select these alternatives using buttons::

    textbutton "Decorated" action StylePreference("text", "decorated")
    textbutton "Large" action StylePreference("text", "large")

.. include:: inc/style_preferences

Other Style Functions
---------------------

.. function:: style.rebuild()

    This causes named styles to be rebuilt, allowing styles to be
    changed after the init phase has finished.

    .. warning::

        Named styles are not saved as part of the per-game data. This
        means that changes to them will not be persisted through a save
        and load cycle.
