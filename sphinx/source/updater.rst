Web Updater
===========

Ren'Py includes an updater that can automatically download and install
updates to a Ren'Py game hosted at a website. This can be useful in
keeping a large game up to date.

The Ren'Py updater works by automatically performing the following
steps:

#. Downloading an index file that controls what is updated.
#. Asking the user if he or she wants to proceed with the update.
#. Producing an archive file from the files on disk.
#. Downloading a zsync control file from the server.
#. Using the zsync tool to update the archive file to the version on
   the server. Zsync automatically computes the differences between
   the two files, and attempts to only download the portions that
   have changed.
#. Unpacking the archive, replacing the files on disk.
#. Deleting files that have been removed between the old and new
   versions.
#. Restarting the game.

The Ren'Py updater shows an updater screen during this process,
prompting the user to proceed and allowing the user to cancel
when appropriate.

Server Requirements
-------------------

The updater requires that you provide your own hosting. You should be
able to download the update files by going to the appropriate URL
directly, and your server must support HTTP range queries.

(This means paying for web hosting, as "sharing" sites tend not to
support the required features.)


Building an Update
------------------

Updates are built automatically when distributions are built. To build
an update, set build.include_update to True in options.rpy. This will
unlock the "Build Updates" option in the "Build Distributions" section
of the launcher. Check this option, and Ren'Py will create the update
files.

The update files consist of:

updates.json
   An index of available updates and their versions.

*package*.sums
   Contains checksums for each block in the package.

*package*.update.gz
   Contains the update data for the given package.

*package*.update.json
   Contains a list of the files in each package, which the updater
   uses when downloading DLC.

*package*.zsync
   This is a control file that's used by zsync to manage the download.

You must upload all these files to a single directory on your web
server.


Functions
---------

To cause an update to occur, invoke either updater.update or the
updater.Update action.

.. include:: inc/updater

Screen
------

To customize the look of the updater, you may override the ``updater``
screen. The default screen is defined in common/00updater.rpy.
