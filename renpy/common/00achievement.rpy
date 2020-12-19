# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

python early:

    # Should steam be enabled?
    config.enable_steam = True

init -1500 python in achievement:
    from store import persistent, renpy, config, Action

    # A list of backends that have been registered.
    backends = [ ]

    class Backend(object):
        """
        Achievement backends should inherit from this class, so new methods
        will be ignored.
        """


        def register(self, name, **kwargs):
            """
            Called to register a new achievement.
            """

        def grant(self, name):
            """
            Grants the achievement with `name`, if it has not already been
            granted.
            """

        def clear(self, name):
            """
            Clears the achievement with `name`, if it has been granted.
            """

        def clear_all(self):
            """
            Clears all achievements.
            """

        def progress(self, name, complete):
            """
            Reports progress towards the achievement with `name`.
            """

        def has(self, name):
            """
            Returns true if the achievement with `name` is unlocked.
            """

            return False

    class PersistentBackend(Backend):
        """
        A backend that stores achievements in persistent._achievements.
        """

        def __init__(self):
            if persistent._achievements is None:
                persistent._achievements = _set()

            if persistent._achievement_progress is None:
                persistent._achievement_progress = _dict()

        def grant(self, name):
            persistent._achievements.add(name)

        def clear(self, name):
            persistent._achievements.discard(name)

        def clear_all(self):
            persistent._achievements.clear()

        def has(self, name):
            return name in persistent._achievements

        def progress(self, name, complete):
            old = persistent._achievement_progress.get(name, 0)
            persistent._achievement_progress[name] = max(complete, old)

    def merge(old, new, current):
        if old is None:
            old = set()

        if new is None:
            new = set()

        return old | new

    def merge_progress(old, new, current):

        if old is None:
            old = { }
        if new is None:
            new = { }

        rv = _dict()
        rv.update(old)

        for k in new:
            if k not in rv:
                rv[k] = new[k]
            else:
                rv[k] = max(new[k], rv[k])

        return rv

    renpy.register_persistent("_achievements", merge)
    renpy.register_persistent("_achievement_progress", merge_progress)

    backends.append(PersistentBackend())

    steam_maximum_framerate = 15

    # The position of the steam notification popup. One of "top left", "top right",
    # "bottom left", or "bottom right".
    steam_position = None

    class SteamBackend(Backend):
        """
        A backend that sends achievements to Steam. This is only used if steam
        has loaded and initialized successfully.
        """

        def __init__(self):
            # A map from achievement name to steam name.
            self.names = { }
            self.stats = { }

            steam.retrieve_stats()
            renpy.maximum_framerate(steam_maximum_framerate)

        def register(self, name, steam=None, steam_stat=None, stat_max=None, stat_modulo=1, **kwargs):
            if steam is not None:
                self.names[name] = steam

            self.stats[name] = (steam_stat, stat_max, stat_modulo)

        def grant(self, name):
            name = self.names.get(name, name)

            renpy.maximum_framerate(steam_maximum_framerate)
            steam.grant_achievement(name)
            steam.store_stats()

        def clear(self, name):
            name = self.names.get(name, name)

            steam.clear_achievement(name)
            steam.store_stats()

        def clear_all(self):
            for i in steam.list_achievements():
                steam.clear_achievement(i)

            steam.store_stats()

        def progress(self, name, completed):

            orig_name = name

            completed = int(completed)

            if name not in self.stats:
                if config.developer:
                    raise Exception("To report progress, you must register {} with a stat_max.".format(name))
                else:
                    return

            current = persistent._achievement_progress.get(name, 0)

            steam_stat, stat_max, stat_modulo = self.stats[name]

            name = self.names.get(name, name)

            if (current is not None) and (current >= completed):
                return

            renpy.maximum_framerate(steam_maximum_framerate)

            if completed >= stat_max:
                steam.grant_achievement(name)
            else:
                if (stat_modulo is None) or (completed % stat_modulo) == 0:
                    steam.indicate_achievement_progress(name, completed, stat_max)

            steam.store_stats()

        def has(self, name):
            name = self.names.get(name, name)

            return steam.get_achievement(name)

    def steam_preinit():
        """
        This runs before steam.init(), and sets up the steam_appid
        from config.steam_appid.
        """

        import os

        if config.early_script_version is not None:
            return

        if config.steam_appid is None:
            return

        with open(os.path.join(config.renpy_base, "steam_appid.txt"), "w") as f:
            f.write(str(config.steam_appid) + "\n")

    # Are the steam libraries installed? Used by the launcher.
    has_steam = False

    try:
        import _renpysteam as steam
        has_steam = True
        renpy.write_log("Imported steam.")
    except Exception as e:
        steam = None
        renpy.write_log("Importing _renpysteam: %r", e)

    if steam is not None:

        want_version = 2

        if steam.version < want_version:
            raise Exception("_renpysteam module is too old. (want version %d, got %d)" % (steam.version, want_version))

        steam_preinit()

        if not config.enable_steam:
            steam = None
        elif steam.init():
            renpy.write_log("Initialized steam.")
            backends.insert(0, SteamBackend())
        else:
            renpy.write_log("Failed to initialize steam.")
            steam = None


    def register(name, **kwargs):
        """
        :doc: achievement

        Registers an achievement. Achievements are not required to be
        registered, but doing so allows one to pass information to the
        backends.

        `name`
            The name of the achievement to register.

        The following keyword parameters are optional.

        `steam`
            The name to use on steam. If not given, defaults to `name`.

        `stat_max`
            The integer value of the stat at which the achievement unlocks.

        `stat_modulo`
            If the progress modulo `stat_max` is 0, progress is displayed
            to the user. For example, if stat_modulo is 10, progress will
            be displayed to the user when it reaches 10, 20, 30, etc. If
            not given, this defaults to 0.
        """

        for i in backends:
            i.register(name, **kwargs)

    def grant(name):
        """
        :doc: achievement

        Grants the achievement with `name`, if it has not already been
        granted.
        """

        if not has(name):
            for i in backends:
                i.grant(name)

    def clear(name):
        """
        :doc: achievement

        Clears the achievement with `name`.
        """

        if has(name):
            for i in backends:
                i.clear(name)

    def clear_all():
        """
        :doc: achievement

        Clears all achievements.
        """

        for i in backends:
            i.clear_all()

    def progress(name, complete, total=None):
        """
        :doc: achievement
        :args: (name, complete)

        Reports progress towards the achievement with `name`, if that
        achievement has not been granted. The achievement must be defined
        with a completion amount.

        `name`
            The name of the achievement. This should be the name of the
            achievement, and not the stat.

        `complete`
            An integer giving the number of units completed towards the
            achievement.
        """

        if has(name):
            return

        for i in backends:
            i.progress(name, complete)

    def grant_progress(name, complete, total=None):
        progress(name, complete)

    def has(name):
        """
        :doc: achievement

        Returns true if the player has been granted the achievement with
        `name`.
        """

        for i in backends:
            if i.has(name):
                return True

        return False

    def sync():
        """
        :doc: achievement

        Synchronizes registered achievements between local storage and
        other backends. (For example, Steam.)
        """

        for a in persistent._achievements:
            for i in backends:
                if not i.has(a):
                    i.grant(a)

    class Sync(Action):
        """
        :doc: achievement

        An action that calls achievement.sync(). This is only sensitive if
        achievements are out of sync.
        """

        def __call__(self):
            sync()

        def get_sensitive(self):
            for a in persistent._achievements:
                for i in backends:
                    if not i.has(a):
                        return True
            return False

init 1500 python in achievement:

    # Steam position.
    if steam is not None:
        if steam_position == "top left":
            steam.set_overlay_notification_position(steam.POSITION_TOP_LEFT)
        elif steam_position == "top right":
            steam.set_overlay_notification_position(steam.POSITION_TOP_RIGHT)
        elif steam_position == "bottom left":
            steam.set_overlay_notification_position(steam.POSITION_BOTTOM_LEFT)
        elif steam_position == "bottom right":
            steam.set_overlay_notification_position(steam.POSITION_BOTTOM_RIGHT)
