# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

init -1050 python in bubble:

    from store import config, ADVCharacter, Character, JSONDB, Action

    # The path to the json file the bubble database is stored in.
    db_filename = "bubble.json"

    # The number of rows and columns in the bubble database.
    cols = 24
    rows = 24

    # The default window area rectangle. This is expressed as squares, where units
    # are  defined by the rows and columns.
    default_window_area = (0, 18, 24, 6)

    # Additional properties that the player can use to customize the bubble.
    # This is a map from a property name to a list of choices that are cycled
    # through.
    properties = { }

    # This is set to the JSONDB object that stores the bubble database,
    # or None if the databse doesn't exist yet.
    db = None


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

            super(BubbleCharacter, self).__init__(*args, **kwargs)

            if self.image_tag is None:
                raise Exception("BubbleCharacter require an image tag (the image='...' parameter).")

            global db

            if db is None:
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

            rv = { }

            xgrid = config.screen_width / cols
            ygrid = config.screen_height / rows

            rv["window_area"] = (
                int(default_window_area[0] * xgrid),
                int(default_window_area[1] * ygrid),
                int(default_window_area[2] * xgrid),
                int(default_window_area[3] * ygrid)
            )

            for i in properties:
                rv[i] = properties[i][0]

            return rv


        def do_show(self, who, what, multiple=None, extra_properties=None):

            if extra_properties is None:
                extra_properties = { }
            else:
                extra_properties = dict(extra_properties)

            extra_properties["window_background"] = "#f00"

            image_tag = self.image_tag

            if image_tag not in self.properties:
                tag_properties[image_tag] = self.bubble_default_properties(image_tag)

            tlid = renpy.get_translation_identifier()

            if tlid is not None:
                tag_properties[image_tag].update(db[tlid])

                current_dialogue.append((image_tag, tlid))

            return super(BubbleCharacter, self).do_show(who, what, multiple=multiple, extra_properties=tag_properties[image_tag])

    def render_bubble_property(name, value):
        """
        Converts a bubble property into a text string. This may be overridden
        if you want to shorten the property.
        """

        return "{}={!r}".format(name, value)

    class CycleBubbleProperty(Action):
        """
        This is an action that causes the given property to be cycled
        through.
        """

        def __init__(self, image_tag, tlid, property):
            self.image_tag = image_tag
            self.tlid = tlid
            self.property = property

        def get_selected(self):
            return self.property in db[self.tlid]

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
            return "window_area" in db[self.tlid]

        def finished(self, rect):
            rect = list(rect)
            db[self.tlid]["window_area"] = rect
            renpy.rollback(checkpoints=0, force=True, greedy=True)

    def GetCurrentDialogue():
        """
        Returns the properties of the current bubble.

        Returns a list of (tlid, property list) pairs, where each property list
        contains a (name, action) pair.
        """

        rv = [ ]

        for image_tag, tlid in current_dialogue:
            properties = [ ]

            for k, v in sorted(tag_properties[image_tag].items()):
                properties.append((
                    render_bubble_property(k, v),
                    SetWindowArea(image_tag, tlid) if (k == "window_area") else CycleBubbleProperty(image_tag, tlid, k)
                    ))

            rv.append((image_tag, properties))

        return rv


screen _bubble_editor():
    zorder 1050

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
                        action Hide()
                        text_color "#ddd"
                        text_hover_color "#fff"
                        text_size gui._scale(14)

                null height gui._scale(5)

                for image_tag, properties in bubble.GetCurrentDialogue():

                    hbox:
                        spacing gui._scale(5)

                        text "[image_tag!q]":
                            style "_default"
                            color "#fff"
                            size gui._scale(14)

                        for prop, action in properties:
                            textbutton "[prop!q]":
                                style "_default"
                                action action
                                text_color "#ddd8"
                                text_selected_idle_color "#ddd"
                                text_hover_color "#fff"
                                text_size gui._scale(14)

screen _bubble_window_area_editor(action):
    modal True
    zorder 1051

    areapicker:
        cols bubble.cols
        rows bubble.rows

        finished action.finished

        add "#f004"

    key "game_menu" action Hide()
