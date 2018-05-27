===
iOS
===

Ren'Py supports creating iOS apps that run on iPhone and iPad devices. As
creating an iOS app requires Apple-developed programs (like the Xcode IDE),
iOS apps can only be created on Macintosh computers.

Required Language
=================

Some of the libraries used by Ren'Py on iOS are licensed under the terms
of the GNU Lesser/Library General Public License. You'll need to comply
with the terms of that license to distribute Ren'Py. We believe including
the following language in your app's description will suffice, but check
with a lawyer to be sure.

    This program contains free software licensed under a number of licenses,
    including the GNU Lesser General Public License. A complete list of
    software is available at https://www.renpy.org/l/license/.

Work in Progress
================

The current Ren'Py iOS support is a work in progress. While it has been
used to release games to the Apple App Store, the default Ren'Py interface
does not comply with Apple's guidelines and will need to be changed.

Please let us know the results of getting your game through the App Store
approval process.


Platform Differences
====================

iOS is similar to Android, but differs from the mouse-based platforms
that Ren'Py supports. All of the :ref:`android platform differences <android-platform-differences>`
apply to iOS.

iOS does not support :class:`MultiPersistent`.

A list of video formats supported by iOS can be found
`here <https://developer.apple.com/library/ios/documentation/Miscellaneous/Conceptual/iPhoneOSTechOverview/MediaLayer/MediaLayer.html#//apple_ref/doc/uid/TP40007898-CH9-SW6>`_.


Testing and Emulation
=====================

For testing purposes, Ren'Py supports two iOS emulation modes. These
are accessed from the iOS screen of the launcher. Both modes simulate
running on a touchscreen, such that events only reach the game when
the mouse button is down.

iPhone
    This mode emulates an iPhone.

Tablet
    This mode emulates an iPad.

While these emulators can be used to quickly test your project, it's best to
also test on real hardware. The emulators do not deal with some human-factors
issues, like the size of a user's fingers.


Packaging
=========

Packaging a Ren'Py game for iOS is currently an involved process compared
to the other platforms Ren'Py supports. We currently assume you have some
experience with creating iOS apps, or can follow Apple's instructions.

Getting Started
---------------

Before you can package a Ren'Py game, you'll need to set up your Macintosh
to create iOS applications. This means setting up Xcode on your Mac,
enrolling in the iOS Developer Program, and creating a provisioning
profile that allows your apps to run on your iOS device.

The Apple-written `App Distribution Quick Start <https://developer.apple.com/library/ios/documentation/IDEs/Conceptual/AppStoreDistributionTutorial/Introduction/Introduction.html>`_
guide explains how to configure all of the above. We suggest working through
it, and even packaging a one of the template apps before moving on to
Ren'Py games.

Creating the Xcode Project
--------------------------

The first step in creating your iOS application is to create the Xcode project.
This is done by selecting "Create Xcode Project" from the iOS menu in the
Ren'Py launcher.

The name of the Xcode project is automatically chosen based on the name that
shows up in the launcher. The project is customized based this name, but
those customizations can be edited in Xcode.

Xcode projects created in this way are specific to a single version of
Ren'Py. After upgrading Ren'Py, you must create a new Xcode project for your
game, and repeat the project customizations.

Building the Project
--------------------

After the project has been created in Ren'Py, it can be opened in Xcode by
choosing "Launch Xcode" from the launcher. Once the project is open in Xcode,
it can be built and installed on the iOS device.

Updating the Project
--------------------

Choosing "Update Xcode Project" will copy the latest version of your
Ren'Py project into the Xcode project. This is suitable for when your project
files change, but not for when Ren'Py itself has been updated.


Customization
=============

Most customization is performed in the Xcode project. For example, the
icon, launch images, and orientations are all customized in Xcode.

Launch Images
-------------

When the application is run, the Launch Image (configure as part of the
Xcode project, outside of Ren'Py) will be displayed until Ren'Py is ready
to display the game's user interface.

Once Ren'Py finishes initializing, it will either resume the current game,
or run the splashscreen and main menu.


