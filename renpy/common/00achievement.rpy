# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

init -1500 python in achievement:
    from store import persistent, renpy


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

        def progress(self, name, complete, total):
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


        def grant(self, name):
            persistent._achievements.add(name)

        def clear(self, name):
            persistent._achievements.discard(name)

        def clear_all(self):
            persistent._achievements.clear()

        def has(self, name):
            return name in persistent._achievements

    def merge(old, new, current):
        return old | new

    renpy.register_persistent("_achievements", merge)

    backends.append(PersistentBackend())


    class SteamBackend(Backend):
        """
        A backend that sends achievements to Steam. This is only used if steam
        has loaded and initialized successfully.
        """

        def __init__(self):
            # A map from achievement name to steam name.
            self.names = { }

            steam.retrieve_stats()
#             steam.retrieve_stats(self.got_stats)

#         def got_stats(self):
#             renpy.restart_interaction()

        def register(self, name, steam=None, **kwargs):
            if steam is not None:
                self.names[name] = steam

        def grant(self, name):
            name = self.names.get(name, name)

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

        def progress(self, name, completed, total):
            name = self.names.get(name, name)

            steam.indicate_achievement_progress(name, completed, total)
            steam.store_stats()

        def has(self, name):
            name = self.names.get(name, name)

            return steam.get_achievement(name)

    try:
        import _renpysteam as steam

        if steam.init():
            backends.append(SteamBackend())
    except:
        pass


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

    def progress(name, complete, total):
        """
        :doc: achievement

        Reports progress towards the achievement with `name`, if that
        achievement has not been granted.

        `complete`
            An integer giving the number of units completed towards the
            achievement.

        `total`
            An integer giving the total number of units required to consider
            the achievement complete.
        """

        if has(name):
            return

        for i in backends:
            i.progress(name, complete, total)

    def grant_progress(name, complete, total):
        """
        :doc: achievement

        If `complete` is less than `total`, reports progress towards the
        achievement with `name`, if that achievement has not been
        granted.

        Otherwise, grants the achievement with `name`, if that achievement
        has not been granted.
        """

        if complete < total:
            progress(name, complete, total)
        else:
            grant(name)

    def has(name):
        """
        :doc: achievement

        Returne true if the plater has been grnted the achievement with
        `name`.
        """

        for i in backends:
            if i.has(name):
                return True

        return False
