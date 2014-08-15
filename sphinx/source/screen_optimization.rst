.. _screen_optimization:

============================
Screen Language Optimization
============================

Ren'Py uses a number of techniques to optimize screen language speed. When
using Ren'Py to create complex interfaces, such as those used by simulation
games, it may help to understand how screen language works so you can
achieve maximal performance.

This guide is applicable to the second implementation of screen language,
which was added to Ren'Py 6.18. If your game was created in Ren'Py 6.17
or earlier, it may be necessary to chose the "Force Recompile" option
in the launcher to ensure its screens are upgraded to the latest version.

This guide isn't a substitute for good programming practice. If a screen
uses nested loops to do a lot of unproductive work, it will be slower than
a screen that avoids such looping. While understanding the techniques in
this guide is important,

Parameter List
==============

For best performance, all screens should be defined with a parameter list.
When a screen doesn't take parameters, it should be define with an empty
parameter list. The screen::

    screen test():
        vbox:
            for i in range(10):
                text "[i]"

is faster than::

    screen test:
        vbox:
            for i in range(10):
                text "[i]"

When a screen is defined without a parameter list, any name used in that
screen can be redefined when the screen is show. This requires Ren'Py to be
more conservative when analyzing the screen, which can limit the optimization
it performs.

Prediction
==========


Displayable Reuse
=================

When evaluating a screen language statement that creates a displayable, Ren'Py
will check to see if the positional arguments and properties given to that
displayable are equal to the positional arguments and properties given the
last time that statement was evaluated. If they are, instead of making a new
displayable, Ren'Py will reuse the existing displayable.

Displayable reuse has a number of performance implications. It saves the cost
of creating a new displayable, which may be significant for displayables that
contain a lot of internal state. More importantly, reusing a displayable means
that in many cases, Ren'Py will not need to re-render the displayable before
showing it to the user, which can lead to another significant speedup.

To compare positional arguments and properties, Ren'Py uses the notion of
equality embodied by Python's == operator. We've extended this notion of
equality to actions by deciding two actions should be equal when they are
indistinguishable from each other - when it doesn't matter which action
is invoked, or which action is queried to determine sensitivity or
selectedness.

All actions provided with Ren'Py conform to this definition. When defining
your own actions, it makes sense to provide them with this notion of
equality. This can be done by supplying an appropriate __eq__ method.
For example::

    class TargetShip(Action):
        def __init__(self, ship):
            self.ship = ship

        def __eq__(self, other):
            if not isinstance(other, TargetShip):
                return False

            return self.ship is other.ship

        def __call__(self):
            global target
            target = self.ship

It's important to define the __eq__ function carefully, making sure it
compares all fields, and uses equality (==) and identity (is) comparison
as appropriate.

Const
=====

Profiling
=========

Const Names
===========

Pure Names
==========
