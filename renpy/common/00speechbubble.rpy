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


init -1050 python in bubble:

    from store import config, ADVCharacter, Character, JSONDB

    # The path to the json file the bubble database is stored in.
    config.bubble_json = "bubble.json"

    # The number of rows and columns in the bubble database.
    config.bubble_cols = 24
    config.bubble_rows = 24

    # The default window area rectangle. This is expressed as squares, where units
    # are  defined by the rows and columns.
    config.bubble_default_window_area = (0, 18, 24, 6)

    # Additional properties that the player can use to customize the bubble.
    # This is a map from a property name to a list of choices that are cycled
    # through.
    config.bubble_properties = { } # type: ignore

    # This is set to the JSONDB object that stores the bubble database,
    # or None if the databse doesn't exist yet.
    db = None # type: ignore

    # A map from an image tag to the properties used by speech bubbles with
    # that image tag.
    tag_properties = { } # type: ignore

    def scene_callback(layer):
        global tag_properties

        if layer == "master":
            tag_properties = { }

    config.scene_callbacks.append(scene_callback)


    class BubbleCharacter(ADVCharacter):

        def __init__(self, *args, **kwargs):

            super(BubbleCharacter, self).__init__(*args, **kwargs)

            if kwargs.get("_bubble", False):
                return

            if self.image_tag is None:
                raise Exception("BubbleCharacter require an image tag (the image='...' parameter).")

            global db

            if db is None:
                db = JSONDB(config.bubble_json)


        def bubble_default_properties(self, image_tag):
            """
            This is responsible for creating a reasonable set of bubble properties
            for the given image tag.
            """

            rv = { }

            xgrid = config.screen_width / config.bubble_cols
            ygrid = config.screen_height / config.bubble_rows

            rv["window_area"] = (
                int(config.bubble_default_window_area[0] * xgrid),
                int(config.bubble_default_window_area[1] * ygrid),
                int(config.bubble_default_window_area[2] * xgrid),
                int(config.bubble_default_window_area[3] * ygrid)
            )

            for i in config.bubble_properties:
                rv[i] = config.bubble_properties[i][0]

            return rv

        def __call__(self, *args, **kwargs):
            bubble = kwargs.pop("_bubble", None)

            if not bubble:

                image_tag = self.image_tag

                if image_tag not in self.properties:
                    self.properties[image_tag] = self.bubble_default_properties(image_tag)

                char_args = dict(self.properties[image_tag])
                char_args["kind"] = self
                char_args["_bubble"] = True

                kwargs["_bubble"] = True


                Character(**char_args).__call__(*args, **kwargs)

            else:
                super(BubbleCharacter, self).__call__(*args, **kwargs)
