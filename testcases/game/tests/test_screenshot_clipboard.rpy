# Tests for the screenshot key copying the saved screenshot to the clipboard.

# ==============
# == Fixtures ==
# ==============

init python:

    def screenshot_clipboard__patch(copy_fails, environ="1"):
        """
        Saves screenshots to a temporary directory and replaces the clipboard copy with a recording
        stand-in. The real copy must not run here: it would overwrite the developer's clipboard, and
        whether it can fail depends on the platform's clipboard rather than on the test.

        Sets RENPY_SCREENSHOT_CLIPBOARD to `environ`, so the result does not depend on the
        environment the tests were started in.
        """

        import os
        import tempfile

        def fake_copy(filename, absolute_path=False):
            store.screenshot_clipboard__copied.append((filename, absolute_path))

            if copy_fails:
                raise RuntimeError("Simulated clipboard failure.")

        store.screenshot_clipboard__copied = [ ]
        store.screenshot_clipboard__directory = tempfile.mkdtemp()
        store.screenshot_clipboard__real_copy = renpy.put_clipboard_image_file

        renpy.put_clipboard_image_file = fake_copy

        store.screenshot_clipboard__environ = os.environ.get("RENPY_SCREENSHOT_CLIPBOARD")
        os.environ["RENPY_SCREENSHOT_CLIPBOARD"] = environ

        directory = store.screenshot_clipboard__directory.replace("%", "%%")
        store._screenshot_pattern = os.path.join(directory, "screenshot%04d.png")

    def screenshot_clipboard__unpatch():
        """
        Undoes screenshot_clipboard__patch and removes the temporary directory.
        """

        import os
        import shutil

        if store.screenshot_clipboard__environ is None:
            os.environ.pop("RENPY_SCREENSHOT_CLIPBOARD", None)
        else:
            os.environ["RENPY_SCREENSHOT_CLIPBOARD"] = store.screenshot_clipboard__environ

        renpy.put_clipboard_image_file = store.screenshot_clipboard__real_copy
        store._screenshot_pattern = None

        shutil.rmtree(store.screenshot_clipboard__directory, ignore_errors=True)

    def screenshot_clipboard__copied_saved_file():
        """
        Returns True if the copy was attempted exactly once, on a screenshot that exists on disk.
        """

        import os

        if len(store.screenshot_clipboard__copied) != 1:
            return False

        filename, absolute_path = store.screenshot_clipboard__copied[0]

        return absolute_path and os.path.exists(filename)

    def screenshot_clipboard__notify_message():
        """
        Returns the message shown by the notify screen.
        """

        return renpy.get_screen("notify").scope["message"]


# ==============
# === Tests ====
# ==============

testsuite screenshot_clipboard:
    parameter copy_fails = [False, True]

    before testcase:
        $ screenshot_clipboard__patch(copy_fails)

    after testcase:
        $ screenshot_clipboard__unpatch()

    testcase screenshot_key:
        description "The screenshot key saves, copies, and notifies, even when the copy fails."

        keysym "screenshot"
        pause until screen "notify"

        assert eval screenshot_clipboard__copied_saved_file()
        assert eval screenshot_clipboard__notify_message().endswith(" Copied screenshot to clipboard.")


testsuite screenshot_clipboard_disabled:

    before testcase:
        $ screenshot_clipboard__patch(False, environ="0")

    after testcase:
        $ screenshot_clipboard__unpatch()

    testcase screenshot_key:
        description "With RENPY_SCREENSHOT_CLIPBOARD=0, the screenshot key saves without copying (#7539)."

        keysym "screenshot"
        pause until screen "notify"

        assert eval not screenshot_clipboard__copied
        assert eval os.listdir(screenshot_clipboard__directory)
        assert eval not screenshot_clipboard__notify_message().endswith(" Copied screenshot to clipboard.")
