# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This contains the performance monitoring screen.

init python:

    def _clear_performance():
        renpy.display.interface.frame_times[:] = [ ]

screen _performance:
    layer config.interface_layer

    on "show" action Function(_clear_performance)

    python:

        frame_times = renpy.display.interface.frame_times


        if len(frame_times) < 11:

            fps = 0.0
            cur_time = 0
            max_time = 0

        else:

            ift = [ (j - i) for i, j in zip(frame_times, frame_times[1:]) ]

            fps = 1.0 / (sum(ift[-10:]) / 10.0)

            cur_time = ift[-1] * 1000
            max_time = max(ift) * 1000

        renderer = renpy.get_renderer_info()["renderer"]

    zorder 1000

    drag:
        draggable True
        focus_mask None
        xpos 0
        ypos 0

        frame:
            style_prefix "_performance"
            style "empty"
            background "#0004"
            xpadding 5
            ypadding 5
            xminimum 150

            vbox:
                text "[fps:.1f] fps\n[cur_time:.3f] ms\n[max_time:.3f] ms max\n[renderer]":
                    style "_default"
                    color "#fff"
                    size gui._scale(14)

                if _preferences.gl_powersave:
                    $ mode = "powersave"
                else:
                    $ mode = "performance"

                textbutton "[mode]":
                    style "_default"
                    action Preference("gl powersave", "toggle")
                    text_color "#ddd"
                    text_hover_color "#fff"
                    text_size gui._scale(14)

init -1010 python:
    config.per_frame_screens.append("_performance")
