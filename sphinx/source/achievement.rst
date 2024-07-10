.. _achievement:

Achievements
============

The Achievement module allows the developer to grant achievements to the
player, to clear achievements, and to determine if an achievement has been
granted. It also allows the recording of progress towards an achievement.

By default, the achievement stores information in the persistent file. If
Steam support is available and enabled, achievement information is
automatically synchronized with Steam.

Steam support must be added to Ren'Py, to ensure that it is only distributed
by creators that have been accepted to the Steam partner program. To install
it, choose "preferences", "Install libraries", "Install Steam Support".


.. include:: inc/achievement


Variables that control achievements are:

.. var:: achievement.steam_position = None

    If not None, this sets the position of the steam notification popup.
    This must be a string, one of "top left", "top right", "bottom left",
    or "bottom right".

.. var:: config.steam_appid = None

    If not None, this should be the Steam appid. Ren'Py will automatically
    set this appid when it starts. This needs to be set using the define
    statement::

        define config.steam_appid = 12345

.. var:: config.automatic_steam_timeline = True

    If true, when run under Steam, the game will automatically update the Steam Timeline.

    This currently consists of:

    * Updating the state description to match :var:`save_name`, if the variables is set.
    * Updating the game mode to reflect when the player is inside a menu.


Steamworks API
--------------

When Steam is available, a ctypes-based binding to the Steamworks API is
available as ``achievement.steamapi``. The binding is an instance of the
steamapi module, as found `here <https://github.com/renpy/renpy-build/blob/master/steamapi/steamapi.py>`_,
and represents a machine translation of the C++ Steamworks API to Python.

In addition, a large number of functions are available in the achievement.steam object, if and only
if the Steamworks API is available.

.. var:: achievement.steam

    If Steam initialized successfully, this is a namespace with high-level Steam methods. If Steam did not
    initialize, this is None. Always check that this is not None before calling a method.

Steam Apps
^^^^^^^^^^

.. include:: inc/steam_apps

Steam Overlay
^^^^^^^^^^^^^

.. include:: inc/steam_overlay

Steam Stats
^^^^^^^^^^^

.. include:: inc/steam_stats

Steam Timeline
^^^^^^^^^^^^^^

.. include:: inc/steam_timeline

Steam User
^^^^^^^^^^

.. include:: inc/steam_user

Steam Workshop
^^^^^^^^^^^^^^

.. include:: inc/steam_ugc
