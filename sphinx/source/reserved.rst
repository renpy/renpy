:orphan:

.. _reserved-names:

Reserved Names
==============

Ren'Py reserves filenames that are do not begin with a letter or number,
and filenames that begin with "00". Very specifically, filenames that start
with "00" and "\_" are used by Ren'Py internally.

Ren'Py reserves all names beginning with a single underscore (\_). Do not
use names beginning with an underscore, as that may cause your game to break
in future versions of Ren'Py.

The following is a list of names that are used by Python. Re-using these
names can lead to obscure problems.

.. include:: inc/reserved_builtins

The following is a list of names that are used by Ren'Py. While in some
cases it makes sense to redefine these names, one should be aware that doing
so can cause obscure problems.

.. include:: inc/reserved_renpy

