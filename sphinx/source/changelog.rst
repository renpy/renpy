==============
Full Changelog
==============

Ren'Py 6.11.0
=============

OpenGL Support
--------------

Screens and Screen Language
---------------------------

TODO: Document config.screen_layers.

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
  screen. [doc]

  This can lead to a behavior change. When an image is shown, and then
  shown transforms, the transform will be initialized to the bottom
  center of the screen, not the top-left. The reset transform can be
  used to reset the position to the top-left.

* Transform (and ui.transform) have been changed so that their
  arguments can now be prefixed with a style prefix. One can write
  ui.transform(idle_rotate=30, hover_rotate=90) and have it
  work. [doc]

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
  screen. [doc]

* The new LiveTile displayable tiles its child, without consuming a
  large amount of memory to do so. [doc]

* config.quit_action allows one to specify an action that is run when
  the quit button (in the corner of the window) is pressed.
  config.game_menu_action allows one to specify an action that is run
  when entering the game menu. [doc]

* The config.screenshot_crop configuration variable controls the area of
  the screen that it stored when the user presses the screenshot key. [doc]

* The renpy.music.register_channel method now has two additional
  parameters, file_prefix and file_suffix. These are prepended and
  appended to filenames provided to the registered channel,
  respectively.
  
* The new renpy.list_files method returns a list of files in the game
  directory and archives. This can be used to write your own automatic
  image loading method, among other things.

* The distribution code has been moved into launcher/distribute.py. This
  file can be run from the command line to build distributions in shell
  scripts and other automated processes.

* When there are transparent areas on the screen, and
  :var:`config.developer` is true, the transparent areas are filled
  with a checkerboard pattern.
  
* The python compiler has been rewritten to use the python ast module.
  This should both improve performance, and improve error handling for
  python syntax. 

* The following numbered bugs were fixed:

  * lp:526297 - im.Rotozoom()s crash when Ren'Py is scaled down. (Thanks to Spiky Caterpillar for the bug report and fix.)

* Renamed the internal show and hide methods of Displayable, so those
  names can once again be used by user-defined displayables.

* Rewrote MultipleTransition (which is used by Fade) to fix some
  problems it was exhibiting.




