Achievements
============

The Achievement module allows the developer to grant achievements to the
player, to clear achievements, and to determine if an achievement has been
granted. It also allows the recording of progress towards an achievement.

By default, the achievement stores information in the persistent file. If
Steam support is available and enabled, achivement information is
automatically synchronized with Steam.


.. include:: inc/achievement


Variables that control achievements are::

.. var:: achievement.steam_position = None

    If not None, this sets the position of the steam notification popup.
    This must be a string, one of "top left", "top right", "bottom left",
    or "bottom right".
