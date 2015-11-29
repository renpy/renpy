=======
Android
=======

Ren'Py support devices running the Android operating system, such as
smartphones and tablets. While these devices do not support 100% of
Ren'Py's functionality, with minimal modification code can be packaged
and ported to these devices.

RAPT - the Ren'Py Android Packaging Tool - is a program, downloaded separately
from Ren'Py, that creates an Android package for testing or release purposes.

Required Language
=================

Some of the libraries used by Ren'Py on iOS are licensed under the terms
of the GNU Lesser/Library General Public License. You'll need to comply
with the terms of that license to distribute Ren'Py. We believe including
the following language in your app's description will suffice, but check
with a lawyer to be sure.

    This program contains free software licensed under a number of licenses,
    including the GNU Lesser General Public License. A complete list of
    software is available at http://www.renpy.org/doc/html/license.html.


User Instructions
=================

When a Ren'Py game has been launched on Android, the following
keybindings work:

`Home`
     Returns to the Android home screen, suspending the Ren'Py
     game. As part of the suspend process, Ren'Py will automatically
     save the game. If necessary, the save will be automatically
     loaded when the user returns to the game.

`Menu`
     Brings up the in-game menu, and returns to the game.

`Back`
     Rolls back.

`Volume Up`, `Volume Down`
     Controls Android's media volume.


.. _android-platform-differences:

Platform Differences
====================

There are many important differences between the touch-based Android
platform and the mouse-based platforms that Ren'Py supports. Changes
due to the Android software and hardware are:

* The touchscreen is treated as if it was a mouse. However, it will
  only produce mouse events when the user is actively touching the
  screen.

* Movie playback is only supported in fullscreen mode, and only with
  media formats that are supported by Android devices. See
  `this page <http://developer.android.com/guide/appendix/media-formats.html>`_
  for a list of supported video formats.

* Ren'Py cannot change the device volume. However, the android volume
  buttons work normally.

* Ren'Py can't handle transparency in buttons and imagemaps.
  (This is due to performance problems on some devices with the
  display modes needed to support deciding which pixels are
  transparent.)

In addition, there are a few changes that may be necessary due to
human factors:

* Since Android smartphones can be smaller than a computer monitor, it
  may be necessary to increase text size.

* Since touch input is less accurate than mouse input, touch-based
  buttons need to be larger than mouse-based ones.

To help you adapt to these differences, Ren'Py for Android
automatically selects screen variants based on the
device's screen size and capabilities. See :ref:`screen-variants` for
more information.


Testing and Emulation
=====================

For testing purposes, Ren'Py supports three Android emulation modes. These
are accessed from the Android screen of the launcher.

Phone
    This mode emulates an Android phone. Touch emulation is performed
    using the mouse, but only when the mouse button is held down. Escape
    is mapped to the menu button, and Page Up is mapped to the back button.

Tablet
    This mode emulates an Android tablet. Touch emulation is performed
    using the mouse, but only when the mouse button is held down. Escape
    is mapped to the menu button, and Page Up is mapped to the back button.

Television / OUYA
    This mode emulates a television-based Android device, such as the OUYA
    console. The keyboard is mapped to remote or controller input, with the
    arrow keys providing navigation. Select is enter, Escape is menu, and
    page-up is back.

    This mode also displays an overlay showing the Television-unsafe area.
    Content in the Television-unsafe area may not display on all Televisions.

While these emulators can be used to quickly test your project, it's best to
also test on real hardware. The emulators do not deal with some human-factors
issues, like the size of a user's fingers.


.. include:: android-packaging.rst

