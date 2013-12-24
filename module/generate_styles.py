# Code for generating the includes used by renpy.styleaccel.

# A map from prefix name to Prefix object.
prefixes = { }

class Prefix(object):
    def __init__(self, index, name, priority, alts):

        # The index of where this prefix is stored in memory, or -1 if this
        # prefix isn't stored in memory.
        self.index = index

        # The name of this prefix.
        self.name = name

        # The priority of this prefix. When added at the same time, higher
        # priority prefixes take precendence over lower priority prefixes.
        self.priority = priority

        # A list of prefix indexes that should be updated when this prefix is
        # updated, including this prefix.
        if index >= 0:
            self.alts = [ self.index ]
        else:
            self.alts = [ ]

        for i in alts:
            self.alts.append(prefixes[i].index)

        prefixes[name] = self

# The number of priority levels we have.
PRIORITY_LEVELS = 4

Prefix(5, 'selected_hover_', 3, [ ])
Prefix(4, 'selected_idle_', 3, [ ])
Prefix(3, 'selected_insensitive_', 3, [ ])
Prefix(-1, 'selected_', 2, [ "selected_hover_", "selected_idle_", "selected_insensitive_" ])
Prefix(2, 'hover_', 1, [ "selected_hover_" ])
Prefix(1, 'idle_', 1, [ "selected_idle_" ] )
Prefix(0, 'insensitive_', 1, [ "selected_insensitive_" ])
Prefix(-1, '', 0, [ "selected_hover_", "selected_idle_", "selected_insensitive_", "idle_", "hover_", "insensitive_" ] )

def generate_styles(force=False):

    # TODO: If nothing is out of date, do not generate styles.

    pass

if __name__ == "__main__":
    generate_styles(force=True)
