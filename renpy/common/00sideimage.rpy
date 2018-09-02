# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

init -1650 python:

    ##########################################################################
    # Side Images

    # A tag to use. This can be used to force the side image to only be of the
    # main character.
    config.side_image_tag = None

    # If True, the side image will only be shown if an image with the same tag
    # is not shown.
    config.side_image_only_not_showing = False

    # A transform to use when the side image changes to that of a different
    # character.
    config.side_image_change_transform = None

    # A transform to use when the side image changes to that of the same
    # character.
    config.side_image_same_transform = None

    # The null to use.
    config.side_image_null = Null()

    _side_image_old = config.side_image_null
    _side_image_raw = config.side_image_null
    _side_image = config.side_image_null

    def _side_per_interact():
        """
        Called once per interaction to update the side image.
        """

        global _side_image_raw
        global _side_image

        old = _side_image_raw

        new = renpy.get_side_image(config.side_image_prefix_tag, image_tag=config.side_image_tag, not_showing=config.side_image_only_not_showing)

        if new is None:
            new = config.side_image_null
        else:
            new = ImageReference(new)

        _side_image_raw = new

        if config.skipping or renpy.game.after_rollback:
            tf = None
        elif isinstance(old, Null) and isinstance(new, Null):
            tf = None
        elif isinstance(old, Null) or isinstance(new, Null) or new.name[1] != old.name[1]:
            tf = config.side_image_change_transform
        else:
            tf = config.side_image_same_transform

        if tf:
            _side_image = tf(old, new)
        else:
            _side_image = new

    config.start_interact_callbacks.append(_side_per_interact)

    def SideImage(prefix_tag=None):
        """
        :doc: side_image_function
        :args: ()

        Returns the side image associated with the currently speaking character,
        or a Null displayable if no such side image exists.
        """

        # Compatibility with older games.
        if (prefix_tag is not None) and (prefix_tag != config.side_image_prefix_tag):
            config.side_image_prefix_tag = prefix_tag
            _side_per_interact()

        return _side_image

init 1650 python:

    _side_image_old = config.side_image_null
    _side_image_raw = config.side_image_null
    _side_image = config.side_image_null

