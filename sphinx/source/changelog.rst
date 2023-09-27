=======================
Changelog (Ren'Py 7.x-)
=======================

*There is also a list of* :doc:`incompatible changes <incompatible>`

.. _renpy-8.2.0:
.. _renpy-7.7.0:

8.2.0 / 7.7.0
=============


Harfbuzz Integration
--------------------

Ren'Py now uses the Harfbuzz library to perform text shaping. On all
versions of Ren'Py, Harfbuzz is used to supply additional information
to the freetype authinter.

On Ren'Py 8, Harfbuzz is also used to shape text, reordering and selecting
gtlphs based on the context they're in and the language of the text provided.
This is required to support scripts that require complex text shaping,
such as Brahmic/Indic scripts. (You'll need to provide a font that
supports the appropriate language.)

The new :propref:`shaper` style property controls the shaper used to text,
for compatibility with older versions of Ren'Py.


Emoji-Related Text Improvements
-------------------------------

Next, Ren'Py has gained the ability to render fonts that use the COLRv0 standard
to provide color glyphs. Ren'Py ships with a font that contains the Twiemoji images,
which covers a majority of the Emoji in use (but not all of them).

Ren'Py will automatically switch to the Emoji font when it encounters Emoji
characters in text. The supported characters are those in the
`Emoji 15.1 <https://unicode.org/Public/emoji/15.1/emoji-test.txt>`_ standard.

Ren'Py 8 with Harfbuzz shaping is required to render joining sequences of Emoji,
including things like gender and skin-tone modifiers, so you'll need Ren'Py 8
to have those work. This switching occurrs when a font tag is not being
used.

The new :propref:`emoji_font`, :propref:`prefer_emoji` style properties control
Emoji font selection.

Fundamentally, you can include Emoji into your game by typing it into your
script as character dialogue. For example::

    e "I'm feeling 😃 today."

Variable Fonts
--------------

Ren'Py now supports OpenType variable fonts. These are fonts that use
one or more axes of variablity to change how the font is rendered. For
example, a font may have the "weight" axis, which controls how bold the
font is, and the "width" axis, which controls how wide the font is.

Variable font support required Ren'Py 8 and the harfbuzz shaper to work.

To support variable fonts, Ren'Py has added the :propref:`instance` and
:propref:`axis` style properties, and the :tt:`instance` and :tt:`axis`
text tags, as well as the :func:`renpy.variable_font_info` function.

See the :ref:`variable fonts documentation <variable-fonts>` for more information.

Font Hinting
------------

There is a new :propref:`hinting` mode "auto-light", that performs autohinting
in the vertical but not horizontal direction.

The new :var:`config.font_hinting` variable makes it possible to enable
font hinting on a per-font basis, while the style system can be used to
control hinting per-use. For example::

    define config.font_hinting["MyFont.tff"] = "bytecode"

enables bytecode hinting for MyFont.ttf.

Speech Bubble Improvements
--------------------------

The speech bubble feature that was added in Ren'Py 8.1 now has a new way to
retain speech bubbles, so that the bubbles pop up one at a time, and
remain displayed on the screen until explicitly cleared, similar to
dialogue in motion comics. See the :ref:`speech bubble documentation <retained-bubbles>`
for more information.

The new :var:`bubble.properties_callback` variable can be given a function
that filter the list of bubble property names based on the image tag
that's speaking. This makes it possible to have bubbles that are
specific to some but not all characters.

Features
--------

The virtual dpi of an SVG file can be set with the new `dpi`
parameter to :func:`Image`.

The new :func:`CopyToClipboard` action copies text to the clipboard.

The new :func:`renpy.confirm` function provides a way of using
the confirmation screen from within Python.

The new :func:`renpy.reset_all_contexts` function removes all contexts
from the stack, and creates a new context that continues at the next
statement. It can be used to fully reset the game upon load or when
an error happens.

The new :func:`renpy.last_say` function returns information about the
last say statement to run.

The new :func:`iap.request_review` function allows the game to request
that the player review the game on Google Play and the Apple App Store.

The new :var:`gui.history_spacing` variable controls the spacing between
history entries in newly created games.

The :tt:`nw` text tag can now take a value, which is a number of seconds
to wait before the line containing the tag is automatically dismissed.
The common construct "{w=2}{nw}" can now be written as "{nw=2}".

:class:`Movie` now takes a `keep_last_frame` parameter. When true, this
causes a non-looping movie to display its last frame after the movie
ends.

The ``jump expression`` statement can now take a local label name of the form
".local_name". Previously, only "global_name" or "global_name.local_name" were
allowed.


Other Changes
-------------

The non-default hardware video playback path has been removed from android
and ios. This path hadn't been the defaults since 2020, as it supported
a subset of the video formats Ren'Py supports.

Ren'Py now enforces that the angles given to the :tpref:`angle` and :tpref:`anchorangle`
properties are in the range 0 to 360 degrees, inclusive of 0 but not of 360.
Previously, angles outside this range  gave undefined behavior, now the angles
will be clamped to this range. A 360 degree change will no longer cause motion,
but will instead be treated as a 0 degree change.

When animating :tpref:`angle` and :tpref:`anchorangle` with ATL, if a direction
is not supplied, the shortest arc will be used, even if it passes through 0.

Ren'Py will now produce an error when an ATL block is present, but the block is
empty. (For example, ``show eileen happy:`` with no indented lines following it.)

To make it more useful for making interfaces compatible with right-to-left languages,
the :propref:`box_reverse` style property has changed its
behavior in two ways:

* Space is offered to displayables in the order the displayables are presented in
  the screen, where previously the space was offered in reverse order when
  :propref:`box_reverse` was enabled. This can change the sizes of some displayables.
* A hbox that has :propref:`box_wrap` set will wrap from top to
  bottom, rather than bottom to top. A vbox with :propref:`box_wrap`
  set will wrap from left to right, rather than right to left.

When a file causes an autoreload, Ren'Py will check the directory containing
the file and all parent directories for git lock files. The autoreload will
be deferred until the lock files are removed when the git operation
completes.


.. _renpy-8.1.3:
.. _renpy-7.6.3:

8.1.3 / 7.6.3
=============

Changes
-------

Ren'Py now considers :var:`config.gl2` to be true on macOS. This is because
there are several fixes for window resizing on newer versions of macOS
in the gl2 renderer that are not present in the gl renderer.

MMX acceleration for video playback has been re-enabled on Windows and
Linux.

The way the Steam Deck keyboard is shown has changed. They keyboard
is now shown, once, when a text input is displayed. By default, the
keyboard is shown at the top of the screen, and the keyboard will
only be shown once. If it's hidden (for example, the Steam button
is pressed), the player needs to hit Steam+X to show it. This works
around issues with the Steam Deck.

The 32-bit windows Live2D library will be installed into Ren'Py 7.
You may need to reinstall Live2D to get this library.

Fixes
-----

An issue that prevented keys from being bound to text (for example,
keysyms like "r" rather than "K_r") has been fixed.

There have been several documentation fixes.

An issue with rollback not working at the start of the game has been
fixed.


.. _renpy-8.1.2:
.. _renpy-7.6.2:

8.1.2 / 7.6.2
=============

Changes
-------

There have been many documentation improvements.

When using :func:`renpy.classify`, a directory will now match patterns
that do not end with /. (For example, "renpy.app" will match the renpy.app
directory).

ATL has been changed to use a deep compare to determine if a transform should
be continued or restarted. This means a transform will restart if global
variables it uses are changed.

The styles of a viewport's children will not change when it gains drag
focus. This was rarely used, and the style change could cause drags to
be slow or to miss.

Load will now roll the game back to the statement after the last statement
that interacted to the user. (Previously, it would roll back to the start
of the current statement.) This makes rollback on load match other rollbacks.

The :var:`_autosave` variable now takes precedence over forced autosaves,
including those on quit and at choice menus.

PYTHON* variables are filtered from the environment when launching a
Ren'Py project from the launcher.

In self-voicing mode, Ren'Py will try to ensure that self-voicing
notificatons are fully spoken to the player, even if the notification
window fades away.

Self voicing now speaks screens closer to the player before those
further away from the player.

:func:`Frame` will ensure that the frames it draws are at least one
pixel in size in both dimensions.

:func:`renpy.pause` can now roll forward to calls and jumps from screens.

On the web browser, the ``"display" : "window"`` preference now disables
fullscreen mode.

It is now possible to bind mouse buttons to skipping.

Fixes
-----

Problems with the web port entering fullscreen mode have been fixed.

The Ren'Py 8 launcher can now launch games on Windows systems where the
path to Ren'Py is not representable in the system encoding.

The functionality to import Python from the game/ directory has been
improved to better comply with Python's :pep:`302`.

:func:`GamepadExist` now works as documented. As a byproduct of this fix,
the gamepad screen will be displayed in Help when in developer mode.

An issue analyzing nested comprehensions in screen has been fixed, fixing a
case where nested comprehensions could cause default variables to not be
available.

Viewport inertia continues even if the interaction restarts during the
animation.

The if_changed clause to :ref:`play <play-statement>` (and
:func:`renpy.music.play`) now considers and preserves looping.

VS Code launch has been fixed on Linux.

Several crashes on the web port of Ren'Py 7 have been fixed.

Movie functions now ensure the relevant channels exist before playing. This
can fix issue caused by loading a Movie from a save file.


.. _renpy-8.1.1:
.. _renpy-7.6.1:

8.1.1 / 7.6.1
=============

Android
-------

When creating keys for Android, Ren'Py will now use the same key for APKs
and Play Bundles, as for new games it's not necessary to use different keys.
(For existing games, Ren'Py will continue to use the existing separate
keys.)

We've received reports of games uploaded to the Google Play as bundles
having their APKs rejected for having different keys. This was caused by
an old release of Ren'Py that used the APK key for bundles. A solution to
this problem is documented in :ref:`incompatible changes <android-key-migration>`.


Fixes
-----

The "system cursor" :func:`Preference` now applies to :var:`config.mouse_displayable`,
when it used to only disable :var:`config.mouse`.

Web audio now treats the end time as a time, not a duration.

An issue with that prevented audio volumes and pan from participating
in rollback has been fixed.

Fix an issue where Live2D could select an image despite all of the
required attributes not being present.

Support for start, end, and loop times in videos has been
restored.

Hotspots can no longer be const when the images used by the imagemap
the hotspots come from are not const.

An issue with non-resizable windows on macOS has been fixed.

An issue with linting fonts in the font directory has been fixed.

In some cases, when a class that inherited from the object class was changed
to no longer inherit from the object class, Ren'Py would crash. Ren'Py
now diagnoses this error, and :var:`config.ex_rollback_classes` lets you
suppress the error. The error is only shown to developers, and is otherwise
silently ignored.

Other Changes
-------------

The Ren'Py sync screens now use styles prefixed with ``sync``, allowing
basic customization without having to edit the screens.

Ren'Py will disable text input methods when text editing is not possible, which
makes it possible to use the space key to advance the game even if an input
method that uses the space key is active.

ATL Transitions now use the animation timebase. This is generally the same
behavior as before, until the interaction restarts, in which case the
transition would often incorrectly restart.

Preferences no longer have defaults, meaning all preferences can be
changed using the ``default`` statement.

The :term:`absolute <position>` type, used to represent absolute amounts of pixels,
now ensures the result of mathematical operations with integers and
floats remain absolute numbers. This fixes a class of problems where
operations performed on absolutes could produce the incorrect
type, leading to layout problems.

Live2D now checks for a motion after evaluating an `attribute_filter`,
and does not sustain the previous motions if a new motion is present.


.. _renpy-8.1.0:
.. _renpy-7.6.0:

8.1 / 7.6
=========

Documentation Improvements and Fixes
------------------------------------

There have been many documentation improvements and fixes, many of which
are not in the changelog.

The documentation now has a new theme, including a dark mode.

Ren'Py Sync
-----------

Ren'Py Sync is a new feature that makes it easier to move save files between
devices, using a server that is run as part of the Ren'Py project. For
example, when a player has to leave, they can click "Upload Sync" on their
computer to upload the saves and get a short code. They can then choose
"Download Sync" on the copy of their game on their phone, enter the code,
and keep playing as they travel.

Ren'Py Sync is designed with privacy in mind - the saves are encrypted, and
only a hash of the game title is sent to the server.

Ren'Py Sync is enabled by the new :class:`UploadSync` and :class:`DownloadSync`
actions.

Speech Bubble Dialogue
----------------------

Ren'Py now includes a new :doc:`bubble` dialogue system. This is a comprehensive
system that allows dialogue to be displayed in comic-like speech bubbles, and
includes an interactive editor that allows the speech bubbles to be
repositions, and the look of a bubble to be changed interactively.

Adding bubble support to an existing game requires adding files and script
to the game. The bubble documentation includes the required changes.

Platform Improvements
---------------------

Web
^^^

Ren'Py 8.1 can now be used to create games that run inside the web
browser. When running inside the web browser, Ren'Py used Python 3.11
(3.9 is used on all other platforms).

On Ren'Py 8.1, Ren'Py can be used to create progressive web apps that run inside the
browser. Depending on the browser and platforms, it may be possible to
install a web game on a device in a manner similar to a native application.
Other platforms allow pinning a web app to the home screen.

There is a new :func:`Preference`, "web cache preload". If enabled,
the game will download all game data to the device from the web server.
When online, the game will check the downloaded data, and only download
newer data if required. When offline, the game will use the downloaded
data.

Ren'Py can now play back movies on the web platform. Only movies that
the browser supports can be played.

Macintosh
^^^^^^^^^

On the Macintosh, Ren'Py now uses a universal binary that can run natively
on both Intel and Apple Silicon processors.

Android
^^^^^^^

Android has been changed so that the ``android.keystore`` file and
``bundle.keystore`` file are expected to be found in the project's base
directory, and not in the rapt directory. This allows projects to be
built with different keys, and helps ensure the same keys are used
with multiple Android versions.

When the new "Generate Keys" button is pressed, if old keystore files
exist, Ren'Py will offer to copy the old files into the project.

The android configuration file has been renamed from ``.android.json`` to
``android.json``. Ren'Py will automatically create the new file if the old
exists.

Sticky Layers
-------------

A sticky layer is defined as one that, when a tag is shown upon it, will
be treated as that tag's default layer until it is either hidden, or
shown on another sticky layer.

In practice, that means showing a tag on a layer other than its default,
and assuming that layer is sticky, it will be updated with attributes
set via a show or say statement without the need to respecify the layer.

The following example assumes that the default layer for ``eileen`` is
``master``, and that ``near`` is a sticky layer::

    show eileen onlayer near
    eileen happy "Hello there!"  # will now work, where previously it would not
    show eileen excited          # implicit onlayer near
    hide eileen                  # implicit onlayer near
    show eileen                  # implicit onlayer master, eileen's default

The default for this feature is for the ``master`` layer to be sticky, as
well as any layers created with :func:`renpy.add_layer` unless passed
the new parameter ``sticky=False``.

Detached Layers & Layer Displayable
-----------------------------------

Detached layers are creator-defined layers which are not automatically added to
a scene. They are instead displayed using a new :class:`Layer` displayable
which can be show on other layers.

One of the driving factors behind this is that it allows shaders and other
transform effects to be applied to a group of tags while still allowing them to
operate normally with other systems such as show and say statements. It also
also allows the same layer to be shown multiple times, for instance in
reflections or several TV showing the same channel.

As detached layers don't participate in scene building in the same way as
typical layers, they are defined directly in :var:`config.detached_layers`
rather than through :func:`add_layer`, and are inherently sticky.

New Image Formats and Image Oversampling
----------------------------------------

These releases add support for two new image formats:

* The AV1 Image File Format (AVIF) is a new image format that uses modern
  compression techniques to produce smaller files than JPEG, PNG, or WebP.
  In many cases, converting images to AVIF will reduce their size without
  sacrificing image quality.

* SVG files are a vector graphics format used on the web. Ren'Py supports a
  SVG files containing a subset of SVGs  capability. (Notably, Ren'Py
  does not support text in SVG files.) Ren'Py will automatically oversample
  (or undersample) SVGs when the game is scaled, to ensure the SVGs remain
  sharp at any resolution, similar to the way it oversamples text. This makes
  svgs a reasonable choice for interface elemnts that need to remain sharp.

