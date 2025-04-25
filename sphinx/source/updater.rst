HTTPS/HTTP Updater
==================

Ren'Py includes an updater that can automatically download and install
updates to a Ren'Py game from a web host. The updates work on desktop
platforms, with the exception of macOS apps.

The Ren'Py updater shows an updater screen during this process,
prompting the user to proceed and allowing the user to cancel
when appropriate.

There are two update formats supported. The modern format is called rpu,
and was introduced in Ren'Py 8.2. An older format called zsync is obsolete,
but can be generated to update from older versions.

Server Requirements
-------------------

The updater requires that you provide your own hosting. You should be
able to download the update files by going to the appropriate URL
directly, and your server must support HTTP range queries.

Building an Update
------------------

Updates are built automatically when distributions are built. To build
an update, set :var:`build.include_update` to True in options.rpy. This will
unlock the "Build Updates" option in the "Build Distributions" section
of the launcher. Check this option, and Ren'Py will create the update
files.

The update files consist of:

updates.json
   An index of available updates and their versions.

updates.ecdsa
   A signature of updates.json, used to verify that it has not been
   tampered with.

rpu/
   The rpu directory contains the metadata and data used by the updates.

You should upload these to the same place on your webserver.

Functions
---------

To cause an update to occur, invoke either updater.update or the
updater.Update action.

.. include:: inc/updater

Screen
------

To customize the look of the updater, you may override the ``updater``
screen. Here's an example screen::

   screen updater(u=None):

      add "#000"

      frame:
         style_group ""

         has side "t c b":
            spacing gui._scale(10)

         label _("Updater")

         fixed:

            vbox:

               if u.state == u.ERROR:
                  text _("An error has occurred:")
               elif u.state == u.CHECKING:
                  text _("Checking for updates.")
               elif u.state == u.UPDATE_NOT_AVAILABLE:
                  text _("This program is up to date.")
               elif u.state == u.UPDATE_AVAILABLE:
                  text _("[u.version] is available. Do you want to install it?")
               elif u.state == u.PREPARING:
                  text _("Preparing to download the updates.")
               elif u.state == u.DOWNLOADING:
                  text _("Downloading the updates.")
               elif u.state == u.UNPACKING:
                  text _("Unpacking the updates.")
               elif u.state == u.FINISHING:
                  text _("Finishing up.")
               elif u.state == u.DONE:
                  text _("The updates have been installed. The program will restart.")
               elif u.state == u.DONE_NO_RESTART:
                  text _("The updates have been installed.")
               elif u.state == u.CANCELLED:
                  text _("The updates were cancelled.")

               if u.message is not None:
                  null height gui._scale(10)
                  text "[u.message!q]"

               if u.progress is not None:
                  null height gui._scale(10)
                  bar value (u.progress or 0.0) range 1.0 style "_bar"

         hbox:

            spacing gui._scale(25)

            if u.can_proceed:
               textbutton _("Proceed") action u.proceed

            if u.can_cancel:
               textbutton _("Cancel") action u.cancel

The updater screen is supplied a single parameter, an Updater object, which
must be named `u`. The Updater object has the following fields on it, which
can be used to customize the screen:

.. class:: updater.Updater

   .. attribute:: state

      The current state of the updater. See the example above for possible
      values and their meanings. The values are all constants on the Updater
      object.

   .. attribute:: message

      If not None, a message to display to the user.

   .. attribute:: progress

      If not None, the progress of the current operation, as a float between
      0.0 and 1.0.

   .. attribute:: can_proceed

      If True, the screen is being asked to display a button that will allow
      the user to proceed with the update.

   .. attribute:: proceed

      If can_proceed is True, this is the action that should be invoked when
      the user presses the proceed button.

   .. attribute:: can_cancel

      If True, the screen is being asked to display a button that will allow
      the user to cancel the update.

   .. attribute:: cancel

      If can_cancel is True, this is the action that should be invoked when
      the user presses the cancel button.

   .. attribute:: old_disk_total

      If not None, an integer giving the total number of bytes on the disk
      the game consumed at the start of the update.

   .. attribute:: new_disk_total

      If not None, an integer giving the total number of bytes on the disk
      the game will consume at the end of the update.

   .. attribute:: download_total

      If not None, an integer giving the total number of bytes that will be
      downloaded during the update.

   .. attribute:: download_done

      If not None, an integer giving the number of bytes that have been
      downloaded during the update, so far.

   .. attribute:: write_total

      If not None, an integer giving the total number of bytes that will be
      written to disk during the update.

   .. attribute:: write_done

      If not None, an integer giving the number of bytes that have been
      written to disk during the update, so far.
