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

# A map from an image tag to the properties used by speech bubbles with
# that image tag.
default bubble.tag_properties = { }

# A list of (image_tag, tlid) pairs represening the dialogue that is
# on the screen now.
default bubble.current_dialogue = [ ]

init -1150 python in bubble:

    from store import config, ADVCharacter, Character, JSONDB, Action, Frame, NoRollback

    # This gets set to true if at least one character that uses a speech bubble has been defined.
    active = False

    # This becomes true when the screen is shown.
    shown = NoRollback()
    shown.value = False

    # The path to the json file the bubble database is stored in.
    db_filename = "bubble.json"

    # The number of rows and columns in the grid that is used to position
    # speech bubbles.
    cols = 24
    rows = 24

    # The default window area rectangle. This is expressed as squares, where units
    # are defined by the rows and columns.
    default_area = (15, 1, 8, 5)

    # The property that the area is supplied as.
    area_property = "window_area"

    # Additional properties that the player can use to customize the bubble.
    # This is a map from a property name to a list of choices that are cycled
    # through.
    properties = { }

    # The property group names, in order.
    properties_order = [ ]

    # If not None, a function that takes the character's image tag, and returns
    # the list of property names that are allowed for that image tag.
    properties_callback = None

    # A map from property name to the (left, top, right, bottom) number of pixels
    # areas with that property are expanded by. If a property is not in this
    # map, None is tried.
    expand_area = { }

    # This is set to the JSONDB object that stores the bubble database,
    # or None if the database doesn't exist yet.
    db = None

    # These are not used directly, but are used by the default screens.rpy, and
    # so should not be set.
    frame = None
    thoughtframe = None

    # The layer that retained screens are placed on.
    retain_layer = "screens"

    class ToggleShown(Action):
        def __call__(self):
            if not active and not shown.value:
                return

            shown.value = not shown.value
            renpy.restart_interaction()

        def get_selected(self):
            return shown.value

    def scene_callback(layer):
        global tag_properties

        if layer == "master":
            tag_properties = { }


    def character_callback(event, interact=True, **kwargs):
        global current_dialogue

        if event == "end" and interact:
            current_dialogue = [ ]


    class BubbleCharacter(ADVCharacter):

        def __init__(self, *args, **kwargs):

            open_db = kwargs.pop("_open_db", True)

            kwargs.setdefault("statement_name", "say-bubble")

            super(BubbleCharacter, self).__init__(*args, **kwargs)

            if not open_db:
                return

            if self.image_tag is None:
                raise Exception("BubbleCharacter require an image tag (the image='...' parameter).")

            global active
            global db

            active = True

            if db is None and open_db:
                db = JSONDB(db_filename)

            if character_callback not in config.all_character_callbacks:
                config.all_character_callbacks.insert(0, character_callback)

            if scene_callback not in config.scene_callbacks:
                config.scene_callbacks.insert(0, scene_callback)

        def bubble_default_properties(self, image_tag):
            """
            This is responsible for creating a reasonable set of bubble properties
            for the given image tag.
            """

            if not properties_order:
                raise Exception("A speech bubble is being used, but bubble.properties has not been set.")

            rv = { }

            xgrid = config.screen_width / cols
            ygrid = config.screen_height / rows

            default_area_rect = [
                int(default_area[0] * xgrid),
                int(default_area[1] * ygrid),
                int(default_area[2] * xgrid),
                int(default_area[3] * ygrid)
            ]

            rv = {
                "area" : default_area_rect,
            }


            if properties_callback is not None:
                rv["properties"] = properties_callback(image_tag)[0]
            else:
                rv["properties"] = properties_order[0]

            return rv


        def expand_area(self, area, properties_key):
            """
            This is called to expand the area of a bubble. It is given the
            area, and the properties key, and returns a new area.
            """

            x, y, w, h = area

            expand = expand_area.get(properties_key, None) or expand_area.get(None, None)

            if expand is None:
                return area

            left, top, right, bottom = expand

            x = x - left
            y = y - top
            w = w + left + right
            h = h + top + bottom

            return (x, y, w, h)

        def do_add(self, who, what, multiple=False):

            tlid = renpy.get_translation_identifier()

            if tlid is not None:

                if db[tlid].get("clear_retain", False):
                    renpy.clear_retain(layer=retain_layer)

        def do_show(self, who, what, multiple=None, retain=None, extra_properties=None):

            if extra_properties is None:
                extra_properties = { }
            else:
                extra_properties = dict(extra_properties)

            image_tag = self.image_tag

            if retain or (image_tag not in tag_properties):
                tag_properties[image_tag] = self.bubble_default_properties(image_tag)

            tlid = renpy.get_translation_identifier()

            if tlid is not None:
                for k, v in db[tlid].items():
                    tag_properties[image_tag][k] = v

                current_dialogue.append((image_tag, tlid))

            properties_key = tag_properties[image_tag]["properties"]

            extra_properties.update(properties.get(properties_key, { }))
            extra_properties[area_property] = self.expand_area(tag_properties[image_tag]["area"], properties_key)

            return super(BubbleCharacter, self).do_show(who, what, multiple=multiple, retain=retain, extra_properties=extra_properties)

    class CycleBubbleProperty(Action):
        """
        This is an action that causes the property groups to be cycled
        through.
        """

        def __init__(self, image_tag, tlid):
            self.image_tag = image_tag
            self.tlid = tlid

        def get_selected(self):
            return "properties" in db[self.tlid]

        def __call__(self):

            current = tag_properties[self.image_tag]["properties"]

            if properties_callback is not None:
                properties = properties_callback(self.image_tag)
            else:
                properties = properties_order

            try:
                idx = properties.index(current)
            except ValueError:
                idx = 0

            idx = (idx + 1) % len(properties)

            db[self.tlid]["properties"] = properties[idx]
            renpy.rollback(checkpoints=0, force=True, greedy=True)

        def alternate(self):
            if "properties" in db[self.tlid]:
                del db[self.tlid]["properties"]
                renpy.rollback(checkpoints=0, force=True, greedy=True)


    class ToggleClearRetain(Action):
        """
        This is an action that causes the clear_retain property to be toggled.
        """

        def __init__(self, tlid):
            self.tlid = tlid

        def get_selected(self):
            return db[self.tlid].get("clear_retain", False)

        def __call__(self):
            db[self.tlid]["clear_retain"] = not db[self.tlid].get("clear_retain", False)
            renpy.rollback(checkpoints=0, force=True, greedy=True)

        def alternate(self):
            self()


    class SetWindowArea(Action):
        """
        An action that displays the area picker to select the window area.
        """

        def __init__(self, image_tag, tlid):
            self.image_tag = image_tag
            self.tlid = tlid

        def __call__(self):
            renpy.show_screen("_bubble_window_area_editor", self)
            renpy.restart_interaction()

        def get_selected(self):
            return "area" in db[self.tlid]

        def finished(self, rect):
            rect = list(rect)
            db[self.tlid]["area"] = rect
            renpy.rollback(checkpoints=0, force=True, greedy=True)

        def alternate(self):
            if "area" in db[self.tlid]:
                del db[self.tlid]["area"]
                renpy.rollback(checkpoints=0, force=True, greedy=True)

    def GetCurrentDialogue():
        """
        Returns the properties of the current bubble.

        Returns a list of (tlid, property list) pairs, where each property list
        contains a (name, action) pair.
        """

        rv = [ ]

        for image_tag, tlid in current_dialogue:
            property_list = [ ]

            property_list.append((
                "area={!r}".format(tag_properties[image_tag]["area"]),
                SetWindowArea(image_tag, tlid)))

            property_list.append((
                "properties={}".format(tag_properties[image_tag]["properties"]),
                CycleBubbleProperty(image_tag, tlid)))

            rv.append((image_tag, property_list))

        return rv

    # A character that inherits from bubble.
    character = BubbleCharacter(
        None,
        screen="bubble",
        window_style="bubble_window",
        who_style="bubble_who",
        what_style="bubble_what",
        _open_db=False)


