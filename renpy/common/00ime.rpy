# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

# The in-game IME candidate list. This is shown by Ren'Py while an input
# method is offering candidates, as the platform's candidate window may be
# hidden when the game is fullscreen.

init -1500:

    style _ime_candidates_frame is default:
        background "#000000e0"
        padding (6, 4)

    style _ime_candidates_box is default:
        spacing 8

    style _ime_candidates_item_frame is default:
        background None
        padding (4, 2)

    style _ime_candidates_selected_item_frame is _ime_candidates_item_frame:
        background "#ffffffe0"

    style _ime_candidates_text is default:
        color "#ffffff"
        outlines [ ]
        xalign 0.0
        xmaximum None
        font (gui.system_font or "_WenQuanYiMicroHei.woff2")

    style _ime_candidates_selected_text is _ime_candidates_text:
        color "#000000"

    screen _ime_candidates():
        layer config.interface_layer
        zorder 1100

        $ _ime = renpy.display.ime.get_candidates()

        if _ime is not None:

            _ime_candidates_placer:

                frame:
                    style "_ime_candidates_frame"

                    hbox:
                        style "_ime_candidates_box"
                        box_layout ("horizontal" if _ime.horizontal else "vertical")

                        for _i, _c in enumerate(_ime.candidates):
                            frame:
                                style ("_ime_candidates_selected_item_frame" if _i == _ime.selected else "_ime_candidates_item_frame")

                                text "{}. {}".format(_i + 1, _c.replace("{", "{{")):
                                    style ("_ime_candidates_selected_text" if _i == _ime.selected else "_ime_candidates_text")
                                    substitute False
