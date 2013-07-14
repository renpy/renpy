# This file contains code that helps support the development of Ren'Py
# games.

screen _developer:

    frame:
        style_group ""

        align (.025, .05)

        has vbox

        label "Developer Menu"

        textbutton _(u"Reload Game (Shift+R)"):
            action ui.callsinnewcontext("_save_reload_game")
            size_group "developer"
        textbutton _(u"Variable Viewer"):
            action Jump("_debugger_screen")
            size_group "developer"
        textbutton _(u"Theme Test"):
            action Jump("_theme_test")
            size_group "developer"
        textbutton _(u"Style Hierarchy"):
            action Jump("_style_hierarchy")
            size_group "developer"
        textbutton _(u"Image Location Picker"):
            action Jump("_image_location_picker")
            size_group "developer"
        textbutton _(u"Filename List"):
            action Jump("_filename_list")
            size_group "developer"

        null height 15

        textbutton _(u"Return"):
            action Return()
            size_group "developer"

label _developer_screen:

    call screen _developer

    return

label _debugger_screen:

    python hide:

        ui.window(style=style.gm_root)
        ui.null()

        ui.frame(ymargin=10, xmargin=10, style=style.menu_frame)
        ui.side(['t', 'c', 'r', 'b'])

        layout.label("Variable Viewer", None)

        entries = [ ]

        ebc = store.__dict__.ever_been_changed
        ebc = list(ebc)
        ebc.sort()

        ebc.remove("nvl_list")

        import repr
        aRepr = repr.Repr()
        aRepr.maxstring = 40

        for var in ebc:
            if not hasattr(store, var):
                continue

            if var.startswith("__00"):
                continue

            if var.startswith("_") and not var.startswith("__"):
                continue

            val = aRepr.repr(getattr(store, var))
            s = (var + " = " + val)
            s = s.replace("{", "{{")
            s = s.replace("[", "[[")
            entries.append((0, s))

        if entries:
            vp = ui.viewport(mousewheel=True)
            layout.list(entries)
            ui.bar(adjustment=vp.yadjustment, style='vscrollbar')
        else:
            layout.prompt("No variables have changed since the game started.", None)
            ui.null()

        layout.button(u"Return to the developer menu", None, clicked=ui.returns(True))

        ui.close()

        ui.interact()

    jump _developer_screen

