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

# This file contains mobile build things that are shared by the android
# and iOS builds.

init -1 python:

    def check_hash_txt(module):
        fn1 = module + "_hash.txt"
        fn2 = renpy.fsencode(os.path.join(config.renpy_base, module, "hash.txt"))

        # No hash file? We're in dev mode - ignore.
        if not renpy.loadable(fn1):
            return True

        hash1 = renpy.open_file(fn1, encoding="utf-8").read()

        if not os.path.exists(fn2):
            return False

        hash2 = open(fn2).read()

        return hash1.strip() == hash2.strip()

    class LaunchEmulator(Action):

        def __init__(self, emulator, variants):
            self.emulator = emulator
            self.variants = variants

        def __call__(self):

            env = {
                "RENPY_EMULATOR" : self.emulator,
                "RENPY_VARIANT" : self.variants,
                }

            p = project.current
            p.launch(env=env)

    class MobileInterface(object):
        """
        This is used to interface between the launcher and RAPT/RENIOS.
        """

        def __init__(self, platform, edit=True, filename=None):
            """
            `platform`
                The name of the platform we're using for. Used for libraries,
                cancel labels, and logfiles.

            `edit`
                If true, we launch the log file in the editor on failure.
            """

            self.platform = platform
            self.edit = edit

            self.process = None

            if filename is None:
                filename = platform + ".txt"

            self.filename = project.current.temp_filename(filename)

            self.info_msg = ""

            with open(self.filename, "w") as f:
                f.write(renpy.version() + "\n")
                pass

        def log(self, msg):
            with open(self.filename, "a") as f:
                f.write("\n")
                f.write(unicode(msg))
                f.write("\n")

        def info(self, prompt):
            self.info_msg = prompt
            interface.processing(prompt, pause=False)
            self.log(prompt)

        def open_directory(self, directory, prompt):
            renpy.run(store.OpenDirectory(directory, absolute=True))
            interface.info(prompt)

        def yesno(self, prompt, submessage=None):
            return interface.yesno(prompt, submessage=submessage)

        def yesno_choice(self, prompt, default=None):
            choices = [ (True, "Yes"), (False, "No") ]
            return interface.choice(prompt, choices, default)

        def terms(self, url, prompt):
            submessage = _("{a=%s}%s{/a}") % (url, url)

            if not interface.yesno(prompt, submessage=submessage):
                self.fail("You must accept the terms and conditions to proceed.", edit=False)


        def input(self, prompt, empty=None):

            if empty is None:
                empty = ''

            while True:
                rv = interface.input(_("QUESTION"), prompt, default=empty, cancel=Jump("android"))

                rv = rv.strip()

                if rv:
                    return rv

        def choice(self, prompt, choices, default):
            return interface.choice(prompt, choices, default, cancel=Jump("android"))

        def fail(self, prompt, edit=True):
            self.log(prompt)
            prompt = re.sub(r'(http://\S+)', r'{a=\1}\1{/a}', prompt)

            # Open android.txt in the editor.
            if edit and self.edit:
                self.open_editor()

            interface.error(prompt, label="android")

        def open_editor(self):
            editor.EditAbsolute(self.filename)()

        def success(self, prompt):
            self.log(prompt)
            interface.info(prompt, pause=False)

        def final_success(self, prompt):
            self.log(prompt)
            interface.info(prompt, label="android")

        def run_yes_thread(self):
            import time

            try:
                while self.run_yes:
                    self.process.stdin.write(b'y\n')
                    self.process.stdin.flush()
                    time.sleep(.2)
            except Exception:
                pass

        def call(self, cmd, cancel=False, use_path=False, yes=False):

            renpy.not_infinite_loop(30)

            cmd = [ renpy.fsencode(i) for i in cmd ]

            self.cmd = cmd

            f = open(self.filename, "a")

            f.write("\n\n\n")

            if cancel:
                cancel_action = self.cancel
            else:
                cancel_action = None

            startupinfo = None
            if renpy.windows:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            self.yes_thread = None

            try:
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action)

                kwargs = { }

                try:
                    self.process = subprocess.Popen(cmd, cwd=renpy.fsencode(RAPT_PATH), stdout=f, stderr=f, stdin=subprocess.PIPE, startupinfo=startupinfo, **kwargs)
                    # avoid SIGTTIN caused by e.g. gradle doing empty read on terminal stdin
                    if not yes:
                        self.process.stdin.close()
                except Exception:
                    import traceback
                    traceback.print_exc(file=f)
                    raise

                if yes:
                    import threading
                    self.run_yes = True
                    self.yes_thread = threading.Thread(target=self.run_yes_thread)
                    self.yes_thread.daemon = True
                    self.yes_thread.start()

                renpy.call_screen("android_process", interface=self)
            finally:
                f.close()
                interface.hide_screen()

                if yes and self.yes_thread:
                    self.run_yes = False
                    self.yes_thread.join()

                    try:
                        self.process.stdin.close()
                    except Exception:
                        pass

                self.process = None
                self.yes_thread = None

        def check_process(self):
            rv = self.process.poll()

            if rv is not None:
                renpy.not_infinite_loop(30)

                if rv:
                    raise subprocess.CalledProcessError(rv, self.cmd)
                else:
                    return True

        def download(self, url, dest):
            try:
                d = Downloader(url, dest)
                cancel_action = [ d.cancel, Jump(self.platform) ]
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action, bar_value=DownloaderValue(d))
                ui.timer(.1, action=d.check, repeat=True)
                ui.interact()
            finally:
                interface.hide_screen()

        def background(self, f):
            try:
                t = threading.Thread(target=f)
                t.start()

                interface.processing(self.info_msg, show_screen=True)

                while t.is_alive():
                    renpy.pause(0)
                    t.join(0.25)

            finally:
                interface.hide_screen()


        def cancel(self):
            if self.process:
                self.process.terminate()

            renpy.jump(self.platform)
