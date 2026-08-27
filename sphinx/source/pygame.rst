======
pygame
======

A lot of Ren'Py internals depend on a vendored reimplementation of the
pygame API, built on top of SDL. It is accessible as the ``renpy.pygame``
package::

    from renpy import pygame

When Ren'Py starts, this package is also registered under the ``pygame``
and ``pygame_sdl2`` names, so ``import pygame`` also works inside game
code.

Compatibility
-------------

Ren'Py's pygame tries to be compatible with the non-deprecated public API
of the `pygame-ce <https://github.com/pygame-community/pygame-ce>`_
project. If some things are missing, you can file a feature request to
have them added.

At the same time, Ren'Py's pygame adds extra things beyond the pygame
API, but those are considered an implementation detail. If you need some
non-standard API to be accessible, you can file a feature request to have
it exposed through the ``renpy`` namespace.

Submodules
----------

The following submodules are available. Note that the ``Surface`` and
``Rect`` classes are also available directly from the package root.

``color``
    The Color class and named colors.

``constants``
    Event types and other constants. The same constants are also available
    as ``locals``, and directly in the ``renpy.pygame`` namespace.

``controller``
    Game controller support.

``display``
    Display and window initialization and management.

``draw``
    Drawing shapes, such as rectangles, polygons, circles and lines, onto
    surfaces.

``event``
    Access to the event queue.

``gfxdraw``
    Antialiased drawing primitives.

``image``
    Loading and saving images. For example, ``pygame.image.save`` can save
    a surface to a PNG file.

``joystick``
    Joystick support.

``key``
    Keyboard state.

``mouse``
    Mouse state.

``power``
    Power state information.

``rect``
    The Rect class.

``scrap``
    Clipboard access.

``surface``
    The Surface class.

``time``
    Time-related functions, including the ``Clock`` class.

``transform``
    Surface transformations, such as scaling, rotation and flipping.
