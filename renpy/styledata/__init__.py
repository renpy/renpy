# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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


from __future__ import print_function

import renpy
renpy.update_path()

def import_style_functions():
    import renpy.styledata.stylesets  # @UnresolvedImport

    import renpy.styledata.style_functions  # @UnresolvedImport
    import renpy.styledata.style_activate_functions  # @UnresolvedImport
    import renpy.styledata.style_hover_functions  # @UnresolvedImport
    import renpy.styledata.style_idle_functions  # @UnresolvedImport
    import renpy.styledata.style_insensitive_functions  # @UnresolvedImport

    import renpy.styledata.style_selected_functions  # @UnresolvedImport
    import renpy.styledata.style_selected_activate_functions  # @UnresolvedImport
    import renpy.styledata.style_selected_hover_functions  # @UnresolvedImport
    import renpy.styledata.style_selected_idle_functions  # @UnresolvedImport
    import renpy.styledata.style_selected_insensitive_functions  # @UnresolvedImport

    import renpy.styledata.styleclass  # @UnresolvedImport
    renpy.style.Style = renpy.styledata.styleclass.Style  # @UndefinedVariable
