# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

python early:

    # Should steam be enabled?
    config.enable_steam = True


init -1499 python in _renpysteam:

    import collections
    import time

    ticket = None

    def retrieve_stats():
        """
        :doc: steam_stats

        Retrieves achievements and statistics from Steam.
        """
        """
        `callback` will be
        called with no parameters if and when the statistics become available.
        """

        steamapi.SteamUserStats().RequestCurrentStats()


    def store_stats():
        """
        :doc: steam_stats

        Stores statistics and achievements on the Steam server.
        """

        steamapi.SteamUserStats().StoreStats()


    def list_achievements():
        """
        :doc: steam_stats

        Returns a list of achievement names.
        """

        rv = [ ]

        na = steamapi.SteamUserStats().GetNumAchievements()

        for i in range(na):
            rv.append(steamapi.SteamUserStats().GetAchievementName(i).decode("utf-8"))

        return rv


    def get_achievement(name):
        """
        :doc: steam_stats

        Gets the state of the achievements with `name`. This returns True if the
        achievement has been granted, False if it hasn't, and None if the achievement
        is unknown or an error occurs.
        """

        from ctypes import byref, c_bool

        rv = c_bool(False)

        if not steamapi.SteamUserStats().GetAchievement(name.encode("utf-8"), byref(rv)):
            return None

        return rv.value


    def grant_achievement(name):
        """
        :doc: steam_stats

        Grants the achievement with `name`. Call :func:`_renpysteam.store_stats` to
        push this change to the server.
        """

        return steamapi.SteamUserStats().SetAchievement(name.encode("utf-8"))


    def clear_achievement(name):
        """
        :doc: steam_stats

        Clears the achievement with `name`. Call :func:`_renpysteam.store_stats` to
        push this change to the server.
        """

        return steamapi.SteamUserStats().ClearAchievement(name.encode("utf-8"))


    def indicate_achievement_progress(name, cur_progress, max_progress):
        """
        :doc: steam_stats

        Indicates achievement progress to the user. This does *not* unlock the
        achievement.
        """

        return steamapi.SteamUserStats().IndicateAchievementProgress(name.encode("utf-8"), cur_progress, max_progress)


    def get_float_stat(name):
        """
        :doc: steam_stats

        Returns the value of the stat with `name`, or None if no such stat
        exits.
        """

        from ctypes import c_float, byref

        rv = c_float(0)

        if not steamapi.SteamUserStats().GetStatFloat(name.encode("utf-8"),  byref(rv)):
            return None

        return rv.value


    def set_float_stat(name, value):
        """
        :doc: steam_stats

        Sets the value of the stat with `name`, which must have the type of
        FLOAT. Call :func:`_renpysteam.store_stats` to push this change to the
        server.
        """

        return steamapi.SteamUserStats().SetStatFloat(name.encode("utf-8"), value)


    def get_int_stat(name):
        """
        :doc: steam_stats

        Returns the value of the stat with `name`, or None if no such stat
        exits.
        """
        from ctypes import c_int, byref

        rv = c_int(0)

        if not steamapi.SteamUserStats().GetStatInt32(name.encode("utf-8"), byref(rv)):
            return None

        return rv.value


    def set_int_stat(name, value):
        """
        :doc: steam_stats

        Sets the value of the stat with `name`, which must have the type of
        INT. Call :func:`_renpysteam.store_stats` to push this change to the
        server.
        """

        return steamapi.SteamUserStats().SetStatInt32(name.encode("utf-8"), value)


    ########################################################################### Apps

    def is_subscribed_app(appid):
        """
        :doc: steam_apps

        Returns true if the user owns the app with `appid`, and false otherwise.
        """

        return steamapi.SteamApps().BIsSubscribedApp(appid)


    def get_current_game_language():
        """
        :doc: steam_apps

        Return the name of the language the user has selected.
        """

        return steamapi.SteamApps().GetCurrentGameLanguage().decode("utf-8")


    def get_steam_ui_language():
        """
        :doc: steam_apps

        Return the name of the language the steam UI is using.
        """

        return steamapi.SteamUtils().GetSteamUILanguage().decode("utf-8")


    def get_current_beta_name():
        """
        :doc: steam_apps

        Returns the name of the current beta, or None if it can't.
        """

        from ctypes import create_string_buffer, byref

        rv = create_string_buffer(256)

        if not steamapi.SteamApps().GetCurrentBetaName(rv, 256):
            return None

        return rv.value.decode("utf-8")


    def dlc_installed(appid):
        """
        :doc: steam_apps

        Returns True if `dlc` is installed, or False otherwise.
        """

        return steamapi.SteamApps().BIsDlcInstalled(appid)


    def install_dlc(appid):
        """
        :doc: steam_apps

        Requests the DLC with `appid` be installed.
        """

        steamapi.SteamApps().InstallDLC(appid)


    def uninstall_dlc(appid):
        """
        :doc: steam_apps

        Requests that the DLC with `appid` be uninstalled.
        """

        steamapi.SteamApps().UninstallDLC(appid)


    def dlc_progress(appid):
        """
        :doc: steam_apps

        Reports the progress towards DLC download completion.

        """

        from ctypes import c_ulonglong, byref

        done = c_ulonglong(0)
        total = c_ulonglong(0)

        if steamapi.SteamApps().GetDlcDownloadProgress(appid, byref(done), byref(total)):
            return done.value, total.value
        else:
            return None


    def get_app_build_id():
        """
        :doc: steam_apps

        Returns the build ID of the installed game.
        """

        return steamapi.SteamApps().GetAppBuildId()


    ######################################################################## Overlay

    def is_overlay_enabled():
        """
        :doc: steam_overlay

        Returns true if the steam overlay is enabled. (This might take a while to
        return true once the game starts.)
        """

        return steamapi.SteamUtils().IsOverlayEnabled()


    last_needs_present_call = 0

    def overlay_needs_present():
        """
        :doc: steam_overlay

        Returns true if the steam overlay is enabled. (This might take a while to
        return true once the game starts.)
        """

        global last_needs_present_call

        now = time.time()

        # Steam docs say that BOOL BOverlayNeedsPresent() should be called
        # at around 33 Hz. See also Ren'Py bug #3978.
        if now < last_needs_present_call + 1 / 33.0:
            return False

        last_needs_present_call = now

        return steamapi.SteamUtils().BOverlayNeedsPresent()


    def set_overlay_notification_position(position):
        """
        :doc: steam_overlay

        Sets the position of the steam overlay. `Position` should be one of
        achievement.steam.POSITION_TOP_LEFT, .POSITION_TOP_RIGHT, .POSITION_BOTTOM_LEFT,
        or .POSITION_BOTTOM_RIGHT.
        """

        steamapi.SteamUtils().SetOverlayNotificationPosition(position)


    def activate_overlay(dialog):
        """
        :doc: steam_overlay

        Activates the Steam overlay.

        `dialog`
            The dialog to open the overlay to. One of "Friends", "Community",
            "Players", "Settings", "OfficialGameGroup", "Stats", "Achievements"
        """

        steamapi.SteamFriends().ActivateGameOverlay(dialog.encode("utf-8"))


    def activate_overlay_to_web_page(url):
        """
        :doc: steam_overlay

        Activates the Steam overlay, and opens the web page at `url`.
        """

        steamapi.SteamFriends().ActivateGameOverlayToWebPage(url.encode("utf-8"), steamapi.k_EActivateGameOverlayToWebPageMode_Default)

    def activate_overlay_to_store(appid, flag=None):
        """
        :doc: steam_overlay

        Opens the steam overlay to the store.

        `appid`
            The appid to open.

        `flag`
            One of achievement.steam.STORE_NONE, .STORE_ADD_TO_CART, or .STORE_ADD_TO_CART_AND_SHOW.
        """

        if flag is None:
            flag = STORE_NONE

        steamapi.SteamFriends().ActivateGameOverlayToStore(appid, flag)

    ########################################################################### User

    def get_persona_name():
        """
        :doc: steam_user

        Returns the user's publicly-visible name.
        """

        return steamapi.SteamFriends().GetPersonaName().decode("utf-8")


    def get_csteam_id():
        """
        :doc: steam_user

        Returns the user's full CSteamID as a 64-bit number..
        """

        # Accessing methods on CSteamID was crashing on Windows, so use
        # the flat API instead.

        return steamapi.SteamUser().GetSteamID()


    def get_account_id():
        """
        :doc: steam_user

        Returns the user's account ID.
        """

        return get_csteam_id() & 0xffffffff


    def get_session_ticket():
        """
        :doc: steam_user

        Gets a ticket that can be sent to the server to authenticate this user.
        """

        from ctypes import c_uint, create_string_buffer, byref

        global ticket
        global h_ticket

        if ticket is not None:
            return ticket

        ticket_buf = create_string_buffer(2048)
        ticket_len = c_uint()

        h_ticket = steamapi.SteamUser().GetAuthSessionTicket(ticket_buf, 2048, byref(ticket_len))

        if h_ticket:
            ticket = ticket_buf.raw[0:ticket_len.value]

        return ticket


    def cancel_ticket():
        """
        :doc: steam_user

        Cancels the ticket returned by :func:`_renpysteam.get_session_ticket`.
        """

        global h_ticket
        global ticket

        steamapi.SteamUser().CancelAuthTicket(h_ticket)

        h_ticket = 0
        ticket = None


    def get_game_badge_level(series, foil):
        """
        :doc: steam_user

        Gets the level of the users Steam badge for your game.
        """

        return steamapi.SteamUser().GetGameBadgeLevel(series, foil)


    ########################################################################### UGC

    def get_subscribed_items():
        """
        :doc: steam_ugc

        Returns a list of the item ids the user has subscribed to in the steam
        workshop.
        """

        from ctypes import c_ulonglong, pointer, POINTER, cast

        subscribed = (c_ulonglong * 512)()

        count = steamapi.SteamUGC().GetSubscribedItems(
            cast(pointer(subscribed), POINTER(c_ulonglong)),
            512)

        rv = [ ]

        for i in range(count):
            rv.append(subscribed[i])

        return rv

    def get_subscribed_item_path(item_id):
        """
        :doc: steam_ugc

        Returns the path where an item of user-generated content was installed. Returns
        None if the item was not installed.

        `item_id`
            The item id.
        """

        from ctypes import c_uint, c_ulonglong, create_string_buffer, byref

        path = create_string_buffer(4096)
        size = c_ulonglong()
        timestamp = c_int()

        if not steamapi.SteamUGC().GetItemInstallInfo(item_id, byref(size), byref(path), 4096, byref(timestamp)):
            return None

        return renpy.exports.fsdecode(path.value)

    ############################################ Import API after steam is found.
    def import_api():

        global steamapi
        import steamapi

        global POSITION_TOP_LEFT, POSITION_TOP_RIGHT, POSITION_BOTTOM_LEFT, POSITION_BOTTOM_RIGHT

        POSITION_TOP_LEFT = steamapi.k_EPositionTopLeft
        POSITION_TOP_RIGHT = steamapi.k_EPositionTopRight
        POSITION_BOTTOM_LEFT = steamapi.k_EPositionBottomLeft
        POSITION_BOTTOM_RIGHT = steamapi.k_EPositionBottomRight

        global STORE_NONE, STORE_ADD_TO_CART, STORE_ADD_TO_CART_AND_SHOW

        STORE_NONE = steamapi.k_EOverlayToStoreFlag_None
        STORE_ADD_TO_CART = steamapi.k_EOverlayToStoreFlag_AddToCart
        STORE_ADD_TO_CART_AND_SHOW = steamapi.k_EOverlayToStoreFlag_AddToCartAndShow

    ################################################################## Callbacks

    # A map from callback class name to a list of callables that will be called
    # with the callback instance.


    callback_handlers = collections.defaultdict(list)

    def periodic():
        """
        Called periodically to run Steam callbacks.
        """

        for cb in steamapi.generate_callbacks():
            # print(type(cb).__name__, {k : getattr(cb, k) for k in dir(cb) if not k.startswith("_")})

            for handler in callback_handlers.get(type(cb).__name__, [ ]):
                handler(cb)

        if renpy.variant("steam_deck"):
            keyboard_periodic()

    ################################################################## Keyboard

    # True to show the keyboard once, False otherwise.
    keyboard_mode = "once"

    # True if this is the start of a new interaction, and so the keyboard
    # should be shown if a text box appears.
    keyboard_primed = True

    # True if the keyboard is currently showing.
    keyboard_showing = None

    # Should the layers be shifted so the baseline is in view?
    keyboard_shift = False

    # Where the baseline is shifted to on the screen. This is a floating point number,
    # with 0.0 being the top of the screen and 1.0 being the bottom.
    keyboard_baseline = 0.5

    # The textarea given to steam. This is scaled using the usual
    # position rules.
    keyboard_text_area = (0.0, 0.5, 1.0, 0.5)

    def prime_keyboard():
        global keyboard_primed
        keyboard_primed = True

    renpy.config.start_interact_callbacks.append(prime_keyboard)

    def keyboard_periodic():

        global keyboard_showing
        global keyboard_primed
        global keyboard_shift
        global keyboard_baseline

        if keyboard_mode == "never":
            return
        elif keyboard_mode == "always":
            keyboard_primed = True
        elif keyboard_mode != "once":
            raise Exception("Bad steam keyboard_mode.")

        keyboard_text_rect = renpy.display.interface.text_rect
        _KeyboardShift.text_rect = keyboard_text_rect

        if keyboard_primed and (keyboard_showing is None) and keyboard_text_rect:

            pw, ph = renpy.exports.get_physical_size()

            def scale(n, available):
                if type(n) == float:
                    n = n * available

                return int(n)

            x = scale(keyboard_text_area[0], pw)
            y = scale(keyboard_text_area[1], ph)
            w = scale(keyboard_text_area[2], pw)
            h = scale(keyboard_text_area[3], ph)

            steamapi.SteamUtils().ShowFloatingGamepadTextInput(
                steamapi.k_EFloatingGamepadTextInputModeModeSingleLine,
                x, y, w, h)

            keyboard_showing = time.time()
            keyboard_primed = False

        if keyboard_shift and keyboard_showing and keyboard_text_rect:
            for l in renpy.config.transient_layers + renpy.config.overlay_layers + renpy.config.context_clear_layers:
                if not renpy.display.interface.ongoing_transition.get(l) is _KeyboardShift:
                    renpy.display.interface.set_transition(_KeyboardShift, layer=l, force=True)
                    renpy.exports.restart_interaction()

        if keyboard_showing and not keyboard_text_rect:
            steamapi.SteamUtils().DismissFloatingGamepadTextInput()

        if keyboard_showing is None:
            _KeyboardShift.last_offset = 0
        else:
            _KeyboardShift.rendered_offset = _KeyboardShift.last_offset


    def keyboard_dismissed(cb):
        """
        Called when the keyboard is dismissed.
        """

        global keyboard_showing
        keyboard_showing = None

    callback_handlers["FloatingGamepadTextInputDismissed_t"].append(keyboard_dismissed)

    class _KeyboardShift(renpy.display.layout.Container):
        """
        This is a transition that shifts the screen up, intended for use only
        with the steam deck keyboard.
        """

        # Store the text rectangle in the class, so it's not saved, and
        # is available during render().
        text_rect = None

        # The last offset we computed.
        last_offset = 0

        # The offset we computed last time we rendered.
        rendered_offset = 0

        def __init__(self, new_widget, old_widget, **properties):
            super(_KeyboardShift, self).__init__(**properties)

            self.delay = 0
            self.add(new_widget)

        def render(self, width, height, st, at):
            rv = renpy.display.render.Render(width, height)
            cr = renpy.display.render.render(self.child, width, height, st, at)

            if (keyboard_showing is not None) and self.text_rect:

                yscale = renpy.config.screen_height / renpy.exports.get_physical_size()[1]
                x, y, w, h = self.text_rect
                y -= self.rendered_offset

                text_baseline = y + h
                desired_baseline = int(keyboard_baseline * renpy.config.screen_height)

                offset = int(desired_baseline - text_baseline)
                offset = min(0, offset)

                done = (time.time() - keyboard_showing) / .3
                done = min(1.0, done)
                done = max(0.0, done)

                if offset and done < 1.0:
                    renpy.display.render.redraw(self, 0)

                offset = int(offset * done)

            else:
                offset = 0

            _KeyboardShift.last_offset = offset

            rv.blit(cr, (0, offset))
            self.offsets = [ (0, offset) ]

            return rv

