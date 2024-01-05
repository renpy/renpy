# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
    # Do not participate in saves.
    _constant = True

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

            self.stat_max = { }

        def register(self, name, stat_max=None, **kwargs):
            if stat_max:
                self.stat_max[name] = stat_max

        def grant(self, name):
            persistent._achievements.add(name)

        def clear(self, name):
            persistent._achievements.discard(name)
            if name in persistent._achievement_progress:
                del persistent._achievement_progress[name]

        def clear_all(self):
            persistent._achievements.clear()
            persistent._achievement_progress.clear()

        def has(self, name):
            return name in persistent._achievements

        def progress(self, name, completed):
            current = persistent._achievement_progress.get(name, 0)

            if (current is not None) and (current >= completed):
                return

            persistent._achievement_progress[name] = completed

            if name not in self.stat_max:
                if config.developer:
                    raise Exception("To report progress, you must register {} with a stat_max.".format(name))
                else:
                    return

            if completed >= self.stat_max[name]:
                self.grant(name)

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

    # The Steam back-end has been moved to 00steam.rpy.

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

        for i in backends:
            i.clear(name)

    def clear_all():
        """
        :doc: achievement

        Clears all achievements.
        """

        for i in backends:
            i.clear_all()

    def get_progress(name):
        """
        :doc: achievement

        Returns the current progress towards the achievement identified
        with `name`, or 0 if no progress has been registered for it or if
        the achievement is not known.
        """

        return persistent._achievement_progress.get(name, 0)

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
            renpy.restart_interaction()

        def get_sensitive(self):
            for a in persistent._achievements:
                for i in backends:
                    if not i.has(a):
                        return True
            return False