This release of Ren'Py also adds support for oversampling raster images,
like PNG, JPEG, WebP, and AVIF. For these images, oversampling is done
by including an @ and number in the filename. For example, "eileen happy@2.png"
will be oversampled by a factor of 2. This allows for easier ways of making a
remastered version of a game with minimal changes to the code. Image
manipulators, which are now obsolete but common in older games, support
oversampled images.

For raster images, oversampling causes the image file to be loaded at full
resolution, but treated as if it was smaller by the oversampling factor. For
example, if the image is 1000x1000, and is oversampled by 2, it will be treated
as a 500x500 image for the purpose of layout. If the game is scaled up,
all of the image data is available to keep the image sharp.

Image oversampling can also be used with the new :var:`config.physical_width`
and :var:`config.physical_height` variables to upgrade the resolution of
a game without having to adjust the game's layout.

AV1 Video
---------

Ren'Py now supports the modern AV1 video format. AV1 is supported in
WEBM and MKV containers. AV1 videos should be about 30% smaller than
the equivalent quality movie encoded with VP9, the previous best codec.

Note that the newer AV1 format requires more CPU to decode. It's possible
that some hardware that plays VP9 fluidly will struggle with AV1.

Audio
-----

Mixer now work on power in decibels, similar to the way the volume controls
on audio equipment and computers work. An empty mixer slider represents -40 dB
below the maximum volume, while a full bar represents 0 dB, the full volume.
This makes the mixers more dynamic. Previously, the volume slider had to be
very near the bottom before it had an effect. Now, the volume increases and
decreases match the way people perceive loudness.

Variables that control the default mixer volumes, such as :var:`config.default_music_volume`,
:var:`config.default_sfx_volume`, and :var:`config.default_voice_volume` now work on a scale
where 0.0 is -40 dB, and 1.0 is 0 dB. :func:`SetCharacterVolume` works in a similar way,
as do the new :func:`preferences.set_mixer` and :func:`preferences.get_mixer` functions.

The audio fadein and fadeout functions also work using power. This ensures that
the fade is apparent over the course of the entire fadeout or fadein, rather
than only at the end. The audio fading implementation has also been rewritten
to allow fades of very short lengths. Previously, fading would produce errors
if the fade time was too short.

The :var:`config.fadeout_audio` variable (renamed from config.fade_music) controls
the default fadeout used when stopping audio, or changing audio using ``play``. (It
is not used by ``queue``). The default value is now 0.016 seconds, which eliminates
popping sounds that occured when audio was stopped abruptly.

Audio panning (:func:`renpy.music.set_pan`) is now constant-power, so that
panning audio should not change the volume.

Draggable Viewports
-------------------

Viewports can now be dragged by the user, even if a button or other displayable
inside the viewport is focused. Ren'Py will now detect when the user is dragging,
and switch focus to the viewport, allowing the viewport to move.

The `draggable` property of :ref:`viewports <sl-viewport>` and :ref:`vpgrids <sl-vpgrid>`
can now take a :ref:`screen variant <screen-variants>` like "touch", in which
case the viewport will only be draggable if touch is enabled.

\_ren.py Files - Ren'Py in Python
---------------------------------

:doc:`The new \_ren.py file format <ren_py>` allows Ren'Py script to be embedded
in a valid Python file. For example::

    """renpy
    init python:
    """

    flag = True

is equivalent to::

    init python:

        flag = True

The purpose of this new format is to allow Python-heavy script files to be edited
with Python-specific tools, while still running as Ren'Py script.

Constant Stores
---------------

Ren'Py has the ability to mark a :ref:`named store <named-stores>` as a constant,
by setting the ``_constant`` variable in that store. If true, variables in that
:ref:`constant store <constant-stores>` will not be saved, and objects reachable
solely from that store will not participate in rollback.

The reason to declare a store constant is that there are small per-store and
per-variable overheads that are required to support rollback. Declaring a
store constant can eliminate these overheads.

The following stores are declared to be constant by default:

    _errorhandling
    _gamepad
    _renpysteam
    _sync
    _warper
    audio
    achievement
    build
    director
    iap
    layeredimage
    updater

Variables in a constant store can be updated during the init phase, but should
not change after the init phase finishes.

Lenticular Bracket Ruby Text
-----------------------------

:ref:`Ruby text <ruby-text>`, small text above the main characters used
for readings and translations, can now be written be written by enclosing it in
full-width lenticular brackets (【】), with the full-width or half-width
vertical line character (｜ or \|) separating the bottom text from the top text.
For example::

    e "Ruby can be used for furigana (【東｜とう】 【京｜きょう】)."

    e "It's also used for translations (【東京｜Tokyo】)."

In some contexts, the left full-width lenticular bracket (【) must be
doubled, to "【【", to prevent it from being interpreted as the start of
ruby text. For example::

    e "【【This is not | ruby text.】"

Accessibility
-------------

The new :var:`config.tts_substitutions` variable allows the game to
provide substitution rules for self-voicing. That is meant to allow
the creator to control pronunciation of words that might be mispronounced
by the text to speech engine.

For example::

    define config.tts_substitutions = [
        ("Ren'Py", "Ren Pie"),
    ]

Will cause the word "Ren'Py" to be pronounced as "Ren Pie" whenever
self-voicing speaks it.

Self-voicing now respects the voice volume mixer.

Save Token Security
-------------------

Ren'Py now uses tokens to warn users when a save file is moved between
devices, to prevent the user from making mistakes described in the
:doc:`security documentation <security>`.

This works by generating a token the first time Ren'Py is run on a given
computer. This token is included in saves and in persistent data. If the
token for a different computer is found in a save file, the user is warned
and asked if they want to continue. If they choose yes, the user will be
asked if they want to automatically accept all saves from that computer.

Persistent data is loaded if it's from the current computer, or a computer
with an accepted token.

The first time a game is run with a version of Ren'Py supporting save
tokens, all save files that exist for that game are checked, and if a
token does not exist in those files, the token is added. This should prevent
prompting during upgrades to Ren'Py 8.1/7.6 or later.

There is intentionally no way to disable this feature, as it's important
for end-users to be warned about the security issues when possible.

New Search Paths
----------------

Ren'Py will now search for audio files in the ``game/audio`` directory,
and font files in the ``game/fonts`` directory, if not found in the game
directory. Images will still be searched for in the ``game/images`` directory,
but other files will not be found there.

New 3D Stage Properties
-----------------------

There are several new properties that affect the 3D Stage:

:tpref:`point_to`
    Selects the point that the camera is looking at, or has a sprite
    point at a point or the camera.

:tpref:`xrotate`, :tpref:`yrotate`, :tpref:`zrotate`
    Rotates a sprite or the camera around the given axis.

:tpref:`orientation`
    Rotates a sprite or the camera around all three axes at once,
    using the shortest path on a sphere.

Live2D
------

Ren'Py now supports the new features found in Live2D Cubism Editor
4.2. To support these features, it should be run with Cubism 4 Sdk
for Native R6_2 or later.

Live2D is now supported on x86_64 Android.

The new Live2D.blend_opacity method makes it possible for a
Live2D update_function to change the opacity of the Live2D model.

Launcher and Engine Translations
--------------------------------

Where possible, machine translation has been used to update strings
used by the launcher and the engine, to update translations that might
not have been updated in many years.

If you'd like to improve these translations, you can do so. Edit the
.rpy files in launcher/game/tl/`language`, and send them to us. Please
remove the "Automatic translation" lines when you do.

The following languages have had their translations automatically
updated:

* Finnish
* French
* German
* Greek
* Indonesian
* Italian
* Japanese
* Korean
* Polish
* Portuguese
* Russian
* Simplified Chinese
* Turkish
* Ukrainian

The following translations had manual updates:

* French
* Portuguese
* Spanish
* Japanese
* Ukrainian

More New Features
-----------------

The :ref:`input <sl-input>` displayable can now take multiline
input.

The new :ref:`JSONDB <jsondb>` system allows a developer to
store data in a JSON file that can be saved alongside the
game script. For example, a JSONDB is used to store the
speech bubble information.

The new :ref:`areapicker <sl-areapicker>` displayable provides a
way for tools to let the player select an area on the screen.

:class:`Movie` can now take a `group` argument. If the Movie is
in a group, and it has started up, and another Movie in the same
group had displayed in the prior frame, the Movie will display the
last image of the old Movie. This is intended to allow movie sprites
to switch from one to the other seamlessly.

The new :var:`config.file_slotname_callback` variable allows the
developer to customize how file slot names are generated. One
application of this is allow the developer to apply a prefix to
save slots (for example, to select between dlc and non-dlc saves).
The new :var:`autosave_prefix_callback` allows a similar prefix to
be given to autosaves.

A new tool, accessible through the developer (Shift+D) menu, allows
persistent data to be viewed.

The interactive director can now create a statement that removes an
attribute from an image.

The ``show screen``, ``hide screen``, and ``call screen`` statements can
now take ``expression``, ``as``, ``onlayer``, ``zorder``, and ``with``
clauses, which have the same meaning as the corresponding clauses in the
``show`` and ``hide`` statements.

The :func:`renpy.include_module` function can now be used to load a rpym
file in such a way that its init blocks are interleaved with those from
the rest of the game.

The new "voice after game menu" preference controls if voice is allowed
to continue playing after the game menu is shown.

A creator-defined statement can now execute a function at the same
time the ``default`` statements are executed. This is after the init
phase, but before the game starts; when a save is loaded; after
rollback; before lint; and potentially at other times.

The new :var:`config.after_default_callbacks` allows callbacks to be
run immediately after the default statements are executed.

The interactive director now lets you negate an attribute by right
clicking on the attribute name.

The :func:`Text` displayable now takes a new `tokenized` argument. When
true, the Text displayable expects to take a list of tokens taken from
a :doc:`custom text tag <custom_text_tags>`.

Two new layers are now part of Ren'Py. The "top" layer is displayed above
all other layers, and does not participate in transitions. This makes
it useful for display information that is always shown. The "bottom" layer
is displayed below all other layers. The bottom layer is useful for
handling keys in a way that is always active.

Ren'Py supports the C90 encoding for Thai fonts, which uses the unicode
private area to provide glyphs that are combinations of base characters,
vowel marks, and tone marks. This can be enabled by selecting a Thai font
that supports the C90 encoding, and then setting :propref:`language` to
"thaic90".

It's now possible for a mouse keysym to be given modifiers corresponding
to the state of keyboard modifiers when the mouse button was pressed. For
example, "shift_mouseup_1" will only trigger when mouse button 1 is
released while the shift key is held down.

Keysyms have been reworked to make it possible to bind to numeric keypad keys
(like the arrows and home) when numlock is off, and :doc:`the keymap <keymap>`
has been reworked to make better use of the numeric keypad.

Normally, when a displayable or screen with the same tag or name as one
that is hiding is shown, the hiding displayable or screen is removed,
cancelling the hide transform. The new :tpref:`show_cancels_hide` transform
property controls this behavior.

The console (accessed with shift+O) ``help`` command can now take an
expression, in which case it display the pydoc documentation for the
function or class that expression refers to.

The new :func:`renpy.get_translation_identifier` function returns the
unique identifier for the current line of dialogue, if there is one.

The new :var:`config.scene_callbacks` function contains a list of functions
that are called when the scene statement is run or the :func:`renpy.scene`
function is called.

The size text tag now takes multipliers, so it's possible to have::

    "{size=*2}This is double size{/size} and {size=*0.5}this is half size{/size}."

The :ref:`dismiss <sl-dismiss>` displayable now takes a `keysym` property,
specifying what keysym causes the dismiss.

The new :var:`config.autosave_callback` is run after a background autosave
finishes.

The new :func:`renpy.music.pump` function can be called to cause audio changes
to take effect immediately, rather than at the start of the next interaction.
The main use of this is to allow a sound to be played, and then faded out. (By
default, a ``play`` followed by a ``stop`` causes the track to never be
played, and hence never faded out.)

The new :func:`renpy.clear_attributes` function allows for an image tag to be
cleared of all the attributes attached to it. The previous way to do this was
to hide and show the image again, which had the consequence of also resetting
the placement of the image on the screen. It is not the case with this function.

The new ``config.check_conflicting_properties`` variable, which is disabled
in existing games but enabled in newly created games, enables you to check for
conflicting style or transform properties being set concurrently. This is
dangerous as the resulting behavior is undefined and may vary between platforms
and versions of Ren'Py.

The new :var:`config.font_name_map` variable allows you to name font files or
:ref:`fontgroup`, so that it becomes easier to use them in {font} tags.
Previously, there was no way to use a fontgroup in a {font} tag.

The :class:`Scroll` Action now takes a `delay` parameter, so that the scrolling
is animated over a short period of time.

The new :var:`preferences.audio_when_unfocused` preference now enables the audio
of the game to be paused when the player switches to another window.

The screens' ``for`` loops now support the ``continue`` and ``break`` statements.

Disabling Dialogue's :ref:`monologue-mode` is now possible using the
``rpy monologue none`` statement at the beginning of the file it should apply to.

Other Changes
-------------

The polar motion properties (:tpref:`around`, :tpref:`radius`, and :tpref:`angle`)
will now produce circular, rather than oval motion, with radius using the
minimum of the available wdith and height to scale distances expressed as
heights. The new :tpref:`anchoraround`, :tpref:`anchorradius`, and :tpref:`anchorangle`
properties can position the anchor using polar coordinates.

Ren'Py will now produce errors when a screen sets two conflicting
properties, like :propref:`align`, and :propref:`xalign`. Previously,
the behavior of this was undefined.

Lint will now check your game for statements that can never be reached,
and will report the statements.

Lint will now check your game for translations that are no longer being
used, and report those.

It's possible to configure the channels used to upload to itch.io
using the :var:`build.itch_channels` variable.

Triple quote strings can now be used in most places a single
quoted string can. Most notably, this allows triple quoted strings
to be used in screens. For example, you can use::

    screen example():
        text """\
    line 1
    line 2
    line 3"""

to create three lines in one text displayable.

The maximized window state is now stored int preferences, and if a
game was maximized when it shut down it will be maximized again when
started again.

A screen language displayable can now have ``at transform`` on the
first line::

    text "Spinny text" at transform:
        rotate 0.0
        linear 2.0 rotate 360.0
        repeat

It's now possible for a screen language statement to have both an
`at` property and an ``at transform`` block, provided the property
comes first.

Local variables (prefixed with __) may now be used in f-strings.

The {nw} tag will wait for self-voicing to complete, when self-voicing
is enabled.

The ``selected_insensitive`` style prefix will now be generated, and
``selected`` and ``selected_insensitive`` events will be given to
transforms when appropriate.

Displayables with an `id` property can now be given the `prefer_screen_to_id`
property, which controls if properties supplied by the screen override
the properties supplied by the displayable identifier. The default remains
that the displayable identifier overrides the screen.

The ``fadein`` clause can be used when queuing an audio track.

Ren'Py will limit calls to BOverlayNeedsPresent on Steam Deck, preventing
a freezing issue.

Dialogue is now present in the history list (and hence the history screen)
during the statement in which the dialogue is shown. Previously, it was only
present at the end of the statement.

When :var:`config.steam_appid` is not set, Ren'Py will delete any existing
``steam_appid.txt`` file in the game directory. This is to prevent the wrong
app id from being used.

Audio volumes are now preserved when muted. (This means that the volume will
not drop to 0 when the game is muted.)

It is now explicitly documented that non-self-closing tags will be closed at
the end of a block of text. This was the behavior of many versions of Ren'Py,
but would produce lint warnings. Now, the following is explicitly valid::

    e "{size+=20}This is big!"

Self-voicing and auto-forward mode may now be enabled at the same time. When
this is the case, auto-forward will only occur when the dialogue is focused.

Ren'Py no longer requires grids or vpgrids to be full - it will now pad these
grids with nulls as required.

The `execute_init` argument to :func:`renpy.register_statement` now respects
the `init_priority` argument. Previously, all `execute_init` function ran
at init priority 0.

The config.label_callback variable has been renamed to :var:`config.label_callbacks`,
and now takes a list of callback functions.

A number of documented functions, classes and Actions have seen their signatures
(meaning the arguments they take) corrected in the documentation, making them
safer to use.

Ren'Py used to normalize all whitespace to standard spaces, and now
supports non-standard spaces such as \\u3000, the full-width ideographic space.


.. _renpy-7.5.3:
.. _renpy-8.0.3:

8.0.3 / 7.5.3
=============

Security
--------

There is now a new :doc:`security` page in the documentation, intended to help
players understand the security implications of mods and sharing save files.

