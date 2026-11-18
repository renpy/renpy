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

# This file isn't part of the launcher. scripts/run_updater_test.py copies it into launcher/game of the copy of
# Ren'Py it's testing, and then runs the updater_test testcase, which updates that copy using the launcher.
#
# The testcase runs twice, since a successful update ends with the launcher restarting itself with the arguments it
# was given. The first run, by the Ren'Py being updated, updates and writes expected.json. The second, by the Ren'Py
# that was installed, finds that file and writes result.json, and then finished.json as it quits. The script compares
# them.

init python:

    # The directory the two runs of the testcase and the script use to communicate. It isn't one of the files the
    # updater knows about, so an update leaves it alone.
    UPDATER_TEST_STATE = os.path.join(config.renpy_base, "updater-test-state")

    def updater_test_path(name):
        """
        Returns the path to the file `name` in the state directory.
        """

        return os.path.join(UPDATER_TEST_STATE, name)

    def updater_test_write(name, data):
        """
        Writes `data` to the file `name` in the state directory, as JSON. The file is renamed into place, so that
        the script never reads part of one.
        """

        import json

        os.makedirs(UPDATER_TEST_STATE, exist_ok=True)

        with open(updater_test_path(name + ".new"), "w") as f:
            json.dump(data, f, indent=2)

        os.replace(updater_test_path(name + ".new"), updater_test_path(name))

    def updater_test_channel():
        """
        Returns the update channel named by RENPY_UPDATER_TEST_CHANNEL, as the launcher was offered it.
        """

        name = os.environ["RENPY_UPDATER_TEST_CHANNEL"]
        channels = fetch_update_channels()

        for channel in channels:
            if channel["channel"] == name:
                return channel

        raise Exception("The launcher wasn't offered the {!r} update channel, only {}.".format(
            name, ", ".join(repr(i["channel"]) for i in channels) or "none"))

    def updater_test_offered():
        """
        Returns the update channel named by RENPY_UPDATER_TEST_CHANNEL, from the channels the screen that's showing
        offers. This is what the launcher will install, which can be newer than what updater_test_channel returned.
        """

        name = os.environ["RENPY_UPDATER_TEST_CHANNEL"]

        for channel in renpy.get_screen("update_channel").scope["channels"]:
            if channel["channel"] == name:
                return channel

        raise Exception("The launcher isn't offering the {!r} update channel.".format(name))

    def updater_test_finished():
        """
        Returns True once the update being shown has been installed, and False while it's in progress. Raises an
        exception if the update ended any other way, so the reason is in the test report.
        """

        screen = renpy.get_screen("updater")

        if screen is None:
            return False

        u = screen.scope["u"]

        if u.state == u.DONE:
            return True

        if u.state in (u.ERROR, u.CANCELLED, u.UPDATE_NOT_AVAILABLE, u.DONE_NO_RESTART):
            raise Exception("The update ended in the {} state: {}".format(u.state, u.message))

        return False

    def updater_test_write_result():
        """
        Records the Ren'Py that's running, and the one the updater says it installed, as result.json.
        """

        import json

        with open(os.path.join(config.renpy_base, "update", "current.json")) as f:
            current = json.load(f)

        updater_test_write("result.json", {
            "version" : renpy.version_only,
            "version_tuple" : list(renpy.version_tuple),
            "installed" : { k : v.get("renpy_version") for k, v in current.items() },
        })

    def updater_test_quit():
        """
        Called when Ren'Py quits. If this is the Ren'Py that was installed, this records that it got as far as
        quitting, and if its tests failed, as finished.json. The script waits for this file, so it's written last.
        """

        import sys

        if not os.path.exists(updater_test_path("result.json")):
            return

        reporter = sys.modules["renpy.test.testreporter"].reporter

        updater_test_write("finished.json", { "failed" : bool(reporter.has_failed) })

    if "RENPY_UPDATER_TEST_CHANNEL" in os.environ:
        config.quit_callbacks.append(updater_test_quit)


testcase updater_test:
    description "Updates Ren'Py using the launcher. This is run by scripts/run_updater_test.py."
    enabled "RENPY_UPDATER_TEST_CHANNEL" in os.environ

    if eval os.path.exists(updater_test_path("expected.json")):

        # This is the Ren'Py that the update installed, started by the launcher that was updated.
        $ updater_test_write_result()

    else:

        $ updater_test_selected = updater_test_channel()

        # The launcher doesn't offer the version that's running, unless it's repairing it.
        if eval (updater_test_selected["split_version"] == list(renpy.version_tuple)):
            $ allow_repair_update = True

        click "update" raw
        pause until screen "update_channel" timeout 60.0

        $ updater_test_selected = updater_test_offered()

        # This is spelled expression rather than text, as the Ren'Py being updated may only know the older word.
        click expression updater_test_selected["channel"]

        # This is the warning to close running games. Like update, this is found by the text in the script, so
        # that it's found whatever language the launcher is in.
        click "Continue" raw

        pause until eval updater_test_finished() timeout float(os.environ.get("RENPY_UPDATER_TEST_TIMEOUT", "900"))

        $ updater_test_write("expected.json", { "channel" : updater_test_selected, "updated_from" : renpy.version_only })

        # This quits, and starts the Ren'Py that was installed.
        click "Proceed" raw
