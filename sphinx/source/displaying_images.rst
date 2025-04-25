.. _displaying-images:

=================
Displaying Images
=================

The defining aspect of a visual novel, lending its name to the form, are
the visuals. Ren'Py contains four statements that control the display of
images, and a model that determines the order in which the images are
displayed. This makes it convenient to display images in a manner that
is suitable for use in visual novels and other storytelling games.

The four statements that work with images are:

* ``image`` - defines a new image.
* ``show`` - shows an image on a layer.
* ``scene`` - clears a layer, and optionally shows an image on that layer.
* ``hide`` - removes an image from a layer.

As abrupt changes of image can be disconcerting to the user, Ren'Py
has the ``with`` statement, which allows effects to be applied
when the scene is changed.

Most (if not all) of the statements listed in this page are checked by
:ref:`lint`, which is not the case for their python equivalents.


Concepts
========

.. _concept-image:

Image
-----

An image is something that can be show to the screen using the show
statement. An image consists of a name and a displayable. When the
image is shown on a layer, the displayable associated with it is
displayed on that layer.

An :dfn:`image name` consists of one or more names, separated by
spaces. The first component of the image name is called the :dfn:`image
tag`. The second and later components of the name are the :dfn:`image
attributes`.

For example, take the image name ``mary beach night happy``. The image
tag is ``mary``, while the image attributes are ``beach``, ``night``,
and ``happy``.

A displayable is something that can be shown on the screen. The most
common thing to show is a static image, which can be specified by
giving the filename of the image, as a string. In the example above,
we might use :file:`mary_beach_night_happy.png` as the filename.
However, an image may refer to :doc:`any displayable Ren'Py supports
<displayables>`, not just static images. Thus, the same statements
that are used to display images can also be used for animations, solid
colors, and the other types of displayables.

Layer
-----

A layer is a list of displayables that are shown on the screen. Ren'Py
supports multiple layers, including user-defined layers. The order of
the layers is fixed within a game (controlled by the
:var:`config.layers` variable), while the order of displayables within
a layer is controlled by the order in which the scene and show
statements are called, and the properties given to those statements.

The following layers are defined as part of Ren'Py:

master
    This is the default layer that is used by the scene, show, and
    hide statements. It's generally used for backgrounds and
    character sprites.

transient
    The default layer used by ui functions. This layer is cleared at
    the end of each interaction.

screens
    This layer is used by the screen system.

overlay
    The default layer used when a ui function is called from within
    an overlay function. This layer is cleared when an interaction is
    restarted.

Additional layers can be defined by calling :func:`renpy.add_layer`, and
using the various layer-related :doc:`configuration variables <config>`.
Using the :ref:`camera statement <camera>`, one or more transforms can be
applied to a layer.

.. _defining-images:

Defining Images
===============

There are two ways to define images. You can either place an image file
in the image directory, or an image can be defined using the image statement.
The former is simple, as it involves placing properly named files in a directory,
while the latter a allows more control over how the image is defined, and allows
images that are not image files.

Images defined using the image statement take precedence over those defined
by the image directory.

.. _image-directory:
.. _images-directory:

Images Directory
----------------

The image directory is named "images", and is placed under the game directory.
When a file with a .jpg, .jpeg, .png, or .webp extension is placed underneath this directory,
the extension is stripped, the rest of the filename is forced to lowercase,
and the resulting filename is used as the image name if an image with that
name has not been previously defined.

This process takes place in all directories underneath the image directory. For
example, all of these files will define the image ``eileen happy``::

    game/images/eileen happy.png
    game/images/Eileen Happy.jpg
    game/images/eileen/eileen happy.png

When an image filename is given, and the image is not found, the images directory
is searched.

.. _oversampling:

Oversampling
------------

By default, the pixel size of an image defines the size it will take up
when displayed. For example, if an image is 1920x1080 pixels, and the
game is configured, using :func:`gui.init`, to run at 1920x1080, the
image will fill the entire screen.

When oversampling is enabled, the size that the image is displayed at is
smaller than the image size would imply. For example, if an image is 3480x2160,
and has an oversample of 2, then each axis will be halved, and the image would
fill the same 1920x1080 window.

This is useful when the image might be zoomed in on, and the extra detail is
required. Oversampling is also useful in conjunction with :var:`config.physical_width`
and :var:`config.physical_height` to allow a game to be remade with higher
resolution graphics.

Oversampling is automatically enabled if the image ends with an '@' followed
by a number, before the extension. For example, :file:`eileen happy@2.png` is
2x oversampled, and :file:`eileen happy@3.png` will be 3x oversampled. Oversampling
can also be enabled by giving the `oversample` keyword argument to :func:`Image`.

A directory can also specify how much to oversample images inside it. For example,
:file:`images/@2/eileen happy.png` will be oversampled 2x.

.. _image-statement:

Image Statement
---------------

