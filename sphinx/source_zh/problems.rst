Dealing with Problems
=====================

.. include:: display_problems.rst


Windows Encoding Problems
-------------------------

Ren'Py will fail to start on Windows if it's placed in a directory with a
full path that isn't representable in the current system language. For example,
if Ren'Py is in the directory:

    C:\ビジュアルノベル\renpy-6.16.0-sdk\

and the system is set to use the English language, Ren'Py will be unable to
start. To fix this problem, start the control panel, select "Region and Language
Options", "Advanced", and change the Language for non-Unicode programs.


OS X 10.9 Mavericks
-------------------

A bug in OS X 10.9 Mavericks prevents Ren'Py from starting when launched
on a non-primary display. Until Apple fixes this bug, please launch Ren'Py from
the the primary display.


64-Bit Linux Problems
----------------------

Ren'Py 6.14.x and 6.15.0-3 were compiled incorrectly, and will often
fail to operate on 64-bit Linux computers. The best way to work around
this is to download Ren'Py 6.15.4 or later, and use it to run the game::


  /path/to/renpy-6.15.4/renpy.sh /path/to/game-with-problems
