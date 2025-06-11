========
Launcher
========

The Ren'Py launcher is mostly documented in other portions of the manual. This
page contains information about the launcher that doesn't fit anywhere else.


Project Folders
---------------

The launcher supports folders. You can create a folder by creating a directory
under the projects directory, and moving the project into it, then clicking Refresh.
Only one level of folders is supported, so you can't create a folder inside a folder.

Folders can be expanded and collapsed by clicking on the name in the launcher.

.. warning::

    Currently, the Ren'Py launcher only supports one project with a given name. So it's not
    possible to have the same project name in different folders.

Projects.txt
------------

If a file named ``projects.txt`` exists in the projects directory, it's expected
to contain a list of full paths, one per line. These paths are treated as if
they were inside the projects directory, and projects they contain show
up in the launcher.


No Launcher Links
-----------------

If a file named ``no_launcher_links.txt`` exists in the Ren'Py base directory (the one with
renpy.exe, renpy.sh, and renpy.app in it), the launcher will disable links to renpy.org. While
not guaranteed, this is intended in educational and homeschool environments to prevent young
Ren'Py users from seeing adult sponsors.
