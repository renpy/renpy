# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This code applies an update.
init -1500 python in updater:
    from store import renpy, config, Action
    import store.build as build

    import tarfile
    import threading
    import traceback
    import os
    import urlparse
    import urllib
    import json
    import subprocess
    import hashlib
    import time
    import sys
    import struct
    import zlib
    import codecs
    import StringIO

    try:
        import rsa
    except:
        rsa = None

    from renpy.exports import fsencode

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

        else:
            raise Exception("Bad command.")

    def process_deferred():
        if not os.path.exists(DEFERRED_UPDATE_FILE):
            return

        # Give a previous process time to quit (and let go of the
        # open files.)
        time.sleep(3)

        try:
            log = file(DEFERRED_UPDATE_LOG, "ab")
        except:
            log = StringIO.StringIO()

        with open(DEFERRED_UPDATE_FILE, "rb") as f:
            for l in f:

                l = l.rstrip("\r\n")
                l = l.decode("utf-8")

                log.write(l.encode("utf-8"))

                try:
                    process_deferred_line(l)
                except:
                    traceback.print_exc(file=log)

        try:
            os.unlink(DEFERRED_UPDATE_FILE)
        except:
            traceback.print_exc(file=log)

        log.close()

    # Process deferred updates on startup, if any exist.
    process_deferred()

    def zsync_path(command):
        """
        Returns the full platform-specific path to command, which is one
        of zsync or zsyncmake.
        """

        if renpy.windows:
            suffix = ".exe"
        else:
            suffix = ""

        return os.path.join(os.path.dirname(sys.executable), command + suffix)


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

        def __init__(self, url, base, force=False, public_key=None, simulate=None, add=[], restart=True):
            """
            Takes the same arguments as update().
            """

            threading.Thread.__init__(self)

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

            # Do we need to restart Ren'Py at the end?
            self.restart = restart

            # Packages to add during the update.
            self.add = add

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

            if public_key is not None:
                f = renpy.file(public_key)
                self.public_key = rsa.PublicKey.load_pkcs1(f.read())
                f.close()
            else:
                self.public_key = None

            # The logfile that update errors are written to.
            try:
                self.log = open(os.path.join(self.updatedir, "log.txt"), "w")
            except:
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
                self.can_cancel = True
                self.can_proceed = False
                self.progress = None
                self.message = None
                self.state = self.CANCELLED

                if self.log:
                    traceback.print_exc(None, self.log)
                    self.log.flush()

            except UpdateError as e:
                self.message = e.message
                self.can_cancel = True
                self.can_proceed = False
                self.state = self.ERROR

                if self.log:
                    traceback.print_exc(None, self.log)
                    self.log.flush()

            except Exception as e:
                self.message = type(e).__name__ + ": " + unicode(e)
                self.can_cancel = True
                self.can_proceed = False
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

            if renpy.android:
                raise UpdateError("The Ren'Py Updater is not supported on Android.")

            self.load_state()
            self.test_write()
            self.check_updates()

            pretty_version = self.check_versions()

            if not self.modules:
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.UPDATE_NOT_AVAILABLE
                return

            if not self.add:

                # Confirm with the user that the update is available.
                with self.condition:
                    self.can_cancel = True
                    self.can_proceed = True
                    self.state = self.UPDATE_AVAILABLE
                    self.version = pretty_version

                    while True:
                        if self.cancelled or self.proceeded:
                            break

                        self.condition.wait()

            if self.cancelled:
                raise UpdateCancelled()

            self.can_cancel = True
            self.can_proceed = False

            # Perform the update.
            self.new_state = dict(self.current_state)

            self.progress = 0.0
            self.state = self.PREPARING

            for i in self.modules:
                self.prepare(i)

            self.progress = 0.0
            self.state = self.DOWNLOADING

            for i in self.modules:
                self.download(i)

            self.clean_old()

            self.can_cancel = False
            self.progress = 0.0
            self.state = self.UNPACKING

            for i in self.modules:
                self.unpack(i)

            self.progress = None
            self.state = self.FINISHING

            self.move_files()
            self.delete_obsolete()
            self.save_state()
            self.clean_new()

            self.message = None
            self.progress = None
            self.can_proceed = True
            self.can_cancel = False

            if self.restart:
                self.state = self.DONE
            else:
                self.state = self.DONE_NO_RESTART

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
                raise UpdateError("An error is being simulated.")

            if self.simulate == "not_available":
                self.can_cancel = False
                self.can_proceed = True
                self.state = self.UPDATE_NOT_AVAILABLE
                return

            # Confirm with the user that the update is available.
            with self.condition:
                self.can_cancel = True
                self.can_proceed = True
                self.state = self.UPDATE_AVAILABLE
                self.version = build.version or build.directory_name

                while True:
                    if self.cancelled or self.proceeded:
                        break

                    self.condition.wait()

            self.can_proceed = False

            if self.cancelled:
                raise UpdateCancelled()

            self.progress = 0.0
            self.state = self.PREPARING

            simulate_progress()

            self.progress = 0.0
            self.state = self.DOWNLOADING

            simulate_progress()

            self.can_cancel = False
            self.progress = 0.0
            self.state = self.UNPACKING

            simulate_progress()

            self.progress = None
            self.state = self.FINISHING

            time.sleep(1.5)

            self.message = None
            self.progress = None
            self.can_proceed = True
            self.can_cancel = False

            if self.restart:
                self.state = self.DONE
            else:
                self.state = self.DONE_NO_RESTART

            return

        def proceed(self):
            """
            Causes the upgraded to proceed with the next step in the process.
            """

            if not self.can_proceed:
                return

            if self.state == self.UPDATE_NOT_AVAILABLE:
                renpy.full_restart()

            elif self.state == self.ERROR:
                renpy.full_restart()

            elif self.state == self.CANCELLED:
                renpy.full_restart()

            elif self.state == self.DONE:
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

            if os.path.exists(path + ".old"):
                os.unlink(path + ".old")

            if os.path.exists(path):

                # This might fail because of a sharing violation on Windows.
                try:
                    os.rename(path, path + ".old")
                    os.unlink(path + ".old")
                except:
                    pass

        def rename(self, old, new):
            """
            Renames the old name to the new name. Tries to enforce the unix semantics, even
            on windows.
            """

            try:
                os.rename(old, new)
                return
            except:
                pass

            try:
                os.unlink(new)
            except:
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

            return os.path.join(self.base, name)

        def load_state(self):
            """
            Loads the current update state from update/current.json
            """

            fn = os.path.join(self.updatedir, "current.json")

            if not os.path.exists(fn):
                raise UpdateError("Either this project does not support updating, or the update status file was deleted.")

            with open(fn, "rb") as f:
                self.current_state = json.load(f)

        def test_write(self):
            fn = os.path.join(self.updatedir, "test.txt")

            try:
                with open(fn, "wb") as f:
                    f.write("Hello, World.")

                os.unlink(fn)
            except:
                raise UpdateError("This account does not have permission to perform an update.")

            if not self.log:
                raise UpdateError("This account does not have permission to write the update log.")

        def check_updates(self):
            """
            Downloads the list of updates from the server, parses it, and stores it in
            self.updates.
            """

            fn = os.path.join(self.updatedir, "updates.json")
            urllib.urlretrieve(self.url, fn)

            with open(fn, "rb") as f:
                updates_json = f.read()
                self.updates = json.loads(updates_json)

            if self.public_key is not None:
                fn = os.path.join(self.updatedir, "updates.json.sig")
                urllib.urlretrieve(self.url + ".sig", fn)

                with open(fn, "rb") as f:
                    signature = f.read().decode("base64")

                try:
                    rsa.verify(updates_json, signature, self.public_key)
                except:
                    raise UpdateError("Could not verify update signature.")

                if "monkeypatch" in self.updates:
                    exec self.updates["monkeypatch"] in globals(), globals()

        def add_dlc_state(self, name):
            url = urlparse.urljoin(self.url, self.updates[name]["json_url"])
            f = urllib.urlopen(url)
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
            for name, data in self.current_state.iteritems():

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

            tf = tarfile.open(self.update_filename(module, False), "w")

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
                    info.mode = 0777
                else:
                    info.mode = 0666

                if info.isreg():
                    with open(path, "rb") as f:
                        tf.addfile(info, f)
                else:
                    tf.addfile(info)

            tf.close()

        def download(self, module):
            """
            Uses zsync to download the module.
            """

            start_progress = None

            new_fn = self.update_filename(module, True)


            # Download the sums file.
            sums = [ ]

            f = urllib.urlopen(urlparse.urljoin(self.url, self.updates[module]["sums_url"]))
            while True:
                data = f.read(4)

                if len(data) != 4:
                    break

                sums.append(struct.unpack("I", data)[0])

            f.close()

            # Figure out the zsync command.

            zsync_fn = os.path.join(self.updatedir, module + ".zsync")

            # May not exist, but if it does, we want to delete it.
            try:
                os.unlink(zsync_fn + ".part")
            except:
                pass

            cmd = [
                zsync_path("zsync"),
                "-o", new_fn,
                "-k", zsync_fn,
                ]

            if os.path.exists(new_fn + ".part"):
                self.rename(new_fn + ".part", new_fn + ".part.old")
                cmd.append("-i")
                cmd.append(new_fn + ".part.old")

            for i in self.modules:
                cmd.append("-i")
                cmd.append(self.update_filename(module, False))

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
                    f = file(new_fn + ".part", "rb")
                except:
                    self.log.write("partfile does not exist\n")
                    continue

                done_sums = 0

                for i in sums:

                    if self.cancelled:
                        break

                    data = f.read(65536)

                    if not data:
                        break

                    if (zlib.adler32(data) & 0xffffffff) == i:
                        done_sums += 1

                f.close()

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
                    raise UpdateError("The update file was not downloaded.")

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
                raise UpdateError("The update file does not have the correct digest - it may have been corrupted.")

            if os.path.exists(new_fn + ".part.old"):
                os.unlink(new_fn + ".part.old")

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
            tf = tarfile.open(update_fn, "r")
            for i in tf:
                tf_len += 1
            tf.close()

            tf = tarfile.open(update_fn, "r")

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
                    except:
                        pass

                    continue

                if not info.isreg():
                    raise UpdateError("While unpacking {}, unknown type {}.".format(info.name, info.type))

                # Extract regular files.
                tff = tf.extractfile(info)
                new_path = path + ".new"
                f = file(new_path, "wb")

                while True:
                    data = tff.read(1024 * 1024)
                    if not data:
                        break
                    f.write(data)

                f.close()
                tff.close()

                if info.mode & 1:
                    # If the xbit is set in the tar info, set it on disk if we can.
                    try:
                        umask = os.umask(0)
                        os.umask(umask)

                        os.chmod(new_path, 0777 & (~umask))
                    except:
                        pass

                self.moves.append(path)

        def move_files(self):
            """
            Move new files into place.
            """

            for path in self.moves:

                self.unlink(path)

                if os.path.exists(path):
                    self.log.write("could not rename file %s" % path.encode("utf-8"))

                    with open(DEFERRED_UPDATE_FILE, "wb") as f:
                        f.write("R " + path.encode("utf-8") + "\n")

                    continue

                os.rename(path + ".new", path)

        def delete_obsolete(self):
            """
            Delete files and directories that have been made obsolete by the upgrade.
            """

            def flatten_path(d, key):
                rv = set()

                for i in d.itervalues():
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
                    self.log.write("could not delete file %s" % path.encode("utf-8"))
                    with open(DEFERRED_UPDATE_FILE, "wb") as f:
                        f.write("D " + i.encode("utf-8") + "\n")

            for i in old_directories:
                try:
                    os.rmdir(i)
                except:
                    pass

        def save_state(self):
            """
            Saves the current state to update/current.json
            """

            fn = os.path.join(self.updatedir, "current.json")

            with open(fn, "wb") as f:
                json.dump(self.new_state, f)

        def clean(self, fn):
            """
            Cleans the file named fn from the updates directory.
            """

            fn = os.path.join(self.updatedir, fn)
            if os.path.exists(fn):
                try:
                    os.unlink(fn)
                except:
                    pass

        def clean_old(self):
            for i in self.modules:
                self.clean(i + ".update")

        def clean_new(self):
            for i in self.modules:
                self.clean(i + ".update.new")
                self.clean(i + ".zsync")

    installed_packages_cache = None

    def get_installed_packages(base=None):
        """
        :doc: updater

        Returns a list of installed DLC package names.

        `base`
            The base directory to update. Defaults to the current project's
            base directory.
        """

        global installed_packages_cache

        if installed_packages_cache is not None:
            return installed_packages_cache

        if base is None:
            base = config.basedir

        fn = os.path.join(base, "update", "current.json")

        if not os.path.exists(fn):
            return [ ]

        with open(fn, "rb") as f:
            state = json.load(f)

        rv = list(state.keys())
        installed_packages_cache = rv
        return rv

    def can_update(base=None):
        """
        :doc: updater

        Returns true if it's possible that an update can succeed. Returns false
        if updating is totally impossible. (For example, if the update directory
        was deleted.)
        """

        if rsa is None:
            return False

        return not not get_installed_packages(base)

    def update(url, base=None, force=False, public_key=None, simulate=None, add=[], restart=True):
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
            Restart the game after the update.
        """

        global installed_packages_cache
        installed_packages_cache = None

        u = Updater(url=url, base=base, force=force, public_key=public_key, simulate=simulate, add=add, restart=restart)
        ui.timer(.1, repeat=True, action=renpy.restart_interaction)
        renpy.call_screen("updater", u=u)

    class Update(Action):
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

            print "State:", state

            if u.progress:
                print "Progress: {:.1f}%".format(u.progress * 100.0)

            if u.message:
                print "Message:", u.message

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

init -1500:
    screen updater:

        add "#000"

        frame:
            style_group ""

            xalign .5
            ypos 100
            xpadding 20
            ypadding 20

            xmaximum 400
            xfill True

            has vbox

            label _("Updater")

            null height 10

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
                null height 10
                text "[u.message!q]"

            if u.progress is not None:
                null height 10
                bar value u.progress range 1.0 style "_bar"

            if u.can_proceed or u.can_cancel:
                null height 10

            if u.can_proceed:
                textbutton _("Proceed") action u.proceed xfill True

            if u.can_cancel:
                textbutton _("Cancel") action u.cancel xfill True
