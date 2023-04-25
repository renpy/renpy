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

init -1500 python:
    ##########################################################################
    # File contstants.

    _weekday_name_long = [
        _("{#weekday}Monday"),
        _("{#weekday}Tuesday"),
        _("{#weekday}Wednesday"),
        _("{#weekday}Thursday"),
        _("{#weekday}Friday"),
        _("{#weekday}Saturday"),
        _("{#weekday}Sunday"),
    ]


    _weekday_name_short = [
        _("{#weekday_short}Mon"),
        _("{#weekday_short}Tue"),
        _("{#weekday_short}Wed"),
        _("{#weekday_short}Thu"),
        _("{#weekday_short}Fri"),
        _("{#weekday_short}Sat"),
        _("{#weekday_short}Sun"),
    ]

    _month_name_long = [
        _("{#month}January"),
        _("{#month}February"),
        _("{#month}March"),
        _("{#month}April"),
        _("{#month}May"),
        _("{#month}June"),
        _("{#month}July"),
        _("{#month}August"),
        _("{#month}September"),
        _("{#month}October"),
        _("{#month}November"),
        _("{#month}December"),
    ]


    _month_name_short = [
        _("{#month_short}Jan"),
        _("{#month_short}Feb"),
        _("{#month_short}Mar"),
        _("{#month_short}Apr"),
        _("{#month_short}May"),
        _("{#month_short}Jun"),
        _("{#month_short}Jul"),
        _("{#month_short}Aug"),
        _("{#month_short}Sep"),
        _("{#month_short}Oct"),
        _("{#month_short}Nov"),
        _("{#month_short}Dec"),
    ]

    def _strftime(format, t):
        """
        A version of strftime that's meant to work with Ren'Py's translation
        system.
        """

        month = t[1] - 1
        wday = t[6]

        import re
        import time

        rv = [ ]

        for i in re.split(r'(%[-_^#]?[0-9]*[a-zA-Z])', format):

            if i == "%a":
                rv.append(__(_weekday_name_short[wday]))
            elif i == "%A":
                rv.append(__(_weekday_name_long[wday]))
            elif i == "%b":
                rv.append(__(_month_name_short[month]))
            elif i == "%B":
                rv.append(__(_month_name_long[month]))
            elif "%" in i:
                rv.append(time.strftime(i, t))
            else:
                rv.append(i)

        return "".join(rv)


    ##########################################################################
    # File functions

    config.linear_saves_page_size = None
    config.quicksave_slots = 10

    # The number of file pages per folder.
    config.file_pages_per_folder = 100

    if persistent._file_page is None:
        persistent._file_page = "1"

    if persistent._file_folder is None:
        persistent._file_folder = 0

    if persistent._file_page_name is None:
        persistent._file_page_name = { }

    config.file_page_names = [ ]

    config.predict_file_pages = True

    config.file_slotname_callback = None

    def __slotname(name, page=None, slot=False):

        if slot:
            return name

        if page is None:
            page = persistent._file_page

        try:
            page = int(page)
            page = page + persistent._file_folder * config.file_pages_per_folder
        except ValueError:
            pass

        if config.linear_saves_page_size is not None:
            try:
                page = int(page)
                name = int(name)
                return str((page - 1) * config.linear_saves_page_size + name)
            except ValueError:
                pass

        page = str(page)
        name = str(name)

        if config.file_slotname_callback is not None:
            return config.file_slotname_callback(page, name)
        else:
            return page + "-" + name

    def __newest_slot():
        """
        Returns the name of the newest slot.
        """

        return renpy.newest_slot(r'\d+')

    def __unused_slot_name(page):
        """
        Returns an unused name of a slot on the current page. (This will
        likely be a very big number, as it's based on the current unix time.)
        """

        import time

        rv = int(time.time())

        while True:
            if not renpy.can_load(__slotname(str(rv), page)):
                return str(rv)

            rv += 1

    def FileCurrentPage():
        """
        :doc: file_action_function

        Returns the current file page as a string.
        """

        return str(persistent._file_page)

    def FileUsedSlots(page=None, highest_first=True):
        """
        :doc: file_action_function

        Returns a list of used numeric file slots on the page.

        `page`
            The name of the page that will be scanned. If None, the current page
            is used.

        `highest_first`
            If true, the highest-numbered file slot is listed first.
            Otherwise, the lowest-numbered slot is listed first.
        """

        regexp = __slotname(r'\d+', page)

        rv = [ ]

        for fn in renpy.list_slots(regexp=regexp):
            _page, _, slot = fn.partition('-')

            rv.append(int(slot))

        rv.sort()
        if highest_first:
            rv.reverse()

        return rv

    def FileLoadable(name, page=None, slot=False):
        """
        :doc: file_action_function

        This is a function that returns true
        if the file is loadable, and false otherwise.
        """

        return renpy.can_load(__slotname(name, page, slot))

    def FileScreenshot(name, empty=None, page=None, slot=False):
        """
        :doc: file_action_function

        Returns the screenshot associated with the given file. If the
        file is not loadable, then `empty` is returned, unless it's None,
        in which case, a Null displayable is created.

        The return value is a displayable.
        """

        screenshot = renpy.slot_screenshot(__slotname(name, page, slot=slot))

        if screenshot is not None:
            return screenshot

        if empty is not None:
            return empty
        else:
            return Null(config.thumbnail_width, config.thumbnail_height)


    def FileTime(name, format=_("%b %d, %H:%M"), empty="", page=None, slot=False):
        """
        :doc: file_action_function

        Returns the time the file was saved, formatted according
        to the supplied `format`. If the file is not found, `empty` is
        returned.

        The return value is a string.
        """

        mtime = renpy.slot_mtime(__slotname(name, page, slot))

        if mtime is None:
            return empty

        import time

        format = renpy.translation.translate_string(format)
        return _strftime(format, time.localtime(mtime))

    def FileJson(name, key=None, empty=None, missing=None, page=None, slot=False):
        """
        :doc: file_action_function

        Accesses the Json information associated with `name`.

        This always returns `empty` if the slot is empty.

        If not, and if `key` is None, returns the entire dictionary containing the Json data.

        Otherwise, this returns json[key] if `key` is defined on the json object of the save,
        and `missing` if there is a save with the given name, but it does not contain `key`.

        Such Json data is added to a save slot by callbacks registered using
        :var:`config.save_json_callbacks`.
        """

        json = renpy.slot_json(__slotname(name, page, slot))

        if json is None:
            return empty

        if key is None:
            return json

        return json.get(key, missing)


    def FileSaveName(name, empty="", page=None, slot=False):
        """
        :doc: file_action_function

        Return the save_name that was in effect when the file was saved,
        or `empty` if the file does not exist.
        """

        return FileJson(name, "_save_name", empty=empty, missing=empty, page=page, slot=slot)

    def FileNewest(name, page=None, slot=False):
        """
        :doc: file_action_function

        Returns True if this is the newest file slot, or False otherwise.
        """

        return __newest_slot() == __slotname(name, page, slot)

    class FileSave(Action, DictEquality):
        """
        :doc: file_action

        Saves the file.

        The button with this slot is selected if it's marked as the
        newest save file.

        `name`
            The name of the slot to save to. If None, an unused slot
            (a large number based on the current time) will be used.

        `confirm`
            If true, then we will prompt before overwriting a file.

        `newest`
            Ignored.

        `page`
            The name of the page that the slot is on. If None, the current
            page is used.

        `cycle`
            If true, then saves on the supplied page will be cycled before
            being shown to the user. :var:`config.quicksave_slots` slots are
            used in the cycle.

        `slot`
            If True, `name` is taken to be a slot name, and `page` is ignored.

        `action`
            An action that is run after the save is complete. This is only run
            if the save is successful.
        """

        alt = "Save slot [text]"
        slot = None
        action = None

        def __init__(self, name, confirm=True, newest=True, page=None, cycle=False, slot=False, action=None):
            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.cycle = cycle
            self.slot = slot
            self.action = action

            try:
                self.alt = __("Save slot %s: [text]") % (name,)
            except Exception:
                self.alt = "Save slot %s: [text]" % (name,)

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page, self.slot)

            if renpy.scan_saved_game(fn):
                if self.confirm:
                    layout.yesno_screen(layout.OVERWRITE_SAVE, FileSave(self.name, False, False, self.page, cycle=self.cycle, slot=self.slot, action=self.action))
                    return

            if self.cycle:
                renpy.renpy.loadsave.cycle_saves(self.page + "-", config.quicksave_slots)

            renpy.save(fn, extra_info=save_name)

            renpy.restart_interaction()

            return renpy.run(self.action)

        def get_sensitive(self):
            if _in_replay:
                return False
            elif main_menu:
                return False
            elif (self.page or persistent._file_page) == "auto":
                return False
            else:
                return True

        def get_selected(self):
            if not self.confirm:
                return False

            return __newest_slot() == __slotname(self.name, self.page, self.slot)

    class FileLoad(Action, DictEquality):
        """
        :doc: file_action

        Loads the file.

        `name`
            The name of the slot to load from. If None, an unused slot will be
            used, and hence the file will not be loadable.

        `confirm`
            If true and not at the main menu, prompt for confirmation before loading the file.

        `page`
            The page that the file will be loaded from. If None, the
            current page is used.

        `newest`
            If true, the button is selected if this is the newest file.

        `cycle`
            Ignored.

        `slot`
            If True, `name` is taken to be a slot name, and `page` is ignored.
        """

        alt = "Load slot [text]"
        slot = None

        def __init__(self, name, confirm=True, page=None, newest=True, cycle=False, slot=False):

            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.newest = newest
            self.slot = slot

            try:
                self.alt = __("Load slot %s: [text]") % (name,)
            except Exception:
                self.alt = "Load slot %s: [text]" % (name,)

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page, self.slot)

            if not main_menu:
                if self.confirm:
                    if config.autosave_on_quit and not fn.startswith("auto-"):
                        renpy.loadsave.force_autosave()
                    layout.yesno_screen(layout.LOADING, FileLoad(self.name, False, self.page, slot=self.slot))
                    return

            renpy.load(fn)

        def get_sensitive(self):
            if _in_replay:
                return False

            return renpy.can_load(__slotname(self.name, self.page, self.slot))

        def get_selected(self):
            if not self.confirm or not self.newest:
                return False

            return __newest_slot() == __slotname(self.name, self.page, self.slot)

    @renpy.pure
    class FileDelete(Action, DictEquality):
        """
        :doc: file_action

        Deletes the file.

        `name`
            The name of the slot to delete.

        `confirm`
            If true and not at the main menu, prompt for confirmation before loading the file.

        `page`
            The page that the file will be loaded from. If None, the
            current page is used.

        `slot`
            If True, `name` is taken to be a slot name, and `page` is ignored.
        """

        alt = _("Delete slot [text]")
        slot = None

        def __init__(self, name, confirm=True, page=None, slot=False):
            self.name = name
            self.confirm = confirm
            self.page = page
            self.slot = slot

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page, self.slot)

            if self.confirm:
                layout.yesno_screen(layout.DELETE_SAVE, FileDelete(self.name, False, self.page, self.slot))
                return

            renpy.unlink_save(fn)

        def get_sensitive(self):
            return renpy.can_load(__slotname(self.name, self.page, self.slot))


    def FileAction(name, page=None, **kwargs):
        """
        :doc: file_action

        "Does the right thing" with the file. This means loading it if the
        load screen is showing (current screen is named "load"), and saving
        otherwise.

        `name`
            The name of the slot to save to or load from. If None, an unused slot
            (a large number based on the current time) will be used.

        `page`
            The page that the file will be saved to or loaded from. If None, the
            current page is used.

        Other keyword arguments are passed to FileLoad or FileSave.
        """

        if renpy.current_screen().screen_name[0] == "load":
            return FileLoad(name, page=page, **kwargs)
        else:
            return FileSave(name, page=page, **kwargs)

    def _predict_file_page(page):
        """
        Predicts the screenshots on `page`.
        """

        if not config.predict_file_pages:
            return

        if page is None:
            return

        page = unicode(page)

        for i in renpy.list_slots(__slotname(page, r'\d+')):
            renpy.predict(renpy.slot_screenshot(i))

    @renpy.pure
    class FilePage(Action, DictEquality):
        """
        :doc: file_action

        Sets the file page to `page`, which should be one of "auto", "quick",
        or an integer.
        """

        def __init__(self, page):
            self.page = str(page)

            if page == "auto":
                self.alt = _("File page auto")
            elif page == "quick":
                self.alt = _("File page quick")
            else:
                self.alt = _("File page [text]")

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_selected(self):
            return self.page == persistent._file_page

        def predict(self):
            _predict_file_page(self.page)

    def FilePageName(auto="a", quick="q"):
        """
        :doc: file_action_function

        Returns the name of the current file page, as a string. If a normal
        page, this returns the page number. Otherwise, it returns
        `auto` or `quick`.
        """

        page = persistent._file_page

        if page == "quick":
            return quick
        elif page == "auto":
            return auto
        else:
            return page

    @renpy.pure
    class FilePageNameInputValue(InputValue, DictEquality):
        """
        :doc: input_value

        An input value that updates the name of a file page.

        `pattern`
            This is used for the default name of a page. Python-style substition
            is performed, such that {} is replaced with the number of the page.

        `auto`
            The name of the autosave page.

        `quick`
            The name of the quicksave page.

        `page`
            If given, the number of the page to display. This should usually
            be left as None, to give the current page.

        `default`
            If true, this input can be editable by default.
        """

        def __init__(self, pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"), page=None, default=False):

            self.pattern = pattern
            self.auto = auto
            self.quick = quick

            self._page = page

            self.default = default

        def get_page(self):
            if self._page is not None:
                return self._page
            else:
                return persistent._file_page

        @property
        def editable(self):
            page = self.get_page()

            if page == "auto":
                return False
            elif page == "quick":
                return False

            return True

        def get_text(self):
            page = self.get_page()

            if page == "auto":
                return __(self.auto)
            elif page == "quick":
                return __(self.quick)
            else:

                page = int(page)
                default = __(self.pattern).format(page)
                rv = persistent._file_page_name.get(page, default)

                if not rv.strip():

                    current, active = renpy.get_editable_input_value()

                    if not ((current is self) and active):
                        rv = default

                return rv

        def set_text(self, s):

            page = self.get_page()

            if page == "auto" or page =="quick":
                return

            default = __(self.pattern).format(page)

            page = int(page)

            fnp = persistent._file_page_name

            if s == default:
                fnp.pop(page, None)
            else:
                fnp[page] = s

        def enter(self):
            renpy.run(self.Disable())
            raise renpy.IgnoreEvent()


    def FileSlotName(slot, slots_per_page, auto="a", quick="q", format="%s%d"):
        """
        :doc: file_action_function

        Returns the name of the numbered slot. This assumes that slots on
        normal pages are numbered in a linear order starting with 1, and
        that page numbers start with 1. When slot is 2, and slots_per_page
        is 10, and the other variables are the defaults:

        * When the first page is showing, this returns "2".
        * When the second page is showing, this returns "12".
        * When the auto page is showing, this returns "a2".
        * When the quicksave page is showing, this returns "q2".

        `slot`
            The number of the slot to access.

        `slots_per_page`
            The number of slots per page.

        `auto`
            A prefix to use for the auto page.

        `quick`
            A prefix to use for the quick page.

        `format`
            The formatting code to use. This is given two arguments: A string
            giving the page prefix, and an integer giving the slot number.
        """

        page = persistent._file_page

        if page == "quick":
            prefix = quick
            page = 0
        elif page == "auto":
            prefix = auto
            page = 0
        else:
            prefix = ""
            page = int(page) - 1

        return format % (prefix, page * slots_per_page + slot)


    class FilePageNext(Action, DictEquality):
        """
        :doc: file_action

        Goes to the next file page.

        `max`
            If set, this should be an integer that gives the number of
            the maximum file page we can go to.

        `wrap`
            If true, we can go to the first page when on the
            last file page if `max` is set.

        `auto`
            If true and wrap is set, this can bring the player to
            the page of automatic saves.

        `quick`
            If true and wrap is set, this can bring the player to
            the page of automatic saves.
        """

        alt = _("Next file page.")

        def __init__(self, max=None, wrap=False, auto=True, quick=True):

            page = persistent._file_page

            if page == "auto":
                if config.has_quicksave and quick:
                    page = "quick"
                else:
                    page = "1"

            elif page == "quick":
                page = "1"

            else:
                page = int(page) + 1

                if max is not None:
                    if page > max:
                        if wrap:
                            if config.has_autosave and auto:
                                page = "auto"
                            elif config.has_quicksave and quick:
                                page = "quick"
                            else:
                                page = "1"
                        else:
                            page = None

                if page is not None:
                    page = str(page)

            self.page = page

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page is not None

        def predict(self):
            _predict_file_page(self.page)


    class FilePagePrevious(Action, DictEquality):
        """
        :doc: file_action

        Goes to the previous file page, if possible.

        `max`
            If set, this should be an integer that gives the number of
            the maximum file page we can go to. This is required to enable
            wrap.

        `wrap`
            If true, we can go to the last page when on the first file page if max is set.

        `auto`
            If true, this can bring the player to
            the page of automatic saves.

        `quick`
            If true, this can bring the player to
            the page of automatic saves.
        """

        alt = _("Previous file page.")

        def __init__(self, max=None, wrap=False, auto=True, quick=True):

            if wrap and max is not None:
                max = str(max)
            else:
                max = None

            page = persistent._file_page

            if page == "auto":
                page = max

            elif page == "quick":
                if config.has_autosave and auto:
                    page = "auto"
                else:
                    page = max

            elif page == "1":
                if config.has_quicksave and quick:
                    page = "quick"
                elif config.has_autosave and auto:
                    page = "auto"
                else:
                    page = max

            else:
                page = str(int(page) - 1)

            self.page = page

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page

        def predict(self):
            _predict_file_page(self.page)

    @renpy.pure
    class FileTakeScreenshot(Action, DictEquality):
        """
        :doc: file_action

        Take a screenshot to be used when the game is saved. This can
        be used to ensure that the screenshot is accurate, by taking
        a picture of the screen before a file save screen is shown.
        """

        def __call__(self):
            renpy.take_screenshot()
            renpy.restart_interaction()

    @renpy.pure
    def QuickSave(message=_("Quick save complete."), newest=False):
        """
        :doc: file_action

        Performs a quick save.

        `message`
            A message to display to the user when the quick save finishes.

        `newest`
            Set to true to mark the quicksave as the newest save.
         """

        rv = [ FileSave(1, page="quick", confirm=False, cycle=True, newest=newest, action=Notify(message)) ]

        rv[0].alt = _("Quick save.")

        if not getattr(renpy.context(), "_menu", False):
            rv.insert(0, FileTakeScreenshot())

        return rv

    @renpy.pure
    def QuickLoad(confirm=True):
        """
        :doc: file_action

        Performs a quick load.

        `confirm`
            If true and not at the main menu, prompt for confirmation before loading the file.
        """

        rv = FileLoad(1, page="quick", confirm=confirm, newest=False)
        rv.alt = _("Quick load.")
        return rv

init 1050 python hide:

    if config.has_quicksave:
        config.file_page_names.append("quick")
    if config.has_autosave:
        config.file_page_names.append("auto")

    if persistent._file_page not in config.file_page_names:
        try:
            int(persistent._file_page)
        except Exception:
            persistent._file_page = "1"
