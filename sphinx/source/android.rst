=======
Android
=======

Ren'Py support devices running the Android operating system, such as
smartphones and tablets. While these devices do not support 100% of
Ren'Py's functionality, with minimal modification code can be packaged
and ported to these devices.

RAPT - the Ren'Py Android Packaging Tool - is a program, downloaded separately
from Ren'Py, that creates an Android package for testing or release purposes.


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


Platform Differences
====================

There are many important differences between the touch-based Android
platform and the mouse-based platforms that Ren'Py supports. Changes
due to the Android software and hardware are:

* The touchscreen is treated as if it was a mouse. However, it will
  only produce mouse events when the user is actively touching the
  screen. When the user is not touching the screen, the virtual
  pointer will move to the upper-left corner of the screen.

* :func:`ImageDissolve`, :func:`AlphaDissolve`, and :func:`AlphaBlend`
  are not supported.

* Functions that render to a texture can only render an opaque
  texture. This means that the :func:`Dissolve` and :func:`Pixellate`
  transitions will only produce opaque output.

* The :propref:`focus_mask` property is not supported. It will be
  treated as if all pixels in the mask are opaque.

* Movie playback is not supported.

* Launching the web browser is not supported.

* Some python modules (including network communication) modules are
  not supported.

* Ren'Py cannot change the device volume. However, the android volume
  buttons work normally.

In addition, there are a few changes that may be necessary due to
human factors:

* Since Android smartphones can be smaller than a computer monitor, it
  may be necessary to increase text size.

* Since touch input is less accurate than mouse input, touch-based
  buttons need to be larger than mouse-based ones.

To help you adapt to these differences, Ren'Py for Android
automatically selects a screen variant of ``touch``. It also
selects screen variants of ``phone`` or ``tablet`` based on the
device's screen size. See :ref:`screen-variants` for more information.

.. include:: android-packaging.rst

