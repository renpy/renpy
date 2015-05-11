==============
Full Changelog
==============

Ren'Py 6.99.4
=============

The Ren'Py script language now includes a new :ref:`default statement <default-statement>`.
This statement sets a variable to a value a default value at game start or load,
if the variable is not defined. This makes it possible to initialize saved
variables near the relevant code, rather than all at once at label start.

The screen language :ref:`use statement <sl-use>` now takes a block, which
can be transcluded into a screen using the ``transclude`` statement. This makes
it possible to use statements to "wrap" a block of screen language code.

The screen language also supports :ref:`creator-defined statements <creator-defined-sl>`,
which are transformed into use statements. These make it possible to extend the
screen language syntax.

Ren'Py now logs errors importing the steam module to log.txt.

There are a number of improvements to iOS support, to support passing Apple's
package verification process.

The launcher now checks that the version of rapt and renios match the version
of Ren'Py proper.

Fixes
-----

Fixed a performance problem caused by failing to release the Global Interpreter
Lock while waiting for event input. This could cause problems running various
background threads, like the image preloader and autosave.

Ensured that screens are only analyzed once as the game starts. Previously,
screens could be analyzed multiple times as the styles and languages were
set, leading to excessive startup times, especially on mobile platforms.

The volume curve has been changed to be more correct and perceptually
accurate. The previous curve had serveral problems, most notably that
is sharply jumped from 0 to 10%. This may require players to adjust their
volume settings.

The gallery slideshow timer now repeats through multiple images.

Text blits are now expanded to include an outline on a descender on the
bottom row of text.

Drags outside of a draggroup can now be snapped into place.


Ren'Py 6.99.3
=============

Removed debugging code that could cause problems by writing an unnecessary
zipfile.txt file.


Ren'Py 6.99.2
=============

Ren'Py now supports an images directory underneath the game directory.
Images found inside this directory - or in subdirectories of this directory - will
be automatically defined as images in Ren'Py. This will likely render the use of
the image statement obsolete in simple games.

The new :func:`AlphaMask` displayable allows one displayable to be masked by the alpha
channel of another.

The android and iOS emulators now emulate the onscreen keyboard.

The achievement API has been changed somewhat, but only with respect for
progress functions. (Which were broken in the previous releases.)

Actions that care about the current screen (like SetScreenVariable) now work
when used with the hovered and unhovered properties.

The updater has improved. If an incremental download fails, Ren'Py will try
downloading the complete file before giving up.

When building for Android, Ren'Py will copy the apk files in to the dists
directory used by the desktop platforms.

Added the :func:`RestartStatement` action.

Added the :func:`renpy.reset_physical_size` and :func:`ui.screen_id` functions.

Allowed the screen language key statement to take the activate_sound style
property. This makes it easier to play a sound when a key is pressed.

Documented :func:`ui.interact`.

Updated the Simplified Chinese and Korean translations, and the Italian template.


Ren'Py 6.99.1
=============

Added the :func:`renpy.load_image`, :func:`renpy.load_surface`, and
:func:`renpy.get_showing_tags` functions.


Ren'Py 6.99
===========

SDL2
----

Ren'Py is now based on Pygame_SDL2, a reimplementation of the Pygame API
based on the SDL2 library. One of the largest changes in Ren'Py's history,
switching to SDL2 lays the groundwork for many improvements, in this
and future releases.


iOS Support
-----------

Ren'Py now supports the iOS platform. To develop for iOS, you will need a
Macintosh computer, Xcode, and a paid membership in the iOS developer
program. (An iPad or iPhone to test with is highly recommended.)

Ren'Py's iOS support includes the ability to create Xcode projects, and
to update those projects with the latest version of a Ren'Py game. Xcode
can be used to change project settings, and to create debug and release
builds.

The iOS port supports iOS 7 and higher. Almost all of Ren'Py is supported,
with the exception being that video playback is limited to fullscreen video
in formats the iOS device supports.

For now, the default set of Ren'Py screens are not particularly compatible
with iOS. You will need to customize your game to make it touch friendly and
compliant with Apple's guidelines before submitting it to the iOS app store.

Please see the iOS documentation for more information and a copyright
notice you must include as part of your app description on iOS.


Android Support
---------------

Android support has been rewritten, and is now based in SDL2. This release
brings Android support to parity with desktop platforms. Improvements
include:

* Support for rotating the screen to match the user's preferred orientation.
* Improved in-app purchase support, with the ability to retrieve prices and
  create a single .apk that supports the Google and Amazon stores.
* Android audio playback is now based on the same code that's used on
  the desktop and iOS platforms. This enables support for features like
  panning and fading volume. It also means the same sound files can be
  used on Android, iOS, and desktop platforms.
* Keyboard input is now supported on Android.
* Languages requiring bidirectional text (like Arabic and Hebrew) are supported
  on Android.

A number of issues with Android support have been fixed, including one that
prevented Ren'Py from unzipping the android SDK automatically when the path
to the Ren'Py install was too long.

Please see the Android documentation for more information and a copyright
notice that should be included as part of your app description.


Steam
-----

Ren'Py now ships with Python bindings for the steam API. These bindings
are built as part of the Ren'Py build process, which means they will be
maintained alongside Ren'Py going forwards.

For an explanation of how to use the Steam API, please contact the Ren'Py
developers directly. The bindings make available:

* Initialization.
* User statistics and achievements.
* Retrieving other apps by the same developer that have been installed.
* DLC support.
* The in-game overlay, including the ability to launch a purchase flow.
* Session tickets.

The steam bindings will be integrated with Ren'Py as appropriate. For now,
this integration consists of binding the steam achievement system to the new
Ren'Py achievement API.


Distribution Improvements
-------------------------

The launcher now has the ability to add from clauses to call statements,
automatically turning::

    call dayplanner

into::

    call dayplanner from __call_dayplanner

From clauses, which are really labels, help Ren'Py to find the return
site to use when a game is changed. This should help fix problem with games
that may change greatly between releases.

When asked to package a game that is more than about 2GB in size, Ren'Py
will produce a ZIP64-format archive. These archives may be less compatible
that smaller zip files.


Languages and Translations
--------------------------

There is now a Russian translation of the tutorial game, and a Finnish
translation of the launcher.

Ren'Py supports input methods (IMEs) on platforms where SDL2 makes that
support available. (All platforms except for Linux.) Input methods make
it possible to input complex non-ASCII text, such as Chinese, Japanese,
and Korean.


Clipboard Voicing
-----------------

Ren'Py now supports clipboard voicing, which is accessed by shift+C.

Clipboard voicing is a form of self-voicing that works by copying the
text to the clipboard, where a screenreader program is likely to read
it using settings preferred by the player.


Custom Text Tags
----------------

Ren'Py snow supports a new form of :ref:`custom text tags <custom-text-tags>`.

Custom text tags are applied after the text has been tokenized into tags and
text. This makes it easier to write a custom text tag that manipulates text
or applies multiple existing text tags to text.

The previously-existing form of custom text tag has been renamed to
style text tag, and is still supported.


Other Improvements
------------------

A high-level achievement API has been added to Ren'Py.

Ren'Py now includes support for recognizing touch gestures on Android and
iOS.

It is possible to hide the editing buttons in the launcher, so they can't
be used to open an absurd number of editor windows.

The developer can choose if strings should be empty when generating
translations.

Three new set manipulation actions :func:`AddToSet`, :func:`RemoveFromSet`,
and :func:`ToggleSetMembership` manipulate sets and lists-as-sets. (Such
as inventory lists.)

Drags (as in, drag-and-drop) now support the focus_mask style property.

The complexity of the style system has been reduced, decreasing memory
usage and startup time.

The new :func:`renpy.suspend_rollback` suspends the recording of rollback
checkpoints, while still allowing rollback to occur.

The RENPY_GL_CHECK_ERRORS controlls the logging of OpenGL/ANGLE function
calls and errors.

A completion progress indicator can be toggled by typing shift-alt-P or
swiping up-down-left-right-left-right.

As of this release, dictionary and set comprehensions are wrapped to
support rollback.


Ren'Py 6.18.3
=============

This release adds the :ref:`showif statement <sl-showif>` to screen language.
The showif statement shows and hides its children based on a condition. When
its children are ATL transforms, showif delivers ATL events to manage the
show and hide process.

Ren'Py's image prediction mechanism now models the return stack, and can
predict images through a call and return pair. Previously, a call followed
by a return would block image prediction.

Ren'Py now predicts that the start label will be called from the main menu.
This will help to avoid unpredicted image loads at the very start of a game.

The ATL on statement now can take a comma-separated list of event names.

The new :func:`updater.UpdateVersion` function contacts an update server and
determines if an update is available.

The new :func:`renpy.invoke_in_thread` function runs a function in a background
thread, and restarts the interaction when that thread finishes.

While in self-voicing mode, the {w} and {p} tags are ignored.

The Traditional Chinese and Russian translations have been updated.

Bug Fixes
---------

Fixed a regression that could cause hiding transforms to skip time.

Fixed a bug that would cause the screen language if statement to show
children from blocks with a false condition, if those child blocks were
run during prediction.

Fixed an issue where SetScreenVariable and ToggleScreenVariable were
declared as pure functions, but weren't. They now have been reimplemented
as pure functions.

Fixed an issue where a grab could fail to transfer between interactions,
leaving Ren'Py unresponsive.


Ren'Py 6.18.2
=============

