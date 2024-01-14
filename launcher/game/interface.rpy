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

################################################################################
# Interface actions.
init python in interface:
    from store import OpenURL, config, Return, _preferences, persistent
    import store

    import os.path
    import contextlib

    RENPY_URL = "http://www.renpy.org"
    DOC_PATH = os.path.join(config.renpy_base, "doc/")
    DOC_URL = "http://www.renpy.org/doc/html/"
    DOC_LOCAL_URL = "file:///" + DOC_PATH

    local_doc_exists = os.path.exists(DOC_PATH)

    def get_doc_url(page):
        """
        Returns the URL to the documentation page.
        """

        if local_doc_exists and not persistent.use_web_doc:
            from urllib.parse import urljoin
            from urllib.request import pathname2url

            return urljoin('file:', pathname2url(DOC_PATH + page))
        else:
            return DOC_URL + page

    def OpenDocumentation(page="index.html"):
        """
        An action that opens the documentation.
        """

        return OpenURL(get_doc_url(page))

    def OpenLicense():
        """
        An action that opens the license.
        """

        return OpenDocumentation("license.html")

    def get_sponsor_url():
        """
        Returns the URL to the sponsors page.
        """

        return "https://www.renpy.org/sponsors.html?version={}&language={}".format(
            renpy.version_only,
            _preferences.language or "english"
        )

    # Should we display the bottom links?
    links = True

    @contextlib.contextmanager
    def nolinks():
        global links
        links = False

        try:
            yield
        finally:
            links = True

    # Version.
    import re
    version = re.sub(r'\.\d+(\w*)$', r'\1', renpy.version())

# This displays the bottom of the screen. If the tooltip is not None, this displays the
# tooltip. Otherwise, it displays a list of links (to various websites, and to the
# preferences and update screen), or is just blank.
screen bottom_info:

    zorder 100

    if interface.links:

        frame:
            style_group "l"
            style "l_default"

            left_margin (10 + INDENT)
            right_margin (10 + INDENT)
            xfill True
            ypos 536
            yanchor 0.0

            has vbox:
                spacing 20

            hbox:
                xfill True

                hbox:
                    spacing INDENT
                    textbutton _("Documentation") style "l_link" action interface.OpenDocumentation()
                    textbutton _("Ren'Py Website") style "l_link" action OpenURL(interface.RENPY_URL)
                    textbutton _("[interface.version]") style "l_link" action Jump("about")

                hbox:
                    spacing INDENT
                    xalign 1.0

                    if ability.can_update:
                        textbutton _("update") action Jump("update") style "l_link":
                            if persistent.has_update:
                                text_color "#F96854"
                                text_hover_color Color("#F96854").tint(.8)

                    textbutton _("preferences") style "l_link" action Jump("preferences")
                    textbutton _("quit") style "l_link" action Quit(confirm=False)

            if persistent.sponsor_message:

                textbutton _("Ren'Py Sponsor Information"):
                    style "l_link"
                    text_color "#F96854"
                    text_hover_color Color("#F96854").tint(.8)

                    xalign 0.0
                    yalign 1.0
                    yoffset -10

                    action OpenURL(interface.get_sponsor_url())



