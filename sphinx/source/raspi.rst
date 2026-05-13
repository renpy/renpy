Raspberry Pi
============

Ren'Py has limited support for running on the Raspberry Pi. It's been
demonstrated to run on the Raspberry Pi 3B, but may run on other models.

It's important to realize that the Raspberry Pi is a very limited system,
even compared to iOS and Android smartphones. As a result, not every Ren'Py
game will run well – or at all – on a Raspberry Pi. What's more, it's possible
to crash Ren'Py by allowing a game to use more RAM than the system has available
to it.

When the Raspberry Pi is configured correctly, Ren'Py should run using the
device's hardware OpenGL ES. This means that it has the same limitations as
the Android and iOS platforms, with respect to :propref:`focus_mask` not working.


Configuring the Raspberry Pi
----------------------------

Before Ren'Py is used, the Raspberry Pi should be reconfigured, using the
raspi-config tool. These settings are under advanced options.

* Memory Split: 256 MB
* Resolution: 1280x720 or smaller
* GL Driver: GL (Fake KMS)

After changing the settings, reboot the Raspberry Pi.

Configuring Ren'Py
------------------

Running on a Raspberry Pi requires the Arm Linux SDK. This version of
Ren'Py includes support for all other platforms, and can be downloaded
from the downloads pages for Ren'Py 7.5 and later.

Once you have the ARM-Linux SDK, untar it, and change in to the newly-created
directory.

Running a Game
--------------

As the Raspberry Pi is a resource-limited platform, we recommend avoiding
the Ren'Py launcher. Instead, we suggest using renpy.sh directly to launch
the project, using a command like::

    ./renpy.sh /path/to/project

This same approach can be used to play Ren'Py games that do not directly
support the Raspberry Pi.