The define statement can now take a store name, and the say statement
will search the ``character`` store before searching the default store.
This means that if one uses::

    define character.e = Character("Eileen")

Say statements like::

    e "Hello, world."

will continue to work, even though ``e`` has been freed up for other
purposes.

The default image cache size (set in :var:`config.image_cache_size`) has
been increased from 8 to 16 screens worth of images.

When set to True, the new :tpref:`crop_relative` transform property tells
a Transform to interpret float components of its :tpref:`crop` property
relative to the width or height of its transformed child, as appropriate.
For example, (0.5, 0.0, 0.5, 1.0) will cropout the lower-right quadrant
of the child.

When set to false, the new :propref:`keyboard_focus` style property hides
buttons, bars, and imagemap hotspots from the keyboard focus mechanism.

The :ref:`mousearea` screen language statement now respects the
:propref:`focus_mask` style property, making it possible to have
non-rectangular mouseareas.

Ren'Py now includes functions that can be used to profile
the memory consumption of a game, including the memory consumption of
Ren'Py itself. These functions are :func:`renpy.profile_memory` and
:func:`renpy.diff_memory`. The new :func:`renpy.profile_rollback`
lets one more specifically see the memory consumption of the internal
rollback log.

When self-voicing mode is enabled, Ren'Py displays a notification that
explains how to disable self-voicing mode.

This release fixes a subtle bug caused by incorrect analysis of for
loops in screen language screens, when the iteration variable is a
constant. (For example, when the iteration variable is ``define``\ed
somewhere else in the game.)

This release adds Traditional Chinese translations of the launcher and
template game, contributed by Civalin.

Ren'Py 6.18.1
=============

This release includes a new :func:`Placeholder` displayable, which can be
used to display placeholder characters. Placeholders are now used when
displaying images that are not defined.

The new :var:`sv` Character-like object can be used when self-voicing is
enabled to display (and hence speak) descriptive text.

ATL transforms in screens now begin executing when first shown. Previously, ATL transforms
began executing when the screen containing the ATL transform was first shown,
which meant that if the transform changed over the course of screen display,
a portion of the new transform would be skipped.

This release includes a German template contributed by NoJoker.


Ren'Py 6.18
===========

Screen Language Improvements
----------------------------

This release includes a new implementation of screen language that has the
potential to be much faster than the original implementation of screen language.
Where the original screen language evaluated screens from scratch at the start
of each interaction, this new implementation can incrementally reuse large
portions of a screen between interactions. Please see the new
:ref:`Screen Language Optimization <screen-optimization>` documentation for
information on how to maximize screen language performance.

Of special note is that screens now perform better when defined with a parameter
list. Screens that do not expect parameters should be defined with an empty
parameter list.

To support improved optimization, when the screen language use statement
calls a screen with a parameter list, only variables in that parameter list
are updated. (This is a change in previously-undocumented behavior.)

Screens now support passing properties to a displayable from within an if
statement, provided the if statement is the first thing inside the
displayable. For example::

    text "Eileen":
         if eileen_mad:
             color "#fcc"
         else:
             color "#cfc"

now works.

As there is now a larger benefit from predicting screens, screen prediction
has been improved in several ways:

* By default, Ren'Py will now use the arguments supplied to a screen in
  the ``show screen`` and ``call screen`` statements to predict the
  screen. This is potentially dangers, as it means that if either statement
  has side effects, those side effects will occur as part of screen prediction.
  To mitigate this problem, both statements now take a ``nopredict`` clause
  that prevents screen prediction.

* Ren'Py will now attempt to predict images inside if clauses that would
  not be taken, and will ignore errors that occur during statement prediction.

* A pair of functions, :func:`renpy.start_predict_screen` and
  :func:`renpy.stop_predict_screen` allows for manual prediction of time
  images that will be used by screens, including parameterized screens.

Ren'Py now supports profiling of screens, via the :func:`renpy.profile_screen`
function.

Ren'Py has been changed to make a copy of the screens being displayed before
a transition occurs. This makes it possible to use a transition to show
screen updates. For example, one could increase the value displayed
by a bar, and then use the dissolve transition to dissolve in the new
segment of bar.

Image Prediction
----------------

Ren'Py now has a supported mechanism for manually predicting images in
cases where automatic image prediction fails. This mechanism consists
of two functions: :func:`renpy.start_predict` starts prediction of images,
while :func:`renpy.stop_predict` stops prediction.

Accessibility
-------------

Ren'Py now includes support for self-voicing, a mode in which Ren'Py will
read on-screen text to vision impaired players. To activate self-voicing,
press the ``v`` key.  For more information, please read the :ref:`self-voicing <self-voicing>`
documentation.

The new :propref:`alt` style property allows one to supply alternative
text that allows Ren'Py to voice imagemap components and buttons with
incomplete names.

The Ren'Py launcher now includes a large-text mode that can be accessed from
the preferences page. This mode increases text size and contrast.

Android In-App Purchasing
-------------------------

This version of Ren'Py includes a high-level interface that supports
in-app purchasing on the Android platform. This interface currently
support Google Play and the Amazon App Store.

Pixel Art
---------

Ren'Py supports nearest-neighbor filtering of images. This ensures that
screen pixels correspond to a single texture pixel, which is the scaling
mode preferred for use with pixel art. Nearest-neighbor mode is enabled
with the new :tpref:`nearest` transform property.

The new :func:`config.adjust_view_size` callback makes it possible to
set the size of the Ren'Py viewport to something other than the size of
the window (or screen, in fullscreen mode). For example, a game can use
this callback to limit its viewport size to integer multiples of its
native size.

Voice Improvements
------------------

Voice volume is now adjustable on a per-character basis, using the
voice_tag argument to :func:`Character` and the new :func:`VoiceVolume`
value.

Using the new :var:`config.emphasize_audio_channels` variable, Ren'Py
can emphasize audio on some channels. This is doen by lowering the
volume of non-emphasized channels when a emphasized channel is playing,
and returning the volumes to normal when no emphasized chanels are
playing. By setting this variable to ``[ 'voice' ]``, the voice
channel can be emphasized over music and other sounds,


OS X Bug Workaround
-------------------

To workaround a bug in Mac OS X 10.9, Ren'Py will now always open on the
the primary monitor of a Macintosh.

Other
-----

With some limitations, non-ASCII characters can now be used as character
names. Since Python code does not allow non-ASCII identifiers, such character
names must be defined by the define statement, and used outside Python code.

The `auto` property of imagebuttons and imagemaps now can take image names
as well as image filenames.

The new :func:`renpy.image_exists` function returns true if an image has
been defined.

Gallery navigation can now be customized by customizing the ``gallery_nav``
screen.

The new :func:`renpy.count_dialogue_blocks` and :func:`renpy.count_seen_dialogue_blocks`
return the total number of dialogue blocks and the number of dialogue blocks that have
been seen by the current user in any game. With some caveats, these can provide an
indication of how much of the game the user has seen.

The :var:`config.autosave_on_choice` variable determines if Ren'Py will
autosave on choice, while the :var:`config.autosave_on_quit` variable
determines if Ren'Py will autosave when the game is about to end (by quit,
return, or loading a save slot).

The new :tpref:`events` transform property determines if events are
passed to a transform's children. This is useful for ATL transforms,
when some children should not receive events.

Save dumps (enabled by :var:`config.save_dump`) are performed before the
save occurs, making them far more useful for debugging pickling problems.

When show\_ arguments are past to an :func:`NVLCharacter`, the show\_ prefix
is stripped and those arguments are passed to the ``nvl`` screen.

Translations
------------

This release add an Italian translation of the launcher and template game,
contributed by Oshi-Shinobu.

This release adds a Portuguese translation of the template game, contributed
by Mrstalker.

This release adds a Simplified Chinese translation of the launcher, contributed by
Huanxuantian.



Ren'Py 6.17.7
=============

This release includes a number of Android changes:

* RAPT has been updated to use the latest version of the SDK. Please install
  the SDK again if you have build problems.

* RAPT no longer includes a copy of Ren'Py. Instead, Ren'Py includes a copy of
  itself into the built game that RAPT uses. This makes it possible to include
  fixes to Ren'Py in an Android package.

* A low-level In-App Purchase implementation, contributed
  by Emmanuel Marty and Winter Wolves. The low-level IAP code supports Google
  Play and the Amazon App Store. This code is not currently documented, as it
  will be wrapped in a higher-level implementation.

This release includes a fix to an audio-video sync issue that affected the
Windows, Mac OS X, and Linux platforms.


Ren'Py 6.17.6
=============

This release adds a German translation of the launcher, contributed by
Marcel.

This release adds a Korean translation of the launcher and template game,
contributed by Baekansi.

This release includes a workaround for an issue that could prevent the
launcher from starting on certain Mac OS X computers.


Ren'Py 6.17.5
=============

Translations
------------

This release features an Arabic translation of the launcher and template
game, contributed by Renoa.

The Japanese and Spanish translations have been updated.

Changes
-------

The traceback system has been changed to generally report script statements,
rather than the functions Ren'Py uses to implement those statements.

The :func:`renpy.pause` function now only sets a checkpoint (allowing rollback)
if the delay time is 0. This prevents rollback from being blocked by short
pauses.

The new :func:`renpy.queue_event` function provides a way to queue Ren'Py
events from user-written interface code. (For example, it could be used to
listen to commands on a serial port that's connected to a custom
controller.)

If set, RENPY_SKIP_MAIN_MENU and RENPY_SKIP_SPLASHSCREEN environment
variables cause Ren'Py to skip the main menu and splashscreen, respectively.

