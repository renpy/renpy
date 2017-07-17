init:
    $ mp = MultiPersistent("demo.renpy.org")

label demo_persistent:

    "Ren'Py supports per-game and multi-game persistent data."

    "Persistent data can store flags and other per-game information that should be shared between plays of a single game."

    # per-game persistent data example.
    python:
        if persistent.plays is None:
            persistent.plays = 1
        else:
            persistent.plays += 1

        plays = persistent.plays

    "For example, I can tell you that you've see this line [plays] time(s) since you cleared the per-game persistent data."

    "Multipersistent data is shared between games, which lets one game unlock features in a second."

    "A sequel might play differently if the player has beaten the first game."

    # multipersistent data example.
    python:
        if mp.plays is None:
            mp.plays = 1
        else:
            mp.plays += 1

        mp.save()
        plays = mp.plays

    "According to the multipersistent data, you've seen this line [plays] times total."

    return
