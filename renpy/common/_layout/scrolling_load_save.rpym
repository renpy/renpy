# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('load_save')

    # Store some global information that won't be saved.
    __session = object()
    __session.scrollbar_position = None

    # Should we prompt to load?
    _load_prompt = True

    # The number of normal save slots.
    config.load_save_slots = 50

    # The number of autosave slots.
    config.load_save_auto_slots = 5

    # The number of quicksave slots.
    config.load_save_quick_slots = 5

    # How we format time in a file entry.
    config.time_format = "%b %d, %H:%M"

    # How we format a file entry.
    config.file_entry_format = "%(time)s\n%(save_name)s"

    # Set the default size of thumbnails.
    config.thumbnail_width = 320
    config.thumbnail_height = 240

    # The default empty slot thumbnail.
    config.load_save_empty_thumbnail = None

    # Styles.
    style.file_picker_frame = Style(style.frame, help="frame containing the file picker")
    style.file_picker_side = Style(style.default, help="ui.side containing the file picker and the scrollbars")
    style.file_picker_viewport = Style(style.viewport, help="viewport containing the file picker entries")
    style.file_picker_box = Style(style.vbox, help="box containing the file picker entries")
    style.file_picker_entry = Style(style.large_button, help="the buttons containing information about each file")
    style.file_picker_text = Style(style.large_button_text, help="the text inside a file picker entry.")
    style.file_picker_scrollbar = Style(style.vscrollbar, help="the text inside a file picker entry.")

    style.thumbnail_frame = Style(style.frame, help="the style of the frame containing a thumbnail")


    # Position things correctly.
    style.file_picker_frame.xmaximum = 0.5
    style.file_picker_frame.xmargin = 6
    style.file_picker_frame.ymargin = 6
    style.file_picker_frame.yfill = True

    style.file_picker_entry.xfill = True
    style.file_picker_entry.yminimum = 58

    style.thumbnail_frame.ymargin = 6
    style.thumbnail_frame.xpos = 0.75
    style.thumbnail_frame.xanchor = 0.5

    def _file_picker_thumbnail(st, at):
        if __session.thumbnail:
            rv = __session.thumbnail
        elif config.load_save_empty_thumbnail:
            rv = config.load_save_empty_thumbnail
        else:
            rv = Null(width=config.thumbnail_width, height=config.thumbnail_height)

        return rv, None


    def _file_picker(screen):

        while True:

            @renpy.curry
            def hovered(thumbnail):
                if __session.thumbnail is not thumbnail:
                    __session.thumbnail = thumbnail
                    renpy.restart_interaction()

            @renpy.curry
            def unhovered(thumbnail):
                if __session.thumbnail is thumbnail:
                    __session.thumbnail = None
                    renpy.restart_interaction()

            __session.thumbnail = None

            layout.navigation(screen)

            newest = None
            newest_time = None

            info = { }

            for name, extra_info, thumbnail, time in renpy.list_saved_games():

                info[name] = (extra_info, thumbnail, time)

                if not name[0] in "0123456789":
                    continue

                if time > newest_time:
                    newest = name
                    newest_time = time

            slots = [ ]

            for i in range(1, config.load_save_slots + 1):
                slots.append((str(i), str(i)))

            if config.has_quicksave:
                for i in range(1, config.load_save_quick_slots + 1):
                    slots.append(('quick-'+ str(i), _(u'q') + str(i)))

            if config.has_autosave:
                for i in range(1, config.load_save_auto_slots + 1):
                    slots.append(('auto-' + str(i), _(u'a') + str(i)))

            ui.frame(style=style.file_picker_frame)
            ui.side(['c', 'r'], style=style.file_picker_side)



            if __session.scrollbar_position is None:
                if newest is None:
                    yoffset = 0
                else:
                    yoffset = 1.0 * (int(newest) - 1) / len(slots)
                value = 0

            else:
                value = __session.scrollbar_position
                yoffset = None

            adj = ui.adjustment(value=value)
            ui.viewport(yadjustment=adj, offsets=(0, yoffset), style=style.file_picker_viewport, mousewheel=True)

            ui.vbox(style=style.file_picker_box, focus=renpy.time.time())


            for i, (fn, n) in enumerate(slots):

                clicked = ui.returns(("select", fn))

                if screen == "save" and fn.startswith("auto-"):
                    clicked = None

                if screen == "load" and fn not in info:
                    clicked = None

                if fn in info:
                    extra_info, thumbnail, time = info[fn]

                    ui.button(style=style.file_picker_entry[i],
                              clicked=clicked,
                              hovered=hovered(thumbnail),
                              unhovered=unhovered(thumbnail),
                              role = "selected_" if (fn == newest) else "",
                              keymap = { "save_delete" : ui.returns(("unlink", fn)) },
                              )

                    s = config.file_entry_format % dict(
                        time=renpy.time.strftime(
                            config.time_format,
                            renpy.time.localtime(time)),
                        save_name=extra_info)

                    ui.text(n + ". " + s, style=style.file_picker_text[i])

                else:
                    ui.button(style=style.file_picker_entry[i],
                              clicked=clicked,
                              role = "selected_" if (fn == newest) else "")

                    ui.text(n + ". " + _(u"Empty Slot."),
                            style=style.file_picker_text[i])

            ui.close() # vbox/viewport

            ui.bar(adjustment=adj, style=style.file_picker_scrollbar)

            ui.close() # side/window

            # Thumbnail.
            ui.frame(style=style.thumbnail_frame)
            ui.add(DynamicDisplayable(_file_picker_thumbnail))

            try:
                action, arg = ui.interact(mouse="gamemenu")
            finally:
                __session.scrollbar_position = adj.value
                __session.thumbnail = None

            if action == "select":
                return arg

            elif action == "unlink":
                if layout.yesno_prompt("save", layout.DELETE_SAVE):
                    renpy.unlink_save(arg)


label save_screen:

    python hide:
        while True:
            fn = _file_picker("save")

            if renpy.can_load(fn):
                if not layout.yesno_prompt("save", layout.OVERWRITE_SAVE):
                    continue

            renpy.save(fn, extra_info=store.save_name)


label load_screen:

    python hide:

        while True:
            fn = _file_picker("load")

            if _load_prompt:
                if not layout.yesno_prompt("load",  layout.LOADING):
                    continue

            renpy.load(fn)