screen common:

    default complete = None
    default total = None
    default yes = None
    default no = None
    default choices = None
    default cancel = None
    default bar_value = None

    frame:
        style "l_root"

        frame:
            style_group "l_info"

            has vbox

            text message:
                textalign 0.5
                xalign 0.5
                layout "subtitle"

            if complete is not None:
                add SPACER

                frame:
                    style "l_progress_frame"

                    bar:
                        range total
                        value complete
                        style "l_progress_bar"

            if bar_value is not None:
                add SPACER

                frame:
                    style "l_progress_frame"

                    bar:
                        value bar_value
                        style "l_progress_bar"


            if choices:
                add SPACER

                for v, l in choices:
                    textbutton l:
                        action SetScreenVariable("selected", v)
                        selected_background REVERSE_IDLE
                        selected_hover_background REVERSE_HOVER
                        xpadding 20
                        size_group "choice"
                        text_selected_idle_color REVERSE_TEXT
                        text_selected_hover_color REVERSE_TEXT
                        text_xalign 0.5

                if selected is not None:
                    $ continue_ = Return(selected)
                else:
                    $ continue_ = None

            if submessage:
                add SPACER

                text submessage:
                    textalign 0.5
                    xalign 0.5
                    layout "subtitle"

            if yes:
                add SPACER

                hbox:
                    xalign 0.5
                    textbutton _("Yes") style "l_button" action yes
                    null width 160
                    textbutton _("No") style "l_button" action no


        label title text_color title_color style "l_info_label"

    if back:
        textbutton _("Return") action back style "l_left_button"
    elif cancel:
        textbutton _("Cancel") action cancel style "l_left_button"

    if continue_:
        textbutton _("Continue") action continue_ style "l_right_button"
        key "input_enter" action continue_


screen launcher_input:

    default value = default

    frame:
        style "l_root"

        frame:
            style_group "l_info"

            has vbox

            text message:
                textalign 0.5
                xalign 0.5
                layout "subtitle"

            add SPACER

            input style "l_default":
                value ScreenVariableInputValue("value", returnable=True)
                size 24
                xalign 0.5
                color INPUT_COLOR
                allow allow
                copypaste True

            if filename:
                add SPACER
                text _("Due to package format limitations, non-ASCII file and directory names are not allowed.")

        label title style "l_info_label" text_color QUESTION_COLOR

    if cancel:
        textbutton _("Cancel") action cancel style "l_left_button"

    textbutton _("Continue") action Return(value) style "l_right_button"


