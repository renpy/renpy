# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This code applies an update.
init -1500 python in updater:
    # Do not participate in saves.
    _constant = True

    from store import renpy, config, Action, DictEquality, persistent
    import store.build as build

    import tarfile
    import threading
    import traceback
    import os
    import urllib.parse as urlparse
    import json
    import subprocess
    import hashlib
    import time
    import sys
    import struct
    import zlib
    import codecs
    import io
    import future.utils

    def urlopen(url):
        import requests
        return io.BytesIO(requests.get(url).content)

    def urlretrieve(url, fn):
        import requests

        data = requests.get(url).content

        with open(fn, "wb") as f:
            f.write(data)

    try:
        import rsa
    except Exception:
        rsa = None

    from renpy.exports import fsencode

    # A map from update URL to the last version found at that URL.
    if persistent._update_version is None:
        persistent._update_version = { }

    # A map from update URL to the time we last checked that URL.
    if persistent._update_last_checked is None:
        persistent._update_last_checked = { }

    # A file containing deferred update commands, one per line. Right now,
    # there are two commands:
    # R <path>
    #     Rename <path>.new to <path>.
    # D <path>
    #     Delete <path>.
    # Deferred commands that cannot be accomplished on start are ignored.
    DEFERRED_UPDATE_FILE = os.path.join(config.renpy_base, "update", "deferred.txt")
    DEFERRED_UPDATE_LOG = os.path.join(config.renpy_base, "update", "log.txt")

    def process_deferred_line(l):

        cmd, _, fn = l.partition(" ")

        if cmd == "R":
            if os.path.exists(fn + ".new"):

                if os.path.exists(fn):
                    os.unlink(fn)

                os.rename(fn + ".new", fn)

        elif cmd == "D":

            if os.path.exists(fn):
                os.unlink(fn)

        elif cmd == "":

            pass

        else:
            raise Exception("Bad command. %r (%r %r)" % (l, cmd, fn))

    def process_deferred():
        if not os.path.exists(DEFERRED_UPDATE_FILE):
            return

        # Give a previous process time to quit (and let go of the
        # open files.)
        time.sleep(3)

        try:
            log = open(DEFERRED_UPDATE_LOG, "a")
        except Exception:
            log = io.BytesIO()

        with log:
            with open(DEFERRED_UPDATE_FILE, "r") as f:
                for l in f:

                    l = l.rstrip("\r\n")

                    log.write(l)

                    try:
                        process_deferred_line(l)
                    except Exception:
                        traceback.print_exc(file=log)

            try:
                os.unlink(DEFERRED_UPDATE_FILE + ".old")
            except Exception:
                pass

            try:
                os.rename(DEFERRED_UPDATE_FILE, DEFERRED_UPDATE_FILE + ".old")
            except Exception:
                traceback.print_exc(file=log)

    # Process deferred updates on startup, if any exist.

    process_deferred()

    DELETED = os.path.join(config.renpy_base, "update", "deleted")

    def process_deleted():
        if not os.path.exists(DELETED):
            return

        import shutil

        try:
            shutil.rmtree(DELETED)
        except Exception as e:
            pass

    process_deleted()

    def zsync_path(command):
        """
        Returns the full platform-specific path to command, which is one
        of zsync or zsyncmake. If the file doesn't exists, returns the
        command so the system-wide copy is used.
        """

        if renpy.windows:
            suffix = ".exe"
        else:
            suffix = ""

        executable = renpy.fsdecode(sys.executable)

        rv = os.path.join(os.path.dirname(executable), command + suffix)

        if os.path.exists(rv):
            return rv

        return command + suffix

    class UpdateError(Exception):
        """
        Used to report known errors.
        """

    class UpdateCancelled(Exception):
        """
        Used to report the update being cancelled.
        """

    class Updater(threading.Thread):
        """
        Applies an update.

        Fields on this object are used to communicate the state of the update process.

        self.state
            The state that the updater is in.

        self.message
            In an error state, the error message that occured.

        self.progress
            If not None, a number between 0.0 and 1.0 giving some sort of
            progress indication.

        self.can_cancel
            A boolean that indicates if cancelling the update is allowed.

        """

        # Here are the possible states.

        # An error occured during the update process.
        # self.message is set to the error message.
        ERROR = "ERROR"

        # Checking to see if an update is necessary.
        CHECKING = "CHECKING"

        # We are up to date. The update process has ended.
        # Calling proceed will return to the main menu.
        UPDATE_NOT_AVAILABLE = "UPDATE NOT AVAILABLE"

        # An update is available.
        # The interface should ask the user if he wants to upgrade, and call .proceed()
        # if he wants to continue.
        UPDATE_AVAILABLE = "UPDATE AVAILABLE"

        # Preparing to update by packing the current files into a .update file.
        # self.progress is updated during this process.
        PREPARING = "PREPARING"

        # Downloading the update.
        # self.progress is updated during this process.
        DOWNLOADING = "DOWNLOADING"

        # Unpacking the update.
        # self.progress is updated during this process.
        UNPACKING = "UNPACKING"

        # Finishing up, by moving files around, deleting obsolete files, and writing out
        # the state.
        FINISHING = "FINISHING"

        # Done. The update completed successfully.
        # Calling .proceed() on the updater will trigger a game restart.
        DONE = "DONE"

        # Done. The update completed successfully.
        # Calling .proceed() on the updater will trigger a game restart.
        DONE_NO_RESTART = "DONE_NO_RESTART"

        # The update was cancelled.
        CANCELLED = "CANCELLED"

        def __init__(self, url, base=None, force=False, public_key=None, simulate=None, add=[], restart=True, check_only=False, confirm=True, patch=True, prefer_rpu=True, size_only=False, allow_empty=False, done_pause=True, allow_cancel=True):
            """
            Takes the same arguments as update().
            """

            # Make sure the URL has the right type.
            url = str(url)

            self.patch = patch

            if not url.startswith("http:"):
                self.patch = False

            threading.Thread.__init__(self)

            import os
            if "RENPY_FORCE_UPDATE" in os.environ:
                force = True

            # The main state.
            self.state = Updater.CHECKING

            # An additional message to show to the user.
            self.message = None

            # The progress of the current operation, or None.
            self.progress = None

            # True if the user can click the cancel button.
            self.can_cancel = True

            # True if the user can click the proceed button.
            self.can_proceed = False

            # True if the user has clicked the cancel button.
            self.cancelled = False

            # True if the user has clocked the proceed button.
            self.proceeded = False

            # The url of the updates.json file.
            self.url = url

            # Force the update?
            self.force = force

            # Packages to add during the update.
            self.add = add

            # Do we need to restart Ren'Py at the end?
            self.restart = restart

            # If true, we check for an update, and update persistent._update_version
            # as appropriate.
            self.check_only = check_only

            # Do we prompt for confirmation?
            self.confirm = confirm

            # Should rpu updates be preferred?
            self.prefer_rpu = prefer_rpu

            # Should the update be allowed even if current.json is empty?
            self.allow_empty = allow_empty

            # Should the user be asked to proceed when done.
            self.done_pause = done_pause

            # Should the user be allowed to cancel the update?
            self.allow_cancel = False

            # Public attributes set by the RPU updater
            self.new_disk_size = None
            self.old_disk_size = None

            self.download_total = None
            self.download_done = None

            self.write_total = None
            self.write_done = None

            # The base path of the game that we're updating, and the path to the update
            # directory underneath it.

            if base is None:
                base = config.basedir

            self.base = os.path.abspath(base)
            self.updatedir = os.path.join(self.base, "update")

            # If we're a mac, the directory in which our app lives.
            splitbase = self.base.split('/')
            if (len(splitbase) >= 4 and
                splitbase[-1] == "autorun" and
                splitbase[-2] == "Resources" and
                splitbase[-3] == "Contents" and
                splitbase[-4].endswith(".app")):

                self.app = "/".join(splitbase[:-3])
            else:
                self.app = None

            # A condition that's used to coordinate things between the various
            # threads.
            self.condition = threading.Condition()

            # The modules we'll be updating.
            self.modules = [ ]

            # A list of files that have to be moved into place. This is a list of filenames,
            # where each file is moved from <file>.new to <file>.
            self.moves = [ ]

            if self.allow_empty:
                if not os.path.isdir(self.updatedir):
                    os.makedirs(self.updatedir)

            if public_key is not None:
                with renpy.open_file(public_key, False) as f:
                    self.public_key = rsa.PublicKey.load_pkcs1(f.read())
            else:
                self.public_key = None

            # The logfile that update errors are written to.
            try:
                self.log = open(os.path.join(self.updatedir, "log.txt"), "w")
            except Exception:
                self.log = None

            self.simulate = simulate

            self.daemon = True
            self.start()


        def run(self):
            """
            The main function of the update thread, handles errors by reporting
            them to the user.
            """

            try:
                if self.simulate:
                    self.simulation()
                else:
                    self.update()

            except UpdateCancelled as e:
                self.can_cancel = False
                self.can_proceed = True
                self.progress = None
                self.message = None
                self.state = self.CANCELLED

                if self.log:
                    traceback.print_exc(None, self.log)
                    self.log.flush()

            except UpdateError as e:
                self.message = e.args[0]
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.ERROR

                if self.log:
                    traceback.print_exc(None, self.log)
                    self.log.flush()

            except Exception as e:
                self.message = _type(e).__name__ + ": " + unicode(e)
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.ERROR

                if self.log:
                    traceback.print_exc(None, self.log)
                    self.log.flush()

            self.clean_old()

            if self.log:
                self.log.close()

        def update(self):
            """
            Performs the update.
            """

            self.load_state()
            self.test_write()
            self.check_updates()

            self.pretty_version = self.check_versions()

            if not self.modules:
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.UPDATE_NOT_AVAILABLE
                persistent._update_version[self.url] = None
                renpy.restart_interaction()
                return

            persistent._update_version[self.url] = self.pretty_version

            if self.check_only:
                renpy.restart_interaction()
                return

            # Disable autoreload.
            renpy.set_autoreload(False)

            self.new_state = dict(self.current_state)
            renpy.restart_interaction()

            self.progress = 0.0
            self.state = self.PREPARING

            import os

            has_rpu = False
            has_zsync = False

            prefer_rpu = self.prefer_rpu or "RPU_UPDATE" in os.environ

            for i in self.modules:

                for d in self.updates:
                    if "rpu_url" in self.updates[d]:
                        has_rpu = True
                    if "zsync_url" in self.updates[d]:
                        has_zsync = True

            if has_rpu and has_zsync:

                if prefer_rpu:
                    self.rpu_update()
                else:
                    self.zsync_update()

            elif has_rpu:
                self.rpu_update()

            elif has_zsync:
                self.zsync_update()

            else:
                raise UpdateError(_("No update methods found."))


        def prompt_confirm(self):
            """
            Prompts the user to confirm the update. Returns if the update
            should proceed, or raises UpdateCancelled if it should not.
            """

            if self.confirm:

                self.progress = None

                # Confirm with the user that the update is available.
                with self.condition:
                    self.can_cancel = self.allow_cancel
                    self.can_proceed = True
                    self.state = self.UPDATE_AVAILABLE
                    self.version = self.pretty_version

                    renpy.restart_interaction()

                    while self.confirm:
                        if self.cancelled or self.proceeded:
                            break

                        self.condition.wait(.1)

            if self.cancelled:
                raise UpdateCancelled()

            self.can_cancel = False
            self.can_proceed = False

        def fetch_files_rpu(self, module):
            """
            Fetches the rpu file list for the given module.
            """

            import requests, zlib

            url = urlparse.urljoin(self.url, self.updates[module]["rpu_url"])

            try:
                resp = requests.get(url)
                resp.raise_for_status()
            except Exception as e:
                raise UpdateError(__("Could not download file list: ") + str(e))

            if hashlib.sha256(resp.content).hexdigest() != self.updates[module]["rpu_digest"]:
                raise UpdateError(__("File list digest does not match."))

            data = zlib.decompress(resp.content)

            from renpy.update.common import FileList

            rv = FileList.from_json(json.loads(data))
            return rv

        def rpu_copy_fields(self):
            """
            Copy fields from the rpu object.
            """

            self.old_disk_total = self.u.old_disk_total
            self.new_disk_total = self.u.new_disk_total

            self.download_total = self.u.download_total
            self.download_done = self.u.download_done

            self.write_total = self.u.write_total
            self.write_done = self.u.write_done

        def rpu_progress(self, state, progress):
            """
            Called by the rpu code to update the progress.
            """

            self.rpu_copy_fields()

            old_state = self.state

            self.state = state
            self.progress = progress

            if state != old_state or progress == 1.0 or progress == 0.0:
                renpy.restart_interaction()

        def rpu_update(self):
            """
            Perform an update using the .rpu files.
            """

            from renpy.update.common import FileList
            from renpy.update.update import Update

            # 1. Load the current files.

            target_file_lists = [ ]

            for i in self.modules:
                target_file_lists.append(FileList.from_current_json(self.current_state[i]))

            # 2. Fetch the file lists.

            source_file_lists = [ ]
            module_lists = { }

            for i in self.modules:
                fl = self.fetch_files_rpu(i)
                module_lists[i] = fl
                source_file_lists.append(fl)

            # 3. Compute the update, and confirm it.

            self.u = Update(
                urlparse.urljoin(self.url, "rpu"),
                source_file_lists,
                self.base,
                target_file_lists,
                progress_callback=self.rpu_progress,
                logfile=self.log
            )

            self.u.init()

            self.rpu_copy_fields()

            self.prompt_confirm()

            self.can_cancel = False

            # 4. Remove the version.json file.

            version_json = os.path.join(self.updatedir, "version.json")

            if os.path.exists(version_json):
                os.unlink(version_json)

            # 5. Apply the update.
            self.u.update()

            # 6. Update the new state.
            for i in self.modules:
                d = module_lists[i].to_current_json()
                d["version"] = self.updates[i]["version"]
                d["renpy_version"] = self.updates[i]["renpy_version"]
                d["pretty_version"] = self.updates[i]["pretty_version"]
                self.new_state[i] = d

            # 7. Write the version.json file.
            version_state = { }

            for i in self.modules:
                version_state[i] = {
                    "version" : self.updates[i]["version"],
                    "renpy_version" : self.updates[i]["renpy_version"],
                    "pretty_version" : self.updates[i]["pretty_version"]
                    }

                with open(os.path.join(self.updatedir, "version.json"), "w") as f:
                    json.dump(version_state, f)

            # 8. Finish up.

            persistent._update_version[self.url] = None

            if self.restart:
                self.state = self.DONE
            else:
                self.state = self.DONE_NO_RESTART

            self.message = None
            self.progress = None
            self.can_proceed = self.done_pause
            self.can_cancel = False

            renpy.restart_interaction()

        def zsync_update(self):

            self.prompt_confirm()
            self.can_cancel = self.allow_cancel

            if self.patch:
                for i in self.modules:
                    self.prepare(i)

            self.progress = 0.0
            self.state = self.DOWNLOADING
            renpy.restart_interaction()

            for i in self.modules:

                if self.patch:

                    try:
                        self.download(i)
                    except Exception:
                        self.download(i, standalone=True)

                else:
                    self.download_direct(i)

            self.clean_old()

            self.can_cancel = False
            self.progress = 0.0
            self.state = self.UNPACKING
            renpy.restart_interaction()

            for i in self.modules:
                self.unpack(i)

            self.progress = None
            self.state = self.FINISHING
            renpy.restart_interaction()

            self.move_files()
            self.delete_obsolete()
            self.save_state()
            self.clean_new()

            persistent._update_version[self.url] = None

            if self.restart:
                self.state = self.DONE
            else:
                self.state = self.DONE_NO_RESTART

            self.message = None
            self.progress = None
            self.can_proceed = self.done_pause
            self.can_cancel = False

            renpy.restart_interaction()

            return

        def simulation(self):
            """
            Simulates the update.
            """

            def simulate_progress():
                for i in range(0, 30):
                    self.progress = i / 30.0
                    time.sleep(.1)

                    if self.cancelled:
                        raise UpdateCancelled()

            time.sleep(1.5)

            if self.cancelled:
                raise UpdateCancelled()

            if self.simulate == "error":
                raise UpdateError(_("An error is being simulated."))

            if self.simulate == "not_available":
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.UPDATE_NOT_AVAILABLE
                persistent._update_version[self.url] = None
                return

            pretty_version = build.version or build.directory_name
            persistent._update_version[self.url] = pretty_version

            if self.check_only:
                renpy.restart_interaction()
                return

            # Confirm with the user that the update is available.

            self.prompt_confirm()

            if self.cancelled:
                raise UpdateCancelled()

            self.progress = 0.0
            self.state = self.PREPARING
            renpy.restart_interaction()

            simulate_progress()

            self.progress = 0.0
            self.state = self.DOWNLOADING
            renpy.restart_interaction()

            simulate_progress()

            self.can_cancel = False
            self.progress = 0.0
            self.state = self.UNPACKING
            renpy.restart_interaction()

            simulate_progress()

            self.progress = None
            self.state = self.FINISHING
            renpy.restart_interaction()

            time.sleep(1.5)

            persistent._update_version[self.url] = None

            if self.restart:
                self.state = self.DONE
            else:
                self.state = self.DONE_NO_RESTART

            self.message = None
            self.progress = None
            self.can_proceed = self.done_pause
            self.can_cancel = False

            renpy.restart_interaction()

            return

        def periodic(self):
            """
            Called periodically by the screen.
            """

            renpy.restart_interaction()

            if self.state == self.DONE or self.state == self.DONE_NO_RESTART:
                if not self.done_pause:
                    return self.proceed(force=True)

        def proceed(self, force=False):
            """
            Causes the upgraded to proceed with the next step in the process.
            """

            if not self.can_proceed and not force:
                return

            if self.state == self.UPDATE_NOT_AVAILABLE or self.state == self.ERROR or self.state == self.CANCELLED:
                return False

            elif self.state == self.DONE:
                if self.restart == "utter":
                    renpy.utter_restart()
                else:
                    renpy.quit(relaunch=True)

            elif self.state == self.DONE_NO_RESTART:
                return True

            elif self.state == self.UPDATE_AVAILABLE:
                with self.condition:
                    self.proceeded = True
                    self.condition.notify_all()

        def cancel(self):

            if not self.can_cancel:
                return

            with self.condition:
                self.cancelled = True
                self.condition.notify_all()

            if self.restart:
                renpy.full_restart()
            else:
                return False

        def unlink(self, path):
            """
            Tries to unlink the file at `path`.
            """

            if os.path.exists(path):

                import random

                newname = os.path.join(DELETED, os.path.basename(path) + "." + str(random.randint(0, 1000000)))

                try:
                    os.mkdir(DELETED)
                except Exception:
                    pass

                # This might fail because of a sharing violation on Windows.
                try:
                    os.rename(path, newname)
                    os.unlink(newname)
                except Exception:
                    pass

        def rename(self, old, new):
            """
            Renames the old name to the new name. Tries to enforce the unix semantics, even
            on windows.
            """

            try:
                os.rename(old, new)
                return
            except Exception:
                pass

            try:
                os.unlink(new)
            except Exception:
                pass

            os.rename(old, new)


        def path(self, name):
            """
            Converts a filename to a path on disk.
            """

            if self.app is not None:

                path = name.split("/")
                if path[0].endswith(".app"):
                    rv = os.path.join(self.app, "/".join(path[1:]))
                    return rv

            rv = os.path.join(self.base, name)

            if renpy.windows:
                rv = "\\\\?\\" + rv.replace("/", "\\")

            return rv

        def load_state(self):
            """
            Loads the current update state from update/current.json
            """

            fn = os.path.join(self.updatedir, "current.json")

            if not os.path.exists(fn):
                if self.allow_empty:
                    self.current_state = { }
                    return

                raise UpdateError(_("Either this project does not support updating, or the update status file was deleted."))

            with open(fn, "r") as f:
                self.current_state = json.load(f)

        def test_write(self):
            fn = os.path.join(self.updatedir, "test.txt")

            try:
                with open(fn, "w") as f:
                    f.write("Hello, World.")

                os.unlink(fn)
            except Exception:
                raise UpdateError(_("This account does not have permission to perform an update."))

            if not self.log:
                raise UpdateError(_("This account does not have permission to write the update log."))

        def check_updates(self):
            """
            Downloads the list of updates from the server, parses it, and stores it in
            self.updates.
            """

            fn = os.path.join(self.updatedir, "updates.json")
            urlretrieve(self.url, fn)

            with open(fn, "rb") as f:
                updates_json = f.read()

            # Was updates.json verified?
            verified = False

            # Does updates.json need to be verified?
            require_verified = False

            # New-style ECDSA signature.
            key = os.path.join(config.basedir, "update", "key.pem")

            if not os.path.exists(key):
                key = os.path.join(self.updatedir, "key.pem")

            if os.path.exists(key):
                require_verified = True

                self.log.write("Verifying with ECDSA.\n")

                try:

                    import ecdsa
                    verifying_key = ecdsa.VerifyingKey.from_pem(open(key, "rb").read())

                    url = urlparse.urljoin(self.url, "updates.ecdsa")
                    f = urlopen(url)

                    while True:
                        signature = f.read(64)
                        if not signature:
                            break

                        if verifying_key.verify(signature, updates_json):
                            verified = True

                    self.log.write("Verified with ECDSA.\n")

                except Exception:
                    if self.log:
                        import traceback
                        traceback.print_exc(None, self.log)

            # Old-style RSA signature.
            if self.public_key is not None:
                require_verified = True

                self.log.write("Verifying with RSA.\n")

                try:

                    fn = os.path.join(self.updatedir, "updates.json.sig")
                    urlretrieve(self.url + ".sig", fn)

                    with open(fn, "rb") as f:
                        import codecs
                        signature = codecs.decode(f.read(), "base64")

                    rsa.verify(updates_json, signature, self.public_key)
                    verified = True

                    self.log.write("Verified with RSA.\n")

                except Exception:
                    if self.log:
                        import traceback
                        traceback.print_exc(None, self.log)

            if require_verified and not verified:
                raise UpdateError(_("Could not verify update signature."))

            self.updates = json.loads(updates_json)

            if verified and "monkeypatch" in self.updates:
                future.utils.exec_(self.updates["monkeypatch"], globals(), globals())

        def add_dlc_state(self, name):

            has_rpu = "rpu_url" in self.updates[name]
            has_zsync = "zsync_url" in self.updates[name]

            prefer_rpu = self.prefer_rpu or "RPU_UPDATE" in os.environ

            if has_rpu and has_zsync:
                if prefer_rpu:
                    has_zsync = False
                else:
                    has_rpu = False

            if has_rpu:
                fl = self.fetch_files_rpu(name)
                d = { name : fl.to_current_json() }
            else:
                url = urlparse.urljoin(self.url, self.updates[name]["json_url"])
                f = urlopen(url)
                d = json.load(f)

            d[name]["version"] = 0
            self.current_state.update(d)

        def check_versions(self):
            """
            Decides what modules need to be updated, if any.
            """

            rv = None

            # A list of names of modules we want to update.
            self.modules = [ ]

            # DLC?
            if self.add:
                for name in self.add:
                    if name in self.updates:
                        self.modules.append(name)

                    if name not in self.current_state:
                        self.add_dlc_state(name)

                    rv = self.updates[name]["pretty_version"]

                return rv

            # We update the modules that are in both versions, and that are out of date.
            for name, data in self.current_state.items():

                if name not in self.updates:
                    continue

                if data["version"] == self.updates[name]["version"]:
                    if not self.force:
                        continue

                self.modules.append(name)

                rv = self.updates[name]["pretty_version"]

            return rv

        def update_filename(self, module, new):
            """
            Returns the update filename for the given module.
            """

            rv = os.path.join(self.updatedir, module + ".update")
            if new:
                return rv + ".new"

            return rv

        def prepare(self, module):
            """
            Creates a tarfile creating the files that make up module.
            """

            state = self.current_state[module]

            xbits = set(state["xbit"])
            directories = set(state["directories"])
            all = state["files"] + state["directories"]
            all.sort()

            # Add the update directory and state file.
            all.append("update")
            directories.add("update")
            all.append("update/current.json")

            with tarfile.open(self.update_filename(module, False), "w") as tf:
                for i, name in enumerate(all):

                    if self.cancelled:
                        raise UpdateCancelled()

                    self.progress = 1.0 * i / len(all)

                    directory = name in directories
                    xbit = name in xbits

                    path = self.path(name)

                    if directory:
                        info = tarfile.TarInfo(name)
                        info.size = 0
                        info.type = tarfile.DIRTYPE
                    else:
                        if not os.path.exists(path):
                            continue

                        info = tf.gettarinfo(path, name)

                        if not info.isreg():
                            continue

                    info.uid = 1000
                    info.gid = 1000
                    info.mtime = 0
                    info.uname = "renpy"
                    info.gname = "renpy"

                    if xbit or directory:
                        info.mode = 0o777
                    else:
                        info.mode = 0o666

                    if info.isreg():
                        with open(path, "rb") as f:
                            tf.addfile(info, f)
                    else:
                        tf.addfile(info)

        def split_inputs(self, sfn):
            """
            Given an input file `sfn`, returns a list of option arguments and
            input files that can be supplied to zsync.
            """

            size = os.path.getsize(sfn)

            if size < (1 << 30):
                return [ "-i", sfn ]

            rv = [ ]

            with open(sfn, "rb") as f:
                count = 0

                while count * (1 << 30) < size:
                    count += 1

                    out_fn = sfn + "." + str(count)

                    with open(out_fn, "wb") as out_f:

                        for i in range(1 << 4):

                            data = f.read(1 << 26)

                            if not data:
                                break

                            out_f.write(data)

                    rv.extend([ "-i", out_fn ])

            return rv

        def download(self, module, standalone=False):
            """
            Uses zsync to download the module.
            """

            start_progress = None

            new_fn = self.update_filename(module, True)

            # Download the sums file.
            sums = [ ]

            f = urlopen(urlparse.urljoin(self.url, self.updates[module]["sums_url"]))
            data = f.read()

            for i in range(0, len(data), 4):
                try:
                    sums.append(struct.unpack("<I", data[i:i+4])[0])
                except Exception:
                    pass

            f.close()

            # Figure out the zsync command.

            zsync_fn = os.path.join(self.updatedir, module + ".zsync")

            # May not exist, but if it does, we want to delete it.
            try:
                os.unlink(zsync_fn + ".part")
            except Exception:
                pass

            try:
                os.unlink(new_fn)
            except Exception:
                pass

            cmd = [
                zsync_path("zsync"),
                "-o", new_fn,
                ]

            if not standalone:
                cmd.extend([
                    "-k", zsync_fn,
                ])

            if os.path.exists(new_fn + ".part"):
                self.rename(new_fn + ".part", new_fn + ".part.old")

                if not standalone:
                    cmd.extend(self.split_inputs(new_fn + ".part.old"))

            if not standalone:
                for i in self.modules:
                    cmd.extend(self.split_inputs(self.update_filename(i, False)))

            cmd.append(urlparse.urljoin(self.url, self.updates[module]["zsync_url"]))

            cmd = [ fsencode(i) for i in cmd ]

            self.log.write("running %r\n" % cmd)
            self.log.flush()

            if renpy.windows:

                CREATE_NO_WINDOW=0x08000000
                p = subprocess.Popen(cmd,
                    stdin=subprocess.PIPE,
                    stdout=self.log,
                    stderr=self.log,
                    creationflags=CREATE_NO_WINDOW,
                    cwd=renpy.fsencode(self.updatedir))
            else:

                p = subprocess.Popen(cmd,
                    stdin=subprocess.PIPE,
                    stdout=self.log,
                    stderr=self.log,
                    cwd=renpy.fsencode(self.updatedir))

            p.stdin.close()

            while True:
                if self.cancelled:
                    p.kill()
                    break

                time.sleep(1)

                if p.poll() is not None:
                    break

                try:
                    f = open(new_fn + ".part", "rb")
                except Exception:
                    self.log.write("partfile does not exist\n")
                    continue

                done_sums = 0

                with f:
                    for i in sums:

                        if self.cancelled:
                            break

                        data = f.read(65536)

                        if not data:
                            break

                        if (zlib.adler32(data) & 0xffffffff) == i:
                            done_sums += 1

                raw_progress = 1.0 * done_sums / len(sums)

                if raw_progress == 1.0:
                    start_progress = None
                    self.progress = 1.0
                    continue

                if start_progress is None:
                    start_progress = raw_progress
                    self.progress = 0.0
                    continue

                self.progress = (raw_progress - start_progress) / (1.0 - start_progress)

            p.wait()

            self.log.seek(0, 2)

            if self.cancelled:
                raise UpdateCancelled()

            # Check the existence of the downloaded file.
            if not os.path.exists(new_fn):
                if os.path.exists(new_fn + ".part"):
                    os.rename(new_fn + ".part", new_fn)
                else:
                    raise UpdateError(_("The update file was not downloaded."))

            # Check that the downloaded file has the right digest.
            import hashlib
            with open(new_fn, "rb") as f:
                hash = hashlib.sha256()

                while True:
                    data = f.read(1024 * 1024)

                    if not data:
                        break

                    hash.update(data)

                digest = hash.hexdigest()

            if digest != self.updates[module]["digest"]:
                raise UpdateError(_("The update file does not have the correct digest - it may have been corrupted."))

            if os.path.exists(new_fn + ".part.old"):
                os.unlink(new_fn + ".part.old")

            if self.cancelled:
                raise UpdateCancelled()


        def download_direct(self, module):
            """
            Uses zsync to download the module.
            """

            import requests

            start_progress = None

            new_fn = self.update_filename(module, True)
            part_fn = new_fn + ".part.gz"

            # Figure out the zsync command.

            zsync_fn = os.path.join(self.updatedir, module + ".zsync")

            try:
                os.unlink(new_fn)
            except Exception:
                pass

            zsync_url = self.updates[module]["zsync_url"][:-6] + ".update.gz"
            url = urlparse.urljoin(self.url, zsync_url)

            self.log.write("downloading %r\n" % url)
            self.log.flush()

            resp = requests.get(url, stream=True)

            if not resp.ok:
                raise UpdateError(_("The update file was not downloaded."))

            try:
                length = int(resp.headers.get("Content-Length", "20000000"))
            except Exception:
                length = 20000000

            done = 0

            with open(part_fn, "wb") as part_f:

                for data in resp.iter_content(1000000):

                    if self.cancelled:
                        break

                    part_f.write(data)

                    done += len(data)

                    self.progress = min(1.0, 1.0 * done / length)

            resp.close()

            if self.cancelled:
                raise UpdateCancelled()

            # Decompress the file.
            import gzip

            with gzip.open(part_fn, "rb") as gz_f:
                with open(new_fn, "wb") as new_f:

                    while True:
                        data = gz_f.read(1000000)

                        if not data:
                            break

                        new_f.write(data)

            os.unlink(part_fn)

            # Check that the downloaded file has the right digest.
            import hashlib
            with open(new_fn, "rb") as f:
                hash = hashlib.sha256()

                while True:
                    data = f.read(1024 * 1024)

                    if not data:
                        break

                    hash.update(data)

                digest = hash.hexdigest()

            if digest != self.updates[module]["digest"]:
                raise UpdateError(_("The update file does not have the correct digest - it may have been corrupted."))

            if self.cancelled:
                raise UpdateCancelled()



        def unpack(self, module):
            """
            This unpacks the module. Directories are created immediately, while files are
            created as filename.new, and marked to be moved into position when all packing
            is done.
            """

            update_fn = self.update_filename(module, True)

            # First pass, just figure out how many tarinfo objects are in the tarfile.
            tf_len = 0
            with tarfile.open(update_fn, "r") as tf:
                for i in tf:
                    tf_len += 1

            with tarfile.open(update_fn, "r") as tf:
                for i, info in enumerate(tf):

                    self.progress = 1.0 * i / tf_len

                    if info.name == "update":
                        continue

                    # Process the status info for the current module.
                    if info.name == "update/current.json":
                        tff = tf.extractfile(info)
                        state = json.load(tff)
                        tff.close()

                        self.new_state[module] = state[module]

                        continue

                    path = self.path(info.name)

                    # Extract directories.
                    if info.isdir():
                        try:
                            os.makedirs(path)
                        except Exception:
                            pass

                        continue

                    if not info.isreg():
                        raise UpdateError(__("While unpacking {}, unknown type {}.").format(info.name, info.type))

                    # Extract regular files.
                    tff = tf.extractfile(info)
                    new_path = path + ".new"
                    with open(new_path, "wb") as f:
                        while True:
                            data = tff.read(1024 * 1024)
                            if not data:
                                break
                            f.write(data)

                    tff.close()

                    if info.mode & 1:
                        # If the xbit is set in the tar info, set it on disk if we can.
                        try:
                            umask = os.umask(0)
                            os.umask(umask)

                            os.chmod(new_path, 0o777 & (~umask))
                        except Exception:
                            pass

                    self.moves.append(path)

        def move_files(self):
            """
            Move new files into place.
            """

            for path in self.moves:

                self.unlink(path)

                if os.path.exists(path):
                    self.log.write("could not rename file %s" % path)

                    with open(DEFERRED_UPDATE_FILE, "a") as f:
                        f.write("R " + path + "\r\n")

                    continue

                try:
                    os.rename(path + ".new", path)
                except Exception:
                    pass

        def delete_obsolete(self):
            """
            Delete files and directories that have been made obsolete by the upgrade.
            """

            def flatten_path(d, key):
                rv = set()

                for i in d.values():
                    for j in i[key]:
                        rv.add(self.path(j))

                return rv

            old_files = flatten_path(self.current_state, 'files')
            old_directories = flatten_path(self.current_state, 'directories')

            new_files = flatten_path(self.new_state, 'files')
            new_directories = flatten_path(self.new_state, 'directories')

            old_files -= new_files
            old_directories -= new_directories

            old_files = list(old_files)
            old_files.sort()
            old_files.reverse()

            old_directories = list(old_directories)
            old_directories.sort()
            old_directories.reverse()

            for i in old_files:
                self.unlink(i)

                if os.path.exists(i):
                    self.log.write("could not delete file %s" % i)
                    with open(DEFERRED_UPDATE_FILE, "a") as f:
                        f.write("D " + i + "\r\n")

            for i in old_directories:
                try:
                    os.rmdir(i)
                except Exception:
                    pass

        def save_state(self):
            """
            Saves the current state to update/current.json
            """

            fn = os.path.join(self.updatedir, "current.json")

            with open(fn, "w") as f:
                json.dump(self.new_state, f)

        def clean(self, fn):
            """
            Cleans the file named fn from the updates directory.
            """

            fn = os.path.join(self.updatedir, fn)
            if os.path.exists(fn):
                try:
                    os.unlink(fn)
                except Exception:
                    pass

        def clean_old(self):
            for i in self.modules:
                self.clean(i + ".update")

        def clean_new(self):
            for i in self.modules:
                self.clean(i + ".update.new")
                self.clean(i + ".zsync")

    installed_state_cache = None

    def get_installed_state(base=None):
        """
        :undocumented:

        Returns the state of the installed packages.

        `base`
            The base directory to update. Defaults to the current project's
            base directory.
        """

        global installed_state_cache

        if installed_state_cache is not None:
            return installed_state_cache

        if base is None:
            base = config.basedir

        fn = os.path.join(base, "update", "current.json")

        if not os.path.exists(fn):
            return None

        with open(fn, "r") as f:
            state = json.load(f)

        installed_state_cache = state
        return state

    def get_installed_packages(base=None):
        """
        :doc: updater

        Returns a list of installed DLC package names.

        `base`
            The base directory to update. Defaults to the current project's
            base directory.
        """

        state = get_installed_state(base)

        if state is None:
            return [ ]

        rv = list(state.keys())
        return rv


    def can_update(base=None):
        """
        :doc: updater

        Returns true if it's possible that an update can succeed. Returns false
        if updating is totally impossible. (For example, if the update directory
        was deleted.)


        Note that this does not determine if an update is actually available.
        To do that, use :func:`updater.UpdateVersion`.
        """

        # Written this way so we can use this code with 6.18 and earlier.
        if getattr(renpy, "mobile", False):
            return False

        if rsa is None:
            return False

        return not not get_installed_packages(base)


    def update(url, base=None, force=False, public_key=None, simulate=None, add=[], restart=True, confirm=True, patch=True, prefer_rpu=True, allow_empty=False, done_pause=True, allow_cancel=True, screen="updater"):
        """
        :doc: updater

        Updates this Ren'Py game to the latest version.

        `url`
            The URL to the updates.json file.

        `base`
            The base directory that will be updated. Defaults to the base
            of the current game. (This can usually be ignored.)

        `force`
            Force the update to occur even if the version numbers are
            the same. (Used for testing.)

        `public_key`
            The path to a PEM file containing a public key that the
            update signature is checked against. (This can usually be ignored.)

        `simulate`
            This is used to test update guis without actually performing
            an update. This can be:

            * None to perform an update.
            * "available" to test the case where an update is available.
            * "not_available" to test the case where no update is available.
            * "error" to test an update error.

        `add`
            A list of packages to add during this update. This is only necessary
            for dlc.

        `restart`
            If true, the game will be re-run when the update completes. If
            "utter", :func:`renpy.utter_restart` will be called instead. If False,
            the update will simply end.c

        `confirm`
            Should Ren'Py prompt the user to confirm the update? If False, the
            update will proceed without confirmation.

        `patch`
            If true, Ren'Py will attempt to patch the game, downloading only
            changed data. If false, Ren'Py will download a complete copy of
            the game, and update from that. This is set to false automatically
            when the url does not begin with "http:".

            This is ignored if the RPU update format is being used.

        `prefer_rpu`
            If True, Ren'Py will prefer the RPU format for updates, if both
            zsync and RPU are available.

        `allow_empty`
            If True, Ren'Py will allow the update to proceed even if the
            base directory does not contain update information. (`add` must
            be provided in this case.)

        `done_pause`
            If true, the game will pause after the update is complete. If false,
            it will immediately proceed (either to a restart, or a return).

        `allow_cancel`
            If true, the user will be allowed to cancel the update. If false,
            the user will not be allowed to cancel the update.

        `screen`
            The name of the screen to use.
        """

        global installed_packages_cache
        installed_packages_cache = None

        u = Updater(
            url=url,
            base=base,
            force=force,
            public_key=public_key,
            simulate=simulate,
            add=add,
            restart=restart,
            confirm=confirm,
            patch=patch,
            prefer_rpu=prefer_rpu,
            allow_empty=allow_empty,
            done_pause=done_pause,
            allow_cancel=allow_cancel,
        )

        ui.timer(.1, repeat=True, action=u.periodic)

        if not renpy.call_screen(screen, u=u):
            renpy.full_restart()
        else:
            return



    @renpy.pure
    class Update(Action, DictEquality):
        """
        :doc: updater

        An action that calls :func:`updater.update`. All arguments are
        stored and passed to that function.
        """

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            renpy.invoke_in_new_context(update, *self.args, **self.kwargs)


    # A list of URLs that we've checked for the update version.
    checked = set()

    def UpdateVersion(url, check_interval=3600*6, simulate=None, **kwargs):
        """
        :doc: updater

        This function contacts the server at `url`, and determines if there is
        a newer version of software available at that url. If there is, this
        function returns the new version. Otherwise, it returns None.

        Since contacting the server can take some time, this function launches
        a thread in the background, and immediately returns the version from
        the last time the server was contacted, or None if the server has never
        been contacted. The background thread will restart the current interaction
        once the server has been contacted, which will cause screens that call
        this function to update.

        Each url will be contacted at most once per Ren'Py session, and not
        more than once every `check_interval` seconds. When the server is not
        contacted, cached data will be returned.

        Additional keyword arguments (including `simulate`) are passed to the
        update mechanism as if they were given to :func:`updater.update`.
        """

        if not can_update() and not simulate:
            return None

        check = True

        if url in checked:
            check = False

        if time.time() < persistent._update_last_checked.get(url, 0) + check_interval:
            check = False

        if check:
            checked.add(url)
            persistent._update_last_checked[url] = time.time()
            Updater(url, check_only=True, simulate=simulate, **kwargs)

        return persistent._update_version.get(url, None)


    def update_command():
        import time

        ap = renpy.arguments.ArgumentParser()

        ap.add_argument("url")
        ap.add_argument("--base", action='store', help="The base directory of the game to update. Defaults to the current game.")
        ap.add_argument("--force", action="store_true", help="Force the update to run even if the version numbers are the same.")
        ap.add_argument("--key", action="store", help="A file giving the public key to use of the update.")
        ap.add_argument("--simulate", help="The simulation mode to use. One of available, not_available, or error.")

        args = ap.parse_args()

        u = Updater(args.url, args.base, args.force, public_key=args.key, simulate=args.simulate)

        while True:

            state = u.state

            print("State:", state)

            if u.progress:
                print("Progress: {:.1%}".format(u.progress))

            if u.message:
                print("Message:", u.message)

            if state == u.ERROR:
                break
            elif state == u.UPDATE_NOT_AVAILABLE:
                break
            elif state == u.UPDATE_AVAILABLE:
                u.proceed()
            elif state == u.DONE:
                break
            elif state == u.CANCELLED:
                break

            time.sleep(.1)

        return False

    renpy.arguments.register_command("update", update_command)


    # The update object that's being used to update the game.
    downloader = None
    downloader_kwargs = None

    def start_game_download(url, **kwargs):
        """
        :doc: downloader

        Starts downloading the game data from `url`. This begins the process
        of determining what needs to be downloaded, and returns an Update object.
        """

        default_kargs = dict(
            url=url,
            base=renpy.get_alternate_base(config.basedir, True),
            add=["gameonly"],
            prefer_rpu=True,
            restart="utter",
            allow_empty=True,
            allow_cancel=False,
            done_pause=False,
        )

        for k, v in default_kargs.items():
            kwargs.setdefault(k, v)

        global downloader
        global downloader_kwargs

        downloader_kwargs = kwargs
        downloader = Updater(confirm=True, **kwargs)

        return downloader

    def continue_game_download(screen="downloader"):
        """
        :doc: downloader

        Continues downloading the game data. This will loop until the
        download is complete, or the user exits the game.
        """

        global downloader

        # Avoid showing the update_available screen.

        downloader.confirm = False

        while downloader.state == downloader.UPDATE_AVAILABLE:
            renpy.pause(.1)

        # Loop, attempting to download the game until the download
        # completes or the player gives up.

        while True:

            ui.timer(.1, repeat=True, action=downloader.periodic)
            renpy.call_screen(screen, u=downloader)

            downloader = Updater(confirm=False, **downloader_kwargs)


init -1500:

    screen updater(u):

        add "#000"

        frame:
            style_group ""

            has side "t c b":
                spacing gui._scale(10)

            label _("Updater")

            fixed:

                vbox:

                    if u.state == u.ERROR:
                        text _("An error has occured:")
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
                text _("An error occured when trying to download game data:")

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