Modal Screen, Pauses, and Timers
--------------------------------

Based on feedback from creators, the changes to how modal screens interact
with pauses and timers have been redone. As of this version, pauses will
not end when a modal screen is shown, while timers will trigger while
a modal screen is shown above the timer.

There are some cases where this behavior may not be wanted. To deal with
those cases, the :ref:`timer displayable <sl-timer>` and :func:`renpy.pause`
have a new `modal` property/parameter. If `modal` is True, pauses will
end and timers will respect the modal screen, and will not trigger until
the screen disappears. If false, the modal screen will not be respected,
causing pauses to end and timers to trigger while the modal screen is
still displayed.

Changes and Fixes
-----------------

Ren'Py has been updated to target Android API level 33, corresponding to Android 13,
allowing new games to be added to the Google Play store. The Play Billing library
has been updated to version 5.

Init statements inside a module loaded with :func:`renpy.load_module` are now
run in init-priority order.

Lint now respects :var:`config.adjust_attributes`.

A case where blurs could become transparent has been addressed.

When the translation language changes during a menu that is using dialogue as a
caption, Ren'Py will jump the game back to the start of the say statement that
added that dialogue, allowing it to be re-translated.

When a game is being developed, Ren'Py will now produce an error if the first
use of :func:`gui.preference` has not been given a default. This makes an error
that could happen at runtime in that case more explicit.

There have been many documentation improvements.

This release fixes a problem with Matrix equality that could prevent
transform properties that use Matrixes from being animated correctly.

Ren'Py now properly analyzes variables that are bound by lambdas.

The Tutorial and The Question have been translated into Ukrainian, and the
Ukrainian translation of the launcher has been updated.


.. _renpy-7.5.2:
.. _renpy-8.0.2:

8.0.2 / 7.5.2
=============

Fixes
-----

There have been a number of changes to the way autoreload (shift+R) works, to
try to prevent Ren'Py from creating an invalid save file when an autoreload after
an error happens, and Ren'Py is in an invalid state. The goal of these changes
is to preserve the save file from before the change, and reuse that.

Ren'Py is now able to perform audio fadeins and fadeouts of less than 0.68
seconds. Previously such short fadeins and fadeouts would be result in an
underflow and no fading. In this release, the precise duration of a fadein
and fadeout is not strictly guaranteed.

Several functions in achievement.steam (or _renpysteam) had regressions when
reimplmented in terms of achievement.steamapi. These regressions have been
fixed.

An issue that prevented built distributions from launching on aarch64 has
been fixed.

An issue that could cause excessive CPU and memory usage when a store had
large number of variables in it has been fixed.

Loading a save slot that was saved with a different language than is currently set will no
longer prevent :var:`config.after_load_transition` from occurring.

Several problems that preventing In-App Purchases (IAP) from working on Ren'Py
8 have been fixed.

An issue with examples in the tutorial game not working in a non-English languages
has been fixed.

Tinydialogs is now included in the source code distribution of Ren'Py.


Default Focus Changes
---------------------

There have been several changes to the `default_focus` property of focusable
displayables like buttons and bars. This property allows Ren'Py to select a
displayable to gain default focus when displayables are added to removed.

The new rules are:

* When the mouse is used, focus follows the mouse and `default_focus` is ignored.
* When a displayable with a higher `default_focus` than any other displayable
  is shown, it is given focus.
* When the displayable with the highest `default_focus` is hidden, the displayable
  with the next highest non-zero `default_focus` is given focus.

The goal is to support common keyboard and controller navigation patterns,
while not getting in the way of mouse users.


Other Improvements
------------------

Ren'Py will now warn when encoutering an explicit ``translate None`` statement
that does not translate strings, styles, or python.

Ren'Py will now predict dialogue followed by the :ref:`extend <extend>` special
character, and if it can prove that the extend will always occur, will take the
extended text into account when determining line breaking and spacing.

There have been many copyedits and other improvements to Ren'Py's documentation.

The console has been improved to display more Python 3 types.

:func:`MouseDisplayable` now respects :var:`default_mouse`, if set.

In Ren'Py 8, Python blocks are now compiled as if the ``from __future__ import annotations``
statement was present.

A modal screen or dismiss statement now blocks the ``pause`` statement and :func:`renpy.pause``
from ending. Previously, what happened in this case was undefined and varied between
versions.

On macOS, Ren'Py will now properly adjust when the game window is moved between
displays with different scaling.

Command-C and Command-V now work for copy and paste on macOS.

The default input screen in screens.rpy has now been changed to prevent a
conflict between the :propref:`xalign` and :propref:`xpos` of the vbox.
The fix was to change the use of xalign to :propref:`xanchor`.

Ren'Py will now start if a sound card is not present, even in developer mode.
Errors with audio hardware are now written to log.txt.

The Japanese translation has been updated.

New games created with Ren'Py no longer filter out ruby/furigana text tags.



.. _renpy-7.5.1:
.. _renpy-8.0.1:

8.0.1 / 7.5.1
=============

Improvements
------------

The launcher now has a Ukrainian translation, courtesy of Matias B.

The web port will now reuse audio data when an audio file loops, reducing
the memory usage.

ATL transforms used inside a :func:`MouseDisplayable` are now reset each
time the mouse is changed. Previously, this behavior was undefined.

The trace screen used by the console is now updated once per frame.

There have been a large number of documentation improvements.

Fixes
-----

Alt text is now played in first-to-last order. A change to 8.0 caused
the order alt text was played in to be reversed.

A rounding error that would cause the CropMove transitions to work
incorrectly was fixed.

An issue preventing the zoomin and zoomout transitions from working
was fixed.

The Movie displayable can once again take a list of movie files to
play, rather than only a single filename.

An issue with building on Android has been fixed.

Object identity is used to compared the arguments of :func:`Function`
actions. This prevents an issue where an action could be incorrectly
reused if the action's arguments where equal, but not the same (for
example, two empty lists).

Problems with getting and setting Steam statistics have been fixed.

The :ref:`dismiss <sl-dismiss>` is now correctly modal.



.. _renpy-7.5.0:
.. _renpy-8.0.0:

8.0 / 7.5
=========

Python 3 Support (Ren'Py 8.0)
-----------------------------

Ren'Py 8.0 runs under Python 3, the latest major version of the Python
language.

If your game uses minimal Python (for example, just storing character
names and flags), it should work the same as it did before. Otherwise,
please read on.

The move to Python 3 makes over a decade of Python language and
library improvements available to the Ren'Py developer, as described
in the `What's new in Python <https://docs.python.org/3.9/whatsnew/index.html>`_
documentation. There are far too many changes in Python 3 to include here,
so please check that and other Python websites for descriptions.

That being said, a few things made available to the Python in your Ren'Py
games are:

* Functions can have keyword-only parameters. (These are also supported
  in parameter lists for labels, transforms, and screens.)

* The ability to annotate functions arguments and return values with type
  information. (This is only supported in Python.)

* Formatted string literals can now be used. These
  are strings like ``f"characters/{character}.chr"``, where the text in
  braces is replaced by a formatted Python variable, similarly to the
  way that interpolation works in Ren'Py dialogue. This is only available
  in Python, however, and not in most purely Ren'Py statements.

There are a huge number of other improvements in the ten major releases of
Python between 2.7 and 3.9, so be sure to read the above and other Python
documentation to find out everything that's improved.

One of the greatest advantages is that this moves Ren'Py off Python 2.7,
which is no longer supported by the Python Software Foundation, and so
the move to Ren'Py 8.0 helps secure Ren'Py's future.

There are a few things that may need to be converted if you used advanced
Python.

* In Python 3, division always returns a float, rather than an integer.
  (for example, ``3 / 2`` is now 1.5 rather than 1). The ``//`` operator
  divides as an integer. This change can affect Ren'Py positioning,
  where floats are treated differently from integers.

* In Python 3, the keys, items, and values methods of dictionaries now
  return views, not lists. The iterkeys, iteritems, and itervalues
  methods are not supported. The xrange method is gone, and range
  no longer returns a list.

* Except clauses now must be written like ``except Exception as e:``,
  as the old syntax, ``except Exception, e:`` is not supported.

* All strings are now unicode by default (Ren'Py has been forcing this
  for several years), and files are opened in text mode by default.
  (However, :func:`renpy.file` opens files in binary mode. It's been
  renamed to :func:`renpy.open_file` and can take a default encoding.)

* Many Python modules have been renamed.

This is not an exhaustive list.

Ren'Py ships with a cut-down version of the Python Standard library, so
not every Python module is available in Ren'Py. Please let us know if there
is something missing you have a good use for, especially if that module
does not require a library dependency. While ``async`` and ``await``
are available, Ren'Py doesn't directly support coroutines.

Ren'Py 8.0 ships with Python 3.9.10, and is available on the Windows,
macOS, Linux, Android, and iOS platforms. The web platform will
be supported in a future release.

When running under Ren'Py 8, Ren'Py now runs without the equivalent of the
Python ``-O`` flag. This means that docstrings and assert statements are
available.

Our experience is that many games run unchanged under Python 3, especially
games that use Python primarily through the Ren'Py API, to manage
game state. Ren'Py 8 has been used to run unmodified Ren'Py games
going back to the year 2006.


