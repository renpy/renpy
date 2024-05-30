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

# Should translation files be shown in the launcher file navigation?
default persistent.show_translation_files = True

init python in navigation:
    import store.interface as interface
    import store.project as project
    import store.editor as editor
    from store import persistent, Action


    # The last navigation screen we've seen. This is the scree we try to go
    # to the next time we enter navigation. (We may not be able to go there,
    # if the screen is empty.)
    if persistent.navigation is None:
        persistent.navigation = "label"

    # A map from a kind of information, to how we should sort it. Possible
    # sorts are alphabetical, by-file, natural.
    if persistent.navigation_sort is None:
        persistent.navigation_sort = { }

    if persistent.navigate_private is None:
        persistent.navigate_private = False

    if persistent.navigate_library is None:
        persistent.navigate_library = False

    # A list of kinds of navigation we support.
    KINDS = [ "file", "label", "define", "transform", "screen", "callable", "todo" ]

    # A map from kind name to adjustment.
    adjustments = { }

    for i in KINDS:
        persistent.navigation_sort.setdefault(i, "by-file")
        adjustments[i] = ui.adjustment()

    def group_and_sort(kind):
        """
        This is responsible for pulling navigation information of the
        appropriate kind out of project.current.dump, grouping it,
        and sorting it.

        This returns a list of (group, list of (name, filename, line)). The
        group may be a string or None.
        """

        project.current.update_dump()

        sort = persistent.navigation_sort[kind]

        name_map = project.current.dump.get("location", {}).get(kind, { })

        groups = { }

        for name, loc in name_map.items():
            filename, line = loc
            filename = filename.replace("\\", "/")

            if sort == "alphabetical":
                group = None
            else:
                group = filename
                if group.startswith("game/"):
                    group = group[5:]

            g = groups.get(group, None)
            if g is None:
                groups[group] = g = [ ]

            g.append((name, filename, line))

        for g in groups.values():
            if sort == "natural":
                g.sort(key=lambda a : a[2])
            else:
                g.sort(key=lambda a : a[0].lower())

        rv = list(groups.items())
        rv.sort()

        return rv

    def group_and_sort_files():

        rv = [ ]

        for fn in project.current.script_files():
            shortfn = fn
            shortfn = shortfn.replace("\\", "/")

            if shortfn.startswith("game/"):
                shortfn = fn[5:]

            if shortfn.startswith("tl/") and not persistent.show_translation_files:
                continue

            rv.append((shortfn, fn, None))

        rv.sort()

        return [ (None, rv) ]

    class ChangeKind(Action):
        """
        Changes the kind of thing we're navigating over.
        """

        def __init__(self, kind):
            self.kind = kind

        def get_selected(self):
            return persistent.navigation == self.kind

        def __call__(self):
            if persistent.navigation == self.kind:
                return

            persistent.navigation = self.kind
            renpy.jump("navigation_loop")

    class ChangeSort(Action):
        """
        Changes the sort order.
        """

        def __init__(self, sort):
            self.sort = sort

        def get_selected(self):
            return persistent.navigation_sort[persistent.navigation] == self.sort

        def __call__(self):
            if self.get_selected():
                return

            persistent.navigation_sort[persistent.navigation] = self.sort
            renpy.jump("navigation_loop")


screen navigation:

    $ todo_count = len(project.current.dump.get("location", {}).get("todo", []))

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            frame style "l_label":
                has hbox xfill True
                text _("Navigate: [project.current.display_name!q]") style "l_label_text"
                alt _("Navigate Script")

                frame:
                    style "l_alternate"
                    style_group "l_small"

                    has hbox

                    if persistent.navigation != "file":
                        text _("Order: ")
                        textbutton _("alphabetical") action navigation.ChangeSort("alphabetical")
                        text " | "
                        textbutton _("by-file") action navigation.ChangeSort("by-file")
                        text " | "
                        textbutton _("natural") action navigation.ChangeSort("natural")

                        null width HALF_INDENT

                    textbutton _("refresh") action Jump("navigation_refresh")


            add HALF_SPACER

            frame style "l_indent":
                hbox:
                    spacing HALF_INDENT
                    text _("Category:")
                    alt ""

                    textbutton _("files") action navigation.ChangeKind("file")
                    textbutton _("labels") action navigation.ChangeKind("label")
                    textbutton _("defines") action navigation.ChangeKind("define")
                    textbutton _("transforms") action navigation.ChangeKind("transform")
                    textbutton _("screens") action navigation.ChangeKind("screen")
                    textbutton _("callables") action navigation.ChangeKind("callable")
                    textbutton (__("TODOs") + " (" + str(todo_count) + ")") action navigation.ChangeKind("todo")

            add SPACER
            add SEPARATOR

            frame style "l_indent_margin":

                if groups:

                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        yadjustment navigation.adjustments[persistent.navigation]

                        vbox:
                            style_group "l_navigation"

                            if persistent.navigation == "file":
                                textbutton _("Show translation files") style "l_checkbox" action [ ToggleField(persistent, "show_translation_files"), Jump("navigation_loop") ]
                                add SPACER

                            for group_name, group in groups:

                                if group_name is not None:
                                    text "[group_name!q]"

                                if persistent.navigation == "todo":
                                    vbox:
                                        for name, filename, line in group:
                                            textbutton "[name!q]" action editor.Edit(filename, line)

                                else:
                                    hbox:
                                        box_wrap True

                                        for name, filename, line in group:
                                            textbutton "[name!q]" action editor.Edit(filename, line)

                                if group_name is not None:
                                    add SPACER

                            if persistent.navigation == "file":
                                add SPACER
                                textbutton _("+ Add script file") action Jump("add_file") style "l_button"

                else:

                    fixed:

                        if persistent.navigation == "todo":

                            text _("No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."):
                                textalign 0.5
                                xalign 0.5
                                yalign 0.5

                        else:

                            text _("The list of names is empty."):
                                xalign 0.5
                                yalign 0.5

    textbutton _("Return") action Jump("front_page") style "l_left_button"
    textbutton _("Launch Project") action project.Launch() style "l_right_button"

label navigation:
label navigation_loop:

    python in navigation:

        kind = persistent.navigation

        if kind == "file":
            groups = group_and_sort_files()
        else:
            groups = group_and_sort(kind)

        renpy.call_screen("navigation", groups=groups)

label navigation_refresh:
    $ project.current.update_dump(True)
    jump navigation_loop