The RENPY_TIMEWARP environment variable makes it possible to speedup and
slow down time.

An experimental new autoreload system can be accessed by setting
:var:`config.autoreload` to True, then pressing shift+R to toggle
automatic reloading.

Fixes
-----

A regression in 6.17.4 caused a major memory leak on shift+R. This has
been fixed. Several other problems with shift+R have also been fixed.

An issue preventing transitions from working properly inside a restarted
ATL transform has been fixed.

The --warp was documented incorrectly, and had stopped working. It's been
repaired, and its documentation has been improved.


Ren'Py 6.17.4
=============

Reloading
---------

This release contains a complete rewrite of shift+R reloading.

The rewrite was necessary to eliminate several major memory leaks that
were triggered by reloading.

Android
-------

Ren'Py has been updated to use the newest (at the time of release) versions
of the Android SDK and Ant. This should fix build problems caused by the
use of older versions.

Ren'Py now recognizes and supports the Amazon Fire TV device. When a Fire TV
is detected, the "firetv" screen variant is selected. To support pushing games
to this device, Ren'Py now supports connecting to Android devices via the
Remote ADB protocol.

Other
-----

Fixed a problem that occurred when an interaction containing a MoveTransition
was restarted.

Added support for imagemaps that are larger than the screen. This allows an
imagemap to be placed inside a viewport.

It is now possible to select the layer used by the say, choice, and nvl
choice screen. Please see :var:`config.say_layer`, :var:`config.choice_layer`,
and :var:`config.nvl_layer` statements.

The prediction of window and bar images has been improved.


Ren'Py 6.17
===========

Styles
------

The style system, which makes it possible to configure the look of
displayables, has been rewritten from scratch. The new code reduces
the amount of time it takes to create a new style to a small fraction
of the previous time. Since every displayable creates an associated
style, this has the potential to lead to a substantial performance
improvement.

This release also introduced a new style statement that can be used
to define styles, in place of python code. (Of course, the older form
remains fully supported.) Lengthy and redundant code like::

    init python:
        style.quick_button_text.set_parent('default')
        style.quick_button_text.size = 12
        style.quick_button_text.idle_color = "#8888"
        style.quick_button_text.hover_color = "#ccc"

can be replaced with::

    style quick_button_text is default:
        size 12
        idle_color "#8888"
        hover_color "#ccc"

Finally, the style inspector (accessed through shift+I) has been
rewritten.

Syntax Changes
--------------

In addition to the new style statement, there are four other syntax
changes:

* The definition of a simple expression has been expanded. Simple expressions
  (which are used in ATL and the screen language, among other places) now
  encompass all Python expressions that do not include lambda or the
  ternary (... if ... else ...) operator.

  This means that code like::

      show logo:
          xpos 800 / 2

  is now legal. Previously, the expression had to be parenthesized.

* The new ``show layer`` statement allows one to apply a transform
  or ATL transform to an entire layer, using syntax like::

      show layer master at flip

  or::

      show layer master:
          xalign 0.5 yalign 0.5 rotate 180

* The new ``window auto`` statement makes it possible for Ren'Py to
  automatically show and hide the dialogue window. By default, it is
  shown before ``say`` statements, and hidden before ``scene`` statements,
  but this can be customized.

* The init statement has been extended so it can be combined with
  other statements. It's now possible to write "init 1 image = ...",
  "init -2 define name = ..." and so on.

Translations
------------

This release adds French and Russian template games and translations
of the launcher.

Android
-------

