# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

import pygame_sdl2
import os

from renpy.store import config

class ImageGenerator(object):

    def __init__(self, parameters):

        pygame_sdl2.image.init()

        self.p = p = parameters

        self.width = p.width
        self.height = p.height

        self.scale = p.scale

        self.accent_color = p.accent_color
        self.boring_color = p.boring_color

        self.hover_color = p.hover_color
        self.muted_color = p.muted_color
        self.hover_muted_color = p.hover_muted_color

        self.menu_color = p.menu_color

        self.prefix = os.path.join(p.prefix, "gui", "")

        try:
            os.mkdir(self.prefix, 0o777)
        except:
            pass

        self.full_width = self.width / self.scale
        self.full_height = self.height / self.scale

        self.overwrite = p.replace_images

    def scale_int(self, n):
        rv = int(n * self.scale)

        if rv < 1:
            rv = 1

        return rv

    def rescale_template(self, t):

        rv = [ ]

        for pos, opacity in t:
            rv.append((pos * self.scale, opacity))

        return rv

    def generate_line(self, template):

        size = int(max(i[0] for i in template))

        rv = [ ]

        right_pos, right_value = template[0]

        for i in range(size):

            if i == right_pos:
                rv.append(right_value)
                continue

            while i >= right_pos:
                left_pos = right_pos
                left_value = right_value

                right_pos, right_value = template.pop(0)

            done = 1.0 * (i - left_pos) / (right_pos - left_pos)
            rv.append(left_value + done * (right_value - left_value))

        return rv

    def crop_line(self, line, size):
        """
        Crops the center `size` pixels out of `line`.
        """

        if len(line) <= size:
            return line

        start = (len(line) - size) // 2

        return line[start:start + size ]

    def save(self, s, filename, overwrite=True):

        fn = self.prefix + filename + ".png"
        dn = os.path.dirname(fn)

        try:
            os.makedirs(dn, 0o777)
        except:
            pass

        if os.path.exists(fn):

            if not overwrite:
                return

            if not self.overwrite:
                return

            index = 1

            while True:
                bfn = "{}.{}.bak".format(fn, index)

                if not os.path.exists(bfn):
                    break

                index += 1

            if not self.p.skip_backup:
                os.rename(fn, bfn)

        pygame_sdl2.image.save(s, fn)

    def make_surface(self, width, height):
        return pygame_sdl2.Surface((width, height), pygame_sdl2.SRCALPHA)

    def generate_image(self, filename, xtmpl, ytmpl, color=(0, 0, 0, 255)):

        r, g, b, a = color

        xtmpl = self.rescale_template(xtmpl)
        ytmpl = self.rescale_template(ytmpl)

        xline = self.generate_line(xtmpl)
        yline = self.generate_line(ytmpl)

        xline = self.crop_line(xline, self.width)
        yline = self.crop_line(yline, self.height)

        s = self.make_surface(len(xline), len(yline))

        for x, xv in enumerate(xline):
            for y, yv in enumerate(yline):
                v = xv * yv
                s.set_at((x, y), (r, g, b, int(a * v)))

        self.save(s, filename)

    def generate_textbox(self):

        XSIZE = self.full_width
        XINSIDE = (XSIZE - 744) // 2

        YSIZE = 185
        YBORDER = 5

        X = [
            (0, 0.0),
            (XINSIDE, 1.0),
            (XSIZE - XINSIDE, 1.0),
            (XSIZE, 0.0),
            ]

        Y = [
            (0, 0.0),
            (YBORDER, 1.0),
            (YSIZE, 1.0),
            ]

        self.generate_image("textbox", X, Y, self.boring_color.opacity(.8))


        YSIZE = 240
        YBORDER = 5

        X = [ (0, 1.0), (self.full_width, 1.0) ]

        Y = [
            (0, 0.0),
            (YBORDER, 1.0),
            (YSIZE, 1.0),
            ]

        self.generate_image("phone/textbox", X, Y, self.boring_color.opacity(.8))

    def generate_nvl(self):
        XSIZE = self.full_width
        XINSIDE = (XSIZE - 800) // 2

        YSIZE = self.full_height

        X = [
            (0, 0.0),
            (XINSIDE, 1.0),
            (XSIZE - XINSIDE, 1.0),
            (XSIZE, 0.0),
            ]

        Y = [
            (0, 1.0),
            (YSIZE, 1.0),
            ]


        self.generate_image("nvl", X, Y, self.boring_color.opacity(.8))

        X = [
            (0, 1.0),
            (XSIZE, 1.0),
            ]

        Y = [
            (0, 1.0),
            (YSIZE, 1.0),
            ]

        self.generate_image("phone/nvl", X, Y, self.boring_color.opacity(.8))



    def generate_choice_button(self):
        XSIZE = 790
        XINSIDE = 100

        YSIZE = 30
        YBORDER = 3

        X = [
            (0, 0.0),
            (XINSIDE, 1.0),
            (XSIZE - XINSIDE, 1.0),
            (XSIZE, 0.0),
            ]

        Y = [
            (0, 0.0),
            (YBORDER, 1.0),
            (YSIZE - YBORDER, 1.0),
            (YSIZE, 0.0),
            ]

        self.generate_image("choice/idle_background", X, Y, self.boring_color.opacity(.8))
        self.generate_image("choice/hover_background", X, Y, self.accent_color.opacity(.95))

    def generate_overlay(self):

        width = self.scale_int(280)
        phone_width = self.scale_int(340)

        game_y = self.scale_int(120)
        game_height = self.scale_int(570)

        line_width = self.scale_int(3)

        # Main menu.
        mm = self.make_surface(self.width, self.height)
        mm.subsurface((0, 0, width, self.height)).fill(self.boring_color.opacity(.8))
        mm.subsurface((width - line_width, 0, line_width, self.height)).fill(self.accent_color)
        self.save(mm, "overlay/main")

        mm = self.make_surface(self.width, self.height)
        mm.subsurface((0, 0, phone_width, self.height)).fill(self.boring_color.opacity(.8))
        mm.subsurface((phone_width - line_width, 0, line_width, self.height)).fill(self.accent_color)
        self.save(mm, "phone/overlay/main")

        # Game menu.
        gm = self.make_surface(self.width, self.height)
        gm.fill(self.boring_color.opacity(.8))
        gm.subsurface((width - line_width, game_y, line_width, game_height)).fill(self.accent_color)
        self.save(gm, "overlay/game")

        gm = self.make_surface(self.width, self.height)
        gm.fill(self.boring_color.opacity(.8))
        gm.subsurface((phone_width - line_width, game_y, line_width, game_height)).fill(self.accent_color)
        self.save(gm, "phone/overlay/game")

        # Confirm.
        gm = self.make_surface(self.width, self.height)
        gm.fill(self.boring_color.opacity(.6))
        self.save(gm, "overlay/confirm")

    def generate_file_slot(self):

        width = self.scale_int(276)
        height = self.scale_int(216)

        bar_width = self.scale_int(6)
        shot_width = self.scale_int(256)
        shot_offset = self.scale_int(10)

        top_y = self.scale_int(10)
        top_height = self.scale_int(144)

        s = self.make_surface(width, height)
        # s.subsurface((0, top_y, bar_width, top_height)).fill(self.accent_color)
        s.subsurface((shot_offset, top_y, shot_width, top_height)).fill(self.accent_color.shade(.33))
        self.save(s, "idle_file_slot")

        s = self.make_surface(width, height)
        s.subsurface((0, top_y, bar_width, top_height)).fill(self.accent_color)
        s.subsurface((shot_offset, top_y, shot_width, top_height)).fill(self.accent_color.shade(.5))
        self.save(s, "hover_file_slot")


    def generate_frame(self):
        width = self.scale_int(600)
        height = self.scale_int(250)

        border = self.scale_int(3)

        s = self.make_surface(width, height)
        s.fill(self.accent_color)
        s.subsurface((border, border, width - 2 * border, height - 2 * border)).fill(self.boring_color)
        self.save(s, "frame")

    def generate_bars(self):

        def fill(name, color, width, height, vname):
            width = self.scale_int(width)
            height = self.scale_int(height)

            s = self.make_surface(width, height)
            s.fill(color)
            self.save(s, name)

            s = self.make_surface(height, width)
            s.fill(color)
            self.save(s, vname)

        fill("bar/left", self.accent_color, 350, 30, "bar/bottom")
        fill("bar/right", self.muted_color, 350, 30, "bar/top")

        fill("slider/horizontal_idle_bar", self.muted_color, 350, 30, "slider/vertical_idle_bar")
        fill("slider/horizontal_hover_bar", self.hover_muted_color, 350, 30, "slider/vertical_hover_bar")
        fill("slider/horizontal_idle_thumb", self.accent_color, 10, 30, "slider/vertical_idle_thumb_bar")
        fill("slider/horizontal_hover_thumb", self.hover_color, 10, 30, "slider/vertical_hover_thumb_bar")

        fill("scrollbar/horizontal_idle_bar", self.muted_color, 350, 10, "scrollbar/vertical_idle_bar")
        fill("scrollbar/horizontal_hover_bar", self.hover_muted_color, 350, 10, "scrollbar/vertical_hover_bar")
        fill("scrollbar/horizontal_idle_thumb", self.accent_color, 350, 10, "scrollbar/vertical_idle_thumb")
        fill("scrollbar/horizontal_hover_thumb", self.hover_color, 350, 10, "scrollbar/vertical_hover_thumb")

    def generate_buttons(self):

        padding = self.scale_int(4)

        def fill(name, width, height, color=None, fill_width=None):
            width = self.scale_int(width) + padding * 2
            height = self.scale_int(height) + padding * 2

            s = self.make_surface(width, height)

            if fill_width is not None:
                fill_width = self.scale_int(fill_width)
                ss = s.subsurface((padding, padding, fill_width, height - padding * 2))
            else:
                ss = s

            if color is not None:
                ss.fill(color)

            self.save(s, name)

        def button_family(prefix, width, height, fill_width=None):

            fill(prefix + "/idle_background", width, height)
            fill(prefix + "/hover_background", width, height)

            if fill_width is not None:
                fill(prefix + "/selected_idle_background", width, height, self.accent_color, fill_width=fill_width)
                fill(prefix + "/selected_hover_background", width, height, self.accent_color, fill_width=fill_width)

        button_family("button", 280, 37)
        button_family("button/medium", 106, 37)
        button_family("button/small", 50, 37)
        button_family("button/check", 280, 37, self.scale_int(5))
        button_family("button/radio", 280, 37,  self.scale_int(5))


    def generate_skip(self):
        XSIZE = 240
        XRIGHT = 50

        YSIZE = 43

        X = [
            (0, 1.0),
            (XSIZE - XRIGHT, 1.0),
            (XSIZE, 0.0),
            ]

        Y = [
            (0, 1.0),
            (YSIZE, 1.0),
            ]

        self.generate_image("skip", X, Y, self.boring_color.opacity(.8))

    def generate_notify(self):
        XSIZE = 922
        XRIGHT = 50

        YSIZE = 43

        X = [
            (0, 1.0),
            (XSIZE - XRIGHT, 1.0),
            (XSIZE, 0.0),
            ]

        Y = [
            (0, 1.0),
            (YSIZE, 1.0),
            ]

        self.generate_image("notify", X, Y, self.boring_color.opacity(.8))


    def generate_icon(self):

        icon_fn = os.path.join(config.renpy_base, "launcher", "game", "gui7", "icon.png")
        icon = pygame_sdl2.image.load(icon_fn)

        width, height = icon.get_size()
        surf =  pygame_sdl2.Surface((width, height), pygame_sdl2.SRCALPHA)

        ro, go, bo, _ao = tuple(self.accent_color)

        ro -= 23
        go -= 23
        bo -= 23


        for y in range(height):
            for x in range(width):
                r, g, b, a = icon.get_at((x, y))

                r = max(0, min(r + ro, 255))
                g = max(0, min(g + go, 255))
                b = max(0, min(b + bo, 255))



                surf.set_at((x, y), (r, g, b, a))

        self.save(surf, "window_icon")


    def generate_menus(self):
        s = self.make_surface(self.width, self.height)
        s.fill(self.menu_color)

        self.save(s, "main_menu", overwrite=False)
        self.save(s, "game_menu", overwrite=False)


    def generate_all(self):
        self.generate_textbox()
        self.generate_choice_button()
        self.generate_overlay()
        self.generate_file_slot()
        self.generate_frame()
        self.generate_nvl()
        self.generate_bars()
        self.generate_buttons()
        self.generate_skip()
        self.generate_notify()
        self.generate_menus()
        self.generate_icon()

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()

    ap.add_argument("prefix")
    ap.add_argument("width", type=int)
    ap.add_argument("height", type=int)

    args = ap.parse_args()

    ImageGenerator(args.prefix, args.width, args.height).generate_all()


