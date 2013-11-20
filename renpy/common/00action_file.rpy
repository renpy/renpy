# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:


    ##########################################################################
    # File functions

    config.linear_saves_page_size = None

    if persistent._file_page is None:
        persistent._file_page = "1"

    def __slotname(name, page=None):

        if page is None:
            page = persistent._file_page

        if config.linear_saves_page_size is not None:
            try:
                page = int(page)
                name = int(name)
                return str((page - 1) * config.linear_saves_page_size + name)
            except ValueError:
                pass

        return str(page) + "-" + str(name)

    def __newest_slot():
        """
        Returns the name of the newest slot on a page.
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

    def FileLoadable(name, page=None):
        """
         :doc: file_action_function

         This is a function that returns true
         if the file is loadable, and false otherwise.
         """

        return renpy.can_load(__slotname(name, page))

    def FileScreenshot(name, empty=None, page=None):
        """
         :doc: file_action_function

         Returns the screenshot associated with the given file. If the
         file is not loadable, then `empty` is returned, unless it's None,
         in which case, a Null displayable is created.

         The return value is a displayable.
         """

        screenshot = renpy.slot_screenshot(__slotname(name, page))

        if screenshot is not None:
            return screenshot

        if empty is not None:
            return empty
        else:
            return Null(config.thumbnail_width, config.thumbnail_height)


    def FileTime(name, format=_("%b %d, %H:%M"), empty="", page=None):
        """
         :doc: file_action_function

         Returns the time the file was saved, formatted according
         to the supplied `format`. If the file is not found, `empty` is
         returned.

         The return value is a string.
         """

        mtime = renpy.slot_mtime(__slotname(name, page))

        if mtime is None:
            return empty

        import time

        format = renpy.translation.translate_string(format)
        return time.strftime(format.encode("utf-8"), time.localtime(mtime)).decode("utf-8")

    def FileJson(name, key=None, empty=None, missing=None, page=None):
        """
        :doc: file_action_function

        Accesses the Json information associated with `name`.

        If `key` is None, returns the entire Json other object, or `empty` if the slot
        is empty.

        Otherwise, this returns json[key] if `key` is defined on the json object of the save,
        `missing` if there is a save with the given name, but it does not contain `key`, or
        `empty` if the save slot is empty.
        """

        json = renpy.slot_json(__slotname(name, page))

        if json is None:
            return empty

        if key is None:
            return json

        return json.get(key, missing)


    def FileSaveName(name, empty="", page=None):
        """
         :doc: file_action_function

         Return the save_name that was in effect when the file was saved,
         or `empty` if the file does not exist.
         """

        return FileJson(name, "_save_name", empty=empty, missing=empty, page=page)

    def FileNewest(name, page=None):
        """
        :doc: file_action_function

        Returns True if this is the newest file slot, or False otherwise.
        """

        return __newest_slot() == __slotname(name, page)

    class FileSave(Action):
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
             being shown to the user.
         """

        def __init__(self, name, confirm=True, newest=True, page=None, cycle=False):
            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.cycle = cycle

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page)

            if renpy.scan_saved_game(fn):
                if self.confirm:
                    layout.yesno_screen(layout.OVERWRITE_SAVE, FileSave(self.name, False, False, self.page, cycle=self.cycle))
                    return

            if self.cycle:
                renpy.renpy.loadsave.cycle_saves(self.page + "-", 10)

            renpy.save(fn, extra_info=save_name)

            renpy.restart_interaction()

        def get_sensitive(self):
            if _in_replay:
                return False
            elif renpy.context()._main_menu:
                return False
            elif (self.page or persistent._file_page) == "auto":
                return False
            else:
                return True

        def get_selected(self):
            if not self.confirm:
                return False

            return __newest_slot() == __slotname(self.name, self.page)

    class FileLoad(Action):
        """
         :doc: file_action

         Loads the file.

         `name`
             The name of the slot to load from. If None, an unused slot
             the file will not be loadable.

         `confirm`
             If true, prompt if loading the file will end the game.

         `page`
             The page that the file will be loaded from. If None, the
             current page is used.

         `newest`
             If true, the button is selected if this is the newest file.
         """

        def __init__(self, name, confirm=True, page=None, newest=True):

            if name is None:
                name = __unused_slot_name(page)

            self.name = name
            self.confirm = confirm
            self.page = page
            self.newest = newest

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page)

            if not renpy.context()._main_menu:
                if self.confirm:
                    layout.yesno_screen(layout.LOADING, FileLoad(self.name, False, self.page))
                    return

            renpy.load(fn)

        def get_sensitive(self):
            if _in_replay:
                return False

            return renpy.can_load(__slotname(self.name, self.page))

        def get_selected(self):
            if not self.confirm or not self.newest:
                return False

            return __newest_slot() == __slotname(self.name, self.page)

    class FileDelete(Action):
        """
         :doc: file_action

         Deletes the file.

         `confirm`
             If true, prompts before deleting a file.
         """

        def __init__(self, name, confirm=True, page=None):
            self.name = name
            self.confirm = confirm
            self.page = page

        def __call__(self):

            if not self.get_sensitive():
                return

            fn = __slotname(self.name, self.page)

            if self.confirm:
                layout.yesno_screen(layout.DELETE_SAVE, FileDelete(self.name, False, self.page))
                return

            renpy.unlink_save(fn)

        def get_sensitive(self):
            return renpy.can_load(__slotname(self.name, self.page))

        def get_selected(self):
            return __newest_slot() == __slotname(self.name, self.page)


    def FileAction(name, page=None):
        """
         :doc: file_action

         "Does the right thing" with the file. This means loading it if the
         load screen is showing, and saving to it otherwise.

         `name`
             The name of the slot to save to or load from. If None, an unused slot
             (a large number based on the current time) will be used.

         `page`
             The page that the file will be saved to or loaded from. If None, the
             current page is used.
         """

        if renpy.current_screen().screen_name[0] == "load":
            return FileLoad(name, page=page)
        else:
            return FileSave(name, page=page)


    class FilePage(Action):
        """
         :doc: file_action

         Sets the file page to `page`, which should be one of "auto", "quick",
         or an integer.
         """

        def __init__(self, page):
            self.page = str(page)

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_selected(self):
            return self.page == persistent._file_page

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

    def FileSlotName(slot, slots_per_page, auto="a", quick="q", format="%s%d"):
        """
         :doc: file_action_function

         Returns the name of the numbered slot. This assumes that slots on
         normal pages are numbered in a linear order starting with 1, and
         that page numbers start with 1. When slot is 2, and slots_per_page
         is 10, and the other variables are the defauts:

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


    class FilePageNext(Action):
        """
         :doc: file_action

         Goes to the next file page.

         `max`
             If set, this should be an integer that gives the number of
             the maximum file page we can go to.

         `wrap`
             If true, we can go to the first page when on the last file page if max is set.
         """

        def __init__(self, max=None, wrap=False):

            page = persistent._file_page

            if page == "auto":
                if config.has_quicksave:
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
                            if config.has_autosave:
                                page = "auto"
                            elif config.has_quicksave:
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


    class FilePagePrevious(Action):
        """
         :doc: file_action

         Goes to the previous file page, if possible.

         `max`
             If set, this should be an integer that gives the number of
             the maximum file page we can go to. This is required to enable
             wrap.

         `wrap`
             If true, we can go to the last page when on the first file page if max is set.
         """

        def __init__(self, max=None, wrap=False):

            if wrap and max is not None:
                max = str(max)
            else:
                max = None


            page = persistent._file_page

            if page == "auto":
                page = max

            elif page == "quick":
                if config.has_autosave:
                    page = "auto"
                else:
                    page = max

            elif page == "1":
                if config.has_quicksave:
                    page = "quick"
                elif config.has_autosave:
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

    class FileTakeScreenshot(Action):
        """
         :doc: file_action

         Take a screenshot to be used when the game is saved. This can
         be used to ensure that the screenshot is accurate, by taking
         a pictue of the screen before a file save screen is shown.
         """

        def __call__(self):
            renpy.take_screenshot()

    def QuickSave(message=_("Quick save complete."), newest=False):
        """
        :doc: file_action

        Performs a quick save.

        `message`
            A message to display to the user when the quick save finishes.

        `newest`
            Set to true to mark the quicksave as the newest save.
         """

        return [
            FileTakeScreenshot(),
            FileSave(1, page="quick", confirm=False, cycle=True, newest=newest),
            Notify(message) ]

    def QuickLoad():
        """
        :doc: file_action

        Performs a quick load.
        """

        return FileLoad(1, page="quick", confirm=True, newest=False)
