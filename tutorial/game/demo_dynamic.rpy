# This file demonstrates how to use DynamicDisplayable to make parts of the
# display that update without there being an interaction.

init:
    python:

        # This function will run a countdown of the given length. It will
        # be white until 5 seconds are left, and then red until 0 seconds are
        # left, and then will blink 0.0 when time is up.
        def countdown(st, at, length=0.0):

            remaining = length - st

            if remaining > 5.0:
                return Text("%.1f" % remaining, color="#fff", size=72), .1
            elif remaining > 0.0:
                return Text("%.1f" % remaining, color="#f00", size=72), .1
            else:
                return anim.Blink(Text("0.0", color="#f00", size=72)), None

    # Show a countdown for 10 seconds.
    image countdown = DynamicDisplayable(countdown, length=10.0)


label demo_dynamic:

    e "The DynamicDisplayable function lets you change what's displayed over the course of an interaction."

    show countdown at Position(xalign=.1, yalign=.1)

    e "This makes it possible to display things like countdown timers and progress bars."

    e "Remember, people read at different speeds, so it's probably better to use this for flavor, rather then to make games time-sensitive."

    hide countdown
    with dissolve

    return
