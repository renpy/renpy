.. _screen-optimization:

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

Screens perform better when they're predicted in advance. That's because
Ren'Py will execute the screen during prediction time, and load in images
that are used by the screen.

There are two ways Ren'Py automatically predicts screens:

* Ren'Py will predict screens shown by the ``show screen`` and ``call screen``
  statements.
* Ren'Py will predict screen that will be shown by the :func:`Show` and :func:`ShowMenu`
  actions.

If screens are shown from Python, it's a good idea to start predicting
the screen before it is shown. To start predicting a screen, use the
:func:`renpy.start_predict_screen` function. To stop predicting a screen,
use the :func:`renpy.stop_predict_screen` function.


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

Const Expressions and Pure Functions
====================================

Ren'Py can exploit the properties of const variables and pure functions
to improve the speed of screen evaluation, and to entirely avoid the
evaluation of some parts of screens.

Definitions
-----------

An expression is **const** (short for constant) if it always represents the
same value when it is evaluated. For Ren'Py's purposes, an expression is
const if and only if the following expressions always evaluate to the same
const value or are undefined:

* Applying any unary, binary, or ternary operator to the expression, provided
  the other operands are also const.
* Accessing a field on the expression.
* Indexing the expression, either using a number or an object.

Python numbers and strings are const, as are list, tuple, set, and dict
literals for which all components are const. Ren'Py marks
variables defined using the ``define`` statement as const.
The :func:`renpy.const` and :func:`renpy.not_const` functions
can be used to further control what Ren'Py considers to be const. The
default list of const names is given in the :ref:`Const Names <const-names>`
section below.

If you have a variable that will never change, it makes sense to use ``define``
to both define it and declare it const. For example::

    define GRID_WIDTH = 20
    define GRID_HEIGHT = 10

A callable function, class, or action is **pure** if, when all of its arguments
are const values, it always gives the same const value. Alternatively, an
expression that invokes a pure function with const expression is also a
const expression.

A large number of default functions, classes, and actions are marked as
pure. These functions are listed in the :ref:`Pure Names <pure-names>`
section below.

Functions are declared pure using the :func:`renpy.pure` function, which
can be used as a decorator for functions declared in the default store.

Const expressions and pure functions do not need to retain the same value
across the following events:

* The end of the init phase.
* A change of the language.
* A style rebuild.

How Const Optimizes Screen Language
-----------------------------------

There are three advantages to ensuring that screen language arguments and
properties are const.

The first is that const arguments and properties are evaluated when
screens are prepared, which is at the end of the init phase, when the
language is changed, or when styles are rebuilt. After that, it is no
longer necessary to spend time evaluating const arguments and properties.

The second is that const works well with displayable reuse. When all of
the arguments and properties of a displayable are const, the displayable
can always be reused, which gains all the benefits of displayable reuse.

Lastly, when Ren'Py encounters a tree of displayables such that all
arguments, properties, and expressions affecting control flow are
also const, Ren'Py will reuse the entire tree without evaluating
expressions or creating displayables. This can yield a significant
performance boost.

For example, the following screen does not execute any Python or create
any displayables after the first time it is predicted or shown::

    screen mood_picker():
        hbox:
            xalign 1.0
            yalign 0.0

            textbutton "Happy" action SetVariable("mood", "happy")
            textbutton "Sad" action SetVariable("mood", "sad")
            textbutton "Angry" action SetVariable("mood", "angry")

Const Text
----------

When defining text, please note that strings containing new-style text
substitutions are const::

    $ t = "Hello, world."
    text "[t]"

Supplying a variable containing the text directly is generally not const::

    $ t = "Hello, world."
    text t

Neither is using percent-substitution::

    $ t = "Hello, world."
    text "%s" % t

Lastly, note that the _ text translation function is pure, so if it contains
a string, the entire expression is const::

    text _("Your score is: [score]")


Const Functions
----------------

.. include:: inc/const

Profiling
=========

Ren'Py supports profiling screen execution through the ``renpy.profile_screen``
function:

.. include:: inc/profile_screen


.. _const-names:

Const Names
===========

The following names are const by default.

.. include:: inc/const_vars


.. _pure-names:

Pure Names
==========

The following names are both pure and const by default.

.. include:: inc/pure_vars