init python in interface:

    import traceback
    from store import Jump
    import store._errorhandling as _errorhandling

    def common(title, title_color, message, submessage=None, back=None, continue_=None, pause0=False, show_screen=False, **kwargs):
        """
        Displays the info, interaction, and processing screens.

        `title`
            The title of the screen.

        `message`
            The main message that is displayed when the screen is.

        `submessage`
            If not None, a message that is displayed below the main message.

        `back`
            If not None, a back button will be present. `back` is the action that
            is called when the button is clicked.

        `cancel`
            If not None, a cancel button will be present. `cancel` is the action
            that is called when the button is clicked.

        `continue_`
            If True, a continue button will be present. `continue_` gives the action
            that is called when that button is clicked.

        `pause0`
            If True, a zero-length pause will be inserted before calling the
            screen. This will display it to the user and then immediately
            return.

        `show_screen`
            If True, the screen will be show, and will return immediately. if False,
            the screen will be called, and interaction will pause.

        Other keyword arguments are passed to the screen itself.
        """


        if show_screen:
            screen_func = renpy.show_screen
        else:
            screen_func = renpy.call_screen

            if pause0:
                ui.pausebehavior(0)

        return screen_func("common", title=title, title_color=title_color, message=message, submessage=submessage, back=back, continue_=continue_, **kwargs)

    def hide_screen():
        """
        Hides a screen that was shown with show_screen=True.
        """

        renpy.hide_screen("common")


    def error(message, submessage=None, label="front_page", **kwargs):
        """
        Indicates to the user that an error has occured.

        `message`
            The message to display.

        `submessage`
            Optional secondary message information. For example, this may be
            used to display an exception string.

        `label`
            The label to redirect to when the user finishes displaying the error. None
            to just return False.

        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """

        if label is None:
            action = Return(False)
        else:
            action = Jump(label)

        common(_("ERROR"), store.ERROR_COLOR, message=message, submessage=submessage, back=action, **kwargs)


    store._ignore_action = Jump("front_page")

    _errorhandling.rollback = False
    _errorhandling.ignore = True
    _errorhandling.reload = False
    _errorhandling.console = False

    @contextlib.contextmanager
    def error_handling(what, label="front_page"):
        """
        This is a context manager that catches exceptions and displays them using
        interface.error.

        `what`
            What we're doing when the error occurs. This is usually written using
            the present participle.

        `label`
            The label to jump to when error handling finishes.

        As an example of usage::

            with interface.error_handling(_("opening the log file")):
                f = open("log.txt", "w")
        """

        try:
            yield
        except Exception as e:
            renpy.renpy.error.report_exception(e, editor=False)

            error(_("While [what!qt], an error occured:"),
                _("[exception!q]"),
                what=what,
                label=label,
                exception=traceback.format_exception_only(type(e), e)[-1][:-1])

    import string
    DIGITS_LETTERS = string.digits
    PROJECT_LETTERS = string.digits + string.ascii_letters + " _"
    FILENAME_LETTERS = PROJECT_LETTERS + "\\/"
    TRANSLATE_LETTERS = string.ascii_letters + string.digits + "_"

    def input(title, message, filename=False, sanitize=True, cancel=None, allow=None, default=""):
        """
        Requests typewritten input from the user.
        """

        rv = default

        while True:

            rv = renpy.call_screen(
                "launcher_input",
                title=title,
                message=message,
                filename=filename or (allow in [PROJECT_LETTERS, FILENAME_LETTERS]),
                allow=allow,
                cancel=cancel,
                default=rv
            )

            if sanitize:
                if ("[" in rv) or ("{" in rv):
                    error(_("Text input may not contain the {{ or [[ characters."), label=None)
                    continue

            if filename:
                if filename and (filename != "withslash") and (("\\" in rv) or ("/" in rv)):
                    error(_("File and directory names may not contain / or \\."), label=None)
                    continue

                try:
                    rv.encode("ascii")
                except Exception:
                    error(_("File and directory names must consist of ASCII characters."), label=None)
                    continue

            return rv

    def info(message, submessage=None, pause=True, **kwargs):
        """
        Displays an informational message to the user. The user will be asked to click to
        confirm that he has read the message.

        `message`
            The message to display.

        `pause`
            True if we should pause while showing the info.

        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """

        if pause:
            common(_("INFORMATION"), store.INFO_COLOR, message, submessage, continue_=Return(True), **kwargs)
        else:
            common(_("INFORMATION"), store.INFO_COLOR, message, submessage, pause0=True, **kwargs)


    def interaction(title, message, submessage=None, pause=0, **kwargs):
        """
        Put up on the screen while an interaction with an external program occurs.
        This shows the message, then immediately returns.

        `title`
            The title of the interaction.

        `message`
            The message itself.

        `submessage`
            An optional sub message.

        `pause`
            The amount of time to pause for after showing the message.
        """

        common(title, store.INTERACTION_COLOR, message, submessage=submessage, pause=pause, show_screen=True, **kwargs)
        renpy.pause(pause)

    def processing(message, submessage=None, complete=None, total=None, **kwargs):
        """
        Indicates to the user that processing is taking place. This should be used when
        there is an indefinite amount of work to be done.

        `message`
            The message to display.

        `submessage`
            An additional message to display.

        `complete`
            The fraction complete the step is.

        `total`
            The total amount of work to do in this step.

        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """

        common(_("PROCESSING"), store.INTERACTION_COLOR, message, submessage, pause0=True, complete=complete, total=total, **kwargs)


    def yesno(message, yes=Return(True), no=Return(False), **kwargs):
        """
        Asks the user a yes or no question.

        `message`
            The question to ask.

        `yes`
            The action to perform if the user answers yes.

        `no`
            The action to perform if the user answer no.
        """

        return common(_("QUESTION"), store.QUESTION_COLOR, message, yes=yes, no=no, **kwargs)

    def choice(message, choices, selected, **kwargs):
        """
        Asks the user to pick a choice from a menu.

        `choices`
            A list of (value, label) tuples, giving the choices.

        `selected`
            The default choice that we mark as selected.
        """

        return common(_("CHOICE"), store.QUESTION_COLOR, message, choices=choices, selected=selected, **kwargs)
