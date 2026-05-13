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

Ren'Py runs on Android 5.0 and later, though older devices may lack the
resources to run larger games properly.

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

* Text input (such as :func:`renpy.input`) is limited to the input methods
  that do not require completions to work. (Western languages probably work,
  while other languages might not.)

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

Due to the security policy of mobile devices, MultiPersistent functionality
is limited only to this game and its updates, i.e. it cannot be shared by
another game.


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

Television
    This mode emulates a television-based Android device
    console. The keyboard is mapped to remote or controller input, with the
    arrow keys providing navigation. Select is enter, Escape is menu, and
    page-up is back.

    This mode also displays an overlay showing the Television-unsafe area.
    Content in the Television-unsafe area may not display on all televisions.

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

2. Use the launcher to install the Android SDK.

3. Use the launcher to generate keys.

4. Use the launcher to configure the Android build.

5. Use the launcher to build the Android application.

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
RAPT, including the tools used to generate keys and sign
packages. It can be downloaded from:

    https://adoptopenjdk.net/releases.html
    https://adoptium.net/temurin/releases/?version=21

You'll need version 21 of the JDK.

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

This step requires Internet access.

To perform this step, choose "Install SDK" from the
Android screen in the Ren'Py Launcher. RAPT will report on what it's
doing. It will also prompt you to accept the licenses.

If you don't want to download the SDK each time, you can create a file
named sdk.txt containing a single line that is the path to the
already-installed SDK.

Step 3: Generate keys
---------------------

After this, choose "Generate Keys" to generate Android and Bundle
keys for your package.

.. warning::

    The keys generated by RAPT are created with a standard
    passphrase. You need to make sure you do not lose access to these
    files.

    You should keep the android.keystore and bundle.keystore files in
    a safe place. You should also back it up, because without the
    key, you won't be able to upload the generated applications.

    You should make sure that these files are never made public,
    especially if version control is being used.

When creating Android keys, Ren'Py will back them up to the same place it
backs up script files. This isn't a substitute for making your own backups.

Step 4: Configure Your Game
---------------------------

Before building a package, you must give Ren'Py some information
about the Android build of your game. To do this, choose "Configure"
from the Android screen of the Ren'Py launcher.

If you need to change the information you can re-run the configure command.
Your previous choices will be remembered.

Step 5: Build and Install the Package
-------------------------------------

Finally, you can build and install the package.  You'll first want to
choose between one of the two release modes:

Play Bundle
    Play bundle releases are in the Android App Bundle (AAB) format,
    and are suitable only for upload to the Google Play store, though
    such releases can also be installed on Play-enabled Android devices.

    Play bundles may be up to 2 GB in size, but this is divided into
    4 500MB fast-follow pack files, with each file in your game assigned
    to one of the four bundles. This may be an issue with four files -
    a game won't be able to fit 5 files of 300 MB in size, as there will
    only be room for one in each of the four pack files.

Universal APK
    Universal APK release are suitable for direct installation onto
    Android devices, either through Ren'Py, ADB, non-Play app stores,
    or sideloading through the web.

    Universal APKs can be up to 2 GB in size, with no restrictions on
    the contents.

There are three commands which allow you to perform various combinations
of building the package, installing it on your device, and launching the
application for testing.

You may need to uninstall the app when switching between release modes.


Very Large Games
================

It's possible to build games that are larger than 2 GB. This is done using
the :doc:`downloader`, with a small game being included in the Play
bundle or Universal APK, and the rest of the game being downloaded
from a capable web server.


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

.. _android-presplash:

Presplash
---------

The presplash is shown before Ren'Py fully loads, before the main splashscreen
starts. It's especially important on Android, as the first time Ren'Py runs
it will unpack supporting files, which make take some time.

android-presplash.jpg
    The image that's used when the app is loading. This should be surrounded
    by 1px of a monocolored border. When displayed, the image is scaled to
    fit available space while preserving aspect ratio, and the rest of the
    screen is filled with the border color.

android-downloading.jpg
    The image that's used when the app is downloading assets from Google
    Play Asset delivery. This should be surrounded
    by 1px of a monocolored border. When displayed, the image is scaled to
    fit available space while preserving aspect ratio, and the rest of the
    screen is filled with the border color.

    A 20px-high progress bar is displayed 20px from the bottom, left, and
    right sides of the screen, showing download progress.

.. _pyjnius:

Pyjnius
=======

When running on Android, a version of the `Pyjnius <https://pyjnius.readthedocs.io/en/latest/>`__
library is available. This allows advanced creators to call into the Android
libraries.

It may be necessary to get the main activity. It can be found in the mActivity
field in the org.renpy.android.PythonSDLActivity class. For example::

    init python:
        if renpy.android:
            import jnius
            mActivity = jnius.autoclass("org.renpy.android.PythonSDLActivity").mActivity
        else:
            mActivity = None


.. _android-permissions:

Permissions
===========

While Ren'Py doesn't require additional permissions to run, if your
game uses Pyjnius to call into Android, it might be necessary to
request permissions. Ren'Py has a variable and two functions to
interact with the Android permissions system.

.. var:: build.android_permissions = [ ]

    This is a list of strings, with each string giving the full name
    of an Android permission. For example, "android.permission.WRITE_EXTERNAL_STORAGE".
    This simply declares that the application might request these permissions, it's
    necessary to use renpy.check_permission and renpy.request_permission as necessary
    to request the permission.

.. include:: inc/android_permission