It is no longer necessary to download RAPT (the Ren'Py Android Packaging Tool)
separately from Ren'Py. As of this release, RAPT will be downloaded by the
Ren'Py launcher when an Android build is requested, and will be updated
by the Ren'Py updater.

Buttons may now have an alternate action that is triggered by longpress
on Android and right-click on desktop computers.

This release fixes a bug in which Ren'Py would not save persistent data
(including preferences) before being terminated by the Android system, and
a regression that broke compatibility with some Android 2.3 systems.

New and Changed Preferences
---------------------------

There are two new preferences accessible through the :func:`Preferences`
function:

* "auto-forward after click" controls if auto-forward mode is stopped
  by a click.

* "show empty window" determines is if the "window show" and "window auto"
  statements will cause an empty window to be shown.

Neither of these is exposed as part of the default preferences screen, but
both can be added by interested developers.

There is one changed preference:

* "display" now has an "any window" option, which restores a fullscreen
  Ren'Py to its prior windowed size.


Other
-----

:func:`ShowMenu` can now pass arguments to the screen it displays.

The input displayable now takes a pixel_width property, that limits
the size of the input field it a certain number of pixels.

The :func:`FileCurrentScreenshot` function

The new :propref:`xsize`, :propref:`ysize`, and :propref:`xysize` style
properties make it possible to directly set the size of a displayable.

The :propref:`focus_mask` style property can now take as an argument a callable
that returns true when a displayable should be focused. If such a callable
can be written, it may be much faster than the current method of determining
pixel opacity.

Viewport now respects the xfill and yfill properties. The default viewport
style sets these to true. Setting them to False will cause the viewport to
shrink to fit its contents when those contents do not fill the entire
viewport.

The new :func:`renpy.get_image_bounds` function retrieves the bounding box
of an image that is being displayed, after all Transforms have been applied
to it.

The new :func:`renpy.retain_after_load` can be used to retain data updated
by a screen after the game is loaded.

The new :propref:`xsize`, :propref:`ysize`, and :propref:`xysize` style
properties make it possible to directly set the size of resizable
displayables.

Prediction of images with partial attributes and side images used in
dialogue has been improved. Prediction of creator-defined statements
now works as documented.




Ren'Py 6.16.2
=============

This release adds a Spanish translation of the launcher and the template game.

This release adds the new :func:`renpy.get_mouse_pos` function, which
retrieves the mouse position if a mouse is supported.

Ren'Py 6.16
===========

Android
-------

Android support has now been integrated into the Ren'Py launcher. While
for size reasons RAPT is still a separate download, once RAPT has been
placed inside the Ren'Py directory, the launcher will allow you to:

* Install the Android SDK.
* Configure a project as an Android application.
* Build and Install the Android application.

The launcher can now launch Ren'Py in modes that simulate Android phones,
tablets, and television-based consoles.

Ren'Py includes support for television-based Android consoles, such as the
OUYA. It includes support for detecting the OUYA specifically, and choosing
a variant as appropriate.

This release adds some video playback support to the Android port. While
limited to full-screen video and codecs that the Android platform supports
(which unfortunately have little overlap with desktop Ren'Py), this may
be enough to enable cutscene movies.

Ren'Py now includes a new set of screen variants, with "large", "medium", and
"small" reflecting the visual size of devices (televisions are considered to
be small because they're far away), while "touch", "tv", and "pc" reflect
the input devices involved.

Android now supports displaying vertical text.


Save, Load, and Persistent Improvements
---------------------------------------

The low-level load/save API has been overhauled. It's now possible to
access save slot information directly, instead of having to scan all save
slots to find the one you want. New functions include :func:`renpy.list_slots`,
:func:`renpy.newest_slot`, :func:`renpy.slot_mtime`,
:func:`renpy.slot_json`, and :func:`renpy.slot_screenshot`.

At a higher level, there is a new :func:`FileNewest` function that's
true for the newest save slot. :func:`FilePageNext` and
:func:`FilePagePrevious` now support a wrap argument that causes them
to wrap around a defined number of screens.

There is now support for adding arbitrary JSON information to save
files. This allows per-save information (like the path you're on
in a VN, date and amount of money in a sim, or party composition
in an RPG) to be accessed from the save and load screens.

JSON information is created by :var:`config.save_json_callbacks`,
and can be accessed through the low-level :func:`renpy.slot_json` or
high-level :func:`FileJson` functions.

When possible, Ren'Py now stores save files with the game, as well as in
a user-global save directory. This means that if a Ren'Py game is placed
on a USB drive or shared on a network, the saves will be available on
multiple computers. (When save files are available in both places, the
newest file wins.)

When a save file on a network share is updated, Ren'Py will automatically
rescan the contents of that file, and restart the current interaction. (This
will update the save and load screens, making the file available to be
loaded.)

Ren'Py will no longer auto-save while at the main menu.

Persistent data is also stored in both locations. When the persistent
data is not identical, it will be merged. By default, the most recently
updated value for each field will be used. In some cases (for example, a set
of endings the player has reached), this is not the correct behavior. The
new :func:`renpy.register_persistent` can be used to register different
merge behavior.

Voice
-----

This release adds support for playing voice without having to fill
the script with voice statements. This support consists of two
new pieces of functionality:

* The launcher contains a new "Extract Dialogue" function. This extracts
  the dialogue into a tab-delimited file. Each record includes the character,
  the dialogue text, the filename and line number, and a unique identifier
  for that line.

* The :var:`config.auto_voice` variable is used to give a filename pattern
  that is formatted with the unique identifier. If a file with that filename
  exists, and no other voice file is being played, that file is used as the
  voice.

There are also several new voice-related preferences. The "voice sustain"
preference determines if voice is sustained through multiple interactions.
The "wait for voice" preference determines if auto-forward mode waits for
the voice to finish before advancing.

Image Gallery and Music Room
----------------------------

The image gallery now can display a navigation overlay with next, previous,
slide show, and return buttons. The creator can choose if these buttons
display the images associated with a single button, or advance between
multiple buttons.

The Music Room includes the ability to play a random track, and to determine
if the tracks are shuffled, looped, or if play is confined to a single
selected track.

Text Rendering
--------------

Ren'Py now renders portions of font characters that leave the character
bounding box. This prevents text (especially hinted and anti-aliased text)
from being cut off, but may lead to apparent placement problems for fonts
with very inaccurate bounding boxes.

Japanese Language
-----------------

The Ren'Py launcher has been translated into Japanese. The language
used by the launcher can be switched from the preferences screen.

There is now a Japanese language template game, which defaults to
a Japanese font and has a translated interface.

Much of the documentation has been translated
to Japanese. The Japanese translation can be found at:

    http://ja.renpy.org/doc/html/

Documentation
-------------

The Ren'Py documentation has been improved. The following pages have been
added or migrated from the old wiki-based documentation.

* :doc:`label`
* :doc:`python`
* :doc:`conditional`
* :doc:`audio`
* :doc:`movie`
* :doc:`persistent`
* :doc:`cds`
* :doc:`character_callbacks`
* :doc:`file_python`
* :doc:`environment_variables`
* :doc:`reserved`

Many other documentation pages have been improved and edited.


Other
-----

The default quick menu now includes rollback and fast skip
functionality. (This functionality is contained in the template screens.rpy,
and may need to be copied into your game.)

The default yes_no screen now answers no when the user right-clicks. (This
functionality is contained in the template screens.rpy, and may need to be
copied into your game.)

The fast skipping function now stops when it visits seen text.

The :var:`build.destination` variable can be used to select the directory
in which Ren'Py places files when building a distribution.

There is a new NullAction that can be used when one wants a button
to be sensitive to hover and unhover, but not performing a useful
action on click.

ConditionSwitch is now much faster.

Ren'Py will deal with files with insane timestamps by giving them the
current time.

Bugfixes
--------

This release includes many bugfixes. Some of the more important are:

* A fix to a problem that would cause Ren'Py to restart the display when
  starting up on Windows. This could cause Ren'Py to spuriously detect a
  slow video card, and present the user with the appropriate error message.

* A fix to a problem where Ren'Py would fail to display the proper error
  message when python code containing non-ASCII characters fails to compile.



Ren'Py 6.15.6
=============

This release includes improvements for the Android platform:

* Assets are now read exclusively from the APK and expansion file.
* Logs and tracebacks are placed on external storage.
* Saves are placed on external storage, except when saves from
  older versions of Ren'Py exist.

The GL2 shaders Ren'Py uses have been simplified in the (usual) case
where no clipping is occurring. This leads to a noticeable speed
improvement on Android, and potentially other platforms as well.

An issue with Drag-and-drop has been fixed. Thanks go to Kinsman
for contributing this fixe.

The :func:`Skip` action now triggers the skip indicator. It also
supports a new fast parameter, which causes skipping to the
next menu.

This release includes various minor changes to improve compatibility
with very old Ren'Py games. (It now runs the Ren'Py 5 demo.)


Ren'Py 6.15.5
=============

This release adds two new features:

* The GL renderer now supports additive blending. This is enabled using the
  :tpref:`additive` transform property in an ATL transform or use of the
  :func:`Transform` class. Additive blending will not work if the software
  renderer is in use, and it's up to creators to deal with that issue.

* The new :func:`Flatten` displayable combines multiple textures into
  a single texture. This can be used to prevent incorrect behavior
  when a displayable containing multiple overlapping textures (like a
  :func:`LiveComposite` is shown with an :tpref:`alpha` between 0 and 1.

It also fixes the following issues:

* Whitespace is now skipped before default arguments, which previously
  caused parse errors in some cases.

* Ren'Py now sets the unix mode of files and directories in zip and tar
  files to 644 and 755 as appropriate. Prior versions of Ren'Py used
  666 and 777 as the permissions, which lead to a security problem
  when the file was unpacked by a tool that didn't respect the user's
  umask. (Info-zip had this problem.)

* Auto-hinting for fonts is now enabled by default. This restores font
  rendering compatibility with prior releases.

* Ren'Py now builds with and requires the current version of libav. It
  should also work with current versions of ffmpeg when libav is
  available.

* The version of SDL distributed with Ren'Py has been patched to
  prevent multiple windows from showing up in the Window menu
  when entering and leaving fullscreen mode.



Ren'Py 6.15.4
-------------

This release fixes a compile problem that prevented Ren'Py 6.14.x and Ren'Py
6.15.0-3 from running on most 64-bit Linux systems.

Image prediction has become more fine-grained, and can take place while the
screen is animating.

The new :var:`build.exclude_empty_directories` determines if empty directories
are include or excluded from the distribution. It defaults to true,
previously the default was platform-dependant.



Ren'Py 6.15
===========

Translation Framework
---------------------

Ren'Py now includes a comprehensive
:ref:`translation framework <translation>`. This framework includes support
for using a single language selection to change dialogue, menus and other
interface text, images and files, styles and styles.

The dialogue translation support allows lines of dialogue to be split and
combined at the translator's discretion. As most Ren'Py statements are
allowed inside the new translation blocks, it's possible to use logic (like
conditions) to tailor the translations to your language.

The launcher includes a new "Generate Translations" button, which - as part of
a sanctioned translation where the full script is present - will generate
empty translation files for a new language.

Improved Japanese Support
-------------------------

Ren'Py 6.15 includes multiple changes to better support the Japanese language.

* The tutorial game has been translated to Japanese, with the language being
  selectable from the preferences menu.

  The tutorial was translated by Koichi Akabe.

* Support for vertical writing has been added to Ren'Py. Consisting of the
  :propref:`vertical` style property for text, and the new
  :propref:`box_reverse` property on hboxes, this support makes it possible
  to display dialogue, menus, and other text in a vertical orientation.

  Vertical text support was written by Koichi Akabe.

* The line-breaking algorithm has been updated to match Unicode 6.2. In
  addition, three new "languages" have been added. The new "japanese-strict",
  "japanese-normal", and "japanese-loose" languages (based on the line-break
  options in the CSS3 Text module) allow greater control of how Ren'Py breaks
  lines with small kana and other special characters.

  Linebreaking can be further tailored using the new
  :func:`renpy.language_tailor` function, which can change the linebreaking
  class of a character.

Console
-------

The new debug console makes it possible to interactively run Ren'Py script and
Python statements, and immediately see the results. The console is available
in developer mode or when :var:`config.console` is True, and can be accessed
by pressing shift+O.

The console can be used to:

* Jump to a label.
* Interactively try out Ren'Py script statements.
* Evaluate a python expression or statement to see the result.
* Trace python expressions as the game progresses.

The console was originally written by Shiz, C, and delta.

Screen Parameters
-----------------

Screens now take named parameters, similar to the way that labels and
transforms take named parameters. It's now possible to write::

  screen top_text(s, size=36):
       text s xalign 0.5 size size

and::

  show screen top_text("It works!")

Replay Gallery
--------------

Ren'Py now includes support for :ref:`replaying <replay>` scenes. A scene
replay can be invoked from anywhere in Ren'Py (for example, from a main menu
or game menus screen, even when the game has started). When the replay ends,
Ren'Py will return to the location the replay was invoked from, even if that
location is in a screen or in python code. Rollback works inside a replay,
but saving and loading is disabled.

The :func:`Replay` action begins a replay. The :func:`renpy.end_replay` ends a
replay if one is in progress, and is ignored otherwise.

Voice Improvements
------------------

There have been several improvements to the voice playback system. The new
:var:`config.voice_filename_format` variable makes it possible to use only
part of the filename in a voice statement. The new voice_tag parameter to
:func:`Character`, in conjunction with the :func:`SetVoiceMute` and
:func:`ToggleVoiceMute` actions, makes it possible to selectively mute
particular characters' voices. The new :func:`VoiceReplay` action makes it
possible to replay the current voice.

Launcher Improvements
---------------------

There were a few launcher improvements in this release.

* The files pane of the navigation page has a new button that allows the
  user to create a new script file.

* The launcher can generate translation templates, and can be translated
  using the translation framework.

* The Ren'Py launcher now has a small amount of support for skins. While the
  basic layout of the launcher remains fixed, skins allow the background
  images and colors to be changed. See the :ref:`skin documentation <skins>`
  for more details.

Macintosh Changes
-----------------

The Macintosh version of Ren'Py now requires a 64-bit capable processor, and
Mac OS X 10.6 or newer.

Packaging Improvements
----------------------

The file layout of Ren'Py games has been somewhat altered. With the exception
of small launcher programs, all platform-dependent binaries are under the
lib/ directory. Ren'Py itself has now been placed in the renpy/ directory.
The common/ directory has been moved to renpy/common/, as it's considered an
integral part of Ren'Py.

Ren'Py now uses renamed but otherwise unmodified python binaries on all
desktop platforms. (Previously, it used platform-specific binaries.) Portions
of the library are shared between the desktop builds.

A running Ren'Py process on Linux will now be named after the game, rather
than having python as a name.




Other Changes
-------------

* :ref:`Viewports <sl-viewport>` now support edge scrolling, which scrolls
  the viewport when the mouse is within a a configurable distance of the
  viewport edge.

* Most keyboard keys now automatically repeat. The repeat rate is controlled
  by :var:`config.key_repeat`.

* Side images can now be used with menus.

* The :var:`config.enter_yesno_transition` and
  :var:`config.exit_yesno_transition` variables make it possible to define a
  transition that is run when yes/no prompts appear and disappear,
  respectively.

* The :ref:`viewport statement <sl-viewport>` now supports edge scrolling -
  automatic scrolling when the mouse approaches the sides of the viewport.

* The new :tpref:`transform_anchor` transform property makes the anchor the
  point around which a transform is scaled and rotated. (For example, it's
  now possible to rotate around the bottom-right corner of an image, rather
  than just its center.)

* The common directory has been moved to renpy/common, as it's part of
  Ren'Py. The giant 00screens.rpy file has been broken up into a large number
  of smaller files.

* The new :propref:`box_reverse` and :propref:`order_reverse` style
  properties allow the user to control the order in which children of vbox
  and hboxes are placed and drawn, respectively.

* The xoffset and yoffset transform properties now take floating point
  numbers, allowing more precise positioning if subpixel is true.

* The :propref:`child` style property of buttons is now exposed to the
  screen language.

* The new :var:`config.enter_yesno_transition` and
  :var:`config.exit_yesno_transition` variables allow a creator to supply
  transitions that are used upon entering and exiting yes/no prompts.

* The python decimal module is now included in the default builds of Ren'Py.

Bugfixes
--------

Among others, the following bugs were fixed:

* :ghbug:`37`: A crash with LiveTile when sizes were not integers.

* :ghbug:`41`: :func:`renpy.loadable` failed to search for files inside
  android packages.

* :ghbug:`42`: The launcher can now run a game that's in a read-only
  directory.

* :ghbug:`45`: Ren'Py would fail when the hiding of a screen caused a screen
  beneath it to be hidden.

* :ghbug:`46`: A bug that prevented Ren'Py from evicting images from an
  over-full image cache, that manifested as a runaway memory leak.

* :ghbug:`50`: Vertical bars would scroll with the left and right arrow
  keys; and bars would remain grabbed even if they were grabbed while leaving
  the screen, preventing further input.

* :ghbug:`51`: The slow_done callback was not called after a rollback.

* :ghbug:`56`, :ghbug:`57`: :func:`renpy.loadable` now works with Android
  assets.

* :ghbug:`60`: Fixed a bug that prevented {p} and {w} from working properly
  when followed immediately by a text tag.

* :ghbug:`61`: Ren'Py no longer crashes when an end_game_transition is set
  and a screen uses a variable that is no longer defined when the game
  restarts.

* :ghbug:`65`: Multiplying a rollback list by a number now always produces a
  rollback list.

* Editra should work better on Windows.

* It's now possible to :func:`renpy.call` a label that doesn't take
  parameters.

* Fixed an error handling failure when a style used by error handling was
  not buildable.

* Fixed an error handling failure when a python early block contained a
  syntax error.



Ren'Py 6.14
===========

Ren'Py Launcher Rewrite
-----------------------

The Ren'Py launcher has been rewritten. Some of the improvements are:

* A new visual design by Doomfest of the Dischan visual novel team.

* The launcher now includes direct access to open the script and game
  directories, and common script files.

* The launcher includes Script Navigation support. Clicking the name of a
  label, define, transform, screen, or callable will open the editor to the
  location where that name is defined.

  Script navigation also provides access to individual script files.

* The launcher now supports one-click project building. Instead of using
  multiple steps to build a project, a single click will now cause the
  launcher to:

  * Read the build process configuration from the game script.
  * Build the archives needed.
  * Generate the archive and update files.

* The launcher can now use the Ren'Py updater to update Ren'Py, and to
  download editors.

Editra & Text Editing
---------------------

For most users, Ren'Py recommends the use of the Editra editor. We have
developed an Editra plugin that communicates with the Ren'Py launcher and
supports the editing of Ren'Py script.

While still in beta, Editra is a fast and light editor with good code editing
support. Editra also includes a spell-checker that can be enabled, and
applies to dialogue and other strings.

If Editra is selected by the user, and it is not installed, Ren'Py will
automatically download it.

The jEdit editor remains supported, and is preferred for use with languages
(like Chinese, Japanese, and Korean) that Editra doesn't support fully. If
selected, Ren'Py will download jEdit automatically.

Ren'Py also supports editing files through system-specific file associations.
(This support will not send the cursor to the correct line, however.)

Ren'Py Web Updater
------------------

Ren'Py includes an updater that can update Ren'Py and individual Ren'Py games
by downloading changes from a properly-configured web server with a small
number of update files uploaded to it.

The updater uses zsync to download the minimal set of changes between the
local files on disk and the files stored on the server. A single set of files
on the server supports updating from all prior versions of a project.

Ren'Py includes a default updater interface that can be further configured by
interested users.


Transform Changes
-----------------

This release changes the behavior of transforms to make them more correct and
easier to use.

The xzoom and yzoom properties are now applied before, rotation. This means
that the shape of the image will remain consistent as the image is rotated.
Previously, the image to change shape as it was rotated.

The xzoom and yzoom properties may now be negative, with negative zoom values
causing the images to be flipped. The positioning code now takes this into
account, and positions a flipped image properly.

Thanks to Edwin for contributing these changes.

Screen Language, Displayable, and Transition Enhancements
---------------------------------------------------------

* The :ref:`sl-textbutton` and :ref:`sl-label` screen language statements
  now take properties prefixed with ``text\_``. These properties have the
  text\_ prefix stripped, and are then passed to the internal text displayable.

* The :ref:`sl-viewport` screen language statement now takes a `scrollbars`
  parameter. If given, scrollbars that manipulate the viewport are created.

* The :ref:`sl-viewport` screen language statement now takes `xinitial` and
  `yinitial` parameters. If given, these control the initial positioning of
  the viewport.

* A screen language block may now contain multiple has statements. Screen
  language widgets that take single children can now take a has statement.

* The input displayable now supports the use of the left and right arrow
  keys within the text. (Thanks to Edwin for this feature.)

* :func:`MoveTransition` has been rewritten. The new version now uses
  transforms to control the positioning of entering and leaving images, and
  can interpolate between the locations of moving images.

Rollback Improvements
---------------------

* The new :func:`renpy.fix_rollback` function allows the game to fix
  choices, even if they are made in rollback mode. The user can roll back and
  roll forward, but is restricted to making the choices he made the first
  time through the game.

  Thanks to Edwin for contributing fix_rollback.

* Rolling forward now works through a jump out of a ``call screen``
  statement.

Video Improvements
------------------

Ren'Py's video playback support has been partially rewritten to improve
robustness, speed, and framerate stability. These improvements should reduce
the number of frame drops Ren'Py performs, and should also prevent Ren'Py
from locking up if too many frames are dropped.

Ren'Py now supports the WebM video format.


Image Load Log
--------------

When :var:`config.developer` is true, Ren'Py keeps an internal log of image
loads.

This log can be access by showing the _image_load_log screen. This screen
displays the name of an image file for a few seconds after that image has
been loaded. The name is in white if the image was loaded by the image
predictor, and pink if Ren'Py was unable to predict the image.


File Actions and Functions
--------------------------

Two screen functions have been added, and two screen actions have been changed:

* The new :func:`FileUsedSlots` function returns a list of used file slots
  on the current page.

* The new :func:`FileCurrentPage` function returns the name of the current
  page.

* The :func:`FileSave` and :func:`FileAction` actions have been modified so
  that if the slot name is None, an unused slot based on the current time is
  used.

Taken together, these changes make it possible to create a list of save slots
where the user is able to add new slots to the list.


Multiple Store Support
----------------------

Ren'Py now supports multiple stores - multiple namespaces in which python code
can be run. Variables in these stores are saved, loaded, and rolled-back in
the same way that variables in the default store are.

Stores are accessed by supplying an in-clause to a python block. For example::

   init python in stats:

       def reset():
           """
           Code to reset the statistics.
           """

User-created stores are placed into the "store" package, with the default
store being the package itself. Names can be imported between packages.::


   init python:
       from store.stats import reset

   init python in stats:
       from store import ToggleField

Note that stores do not affect the order in which init python blocks are run.
A name must be defined in a block before the one that imports that name.


Platform Support and Library Updates
------------------------------------

Linux support has been changed.

* The Linux platform supports the x86_64 CPU architecture in addition to the
  x86 architecture. The Ren'Py shell script will automatically determine the
  platform it is running on when it is launched.

* The Linux version is now linked against the libraries from the 2009-era
  Ubuntu 10.04 Lucid. (Previously, Ren'Py had been linked against 2006's
  Dapper.) Older versions of Linux are no longer supported.

Many libraries that Ren'Py depends on have been updated. Some of the changes
that have occurred are:

* Python has been updated to version 2.7.3.

* Pygame has been updated to version 1.9.1.

* GLEW has been updated to version 1.7.0. This may fix OpenGL problems on
  some Linux systems.

* LibAV has been updated to version 0.7.6, and has been compiled with CPU
  detection enabled.

Other Changes
-------------

* The :func:`renpy.call` function allows - with major and important caveats -
  a call to a Ren'Py label to begin from inside python code. Such a call
  immediately terminates the current statement.

* When an action is expected, nested lists of actions can be given. The
  lists are flattened and the action executed.

* Added the :func:`OpenURL` action, which opens a URL in a web browser.

* Added the :var:`config.gl_resize` variable, which determines if the user
  can resize OpenGL windows.

* Ren'Py's handling of command line arguments has been rewritten. Most
  notably, lint is now invoked with the::

    renpy.sh <gamename> lint

  command. (Which also works with renpy.exe.)

* Ren'Py can now dump information about the game to a json file when
  starting up. The information dumped can assist other tools in providing
  launcher-like code navigation.

* The little-used remote control feature has been removed from Ren'Py.

* The :var:`config.gl_resize` variable now controls resizing of a game
  running in GL mode.

* Documentation fixes (by SleepKirby and others).

* The NVL-Mode tutorial has been ported to Sphinx (by Apricotorange).

* Ren'Py now defaults to reporting errors with sound and music files when
  config.developer is True.

Ren'Py 6.13.9
=============

The new RAPT tool makes it far easier to package a Ren'Py game for Android. It
can semi-automatically set up an Android build environment on your system,
build a package, and install that package on your Android device.

To fix some editor-related problems, backported the 6.14 editor system. This
changes how editors are configured. Please see :ref:`text-editor-integration`
for a description of the new system.

The new :var:`config.save_dump` variable causes Ren'Py to write out
save_dump.txt each time it saves. This file describes the contents of the
save, making it possible to figure out what's causing an overly large save
file.

Worked around a bug in Mesa that can cause crashes on certain Linux systems.

Fixed the following bugs in Ren'Py.

* The (default) texwrap layout represents character widths as floating-point
  numbers. This fixes a bug where non-integer kerning would lead to text
  overflowing its bounding box.
* Menu choices are logged correctly.
* All file access is now done in unicode, rather than the system's native
  encoding. This prevents crashes that occurred when Ren'Py was placed in a
  directory that had non-ASCII characters in it.
* Fixed focus_mask on the ANGLE renderer.
* Displayables can now have fractional-pixel sizes. This allows a zooming
  image to remain precisely centered on the screen.
* Fixed a problem where Ren'Py would save unnecessary trees of displayables
  each time it saved a screen. This would lead to overly large save files and
  slow save performance.
* Ren'Py would not attempt an alternate rendering method if the texture test
  failed, leading a "Textures are not rendering properly." exception.
* A crash in Render.fill.

Ren'Py 6.13.8
=============


Side images can now be limited to showing a single character, or only showing
characters that are not on the screen. See :var:`config.side_image_tag` and
:var:`config.side_image_only_not_showing`.

Added :var:`config.python_callbacks`, a list of python functions that are
called at the end of each python block.

Ren'Py now tests the video card it is running on for functionality. If it
can't draw textured rectangles to the screen, it will proceed to a different
renderer.

Old-style string interpolation is now enabled by default, alongside new-style
string interpolation.

Ren'Py is now compatible with libpng 1.5. Thanks to James Broadhead for the
patch.

Fixed the following bugs:

* A crash when dealing with certain invalid fonts.
* Pausing too long when typing out text.
* Cutting one pixel off a block of text when fractional kerning was used.
* Crashing when the time was set in the far future or past.
* Immediately exiting when rolling forward at the quit prompt.
* Crashing when a non-existing directory is added to the search path. (This
  prevented Katawa Shoujo from starting in the latest version.)
* Save-file size was overly large due to screens being included in save
  files.


Ren'Py 6.13
===========

Text Rewrite
------------

:ref:`Text display <text>` has been rewritten from scratch. In addition to
supporting many new features, the new implementation of Text is much faster
at text layout and display, and contains much cleaner code.

Some of the new features that are now supported by the text display system are:

* Interpolation of variables enclosed in square brackets. It's now possible
  to write code like::

      "You scored [score] out of a possible [max_score] points."

  The new string interpolation takes place on all text that is displayed,
  rather than just say and menu statements. When used as part of a screen,
  interpolation has access to screen-local variables.

  PEP 3101-style string formatting is supported, which means that this
  syntax can be used to display fields and items, as well as variables.

* Kerning support was added, both as the :propref:`kerning` style property
  and the :tt:`k` text tag.

* Support for ruby text (also known as furigana), via the :tt:`rt` and
  :tt:`rb` text tags, and the :propref:`ruby_style` style property.

* The new :tt:`space` and :tt:`vspace` text tags make it easy to whitespace
  into the text.

* The new :tt:`cps` text tag controls the speed of text display.

* By default, Ren'Py uses the unicode linebreaking algorithm to find points
  at which a line can be broken. This algorithm should correctly break lines
  that contain a mix of western and eastern languages. Since that algorithm
  is incorrect on some Korean texts, Ren'Py also implements a
  korean-with-spaces variant, that only breaks runs of Korean text at
  whitespace. These algorithms can be selected by the :propref:`language`
  style property.

* Ren'Py now uses the Knuth-Plass linebreaking algorithm to choose the
  points at which it actually splits lines. This algorithm attempts to
  minimize the unevenness of all lines except the last. Ren'Py also supports
  a nobreak mode, which allows one to create a Text larger than the screen
  without it being automatically wrapped. These can be selected using the
  :propref:`layout` style property.

* The new :propref:`newline_indent` style property determines if Ren'Py adds
  indentation after a newline in text.

* The new :propref:`line_leading` style property inserts space above a line
  of text. (Ruby text can be placed into this space.)

* Text can be automatically translated before it is displayed. (This support
  will be improved in a future major release.)

DirectX Support
---------------

On Windows systems that have the February 2010 DirectX update installed,
Ren'Py will use DirectX via the ANGLE adaptation layer, if OpenGL 2.0 or
later is not found. The ANGLE layer is used by popular web browsers such as
Firefox and Google Chrome.  This allows hardware rendering to be used on
netbooks, where drivers often support DirectX far better than OpenGL.

At startup, Ren'Py will test the graphics capabilities of the computer it is
running on. If the software render is being used, or the game renders at an
unacceptably slow speed, Ren'Py will display a warning message to the user.
The warning message includes a link to a page on renpy.org that explains how
to update the graphics drivers.

This version of Ren'Py will only use the software renderer if both DirectX and
OpenGL are incapable of rendering Ren'Py games. Screen-scaling in the
software renderer has been replaced by a simpler but slower version.

Other Changes
-------------

* Ren'Py now includes a :ref:`style preference <style-preferences>` system.
  This system allows styles to be changed after the init phase has finished.
  These changes are saved with the persistent data. Among other things, style
  preferences allow a game to offer the user the option to change the font,
  size, and color of dialogue text.

* Support has been added for screen-based
  :ref:`image galleries <image-gallery>` and :ref:`music rooms <music-room>`.
  This support consists of a classes that provides actions that make it easy
  to present the user with graphics and music. The creator is responsible for
  creating screens that use the supplied actions.

* The default screens.rpy file, used when a new game is created, contains
  support for a "quick menu". This menu adds buttons to screens that allow
  the user to quick save, quick load, save, toggle skipping, toggle
  auto-forward mode, and access the preferences menu.

* Ren'Py includes 5 new themes, and a number of new color schemes.

* Several new actions have been added. The :func:`SelectedIf` action allows
  the creator to control if a button is displayed in the selected state. The
  :func:`SetMixer` action allows a mixer to be set to a specific value. The
  :func:`Rollback` and :func:`RollForward` actions allow the creator to bind
  rollback to buttons.

* The behavior of the xfill and yfill style properties was accidentally
  changed in the 6.12 series. It has been returned to the historical behavior.

* The :func:`Dissolve` and :func:`ImageDissolve` transitions now take a
  time_warp parameter.

* The :func:`Frame` displayable now allows the user to specify the left,
  top, right, and bottom borders independently.

* The :propref:`caret` style property allows the user to customize the caret
  of an input widget.

* The :func:`renpy.displayable` function has been exposed to the user.

* Timers can now take a list of actions, rather than just a single callable.

* Three transforms were added to the default library: :var:`top`,
  :var:`topleft`, and :var:`topright`.

* Ren'Py can now load files (including images, music, and fonts) from an
  Android package.

* User-defined statements can now take a block, which the statement is
  responsible for parsing.

* Wrote documentation for:

  * :ref:`Menus <menus>`
  * :ref:`Transforms <transforms>`
  * :ref:`Creator-Defined Displayables <cdd>`

  Several indexes were added to the documentation, and the style was updated.

* Ren'Py now uses the libjpeg-turbo library, for faster jpeg loading. Ren'Py
  now uses libav 0.7.1, for improved compatibility with movie formats.

* Removed support for the iLiad platform.

* PowerPC support has been removed from the main Ren'Py distribution. It's
  available as a download from the Ren'Py web site.

Thanks to Aleema for contributing the new themes and color schemes.


Ren'Py 6.12.2
=============

This release contains the following changes:

* ATL Transforms with parameters compile correctly.
* MultipleTransition works in conjunction with pauses.
* The mouse is shown when a quit action is run while a movie is playing.
* A fix for a lockup that occurred when the user entered the game menu while
  a transition was running.
* RENPY_SCALE_FAST works again.
* Ren'Py compiles with newer versions of ffmpeg.
* Skipping ends when the game restarts.
* Fixed a problem with texture upload that made games noticeably slower.
* Choose a better default size for windows on small monitors, like netbooks.
* xfill and yfill now work for vbox and hbox, respectively.
* Click-to-continue fixes.
* Side image fixes.
* Documentation fixes.

Thanks to David Gowers and zhangning for contributing patches to this release.


Ren'Py 6.12.1
=============

Image Attributes
----------------

The process of showing images is now attribute-based. Image names now consist
of a tag, and zero or more attributes. When showing an image, the order of
attributes is no longer important - it's now possible to define an image
using one set of attributes, and show it using those attributes in a
different order.

Attributes are also "sticky". This means that we attempt to preserve as many
attributes as possible when showing a new image.

For example, say we had the following images::

   image eileen beach happy = "eileen_beach_happy.png"
   image eileen beach woozy = "eileen_beach_woozy.png"

We can now show the first image using the command::

   show eileen happy beach

Since the order of attributes no longer matters, this will show the "eileen
beach happy" image. If we follow this with the show statement::

    show eileen woozy

the image "eileen beach woozy" will be shown. (Assuming no other images exist.
If the image "eileen happy woozy" existed, an ambiguity error would occur.)

When an image tag is shown without any attributes, then the current attributes
are retained. Now, one can write::

    show eileen at right

to display Eileen on the right side of the screen, without changing the
attributes supplied to an image.

**Say Attributes.** Image attributes can be updated as part of a say
statement. A character can be given an `image` argument, giving the name of
an image that character is linked to. As part of the say statement, image
attributes can be given before the dialogue string. These attributes are
given to the linked image.

For example, if we define a character using the code::

    define e = Character('Eileen', image="eileen")

the code::

    e woozy "I think I'm getting too much sun."

is equivalent to::

    show eileen woozy
    e "I think I'm getting too much sun."

whenever an image with the tag eileen is being shown.

**Side Image.** This release features a new implementation of
:ref:`side-images`, which allows side images to be defined like other images,
and allows side images to be integrated with screens easily.

**Sticky Transforms.** Finally, showing an image without providing a transform
or ATL block will now continue the previous transform that an image with that
tag was using. Previously, it caused those transforms to stop.

Error Handling
--------------

Ren'Py now has a new exception handing framework. Instead of always crashing
when an error occurs, Ren'Py will now display the error message on the
screen, and give the user the following choices, as appropriate to the
situation:

* Rollback
* Reload
* Ignore
* Open Traceback
* Quit

When an editor is defined, Ren'Py will allow the user to click on a filename
and line number to open that line in the editor.

The framework is used to handle exceptions and parse errors.

Other
-----

When in OpenGL mode, Ren'Py now remembers the window size between  sessions.
(This can be disabled using :var:`config.save_physical_size`, and it  may
make sense to do so if your game is using the pre-screen preferences system.)
Choosing the "Window" display preference now resizes the window to 100% of
normal size.

Added the :propref:`xcenter` and :propref:`ycenter` position and transform
properties. These set the position of the center of a displayable.

The :func:`renpy.vibrate` function allows Ren'Py to ask Android devices to
vibrate.

The hyperlink style, callback, and focus functions have now been moved to the
:propref:`hyperlink_functions` style  property. This allows the functions to
be changed on a per-style basis.

Indentation errors are now reported on the indented line, and not the line
preceding the erroneous indentation.

Added the :func:`SetScreenVariable` and :func:`ToggleScreenVariable` actions.
These allow screen-local variables to be changed.

Ren'Py now attempts to elide personal information from filenames. Where
possible, filenames are reported relative to the base or Ren'Py base
directories,  rather than the root of the filesystem.

The new :propref:`box_wrap` style property allows hboxes and vboxes to
automatically wrap when they reach the edge of their enclosing area.

Actions now can have an :func:`Action.unhovered` method. This method is called
when an action supplied as a `hovered` parameter loses focus.

Added the :class:`Tooltip` class, which makes it easier to define tooltips as
part of a screen.

Added :var:`config.debug_text_overflow`, which controls the logging of cases
where text exceeds its allocated area.

Ren'Py no longer attempts to adjust the system level mixer controls, which
means that it's no longer possible to raise the volume from within Ren'Py.
Controlling the system volume exhibited bugs on all three platforms,
including hard-to-predict volume changes that affect other applications.

Along with the new features, transitions have been documented in the new
manual.

Archives are now automatically detected in asciibetical order. See the
documentation for :var:`config.archives` for more details.

Bug fixes:

* :lpbug:`734137` - Timers do not participate in rollback.
* :lpbug:`735187` - Ren'Py get stuck when using {nw}. (Thanks to Franck_v
  for tracking this down.)


