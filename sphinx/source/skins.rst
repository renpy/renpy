.. _skins:

=====
Skins
=====

Ren'Py supports skinning the launcher - changing what the launcher
looks like. To do this, follow the following steps:

Skins are specific to the Ren'Py version in use, and can't be
expected to be forward or backwards compatible.

1. Open the launcher in the launcher. This can be done from the
   preferences screen.

2. Create the skin.rpy script file.

3. Copy the following into skin.rpy::

    init python:

        # The color of non-interactive text.
        TEXT = "#545454"

        # Colors for buttons in various states.
        IDLE = "#42637b"
        HOVER = "#d86b45"
        DISABLED = "#808080"

        # Colors for reversed text buttons (selected list entries).
        REVERSE_IDLE = "#78a5c5"
        REVERSE_HOVER = "#d86b45"
        REVERSE_TEXT = "#ffffff"

        # Colors for the scrollbar thumb.
        SCROLLBAR_IDLE = "#dfdfdf"
        SCROLLBAR_HOVER = "#d86b45"

        # An image used as a separator pattern.
        PATTERN = "images/pattern.png"

        # A displayable used for the background of everything.
        BACKGROUND = "images/background.png"

        # A displayable used for the background of windows
        # containing commands, preferences, and navigation info.
        WINDOW = Frame("images/window.png", 0, 0, tile=True)

        # A displayable used for the background of the projects list.
        PROJECTS_WINDOW = Null()

        # A displayable used the background of information boxes.
        INFO_WINDOW = "#f9f9f9"

        # Colors for the titles of information boxes.
        ERROR_COLOR = "#d15353"
        INFO_COLOR = "#545454"
        INTERACTION_COLOR = "#d19753"
        QUESTION_COLOR = "#d19753"

        # The color of input text.
        INPUT_COLOR = "#d86b45"

4) Modify skin.rpy to skin the launcher. Place the image files you use
   into the launcher's game directory.

An incorrect skin.rpy file could prevent the launcher from
starting. To fix it, you'll need to remove skin.rpy and skin.rpyc from
the launcher's game directory, start the launcher, and then put them
back.