Continued Python 2.7 Support (Ren'Py 7.5)
-----------------------------------------

Ren'Py 7.5 is being released at the same time as Ren'Py 8.0, to continue
to provide a version of Ren'Py that runs on Python 2.7, as a way of
supporting games in development (or being maintained after release)
that still require Python 2.7.

In this release, Ren'Py 7.5 also supports the web platform, which
Ren'Py 8.0 does not yet support.

For this release, Ren'Py 7.5 and Ren'Py 8.0 should support the same
set of of features.

We plan to continue to support Ren'Py 7.x until we see that the community
has moved to Ren'Py 8.x, or until changes to the Python ecosystem mean
that supporting Ren'Py on Python 2 is no longer tenable.

Please test your games on Ren'Py 8 - for many games, few to no changes
will be needed. If for some reason you can't port your game to Ren'Py
8, please let us know what is holding you back.


Platform Support Changes
------------------------

This release adds support for the 64-bit ARM Linux (linux-aarch64)
platform. While based on Ubuntu 20.04, this has been tested on Chromebooks,
and should also work on the 64-bit ARM platform.

The intended way to run Ren'Py games on ARM Linux would be to download
the new ARM Linux SDK package, place the game in the projects directory,
and use that to launch the game. If the files from the ARM Linux SDK are
present when a Linux distribution is made, they will be included, creating
a game that can be launched on ARM, but this is not the default, for
size reasons.

With the move to Ren'Py 8, we are removing support for the
following platforms:

* 32-bit x86 Windows (i686)
* 32-bit x86 Linux (i686)

This reflects the obsolescence of 32-bit x86 computing. These platforms remain
supported by Ren'Py 7.5, but will not be supported by Ren'Py 8.

Web and ChromeOS
----------------

The web platform is currently only supported on Ren'Py 7.5.

Changes to the Safari and Chrome web browsers increased the memory Ren'Py
used by about 50 times, causing RangeErrors when the web browser ran out
of stack memory. Ren'Py 7.5 includes changes to reduces the amount of
memory used inside web browsers. As a result, Ren'Py now runs again
inside Chrome and Safari, including on iOS devices.

The new :var:`config.webaudio_required_types` variable can be given a list of
mime types of audio files used by the game. Ren'Py will only use the web
browser's Web Audio system for playback if all of the mime types are supported
in the browser. If not, webasm is used for playback, which is more likely to
cause skipping if the computer is slow.

The config.webaudio_required_types variable is intended to allow games using ogg
or opus audio to run on Safari, and can be changed if a game only uses mp3 audio.

When importing save files into a web distribution, Ren'Py will now refresh
the list of save files without a restart.

When running as an Android application on a ChromeOS device, the "chromeos"
variant will be selected.

The Ren'Py SDK can be run on ARM Chromebooks.

Android and iOS
---------------

The Android configuration once again prompts as to which store to use
for in app purchases. When no store is selected, libraries to support
purchasing are not included in the project. These libraries would include
the billing permission, which would flag the game as supporting in-app
purchases even if no purchases were used.

Due to issues in underlying libraries, the :func:`renpy.input` function
and ``input`` displayable are now documented as not supporting IME-based
(non-alphabetic) input on Android.

On iOS, OpenGL ES calls are translated to the native Metal graphics system.
Doing this should improve compatibility with recent Apple devices, and
fixes problems running applications under the iOS simulator on Apple
Silicon-based devices.


Steam, Steam Deck, and Epic Games Store
---------------------------------------

This release includes rewritten Steam support, provided by a new
ctypes-based binding that gives access to the entire Steamworks API,
including callbacks. While the Steam support available through the
:doc:`achievement module <achievement>` remains unchanged, this
gives advanced Python programmers access to more Steam functionality.

When Steam is active, Ren'Py will now enable the "steam" variant.

This release includes built-in support for the Steam Deck hardware.
The support includes the ability to automatically display the
on-screen keyboard when :func:`renpy.input` is called.
The steam deck also causes Ren'Py to enable the "steam_deck",
"steam", "medium", and "touch" variants.

We have a `Ren'Py on Steam Deck Guide <https://github.com/renpy/steam-deck-guide>`_
to help you get your game certified on that platform. Thanks go to Valve for
supplying a Steam Deck to test on.

The "Windows, Mac, and Linux for Markets" distribution has been changed to
no longer prefix the contents of the zip file created with the directory
name and version number, meaning it's no longer required to update launch
configurations with each release to Steam. This may require a one-time
update to the launch configuration.

Ren'Py now includes support for being launched by the Epic Games Store,
by ignoring various command line arguments supplied by EGS.


Visual Studio Code
------------------

Ren'Py now includes support for downloading and using Visual Studio Code,
including downloading the `Ren'Py Language <https://marketplace.visualstudio.com/items?itemName=LuqueDaniel.languague-renpy>`_
extension.

The Ren'Py Language extension provides rich support for Ren'Py, including
syntax highlighting, snippets, completion, color previews, documentation,
go to definition, function signatures, error diagnostics, outlining,
and more.

Visual Studio Code also has a large system of extensions, including
spell-checkers, that can be used with with the Ren'Py Language extension.

Visual Studio Code can be activated by going to the editor preferences
and choosing to download it. It's also possible to configure Ren'Py
to use a system install of Ren'Py with extensions that you choose.


Dismiss, Nearrect, and Focus Rectangles
---------------------------------------

Two new displayables have been added to Ren'Py to help use cases like
drop-down menus, pulldown menus, and tooltips.

The :ref:`dismiss <sl-dismiss>` displayable is generally used behind a
modal frame, and causes an action to run when it is activated. This allows,
among other things, a behavior where if the player clicks outside the frame,
the frame gets hidden.

The :ref:`nearrect <sl-nearrect>` displayable lays out a displayable either
above or below a rectangle on the screen. This can be used to display a
tooltip above a button, or a drop-down menu below it. (An example of
a drop-down menu is documented with nearrect, and an example of tooltip
usage is with :ref:`tooltips <tooltips>`.

The rectangles aside of which the nearrect places things can be captured by
the new :func:`CaptureFocus` action, which captures the location of the current
button on the screen. After being captured, the :func:`GetFocusRect` function
can get the focus rectangle, and the :func:`ClearFocus` can clear the
captured focus,  and the :func:`ToggleFocus` action
captures and clears focus based on the current focus state.

ATL and Transforms
------------------

It's now possible to include a block as part of an ATL interpolation.
This means that::

    linear 2.0:
        xalign 1.0
        yalign 1.0

is now allowed, and equivalent to::

    linear 2.0 xalign 1.0 yalign 1.0

Information about :ref:`ATL Transitions <atl-transitions>` and :ref:`Special ATL Keyword Parameters <atl-keyword-parameters>`
has been added to the documentation.

The ``pause 0`` statement has been special-cased to always display one frame,
and is the only way to guarantee at least one frame is displayed. Since 6.99.13,
Ren'Py has been trying various methods to guarantee single frame display, and
many of which led to visual glitches.

When an ATL image is used as one of the children of an image button, its
shown time begins each time it is shown.

The default for the :tpref:`crop_relative` transform property has been changed to
True.

The ``function`` statement will now block execution only if producing a delay,
which allows transforms using it to behave more naturally when catching up with
an inherited timebase.

Image Gallery
-------------

The :class:`Gallery` class now has a new field, `image_screen`, that can be
used to customize how gallery image are displayed.

The :func:`Gallery.image` and :func:`Gallery.unlock_image` methods now
take keyword arguments beginning with `show\_`. These arguments have the
`show\_` prefix stripped, and are then passed to the Gallery.image_screen
as additional keyword arguments. This can be used to include additional
information with the images in the gallery.


Boxes, Grids and Vpgrids
------------------------

Displayables that take up no space (like :ref:`key <sl-key>`, :ref:`timer <sl-timer>`
or a false :ref:`showif <sl-showif>`) inside a :ref:`vbox <sl-vbox>` or :ref:`hbox <sl-hbox>`
will not be surrounded with :propref:`spacing`. These displayables still take
up space in other layouts, such as grids.

Having an overfull vpgrid - when both ``rows`` and ``cols`` are specified - is now
disallowed.

Having an underfull vpgrid now raises an error unless the warning is opted-out using
either the ``allow_underfull`` property or :var:`config.allow_underfull_grids`, the
former taking precedence on the latter.

A vpgrid with both cols and rows specified is underfull if and when it has less than
rows \* cols children. A vpgrid with either cols or rows specified is underfull if and when its number of
children is not a multiple of the specified value.

.. _call-screen-roll-forward:

Call Screen and Roll Forward
----------------------------

The roll forward feature has been disabled by default in the ``call screen``
statement, as it's unsafe and confusing in the general case. The problem is
that the only side-effect of a screen that roll-forward preserves is the return
value of the screen, or the jump location if a screen jumps. Actions with other
side effects, like changing variables or playing music, were not preserved
through a roll forwards.

Roll forward may be safe for a particular screen, and so can be enabled
on a per-screen basis by enabling the new `roll_forward` property on the
screen. If all screens in your game support roll forward, it can be enabled
with the new :var:`config.call_screen_roll_forward` variable.

New Features
------------

The ``show screen``, ``hide screen`` and ``call screen`` statements now
take an ``expression`` modifier, which allows a Python expression to supply
the name of the screen.

There is a new "main" volume that can be accessed through :func:`Preferences`.
The main volume is multiplied with all the other volumes to globally reduce
the volume of the game.

The new  :var:`config.preserve_volume_when_muted` variable causes
Ren'Py to show the current volume when channels are muted.

A button to clean the Ren'Py temporary directory has been added
to the preferences screen of the launcher. This can remove these
files to reduce the space Ren'Py requires.

The new :var:`config.choice_empty_window` variable can customize
the empty window that is shown when a choice menu is displayed. The intended
use is::

    define config.choice_empty_window = extend

Which repeats the last line of dialogue as the caption of the
choice menu.

The :ref:`key <sl-key>` displayable now supports a `capture`
property, which controls if the pressed key is handled further
it does not end an interaction.

The new "anywhere" value of the :propref:`language` style property
allows Ren'Py to break anywhere in a string, for when keeping to
a fixed width is the most important aspect of breaking.

The new `predict` argument to :func:`renpy.pause` makes it possible to pause
until image prediction is finished, including prediction caused by
:func:`renpy.start_predict` and :func:`renpy.start_predict_screen`.

It is now possible to select a language other than the default when
extracting dialogue.

The screen language ``add`` statement now takes an `alt` property,
making it possible to write::

    screen test():
        add "icon.png" alt "The Icon"

The :func:`Hide` action now takes None for the screen name, to hide
the current screen.

:func:`Placeholder` now takes a `text` argument, that overrides the
automatically determined text with something the creator specifies.

The :func:`renpy.dynamic` function can now make variables in namespaces
dynamic.

The new :var:`config.always_shown_screens` variable allows one to define
screens that are always shown (even in the main and game menus). See also
the existing :var:`config.overlay_screens`.

The location and size of the OpenGL viewport is made available to shaders as
u_viewport.

The new RENPY_PATH_TO_SAVES environment variable makes it possible to control
where Ren'Py places system-level saves. The RENPY_MULTIPERSISTENT variable has
been documented, and controls the same thing with multipersistent data.

The new :var:`config.at_exit_callbacks` functions are called when the game
quits. This is intended to allow the game to save additional data created
by the developer.

The :var:`config.default_attribute_callbacks` variable allows a game to
specify default attributes for a tag that are used when other attributes
do not conflict.


Other Changes
-------------

It is now possible to copy from :func:`renpy.input` with ctrl-C, and paste
with ctrl-V. When text input is displayed, ctrl will no longer cause skipping
to happen.

The :func:`renpy.file` function has been renamed to :func:`renpy.open_file`,
with the old named retained. It has also gained an `encoding` parameter to
open the file with an encoding.

The :propref:`focus_mask` style property now defaults to None for drag displayables.
This improves performance, but means that the displayable can be dragged by
transparent pixels.

When adding files to the audio namespace, Ren'Py now scans for flac
files.

Say statements used as menu captions can now take permanent and temporary
image attributes, just like say statements elsewhere.

All position properties can now be supplied as gui variables to buttons.
For example::

    define gui.navigation_button_text_hover_yoffset = -3

now works.

The behavior of modal :ref:`frames <sl-frame>` has been changed. A modal
frame now blocks mouse events when inside the frame, and blocks focus from
being transferred to displayables fully behind the frame, while allowing focus
to be given to other displayables.

The new :var:`config.main_menu_stop_channels` variable controls the
channels that are stopped when entering the main menu.

Layered images are now offered the the full size of the screen whenever
rendered. Previously, when a layered image was used inside a layout (like
hbox, vbox, side, and others), the space offered to the layered image
could change, and relative positions could also change. (This is unlikely,
but happened at least once.) The new `offer_screen` property of layered images
controls this behavior.

A :func:`Character` defined with `interact` false, or otherwise used in a
non-interactive way will now cause an automatic voice line to play, if the
relevant file exists.

When ``window auto`` displays the window before a say or menu-with-caption
statement, Ren'Py will automatically determine if the character to speak
uses NVL or ADV, and will display the correct window. Previously, the last
character in a say statement was used.

The :propref:`activate_sound` plays when activating a drag displayable.

The :func:`VariableValue`, :func:`FieldValue`, and :func:`DictValue` Bar Values
can now call :func:`Return`, to cause the interaction to return a specific value.

The :propref:`adjust_spacing` property is now set to False for dialogue and
narration in new games. This might cause the spacing of text to change, when
the game is resized, in exchange for keeping it stable when extend is used.

Playing or stopping music on a channel now unpauses that channel.

The new :var:`preferences.audio_when_minimized` preference now enables the
audio of the game to be paused when the window is minimized.

The default for :propref:`outline_scaling` is now "linear".

The version of SDL used by Ren'Py has been upgraded to 2.0.20 on non-web
platforms.

Many translations have been updated.

The jEdit editor has been removed, as the Ren'Py integration was largely
obsolete. However, if the version from 7.4.0 is unpacked, it should be
selectable in the launcher.

Versioning
----------

Ren'Py's full version numbers are now of the form major.minor.patch.YYMMDDCCnu,
where:

* YY is the two digit year of the latest commit.
* MM is the month of the commit.
* DD is the day of the commit
* CC is the commit number on that day
* n is present if this is a nightly build.
* u is present if this is an unofficial build.


.. _renpy-7.4.11:

7.4.11
======

The gui.variant Decorator
-------------------------

A new gui.variant decorator has been added to Ren'Py. This should be used
to decorate a function with the name of a variant, and causes that function
to be run, if the variant is active, when the game is first started, and then
each time the gui is rebuilt (which happens when :func:`gui.rebuild` is called,
when a gui preference is changed, or when the translation changes.)

This is expected to be used like::

    init python:

        @gui.variant
        def small():

            ## Font sizes.
            gui.text_size = gui.scale(30)
            gui.name_text_size = gui.scale(36)
            # ...

as a replacement for::

    init python:

        if renpy.variant("small"):
            ## Font sizes.
            gui.text_size = gui.scale(30)
            gui.name_text_size = gui.scale(36)
            # ...

Which only runs once, and lost the changes if the gui was ever rebuilt.

Fixes
-----

The new :var:`config.mouse_focus_clickthrough` variable determines if clicks that
cause the game window to be focused will be processed normally.

The launcher now runs with :var:`config.mouse_focus_clickthrough` true, which
means that it will only take a single click to launch the game.

The `caret_blink` property of Input is now exposed through screen language.

When a Live2D motion contains a curve with a shorter duration then the motion
it is part of, the last value of the curve is retained to the end of the
motion.

Rare issues with a displayable being replaced by a displayable of a different
type are now guarded against. This should only occur when a game is updated
between saves.

Modal displayables now prevent pauses from ending.

An issue that could cause images to not display in some cases (when a displayable
was invalidated) has been fixed.

Starting a movie no longer causes paused sounds to unpause.

AudioData objects are no longer stored in the persistent data. Such objects
are removed when persistent data is loaded, if present.

Platform variables like renpy.android and renpy.ios are now set to follow
the emulated platform, when Ren'Py is emulating ios or android.

When in the iOS and Android emulator, the mobile rollback side is used.

Ren'Py will now always run an `unhovered` action when a displayable (or its
replacement) remains shown, and the focus changes. Previously, the unhovered
action would not run when the loss of focus was caused by showing a second
screen.

When :var:`config.log` is true, the selected choice is now logged properly.

The new :func:`gui.variant` function makes it possible to work around
an issue in the standard gui where the calling :func:`gui.rebuild` would cause
gui variants to reset.

The web browser now checks for progressively downloaded images once per
frame, allowing images to be loaded into the middle of an animation.

Live2D now uses saturation arithmetic to combine motion fadeins and fadeouts,
such that if the fadein contributes 80% of a parameter value, and the
fadeout contributes 20% of the value, 100% of the value comes from
the two motions. (Previously, the fadein and fadeout were applied
independently, such that together, the fadein and fadeout would
contribute 84% of the value, with the remaining 16% taken from
the default.)

When fading from one sequence of Live2D motions to another, the original
sequence ends when a motion fades out.

When preserving screens in the old state for a transition, the later_at_list
and camera lists are taken from the old state, preventing unexpected changes.

The :tpref:`gl_depth` property now causes Ren'Py to use GL_LEQUALS,
which more closely matches Ren'Py's semantics.

The 4-component constructor for matrices has been fixed.

Ren'Py now cleans out the android build directories when producing a Android
App Bundle (AAB) file, preventing problems that might be caused when packaging
multiple games, or a single game where files are deleted.

Live2d now properly handles seamless animation when the same motion is repeated
in a displayable. (For example, ``show eileen m1 m1 m2`` where ``m1`` is seamless.)

Mouse motion is now tracked on Chrome OS devices. This prevents the mouse cursor
from being hidden between clicks.

An issue with windows partially rendering on ChromeOS has been resolved.

An issue with transcludes in screens has been fixed.

An issue that could prevent a transform with both :tpref:`perspective` and
:tpref:`mesh` true from displaying has been fixed.

Buttons now only propagate transform state to direct children, not to
children accessed through ImageReferences.

The ``repeat_`` modifier can now be applied to gamepad events.

A new :var:`config.debug_prediction` variable has been split out of
:var:`config.debug_image_cache`. This controls the logging of
prediction errors to the console and log.txt, making the latter
variable act as documented.

Translations
------------

The German, Indonesian, Polish, and Russian translations have been updated.


.. _renpy-7.4.10:

7.4.10
======

Fixes
-----

This released fixes an issue that prevented large images (larger than
maximum texture size, 4096x4069 on most platforms) from being displayed
by the gl2 renderer.

Dialogue lines that end with the {nw} tag now do not wait for voice to
finish.

Dialogue lines that contain {fast} (including those created
with the ``extend`` character) sustain the voice from the previous
statement.

These supplement a change introduced in 7.4.9 (that missed the changelog),
where timed {w} and {p} text tags will no longer wait for voice to stop
playing before advancing.

The :propref:`focus_mask` property can be slow, but several changes to
have been included to fix pathological cases of slowness. While it's best
to avoid it if possible (the default will change to None for drags, where
it's True now, in 7.5), this should allow for some speedups where it is
True.

Live2D support no longer logs to log.txt by default. That logging can be
restored with :var:`config.log_live2d_loading`.

A problem with automatically determining the Android store has been fixed.


Translations
------------

The Indonesian and Polish translations were updated.

.. _renpy-7.4.9:

7.4.9
=====

Android
-------

This release features major changes to Ren'Py's Android support, starting
with support for the Android App Bundle format, now required for your game
to be uploaded to Google Play.

As bundles use different signing keys than APKs, it will be necessary to
uninstall and reinstall the game when switching from APKs to Bundles
for testing.

When run on Google Play, Ren'Py will use Play Asset Delivery to deliver
the game data to the player's device. This should have the same 2 GB limit
of previous versions of Ren'Py, with each file in your game automatically
assigned to one of four 500 MB asset packs. If the games is started before
all of the asset packs have been delivered, Ren'Py will wait for delivery
to finish before starting.

A new android-downloading.jpg file is used in place of android-presplash.jpg
when Play Asset Delivery is downloading the game's assets. This screen is
overlayed with a progress bar.

Ren'Py still supports building 2GB APKs that can be sideloaded onto devices,
and supplied to other app stores.

Ren'Py now builds against version 30 of the Android SDK.

Ren'Py supports wireless debugging on Android 11 devices.

A number of questions have been removed from the Android configuration
process, simplifying the process. Most notably, Ren'Py now automatically
manages the numeric version of the package, so it's no longer required to
increment that version with each build.

Ren'Py will now look for archives in the external files directory, and
automatically use the archives if found. This makes it possible to
distribute patches, updates, and additional asset to users.

The inclusion of :ref:`Pyjnius <pyjnius>`, a library for calling
the Android API, is now documented.

The new :var:`build.android_permissions` variable, :func:`renpy.check_permission`
function, and :func:`renpy.request_permission` function provide a way to
request permissions on Android beyond those that Ren'Py users itself.

When creating Android keys, Ren'Py will back them up to the same place it
backs up script files. This isn't a substitute for making your own backups.

An issue that could cause black screenshots on Android and other platforms has
been (hopefully) fixed.

The permissions of saves and log.txt are now explicitly managed on Android
to make these files group-readable, ensuring the player can access logs and
files.

iOS
---

The iOS build process has been updated create a project that is more complete
after the initial generation, with the launch screen set up and no unused
schemas.

As always, it's necessary to create a new iOS project each time Ren'Py is
updated.

The inclusion of :ref:`Pyobjus <pyobjus>` with Ren'Py is now documented. The
Pyobjus library allows games to call APIs on iOS and macOS.


Updater
-------

The Ren'Py updater has been improved. It is now possible to download
updates over https, though doing so is less efficient, as the entire
update file will need to be download rather than just the required
changes.

It is possible to opt into a daily check for updates in the launcher
preferences. This will cause Ren'Py to check once a day for updates,
and highlight the update button if one exists.

Camera/Perspective Improvements
-------------------------------

Using the ``camera`` statement in non-trival manners, such as to apply
perspective, could cause problems with several transitions, most notably
the move transitions. This has been fixed, and so these transions should
work.

Operations that required the taking of a subsurface (for
example, the slide and wipe transitions, or the use of viewports) didn't
work when applied to a perspective transform. This has been fixed, but
it does require a render to texture operation to work, leaving it up
to the creator to decide if the performance penalty is desirable.

Accessibility
-------------

The shift+A Accessibility menu now supports enabling high contrast text, which
converts all text to light-on-black. This is intended to assist player who
need higher contrast to experience a game.

Descriptive text (the :var:`alt` character) no longer causes the dialogue
window to fade in if the descriptive text is disabled.

The order in which self-voicing reads out layers, screens, and displayables
directly on a layer has changed, such that the screen and displayables that
are drawn last (closest to the player) are read out first. This does not
apply to displayables within a screen or layout displayable, which are
still read first to last.

Modal screens cause self-voicing to stop after the contents of the screen
has been read.


Transform Properties
--------------------

The :tpref:`xsize` and :tpref:`ysize` transform properties have slightly changed
in behavior, to match the corresponding style properties. While they used to
accept only numbers of pixels, they now take "position" values, which means
either a number of pixels expressed as an ``int`` or ``absolute``, or a fraction
of the available room expressed as a ``float``. The old wrapper, :tpref:`size`,
is deprecated, and the new wrapper, :tpref:`xysize`, should be used instead.

Other
-----

The :ref:`bar <sl-bar>` screen language statement now has a new property,
`released`, that gives an action to perform when the bar is released.

It's now documented that the :ref:`key <sl-key>` screen language statement
can take a list of keysyms.

On Linux, if Ren'Py detects the "C" locale, it will enable support for
UTF-8 filesystems. This is intended to provide better compatibility with
Steam Linux, which uses this locale.

A new Polish translation of the launcher has been added.

The music room has been updated to include a TogglePause button,
that pauses and unpauses music.

There is now a --safe-mode flag, that starts Ren'Py in safe mode.

Mute now mutes movies.

An issue that caused analysis files to grow unconstrained, slowing down
Ren'Py startup, has been fixed. The analysis file will be reduced in size
when the game scripts are recompiled.

The :propref:`hover_sound` and :propref:`activate_sound` properties now
apply to bars.

When dispatching events in ATL, if an event with a ``selected_`` prefix is not
handled, the prefix is stripped and the event is matched again. This means
that a ``hover`` handler will handle the ``selected_hover`` even if the
``selected_hover`` handler does not exist, and same thing with ``selected_idle``

Ren'Py versions can now include an optional letter at the end. The ``n`` suffix
is applied to nightly builds of Ren'Py, while the ``u`` suffix is applied to
unofficial builds.

The ``default`` statement is applied after each rollback.

A regression that could prevent text in buttons from changing has been fixed.


.. _renpy-7.4.8:

7.4.8
=====

Fixes
-----

This fixes a major problem that could cause rollback to corrupt lists,
dictionaries, sets, and objects. Everyone that uses 7.4.7 is recommended
to upgrade.

A crash that could be caused by non-integer outlines has been fixed.

The correct size of a viewport is used for edge and mouse wheel scrolling.

Game controller detection has been fixed.

Features
--------

It is now possible, using :func:`PauseAction` or :func:`renpy.music.set_pause`,
to pause a channel that's playing video.

The default channel for movies can now be set with :var:`config.single_movie_channel`.

Changes
-------

When in developer mode, errors parameterizing an image will be reported to
the developer, rather than causing a placeholder (the gray ghost girl) to
appear.

The text window will not be shown before being hidden by the ``centered``
and ``vcentered`` characters.

Rolling back to a place where the shift+O console caused a change in the
state of the game will not cause the effects of the console to be reverted.
Rolling back one step further will.


.. _renpy-7.4.7:

7.4.7
=====

Web and Web Audio
-----------------

The way that the web platform plays audio has been rewritten. Instead of
using ffmpeg as Ren'Py does on other platform, the web version of Ren'Py
will hand sound files off to the browser's builtin audio player. This
is often multithreaded, and so prevents the skipping and crackling that
had been occurring with the web port.

The file formats that are supported on the web platform are now the
formats supported in browsers. This is Opus, Ogg, and MP3 in modern
web browsers, and just MP3 in Safari. (But see the Safari issues
below.)

The new :var:`config.audio_filename_callback` makes it possible to
adjust audio filenames on play, on the web and on other platforms.

Self-voicing, with the 'v' key, now works on the web platform if the
browser supports it.

Support for Ren'Py is limited on webkit-based browsers, due to
https://bugs.webkit.org/show_bug.cgi?id=227421 . This seems to affect
Safari on macOS, especially the M1, as well all web browsers on iOS. As there
is no way to fix this issue in Ren'Py, the web shell has been modified to
report the issue.

iOS
---

The iOS build is now compiled with a more modern version of Clang, allowing
it to run on the 12th generation iPhone and 2nd generation iPhone SE without
the pillarboxing (or worse, both pillarboxing and letterboxing) that
would otherwise be required.

Ren'Py can compile for the iOS simulator on M1 macs, but the simulator itself
may cause runtime issues.

Input
-----

The input displayable now supports a number of new quality of life
features. Specifically, the following new features now work:

* Jumping a word to the left. (Ctrl-Left, Alt-Left on Macintosh.)
* Jumping a word to the right. (Ctrl-Right, Alt-Right on Macintosh.)
* Deleting a word. (Ctrl-Backspace, Alt-Backspace on Macintosh.)
* Deleting the line. (Windows-Backspace, Command-Backspace on Macintosh.)

In addition, Command-Left and Command-Right on Macintosh now navigate to
the start and end of the line, in addition to the usual Home and End keys.

The input caret now blinks to draw attention. The blink rate is
controlled by the :var:`config.input_caret_blink` variable.

Other
-----

The :func:`Preferences` function can now return actions that allow
access to the renderer and accessibility menus.

The new :func:`renpy.set_focus` function makes it possible to set
the focused displayable, though mouse motions might immediately
change the focus.

In layered images, transform properties given to attributes now take
precedence to those given in groups. Previously, it was possible for
the attributes to conflict, such as when :tpref:`align` was given to the group
and :tpref:`xalign` was given to the attribute.

It is now possible to roll back past variables set in the console.

The new :func:`mark_label_seen` and :func:`mark_label_unseen` make it
possible to manipulate the set of seen labels.

The new :func:`mark_audio_seen` and :func:`mark_audio_unseen` make it
possible to manipulate the set of seen audio files.

The new :func:`mark_image_seen` and :func:`mark_image_unseen` make it
possible to manipulate the set of seen images.

ATL transforms in screens now start when first shown, rather than when the
screen containing the transform is first shown.

The new :var:`config.autosave_on_input` variabel controls if autosaving
occurs on input.

Ren'Py will now report an error when a positional argument follows a
keyword argument.

It is now possible to use floating point numbers for :propref:`xsize` and
:propref:`ysize`, and have the result be correct. Previously, the floating
point numbers would be applied twice, so a :func:`xsize` of .5 would
represent 1/4 of the available width, rather than the correct 1/2 as it
does now.

The :func:`persistent._clear` method, which clears persistent data, is now
documented.

The Spanish translation has been updated.

Atom has been updated.


.. _renpy-7.4.6:

7.4.6
=====

Camera Statement
----------------

There is a new ``camera`` statement, intended for use with the 3D Stage system.
This statement is similar to the ``show layer`` statement, except that the layer
name is not required, and it is not cleared when a ``scene`` statement is run.

This statement lets you write::

    camera:
        perspective True

to enable the 3D State system.

As part of this, the ``show layer`` and ``scene`` statements have been reverted
to their behavior in 7.4.4 and earlier, where the ``scene`` statement clears
the list of transforms.

Model Displayable
-----------------

The new :class:`Model` displayable serves as a way to create models for
use with the model-based renderer. Right now, the class is able to
create 2D models with multiple textures, making it possible to create
custom transforms that work like some of the built-in transforms do.

This displayable doesn't support 3D, yet, but that's expected in the future.

Other Improvements
------------------

The Atom text editor has been updated, and the language-renpy plugin assoicated
with it has been updated to support the new keywords introduced in recent
versions of Ren'Py.

Using a controller immediately hides the mouse cursor.

Fixes
-----

A mistake in the build process meant that a change to fix compilation
on iOS that had been in the nightly didn't make it into the Ren'Py
release.

An issue where a modal screen would not block time events when the Ren'Py
window lost focus has been fixed.

The number of iterations of the blur shader has been limited, which ensures
that Ren'Py is compatible with more webgl devices.

Ren'Py will re-compile the Python files in the renpy/ directory, when the
Force Recompile option is checked. This ensures that if those files are
recompiled for some reason, the path to Ren'Py on the creator's system
will not be included.

ATL will now skip to the first frame to be displayed when using the animation
timebase.

Ren'Py will no longer pauses without timeouts after a rollback.


.. _renpy-7.4.5:

7.4.5
=====

Model-Based Renderer
--------------------

The model-based renderer is now the default for games that are released
with Ren'Py 7.4.5. To disable it for your game, please set :var:`config.gl2`
to False.

When the model-based renderer is being used, Ren'Py now supports a "3D Stage".
This adds a third dimension to shown images, allowing for perspective correct
zooming and motion, the rotation and translation of displayables in 3D,
and many other new effects. Please see the :doc:`3D Stage <3dstage>`
documentation for more information.

To facilitate the 3D Stage, the ``scene`` statement no longer clears
transforms applied to a layer as a whole with ``show layer`` or
:func:`renpy.layer_at_list`.

The new :func:`Swing` transition is usable when the model-based renderer
is enabled. This causes the scene to rotate around the vertical or horizontal
axis, in three dimensions, and to be replaced with a previous scene.

The new :tpref:`blend` transform property allows the blend function to be
specified. The blend function controls how a pixel being drawn is combined
to the pixel it is being drawn to.In addition to the "normal" and "add" blend
functions that Ren'Py already supported, new "multiply", "min", and "max" functions
have been added.


Mouse
-----

There have been a number of changes and improvements to the hardware mouse
support, and it's now documented that GPUs have limits to the size of the
hardware mouse that can be supported.

A new variable :var:`config.mouse_displayable` and displayable,
:func:`MouseDisplayable`, now can be used to replace the hardware mouse
with a software one, similar to the way it was done in Ren'Py 7.3 and
earlier.

Features
--------

A new function, :func:`renpy.screenshot_to_bytes`, takes a screenshot
and stores it in a bytes object that can be passed to :func:`im.Data`.
While these objects are large, it is possible to store them in regular
and persistent saves.

The new :func:`renpy.music.get_loop` function returns a list of sound
files that are set to be looped on a channel, making it possible to
store and replay them.

The :func:`renpy.input` function and the input displayable take a new
`mask` parameter, that specifies a string that masks out characters
that would be shown to the player. This can be used to hide the text
of a password.

There is now a dark theme for the launcher.

The new :var:`config.adjust_attributes` callback allows you to intercept
image attributes when show, and replace them with a list of your own.
For example, it's possible to use this to rewrite ``eileen happy``
to ``eileen happy_eyes happy_mouth``, which interacts well with
LayeredImage.

When running lint from the command line, the ``--error-code`` option can
be given to cause Ren'Py to return with an error code if lint fails.

Layer transitions can now persist past the end of an interaction.

Ren'Py avoids pausing right after a rollback, so that the rollback tries
to finish at a more interactive statement.

When playing a sound, it is possible to sync the start time of an audio
file in one channel with the time of the audio file in another channel.

Android
-------

Several packages that are required to build on Android are now included
as part of Ren'Py. This fixes errors that are related to Bintray being
shut down, that prevented new installs of Ren'Py 7.4.4 from being able
to build for Android.

The way Ren'Py displays the presplash screen on Android has been
changed. The presplash is now displayed by the Java bootstrap, in
a new layer on top of the OpenGL layer. This is a new approach
compared to Ren'Py 7.4, where the presplash was displayed using SDL's
2D rendering. This change appears to improve compatibility with Android
devices, and prevent instances of black screens on start.

As part of this change, the way Ren'Py scales the presplash image has
been changed. Ren'Py will now scale-to-fit the presplash image inside
the available area.

An issue that prevented blur from working properly on certain Android
devices has been fixed.

An issue playing some less-used video and audio file formats on Android
has been fixed.

The Android fixes will require you to regenerate your Android project,
by answering the Android Configuration question "Do you want to automatically
update the Java source code?" with "Yes."

Other Platforms
---------------

The Web Platform beta has been updated.

A regression in Mobile Safari for iOS 14.5.1 and later prevents Ren'Py from
starting on that platform. As the issue is with Mobile Safari, no workaround
is possible, and a message is displayed prompting the player to contact
Apple. This regression affects other iOS browsers that are shells for Mobile
Safari, like Chrome and Firefox.

Building for iOS has been fixed.

Support for Steam on macOS has been fixed.

Signing and Notarizing macOS applications has been fixed.

Other Fixes
-----------

The default level-of-detail bias has been set to -0.5, and can be changed
with :var:`config.gl_lod_bias`. This is used to bias Ren'Py into scaling
down, rather than scaling up, but the previous bias would cause Ren'Py
to create jagged edges on images.

There have been a number of improvements to the way Ren'Py handles
modal screens.


.. _renpy-7.4.4:

7.4.4
=====

The old-game directory
----------------------

To help creators that make multiple releases of their games (as with
early access or Patreon releases), Ren'Py now supports an old-game directory,
which can be a copy of the game directory from the previous release. Ren'Py
will use the information found in the .rpyc files in this directory when it
generates .rpyc files. As the .rpyc files are used when loading games,
this will tend to help Ren'Py load games created by multiple
developers.

For more information, see the :ref:`documentation <old-game>`.

Fixes
-----

A crash that could occur with gestures or controllers has been fixed.

A crash that occurred when generating web distributions on windows has
been fixed.

The persistent backend for achievements now supports the clearing of
progress.

Live2D now resets opacities with other parameters.

Ren'Py does not change the size of a maximized window when reloading.

Other
-----

There is a new GL property, ``blend_func`` that is supported by the
model-based renderer. This allows the customization of the GL blend
function, allowing Ren'Py to start to support new blend modes.

Live2D now supports the additive and multiply blend modes.

Using default or define with the ``renpy`` namespace will now produce an
error.

A number of previously-undocumented methods on the :doc:`preferences object <preferences>`
have been documented. These methods make it possible to get or set the current value
of the volume and the current value of mute.


.. _renpy-7.4.3:

7.4.3
=====

Windows
-------

The code for changing icons has been rewritten, to produce executables that
do not include any extraneous data other than the software and the icons
being added. This should prevent some antivirus programs from producing
false positives.

Ren'Py is now linked against the Universal C Runtime on Windows. This
may raise the version of Windows that Ren'Py runs on to Windows Vista
with certain hotfixes. This both modernizes Ren'Py, and should prevent
some antivirus programs from producing false positives.

Ren'Py will now disable Threaded Optimization on Nvidia GPUs. Threaded
Optimization interacted poorly with Ren'Py, causing pauses in places where
Ren'Py did not expect pauses to occur. This could manifest as audio glitches
that this change fixes.

Ren'Py will automatically use the ANGLE library to emulate OpenGL ES using
DirectX, if DirectX is available and OpenGL is not. This had not worked
properly in Ren'Py 7.4. The window may appear and disappear multiple times
as Ren'Py tries different video systems, this is expected.

Android
-------

The non-model-based renderer now properly deallocates textures when Android
causes a render context to change. This prevents visual glitches that would
randomly occur, often during Dissolves.

Ren'Py now checks that it has focus when the game actually starts. This
fixes an issue where, if the player switched out of the application before
the game could fully start. Now, if Ren'Py has lost focus at game start,
it will save and quit, then re-launch when the player returns to the game.

In general, compatibility with Android devices has been improved.

Features
--------

Added :var:`config.main_menu_music_fadein`, a way of fading in the main
menu music.

The new :func:`renpy.get_zorder_list` and :func:`renpy.change_zorder` allow
the zorder of images and screens to be manipulated after being shown.

Windows and frames can now take the :propref:`modal` style property. This is
similar to the modal property of screens, but only applies when the mouse
is within the boundaries of the window or frame. This can be used to ensure
the player can't click a button behind the window, while allowing buttons
that are not obstructed to be used.

The :func:`Live2D` displayable now takes an `update_function` parameter,
which makes it possible to update parameters directly.

Ren'Py now supports the display of Emoji and other characters from outside
the Basic Multilingual Plane, if the fonts in use support the characters.
Right now, the emoji are displayed using the font rendering system, which
produces monochrome glyphs.

The :class:`FontGroup` class can now be used to remap characters inside
a font.

Displayables in the mask portion of a :func:`AlphaMask` are now focusable,
allowing new effects.

The player can now choose to ingore image files that cannot be loaded.

The new :func:`renpy.get_sdl_dll` and :func:`renpy.get_sdl_window_pointer`
functions make it possible to access the SDL DLL using ctypes. This may
make it possible to implement funcitonality that is in SDL, but Ren'Py
does not provide access to.

Clicking now ends a transition introduced with :func:`renpy.transition`,
or statements that have a ``with`` clause.

:func:`renpy.translate_string` is now a documented function that provides
the ability to translate a string to a selected language.

It is now possible to create a ``hide_windows`` label, that provides a way
to customize the hiding of windows that occurs when middle-clicking or
pressing the h key.

New properties, like the :tpref:`mesh_pad` transform property
and the ``gl_pixel_perfect`` gl property, make it possible to
perform pixel perfect rendering after applying a shader to text.

The :func:`renpy.input` function now takes properties beginning with
``show_``, that are passed to the ``input`` screen.

The :class:`Color` class now has an rgba property, that returns an
rgba tuple.

Old Features
------------

The :var:`default_mouse` variable was introduced in Ren'Py 7.4, as a way
to allow the mouse cursor to be changed without changing :var:`config.mouse`
at runtime, as changing config variables at runtime isn't supported.

Other Fixes
-----------

An issue that prevented multiple modal screens from being processed correctly
has been fixed. This would manifest as focus problems.

Lint now produces files with Windows-style newlines, on Windows.

SDL error messages are decoded using the system encoding on Windows, making
them more readable.

Issues with quoting unicode characters in Python have been fixed.

Values of the :tpref:`blur` transform property between 0 and 1 now work properly.

The {done} text tag now works as defined.

Ren'Py is better at checking for GL load failuires and falling back to older
libraries.

Apps built for macOS should enable HighDPI mode.

Translations
------------

The Ren'Py documentation has been translated into both Simplified and
Traditional Chinese, courtesy of 被诅咒的章鱼 and 逆转咸鱼.

The French translations have been updated.

.. _renpy-7.4.2:

7.4.2
=====

Fixes and Changes
-----------------

The new :var:`config.context_fadeout_music` and :var:`config.context_fadein_music`
variables make it possible to fade out and in music when a game is loaded or
other context changes cause the music to change.

Ren'Py now searches for Live2D motion and expression files using the
extensions (.motion3.json and .exp3.json), rather than using
directory names.

The new :var:`build.include_i686` variable determines if the 32-bit
versions of Ren'Py are included in the build. Not including 32-bit
binaries can reduced download size and prevent overzealous antivirus
programs from incorrectly reporting distributions as infected.

The new :var:`build.change_icon_i686` will prevent the icon for the
i686 version from being changed. This may prevent antivirus programs
from incorrect detections.

Ren'Py will no longer disable the screen saver or prevent the
system from going to sleep when a game is running.

A macOS issue with the operating system's fullscreen (invoked using the gree
button) disabling resizing, and hence preventing the window from being
restored to it's normal size, has been resolved.

A crash on raspberry pi displaying a webp image has been fixed.

This release fixes missing files caused by a mistake in the build process:

* The say.vbs file was missing, preventing self-voicing from working on
  Windows.
* Various files required to support ANGLE were missing, which prevented
  DirectX rendering from working.

Android
-------

There is a known issue with Samsung devices with the magnification shortcut
enabled, where the game may become unresponsive. I'm working on a fix, but
didn't want to delay the release for this.

The detection of the JVM on macOS is more robust, and less likely to
be confused by a browser plug-in.

Ren'Py now recommends the use of AdoptOpenJDK as a source for the
JVM.


.. _renpy-7.4.1:

7.4.1
=====

Pause Statement Changes
-----------------------

The behavior of the ``pause`` statement with a time has changed, so that::

    pause 1.0

is now equivalent to::

    $ renpy.pause(1.0)

and not::

    with Pause(1.0)

This means that other features that expect a real pause will work during the
pause statement.

Modal screens no longer block the ``pause`` statement, or :func:`renpy.pause()`.
this means that a pause can end even if a modal screen is displayed above it.

Say Statement Id Clause
-----------------------

The say statement has now grown an ``id`` clause, that lets you specify the
old say statement id. This is useful for changing a say statement in the
original language, such as to fix an obvious typo, without needing to
update all the translations.

To use it, just add ``id`` to the say statement, followed by the
statement id::

    e "This used to have a typo." id start_61b861a2

Live2D
------

Live2D support has has a `default_fade` argument added, which can change the
default duration of fades at the start and end of motions and expressions.

An issue with Live2D that manifested as a tuple error has been fixed.

Controller Blocklist
--------------------

The Nintendo Switch Pro Controller, when connected to a computer by
USB, requires an initialization sequence to be sent to cause it to
act as a Joystick, and not return incorrect data.

Ren'Py 7.4.0 attempted to send this sequence, but doing so required
directly accessing the USB bus, which was causing crashes and long
pauses on some computer. We've decided that this functionality is too
prone to compatibility problems to include in Ren'Py.

As a result, the Switch Pro Controller has been added to a new
controller blocklist, and will not function in Ren'Py.

macOS
-----

The minimum supported version of macOS is now 10.10 (Yosemite). Ren'Py
7.4 did not run on this version, so this represents a restoration of
support for this version.

Choosing the projects directory was broken on macOS 11.0 (Big Sur).
This has been fixed.

Pyobjus is now part of the macOS build of Ren'Py, in addition to
the iOS build. This library makes it possible to access Cocoa APIs.

Android
-------

There have been reports that prereleases of Ren'Py 7.4.1 will not run
properly on older Android devices, like the Samsung Galaxy S5. We
are attempting to acquire an example of a device exhibiting the
problem, and will make a new release as required.

Translations
------------

The Spanish translation has been updated.

Other Fixes
-----------

An issue that could cause crashes on movies of certain sizes when
Ren'Py was run on a computer that supports SSE3 has been fixed.

Movie playback now uses multiple cores for video decoding, as it
did in previous versions of Ren'Py.

An issue that could cause the size of the Ren'Py window to increase
when run on Windows with a non-100% DPI has been fixed.

Ren'Py will no longer give a performance warning when an unsupported
renderer is selected, such as when using the GL or ANGLE renderer on
a game that requires gl2.

An issue that would, in some cases, prevent say attributes from being
shown has been fixed.

An issue preventing MultiPersistent files from working on computers that
do not use UTF-8 at the default file encoding has been fixed.

The flags for compiling Python when ``rpy python 3`` is enabled have been
improved.

An issue that prevented triple-quoted strings (like the strings used for
gui.about) from being evaluated correctly has been fixed.

Ren'Py now detects its path during certain reloads.

Ren'Py will determine of all functions a renderer requires can be
dynamically loaded, and will try different renderers if this is not
the case.

Timers that are created after the start of a statement now properly
participate in the rollback system, and will fire if the game rolls
back to a point where the timer has not fired.

Ren'Py now allows the screensaver to activate while a Ren'Py game is
running.

A problem with dynamic variables not remaining dynamic during a rollback
has been fixed.

When given a size, the hbox and vbox displayables now position children
in the same way those children were positioned in Ren'Py 7.4.

The new :propref:`mipmap` style property applies to the  :func:`Dissolve`, :func:`ImageDissolve`,
and :func:`AlphaDissolve` transitions, the :func:`AlphaMask`, :func:`Movie`, and :func:`Text`
displayables, and text in general. This property controls if mipmaps are
generated for the textures created by these displayables. Avoiding creating
mipmaps may improve rendering performance on slower computers, but
can lead to artifacts when scaling down.  When not specified, this property
defaults to :var:`config.mipmap_dissolves`, :var:`config.mipmap_movies`, or
:var:`config.mipmap_text`, as appropriate.

The toggle version of self-voicing preferences have been changed to
provide a better selected state.

Lint now once again reports statistics by translation.


.. _renpy-7.4:

7.4.0
=====

Model-Based Renderer
--------------------

This release includes a new model-based renderer, the component of Ren'Py that
is responsible for drawing text and images to the user's display, supplementing
(with the intent of eventually replacing) the original OpenGL renderer added
in Ren'Py 6.10. This renderer takes better advantage of the hardware present
in modern GPUS (both dedicated graphics cards and GPUs integrated into
processors) to improve performance and increase capability. This renderer
supports desktop computers that support either OpenGL 2.2 or DirectX 9.0c or
11, and mobile devices and embedded systems that support OpenGL ES 3.

The biggest change in the model-based renderer is that Ren'Py is no longer
limited to drawing rectangular images in a 2-dimensional plane. Instead,
Ren'Py has been converted to use meshes made up of triangles in a
three-dimensional space. While existing rectangular sprites are
displayed in the same way, this opens up Ren'Py to non-rectangular
meshes, and eventually full three dimensional geometry.

In addition to mesh geometry, model-based renderering supports shaders,
both shaders included with Ren'Py, and shaders specified by creators as
part of their game. Shaders are small programs that run on the GPU, that
can process geometry and pixel data, to allow for all sorts of graphical
effects.

The model-based renderer implements a new fast texture loading system,
which moves an expensive part of texture loading, alpha
premultiplication, from the CPU to the GPU.

The model-based renderer also creates mipmaps for each texture that is loaded
into the GPU. A mipmap is a series of smaller versions of the texture,
stored on the GPU. By creating and utilizing mipmaps, Ren'Py is now able
to shrink images below 50% of the original size, without the appearance
of the aliasing artifacts. This is especially relevant when assets meant
for 4K monitors are used on 1080P and smaller displays.

For this release, the Model-Based Renderer is opt in, with that opt-in
controlled by the :var:`config.gl2` variable. As we gain more experience
with it, it is indended to be come the default Ren'Py renderer.

Live2D
------

One of the features enabled by the model-based renderer is support for
displaying sprites made in Live2D. Ren'Py requires you to download Live2D
Cubism separately, as you'll need to execute a contract with Live2D, Inc.
before distributing a game that uses their technology.

Ren'Py supports the display of Live2D models, complete with the ability to
change expression and to queue up one or more motions. This is integrated
into Ren'Py's image attribute system. Ren'Py also supports fading from
one motion to another when an attribute changes.

Matrixcolor and Blur
--------------------

The model-based renderer enables new functionality in transforms, such as
matrixcolor and blur.

Transforms (including ATL Transforms) now support a new :tpref:`matrixcolor`
property, which either a matrix or an object that creates a matrix that
changes in time, and uses it to recolor everything that is a child of the
transform.

While previous versions of Ren'Py supported the :func:`im.MatrixColor` image
manipulator, the new property is much improved. The image manipulator would
often take a large fraction of a second, making it too slow for real-time use,
and was limited to single images. The new transform property is fast enough
that it can be changed every frame if necessary, and can be applied to
any displayable. It's now possible to apply a Transform using matrixcolor
to a layer, to recolor the entire layer - making it possible to push your
game into sepia or black-and-white without needing a separate set of
images.

There are a few difference between the image manipulator and the the
transform property versions of matrixcolor, as the new version uses
4x4 matrices and premultiplied alpha color, so the new property can't
use the same matrices. Instead, there are number of new :ref:`ColorMatrix <colormatrix>`
objects that need to be used.

Transforms also support a new :tpref:`blur` property, which blurs the child
of the displayable by the given number of pixels.


Python 2/Python 3 Compatibility Mode
------------------------------------

While Ren'Py is not yet supported on Python 3, this release of Ren'Py
includes several features to allow you to begin writing scripts that will
work on both Python 2 and Python 3.

First, Ren'Py now uses `future <https://python-future.org/>`_ to provide
standard library compatibility. It's now possible to import modules using
their Python 3 names, when a renaming has occured.

When a .rpy file begins with the new ``rpy python 3`` statement, the file is
compiled in a Python 3 compatibility mode. The two changes this causes are:

* Ren'Py will compile the file in a mode that attempts to emulate Python 3
  semantics, including the change to division. In Python 3, ``1/2`` is equal
  to .5, and not 0. Since this changes the type of the expression,
  this can change the position of displayables. ``1//2`` keeps the original
  semantics.
* Ren'Py will change the behavior of dict so that the ``items``, ``keys``, and
  ``values`` methods return views, rather than lists, when called directly
  from that .rpy file. These match the Python 3 semantics for these methods,
  but need to be explicitly turned into a list before being saved or participating
  in rollback.

Upgraded Libraries and Platform Support
---------------------------------------

For Ren'Py 7.4, the build system was redone, replacing the multiple build
systems needed to build Ren'Py with a single build platform that handles
every platform except for webasm. The change in build system also involved
updating all  of the libraries that Ren'Py uses to newer versions.

As a result of this, the list of platforms that Ren'Py offically supports
has changed slightly. Here's the latest list of what is supported:

.. list-table::
    :header-rows: 1

    * - Platform
      - CPU
      - Note
    * - Linux
      - x86_64
      - Raised minimum version to Ubuntu 16.04
    * - Linux
      - i686
      - Raised minimum version to Ubuntu 16.04
    * - Linux
      - i686
      - Raised minimum version to Ubuntu 16.04
    * - Linux
      - armv7l
      - Intended to support Raspberry Pi, uses Raspian Buster
    * - Windows
      - x86_64
      - A new port to 64-bit Windows Vista and later.
    * - Windows
      - i686
      - Raised minimum version to Windows Vista.
    * - macOS
      - x86_64
      - macOS 10.10+
    * - Android
      - armv7a
      - Android 4.4 KitKat
    * - Android
      - arm64
      - Android 5.0 Lollipop
    * - Android
      - x86_64
      - Android 5.0 Lollipop
    * - iOS
      - arm64
      - All 64-bit iOS devices, iOS 11.0+
    * - iOS
      - x86_64
      - The 64-bit iOS simulator, iOS 11.0+
    * - Web
      - webasm
      - Modern web browsers

The biggest new platform that Ren'Py supports is the 64-bit Windows
platform, which means that Ren'Py is available in 64-bits on all major
desktop and mobile platforms.  The new :var:`renpy.bits` variable can
be used to determine if Ren'Py is running on a 32 or 64-bit platform,
if necessary. (For example, to set :var:`config.image_cache_size_mb` appropriately.)

The one platform that loses support in this release is 32-bit (armv7l) iOS
devices. These devices are no longer supported by Apple, and do not support
the level of OpenGL ES that Ren'Py requires.

Web
---

Ren'Py now runs significantly faster in the browser, thanks to new
compilation techniques.

A game built for the web platform can now download image and audio
files from the web server as the game is played. The download begins
when the image or sound is predicted. This can reduce the initial time
it takes before the game begins running, as well as memory usage.

When running inside a web browser on a touch-screen device, Ren'Py
will display a touch-based keyboard, to compensate for web browsers
having difficulty displaying keyboard entry for wasm-based games.

The splash screen displayed while loading can use the WebP format,
including animated WebP.

More Python modules are provided, making the Python environment closer
to native Ren'Py ports.

Support for iOS browsers was improved.

Steam
-----

It is now possible to install Steam support from the Ren'Py launcher, by
choosing "preferences", "Install libraries", "Install Steam Support".

The new :var:`config.steam_appid` variable automatically creates the
steam_appid.txt file for you. This needs to be set by a ``define`` statement,
or in a python early block.

Translations
------------

The Simplified Chinese, Japanese, and Korean translations have been updated, and now
use a unified font.

There is a new Simplified Chinese translation of the tutorial game, courtesy of
Neoteus.

Depreciations and Removals
--------------------------

As described above, Ren'Py no longer support Windows XP.

As described above, Ren'Py no longer supports 32-bit iOS devices.

The choice of downloading the Editra text editor has been removed from Ren'Py.
Editra hadn't been updated in over 5 years, and the website it was originally
distributed from has disappeared.

While not completely removed, the software renderer has been simplified and
removed as an option for gameplay. Its purposes is now limited to informing
players about issues that prevent display of graphics with a GPU-based
renderer.

Miscellaneous
-------------

Support for controllers has been improved. Repeat is now supported
on controllers, and the libraries that Ren'Py uses have been compiled
to support many of the more popular game controllers.

Ren'Py now uses software playback of movies on Android and iOS devices,
meaning the same files can be used on all platforms that support video
playback.

Defining a mouse cursor using :var:`config.mouse` now uses SDL2's color cursor
API, which generally results in hardware acceleration and reduced mouse movement
lag.

The ``define`` statement can now be used to set a key in a dictionary. ::

    # Ren'Py was started in 2004.
    define age["eileen"] = 2020 - 2004

The ``define`` statement can take += and \|=, to apply the appropriate
update operators. ::

    define config.keymap['dismiss'] += [ 'K_KP_PLUS' ]

    # This assumes endings is a set.
    define endings |= { "best" }

It is now possible to specify a relative audio channel whenever an
audio is file is played, using the new ``volume`` clause to ``play`` and
``queue``.

The new :tpref:`fit` property of transforms provides for different ways
of making an image fit size with a different aspect ratio. For example,
it can be scaled to be contained fully within the given size, or to make sure that
it completely covers the given size.

The :tpref:`xpan` and :tpref:`ypan` transform properties no longer double
the size of the displayable they are applied to, making them easier to combine
with positioning transform properties.

The :func:`renpy.input` function can now take regular expressions when determining
what is and is not allowed.

Grids now take :propref:`margin` style properties, that is applied outside the
grid, and inside a containing viewport.

Ren'Py support an {alt} text tag, that causes the text to be spoken during
self-voicing, but not displayed. It also supports a {noalt} text tag that does
the opposite.

The launcher window can now be resized if necessary. A button has been added to
the launcher preferences to restore the default size.

The new :var:`build.mac_info_plist` variable makes it easier to customize
the mac app.

The `requests <https://requests.readthedocs.io/en/master/>`_ library, is
bundled with Ren'Py, making accessing the web much easier.

Pressing PAUSE on your keyboard brings the player to the game menu, finally
giving that key a function.



.. _renpy-7.3.5:

7.3.5
=====

Fixes
-----

On desktop platforms, the presplash screen has been reworked so that it
will not cause the window to become nonresponsive if clicked.

The iOS port has been updated to include modules that have been newly
added to Ren'Py, allowing the compilation of iOS apps.

Other Changes
-------------

The ``audio`` directory, which automatically defines
names in the :ref:`audio namespace <audio-namespace>`, has been made
visible in the launcher, and is added to newly-createrd projects.

The new :var:`config.exception_handler` callback allows an application to
replace Ren'Py's exception handling system in its entirety.


.. _renpy-7.3.4:

7.3.4
=====

Fixes
-----

This release fixes major graphics glitches that were introduced in 7.3.3.

* On Windows, textures would fail to be reloaded when switching from fullscreen
  to windowed mode or vice-versa. This would cause the wrong texture to be
  displayed.
* On all platforms, graphical glitches could occur when :func:`Flatten`
  was used.

Other Changes
-------------

Dynamic images can now include "[prefix\_]" everywhere, and especially when
``add`` has been used to add a dynamic image to buttons, drags, and similar
focusable objects.

Creator-defined screen language statements may now take ``if``
statements as children.

The drag and drop system has been improved to better interact with updated
screens.


.. _renpy-7.3.3:

7.3.3
=====

Audio
-----

Ren'Py now supports an ``audio`` directory, which automatically defines
names in the :ref:`audio namespace <audio-namespace>`. This makes it
possible to have a file named ``game/audio/overture.ogg``, and play
it using::

    play music overture

The new :func:`AudioData` class allows you to provide compressed
audio data to Ren'Py, either generated programatically or taken
from a source other than a file. To support this, the Python wave
and sunau modules are now packaged with Ren'Py.

An issue with enabling the mixing of mono sound files has been fixed.
This issue caused many WAV files not to play. (We still don't recommend
the use of WAV files.)

Platforms
---------

Ren'Py is now distributed as a signed and notarized binary on the
Mac. As this process takes a very long time to accomplish, the
ability to sign macOS binaries has been removed from Ren'Py itself,
in favor of external scripts that take care of the signing and
notarization process.

The minimum version supported by the Android port has been lowered
to Android 19 (Android 4.4 KitKat).

The web port of Ren'Py has seen a number of changes:

* :ref:`Screen variants <screen-variants>` are now detected and set.
* Fullscreen support has been improved, though the user may need to click to enable fullscren.
* Leaving the web page is detected, so persistent data may be saved.
* 'game.zip' can now be renamed. 'DEFAULT_GAME_FILENAME' in index.html controls this.
* Portable HTTP requests (native+renpyweb): see https://github.com/renpy/renpyweb/blob/master/utils/asyncrequest.rpy
* Enable networking in Python web port for testing WebSockets, transparently available through the Python 'socket' module
* HTTP Cache-Control allows for smoother game updates.
* The pygame.draw module is now included, allowing Canvas support.
* WebGL compatibility has been improved.


Other Changes
-------------

During profiling conducted for the GL Rewrite project, it became
clear that the switch to framebuffer objects in 7.3.0 was the
cause of certain performance regressions. By changing how FBOs
are used, Ren'Py performance has been improved.

The :func:`renpy.input` function can now be given the name of a screen
that is used to prompt the user for input.

The creation of list, dicts, and sets inside of screen language is now
analyzed correctly. This will allow more displayables to be analyzed
as constant, improving screen performance.

The notify screen is now hidden on rollback.

The NVL mode screen indicates that it shows the window, which prevents
problems when ``window show`` is in effect.

When a :func:`Call` with `from_current` set to true occurs during a
multi-part statement (like a menu with dialogue), control is restored
to the first part of that multi-part statement (thus causing the dialogue
to be displayed).

More functions now use a tag's default layer.

The :func:`renpy.is_init_phase` function has been added.

Automatic voice now works for dialogue that is part of a menu
statement.

Support for GLES1 has been dropped. (It hadn't been used for years.)

The :func:`SelectedIf` and :func:`SensitiveIf` actions can now take
other actions as arguments.

Many BarValues now take a `force_step` argument, which forces changes to
the bar to be rounded to the nearest step value.

:func:`Frame` now allows the tile argument to be the string "integer",
which tiles the contents of the frame an integer number of times.

:func:`Character` now allows the `name` argument to be a function or
callable object when `dynamic` is true.

Translations
------------

The Korean and Spanish translations have been updated.


.. _renpy-7.3.2:

7.3.2
=====

Fixes
-----

Fix a regression in the platform variables, caused by the previous
release.

Translations
------------

Update the spanish translation.


.. _renpy-7.3.1:

7.3.1
=====

Changes
-------

Descriptive text (text that is intended to be show when self-voicing is
enabled, so that scenes can be described to the vision impared) has been
updated. Descriptive text is now accessed using the ``alt`` character
(the old ``sv`` character has been retained as an alias.) It's also now
possible to display descriptive text using a custom character, rather than
the narrator.

Ren'Py now always initializes the media playback system, so that a movie
can be played even if no audio will be played.

The `default` property of most displayables, which is used to choose a
displayable to be focused by default, has been renamed to `default_focus`
so that it does not conflict with the ``default`` statement. It also now
takes an integer, with the displayable with the highest focus number
getting focus.

The :func:`Flatten` displayable now passes positions from the child.

Seeded random number generators created with renpy.random.Random now
support rollback.

When emulating Android or iOS, the platform variables (like renpy.android,
renpy.ios, renpy.windows, and renpy.mobile) are set properly.

Renpyweb now stores the date and time that a save file was created.


Fixes
-----

This release fixes a fairly major issue that could cause screens that
interpolate text to not update, or update improperly.

This release properly runs the image prediction routine from the
image prediction thread.

A problem with the {clear} text tag has been fixed.

The :var:`config.end_game_transition`, which was not working properly
in most circumstances, has been fixed.

Translations
------------

The Russian, Korean, and Spanish translations were updated.


.. _renpy-7.3.0:

7.3.0
=====

Renpyweb
--------

Courtesy of Sylvain Beucler, Ren'Py now can generate distributions for
the the HTML5 web platforms, capable of running on modern web browsers
that support the Web Assembly standard. This is intended for small games
and demonstrations of larger games, as right now the implementation
downloads the full game to the web browser before running any of it.

Web support is marked as beta, as there are cases where problem with the
web platform (most notably, a lack of threading) cause problems such as
sound glitches if an image takes too long to load. As a result, it is
possible to have a Ren'Py game that works well on all other platforms,
but not in the web browser. As web browsers themselves improve, we will
improve our implementation and eventually remove the beta tag.

Building a web distribution can be done from the new "Web" button
on the Ren'Py launcher. The launcher now includes a small web server,
that can be used to launch the game in a creator's web browser for test
purposes.

Creator-Defined Statements
--------------------------

Ren'Py's creator-defined statements, and the Lexer objects that are
used by them, have been extended to improve the functionality in
many ways. With respect to the Lexer:

* It is now possible to ask the Lexer object to parse a single
  line as a Ren'Py statement, or all the lines remaining in the
  block as Ren'Py statements.

* It is now possible to ask the lexer to catch errors, so as to
  limit the scope of errors to a part of a creator-defined statement
  rather than the whole statement.

The :func:`renpy.register_statement` function has new arguments to enable
new functionality.

* Statement prediction can be controlled by the `predict_all` and `predict_next`
  arguments, which predict all possible next statements or take a function
  that determines what will run next, respectively.

* The new `post_execute` argument lets one specify an execute function that is
  run as the next statement - the one after the creator-defined statement.
  This allows a pattern where a statement runs, executes the block inside it,
  and then runs something after the block to clean it up. (For example, an event
  that serves as a label, and then jumps back to a dispatcher when it is done.)

* The new `post_label` argument lets one specify a function to supply the
  a label that goes after the creator-defined statement, which can function
  like the ``from`` clause to the call statement.

Ren'Py now stores the result of parsing a creator-defined statement in the
.rpyc files. While this allows for more complex syntax and faster startup,
it means that it may be necessary to force a recompile if you change a
creator-defined statement's parse function

Screen Language Improvements
----------------------------

It is now possible to supply an ``as`` clause to a screen
language displayable. This is especially useful with drags,
as it lets the screen capture the drag object and call methods
on it as necessary.

The ``on`` statement can now take a list of events.

A screen now takes a `sensitive` property, which determines if it is
possible to interact with the screen at all.

Ren'Py will now produce an error when a non-constant property follows
a Python statement, inside screen language. (This was very rare, and
almost always a mistake.)


Text Improvements
-----------------

Ren'Py now includes support for self-closing custom text tags, which
are :doc:`custom text tags <custom_text_tags>` that do not require as
closing text tag.

Ren'Py now supports three new flags that can be applied when formatting
text:

* "[varname!u]" forces the text to upper-case.
* "[varname!l]" forces the text to lower-case.
* "[varname!c]" forces the first letter of the text to upper-case, capitalizing it.


Android and iOS Improvements
----------------------------

Ren'Py now uses Framebuffer Objects on any device that claims to
support it. As a result :propref:`focus_mask` now works on Android
and iOS.

Ren'Py now produces 64-bit arm binaries for Android. These will be
required by the Google Play store later this year.

Text input on Android was rewritten again, to fix problems where the user
was unable to advance. Completion was eliminated, as it was the source
of the problems. While languages that require input methods will need
a larger rewrite to function, Ren'Py should now properly handle all direct
input keyboards.

Translations
------------

The Ren'Py launcher and sample project have been translated into Turkish
by Arda Güler.

The Ren'Py tutorial game has been translated into Spanish by Moshibit.

French, Japanese, Korean, Russian and Spanish translations have been updated for
this release.


Other Improvements
------------------

The ``side`` displayable now renders its children in the order
they are provided in the control string.

The ``say`` statement, ``menu`` statement, and ``renpy.call_screen``
statements now take a `_mode` argument, which specifies the :doc:`mode <modes>`
Ren'Py goes into when these statements occur.

The :func:`renpy.show_screen` and :func:`renpy.call_screen` functions now
take a zorder argument.

Ren'Py will now play a mono sound file with the same volume as a stereo
sound file, rather than sending half the energy to each ear.

The new :var:`config.load_failed_label` specifies a label that is jumped
to when a load fails because Ren'Py can no longer find the current statement.
This makes it possible to a game to implement its own recovery mechanism.

The new :var:`config.notify` variable makes it possible to intercept the
notification system and do your own thing.

The interface of :var:`config.say_attribute_transition_callback` has been
changed in an incompatible way, to allow sets of old and new tags to be
given.

:class:`Action` and :class:`BarValue` now support a get_tooltip method,
which allows the object to supply a default tooltip.

Fixes
-----

A problem that could cause Ren'Py to drop certain characters, especially
accent markers in Arabic, has been fixed.

The filename of the internal copy of OpenDyslexic has been changed so as
not to cause problems with copies distributed with games.


.. _renpy-7.2.2:

7.2.2
=====

Ren'Py now supports a new Accessibility menu, which can be accessed
by pressing the "a" key. This menu, which is intended to be used by
players, let's the player override the game font, change the scaling
and spacing of text, and enable self-voicing.

Ren'Py will now allow files in the public game directory
(/mnt/sdcard/Android/`package`/files/game) to override those included with the
game proper. This has been listed as a feature in 7.2.0, but didn't work
right.

Ren'Py will now include temporary image attributes in the say statements
generated as part of the translation process.

When uploading to itch.io, Ren'Py now downloads butler itself. This means
there is no longer a dependence on the location or structure of the Itch
app, as there was before.

The bar values :func:`DictValue`, :func:`FieldValue`, :func:`VariableValue`,
and :func:`ScreenVariableValue` all take a new `action` parameter, which
gives an action that is performed each time the value changes.

The rollback system has been optimized to reduce the amount of garbage
that needs to be collected.

.. _renpy-7.2.1:

7.2.1
=====

iOS Improvements
----------------

Ren'Py will now set the version field for the iOS application when generating
a project.

Ren'Py will now look for the files ios-icon.png and ios-launchimage.png,
and use them to generate the icon and launch image in the sizes required
for iOS.

Other Improvements
-------------------

The :func:`renpy.in_rollback` function returns True when in the rollback that
occurs immediately after a load. This makes it possible to use::

    python:
        if not renpy.in_rollback():
            renpy.run(ShowMenu('save'))

To display a save menu during an initial playthough, but not during loading
or rollback.

:var:`config.say_attribute_transition_callback` now exists, making it possible
to select the transition to use on a per-say-statement basis.

The new ``RENPY_SEARCHPATH`` environment variable makes it possible to
override :var:`config.searchpath` on launch.

Fixes
-----

Ren'Py has been audited to make sure that the semantics of == and != match,
whenever == was redefined.

There was a fix to problems that might occur when a transform is added
to a screen using the ``add`` statement.

The way ``extend`` processes arguments was changed to ensure that newer
arguments take priority over arguments given to the statement being
extended.

Ren'Py now properly considers the scope when comparing dynamic images for
equality. This fixes an issue that prevented some dynamic images from
updating when part of a screen.

A crash when :var:`config.save_dump` is true on macOS has been fixed.

A crash when :var:`config.profile` is true has been fixed.

Ren'Py now explicitly asks for text (as opposed to email, password, phone number
etc) input on Android when the keyboard is displayed.

An issue has been fixed that prevented roll-forward from working through a
menu statement.

Fixes a bug that prevents roll-forward through a menu.


.. _renpy-7.2.0:
.. _renpy-7.2:
.. _renpy-7.1.4:

7.2.0
=====

Menu Arguments
--------------

Ren'Py now has support for :ref:`menu arguments <menu-arguments>`. Arguments
can be passed to a choice menu as a whole, or to the individual choices within
the menu, using the syntax::

    menu ("jfk", screen="airport"):

        "Chicago, IL" (200):
            jump chicago_trip

        "Dallas, TX" (150, sale=True):
            jump dallas_trip

        "Hot Springs, AR" (300) if secret_unlocked:
            jump hot_springs_trip


Menu arguments passed to the menu itself become arguments to the screen,
except the `screen` argument which selects the screen, and the `nvl`
argument, which - if present - selects the NVL-mode menu. The arguments to
the choices become arguments to the items passed to the menu screen.

Temporary Say Attributes
------------------------

Ren'Py now supports temporary say attributes. Just like regular say
attributes, these are included as part of the say statement. However,
these temporary say attributes are reverted once the dialogue has
finished. For example, in the script::

    show eileen happy

    e "I'm happy."

    e @ vhappy "I'm really happy!"

    e "I'm still happy."

In the first line and last line of dialogues, Eileen is using her happy
emotion. The vhappy emotion is shown before the second line of dialogue,
and replaced with the previous emotion (happy in this case), before it.


Text
-----

There have been a number of text changes that affect text when a window
is scaled to a non-default size:

* The text is now aligned on its baseline, rather than at the top of
  the text. This is relevant when an absolute outline offset is
  used.

* It is now possible to choose how the outline scales when the window
  is scaled. This is done with the :propref:`outline_scaling` style
  property.

When positioning a Text object, the :propref:`yanchor` property can be
renpy.BASELINE. When it is, the anchor is set to the baseline of the
first line of the text.

Statements
----------

The new ``window auto show`` and ``window auto hide`` statements
allow :ref:`automatic dialogue window management <dialogue-window-management>`
to continue while showing or hiding the dialogue window.

The ``show screen`` and ``hide screen`` statements now take a with
clause, that works the same way it does with ``show`` and ``hide``.

The screen language ``use`` statement now can take an ``expression``
clause, that makes it take an expression rather than a literal screen
name. This allows a variable to be used when selecting the screen that
is included. See :ref:`sl-use` for more details.


Changes
-------

The new :func:`renpy.is_skipping` function reports if Ren'Py is currently
skipping.

The :ref:`input <sl-input>` displayable now takes a new `copypaste`
property, which when true allows copying with ctrl+C and pasting with
ctrl+V. This is enabled in the console and launcher.

``Preference("display", "window")`` now avoids creating a window bigger
than the screen, and will be selected if the current window size is the
maximum window size, if the size selected with :func:`gui.init` is bigger
than the maximum window size.

:doc:`Creator defined statements <cds>` now have a few more lexer methods available,
making it possible to to parse arguments, image name components, labels, and
delimited python.

The :func:`renpy.force_autosave` function takes a new argument, that causes
the autosave to block until it completes.

The :ref:`ctc screen <ctc-screen>` now takes a number of new parameters,
if required.

The new :func:`im.Blur` image manipulator can blur an image. Thanks to
Mal Graty for contributing it.

LayeredImage groups now support a ``multiple`` property, which allows
multiple attributes in the same group to be displayed at the same time.
This is useful because it allows the auto-definition function of a group
to be applied to non-conflicting images.

Ren'Py will remain fullscreen when the mouse changes desktops, and will avoid
shrinking a maximized window during a reload.

The :var:`config.allow_duplicate_labels` variable can be defined or set in an
init python block to allow duplicate labels to be defined in a game.

The :func:`Movie` displayable can now be told not to loop, and displays the
associated static image when it stops looping. It also can take an image
that is displayed before the movie proper starts.

Android Changes
---------------

The downloading of the Android SDK has been updated to fix a change in the
provided tools that prevented things from downloading.

An explicit action is now given to the keyboard, to make sure the enter
key works.

Ren'Py now uses the Amazon payment APIs when sideloaded onto a device
made by Amazon, allowing their payment system to be tested on a dual-store
APK.

Ren'Py will now allow files in the public game directory (/mnt/sdcard/Android/`package`/files/game)
to override those included with the game proper.

Fixes
------

A bug preventing Ren'Py from displaying zero or negative-width
characters (such as certain diacritics) has been fixed.

An issue that prevented Ren'Py from updating a displayable that was
added to a screen with transform properties has been fixed.

The order of drags within a drag group is now preserved when an
interaction restart occurs.



Size-changing properties like :propref:`xysize` now apply to a Drag and not
the space it can move around in.

A bug that could cause a transparent, black, or gray line to appear on
the bottom line of a screen during a dissolve has been fixed.

A regression in support for imagefonts has been fixed.

Creating a new file from the navigation menu of the launcher now works.

Menu sets now work again.

Ren'Py will no longer crash if an incomparable type is given to :func:`Function`
and other actions.

A case where rolling forward would fail is now fixed.

A problem that prevented the Steam overlay from showing up on macOS was fixed.



.. _renpy-7.1.3:

7.1.3
=====

This was a quick re-release of 7.1.2 in order to fix a single bug, which
was that a test change had been left in causing :var:`config.default_language`
to be set on initial startup.


.. _renpy-7.1.2:

7.1.2
=====

Improvements
------------

Ren'Py's screen language now support the inclusion of anonymous ATL
transforms. It's now possible to write::

    screen hello_title():
        text "Hello.":
            at transform:
                align (0.5, 0.5) alpha 0.0
                linear 0.5 alpha 1.0

The new :func:`SetLocalVariable` and :func:`ToggleLocalVariable` actions
make it possible to set variables inside used screens.

The new :var:`config.menu_include_disabled` variable determines if menus
should include entries disabled by an if clause.

Shift-keybindings (like Shift+I and Shift+R) now work in the Android
emulation mode.

Ren'Py now better reports errors in text tags that require a value but are
not given one.

The new :var:`_version` variable indicates the version of the game itself
that was used when a new game is first created. This only stores the version
at game creation - after that, it's up to the creator to keep it updated.

The :func:`Movie` displayable now supports a new mode the color data and
alpha mask data are placed side-by-side in the same file. This prevents
issues where a main and mask movie could go out of sync.

The :func:`FilePageNext` and :func:`FilePagePrevious` functions now take
arguments that control if the they can bring the player to the auto or
quick save pages.

The new :var:`config.skip_sounds` variables determines if Ren'Py will skip
non-looping audio files that are played while Ren'Py is skipping.

Translations
------------

Ren'Py now has the ability to automatically detect the locale of the user's
system, and use it to set the language. Please see
:var:`config.enable_language_autodetect` and the :ref:`Translation <translation>`
documentation for how this works.

The French, German, Korean, Russian, and Simplifed Chinese translations
have been updated.

Fixes
-----

A Windows-specific bug that caused RTL (the support for languages like
Arabic and Hebrew) to corrupt the second half of text strings has been
fixed. This should prevent garbage characters from being displayed when
rendering those languages.

Ren'Py will now report an error if a game accesses an image that does not
exist, but has as a prefix an image that does exist. Before this change,
if ``eileen happy`` exists and ``eileen happy unknown`` was shown, the
additional attribute would be ignored.

Lint has been improved to deal with images that take attributes that are
not in the image name, like layered images.

Ren'Py generates choice menu images that are suitable for use on the phone.

Android Fixes
-------------

As Ren'Py's new Android support only worked well on a 64-bit version of
Java 8, we make that 64-bit requirement explicit.


.. _renpy-7.1.1:

7.1.1
=====

.. _history-7.1.1:

History Fix
-----------

This release fixes an issue with Ren'Py's history screen. The problem occurred
when a line of dialogue contained a quoted square bracket, so something like::

    "I [[think] I'm having a problem."

When this occurs, the string "I [think] I'm having a problem." is added to
the history. Ren'Py would then display that in history, substitute the
``think`` variable, and crash.

This is fixed by adding ``substitute False`` to the history screen. This
is done to new projects, but for existing ones you'll need to make the fix
yourself. Here's the new history screen::

    screen history():

        tag menu

        ## Avoid predicting this screen, as it can be very large.
        predict False

        use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

            style_prefix "history"

            for h in _history_list:

                window:

                    ## This lays things out properly if history_height is None.
                    has fixed:
                        yfit True

                    if h.who:

                        label h.who:
                            style "history_name"
                            substitute False

                            ## Take the color of the who text from the Character, if set.
                            if "color" in h.who_args:
                                text_color h.who_args["color"]

                    $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                    text what substitute False

            if not _history_list:
                label _("The dialogue history is empty.")


The new lines are the ones with ``substitute False`` on them. You'll want to make
this change to your history screen to prevent his problem from happening.

Android Improvements
--------------------

Ren'Py now sets the amount of memory used by the Android build tool to
the Google-set default of 1536 megabytes. To change this, edit
rapt/project/gradle.properties. To make sure you're capable of building
larger games, please make sure your computer has a 64-bit version of Java 8.

Ren'Py explicitly tells Android to pass the Enter key to an input.

Ren'Py now crops and sizes the icon correctly for versions of Android below
Android 8 (Oreo).

Ren'Py gives a different numeric version number to the x86_64 apk. This will
allow both x86_64 and armeabi-v7a builds to be uploaded to Google Play and
other stores, rather than having to first created one build and then the other,
manually changing the version numbers between.

Other Improvements
------------------

Ren'Py now handles the (lack of) drawing of zero width characters itself, preventing
such characters from appearing as squares in text if the font does not support
the zero width character.

Ren'Py supports the use of non-breaking space and zero-width non-breaking space
characters to prevent images in text from being wrapped.

Ren'Py supports the a new "nestled-close" value for the `ctc_position` parameter
of :func:`Character`. This value prevents there from being a break between the
click-to-continue indicator and the other lines.

Drags (in drag-and-drop) now support alternate clicks. (Right clicks on desktop
and long-clicks on touch platforms.)


Fixes
-----

The :func:`SetVariable` and :func:`ToggleVariable` functions have been extended
to accept namespaces and fields. So it's now possible to have actions like
``SetVariable("hero.strength", hero.strength + 1)`` or
``ToggleVariable("persistent.alternate_perspective")``.

Automatic management of the dialogue window (as enabled by the ``window auto``
statement) now considers if an in-game menu has a dialogue or caption associated
with it, and handles that appropriately.

The source code to the embedded version of fribidi that Ren'Py is expected
to build with is now included in the -source archive.

There have been a number of fixes to the voice sustain preference to make
it work better with history and the voice replay action.

.. _renpy-7.1:

7.1
===

Android
-------

This release sees a major rewrite of Ren'Py's support for Android to
modernize it. This is required so Ren'Py games can be uploaded to the
Google Play store. Some of these changes may require you to update
a game's files. Most notably, the format of icons has changed, so the
icons will need to be redone.

The minimum version of Android that Ren'Py will run on has been raised
to Android 19 (aka 4.4 KitKat), while it targets Android 28 (aka 9 Pie).

The x86_64 architecture has been added, while x86 has been dropped. (Some x86
devices may be able to run the arm platform version through binary translation
layers.)


Monologue Mode
--------------

It's now possible to write multiple blocks of dialogue or narration at
once, using triple-quoted strings. For example::

    e """
    This is one block of dialogue.

    And this is a second block.
    """

will create two blocks of dialogue. See :ref:`monologue-mode` for more
info.

There is also a new {clear} text tag that works with monologue. When
the {clear} tag is part of a line by itself, it is the equivalent of
the ``nvl clear`` statement. See :ref:`NVL Monlologue Mode <nvl-monologue-mode>` for more
about this.


Say-With-Attribute Change
-------------------------

There has been a change to the way a say-with-attributes is handled
when there is not an image with the tag displaying. Previously, Ren'Py
would use the attributes given in the most recent say-with-attributes statement
to selected the side image to show.

Now, Ren'Py will use the provided attributes and existing attributes to resolve
the side image. This makes a say-with-attributes that occurs when an image
is not showing work the same way as when it is. When the attributes do not
select a single side image, Ren'Py will select the image with all of the given
attributes, and the most possible of the existing attributes.

The rationale for this change is to help with side images that are defined
as layered images, where providing only the attributes that change makes
sense.

Updater Changes
---------------

The updater for Ren'Py itself now asks you to select the update channel
each time you go to update. The purpose of this is to make it clear
which channel you're updating to each time you update, so you don't
accidentally update to a prerelease or nightly version after a
release comes out.

As part of this, you might see the Prerelease channel missing for some
updates. That's normal – unlike in previous versions, the channel only
appears when there are prereleases available.

Translations
------------

The Ren'Py launcher, template game, and The Question have been translated
into the Latin script of Malay by Muhammad Nur Hidayat Yasuyoshi.

The Korean translation has been significantly updated.

It is now possible to translate the strings used by RAPT into non-English
languages.

Other
-----

Ren'Py can now automatically save the game upon quit, in a reliable
fashion. (As compared to the previous autosave, which could fail or
be cycled out.) This is controlled by the :var:`_quit_slot` variable.

File actions (like :func:`FileSave`, :func:`FileLoad`, and :func:`FileAction`)
can now take a slot=True argument. When this is given, the action loads
a named slot, without involving the page.

The developer menu (accessed through Shift+D) can now display a screen
that shows the attributes associated with displayed and hidden images.

Added :func:`renpy.transform_text`, a function to transform text without
touching text tags or interpolation.

Buttons created using the ``make_buttons`` method of a Gallery object now
inherit from the empty style, and not button. This prevents properties from
the button style from causing problems.

The code to finish displaying text is now called from the event method,
as if the mouse button was clicked. This helps prevent interaction ends
when menus are up.

Displayable prefixes are supported when evaluating auto images in imagebuttons
and image maps.

A bug that caused an error in an NVL-mode statement if the next statement
was an NVL-mode statement with an undefined character name has been fixed.

When two ATL transforms are nested, the state from both is propagated, not
just the outermost.

Ren'Py now updates dynamic images that are used in windows, bars, and
frames. (And derived displayables, like buttons and imagemaps.)

An issue that caused Ren'Py to consume 100% of a core when modal True was
given has been fixed.

Ren'Py now includes a copy of fribidi, rather than requiring an OS-installed
version.

The new :propref:`box_wrap_spacing` allows control of the spacing between
rows or columns introduced by :propref:`box_wrap`.

The :propref:`adjust_spacing` style property can now take "horizontal" and
"vertical" as values, causing text spacing to be adjusted in only the
specified direction.

LayerdImageProxy can now take an interpolated string.

The new :var:`config.context_callback` is called when starting the game or
entering a new context, like a menu context. It can be used to stop voice
or sounds from playing when entering that context.

The :func:`Drag` displayable (and the screen language equivalent, ``drag``)
have grown a new `activated` property. This is callback that is called when
the user first clicks the mouse on a drag. (Before it starts moving.)


.. _renpy-7.0:

7.0
===

Ren'Py 7.0 marks the completion of over a decade of development since
Ren'Py 6 that brought features like ATL, Screen Language, OpenGL and DirectX
acceleration, support for the Android and iOS platforms, Translation,
Accessibility, and so much more.

For releases between 6.0 and 7.0, see the other entries in this changelog,
and the older changelog on the Ren'Py website. The rest of this entry
contains the differences between 7.0 and 6.99.14.3.

Layered Images
--------------

A :doc:`layered image <layeredimage>` is a new way of defining images
for use in Ren'Py. It's intended to be used with a sprite that has been
created in Photoshop or some other program as a series of layers.
The layered image system can use the attributes the image was displayed
with and Python conditions to determine what layers to display.

Layered images are intended to be a replacement for the use of :func:`Composite`
and :func:`ConditionSwitch` to define layered images. It includes a language
that makes defining such images simpler, and Ren'Py can generate portions
of the definitions from appropriately named files. It also integrates better
with the rest of Ren'Py, as attributes can be predicted in ways that a
ConditionSwitch cannot, and layered images work with the interactive director.

Dict Transitions
----------------

:ref:`Dict Transitions <dict-transitions>` makes it
possible to use the with statement and certain other functions to apply
transitions to one or more layers. Ren'Py will not pause for these
transitions to occur. Dict transitions make it possible – and even
convenient – to have a transition apply to the sprites alone while dialogue is
being displayed.

Changes
-------

The old tutorial and old templates are no longer included with Ren'Py.
They can still be used with new version of Ren'Py if copied into
this or later versions.

The new :func:`Scroll` action makes it possible to have buttons that
change the position of a viewport or the value of a bar.

The :func:`Dissolve`, :func:`ImageDissolve`, and :func:`AlphaDissolve`
transitions now respect the alpha channels of their source displayables, as
if given the ``alpha=True`` argument. As omitting the alpha channel is no
longer an optimization, this change allows the same transitions to be
used in more places.

Automatic image definitions now take place at init level 0, rather than
an init level of greater than 999. This allows :func:`renpy.has_image` to
be used in ``init`` blocks.

The interactive director now has a button that allows you to choose if it
is displayed at the top or the bottom of the screen.

The :ref:`screen language for <sl-for>` statement now takes an index clause::

    for i index i.name in party:
        ...

When provided, it should return a unique value that can map information like
button and transform state to the object it originates from.

There is now alternate ruby text, allowing two kinds of ruby text
to be displayed at once (such as a translation and pronunciation guide).

The new :ref:`displayable prefix <displayable-prefix>` system make it possible to define your
own displayables that can be accessed using strings, the same way that
images, image files, and solids have a string form.

Ren'Py now supports creating .zip files that have single files (such as
.rpa files) that are larger than 2GB. As this requires the use of the
Zip64 standard, unpacking such files may not be supported on some platforms,
most notably Windows XP.

The new :func:`renpy.get_hidden_tags` function returns the set of tags that
have attributes but or otherwise hidden, while the :func:`renpy.get_showing_tags`
function can return a list of tags in sorted order.

Showing a movie sprite a second time will now replay the movie from the start,
for consistency with ATL and other animations.

The documentation has received an editing pass, courtesy of Craig P. Donson.

Translations
------------

The Ren'Py tutorial and The Question now have French translations, thanks
to Alexandre Tranchant.

The Japanese and Russian translations have been updated.

Fixes
-----

This fixes a regression that prevented screens from handling the hide or
replaced events when the screen was not being shown. (This might be the
case when the player is skipping through the game.)

An issue that caused the interactive director to be translated into
Russian when the default (English) language was being used has been
fixed.

The :func:`Composite`, :func:`Crop` and :func:`Tile` displayables are now
actually available under their new names.

An issue that could cause Ren'Py to roll back to an incorrect place when
accessing the console has been fixed. This could cause the console to
display incorrect data, while in the console itself.

Older Changelogs
================

The changelogs for some Ren'Py 6 versions can be found :ref:`here <changelog-6>`,
with older changelogs being found at:

    https://www.renpy.org/dl/6.10.2/CHANGELOG.txt