label _theme_test:

    python hide:

        # Never gets pickled
        def role(b):
            if b:
                return "selected_"
            else:
                return ""

        toggle_var = True
        adj = ui.adjustment(100, 25, page=25, adjustable=True)

        while True:

            ui.window(style=style.gm_root)
            ui.null()

            # Buttons
            ui.hbox(box_spacing=10, xpos=10, ypos=10)

            ui.vbox(box_spacing=10)

            sg = "theme_test"

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Button", None)
            ui.textbutton("Button", size_group=sg, clicked=ui.returns("gndn"))
            ui.textbutton("Button (Selected)", size_group=sg, clicked=ui.returns("gndn"), role=role(True))
            ui.textbutton("Small", clicked=ui.returns("gndn"), style='small_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Radio Button", None)
            ui.textbutton("True", size_group=sg, clicked=ui.returns("set"), role=role(toggle_var), style='radio_button')
            ui.textbutton("False", size_group=sg, clicked=ui.returns("unset"), role=role(not toggle_var), style='radio_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Check Button", None)
            ui.textbutton("Check Button", size_group=sg, clicked=ui.returns("toggle"), role=role(toggle_var), style='check_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.vbox(box_spacing=2)
            ui.bar(adjustment=adj, style='bar', xmaximum=200)
            ui.bar(adjustment=adj, style='slider', xmaximum=200)
            ui.bar(adjustment=adj, style='scrollbar', xmaximum=200)
            ui.close()

            ui.close() # vbox

            ui.frame(style='menu_frame')
            ui.hbox(box_spacing=2)
            ui.bar(adjustment=adj, style='vbar', ymaximum=200)
            ui.bar(adjustment=adj, style='vslider', ymaximum=200)
            ui.bar(adjustment=adj, style='vscrollbar', ymaximum=200)
            ui.close()

            ui.frame(style='menu_frame', xmaximum=0.95)
            ui.vbox(box_spacing=20)
            layout.prompt("This is a prompt. We've made this text long enough to wrap around so it fills multiple lines.", None)
            ui.close()

            ui.close() # hbox

            ui.frame(style='menu_frame', xalign=.01, yalign=.99)
            ui.textbutton("Return to the developer menu", clicked=ui.returns("return"))

            rv = ui.interact()
            if rv == "return":
                renpy.jump("_developer_screen")

            elif rv == "set":
                toggle_var = True
            elif rv == "unset":
                toggle_var = False
            elif rv == "toggle":
                toggle_var = not toggle_var

label _style_hierarchy:

    python hide:

        ui.window(style=style.gm_root)
        ui.null()

        ui.frame(ymargin=10, xmargin=10, style=style.menu_frame)
        ui.side(['t', 'c', 'r', 'b'], spacing=2)

        layout.label("Style Hierarchy", None)

        hier = renpy.style.style_hierarchy()

        entries = [ (i[0], i[1] + " - " + str(i[2])) for i in hier if i[2] ]

        vp = ui.viewport(mousewheel=True)
        layout.list(entries)
        ui.bar(adjustment=vp.yadjustment, style='vscrollbar')

        layout.button(u"Return to the developer menu", None, clicked=ui.returns(True))

        ui.close()

        ui.interact()

    jump _developer_screen

init -1050 python:
    config.missing_background = "black"

init 1050 python:

    if config.developer:

        # This is used to indicate that a scene has just occured,
        # and so if the next thing is a missing_show, we should
        # blank the screen.
        __missing_scene = False

        # This returns the __missing dictionary from the current
        # context object.
        def __missing():
            try:
                return renpy.context().__missing
            except AttributeError:
                rv = dict()
                renpy.context().__missing = rv
                return rv

        def __missing_show_callback(name, what, layer):
            if layer != 'master':
                return False

            global __missing_scene
            if __missing_scene:
                renpy.show(name, what=config.missing_background)
            __missing_scene = False

            what = " ".join(what).replace("{", "{{").replace("[", "[[")
            __missing()[name[0]] = what
            return True

        def __missing_hide_callback(name, layer):
            if layer != 'master':
                return False

            global __missing_scene
            __missing_scene = False

            __missing().pop(name[0], None)
            return True

        def __missing_scene_callback(layer):
            if layer != 'master':
                return False

            global __missing_scene
            __missing_scene = True
            __missing().clear()

            return True

        def __missing_overlay():
            missing = __missing()

            if not missing:
                return

            ui.vbox(xalign=0.5, yalign=0.0)
            ui.text(_("Undefined Images"), xalign=0.5)

            for what in sorted(missing.values()):
                ui.text(what, xalign=0.5)

            ui.close()


        config.missing_scene = __missing_scene_callback
        config.missing_show = __missing_show_callback
        config.missing_hide = __missing_hide_callback
        config.overlay_functions.append(__missing_overlay)

init -1050 python:

    class __FPSMeter(object):

        def __init__(self):
            self.last_frames = None
            self.last_time = None

        def __call__(self, st, at):

            if self.last_time is not None:
                frames = config.frames - self.last_frames
                time = st - self.last_time

                text = "FPS: %.1f" % (frames / time)

            else:
                text = "FPS: --.-"

            self.last_frames = config.frames
            self.last_time = st

            return Text(text, xalign=1.0), .5

label _fps_meter:

    python hide:
        def fps_overlay():
            ui.add(DynamicDisplayable(__FPSMeter()))

        # We normally don't want to change this at runtime... but here
        # it's okay, because we don't want to save the FPS meter anyway.
        #
        # Do as I say, not as I do.
        config.overlay_functions.append(fps_overlay)

    return

init python:

    # This is a displayable that can keep track of the mouse coordinates,
    # and show them to the user.
    class __ImageLocationPicker(renpy.Displayable):

        def __init__(self, fn, **kwargs):
            super(__ImageLocationPicker, self).__init__(**kwargs)

            self.child = Image(fn)

            self.mouse = None
            self.point1 = None
            self.point2 = None

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)

            cr = renpy.render(self.child, width, height, st, at)
            rv.blit(cr, (0, 0))

            text = [ ]


            if self.point1 and self.point2 and not self.point1 == self.point2:
                x1, y1 = self.point1
                x2, y2 = self.point2

                x1 = min(x1, cr.width)
                x2 = min(x2, cr.width)
                y1 = min(y1, cr.height)
                y2 = min(y2, cr.height)

                minx = min(x1, x2)
                miny = min(y1, y2)
                maxx = max(x1, x2)
                maxy = max(y1, y2)

                w = maxx - minx
                h = maxy - miny

                if w and h:

                    sr = renpy.render(Solid("#0ff4"), w, h, st, at)
                    rv.blit(sr, (minx, miny))

                    # text.append("Imagemap rectangle: %r" % ((minx, miny, maxx, maxy),))
                    text.append("Rectangle: %r" % ((minx, miny, w, h),))

            if self.mouse:
                mx, my = self.mouse
                if mx < cr.width and my < cr.height:
                    text.append(_("Mouse position: %r") % (self.mouse,))

            text.append(_("Right-click or escape to quit."))

            td = Text("\n".join(text), size=14, color="#fff", outlines=[ (1, "#000", 0, 0 ) ])
            tr = renpy.render(td, width, height, st, at)

            rv.blit(tr, (0, height - tr.height))

            return rv

        def event(self, ev, x, y, st):
            import pygame

            self.mouse = (x, y)
            renpy.redraw(self, 0)

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.point1 = (x, y)
                self.point2 = (x, y)

            elif ev.type == pygame.MOUSEMOTION and ev.buttons[0]:
                self.point2 = (x, y)

            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.point2 = (x, y)


label _image_location_picker:

    scene black

    python hide:

        image_files = [
            fn
            for dir, fn in renpy.loader.listdirfiles()
            if fn.lower().endswith(".jpg") or fn.lower().endswith(".png")
            if not fn[0] == "_"
            ]

        image_files.sort()


        xadjustment = ui.adjustment()
        yadjustment = ui.adjustment()


        while True:

            ui.frame()
            ui.vbox()

            layout.label(u"Image Location Picker", None)

            ui.textbutton(_(u"Done"), clicked=ui.returns(False), size_group="files")

            ui.side(['c', 'b', 'r'], spacing=5)
            vp = ui.viewport(xadjustment=xadjustment, yadjustment=yadjustment, mousewheel=True)

            ui.vbox()

            for fn in image_files:
                ui.button(clicked=ui.returns(fn), size_group="files", xminimum=1.0)
                ui.text(fn.replace("{", "{{").replace("[", "[["), style="button_text", xalign=0.0)

            ui.close()

            ui.bar(adjustment=xadjustment, style='scrollbar')
            ui.bar(adjustment=yadjustment, style='vscrollbar')
            ui.close()

            ui.close()

            rv = ui.interact()

            if rv is False:
                renpy.jump("_developer_screen")

            # Now, allow the user to pick the image.

            ui.keymap(game_menu=ui.returns(True))
            ui.add(__ImageLocationPicker(rv))
            ui.interact()



        # ...

        renpy.jump("_image_location_picker")

label _filename_list:

    python hide:
        import os
        f = file("files.txt", "w")

        for dirname, dirs, files in os.walk(config.gamedir):

            dirs.sort()
            files.sort()

            for fn in files:
                fn = os.path.join(dirname, fn)
                fn = fn[len(config.gamedir) + 1:]
                print >>f, fn.encode("utf-8", "replace")
                print fn.encode("utf-8", "replace")

        f.close()

        renpy.launch_editor(["files.txt"], transient=1)


    jump _developer_screen

# The style inspector.
screen _inspector:
    zorder 1010
    modal True

    frame:
        style_group ""

        xfill True
        yfill True


        has vbox

        label _("Style Inspector")

        null height 20

        if not tree:
            text _("Nothing to inspect.")
        else:
            for depth, width, height, d in tree:
                $ t = ( "  " * depth +
                        u" \u2022 " +
                        d.__class__.__name__ + " : " +
                        "style=%s, " % (__format_style(d.style),) +
                        "size=(%dx%d)" % (width, height) )

                text "[t!q]"

        null height 20

        text _("(Click to continue.)")

    python:
        ui.saybehavior()

init python:
    def _image_load_log_function(st, at):

        ill = list(renpy.get_image_load_log(3))

        if not ill:
            return Null(), .25

        vbox = VBox()

        for when, filename, preload in ill:
            if preload:
                color="#ffffff"
            else:
                color="#ffcccc"

            vbox.add(Text(filename.replace("{", "{{").replace("[", "[["), size=12, color=color, style="_default"))

        rv = Window(vbox, style="_frame", background="#0004", xpadding=5, ypadding=5, xminimum=200)
        return rv, .25

screen _image_load_log:
    zorder 1000

    add DynamicDisplayable(_image_load_log_function)


init python:

    def __format_style(s):

        while s:
            if s.name:
                break

            if s.parent:
                s = style.get(s.parent)
            else:
                break

        return s.name[0] + "".join([ "[%r]" % i for i in s.name[1:] ])

    def __inspect(tree):
        renpy.context_dynamic("_window")
        store._window = False

        renpy.exports.show_screen("_inspector", _transient=True, tree=tree)
        renpy.ui.interact(mouse="screen", type="screen", suppress_overlay=True, suppress_underlay=True)

    config.inspector = __inspect

init python:
    config.underlay.append(im.Tile("_transparent_tile.png"))

