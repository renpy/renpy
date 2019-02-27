# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.store import Color
import time

# The target width used in templates.
WIDTH = 1280
HEIGHT = 720


class GuiParameters(object):
    """
    This represents the parameters to the gui. This is used to initialize
    the ImageGenerator and CodeGenerator objects to a consistent set of
    parameters.
    """

    def __init__(self, prefix, template, width, height, accent, boring, light, language, replace_images, replace_code, update_code, name=None):

        self.prefix = prefix
        self.template = template

        self.width = width
        self.height = height

        self.scale = min(1.0 * width / WIDTH, 1.0 * height / HEIGHT)

        self.accent_color = Color(accent)
        self.boring_color = Color(boring)

        # tint = n * color + (1-n) * white
        # shade = n * color + (1-n) * black

        self.light = light

        if light:
            self.hover_color = self.accent_color  # .tint(.95)
            self.muted_color = self.accent_color.tint(.6)
            self.hover_muted_color = self.accent_color.tint(.4)
        else:
            self.hover_color = self.accent_color.tint(.6)
            self.muted_color = self.accent_color.shade(.4)
            self.hover_muted_color = self.accent_color.shade(.6)

        self.menu_color = self.accent_color.replace_hsv_saturation(.25).replace_value(.5)
        self.title_color = self.accent_color.replace_hsv_saturation(.5).replace_value(1.0)

        if light:

            self.selected_color = Color("#555555")
            self.idle_color = Color("#aaaaaa")
            self.idle_small_color = Color("#888888")
            self.text_color = Color("#404040")
            self.choice_color = Color("#cccccc")

        else:

            self.selected_color = Color("#ffffff")
            self.idle_color = Color("#888888")
            self.idle_small_color = Color("#aaaaaa")
            self.text_color = Color("#ffffff")
            self.choice_color = Color("#cccccc")

        self.insensitive_color = self.idle_color.replace_opacity(.5)

        self.language = language

        if replace_code:
            update_code = True

        self.replace_images = replace_images
        self.replace_code = replace_code
        self.update_code = update_code

        self.skip_backup = False

        name = name or ''

        self.name = name

        GOOD_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"

        simple_name = "".join(i for i in name if i in GOOD_CHARACTERS).encode("ascii")

        if not simple_name:
            simple_name = "game"

        self.simple_name = simple_name

        self.savedir = self.simple_name + "-" + str(int(time.time()))
