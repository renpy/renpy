Live2D Cubism
=============

`Live2D Cubism <https://www.live2d.com/en/>`_ is a system that allows you
to animate 2D images, such as the character sprites in a visual novel. These
images are drawn in a series of layers - for example, a layer for pupils and
irises, a layer for the whites of the eyes, a layer for the eyebrows, and so
on.

The Live2D software lets you associate meshes with each of these layers,
and then specify how the meshes are deformed (the shape of each mesh is
changed) as the parameters are adjusted. The Live2D software lets you
create motion files that determine how these parameters are adjusted over
time, and expression files that determine expressions.

Ren'Py's Live2D integration involves taking the files that Live2D produces,
and using them to define animations that can be displayed in Ren'Py. Ren'Py
processes the motions and expressions to determine the values of
the parameters. This is passed to the Cubism SDK for Native, which gives
Ren'Py back a list of meshes to show. Ren'Py then renders these meshes, and the result is a Live2D character on the screen.

Ren'Py supports Live2D animations in the Cubism 3 and Cubism 4 formats.
It supports the playback of expressions and motions.

.. warning::

    Live2D is not supported on the x86_64 Android platform, as a DLL is not
    provided for this platform. This means that it may have problems running
    on the Android emulator or ChromeOS.

    Live2D is not supported on the web platform.

    Installing Live2D on iOS requires copying the static libraries into your
    iOS project by hand.

Installing Live2D
-----------------

Before you can use Live2D, you'll need to download and install the Cubism
SDK for Native, found on the
`Live2D website <https://www.live2d.com/en/download/cubism-sdk/download-native/>`_.
Please note that you may need to purchase a license to use Live2D if your
business makes more than a certain amount of money a year.

Once you've downloaded Live2D, you can install it from the Ren'Py launcher. To
install, go to "preferences", then click "Install libraries". Place the
CubismSdkForNative-4-r.1.zip file in the Ren'Py SDK directory, which can
be accessed using the button in the bottom right of the install libraries
screen. Then click "Install Live2D Cubism SDK for Native". After a short
amount of time, Live2D will be installed.

Opt in to GL2
-------------

To use Live2D, you'll need to opt in to the Model-based renderer, by adding
the line::

    define config.gl2 = True

to your game. This has to be done once per game.


Defining Animations
-------------------

Live2D animations are defined using the Live2D displayable and the image statement:

.. function: Live2D(filename, zoom=None, top=0.0, base=1.0, height=1.0, alias={}, loop=False, fade=None, seamless=None, attribute_function=None, **properties)

    This displayable displays a Live2D animation.

    `filename`
        This may either be a model3.json file defining a Live2D animation, or a
        directory containing that animation. In the latter case, the last
        component of the directory is taken, and has .model3.json appended
        to find the file.

        For example, "Resources/Hiyori" and "Resources/Hiyori/Hiyori.model3.json"
        are equivalent.

    `zoom`
        If not None, a zoom factor that is applied. This takes precedence
        over `top` and `base`.

    `top`
        The top of the image, for sizing purposes. This is a fraction of the
        image, with 0.0 being the top and 1.0 the bottom.

    `base`
        The bottom of the image, for sizing purposes. This is a fraction of
        the image, with 0.0 being the top and 1.0 being the bottom. This
        also becomes the default value of yanchor.

    `height`
        The height that the image is scaled to. This is a fraction of the
        virtual height of the screen.

    `loop`
        True if the final motion should be looped, False otherwise.

    `alias`
        A dictionary mapping aliases to the motions or expressions they
        alias.

    `fade`
        True if motion fading should be enabled, False if motion fading
        should not be enabled, and None to use the value of :var:`_live2d_fade`.

    `nonexclusive`
        If not None, this should be a list of names of nonexclusive expressions.
        Expressions default to being exlcusive, with only one beign shown at
        a time. If listed here, any number of nonexclusive expressions can be
        shown, in addition to one exclusive expression.

    `seamless`
        This determines if seamless looping should be used. Seamless looping
        avoids fading between loops of a single motion. This may be True to
        enable seamless looping all the time, False to dispable it all the
        time, or a set of motions to be looped.

    `attribute_function`
        If not None, this is a function that takes a tuple of attributes,
        and returns a second tuple of attributes. This can be used to replace
        attributes for the purpose of display only - the attributes it returns
        are not used when showing an image.  It should ensure
        that at most one attribute corresponding to an expression is given.

    `attribute_filter`
        If not None, this is a function that takes a tuple of attributes,
        and returns a second tuple of attributes. This is usually used to
        filter out nonexclusice attributes that conflict with each other. The attributes
        are ordered such that more recently requested attributes come first,
        meaning that in the case of a conflict, the first attribute should
        win.

    The difference between `attribute_function` and `attribute_filter` is
    that the former is generally used to compute replacement - the presence
    of two attributes means one should be replaced by a third. The latter
    is used to resolve conflicts between attributes, like having a group of
    attributes where only one is valid.

    Only `filename` should be given positionally, and all other arguments should
    be given as keyword arguments.

    The values of `alias`, `fade`, `nonexclusive`, and `seamless`, `attribute_function` and `attribute_filter`
    are shared between all Live2D objects that share `filename`, such that these only need to be supplied once.

