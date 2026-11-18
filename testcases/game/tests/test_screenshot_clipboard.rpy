# Tests for the screenshot key copying the saved screenshot to the clipboard.

# ==============
# == Fixtures ==
# ==============

init python:

    def screenshot_clipboard__patch(copy_fails):
        """
        Saves screenshots to a temporary directory and replaces the clipboard copy with a recording
        stand-in. The real copy must not run here: it would overwrite the developer's clipboard, and
        whether it can fail depends on the platform's clipboard rather than on the test.
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

        directory = store.screenshot_clipboard__directory.replace("%", "%%")
        store._screenshot_pattern = os.path.join(directory, "screenshot%04d.png")

    def screenshot_clipboard__unpatch():
        """
        Undoes screenshot_clipboard__patch and removes the temporary directory.
        """

        import shutil

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