The ``image`` statement is used to define an image. An image statement
consists of a single logical line beginning with the keyword ``image``,
followed by an image name, an equals sign ``=``, and a
displayable. For example::

    image eileen happy = "eileen_happy.png"
    image black = "#000"
    image bg tiled = Tile("tile.jpg")

    image eileen happy question = VBox(
        "question.png",
        "eileen_happy.png",
        )

When an image file is not directly in the game directory, you'll need to
give the directories underneath it. For example, if the image is at
:file:`game/eileen/happy.png`, then you can write::

    image eileen happy = "eileen/happy.png"

The image statement is run at init time, before the menus are shown
or the start label runs. When not contained inside an ``init`` block,
image statements are run as if they were placed inside an ``init`` block of
priority 500.

See also the :ref:`ATL variant of the image statement. <atl-image-statement>`


.. _show-statement:

Show Statement
==============

The ``show`` statement is used to display an image on a layer. A show
statement consists of a single logical line beginning with the
keyword ``show``, followed by an image name, followed by zero or
more properties.

If the show statement is given the exact name of an existing image,
that image is the one that is shown. Otherwise, Ren'Py will attempt to
find a unique image that:

* Has the same tag as the one specified in the show statement.
* Has all of the attributes given in the show statement.
* If an image with the same tag is already showing, shares the largest
  number of attributes with that image.

If a unique image cannot be found, an exception occurs.

If an image with the same image tag is already showing on the layer,
the new image replaces it. Otherwise, the image is placed above all
other images in the layer. (That is, closest to the user.) This order
may be modified by the ``zorder`` and ``behind`` properties.

The show statement does not cause an interaction to occur. For the
image to actually be displayed to the user, a statement that causes an
interaction (like the say, menu, pause, and with statements) must be
run.

The show statement takes the following properties:

``as``
    The ``as`` property takes a name. This name is used in place of the
    image tag when the image is shown. This allows the same image
    to be on the screen twice.

``at``
    The ``at`` property takes one or more comma-separated
    simple expressions. Each expression must evaluate to a
    transform. The transforms are applied to the image in
    left-to-right order.

    If no at clause is given, Ren'Py will retain any existing
    transform that has been applied to the image, if they were
    created with ATL or with :class:`Transform`. If no transform
    is specified, the image will be displayed using the :var:`default`
    transform.

    See the section on :ref:`replacing transforms <replacing-transforms>`
    for information about how replacing the transforms associated with
    a tag can change the transform properties.

``behind``
    Takes a comma-separated list of one or more names. Each name is
    taken as an image tag. The image is shown behind all images with
    the given tags that are currently being shown.

``onlayer``
    Takes a name. Shows the image on the named layer.

``zorder``
    Takes an integer. The integer specifies the relative ordering of
    images within a layer, with larger numbers being closer to the
    user. This isn't generally used by Ren'Py games, but can be useful
    when porting visual novels from other engines. This can also be
    useful for displaying an image that will be above any zorder-less
    image displayed afterwards, without the burden of placing it on
    another layer.

Assuming we have the following images defined::

    image mary night happy = "mary_night_happy.png"
    image mary night sad = "mary_night_sad.png"
    image moon = "moon.png"

Some example show statements are::

    # Basic show.
    show mary night sad

    # Since 'mary night sad' is showing, the following statement is
    # equivalent to:
    # show mary night happy
    show mary happy

    # Show an image on the right side of the screen.
    show mary night happy at right

    # Show the same image twice.
    show mary night sad as mary2 at left

    # Show an image behind another.
    show moon behind mary, mary2

    # Show an image on a user-defined layer.
    show moon onlayer user_layer

Attributes management
---------------------

As shown above, attributes can be set, added and replaced.

They can also be removed using the minus sign::

    # show susan being neutral
    show susan

    # show susan being happy
    show susan happy

    # show susan being neutral again
    show susan -happy

.. _show-expression-statement:

Show expression
---------------

A variant of the show statement replaces the image name with the
keyword ``expression``, followed by a simple expression. The
expression must evaluate to a displayable, and the displayable
is shown on the layer. To hide the displayable, a tag must be
given with the as statement.

For example::

    show expression "moon.png" as moon

Show Layer
----------

The ``show layer`` statement is discussed alongside the :ref:`camera statement <camera>`,
below.

.. _scene-statement:

Scene Statement
===============

The ``scene`` statement removes all displayables from a layer, and then
shows an image on that layer. It consists of the keyword ``scene``,
followed by an image name, followed by zero or more properties. The
image is shown in the same way as in the show statement, and the scene
statement takes the same properties as the show statement.

The scene statement is often used to show an image on the background
layer. For example::

    scene bg beach

**Scene Expression.**
Like the show statement, the scene statement can take expressions
instead of image names.

**Clearing a layer.**
When the image name is omitted entirely, the scene statement clears
all displayables from a layer without showing another
displayable.

.. _hide-statement:

Hide Statement
==============

The ``hide`` statement removes an image from a layer. It consists of the
keyword ``hide``, followed by an image name, followed by an optional
property. The hide statement takes the image tag from the image name,
and then hides any image on the layer with that tag.

