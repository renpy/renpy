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

    class Placeholder(renpy.Displayable):
        """
        :doc: placeholder

        This displayable can be used to display a placeholder character or
        background.
        """

        text = None

        def after_setstate(self):
            self.child = None

        def __init__(self, base=None, full=False, flip=None, text=None, **properties):
            """
            `base`
                The type of image to display. This should be one of:

                'bg'
                    To display a background placeholder. This currently
                    fills the screen with a light-gray, and displays
                    the image name at the top of the screen.

                'boy'
                    Displays a male-identified placeholder with the image
                    name on his chest.

                'girl'
                    Displays a female-identified placeholder with the image
                    name on her chest.

                None
                    Attempts to automatically determine the type of image
                    to use. If the image name begins with "bg", "cg", or
                    "event", uses 'bg'.

                    Otherwise, the 'girl' placeholder is used.

            `full`
                If true, a full-body sprite is used. Otherwise, a 3/4 sprite
                is used.

            `flip`
                If true, the sprite is flipped horizontally.

            `text`
                If provided, no other text than this will be displayed on the
                placeholder. If not, the text will reflect the show
                instruction that was used to display it.
            """

            super(Placeholder, self).__init__(**properties)

            self.base = base
            self.flip = flip
            self.full = full

            # A list of name components.
            self.name = [ ]

            # The child of this placeholder, if known.
            self.child = None

            # The text of this placeholder, if known. This replaces the
            # any derived text.
            self.text = text


        def guess_base(self):
            """
            Tries to guess a base image to use based on the name of
            the image.
            """

            if not self.name:
                return 'girl'

            tag = self.name[0]

            if tag in ( "bg", "cg", "event" ):
                return "bg"

            if not config.developer:
                return "girl"

            if persistent._placeholder_gender is None:
                persistent._placeholder_gender = { }

            if tag in persistent._placeholder_gender:
                return persistent._placeholder_gender[tag]

#             try:
#                 import urllib2
#                 import json
#
#                 u = urllib2.urlopen("http://api.genderize.io/?name=" + tag.encode("utf-8"), timeout=3)
#                 data = json.loads(u.read())
#
#                 if data.get("gender", "") == "male":
#                     rv = "boy"
#                 else:
#                     rv = "girl"
#             except Exception:
#                 rv = "girl"

            rv = "girl"
            persistent._placeholder_gender[tag] = rv

            return rv

        def get_child(self):
            """
            Gets the child image to use.
            """

            if self.child:
                return self.child

            # Determine the base.
            base = self.base

            if base is None:
                base = self.guess_base()

            # Bg bases.
            if base == "bg":
                rv = Fixed(
                    Solid("#aaa"),
                    Text(" ".join(self.name), style="_default", color="#333333", textalign=0.5, xalign=0.5, ypos=5),
                    alt="",
                )

                self.child = rv
                return rv

            # Find the character image to use.
            if base == "boy":
                image = Image("_placeholder/boy.png")
                textpos = (187, 500)
                size = (380, 1800)
            else:
                image = Image("_placeholder/girl.png")
                textpos = (182, 540)
                size = (411, 1800)

            # Get the portion of the image to show.
            if not self.full:
                size = (size[0], 1080)

            # Scale to screen height.
            zoom = 1.0 * config.screen_height / size[1]
            crop = (0, 0) + size
            size = (int(size[0] * zoom), int(size[1] * zoom))
            textpos = (int(textpos[0] * zoom), int(textpos[1] * zoom))

            # Flip as necessary.
            if self.flip:
                xzoom = -1
                textpos = (size[0] - textpos[0], textpos[1])
            else:
                xzoom = 1

            if self.text is not None:
                text = self.text
            else:
                text = "\n".join(self.name)

            rv = Fixed(
                Transform(image, crop=crop, size=size, xzoom=xzoom),
                Text(text, pos=textpos, xanchor=0.5, yanchor=0.5, style="_default", color="#aaa", textalign=0.5),
                xysize=size,
                alt="",
            )

            self.child = rv
            return rv

        _duplicatable = True

        def _duplicate(self, args):
            if not self._duplicatable:
                return False

            args = args or self._args

            rv = Placeholder(self.base, self.full, self.flip, self.text)
            rv.name = list(args.name) + list(args.args)
            rv._duplicatable = False

            return rv

        def visit(self):
            return [ self.get_child() ]

        def render(self, width, height, st, at):
            child = self.get_child()
            return renpy.render(child, width, height, st, at)
