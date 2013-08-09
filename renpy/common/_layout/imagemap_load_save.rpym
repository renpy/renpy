# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('load_save')
    renpy.load_module("_layout/imagemap_common")

    # The ground image.
    config.load_save_ground = { }

    # The idle image.
    config.load_save_idle = { }

    # The hover image.
    config.load_save_hover = { }

    # The selected idle image.
    config.load_save_selected_idle = { }

    # The selected hover image.
    config.load_save_selected_hover = { }

    # The hotspots. Each hotspot is defined by a tuple giving:
    # - The x-coordinate of the left side.
    # - The y-coordinate of the top side.
    # - The x-coordinate of the right side.
    # - The y-coordinate of the bottoms side.
    # - The name of the button or slider this is equivalent to.
    config.load_save_hotspots = { }

    # Define styles
    style.file_picker_text = Style(style.large_button_text, help="text inside a file picker entry")
    style.file_picker_empty_slot = Style(style.file_picker_text, help="text inside an empty file picker entry slot")
    style.file_picker_text_window = Style(style.default, help="a window containing the file picker text.")
    style.file_picker_ss_window = Style(style.default, help="a window containing the screenshot.")

    # Should we disable thumbnails?
    config.disable_thumbnails = False

    # The default thumbnail to use when no file exists.
    config.load_save_empty_thumbnail = None

    # How we format time in a file entry.
    config.time_format = "%b %d, %H:%M"

    # How we format a file entry.
    config.file_entry_format = "%(time)s\n%(save_name)s"

    # True if we should prompt before loading a game.
    _load_prompt = True

    # This is used to store scratch data that's used by the
    # library, but shouldn't be saved out as part of the savegame.
    __scratch = object()
    __scratch.file_picker_page = None
    __scratch.initialized = False
    __scratch.per_page = 0
    __scratch.pages = 0
    __scratch.has_autosave = False
    __scratch.has_quicksave = False

    def _render_savefile(ime, index, name, extra_info, screenshot, mtime, newest, clicked):

        import time

        (x1, y1, x2, y2) = ime.button(
            "slot_%d" % index, clicked, newest,
            keymap={ "save_delete" : ui.returns(("unlink", name)) })

        ui.fixed(xpos=x1, ypos=y1, xmaximum=x2-x1, ymaximum=y2-y1)

        if not config.disable_thumbnails:
            ui.window(style=style.file_picker_ss_window[index])
            ui.add(screenshot)

        s = name + ". " + config.file_entry_format % dict(
            time=time.strftime(config.time_format,
                               time.localtime(mtime)),
            save_name=extra_info)

        ui.window(style=style.file_picker_text_window[index])
        ui.text(s, style=style.file_picker_text[index])

        ui.close()

    def _render_new_slot(ime, index, name, clicked):

        (x1, y1, x2, y2) = ime.button("slot_%d" % index, clicked, False)

        ui.fixed(xpos=x1, ypos=y1, xmaximum=x2-x1, ymaximum=y2-y1)

        if not config.disable_thumbnails:

            if config.load_save_empty_thumbnail:
                ui.window(style=style.file_picker_ss_window[index])
                ui.add(config.load_save_empty_thumbnail)

        ui.window(style=style.file_picker_text_window[index])
        ui.text(name + ". " + _(u"Empty Slot.") + "\n", style=style.file_picker_empty_slot[index])

        ui.close()


    # This function is given a page, and should map it to the names
    # of the files on that page.
    def _file_picker_page_files(page):

        per_page = __scratch.per_page
        rv = [ ]

        if __scratch.has_autosave:
            if page == 0:
                for i in range(1, per_page + 1):
                    rv.append(("auto-" + str(i), _(u"a") + str(i), True))

                return rv
            else:
                page -= 1

        if __scratch.has_quicksave:
            if page == 0:
                for i in range(1, per_page + 1):
                    rv.append(("quick-" + str(i), _(u"q") + str(i), True))

                return rv
            else:
                page -= 1

        for i in range(per_page * page + 1, per_page * page + 1 + per_page):
            rv.append(("%d" % i, "%d" % i, False))

        return rv

    # Given a filename, returns the page that filename is on.
    def _file_picker_file_page(filename):

        per_page = __scratch.per_page

        base = 0

        if __scratch.has_autosave:
            if filename.startswith("auto-"):
                return base
            else:
                base += 1

        if __scratch.has_quicksave:
            if filename.startswith("quick-"):
                return base
            else:
                base += 1

        try:
            return base + int((int(filename) - 1) / per_page)
        except:
            return base

    # Processes a screenshot.
    def _file_picker_process_screenshot(s):
        return s

    # Initialize the scratch information.
    def _file_picker_init():

        hotspots = set()

        if isinstance(config.load_save_hotspots, dict):
            for d in config.load_save_hotspots.values():
                for (x1, y1, x2, y2, name) in d:
                    hotspots.add(name)
        else:
            for (x1, y1, x2, y2, name) in config.load_save_hotspots:
                hotspots.add(name)

        __scratch.has_autosave = ("page_auto" in hotspots)
        __scratch.has_quicksave = ("page_quick" in hotspots)

        __scratch.per_page = 0

        while ("slot_%d" % __scratch.per_page) in hotspots:
            __scratch.per_page += 1

        __scratch.pages = 1

        while ("page_%d" % __scratch.pages) in hotspots:
            __scratch.pages += 1

        __scratch.pages -= 1

    def _file_picker_pages():

        rv = [ ]

        if config.has_autosave:
            rv.append("page_auto")

        if config.has_quicksave:
            rv.append("page_quick")

        for i in range(1, __scratch.pages + 1):
            rv.append("page_%d" % i)

        return rv


    # This displays a file picker that can chose a save file from
    # the list of save files.
    def _file_picker(screen, save):

        if not __scratch.initialized:
            __scratch.initialized = True
            _file_picker_init()

        # The number of slots in a page.
        file_page_length = __scratch.per_page

        update = True

        while True:

            if update:

                update = False

                saved_games = renpy.list_saved_games(regexp=r'(auto-|quick-)?[0-9]+')

                newest = None
                newest_mtime = None
                save_info = { }

                for fn, extra_info, screenshot, mtime in saved_games:
                    screenshot = _file_picker_process_screenshot(screenshot)
                    save_info[fn] = (extra_info, screenshot, mtime)

                    if not fn.startswith("auto-") and mtime > newest_mtime:
                        newest = fn
                        newest_mtime = mtime

                # The index of the first entry in the page.
                fpp = __scratch.file_picker_page

                if fpp is None:

                    if newest:
                        fpp = _file_picker_file_page(newest)
                    else:
                        fpp = _file_picker_file_page("1")


            if fpp < 0:
                fpp = 0

            __scratch.file_picker_page = fpp

            ime = _ImageMapper(
                screen,
                config.load_save_ground,
                config.load_save_idle,
                config.load_save_hover,
                config.load_save_selected_idle,
                config.load_save_selected_hover,
                config.load_save_hotspots,
                variant=screen)


            def tb(enabled, label, clicked, selected):

                if not enabled:
                    return

                ime.button(label, clicked, selected)

            # Previous
            tb(fpp > 0, 'previous', ui.returns(("fppdelta", -1)), selected=False)

            # Quick Access
            for i, name in enumerate(_file_picker_pages()):
                tb(True, name, ui.returns(("fppset", i)), fpp == i)

            # Next
            tb(True, 'next', ui.returns(("fppdelta", +1)), False)

            # This draws a single slot.
            def entry(name, filename, offset, ro):
                clicked = ui.returns(("return", filename))

                if filename not in save_info:
                    if (not save) or ro:
                        clicked = None

                    _render_new_slot(ime, offset, name, clicked)

                else:
                    if save and ro:
                        clicked = None

                    extra_info, screenshot, mtime = save_info[filename]
                    _render_savefile(ime,
                                     offset,
                                     name,
                                     extra_info,
                                     screenshot,
                                     mtime,
                                     newest == filename,
                                     clicked)

            for i, (filename, name, ro) in enumerate(_file_picker_page_files(fpp)):
                entry(name, filename, i, ro)

            ime.close()

            result = ui.interact(mouse="gamemenu")
            type, value = result

            if type == "unlink":
                if layout.yesno_prompt(screen, layout.DELETE_SAVE):
                    renpy.unlink_save(value)
                    update = True

            if type == "return":
                return value

            if type == "fppdelta":
                fpp += value

            if type == "fppset":
                fpp = value


label save_screen:

    python hide:
        while True:
            fn = _file_picker("save", True)

            if renpy.can_load(fn):
                if not layout.yesno_prompt("save", layout.OVERWRITE_SAVE):
                    continue

            renpy.save(fn, extra_info=store.save_name)


label load_screen:

    python hide:
        while True:
            fn = _file_picker("load", False)

            if _load_prompt:
                if not layout.yesno_prompt("load",  layout.LOADING):
                    continue

            renpy.load(fn)