Hide statements are rarely necessary. If a sprite represents a
character, then a hide statement is only necessary when the character
leaves the scene. When the character changes her emotion, it is
preferable to use the show statement instead, as the show statement
will automatically replace an image with the same tag.

The hide statement takes the following property:

``onlayer``
    Takes a name. Hides the image from the named layer.

For example::

    e "I'm out of here."

    hide eileen

You should never write::

    hide eileen
    show eileen happy

Instead, just write::

    show eileen happy


.. _with-statement:

With Statement
==============

The ``with`` statement is used to apply a transition effect when the scene
is changed, making showing and hiding images less abrupt. The with
statement consists of the keyword ``with``, followed by a simple
expression that evaluates either to a transition object or the special
value ``None``.

The transition effect is applied between the contents of the screen at
the end of the previous interaction (with transient screens and
displayables hidden), and the current contents of the scene, after the
show and hide statements have executed.

The with statement causes an interaction to occur. The duration of
this interaction is controlled by the user, and the user can cause it
to terminate early.

For a full list of transitions that can be used, see the chapter on
:doc:`transitions <transitions>`.

An example of the with statement is::

    show bg washington
    with dissolve

    show eileen happy at left
    show lucy mad at right
    with dissolve

This causes two transitions to occur. The first with statement uses
the ``dissolve`` transition to change the screen from what was
previously shown to the washington background. (The ``dissolve``
transition is, by default, defined as a .5 second dissolve.)

The second transition occurs after the Eileen and Lucy images are
shown. It causes a dissolve from the scene consisting solely of the
background to the scene consisting of all three images – the result is
that the two new images appear to dissolve in simultaneously.

.. _with-none:

With None
---------

In the above example, there are two dissolves. But what if we wanted
the background to appear instantly, followed by a dissolve of the two
characters? Simply omitting the first with statement would cause all
three images to dissolve in – we need a way to say that the first
should be show instantly.

The with statement changes behavior when given the special value
``None``. The ``with None`` statement causes an abbreviated
interaction to occur, without changing what the user sees. When the
next transition occurs, it will start from the scene as it appears at
the end of this abbreviated interaction.

For example, in::

    show bg washington
    with None

    show eileen happy at left
    show lucy mad at right
    with dissolve

Only a single transition occurs, from the washington background to the
scene consisting of all three images.

With Clause of Scene, Show, and Hide Statements
-----------------------------------------------

The show, scene, and hide statements can take an optional ``with`` clause,
which allows a transition to be combined with showing or hiding an
image. This clause follows the statements at the end of the same
logical line. It begins with the keyword ``with``, followed by a
simple expression.

The with clause is equivalent to preceding the line with a ``with
None`` statement, and following it by a :ref:`with statement <with-statement>` containing the
text of the with clause. For example::

    show eileen happy at left with dissolve
    show lucy mad at right with dissolve

is equivalent to::

    with None
    show eileen happy at left
    with dissolve

    with None
    show lucy mad at right
    with dissolve

Note that even though this applies to the :ref:`show-screen-statement`
and :ref:`hide-screen-statement` statements too,
:ref:`call-screen-statement` differently.

.. _camera:

Camera and Show Layer Statements
================================

The ``camera`` statement allows one to apply a transform or ATL transform to an
entire layer (such as "master"), using syntax like::

    camera at flip

or::

    camera:
        xalign 0.5 yalign 0.5 rotate 180

To stop applying transforms to the layer, use::

    camera

The camera statement takes an optional layer name, between ``camera`` and
``at`` or ``:``. ::

    camera mylayer at flip

The ``show layer`` statement is an older version of ``camera``, with some
differences, that is still useful. ::


    show layer master:
        blur 10

The differences are:

* The transforms applied with ``show layer`` are cleared at the
  next ``scene`` statement, while ``camera`` transforms last until
  explicitly cleared.

* ``show layer`` requires a layer name, while ``camera`` defaults to the
  master layer.


Hide and Show Window
====================

The ``window`` statement is used to control if a window is shown when a character
is not speaking (for example, during transitions and pauses). The ``window show``
statement causes the window to be shown, while the ``window hide`` statement hides
the window.

If the optional transition is given, it's used to show and hide the window.
If not given, it defaults to :var:`config.window_show_transition` and
:var:`config.window_hide_transition`. Giving None as the transition prevents
it from occurring.

The window itself is displayed by calling :var:`config.empty_window`. It defaults to
having the narrator say an empty string. ::

    show bg washington
    show eileen happy
    with dissolve

    window show dissolve

    "I can say stuff..."

    show eileen happy at right
    with move

    "... and move, while keeping the window shown."

    window hide dissolve

Image Functions
===============

.. include:: inc/image_func

See also
========

:doc:`statement_equivalents` : how to use most of the features described here in a
python context.

:doc:`displayables` : other objects to display, more diverse than basic images.
