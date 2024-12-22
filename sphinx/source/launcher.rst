========
Launcher
========

The Ren'Py launcher is mostly documented in other portions of the manual. This
page contains information about the launcher that doesn't fit anywhere else.

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
