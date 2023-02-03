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

python early:
    renpy.register_sl_statement("iconbutton", 1, 0) \
        .add_property("caption") \
        .add_property_group("window") \
        .add_property_group("button") \
        .add_property_group("text", "text_") \
        .add_property_group("position", "text_") \
        .add_property_group("position", "icon_") \
        .add_prefix_style_property("icon_", "color")

screen iconbutton(icon, caption=None, **properties):
    $ icon_properties, text_properties, button_properties = renpy.split_properties(properties, "icon_", "text_", "")

    button:
        style "iconbutton"
        properties button_properties

        if caption:
           text caption style "iconbutton_text" properties text_properties

        icon icon style "iconbutton_icon" properties icon_properties

