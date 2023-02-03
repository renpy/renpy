Security
========

Games and Mods
--------------

Like all games and other software that you run on your computer, you should
only run a Ren'Py game if you trust the creator and everyone involved in
getting the game to you. Malicious software, including games written in
Ren'Py, can perform arbitrarily harmful actions on your computer, and can
even send information elsewhere.

This includes mods that involve changing a game or Ren'Py's source code -
if you don't trust the creator of the mod and everyone that brought it
to you, you should not apply the mod.

Save and Persistent Files
-------------------------

Ren'Py save files, including the ``persistent`` file, are created using
the Python pickle format. This file format is powerful enough that it
should be treated like software - if a malicious person can get you to
load a file they created, they can run arbitrary code on your computer.

It's best to treat save and persistent files as if the files contained
software, and only load them if you trust the creator of the file, and
everyone that brought it to you.

Save and persistent files are not designed to be shared between players,
and so those files may contain information about you and your computer.
We recommend that you do not share save and persistent files with
other users.
