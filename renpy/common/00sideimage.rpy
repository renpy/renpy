init -1650 python:

    ##########################################################################
    # Side Images

    # A tag to use. This can be used to force the side image to only be of the
    # main character.
    config.side_image_tag = None

    # If True, the side image will only be shown if an image with the same tag
    # is not shown.
    config.side_image_only_not_showing = False

    # The prefix to use on the side image.
    config.side_image_prefix_tag = 'side'

    # A transform to use when the side image changes to that of a different
    # character.
    config.side_image_change_transform = None

    # A transform to use when the side image changes to that of the same
    # character.
    config.side_image_same_transform = None

    # The null to use.
    config.side_image_null = Null()

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