Live2D displayables should be assigned to an image statement::

    image hiyori = Live2D("Resources/Hiyori", base=.6)

It's also possible to define attributes, and this is very useful when
defining different zooms and scaling factors. ::

    image hiyori close = Live2D("Resources/Hiyori", base=.6)
    image hiyori far = Live2D("Resources/Hiyori", base=.9)

Using Animations
----------------

The usual way to display a Live2D image is to display it using the
show statement. In addition to any attributes added as part of the
image statement, the names of expressions and motions can be used.

Some examples are::

    show natori exp_00 mtn_01
    show hiyori m10
    show hiyori m10 m01

These use the default names found in the Cubism SDK sample names. The names
of the motions and expressions are taken from the Live2D files, and if they
begin with the name of the model3.json file (without directories or extensions),
followed by an underscore, then that prefix is removed. (For example, "Hiyori_m01"
becomes just m01.)

At most one exclusive expression can be used, and any number of nonexclusive expressions and
motions can be given. When more than one motion is given, the motions are played in order,
and the final motion is looped if loop is True.
This makes it possible for a motion to be played, followed by an idle animation.
Each motion can only appear once, unless multiple aliases for that motion are created.

There are two special attributes ``null`` and ``still``. The null attribute
means that no exclusive expression file should be applied, giving the character's
default expression. The ``still`` motion stops all motion.

Nonexclusive expressions persist until removed with attribute negation::

    show hiyori -wave

Scaling
-------

Many Live2D models are defined at high resolutions, at least in the internal
coordinate system that the models use. To compensate for this, Ren'Py includes
two ways to scale down the Live2D model.

The first is the `zoom` argument. This can directly set the zoom factor of the
model. If zoom is used, then the other scaling parameters are ignored.

Otherwise, the `top`, `base`, and `height` arguments are used. The first two
specify two lines, relative to the top and bottom of the image. (As elsewhere
in Ren'Py, 0.0 is the top and 1.0 is the bottom.) When these arguments are used,
two things happen:

* The image is scaled so that the area between `top` and `base` takes up `height`,
  where `height` is a fraction of the screen.
* The anchor is adjusted so that `base` will be placed at the bottom of the
  screen.

When figuring out how to scale a Live2D animation, what I do first is adjust the `base` parameter until the right part of the animation is lined
up with the bottom of the screen. Then:

* If the image is too big, reduce `height` until it's the right size.
* If the image is too small, increase `top` to reduce the amount of blank
  space above the animation.

Motion Fading
-------------

Ren'Py's support for Live2D includes motion fading. Normally, when Ren'Py
changes from one animation to another, the transition is abrupt - one
animation is stopped, and the other starts. If a transition occurs,
both animations are played at the same time.

Live2D supports a different model, in which the old animation can be
smoothly faded into the new one, but interpolating the parameters. Think
of this like a character moving their arms into position, rather than
dissolving from one position to another.

Motion fading is controlled with the `fade` argument. If it's true,
motion fading is used, and if it's false, then abrupt changes occur. If None,
motion fading is controlled by the ``_live2d_fade`` variable:

.. var:: _live2d_fade = True

    If true, Live2D animations use motion fading. If False, animations
    are transitioned abruptly.

Aliasing
--------

The `alias` parameter lets you specify your own names for the motions
that would otherwise be automatically defined. For example, one could do::

    image hiyori = Live2D("Resources/Hiyori", base=.6, aliases={"idle" : "m01"})

To be able to use::

    show hiyori idle

Instead of::

    show hiyori m01


Loop and Image Prediction
-------------------------

Ren'Py's Live2D support can loop the final animation if the `loop` parameter
is set to True. If the animation is being looped, it is important to add
greater than .2 second pauses that Ren'Py can exploit to perform expensive
image prediction. (This may not be necessary if image prediction and loading
can happen at other times.)

Functions
---------

.. include:: inc/live2d
