Screen Language
===============

The user interface of a Ren'Py game is divided into screens. Some
screens are shown to the user inside the game, including the screens
for dialogue and menu choices. Other screens are used for the main
menu and the game menu. Ren'Py's screen language provides a flexible
and mostly-declarative way of defining these screens.

Widgets are displayables that have a user interface function. A screen
is a collection of widgets. There can be more than one screen
displayed at a time, provided that a screen doesn't conflict with 
other shown screens. Generally, only the uppermost screen will accept
input from the user, but screens are able to declare that they pass
input to the next lower screen.


Screen Language Basics
----------------------

**Syntax.** Statements in the screen language share a common syntax. Each
statement consists of a single logical line, followed by an optional
block.

The first logical line begins with a keyword, that determines what
kind of statement this is. The keyword is followed by
space-separated mandatory parameters, if the statement takes any,
and zero or more space-separated optional parameters. The first line
ends with a colin if it takes a block. Otherwise, the statement ends
at the end of the line.

An optional parameter consists of a name, a space, and then a value
for the optional parameter. The value is parsed as a
simple_expression, unless a more specific parsing method is noted in
the parameter's description.

There are two kinds of lines that can go in the block of a screen
language statement. The first kind of line is an optional parameter
line, which consists of one or more space-separated optional
parameters. The second is a screen language statement, that defines
a widget to be placed within this one. As a matter of good style,
all optional parameters in a block should be placed before the first
screen language statement in that block, but Ren'Py does not enforce
this restriction.


**Relative Placement.** When a child widget is contained within a parent widget, it is
positioned relative to the area offered to it by the parent widget.

**Namespaces.** When screens execute python code, they execute it in a context that
consists of three namespaces:

#. The local namespace contains parameters passed in when the scene is
   shown, and variables updated over the course of displaying the
   scene. This is the only namespace that can be updated when displaying
   the scene.
#. The scene language namespace contains the Actions and Adjustments
   given below. This namespace is available as the sl module, which is
   imported into the default Ren'Py namespace.
#. The default Ren'Py namespace, which is the namespace where Python
   variables are stored by default.

When a variable is accessed, the namespaces are searched in order.


Defining Screens
----------------

Screen Language Statements
--------------------------

Actions
-------

Adjustments
-----------

Using Screens
-------------

Python Equivalent
-----------------



::

  button area (100, 200, 100, 200)
