Chrome OS/Chromebook
====================

There are two ways to run Ren'Py under Chrome OS.

Android on Chrome OS
--------------------

The easiest way to make a game available for Chrome OS is to package it for
Android, as described in the :ref:`Android documentation <android>`. Ren'Py's
Android support was designed with Chrome OS in mind as well.

This mode only supports playing games, not developing new games.

Linux on Chrome OS
------------------

Ren'Py games and the Ren'Py SDK can also be installed on a Chromebook. This allows
you to develop Ren'Py games on your Chromebook.

To install it:

1. Install Linux for Chrombebook, as described at https://support.google.com/chromebook/answer/9145439?hl=en .

2. Change the Crosstini GPU Support setting to enabled, by typing chrome://flags/#crostini-gpu-support, and choosing enable.

3. Restart your Chromebook.

4. Upgrade Linux, by launching a terminal, and running::

    sudo apt update
    sudo apt dist-upgrade

5. Restart your Chromebook, again.

To install a version of Ren'Py, open a terminal and run::

    wget https://www.renpy.org/dl/7.4.0/renpy-7.4.0-sdk.tar.bz2
    tar xaf renpy-7.4.0-sdk.tar.bz2

To run that version of Ren'Py, open a terminal and run::

    cd ~/ab/renpy-7.4.0-sdk
    ./renpy.sh

Note that this works with other versions of Ren'Py if you change 7.4.0
for another version.
