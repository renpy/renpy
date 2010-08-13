Dealing With Display Problems
=============================

As of version 6.11, Ren'Py will take advantage of OpenGL display
hardware, if it's present and functional. Using OpenGL brings with it
several advantages, such as allowing vertical-blank synchronization
and scaling games to full-screen size while preserving aspect ratio.

On startup, Ren'Py will attempt to determine if the computer has
an OpenGL implementation that supports the features Ren'Py needs. It
will then test that OpenGL performance is sufficient to run Ren'Py
games.

If both tests pass, Ren'Py will continue in OpenGL mode. Otherwise, it
will revert to software rendering, a slower and less functional form
of rendering.

The best way to check if Ren'Py is using OpenGL rendering is to try to
resize the Ren'Py window. If the window can be resized, it's using
OpenGL support. If not, software rendering is being used.

A small fraction of systems may experience problems when running
OpenGL-accelerated Ren'Py games.  These problems are often due to
buggy graphics drivers, and so your first step to fixing them should
be to check for an update to your graphics card drivers.

If upgrading your video drivers does not fix the problem, you should
disable OpenGL support. To disable OpenGL support:

1. Hold down shift while starting Ren'Py.
2. From the "Graphics Acceleration" menu that appears, choose "Prefer Software Renderer".
3. Choose "Continue".

