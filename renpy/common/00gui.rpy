﻿# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

init -1150 python in gui:
    from store import config, layout, _preferences, Frame, Null, persistent, Action, DictEquality
    import math

    config.translate_clean_stores.append("gui")

    config.gui_text_position_properties = True

    _null = Null()

    def init(width, height, fov=75):
        """
        :doc: gui

        Initializes the gui.

        `width`
            The width of the default window.

        `height`
            The height of the default window.

        `fov`
            The field of view of the 3d stage.
        """

        if (not renpy.is_init_phase()) and config.developer:
            raise Exception("gui.init may only be called during the init phase.")

        config.screen_width = width
        config.screen_height = height

        z = (width / 2) / math.tan(math.radians(fov / 2))

        config.perspective = (100.0, z, 100000.0)

        layout.defaults()

        renpy.call_in_new_context("_style_reset")

        # Defer styles until after translation code runs.
        config.defer_styles = True

        size = (width, height)

        if (_preferences.virtual_size is not None) and (_preferences.virtual_size != size):
            _preferences.physical_size = None

        _preferences.virtual_size = size

        from store import build
        build.include_old_themes = False

        if persistent._gui_preference is None:
            persistent._gui_preference = { }

        if persistent._gui_preference_default is None:
            persistent._gui_preference_default = { }

    # A list of variant, function tuples.
    variant_functions = [ ]

    def variant(f, variant=None):
        """
        :doc: gui

        A decorator that causes a function to be called when the gui is first
        initialized, and again each time the gui is rebuilt.  This is intended
        to be used as a function decorator,  of the form::

            @gui.variant
            def small():
                gui.text_size = 30
                # ...

        It can also be called with `f` (a function) and `variant` (a string),
        giving the variant name.
        """

        if variant is None:
            variant = f.__name__

        variant_functions.append((variant, f))

        if renpy.variant(variant):
            f()

        return f

    def rebuild():
        """
        :doc: gui

        Rebuilds the GUI.

        Note: This is a very slow function.
        """

        global variant_functions
        old_variant_functions = variant_functions

        renpy.ast.redefine([ "store.gui" ])

        variant_functions = old_variant_functions

        for variant, f in variant_functions:
            if renpy.variant(variant):
                f()

        for i in config.translate_clean_stores:
            renpy.python.clean_store_backup.backup_one("store." + i)

        # Do the same sort of reset we'd do when changing language, without
        # actually changing the language.
        renpy.change_language(_preferences.language, force=True)

    not_set = object()

    preferences_with_default = set()

    def preference(name, default=not_set):
        """
        :doc: gui_preference
        :args: (name, default=...)

        This function returns the value of the gui preference with
        `name`.

        `default`
            If given, this value becomes the default value of the gui
            preference. The default value must be given the first time
            the preference is used.
        """


        prefs = persistent._gui_preference
        defaults = persistent._gui_preference_default

        if default is not not_set:

            preferences_with_default.add(name)

            if (name not in defaults) or (defaults[name] != default):
                prefs[name] = default
                defaults[name] = default

        else:
            if config.developer and (name not in preferences_with_default):
                raise Exception("Gui preference %r is not set, and does not have a default value." % name)

        return prefs[name]


    class SetPreference(Action, DictEquality):
        """
        :doc: gui_preference

        This Action sets the gui preference with `name` to `value`.

        `rebuild`
            If true, the default, :func:`gui.rebuild` is called to make
            the changes take effect. This should generally be true, except
            in the case of multiple gui.SetPreference actions, in which case
            it should be False in all but the last one.

        This is a very slow action, and probably not suitable for use
        when a button is hovered.
        """

        def __init__(self, name, value, rebuild=True):
            self.name = name
            self.value = value
            self.rebuild = rebuild

        def __call__(self):
            prefs = persistent._gui_preference

            prefs[self.name] = self.value

            if self.rebuild:
                rebuild()

        def get_selected(self):
            prefs = persistent._gui_preference
            return prefs.get(self.name, not_set) == self.value


    class TogglePreference(Action, DictEquality):
        """
        :doc: gui_preference

        This Action toggles the gui preference with `name` between
        value `a` and value `b`. It is selected if the value is equal
        to `a`.

        `rebuild`
            If true, the default, :func:`gui.rebuild` is called to make
            the changes take effect. This should generally be true, except
            in the case of multiple gui.SetPreference actions, in which case
            it should be False in all but the last one.

        This is a very slow action, and probably not suitable for use
        when a button is hovered.
        """

        def __init__(self, name, a, b, rebuild=True):
            self.name = name
            self.a = a
            self.b = b
            self.rebuild = rebuild

        def __call__(self):
            prefs = persistent._gui_preference

            if prefs[self.name] == self.a:
                prefs[self.name] = self.b
            else:
                prefs[self.name] = self.a

            if self.rebuild:
                rebuild()

        def get_selected(self):
            prefs = persistent._gui_preference
            return prefs.get(self.name, not_set) == self.a



    renpy.pure("gui.preference")
    renpy.pure("gui.SetPreference")
    renpy.pure("gui.TogglePreference")

    # The extension used for auto-defined images.
    button_image_extension = ".png"

    def button_properties(kind):
        """
        :doc: gui

        Given a `kind` of button, returns a dictionary giving standard style
        properties for that button. This sets:

        :propref:`background`
            As described below.

        :propref:`padding`
            To gui.kind_borders.padding (if it exists).

        :propref:`xsize`
            To gui.kind_width (if it exists).

        :propref:`ysize`
            To gui.kind_height (if it exists).

        (Note that if `kind` is the string "nvl_button", this will look for
        the gui.nvl_button_background variable.)

        The background is a frame that takes its background picture from
        the first existing one of:

        * gui/button/kind_[prefix\_].background.png
        * gui/button/[prefix\_].background.png

        If a gui variables named gui.kind_borders exists, it's
        used. Otherwise, :var:`gui.button_borders` is used. If gui.kind_tile
        exists, it determines if the borders are tiled, else :var:`gui.button_tile`
        controls tiling.

        For what [prefix\_] means, check out the :ref:`style prefix search <style-prefix-search>`
        documentation.
        """

        g = globals()

        def get(prop):
            if kind + "_" + prop in g:
                return g[kind + "_" + prop]

            return None

        borders = get("borders")

        tile = get("tile")
        if tile is None:
            tile = button_tile

        backgrounds = [ ]

        if kind != "button":
            backgrounds.append("gui/button/" + kind[:-7] + "_[prefix_]background" + button_image_extension)

        backgrounds.append("gui/button/[prefix_]background" + button_image_extension)

        if renpy.variant("small"):
            backgrounds = [ i.replace("gui/button", "gui/phone/button") for i in backgrounds ] + backgrounds

        rv = {
            "background" : Frame(backgrounds, borders or button_borders, tile=tile),
        }

        if borders is not None:
            rv["padding"] = borders.padding

        width = get("width")
        height = get("height")

        if width is not None:
            rv["xsize"] = width

        if height is not None:
            rv["ysize"] = height

        return rv


    def text_properties(kind=None, accent=False):
        """
        :name: gui.text_properties
        :doc: gui

        Given a `kind` of button, returns a dictionary giving standard style
        properties for that button. This sets:

        :propref:`font`
            To gui.kind_text_font, if it exists.

        :propref:`size`
            To gui.kind_text_size, if it exists.

        :propref:`xalign`
            To gui.kind_text_xalign, if it exists.

        :propref:`textalign`
            To gui.kind_text_xalign, if it exists.

        :propref:`layout`
            To "subtitle" if gui.kind_text_xalign is greater than zero
            and less than one.

        There are also a number of variables that set the text
        :propref:`color` style property:

        color
            To gui.kind_text_color, if it exists. If the variable is not
            set, and `accent` is True, sets the text color to the default
            accent color.

        insensitive_color
            To gui.kind_text_insensitive_color, if it exists.

        idle_color
            To gui.kind_text_idle_color, if it exists.

        hover_color
            To gui.kind_text_hover_color, if it exists.

        selected_color
            To gui.kind_text_selected_color, if it exists.

        All other :ref:`text style properties <text-style-properties>`
        are available. When `kind` is not None,
        :ref:`position style properties <position-style-properties>`
        are also available. For
        example, gui.kind_text_outlines sets the outlines style property,
        gui.kind_text_kerning sets kerning, and so on.
        """

        g = globals()

        def get(prop):

            if kind is not None:
                name = kind + "_" + prop
            else:
                name = prop

            if name in g:
                return g[name]

            return None

        rv = { }

        if accent and (accent_color is not None):
            rv["color"] = accent_color


        if kind is not None:

            xalign = get("text_xalign")

            if xalign is not None:
                rv["xalign"] = xalign
                rv["text_align"] = xalign
                rv["textalign"] = xalign

                if (xalign > 0) and (xalign < 1):
                    rv["layout"] = "subtitle"

        if (kind is not None) and config.gui_text_position_properties:
            property_names = renpy.sl2.slproperties.text_property_names + renpy.sl2.slproperties.position_property_names
        else:
            property_names = renpy.sl2.slproperties.text_property_names

        for prefix in renpy.sl2.slparser.STYLE_PREFIXES:
            for property in property_names:

                prop = prefix + property

                text_prop = "text_" + prop

                v = get(text_prop)

                if v is not None:
                    rv[prop] = v

        return rv

    button_text_properties = text_properties


    ############################################################################
    # Strings used by the confirm screen.

    ARE_YOU_SURE = _("Are you sure?")
    DELETE_SAVE = _("Are you sure you want to delete this save?")
    OVERWRITE_SAVE = _("Are you sure you want to overwrite your save?")
    LOADING = _("Loading will lose unsaved progress.\nAre you sure you want to do this?")
    QUIT = _("Are you sure you want to quit?")
    MAIN_MENU = _("Are you sure you want to return to the main menu?\nThis will lose unsaved progress.")
    END_REPLAY = _("Are you sure you want to end the replay?")
    SLOW_SKIP = _("Are you sure you want to begin skipping?")
    FAST_SKIP_SEEN = _("Are you sure you want to skip to the next choice?")
    FAST_SKIP_UNSEEN = _("Are you sure you want to skip unseen dialogue to the next choice?")
    UNKNOWN_TOKEN = _("This save was created on a different device. Maliciously constructed save files can harm your computer. Do you trust this save's creator and everyone who could have changed the file?")
    TRUST_TOKEN = _("Do you trust the device the save was created on? You should only choose yes if you are the device's sole user.")

    ############################################################################
    # Image generation. This lives here since it wants to read data from
    # the gui variables.

    # Should we skip backups?
    _skip_backup = False

    def _gui_images():

        import store.gui as gui
        from store import config, Color

        import pygame_sdl2
        import os

        if not config.developer:
            return

        phone = renpy.variant("small")

        class Image(object):

            def __init__(self, dn, fn, width, height):
                self.s = pygame_sdl2.Surface((width, height), pygame_sdl2.SRCALPHA)


                if phone:
                    self.fn = os.path.join(config.gamedir, "gui", "phone", dn, fn + ".png")
                else:
                    self.fn = os.path.join(config.gamedir, "gui", dn, fn + ".png")

                self.width = width
                self.height = height

            def save(self):
                s = self.s
                fn = self.fn

                dn = os.path.dirname(fn)

                try:
                    os.makedirs(dn, 0o777)
                except Exception:
                    pass

                if os.path.exists(fn):

                    index = 1

                    while True:
                        bfn = "{}.{}.bak".format(fn, index)

                        if not os.path.exists(bfn):
                            break

                        index += 1

                    if not gui._skip_backup:
                        os.rename(fn, bfn)

                pygame_sdl2.image.save(s, fn, 3)

            def fill(self, color=None):
                if color is None:
                    color = gui.accent_color

                color = tuple(Color(color))

                self.s.fill(color)
                return self

            def fill_rect(self, rect, color=None):

                if color is None:
                    color = gui.accent_color

                color = tuple(Color(color))

                ss = self.s.subsurface(rect)
                ss.fill(color)

                return self

            def fill_left(self, width, color=None):
                self.fill_rect((0, 0, width, self.height))
                return self

        def scale(fixed, scaled):

            if fixed is not None:
                return fixed

            factor = 1.0 * config.screen_height / 720
            return int(scaled * factor)


        # Buttons
        width = scale(gui.button_width, 300)

        if phone:
            height = scale(gui.button_height, 43)
        else:
            height = scale(gui.button_height, 33)

        check_width = gui.check_button_borders.padding[0]
        check_margin = scale(None, 3)
        check_rect = (
            check_margin,
            gui.check_button_borders.padding[1],
            min(check_width - check_margin, scale(None, 5)),
            height - gui.check_button_borders.padding[1] - gui.check_button_borders.padding[3],
            )

        radio_width = gui.radio_button_borders.padding[0]
        radio_margin = scale(None, 3)

        radio_rect = (
            radio_margin,
            gui.radio_button_borders.padding[1],
            min(radio_width - radio_margin, scale(None, 5)),
            height - gui.radio_button_borders.padding[1] - gui.radio_button_borders.padding[3],
            )

        Image("button", "idle_background", width, height).save()
        Image("button", "hover_background", width, height).save()

        Image("button", "check_selected_foreground", check_width, height).fill_rect(check_rect).save()
        Image("button", "check_foreground", check_width, height).save()

        Image("button", "radio_selected_foreground", radio_width, height).fill_rect(radio_rect).save()
        Image("button", "radio_foreground", radio_width, height).save()


        # Bars.
        long_size = scale(None, 350)

        Image("bar", "left", long_size, gui.bar_size).fill(gui.hover_color).save()
        Image("bar", "right", long_size, gui.bar_size).fill(gui.muted_color).save()
        Image("bar", "bottom", gui.bar_size, long_size).fill(gui.hover_color).save()
        Image("bar", "top", gui.bar_size, long_size).fill(gui.muted_color).save()

        if phone:
            thumb_size = scale(None, 15)
        else:
            thumb_size = scale(None, 10)

        Image("slider", "horizontal_idle_bar", long_size, gui.slider_size).fill(gui.muted_color).save()
        Image("slider", "horizontal_idle_thumb", thumb_size, gui.slider_size).fill(gui.accent_color).save()
        Image("slider", "horizontal_hover_bar", long_size, gui.slider_size).fill(gui.hover_muted_color).save()
        Image("slider", "horizontal_hover_thumb", thumb_size, gui.slider_size).fill(gui.hover_color).save()

        Image("slider", "vertical_idle_bar", gui.slider_size, long_size).fill(gui.muted_color).save()
        Image("slider", "vertical_idle_thumb", gui.slider_size, thumb_size).fill(gui.accent_color).save()
        Image("slider", "vertical_hover_bar", gui.slider_size, long_size).fill(gui.hover_muted_color).save()
        Image("slider", "vertical_hover_thumb", gui.slider_size, thumb_size).fill(gui.hover_color).save()


        long_size = scale(None, 700)

        Image("scrollbar", "horizontal_idle_bar", long_size, gui.scrollbar_size).fill(gui.muted_color).save()
        Image("scrollbar", "horizontal_idle_thumb", long_size, gui.scrollbar_size).fill(gui.accent_color).save()
        Image("scrollbar", "horizontal_hover_bar", long_size, gui.scrollbar_size).fill(gui.hover_muted_color).save()
        Image("scrollbar", "horizontal_hover_thumb", long_size, gui.scrollbar_size).fill(gui.hover_color).save()

        Image("scrollbar", "vertical_idle_bar", gui.scrollbar_size, long_size).fill(gui.muted_color).save()
        Image("scrollbar", "vertical_idle_thumb", gui.scrollbar_size, long_size).fill(gui.accent_color).save()
        Image("scrollbar", "vertical_hover_bar", gui.scrollbar_size, long_size).fill(gui.hover_muted_color).save()
        Image("scrollbar", "vertical_hover_thumb", gui.scrollbar_size, long_size).fill(gui.hover_color).save()

        sbp = gui.slot_button_borders.padding
        tnx = (gui.slot_button_width - config.thumbnail_width) // 2
        bar_width = scale(None, 5)

        s = Image("button", "slot_idle_background", gui.slot_button_width, gui.slot_button_height)
        s.fill_rect((tnx, sbp[1], config.thumbnail_width, config.thumbnail_height), gui.muted_color)
        s.save()

        s = Image("button", "slot_hover_background", gui.slot_button_width, gui.slot_button_height)
        s.fill_rect((tnx, sbp[1], config.thumbnail_width, config.thumbnail_height), gui.hover_muted_color)
        s.fill_rect((0, sbp[1], bar_width, config.thumbnail_height))

        s.save()


        return False

    renpy.arguments.register_command("gui_images", _gui_images)