init -1499 python in achievement:

    steam_maximum_framerate = 15

    # The position of the steam notification popup. One of "top left", "top right",
    # "bottom left", or "bottom right".
    steam_position = None

    class SteamBackend(Backend):
        """
        A backend that sends achievements to Steam. This is only used if steam
        has loaded and initialized successfully.
        """

        def __init__(self):
            # A map from achievement name to steam name.
            self.names = { }
            self.stats = { }

            steam.retrieve_stats()
            renpy.maximum_framerate(steam_maximum_framerate)

        def register(self, name, steam=None, steam_stat=None, stat_max=None, stat_modulo=1, **kwargs):
            if steam is not None:
                self.names[name] = steam

            self.stats[name] = (steam_stat, stat_max, stat_modulo)

        def grant(self, name):
            name = self.names.get(name, name)

            renpy.maximum_framerate(steam_maximum_framerate)
            steam.grant_achievement(name)
            steam.store_stats()

        def clear(self, name):
            name = self.names.get(name, name)

            steam.clear_achievement(name)
            steam.store_stats()

        def clear_all(self):
            for i in steam.list_achievements():
                steam.clear_achievement(i)

            steam.store_stats()

        def progress(self, name, completed):

            orig_name = name

            completed = int(completed)

            if name not in self.stats:
                if config.developer:
                    raise Exception("To report progress, you must register {} with a stat_max.".format(name))
                else:
                    return

            current = persistent._achievement_progress.get(name, 0)

            steam_stat, stat_max, stat_modulo = self.stats[name]

            name = self.names.get(name, name)

            if (current is not None) and (current >= completed):
                return

            renpy.maximum_framerate(steam_maximum_framerate)

            if completed >= stat_max:
                steam.grant_achievement(name)
            else:
                if (stat_modulo is None) or (completed % stat_modulo) == 0:
                    steam.indicate_achievement_progress(name, completed, stat_max)

            steam.store_stats()

        def has(self, name):
            name = self.names.get(name, name)

            return steam.get_achievement(name)

    def steam_preinit():
        """
        This sets up the steam appid when in development mode.
        """

        import os, sys

        if config.early_script_version is not None:
            return

        steam_appid_fn = os.path.join(os.path.dirname(sys.executable), "steam_appid.txt")

        if config.steam_appid is not None:
            with open(steam_appid_fn, "w") as f:
                f.write(str(config.steam_appid) + "\n")
        else:
            try:
                os.unlink(steam_appid_fn)
            except Exception:
                pass


    # The _renpysteam namespace, or None if steam isn't loaded.
    steam = None

    # The full steam api.
    steamapi = None

    # Are the steam libraries installed? Used by the launcher.
    has_steam = False

    def steam_init():

        global has_steam
        global steam
        global steamapi

        try:
            import sys
            import os
            import ctypes

            if renpy.windows and (sys.maxsize > (1 << 32)):
                dll_name = "steam_api64.dll"
            elif renpy.windows:
                dll_name = "steam_api.dll"
            elif renpy.macintosh:
                dll_name = "libsteam_api.dylib"
            else:
                dll_name = "libsteam_api.so"

            dll_path = os.path.join(os.path.dirname(sys.executable), dll_name)
            has_steam = os.path.exists(dll_path)

            if not has_steam:
                return

            if not config.enable_steam:
                return

            if "RENPY_NO_STEAM" in os.environ:
                return

            dll = ctypes.cdll[dll_path]

            import steamapi
            steamapi.load(dll)

            if not steamapi.Init():
                raise Exception("Init returned false.")

            import store._renpysteam as steam
            sys.modules["_renpysteam"] = steam

            steam.import_api()
            steamapi.init_callbacks()

            config.periodic_callbacks.append(steam.periodic)
            config.needs_redraw_callbacks.append(steam.overlay_needs_present)
            steam.set_overlay_notification_position(steam.POSITION_TOP_RIGHT)

            if steamapi.SteamUtils().IsSteamInBigPictureMode():
                config.variants.insert(0, "steam_big_picture")

            if steamapi.SteamUtils().IsSteamRunningOnSteamDeck():
                config.variants.insert(0, "steam_deck")

                if "large" in config.variants:
                    config.variants.remove("large")

                config.variants.append("medium")
                config.variants.append("touch")

            backends.insert(0, SteamBackend())
            renpy.write_log("Initialized steam.")

        except Exception as e:
            renpy.write_log("Failed to initialize steam: %r", e)
            steam = None
            steamapi = None

    steam_preinit()
    steam_init()


init 1500 python in achievement:

    # Steam position.
    if steam is not None:
        if steam_position == "top left":
            steam.set_overlay_notification_position(steam.POSITION_TOP_LEFT)
        elif steam_position == "top right":
            steam.set_overlay_notification_position(steam.POSITION_TOP_RIGHT)
        elif steam_position == "bottom left":
            steam.set_overlay_notification_position(steam.POSITION_BOTTOM_LEFT)
        elif steam_position == "bottom right":
            steam.set_overlay_notification_position(steam.POSITION_BOTTOM_RIGHT)