Ren'Py 6.12.0
=============

Android Support
---------------

Ren'Py now supports the Android platform. This includes support for a large
fraction of Ren'Py's functionality, although we were unable to add support
for imagedissolves and movie playback. It should be possible to package a
Ren'Py game and distribute it through the Android market.

Android support required several changes in Ren'Py:

* The OpenGL renderer has been extended to support OpenGL ES.

* For performance reasons, much of the display system has been rewritten in
  the Cython language. This also should improve performance on other
  platforms.

* Support was added for the Android lifecycle. Ren'Py automatically saves
  when the android device suspends, and reloads (if necessary) upon resume.

* We added the concept of :ref:`screen-variants`. This allows a single game
  to have multiple interfaces - such a mouse interface for computer
  platforms, and a touch interface for Android-based smartphones and tablets.

* We built a system that allows one to package a game separately from
  Ren'Py. This allows one to build packages without having to set up the
  Android NDK (you'll still need the Android SDK, Java, Python, Ant, and a
  lot of patience).


New Widgets and Displayables
----------------------------

Added the :ref:`SpriteManager <sprites>` displayable. This provides a
high-performance way of drawing many similar sprites to the screen. This can
scale to hundreds of particles, provided those particles are mostly similar
to each other.

Added the :ref:`mousearea` widget. A mousearea allows hovered and unhovered
callbacks to occur when the mouse enters and leaves an area of the screen.
Since it doesn't participate in the focus system, a mousearea can include
buttons and bars.

