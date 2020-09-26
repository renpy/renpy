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

As Rasberry Pi support doesn't ship with Ren'Py itself, it's necessary to
download two files. The first is the Linux version of the SDK, and the
second is the Raspberry Pi support files.

Untar the Linux version of the SDK, change into it, then untar the Raspberry
Pi support files. When done correctly, the SDK will have a lib/linux-armv7l
directory alongside lib/linux-i686 and lib/linux-x86_64.

Running a Game
--------------

As the Raspberry Pi is a resource-limited platform, we recommend avoiding
the Ren'Py launcher. Instead, we suggest using renpy.sh directly to launch
the project, using a command like::

    ./renpy.sh /path/to/project

