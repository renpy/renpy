Downloader for Large Games on Mobile
====================================

Platforms like Android and iOS have a limit on the size of an app that can
be downloaded from their app stores. To support larger games, Ren'Py supports
a downloader, which is a small game that downloads the main game.

Requirements
------------

To make this work, you'll need a web hosting service that is reasonably
capable. Uploader services like mega or game hosting sites like itch.io won't work.
The downloader has been tested with a Digital Ocean droplet that
runs Nginx, and also with Cloudflare's R2, which is free to host 10GB on.

Specifically, the web server needs to support downloading files, and it will
work better if it supports many HTTP Range requests at once.

How it Works
------------

To use the downloader, you'll need to build two games. The first is the
downloader game, which contains the Ren'Py engine and the downloader,
and is what the user will get delivered to their phone.

The second is the main game, the visual novel they want to play. This
will be downloaded by the downloader game, and will be installed onto
the device, if present.

Both need to be built with the same version of Ren'Py - if there is a
mismatch, the downloader will update the main game. Other than that,
it's up to the main game to update itself, which is possible now that
the Ren'Py updater works on mobile platforms.

When the downloader game starts, it checks to see if the main game is
installed. If it is, and the versions are right, the main game will
start. Otherwise the downloader will run and prompt the player to
download the main game.


Building and Uploading the Main Game
------------------------------------

The main change you need to make to your main game is to add the line::

    define build.game_only_update = True

to the top of your options.rpy file. That will add a new option that shows
up to the launcher's Build Distributions screen, "Game-Only Update for Mobile".


In "Build Distributions", check "Game-Only Update for Mobile". Uncheck all other
build packages. Under "Options", make sure "Build Updates" is set, and that
the other options are set as you like. The defaults are fine.

Then run the build process.

When the game is finished building, you'll have everything you need. You'll
want to upload the ``updates.json``, ``updates.ecdsa``, and everything in the
``rpu`` directory to your web server. (Make sure that the rpu directory is next to
the two update files, and the .rpu files are inside the ``rpu`` directory.)


Making a Downloader Game
------------------------

The downloader game is a Ren'Py game, but it should stay well under 100MB
in size. You can do anything you can in a small game - have an opening
scene, play music, etc. You will need to make it separately, and build
it for Android or iOS using the usual techniques.

At the same time, it should ask the player if they want to download, mention
that this can cost money if they're not on WiFi, and then download the the
game.

Here's an example script for a downloader game, using assets from the
tutorial game::

    # The url to updates.json, on your web server.
    define URL = "https://www.domain.com/game-updates/updates.json"

    # Disable saving in the downloader game.
    define config.save = False

    define e = Character("Eileen", image="eileen")

    label splashscreen:

        scene bg washington
        show eileen happy at left

        $ downloader = updater.start_game_download(URL)

        e "Welcome to the downloader game."

        e "This will download the main game onto your phone, so you can play it."

        if downloader.download_total:
            $ download_mb = int(round(downloader.download_total / 1024 / 1024, 0))

            e "To play this game, you'll need to download [download_mb] megabytes of data. If you're not on WiFi, you could be charged for it. Tap the screen to proceed."

        else:

            e "To play this game, you'll need to download some data. If you're not on WiFi, you could be charged for it. Tap the screen to proceed."

        $ updater.continue_game_download()

This is pretty simple, but there are a few things. The first is that it sets
:var:`config.save` to False. This is important, as it disables saving and
loading, including preferences, so the downloader's saves don't influence
the main game.

It's also all happening in the splashscreen, to start immediately and to
disable entering the game menu.

Early on, the game calls :func:`updater.start_game_download`, to gather information
about the download. After this, the game kills some time, having Eileen
say some things as the game checks to find out the size of the download.

After the player makes multiple clicks, the game may know the size of the
download, or it may not, so we use a conditional to check the download
size. If the real number is known, it's converted to megabytes and displayed.
If not, more general text is displayed. (It would also hard-code an estimate
of the download size into the game.)

Finally, :func:`updater.continue_game_download` is called, which starts the download
process. A screen will show up, and you can't do much - but music will play,
and ATL will keep running.

When the download is complete, the main game will automatically start. If it
fails, the downloader will restart, and the player will be able to try again

Downloader Screen
-----------------

The downloader is a screen that shows the progress of the download. A default
screen is in :file:`renpy/common/00updater.rpy`, and can be customized by
creating a copy in your game directory.

Here's the default::

    screen downloader(u):

        style_prefix "downloader"

        frame:

            has vbox

            if u.state == u.CHECKING or u.state == u.PREPARING:
                text _("Preparing to download the game data.")
            elif u.state == u.DOWNLOADING or u.state == u.UNPACKING:
                text _("Downloading the game data.")
            elif u.state == u.FINISHING or u.state == u.DONE:
                text _("The game data has been downloaded.")
            else: # An error or unknown state.
                text _("An error occurred when trying to download game data:")

                if u.message is not None:
                    text "[u.message!q]"

                text _("This game cannot be run until the game data has been downloaded.")

            if u.progress is not None:
                null height gui._scale(10)
                bar value (u.progress or 0.0) range 1.0

            if u.can_proceed:
                textbutton _("Retry") action u.proceed

    style downloader_frame:
        xalign 0.5
        xsize 0.5
        xpadding gui._scale(20)

        ypos .25
        ypadding gui._scale(20)

    style downloader_vbox:
        xfill True
        spacing gui._scale(10)

    style downloader_text:
        xalign 0.5
        text_align 0.5
        layout "subtitle"

    style downloader_label:
        xalign 0.5

    style downloader_button:
        xalign 0.5


Downloader Functions
--------------------

.. include:: inc/downloader
