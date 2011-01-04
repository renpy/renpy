==============
Full Changelog
==============

Ren'Py 6.12.0
-------------

Ren'Py now support hotspot caching for screen language imagemaps. When
:var:`config.developer` is true, Ren'Py will write a PNG file in the
game/cache/ directory containing image data for each of the hotspots
in the imagemap. If the cache file exists (regardless of the
config.developer setting) it will be loaded instead of loading the
hotspot images. As the cache file is often much smaller than the size
of the hotspot images, it will load faster and reduce image cache
pressure, improving game performance. This behavior only applies to
screen language imagemaps, and can be disabled with
:var:`config.imagemap_cache`.


Ren'Py 6.11.2
=============

New Features
------------

This release includes four new themes, generously contributed by
Aleema. You can see and change to these new themes by clicking the
"Choose Theme" button in the launcher.

Software Update
---------------

The jEdit text editor included with Ren'Py has been updated to version
4.3.2, a supported version that should be able to run most plugins.

Behavior Changes
----------------

The maximum default physical size of the Ren'Py window is now 102
pixels smaller than the height of the screen. This should prevent
Ren'Py from creating windows that can't be resized since they are much
bigger than the screen.

Buttons now only pass key events to their children when they are
focused. This allows a screen language key statement to be used as the
child of a button, and only activate when the button is focused.

MoveTransition was rewritten to correctly deal with cases in which
images changed their order. This may lead to differences in behavior
from the old version, where the ordering was undefined.

Bug fixes
---------

Fixed :lpbug:`647686`, a regression that prevented sounds from looping
properly.

Fixed :lpbug:`661983`, which caused insensitive hotspots to default to
the idle, rather than ground, image when no insensitive image was
supplied.

Fixed :lpbug:`647324`, where ImageDissolves are rendered as if
specified with alpha=True whether or not alpha=True was set.

Fixed a problem that caused the game to start when picking "No" after
clicking the (window-level) quit button. 

Fixed a problem that prevented AnimatedValue from functioning properly
when delay was not 1.0. Thanks to Scout for the fix.

Fixed a problem that caused movies to display incorrectly when the
screen was scaled using OpenGL scaling.
  
Ren'Py 6.11.1
=============

New Features
------------

Add the :func:`AlphaBlend` displayable and the :func:`AlphaDissolve`
transition. These take two displayables, and use the alpha channel of
a third displayable to blend them together. (The third displayable is
often an animation, allowing the effect to change over time.)

The new :ref:`modes` system allows one to invoke callbacks when
switching from one type of interaction to another. This can be used,
for example, to automatically hide the window before transitions.

Imagemaps created using the screen language now only have a size equal
to that of their ground image. (Previously, they took up the entire
screen.) This change makes it easier to position an imagemap at a
different location on screen, such as the bottom.

Imagemaps now take an alpha argument. If true (the default), hotspots
are only focused if the mouse is over a non-transparent part of the
idle or hover image. If set to false, the hotspot is focused whenever
the mouse is within its boundaries.

Added the :func:`renpy.focus_coordinates` function, which returns the
coordinates of the currently focused displayable, when possible.

The new :func:`renpy.notify` function and :func:`Notify` action make
it simple to flash small status messages on the screen, such as might
be used to notify the user of a completed quicksave or screenshot.

The new :func:`HideInterface` action allows the interface to
temporarily be hidden, as a screen language action.

The developer menu now includes a command that will list all the files
in the game directory.

The urllib and urllib2 modules from the Python standard library are
now distributed as part of Ren'Py. These modules allow data to be
retrieved from web servers.

The launcher now includes an experimental updater, that makes it easier
to update to the latest pre-release. Hitting shift+U at the launcher's
main screen will cause Ren'Py to be updated.

Fixes
-----

:func:`MoveTransition` now respects the xoffset and yoffset
parameters.

Fixed several bugs with screen-language imagemaps.

