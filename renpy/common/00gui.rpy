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

init -1100 python in gui:
    from store import config, layout, _preferences

    config.translate_clean_stores.append("gui")

    def init(width, height):
        """
        :doc: gui

        Initializes the gui.

        `width`
            The width of the default window.

        `height`
            The height of the default window.
        """

        config.screen_width = width
        config.screen_height = height

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


    ############################################################################
    # Strings used by the confirm screen.

    ARE_YOU_SURE = layout.ARE_YOU_SURE
    DELETE_SAVE = layout.DELETE_SAVE
    OVERWRITE_SAVE = layout.OVERWRITE_SAVE
    LOADING = layout.LOADING
    QUIT = layout.QUIT
    MAIN_MENU = layout.MAIN_MENU
    END_REPLAY = layout.END_REPLAY
    SLOW_SKIP = layout.SLOW_SKIP
    FAST_SKIP_UNSEEN = layout.FAST_SKIP_UNSEEN
    FAST_SKIP_SEEN = layout.FAST_SKIP_SEEN


    ############################################################################
    # gui.Frame

    # This is a wrapper around Frame that allows us to apply standard amounts
    # of padding to each side of a frame.

    from store import Frame as _Frame

    class Insets(object):

        def __init__(self, left, top, right, bottom, pad_left=0, pad_top=0, pad_right=0, pad_bottom=0, tile=False):

            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom

            self.pad_left = pad_left
            self.pad_top = pad_top
            self.pad_right = pad_right
            self.pad_bottom = pad_bottom

            self.tile = tile

        @property
        def padding(self):
            return (
                self.left + self.pad_left,
                self.top + self.pad_top,
                self.right + self.pad_right,
                self.bottom + self.pad_bottom,
                )

    def Frame(d, insets, **properties):

        left = insets.left
        top = insets.top
        right = insets.right
        bottom = insets.bottom

        return _Frame(d,
            left=insets.left,
            top=insets.top,
            right=insets.right,
            bottom=insets.bottom,
            tile=insets.tile,
            **properties)









