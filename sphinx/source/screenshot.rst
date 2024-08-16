Screenshots
===========

Ren'Py includes built-in functionality for taking screenshots of the game, as well as of displayables
in the game. The latter is suitable for creating "paper dolls" made of multiple displayables and saving
them to disk for the player's later use, such as an avatar creator.

When Ren'Py takes a screenshot, of the entire screen or a displayable, the screenshot will be taken
at the drawable size, after window scaling and High DPI adjustments are applied. This generally
captures what the user is seeing or would be seeing, rather than the native size of the assets.

By default, capturing a screenshot is bound to the 's' key.

There are a few screenshot-related actions and screen functions.

* :class:`Screenshot`
* :class:`FileScreenshot`
* :class:`FileTakeScreenshot`

Functions
---------

There are also functions that can be used to take screenshots:

.. include:: inc/screenshot
