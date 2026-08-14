# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

init -1499 python in wavedash:
    # Do not participate in saves.
    _constant = True

    import json
    import os
    import zipfile

    # True iff the game is running inside a Wavedash host (set by
    # wavedash_init below). Gives devs a single boolean to branch on
    # for UI guards — all wavedash.X functions also no-op gracefully
    # when False, so calling them unguarded is safe.
    is_active = False

    if renpy.emscripten:
        import emscripten  # type: ignore

        # Install the JS-side cloud-save helper. Idempotent (gated on
        # window._renpyWavedashCloud) so re-imports are safe.
        #
        # The engineInstance registration tells the Wavedash SDK to do
        # local-file IO against Ren'Py's Emscripten FS instead of the
        # SDK's IndexedDB fallback. Without it, uploadRemoteFile() can't
        # find /savegames.zip — our zipfile writes land in MEMFS.
        emscripten.run_script(r"""
            if (window.Wavedash && !window._renpyWavedashCloud) {
                if (window.Module?.FS) {
                    // SendMessage is required by sdk-js/src/services/gameEvents.ts —
                    // without it, every event (FullscreenChanged, etc.) gets dropped
                    // with an "Engine instance not set" log. Events queue on window
                    // and a Python periodic callback drains them and dispatches to
                    // any listener registered via wavedash.event_listeners.append.
                    window.Wavedash.setEngineInstance({
                        type: "RENPY",
                        FS: window.Module.FS,
                        SendMessage: (_receiver, event, data) => {
                            // SDK calls JSON.stringify(payload) before
                            // SendMessage. Parse here so listeners get a
                            // real object/value, not a JSON string.
                            let payload = data;
                            try { payload = JSON.parse(data); } catch {}
                            (window._renpyWavedashEvents ??= []).push({ event, data: payload });
                        }
                    });
                }
                window._renpyWavedashCloud = {
                    downloadStatus: 0,
                    download(path) {
                        // Generation token: a late resolution from an
                        // abandoned call can't stamp status over a fresh one.
                        const gen = this._downloadGen = (this._downloadGen || 0) + 1;
                        this.downloadStatus = 0;
                        window.Wavedash.downloadRemoteFile(path)
                            .then(() => { if (this._downloadGen === gen) this.downloadStatus = 1; })
                            .catch(() => { if (this._downloadGen === gen) this.downloadStatus = 2; });
                    },
                    upload(path) {
                        this._pendingUpload = path;
                        if (this._uploadInFlight) return;
                        this._uploadInFlight = true;
                        const pump = () => {
                            const p = this._pendingUpload;
                            this._pendingUpload = null;
                            if (!p) { this._uploadInFlight = false; return; }
                            window.Wavedash.uploadRemoteFile(p).then(pump, pump);
                        };
                        pump();
                    },
                };
            }
        """)

    # Avatar size presets in pixels, mirroring Wavedash.AvatarSize on the
    # JS SDK. Any positive integer also works as a custom size.
    AVATAR_SIZE_SMALL = 64
    AVATAR_SIZE_MEDIUM = 128
    AVATAR_SIZE_LARGE = 256


    def _args(args):
        # JSON is a strict subset of JS expression syntax, so json.dumps
        # produces something we can paste directly into JS source.
        return ", ".join(json.dumps(a) for a in args)


    def _call(method, *args):
        """
        Calls `window.Wavedash.<method>(<args>)` for a method that returns
        nothing of interest. No-op outside web builds or when the SDK is
        not present.
        """

        if not renpy.emscripten:
            return
        emscripten.run_script(f"window.Wavedash?.{method}({_args(args)})")


    def _call_int(method, *args):
        """
        Calls `window.Wavedash.<method>(<args>)` for a method that returns
        an int (or a boolean, coerced via `| 0`). Returns 0 outside web
        builds or when the SDK is not present.
        """

        if not renpy.emscripten:
            return 0
        # `undefined | 0` is 0, so optional chaining handles the
        # SDK-missing case without an explicit ternary.
        return emscripten.run_script_int(
            f"window.Wavedash?.{method}({_args(args)}) | 0"
        )


    def _call_json(method, *args):
        """
        Calls `window.Wavedash.<method>(<args>)` for a method that returns
        a JSON-serializable value, and decodes the result on the Python
        side. Returns None outside web builds, when the SDK is not
        present, or when the value is undefined.
        """

        if not renpy.emscripten:
            return None
        # `?? null` covers both SDK-missing (left of `?.` is undefined)
        # and method-returned-undefined (e.g. getUsername for an unknown
        # user) - JSON.stringify(undefined) returns undefined (not a
        # string), which would break json.loads on the Python side.
        rv = emscripten.run_script_string(
            f"JSON.stringify(window.Wavedash?.{method}({_args(args)}) ?? null)"
        )

        try:
            return json.loads(rv)
        except (TypeError, ValueError):
            return None


    # --- Event delivery ---
    #
    # Module-scoped (not config.*) because event dispatch is a Wavedash-
    # specific concern, not a generic Ren'Py mechanism — unlike
    # config.save_callbacks, which any mod can hook. Mirrors the
    # Ren'Py-idiomatic `config.X.append(callback)` shape:
    #
    #     init python:
    #         def on_event(event, data):
    #             if event == "FullscreenChanged":
    #                 ...
    #         wavedash.event_listeners.append(on_event)

    event_listeners = []


    def _drain_events():
        """
        Drain the JS-side event queue and dispatch each event to every
        registered listener. Registered as a periodic_callback by
        wavedash_init so it runs on every Ren'Py interaction tick.
        """

        if not renpy.emscripten:
            return
        raw = emscripten.run_script_string(
            "JSON.stringify((window._renpyWavedashEvents ??= []).splice(0))"
        )

        try:
            events = json.loads(raw)
        except (TypeError, ValueError):
            return

        for ev in events:
            for cb in event_listeners:
                try:
                    cb(ev["event"], ev["data"])
                except Exception:
                    renpy.display.log.exception()


    # --- Lifecycle ---

    def init_sdk(**config):
        """
        :doc: wavedash_lifecycle

        Signals to Wavedash that the game is loaded and interactive. This
        dismisses the Wavedash loading overlay and unblocks SDK event
        delivery. Idempotent - safe to call from `before_main_menu`, which
        Ren'Py re-runs every time the player returns to the main menu.

        Any keyword arguments are forwarded as the JS-side WavedashConfig,
        e.g. `init_sdk(debug=True)` to enable verbose SDK logging.
        """

        if not renpy.emscripten:
            return
        # Gate on a JS-side flag so repeated calls (e.g. on every main-menu
        # return) are silent no-ops.
        emscripten.run_script(f"""
            if (window.Wavedash && !window._renpyWavedashInitCalled) {{
                window._renpyWavedashInitCalled = true;
                window.Wavedash.init({json.dumps(config)});
            }}
        """)


    # --- Achievements & Stats ---

    def set_achievement(identifier):
        """
        :doc: wavedash_stats

        Sets the achievement with `identifier` as unlocked on Wavedash.
        Flushed to the server immediately.
        """

        _call("setAchievement", identifier, True)


    def get_achievement(identifier):
        """
        :doc: wavedash_stats

        Returns True if the achievement with `identifier` is unlocked on
        Wavedash, False otherwise. The PersistentBackend is the source of
        truth for local state, so a False return here does not mean the
        achievement is unknown game-wide.
        """

        return bool(_call_int("getAchievement", identifier))


    def set_stat(identifier, value):
        """
        :doc: wavedash_stats

        Sets the stat with `identifier` to `value` on Wavedash. Flushed
        immediately. `value` can be an int or a float.
        """

        _call("setStat", identifier, value, True)


    def get_stat(identifier):
        """
        :doc: wavedash_stats

        Returns the value of the stat with `identifier` (int or float),
        or 0 if no such stat exists.
        """

        return _call_json("getStat", identifier)


    # --- User ---

    def get_username(user_id=None):
        """
        :doc: wavedash_user

        Returns the user's publicly-visible username.

        If `user_id` is None, returns the current player's username. If a
        `user_id` is given, returns that user's username, or None if the
        game has not yet seen that user (a user is "seen" when they appear
        in a listFriends() response or share a lobby with the player).
        """

        if user_id is None:
            return _call_json("getUsername")

        return _call_json("getUsername", user_id)


    def get_user_id():
        """
        :doc: wavedash_user

        Returns the current player's Wavedash user id, or None if the SDK
        is not present.
        """

        return _call_json("getUserId")


    def get_user_avatar_url(user_id, size=AVATAR_SIZE_MEDIUM):
        """
        :doc: wavedash_user

        Returns a CDN url for the avatar of the user with `user_id`,
        transformed for the requested `size`. `size` is a pixel value -
        any positive integer works, with :const:`wavedash.AVATAR_SIZE_SMALL`
        (64), :const:`.AVATAR_SIZE_MEDIUM` (128), and
        :const:`.AVATAR_SIZE_LARGE` (256) provided as common presets.

        Returns None if the user is not cached or has no avatar. Users are
        cached after appearing in a listFriends() response or sharing a
        lobby with the player.
        """

        return _call_json("getUserAvatarUrl", user_id, int(size))


    def get_launch_params():
        """
        :doc: wavedash_user

        Returns a dictionary of the URL query parameters that were present
        when the game was launched. The well-known `lobby` key holds a
        lobby id when the player launched into the game from a lobby
        invite link.
        """

        return _call_json("getLaunchParams")


    # --- Cloud Saves ---

    # Whole-savedir-as-zip sync via Wavedash.uploadRemoteFile /
    # downloadRemoteFile. The JS-side helper is installed at the top of
    # this module; see _renpyWavedashCloud above.
    #
    # The zip is read/written at CLOUD_SAVE_FILE (an absolute MEMFS path)
    # so the round-trip is CWD-independent. We use our own zip/unzip
    # rather than renpy.savelocation.{zip,unzip}_saves() because those
    # use a relative filename and are intended for callers (the launcher
    # Import/Export buttons) that drive them from a known CWD.
    #
    # Pull on launch: blocks Python boot up to CLOUD_PULL_TIMEOUT_S so the
    # save scanner picks up cloud-pulled slots before the main menu
    # appears. Push on save: fire-and-forget; the save UI doesn't wait
    # for the network. The JS-side upload helper coalesces concurrent
    # pushes into at most one queued upload so rapid saves can't land
    # out of order on the server. Conflict resolution is last-write-wins
    # on the whole zip.

    CLOUD_SAVE_FILE = "/savegames.zip"
    CLOUD_PULL_TIMEOUT_S = 30.0
    CLOUD_POLL_INTERVAL_MS = 50

    # Status values returned by _renpyWavedashCloud.downloadStatus and
    # mirrored on the Python side for readability. Numeric on the wire
    # because that's the cheapest representation through run_script_int.
    _CLOUD_PENDING = 0
    _CLOUD_OK = 1
    _CLOUD_ERROR = 2

    def cloud_pull():
        """
        :doc: wavedash_cloud

        Downloads `/savegames.zip` from Wavedash into IDBFS, blocking until
        complete or `CLOUD_PULL_TIMEOUT_S` seconds elapse. Returns True on
        success (zip is in IDBFS, ready for `unzip_saves()`), False on
        timeout or remote error (e.g. no remote zip yet for new users).
        """

        if not renpy.emscripten:
            return False

        import time

        if not emscripten.run_script_int("window._renpyWavedashCloud ? 1 : 0"):
            return False

        emscripten.run_script(
            f"window._renpyWavedashCloud.download({json.dumps(CLOUD_SAVE_FILE)})"
        )

        deadline = time.time() + CLOUD_PULL_TIMEOUT_S

        while time.time() < deadline:
            status = emscripten.run_script_int(
                "window._renpyWavedashCloud.downloadStatus"
            )

            if status == _CLOUD_OK:
                return True
            if status == _CLOUD_ERROR:
                renpy.write_log("Wavedash cloud pull: remote error")
                return False

            # emscripten.sleep yields to the JS event loop so the Promise
            # callbacks above can run; time.sleep would block the WASM
            # thread and the Promise would never resolve.
            emscripten.sleep(CLOUD_POLL_INTERVAL_MS)

        renpy.write_log("Wavedash cloud pull: timeout after %s seconds", CLOUD_PULL_TIMEOUT_S)
        return False


    def cloud_push(slotname=None):
        """
        :doc: wavedash_cloud

        Re-zips the local savedir into IDBFS and fires off an upload to
        Wavedash. Fire-and-forget; the upload runs in the background after
        this call returns. Multiple rapid pushes coalesce JS-side into at
        most one queued upload, so concurrent saves can't land out of
        order on the server. Intended for use as a
        `config.save_callbacks` entry; the slotname is accepted but not
        used.
        """

        if not renpy.emscripten:
            return

        savedir = renpy.config.savedir
        if not savedir or not os.path.isdir(savedir):
            return

        # ZIP_STORED, not ZIP_DEFLATED: Ren'Py's .save files are themselves
        # zipfiles, so the outer compression burns CPU for no size win.
        try:
            with zipfile.ZipFile(CLOUD_SAVE_FILE, "w", zipfile.ZIP_STORED) as zf:
                for root, _, files in os.walk(savedir):
                    for name in files:
                        full = os.path.join(root, name)
                        zf.write(full, os.path.relpath(full, savedir))
        except Exception:
            # A zip failure (e.g. quota, MEMFS error) must not break the
            # save callback chain or fail the player's local save.
            renpy.display.log.exception()
            return

        emscripten.run_script(
            f"window._renpyWavedashCloud?.upload({json.dumps(CLOUD_SAVE_FILE)})"
        )


    def cloud_extract():
        """
        Extracts CLOUD_SAVE_FILE into renpy.config.savedir. Called by
        wavedash_init() after a successful cloud_pull().
        """

        if not renpy.emscripten:
            return

        savedir = renpy.config.savedir
        if not savedir:
            return

        os.makedirs(savedir, exist_ok=True)

        try:
            with zipfile.ZipFile(CLOUD_SAVE_FILE, "r") as zf:
                # Path-traversal guard: the remote zip is server-controlled
                # but a malformed or compromised entry shouldn't escape
                # savedir. Skip anything absolute or containing '..'.
                safe = []
                for info in zf.infolist():
                    name = info.filename
                    if name.startswith("/") or ".." in name.replace("\\", "/").split("/"):
                        continue
                    safe.append(info)
                zf.extractall(savedir, members=safe)
        except Exception:
            # A bad zip must not abort wavedash_init - the rest of the
            # backend (achievements, etc.) still needs to wire up.
            renpy.display.log.exception()


    # --- Fullscreen ---

    # Wavedash's host page owns the real fullscreen target; the game
    # iframe can't usefully request fullscreen on its own. Ren'Py's
    # built-in fullscreen toggle (Preference("display", ...)) talks to
    # the iframe and is therefore a no-op on Wavedash web - call these
    # helpers from your preferences screen instead.

    def is_fullscreen():
        """
        :doc: wavedash_fullscreen

        Returns True if the host page is currently fullscreen.
        """

        return bool(_call_int("isFullscreen"))


    def request_fullscreen(fullscreen):
        """
        :doc: wavedash_fullscreen

        Asks the host page to enter (`fullscreen=True`) or exit
        (`fullscreen=False`) fullscreen. Entering must be triggered from
        a user gesture (click / keydown handler) - browsers refuse the
        request otherwise.
        """

        _call("requestFullscreen", bool(fullscreen))


    def toggle_fullscreen():
        """
        :doc: wavedash_fullscreen

        Toggles fullscreen. Like `request_fullscreen(True)`, entering
        must be triggered from a user gesture for the browser to permit
        it.
        """

        _call("toggleFullscreen")


    # --- Overlay ---

    def toggle_overlay():
        """
        :doc: wavedash_overlay

        Toggles the Wavedash overlay UI on top of the game. The overlay
        hosts platform-level features (friends, lobbies, settings) and is
        always available to the player; this just lets the game open it
        from a button in its own menus.
        """

        _call("toggleOverlay")


