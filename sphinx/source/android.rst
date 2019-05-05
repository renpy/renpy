.. _android:

=======
Android
=======

Ren'Py support devices running the Android operating system, such as
smartphones and tablets. While these devices do not support 100% of
Ren'Py's functionality, with minimal modification visual novels can be
packaged and ported to these devices.

RAPT – the Ren'Py Android Packaging Tool – is a program, downloaded separately
from Ren'Py, that creates an Android package for testing or release purposes.

Required Language
=================

Some of the libraries used by RAPT are licensed under the terms
of the GNU Lesser/Library General Public License. You'll need to comply
with the terms of that license to distribute Ren'Py. We believe including
the following language in your app's description will suffice, but check
with a lawyer to be sure.

    This program contains free software licensed under a number of licenses,
    including the GNU Lesser General Public License. A complete list of
    software is available at https://www.renpy.org/l/license/.


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

* Movie playback in fullscreen mode can only use
  media formats that are supported by Android devices. See
  `this page <http://developer.android.com/guide/appendix/media-formats.html>`_
  for a list of supported video formats.

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


.. highlight:: none

.. _android-building:

Building Android Applications
=============================


Ren'Py contains tools that help you take a packaging-centric approach
to Android game development. In this approach, you will use a PC to
build an Android package and upload it to your device. You can then
run the game like any Android application. When it works correctly,
you can upload the package you make to Google Play and other app
stores.

Building an Android application consists of four steps:

1. Download and install the Java Development Kit
   and Android USB Drivers (scroll down for links).

2. Use the launcher to install the Android SDK and create keys.

3. Use the launcher to configure the Android build.

4. Use the launcher to build the Android application.

Once you've finished these steps, you'll have a runnable Android
package. You'll only need to run step 3 when you decide to make changes to your
game's configuration or when configuring a new game entirely; you'll run step
4 most often, whenever you need to make a new build of your game.


Step 1: Installing the Dependencies
-----------------------------------

There are three things you may need to manually download and install
before you can build packages:

**Java Development Kit.**
The Java Development Kit (JDK) contains several tools that are used by
|PGS4A|, including the tools used to generate keys and sign
packages. It can be downloaded from:

    http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

You'll need version 8 of the JDK.

Please note that the developer-focused JDK is different from the
user-focused JRE, and you'll need the JDK to create Android packages.


**Android Device.**
You'll also want to set your device up for development. You'll want to enable
developer mode on your device, and set up your computer for Android development.
Instructions on how to set up your computer can be found at:

    https://developer.android.com/studio/run/device

You can also run your app in an x86_64 image on the Android emulator (note
that x86 is not supported). Setting the emulator up is outside of the scope
of this document.


Step 2: Set up the Android SDK and Development Environment
----------------------------------------------------------

The next step is to set up the Android SDK and the rest of your
development environment. This step will:

* Check that the JDK is installed properly.
* Install the Android SDK.
* Use the Android SDK to install the appropriate development
  packages.
* Create a signing key that will be used to sign packages that are
  placed on the market (android.keystore: this will be generated in the
  RAPT directory).

This step requires Internet access.

To perform this step, choose "Install SDK & Create Keys" from the
Android screen in the Ren'Py Launcher.

RAPT will report on what it's doing. It will also prompt you with
warnings about licenses, and ask if you want it to generate a key.

.. warning::

   The key generated by RAPT is created with a standard
   passphrase. You should really use keytool to generate your own
   signing keys.

    http://docs.oracle.com/javase/7/docs/technotes/tools/windows/keytool.html

   At the very least, you should keep the android.keystore file in
   a safe place. You should also back it up, because without the
   key, you won't be able to upload the generated applications.

If you don't want to download the SDK each time, you can create a file
named sdk.txt containing a single line that is the path to the
already-installed SDK.

Step 3: Configure Your Game
---------------------------

Before building a package, you must give Ren'Py some information
about the Android build of your game. To do this, choose "Configure"
from the Android screen of the Ren'Py launcher.

If you need to change the information – for example, if you release a
new version of your game – you can re-run the configure command. Your
previous choices will be remembered.

Step 4: Build and Install the Package
-------------------------------------

Finally, you can build and install the package. This is done with a
by connecting your Android device to your computer, and choosing
"Build & Install" from the Android screen of the Ren'Py launcher.
(The first time you install, your Android device may ask you
to authorize your computer to install applications.)

If you'd rather copy the game's apk file to your Android device manually,
choose "Build Package" from the Android screen of the Ren'Py launcher. Then
navigate to the 'bin' directory underneath the RAPT directory and copy the
appropriate file to your Android device. You will then need to find
the .apk file in your Android device using a file manager application and
open it to install the game.

Ren'Py allows you to select between two release modes, Debug and Release.
The debug mode is useful for testing, as it allows you to easily use Android
studio to view the logs or files on the device. Release produces a version
of the app suitable to upload to the various stores.

You will need to uninstall the app when switching between debug and
release builds.


Icon and Presplash Images
=========================

Icon
-----

Ren'Py will create an icon from your app from two files in the game's
base directory:

android-icon_foreground.png
    The foreground layer of the icon. This should be 432x432 pixels
    and transparent.


android-icon_background.png
    The background layer of the icon. This should be 432x432 pixels
    and opaque.

Android adaptive icons work by masking the two layers of the icon to an area that
is at least 132x132 pixels, in the center. The area outside of this safe
space may be shown, but it might be masked out, too. Bleeding outside
of the safe area is encouraged. The two layers might move a little relative
to each other when the icon is dragged around.

For more information about adaptive icons, please check out:

    https://medium.com/google-design/designing-adaptive-icons-515af294c783

Note that 1dp corresponds to 4 actual pixels.

When generating the application, Ren'Py will convert these files to an
appropriate size for each device, and will generate static icons for devices
that do not support adaptive icons.


Presplash
---------

The presplash is shown before Ren'Py fully loads, before the main splashscreen
starts. It's especially important on Android, as the first time Ren'Py runs
it will unpack supporting files, which make take some time.

android-presplash.jpg
    The image that's used when the app is loading. This should be surrounded
    by a monocolored border. That border is expanded to fill the screen.


.. _expansion-apk:

Google Play Expansion APKs
==========================

Ren'Py optionally supports the use of expansion APKs when used on a device
supporting Google Play. Expansion APKs allow Google Play to host games
larger than 50MB in size. Please see:

    http://developer.android.com/google/play/expansion-files.html

For information about expansion APKs work. Right now, only the
main expansion APK is supported, giving a 2GB limit. When an Expansion
APK is created, all game files will be placed in the
expansion APK. Ren'Py will transparently use these files.

To configure your game to use Expansion APKs, you'll need to set two
variables:

.. var:: build.google_play_key = "..."

    This is the Google Play license key associated with your application,
    which can be found on the "Services & APIs" tab associated with
    your application in the Google Play developer console. (Be sure to
    remove all spaces and newlines from the key.)

.. var:: build.google_play_salt = ( ... )

    This should be a tuple of 20 bytes, where each byte is represented as
    an integer between -128 and 127. This is used to encrypt license
    information returned from Google Play.

    A valid (if insecure) value for this variable is::

        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)

RAPT will place the expansion APK on the device when installing
the APK package on the device. The expansion APK will be an .obb file
found inside the bin subdirectory of the RAPT directory.

In normal operation, Google Play will place the expansion APK on the
device automatically when the user installs the application.
