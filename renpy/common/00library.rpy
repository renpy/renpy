# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# This is kind of a catch-all file for things that are defined in the library,
# but don't merit their own files.


init -1700 python:
    class DictEquality(object):
        """
        Declares two objects equal if their types are the same, and
        their internal dictionaries are equal.
        """

        def __eq__(self, o):
            if self is o:
                return True

            if type(self) is type(o):
                return (self.__dict__ == o.__dict__)

            return False

    class FieldEquality(object):
        """
        Declares two objects equal if their types are the same, and
        the listed fields are equal.
        """

        # The lists of fields to use.
        equality_fields = [ ]
        identity_fields = [ ]

        def __eq__(self, o):
            if self is o:
                return True

            if type(self) is not type(o):
                return False

            for k in self.equality_fields:
                if self.__dict__[k] != o.__dict__[k]:
                    return False

            for k in self.identity_fields:
                if self.__dict__[k] is not o.__dict__[k]:
                    return False

            return True

init -1700 python:

    # basics: True if the skip indicator should be shown.
    config.skip_indicator = True

    # This is updated to give the user an idea of where a save is
    # taking place.
    save_name = ''

    def _default_empty_window():

        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator

        if isinstance(who, NVLCharacter):
            nvl_show_core()
        else:
            store.narrator("", interact=False)

    config.empty_window = _default_empty_window

    style.skip_indicator = Style(style.default, heavy=True, help='The skip indicator.')
    style.skip_indicator.xpos = 10
    style.skip_indicator.ypos = 10


init -1700 python:

    config.extend_interjection = "{fast}"

    def extend(what, interact=True):
        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator

        if isinstance(who, basestring):
            who = unknown.copy(who)

        # This ensures extend works even with NVL mode.
        who.do_extend()

        what = _last_say_what + config.extend_interjection + _last_raw_what

        renpy.exports.say(who, what, interact=interact)
        store._last_say_what = what

    extend.record_say = False


init -1700 python:

    def skip_indicator():

        ### skip_indicator default
        # (text) The style and placement of the skip indicator.

        if config.skip_indicator is True:

            if config.skipping == "slow" and config.skip_indicator:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            if config.skipping == "fast" and config.skip_indicator:
                ui.text(_(u"Fast Skip Mode"), style='skip_indicator')

            return

        if not config.skip_indicator:
            return

        if not config.skipping:
            return

        ui.add(renpy.easy.displayable(config.skip_indicator))

    config.overlay_functions.append(skip_indicator)

    # Prediction of screens.
    def predict():

        s = _game_menu_screen

        if s is None:
            return

        if renpy.has_screen(s):
            renpy.predict_screen(s)
            return

        if s.endswith("_screen"):
            s = s[:-7]
            if renpy.has_screen(s):
                renpy.predict_screen(s)
                return


    config.predict_callbacks.append(predict)

init -1700 python:

    ##########################################################################
    # Side Images

    config.side_image_tag = None
    config.side_image_only_not_showing = False

    def SideImage(prefix_tag="side"):
        """
        :doc: side_image_function

        Returns the side image associated with the currently speaking character,
        or a Null displayable if no such side image exists.
        """

        name = renpy.get_side_image(prefix_tag, image_tag=config.side_image_tag, not_showing=config.side_image_only_not_showing)
        if name is None:
            return Null()
        else:
            return ImageReference(name)


init -1000:
    # Lock the library object.
    $ config.locked = True


# After init, make some changes based on if config.developer is True.
init 1700 python hide:

    if config.developer:

        if config.debug_sound is None:
            config.debug_sound = True

        renpy.load_module("_developer/developer")
        renpy.load_module("_developer/inspector")

# Entry point for the developer screen. The rest of it is loaded from
# _developer.rpym
label _developer:

    if not config.developer:
        return

    $ _enter_menu()

    jump expression "_developer_screen"


# This is used to ensure a fixed click-to-continue indicator is shown on
# its own layer.
screen _ctc:
    add ctc

init -1900 python:

    # directories including images for composite images.
    config.automatic_images_parts = None

    # directories including not necessary images for composite images.
    config.automatic_images_not_necessary_parts = []

init 1900 python hide:

    def create_automatic_composite_images():
        import itertools

        seps = config.automatic_images

        if seps is True:
            seps = [ ' ', '/', '_' ]

        image_parts = dict()

        for dir, fn in renpy.loader.listdirfiles():

            if fn.startswith("_"):
                continue

            # Only .png and .jpg
            if not fn.lower().endswith(".png") and not fn.lower().endswith(".jpg"):
                continue

            # Strip the extension, replace slashes.
            shortfn = fn[:-4].replace("\\", "/")

            #store parts to image_parts
            for i in config.automatic_images_parts:
                if shortfn.find("/"+i+"/") > 0:

                    name = (shortfn[:shortfn.find("/"+i+"/")], )
                    for sep in seps:
                        name = tuple(j for i in name for j in i.split(sep))
                    # Strip name components.
                    while name:
                        for j in config.automatic_images_strip:
                            if name[0] == j:
                                name = name[1:]
                                break
                        else:
                            break

                    parts = (shortfn[shortfn.find("/"+i+"/")+len(i)+2:], )
                    for sep in seps:
                        parts = tuple(j for i in parts for j in i.split(sep))


                    if name not in image_parts:
                        image_parts[name] = { i:[] for i in config.automatic_images_parts }

                    image_parts[name][i].append((parts, fn))

        # define images consisting of several images
        for name in image_parts:
            parts_lists = []
            for part in config.automatic_images_parts:
                if image_parts[name][part]:
                    if part in config.automatic_images_not_necessary_parts:
                        image_parts[name][part].append(None)
                    parts_lists.append(image_parts[name][part])

            all_pattern = map(list, itertools.product(*parts_lists))

            for i in all_pattern:
                if i[0] is not None:
                    size = renpy.image_size(i[0][1])
                    break

            for i in all_pattern:
                name_args = name
                file_args = ()
                for k in i:
                    if k is not None:
                        name_args += k[0]
                        file_args += (0,0), k[1]

                # Only names of 2 components or more by default.
                if len(name_args) < config.automatic_images_minimum_components:
                    continue

                # Reject if it already exists.
                if name_args in renpy.display.image.images:
                    continue

                renpy.image(name_args, LiveComposite(size, *file_args))
 
    if config.automatic_images and config.automatic_images_parts:
        create_automatic_composite_images()
