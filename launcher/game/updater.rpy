﻿# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:
    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = os.environ.get("RENPY_UPDATE_SIMULATE", None)

    PUBLIC_KEY = "renpy_public.pem"

    CHANNELS_URL = "https://www.renpy.org/channels.json"

    version_tuple = renpy.version(tuple=True)

    def check_dlc(name):
        """
        Returns true if the named dlc package is present.
        """

        return name in updater.get_installed_packages()

    def add_dlc(name, restart=False):
        """
        Adds the DLC package, if it doesn't already exist.

        Returns True if the DLC is installed, False otherwise.
        """

        dlc_url = "http://update.renpy.org/{}/updates.json".format(".".join(str(i) for i in version_tuple[:-1]))

        state = updater.get_installed_state()

        if state is not None:
            base_name = state.get("sdk", {}).get('base_name', '')

            if "+nightly" in base_name:
                dlc_url = "http://nightly.renpy.org/{}/updates.json".format(base_name[6:])

        return renpy.invoke_in_new_context(updater.update, dlc_url, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=restart)

    # Strings so they can be translated.


    _("Release")
    _("Release (Ren'Py 8, Python 3)")
    _("Release (Ren'Py 7, Python 2)")
    _("{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games.")

    _("Prerelease")
    _("Prerelease (Ren'Py 8, Python 3)")
    _("Prerelease (Ren'Py 7, Python 2)")
    _("A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games.")

    _("Experimental")
    _("Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer.")

    _("Nightly Fix")
    _("Nightly Fix (Ren'Py 8, Python 3)")
    _("Nightly Fix (Ren'Py 7, Python 2)")
    _("A nightly build of fixes to the release version of Ren'Py.")

    _("Nightly")
    _("Nightly (Ren'Py 8, Python 3)")
    _("Nightly (Ren'Py 7, Python 2)")
    _("The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all.")

default allow_repair_update = False

screen update_channel(channels):

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("Select Update Channel")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    text _("The update channel controls the version of Ren'Py the updater will download.")

                    for c in channels:

                        if c["split_version"] != list(renpy.version_tuple) or allow_repair_update:
                            $ action = [SetField(persistent, "has_update", None), SetField(persistent, "last_update_check", None), updater.Update(c["url"], simulate=UPDATE_SIMULATE, public_key=PUBLIC_KEY, confirm=False, force=allow_repair_update)]

                            if c["channel"].startswith("Release"):
                                $ current = _("• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}")
                            elif c["channel"].startswith("Prerelease"):
                                $ current = _("• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}")
                            else:
                                $ current = ""

                        else:
                            $ action = None
                            $ current = _("• This version is installed and up-to-date.")

                        add SPACER

                        hbox:
                            spacing 7
                            textbutton c["channel"]  action action



                        add HALF_SPACER

                        $ date = _strftime(__("%B %d, %Y"), time.localtime(c["timestamp"]))

                        text "[date] • [c[pretty_version]] [current!t]" style "l_small_text"

                        add HALF_SPACER

                        text c["description"] style "l_small_text"

    textbutton _("Cancel") action Jump("front_page") style "l_left_button"


screen updater:

    frame:
        style "l_root"

        frame:
            style_group "l_info"

            has vbox

            if u.state == u.ERROR:
                text _("An error has occured:")
            elif u.state == u.CHECKING:
                text _("Checking for updates.")
            elif u.state == u.UPDATE_NOT_AVAILABLE:
                text _("Ren'Py is up to date.")
            elif u.state == u.UPDATE_AVAILABLE:
                text _("[u.version] is now available. Do you want to install it?")
            elif u.state == u.PREPARING:
                text _("Preparing to download the update.")
            elif u.state == u.DOWNLOADING:
                text _("Downloading the update.")
            elif u.state == u.UNPACKING:
                text _("Unpacking the update.")
            elif u.state == u.FINISHING:
                text _("Finishing up.")
            elif u.state == u.DONE:
                text _("The update has been installed. Ren'Py will restart.")
            elif u.state == u.DONE_NO_RESTART:
                text _("The update has been installed.")
            elif u.state == u.CANCELLED:
                text _("The update was cancelled.")

            if u.message is not None:
                add SPACER
                text "[u.message!q]"

            if u.progress is not None:
                add SPACER

                frame:
                    style "l_progress_frame"

                    bar:
                        range 1.0
                        value (u.progress or 0.0)
                        style "l_progress_bar"

        label _("Ren'Py Update") style "l_info_label"

    if u.can_cancel:
        textbutton _("Cancel") action u.cancel style "l_left_button"

    if u.can_proceed:
        textbutton _("Proceed") action u.proceed style "l_right_button"

label update:

    $ update_channels = fetch_update_channels(quiet=False)
    call screen update_channel(update_channels) nopredict

    jump front_page

init python:

    def fetch_update_channels(quiet=True):

        if not quiet:
            interface.processing(_("Fetching the list of update channels"))

        import requests

        if not quiet:
            with interface.error_handling(_("downloading the list of update channels")):
                channels = requests.get(CHANNELS_URL).json()["releases"]
        else:
            channels = requests.get(CHANNELS_URL).json()["releases"]

        persistent.has_update = False

        for chan in channels:
            if chan["channel"] == "Release":
                if chan["split_version"] > list(renpy.version_tuple):
                    persistent.has_update = True
                break

        return channels