init -1499 python in achievement:

    class WavedashBackend(Backend):
        """
        A backend that forwards achievement grants to Wavedash. Only
        registered when the game runs as a Wavedash web build.
        """

        def grant(self, name):
            wavedash.set_achievement(name)

        def has(self, name):
            return wavedash.get_achievement(name)


    # The store.wavedash namespace, or None if we're not running on
    # Wavedash (desktop build, or a web build hosted somewhere else).
    # Bound lazily by wavedash_init() after the window.Wavedash probe,
    # mirroring how _renpysteam is bound here (see 00steam.rpy).
    wavedash = None

    def wavedash_init():
        global wavedash

        if not renpy.emscripten:
            return

        # Probe for window.Wavedash before registering. Without this,
        # wavedash.is_active would be True on any web build, and devs'
        # `if wavedash.is_active:` UI guards would surface Wavedash UI
        # on non-Wavedash deployments (where the calls would silently
        # no-op anyway).
        import emscripten  # type: ignore
        if not emscripten.run_script_int("window.Wavedash ? 1 : 0"):
            return

        import store.wavedash as wavedash
        wavedash.is_active = True
        backends.append(WavedashBackend())

        # Cloud-save sync. cloud_pull must complete before the save
        # scanner runs - so we rescan after a successful pull. Falls
        # through to local-only on pull failure (network down,
        # first-time user with no remote zip).
        if wavedash.cloud_pull():
            wavedash.cloud_extract()
            renpy.loadsave.location.scan()

        config.save_callbacks.append(wavedash.cloud_push)
        config.periodic_callbacks.append(wavedash._drain_events)

        renpy.write_log("Initialized Wavedash.")

    wavedash_init()