init 1050 python hide:
    import json

    for k in sorted(bubble.properties):
        if k not in bubble.properties_order:
            bubble.properties_order.append(k)

    if config.developer:
        for k, v in bubble.properties.items():
            for i in v:
                try:
                    json.dumps(i)
                except Exception:
                    raise Exception("bubble.properties[{!r}] contains a value that can't be serialized to JSON: {!r}".format(k, i))

        if bubble.active:
            config.always_shown_screens.append("_bubble_editor")



screen _bubble_editor():
    zorder 1050

    if bubble.shown.value and not _menu:

        drag:
            draggable True
            focus_mask None
            xpos 0
            ypos 0

            frame:
                style "empty"
                background "#0004"
                xpadding 5
                ypadding 5
                xminimum 150

                vbox:
                    hbox:
                        spacing gui._scale(5)

                        text _("Speech Bubble Editor"):
                            style "_default"
                            color "#fff"
                            size gui._scale(14)

                        textbutton _("(hide)"):
                            style "_default"
                            action SetField(bubble.shown, "value", False)
                            selected False
                            text_color "#ddd8"
                            text_hover_color "#fff"
                            text_size gui._scale(14)

                    null height gui._scale(5)

                    if bubble.current_dialogue and renpy.get_screen("_retain_0", layer=bubble.retain_layer):
                        textbutton _("(clear retained bubbles)"):
                            style "_default"
                            text_color "#ddd8"
                            text_selected_idle_color "#ddd"
                            text_hover_color "#fff"
                            text_size gui._scale(16)

                            action bubble.ToggleClearRetain(bubble.current_dialogue[0][1])

                        null height gui._scale(5)

                    for image_tag, properties in bubble.GetCurrentDialogue():

                        hbox:
                            spacing gui._scale(5)

                            text "[image_tag!q]":
                                style "_default"
                                color "#fff"
                                size gui._scale(16)

                            for prop, action in properties:
                                textbutton "[prop!q]":
                                    style "_default"
                                    action action
                                    alternate action.alternate
                                    text_color "#ddd8"
                                    text_selected_idle_color "#ddd"
                                    text_hover_color "#fff"
                                    text_size gui._scale(16)




screen _bubble_window_area_editor(action):
    modal True
    zorder 1051

    areapicker:
        cols bubble.cols
        rows bubble.rows

        finished action.finished

        add "#f004"

    key "game_menu" action Hide()
