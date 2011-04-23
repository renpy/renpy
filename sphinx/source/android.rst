=======
Android
=======

Ren'Py support devices running the Android operating system, such as
smartphones and tablets. While these devices do not support 100% of
Ren'Py's functionality, with minimal modification code can be packaged
and ported to these devices.


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

     
Downloading Ren'Py for Android
==============================

Ren'Py for Android is distributed as an engine that must be downloaded
separately from the games that use it. Games can be run by placing
them in the ``renpy`` directory on the device's external memory (SD
Card), or by downloading a game package. In the latter case, the
package will prompt the user to download Ren'Py if it is not
installed. 

Ren'Py for Android is distributed through the Android market, and as
.apk files available on the Ren'Py website. There are two versions of
Ren'Py for Android available:

* Ren'Py for Android
* Ren'Py for Android (Beta)

The beta version will be updated when a new version of Ren'Py is
undergoing test. While we will attempt to maintain compatibility
between Ren'Py versions, the beta version will games to be tested with
newer code.
     

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
  
Files
=====

Ren'Py for Android requires you to include android.txt, icon.png, and
.nomedia files as part of your game. These files should be placed in
the game's base directory. (This is the directory above the game
directory)

The layout should look like:

* mygame/android.txt
* mygame/icon.ong
* mygame/main.py
* mygame/.nomedia
* mygame/game/...


android.txt
-----------

The android.txt file is a file that's used to control how your game is
displayed in the list of games, and how it is displayed while
running. 

It is a Java Properties file, which consists of a list of
keys separated from values by an equals sign. An example android.txt
file is::

    title=The Question
    author=ATP Projects et al.
    api=61200
    orientation=landscape

The following keys are supported:

name
    The title of the game. Displayed in the list of games.

author
    The author of the game. Displayed in the list of games.

api
    The minimum version of Ren'Py this games requires. This should be
    a number, which is generated from the three components of
    the Ren'Py version multiplying the first component by 10000, the
    second component by 100, the third component by 1, and adding the
    numbers together. For example, version 6.12.0 would use an API
    version of 61200. 

    If the user has an older version of Ren'Py for Android, than the
    game requires, they will be asked to upgraded to a newer version.

orientation
    One of "portrait" or "landscape". This controls the orientation
    of the game on the device.


icon.png
--------

The icon.png file should be a small png file. It's used as an icon in
the list of games.

.nomedia
--------

The .nomedia file should be an empty file. It's used to tell Android
not to scan this directory for media files. If it didn't exist, then
image and audio files used by the game would be indexed and added
to the various galleries on the device.


Testing the Game
================

To test the game, place it onto the device's external storage (usually
the SD card). This can be done in two ways:

Mounting the Card
-----------------

The first is to mount the devices external storage (usually a SD card)
on your computer, creating a ``renpy`` directory on that device, and
then placing your game's directory underneath that. Then unmount the
card so that the device can read it before running Ren'Py.

ADB Push
--------

The game can be pushed to the device using the adb tool, which can be
downloaded as part of the `Android SDK
<http://developer.android.com/sdk/index.html>`_. It's useful to place
the adb command into your path.

The game must be placed into a directory underneath the renpy
directory on the device's sdcard, using a command like::

   adb push mygame /sdcard/renpy/mygame

Running
-------

Once the game is on the device, launching Ren'Py will display it in a
list of games. Choosing the game from this list will launch it.

If the game encounters problems, the traceback.txt, errors.txt, and
log.txt files will be created in the directory on the SD card storing
the game.


Packaging
=========

.. note::

    While the Mac, Windows, and Linux platforms are easy to build
    distributions for, Android is a bit harder. It requires a large
    number of external tools to build an APK and place it in the
    Android market.

Ren'Py games can be converted to .apk packages for use in the Android
market. This is done using the renpy-apk tool, downloadable from the
`Ren'Py download page <http://www.renpy.org/latest.html>`_. 

Please see the `Pygame Subset for Android documentation <http://www.renpy.org/pygame/releasing.html>`_
for instructions on how to use this tool. Packaging a Ren'Py game will
involve a command that looks like::

    ./build.py --dir mygame --package com.domain.mygame \
        --name "My Game" --version 1.0 debug

Note that although the build command is identical, you must user the
Ren'Py renpy-apk tool to package a Ren'Py game.