Added :ref:`drag-and-drop` widgets and displayables. The drag and drop system
can support:

* Windows being repositioned by the user.
* Card games.
* Inventory systems.
* Drag-to-reorder systems.

Image Prediction
----------------

Ren'Py is now better at predicting image usage. Along with predicting images
used by normal gameplay, it now attempts to predict images that are used by
screens one click away from the user. For example, during normal gameplay, it
will predict images on the first screen of the game menu. While at the game
menu, it will predict the other screens of the game menu, and also the images
the user will see when returning to the main menu. This prediction is
automatic, but only occurs when using screens.

Screens may be invoked at any time, in order to allow for image prediction,
unless they have a predict property of False. This means that displaying a
screen should not have side effects. (Most screens only have side effects
when a button is clicked or a bar changed - that's still fine.)

Ren'Py now supports hotspot caching for screen language imagemaps. When
:var:`config.developer` is true, Ren'Py will write a PNG file in the
game/cache/ directory containing image data for each of the hotspots in the
imagemap. If the cache file exists (regardless of the config.developer
setting) it will be loaded instead of loading the hotspot images. As the
cache file is often much smaller than the size of the hotspot images, it will
load faster and reduce image cache pressure, improving game performance. This
behavior only applies to screen language imagemaps, and can be disabled with
:var:`config.imagemap_cache`.

This should remove most of the need for :func:`renpy.cache_pin`. While not an
error, the use of cache pinning can cause unnecessary memory usage when the
wrong image is loaded.

Screens
-------

Ren'Py now ships with a default set of screens, which are used by the demo and
installed by default when a new game is created. You can find them in
template/game/screens.rpy, and they can be used by copying that file into
your project. These screens are not 100% compatible with the previous layout
system - for example, some styles have changed. That's why games must opt-in
to them.

The definition of the `items` parameter of the :ref:`choice-screen` and
:ref:`nvl-screen` screens has changed, and games will need to be updated to
work with the new version.

Character arguments beginning with ``show_`` are passed to the
:ref:`say-screen` screen. This allows things like show_side_image and
show_two_window to work with screens. The screens we ship support these
options.

The new :var:`config.imagemap_auto_function` variable allows the game-maker to
control the interpretation of the ``auto`` property of imagemaps and
imagebuttons.

The imagemap caching behavior described above applies only to screens.

The :func:`FilePageName` and :func:`FileSlotName` functions make it easier to
name slots

Other Improvements
------------------

Ren'Py 6.12 includes a number of other improvements:

* We've continued writing the new manual. Notably, we have rewritten the
  documentation for displayables.

* When taking a screenshot, :var:`config.screenshot_callback` is called. The
  default implementation of this function notifies the user of the location
  of the screenshot.

* The :func:`Solid` and :func:`Frame` displayables are now tiny and no
  longer take up (much) space in the image cache.

* We now create a log.txt file, which replaces the old opengl.txt, and can
  log other subsystems.

* Several missing properties have been added to the screen language.

* Ren'Py now treats filenames as if they were case-insensitive. This means
  that filename mismatches on Linux should no longer be a problem.


Bug Fixes
---------

* :lpbug:`680266` - Ensures that dynamic displayables update before
  Transforms that use them.

* :lpbug:`683412` - Do not crash if a shader fails to compile.

* Fixed a bug that caused Ren'Py to crash when the system volume was lowered
  to 0, but not muted.

* Fixed a bug that prevented :func:`Render.canvas` from working with the
  OpenGL renderer.


Ren'Py 6.11.2
=============

New Features
------------

This release includes four new themes, generously contributed by Aleema. You
can see and change to these new themes by clicking the "Choose Theme" button
in the launcher.

Software Update
---------------

The jEdit text editor included with Ren'Py has been updated to version 4.3.2,
a supported version that should be able to run most plugins.

Behavior Changes
----------------

The maximum default physical size of the Ren'Py window is now 102 pixels
smaller than the height of the screen. This should prevent Ren'Py from
creating windows that can't be resized since they are much bigger than the
screen.

Buttons now only pass key events to their children when they are focused. This
allows a screen language key statement to be used as the child of a button,
and only activate when the button is focused.

MoveTransition was rewritten to correctly deal with cases in which images
changed their order. This may lead to differences in behavior from the old
version, where the ordering was undefined.

Bug fixes
---------

Fixed :lpbug:`647686`, a regression that prevented sounds from looping
properly.

Fixed :lpbug:`661983`, which caused insensitive hotspots to default to the
idle, rather than ground, image when no insensitive image was supplied.

Fixed :lpbug:`647324`, where ImageDissolves are rendered as if specified with
alpha=True whether or not alpha=True was set.

Fixed a problem that caused the game to start when picking "No" after clicking
the (window-level) quit button.

Fixed a problem that prevented AnimatedValue from functioning properly when
delay was not 1.0. Thanks to Scout for the fix.

Fixed a problem that caused movies to display incorrectly when the screen was
scaled using OpenGL scaling.

Ren'Py 6.11.1
=============

New Features
------------

Add the :func:`AlphaBlend` displayable and the :func:`AlphaDissolve`
transition. These take two displayables, and use the alpha channel of a third
displayable to blend them together. (The third displayable is often an
animation, allowing the effect to change over time.)

The new :ref:`modes` system allows one to invoke callbacks when switching from
one type of interaction to another. This can be used, for example, to
automatically hide the window before transitions.

Imagemaps created using the screen language now only have a size equal to that
of their ground image. (Previously, they took up the entire screen.) This
change makes it easier to position an imagemap at a different location on
screen, such as the bottom.

Imagemaps now take an alpha argument. If true (the default), hotspots are only
focused if the mouse is over a non-transparent part of the idle or hover
image. If set to false, the hotspot is focused whenever the mouse is within
its boundaries.

Added the :func:`renpy.focus_coordinates` function, which returns the
coordinates of the currently focused displayable, when possible.

The new :func:`renpy.notify` function and :func:`Notify` action make it simple
to flash small status messages on the screen, such as might be used to notify
the user of a completed quicksave or screenshot.

The new :func:`HideInterface` action allows the interface to temporarily be
hidden, as a screen language action.

The developer menu now includes a command that will list all the files in the
game directory.

The urllib and urllib2 modules from the Python standard library are now
distributed as part of Ren'Py. These modules allow data to be retrieved from
web servers.

The launcher now includes an experimental updater, that makes it easier to
update to the latest pre-release. Hitting shift+U at the launcher's main
screen will cause Ren'Py to be updated.

Fixes
-----

:func:`MoveTransition` now respects the xoffset and yoffset parameters.

Fixed several bugs with screen-language imagemaps.

Fixed a bug (#626303) that was caused by an incorrect texture unit check.
Thanks to tmrwiz for the fix.

Transforms no longer cause a divide by zero exception when the zoom, xzoom, or
yzoom properties are 0.

Clockwise and counterclockwise revolution in transforms now works.

Fixed a bug with scaling, that occurred when switching between the scaled
software and GL renderers.

Hidden screens are no longer considered when assigning default focus.

FieldValues with max_is_zero set to True now work properly. Thanks to
SleepKirby for the fix.




Ren'Py 6.11.0
=============

OpenGL Support
--------------

Ren'Py will now take advantage of a computer's OpenGL hardware acceleration,
if supported. This OpenGL support has several user-visible changes:

* The window containing a Ren'Py game can be resized or maximized, using
  standard window controls. When the window's aspect ratio does not match the
  game's aspect ratio, black bars will be added.

* Displaying in full-screen mode should not change the monitor's resolution.
  This will prevent the game from being distorted when displayed on a monitor
  with a different aspect ratio.

* Unless disabled in the video driver configuration, Ren'Py will use
  vertical blank synchronization, eliminating image tearing.

* GPU rendering is used, which should make drawing the screen faster in most
  circumstances.

Software rendering is still supported, and Ren'Py will automatically fall back
to software rendering if it detects an improperly configured video card.

You can test that Ren'Py is in OpenGL mode by attempting to resize the window.
If it's resizable, it's OpenGL, otherwise, software rendering is being used.


Screens and Screen Language
---------------------------

This release introduces a new screen system, which allows one to use the new
screen language to declaratively specify portions of the user interface. The
screen language supersedes layouts, overlay functions, imagemaps, and most
other means of customizing the out-of-game menus and the in-game screens.

The previous way of customizing the behavior of the game menu, the layout
system, had problems, especially when using imagemap layouts. Screens were
single-purpose, and it would be difficult to (for example) load a quick-save
game from the main menu, without extensive Python code.

The screen system addresses this by providing a pool of functionality, in the
form of Actions and BarValues. This makes it possible to pick and choose
functionality, and add it to screens as is deemed necessary.

Transform Changes
-----------------

* If a transform does not define one of the position properties
  :propref:`xpos`, :propref:`ypos`, :propref:`xanchor`, or
  :propref:`yanchor`, that property will be taken from the transform's child,
  if the defines that property.

  This makes it possible to have one transform control a displayable's
  vertical motion, and the other control the horizontal. But this is
  incompatible with previous behavior, and so can be disabled with the
  :var:`config.transform_uses_child_position` variable.

* The new config.default_transform variable allows a transform to specify
  the initial transform properties of an image that does not have a more
  specific transform applied to it. Its default value is center, a transform
  that shows the image at the center-bottom of the screen.

  This can lead to a behavior change. When an image is shown, and then shown
  transforms, the transform will be initialized to the bottom center of the
  screen, not the top-left. The reset transform can be used to reset the
  position to the top-left.

* Transform (and ui.transform) have been changed so that their arguments can
  now be prefixed with a style prefix. One can write
  ui.transform(idle_rotate=30, hover_rotate=90) and have it work.

* Added the rotate_pad transform property, which controls how Transform pads
  rotated displayables. When set to False, _not_ the default, it's now
  possible to rotate a (100, 50) displayable by 90 degrees, and have the
  result be (50, 100) in size.

Other Changes
-------------

* The Ren'Py documentation is in the process of being rewritten. This
  changelog is now being maintained as part of the Ren'Py documentation.

* Added support for composite style properties, that allow several style
  properties to be set using a single parameter. The new composite style
  properties are:

  * pos - takes a pair, and uses it to set xpos and ypos.
  * anchor - takes a pair, and uses it to set xanchor and yanchor.
  * align - takes a pair, and uses it to set xalign and yalign. (And hence
    xpos, ypos, xanchor, and yanchor.)
  * area - take (x, y, height, width) pair, and tries to set properties
    such that the displayable will be placed inside the rectangle. This sets
    the xpos, ypos, xanchor, yanchor, xfill, yfill, xminimum, yminimum,
    xmaximum, and ymaximum properties.

* ui.add can now take transform properties as keyword arguments. If at least
  one transform property is present, ui.add will create a transform that
  wraps the displayable it's adding to the screen.

* The new :func:`LiveTile` displayable tiles its child, without consuming a
  large amount of memory to do so.

* :var:`config.quit_action` allows one to specify an action that is run when
  the quit button (in the corner of the window) is pressed.
  config.game_menu_action allows one to specify an action that is run when
  entering the game menu.

* The :var:`config.screenshot_crop` configuration variable controls the area
  of the screen that it stored when the user presses the screenshot key.

* The :func:`renpy.music.register_channel` method now has two additional
  parameters, file_prefix and file_suffix. These are prepended and appended
  to filenames provided to the registered channel, respectively.

* The new :func:`renpy.list_files` method returns a list of files in the
  game directory and archives. This can be used to write your own automatic
  image loading method, among other things.

* The interaction between Character and Text has been rewritten to ensure
  that text is only tokenized once. This required changing a few of the
  methods on ADVCharacter and NVLCharacter, so code that inherits from those
  classes should be checked.

* The distribution code has been moved into launcher/distribute.py. This
  file can be run from the command line to build distributions in shell
  scripts and other automated processes.

* When there are transparent areas on the screen, and
  :var:`config.developer` is true, the transparent areas are filled with a
  checkerboard pattern.

* The new ``input``, ``side``, ``grid``, and ``fixed`` styles were created,
  and the corresponding displayables use them by default.

* When a style is accessed at init-time, and doesn't exist, we divide it
  into two parts at the first underscore. If the second part corresponds to
  an existing style, we create a new style instead of causing an error.

* The python compiler has been rewritten to use the python ast module. This
  should both improve performance, and improve error handling for python
  syntax.

  Because of this change, Ren'Py now ships with and requires Python 2.6.

* The following numbered bugs were fixed:

  * 520276 - ctc does not appear when cps interrupted
  * 526297 - im.Rotozoom()s crash when Ren'Py is scaled down. (Thanks to
    Spiky Caterpillar for the bug report and fix.)
  * 543785 - Launcher bug on select Projects Directory
  * 583112 - rollback while a movie displayable is shown leaves a video
    frame onscreen
  * 595532 - Wrong text in tutorial game. (Thanks to Viliam Búr.)

* The following other bugs were fixed:

  * Renamed the internal show and hide methods of Displayable, so those
    names can once again be used by user-defined displayables.

  * Rewrote MultipleTransition (which is used by Fade) to fix some
    problems it was exhibiting.

  * Take the condition parameter to Character into account when
    determining if an nvl clear occurs before the next interaction.

Older Changelogs
================

Older changelogs can be found at:

    http://www.renpy.org/dl/6.10.2/CHANGELOG.txt