Fixed a bug (#626303) that was caused by an incorrect texture unit
check. Thanks to tmrwiz for the fix.

Transforms no longer cause a divide by zero exception when the zoom,
xzoom, or yzoom properties are 0.

Clockwise and counterclockwise revolution in transforms now works.

Fixed a bug with scaling, that occured when switching between the
scaled software and GL renderers.

Hidden screens are no longer considered when assigning default focus.

FieldValues with max_is_zero set to True now work properly. Thanks to
SleepKirby for the fix.




Ren'Py 6.11.0
=============

OpenGL Support
--------------

Ren'Py will now take advantage of a computer's OpenGL hardware
acceleration, if supported. This OpenGL support has several
user-visible changes:

* The window containing a Ren'Py game can be resized or maximized,
  using standard window controls. When the window's aspect ratio does
  not match the game's aspect ratio, black bars will be added.

* Displaying in full-screen mode should not change the monitor's
  resolution. This will prevent the game from being distorted when
  displayed on a monitor with a different aspect ratio.

* Unless disabled in the video driver configuration, Ren'Py will use
  vertical blank synchronization, eliminating image tearing.

* GPU rendering is used, which should make drawing the screen faster
  in most circumstances.

Software rendering is still supported, and Ren'Py will automatically
fall back to software rendering if it detects an improperly configured
video card.

You can test that Ren'Py is in OpenGL mode by attempting to resize the
window. If it's resizable, it's OpenGL, otherwise, software rendering
is being used.

  
Screens and Screen Language
---------------------------

This release introduces a new screen system, which allows one to use
the new screen language to declaratively specify portions of the user
interface. The screen language supersedes layouts, overlay functions,
imagemaps, and most other means of customizing the out-of-game menus
and the in-game screens.

The previous way of customizing the behavior of the game menu, the
layout system, had problems, especially when using imagemap
layouts. Screens were single-purpose, and it would be difficult to
(for example) load a quick-save game from the main menu, without
extensive Python code.

The screen system addresses this by providing a pool of functionality,
in the form of Actions and BarValues. This makes it possible to pick
and choose functionality, and add it to screens as is deemed
necessary.

Transform Changes
-----------------

* If a transform does not define one of the position properties
  :propref:`xpos`, :propref:`ypos`, :propref:`xanchor`, or :propref:`yanchor`,
  that property will be taken from the transform's child, if the
  defines that property.

  This makes it possible to have one transform control a displayable's
  vertical motion, and the other control the horizontal. But this is
  incompatible with previous behavior, and so can be disabled with the
  :var:`config.transform_uses_child_position` variable.

* The new config.default_transform variable allows a transform to
  specify the initial transform properties of an image that does not
  have a more specific transform applied to it. Its default value is
  center, a transform that shows the image at the center-bottom of the
  screen.

  This can lead to a behavior change. When an image is shown, and then
  shown transforms, the transform will be initialized to the bottom
  center of the screen, not the top-left. The reset transform can be
  used to reset the position to the top-left.

* Transform (and ui.transform) have been changed so that their
  arguments can now be prefixed with a style prefix. One can write
  ui.transform(idle_rotate=30, hover_rotate=90) and have it
  work. 

* Added the rotate_pad transform property, which controls how
  Transform pads rotated displayables. When set to False, _not_ the
  default, it's now possible to rotate a (100, 50) displayable by 90
  degrees, and have the result be (50, 100) in size. 

Other Changes
-------------

* The Ren'Py documentation is in the process of being rewritten. This
  changelog is now being maintained as part of the Ren'Py
  documentation.

* Added support for composite style properties, that allow several style
  properties to be set using a single parameter. The new composite style
  properties are:

  * pos - takes a pair, and uses it to set xpos and ypos.
  * anchor - takes a pair, and uses it to set xanchor and yanchor.
  * align - takes a pair, and uses it to set xalign and yalign. (And
    hence xpos, ypos, xanchor, and yanchor.)
  * area - take (x, y, height, width) pair, and tries to set properties
    such that the displayable will be placed inside the rectangle. This 
    sets the xpos, ypos, xanchor, yanchor, xfill, yfill, xminimum, yminimum,
    xmaximum, and ymaximum properties.

* ui.add can now take transform properties as keyword arguments. If at
  least one transform property is present, ui.add will create a
  transform that wraps the displayable it's adding to the
  screen. 

* The new :func:`LiveTile` displayable tiles its child, without consuming a
  large amount of memory to do so.

* :var:`config.quit_action` allows one to specify an action that is run when
  the quit button (in the corner of the window) is pressed.
  config.game_menu_action allows one to specify an action that is run
  when entering the game menu. 

* The :var:`config.screenshot_crop` configuration variable controls the area of
  the screen that it stored when the user presses the screenshot key. 

* The :func:`renpy.music.register_channel` method now has two additional
  parameters, file_prefix and file_suffix. These are prepended and
  appended to filenames provided to the registered channel,
  respectively.
  
* The new :func:`renpy.list_files` method returns a list of files in the game
  directory and archives. This can be used to write your own automatic
  image loading method, among other things.

* The interaction between Character and Text has been rewritten to ensure
  that text is only tokenized once. This required changing a few of the
  methods on ADVCharacter and NVLCharacter, so code that inherits from
  those classes should be checked.
  
* The distribution code has been moved into launcher/distribute.py. This
  file can be run from the command line to build distributions in shell
  scripts and other automated processes.

* When there are transparent areas on the screen, and
  :var:`config.developer` is true, the transparent areas are filled
  with a checkerboard pattern.

* The new ``input``, ``side``, ``grid``, and ``fixed`` styles were created,
  and the corresponding displayables use them by default. 

* When a style is accessed at init-time, and doesn't exist, we divide it
  into two parts at the first underscore. If the second part corresponds
  to an existing style, we create a new style instead of causing an error.
  
* The python compiler has been rewritten to use the python ast module.
  This should both improve performance, and improve error handling for
  python syntax.

  Because of this change, Ren'Py now ships with and requires Python 2.6.

* The following numbered bugs were fixed:

  * 520276 - ctc does not appear when cps interrupted
  * 526297 - im.Rotozoom()s crash when Ren'Py is scaled down. (Thanks to Spiky Caterpillar for the bug report and fix.)
  * 543785 - Launcher bug on select Projects Directory
  * 583112 - rollback while a movie displayable is shown leaves a video frame onscreen
  * 595532 - Wrong text in tutorial game. (Thanks to Viliam Búr.)
  
* The following other bugs were fixed:
  
  * Renamed the internal show and hide methods of Displayable, so those
    names can once again be used by user-defined displayables.

  * Rewrote MultipleTransition (which is used by Fade) to fix some
    problems it was exhibiting.

  * Take the condition parameter to Character into account when determining
    if an nvl clear occurs before the next interaction.



