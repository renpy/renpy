Splashscreen and Presplash
==========================

.. _adding-a-splashscreen:

Adding a Splashscreen
---------------------
A splash screen is an image or movie that appears when the game is starting up
and before it goes to the menu. Usually these are logos or intro videos. The
"splashscreen" label automatically plays before the main menu. However, the same
code applies to a splashscreen located anywhere in your game under a different
label.

To add a textual splashscreen to your game, insert code like the below anywhere in
your script files (as long as it is not itself in a block)::

    label splashscreen:
        scene black
        with Pause(1)

        show text "American Bishoujo Presents..." with dissolve
        with Pause(2)

        hide text with dissolve
        with Pause(1)

        return

Here's another example of a splashscreen, this time using an image and
sound::

    image splash = "splash.png"

    label splashscreen:
        scene black
        with Pause(1)

        play sound "ping.ogg"

        show splash with dissolve
        with Pause(2)

        scene black with dissolve
        with Pause(1)

        return

And finally, with a movie file::

    label splashscreen:

        $ renpy.movie_cutscene('movie.ogv')

        return

.. _presplash:

Adding a Presplash
------------------

A presplash is an image shown while Ren'py is reading the scripts and
launching the game. To show such and image while the engine is starting up,
create an image file named :file:`presplash.png`, :file:`presplash.jpg`,
:file:`presplash.webp`, or :file:`presplash.avif` and save it into the game directory.

presplash.png (or .jpg, .webp, .avif)
    The image that's used when the game is loading.

This will only work on computer platforms, not on android, ios or web.
For the android platform, see :ref:`android-presplash`, and for the web,
see :ref:`Web Presplash <web-presplash>`.

The :var:`config.minimum_presplash_time` variable sets a minimum time the
presplash is shown for.

Adding a Progress Bar
---------------------

Instead of a static image, it is also possible to show a progress bar indicating
the progress until the engine has loaded. This replaces the regular presplash image
and will automatically take precedence if both are supplied.

The progress bar is themeable and requires you to supply two files in either
PNG, JPG, or WEBP format:

presplash_background.png (or .jpg, .webp, .avif)
    The background image of the progress bar. This is shown in its entirety during
    startup, so it can be used to provide any kind of background for the progress
    bar, i.e. by adding a border or any other solid background.
    This should always be completely opaque.

presplash_foreground.png (or .jpg, .webp, .avif)
    The foreground image of the progress bar. This is revealed from left to right
    during the loading sequence. This should be used to provide the look of the
    actual progress bar.
    This may contain transparency.

The way this works is that Ren'Py will first show :file:`presplash_background.png` and
subsequently will render :file:`presplash_foreground.png` on top, revealing it from
left to right as the loading progresses.

The theming of the bar is completely up to you, but you can find two examples of
how things could look below:

.. ifconfig:: renpy_figures

    .. figure:: presplash/presplash_background_1.png
        :width: 100%

        An example of how the progress bar background could look.

    .. figure:: presplash/presplash_foreground_1.png
        :width: 100%

        An example of how the progress bar foreground could look.

    .. figure:: presplash/presplash_background_2.png
        :width: 100%

        A slightly more elaborate example of how the progress bar background
        could look.

    .. figure:: presplash/presplash_foreground_2.png
        :width: 100%

        A slightly more elaborate example of how the progress bar foreground
        could look.

Transparent Presplash
---------------------

If the top-left pixel of the presplash background image is transparent, the
presplash window will be transparent as well. 1-bit transparency is used,
with pixels with 0 alpha being transparent, and all other pixels being
opaque.


Mobile and Web Presplash Screens
--------------------------------

The Android, iOS, and Web platforms have their own presplash screens. These
are documented elsewhere:

* Android :ref:`android-presplash`
* iOS :ref:`ios-storyboard`
* Web :ref:`web-presplash`
