=======================
Changelog (Ren'Py 7.x-)
=======================

.. _renpy-7.5.0:
.. _renpy-8.0.0:

7.5 / 8.0
=========

ATL
---

It's now possible to include a block as part of an ATL interpolation.
This means that::

    linear 2.0:
        xalign 1.0
        yalign 1.0

is now allowed, and equivalent to::

    linear 2.0 xalign 1.0 yalign 1.0

Information about :ref:`ATL Transitions <atl-transitions>` and :ref:`Special ATL Keyword Parameters <atl-keyword-parameters>`
has been added to the documentation.

Image Gallery
-------------

The :class:`Gallery` class now has a new field, `image_screen`, that can be
used to customize how gallery image are displayed.

The :func:`Gallery.image` and :func:`Gallery.unlock_image` methods now
take keywork arguments beginning with `show\_`. These arguments have the
`show\_` prefix stripped, and are then passed to the Gallery.image_screen
as additional keyword arguments. This can be used to include additional
information with the images in the gallery.

ChromeOS
--------

When running as an Android application on a ChromeOS device, the "chromeos"
variant will be selected.

Boxes, Grids and Vpgrids
------------------------

A :ref:`showif <sl-showif>` statement inside a :ref:`vbox <sl-vbox>` or :ref:`hbox <sl-hbox>`
will not be surrounded with :propref:`spacing` when the condition is false and the child
displayable is not shown.

Having an overfull vpgrid - when both ``rows`` and ``cols`` are specified - is now
disallowed.

Having an underfull vpgrid now raises an error unless the warning is opted-out using
either the ``allow_underfull`` property or :var:`config.allow_underfull_grids`, the
former taking precedence on the latter.

A vpgrid with both cols and rows specified is underfull if and when it has less than
rows \* cols children. A vpgrid with either cols or rows specified is underfull if and when its number of
children is not a multiple of the specified value.

Features
--------

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

The :propref:`focus_mask` style property now defaults to None for drag displayables.
This improves performance, but means that the displayable can be dragged by
transparent pixels.

Other changes
-------------

The :propref:`activate_sound` plays when activating a drag displayable.

The :func:`VariableValue`, :func:`FieldValue`, and :func:`DictValue` Bar Values
can now call :func:`Return`, to cause the interaction to return a specific value.

The :propref:`adjust_spacing` property is now set to False for dialogue and
narration in new games. This might cause the spacing of text to change, when
the game is resized, in exchange for keeping it stable when extend is used.

Playing or stopping music on a channel now unpauses that channel.

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

The inclusion of :ref:`Pyjnius <pyjinus>`, a library for calling
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
and many other new effects. Please see the :ref:`3D Stage <3dstage>`
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

A number of previously-undocumented methods on the `preferences object <preference-variables>`
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

When a .rpyc file begins with the new ``rpy python 3``, the file is compiled
in a Python 3 compatibility mode. The two changes this causes are:

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

    define config.keymap['dismiss'] = [ 'K_KP_PLUS' ]

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
to the first part of that multi-part statement (thus causing the dialouge
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
are :ref:`custom text tags <custom-text-tags>` that do not require as
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
statements now tak a `_mode` argument, which specifies the :ref:`mode <modes>`
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

:func:`Preference("display", "window")` now avoids creating a window bigger
than the screen, and will be selected if the current window size is the
maximum window size, if the size selected with :func:`gui.init` is bigger
than the maximum window size.

:ref:`Creator defined statements <cds>` now have a few more lexer methods available,
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

A :ref:`layered image <layered-images>` is a new way of defining images
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
