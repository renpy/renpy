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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy

scene_lists = renpy.display.scenelists.scene_lists


def count_displayables_in_layer(layer):
    """
    Returns how many displayables are in the supplied layer.
    """

    sls = scene_lists()

    return len(sls.layers[layer])


def image(name, d):
    """
    :doc: se_images

    Defines an image. This function is the Python equivalent of the
    image statement.

    `name`
        The name of the image to display, a string.

    `d`
        The displayable to associate with that image name.

    This function may only be run from inside an init block. It is an
    error to run this function once the game has started.
    """

    if d is None:
        raise Exception("Images may not be declared to be None.")

    if not renpy.game.context().init_phase:
        raise Exception("Images may only be declared inside init blocks.")

    if not isinstance(name, tuple):
        name = tuple(name.split())

    d = renpy.easy.displayable(d)
    renpy.display.image.register_image(name, d)


def copy_images(old, new):
    """
    :doc: image_func

    Copies images beginning with one prefix to images beginning with
    another. For example::

        renpy.copy_images("eileen", "eileen2")

    will create an image beginning with "eileen2" for every image beginning
    with "eileen". If "eileen happy" exists, "eileen2 happy" will be
    created.

    `old`
        A space-separated string giving the components of the old image
        name.

    `new`
        A space-separated string giving the components of the new image
        name.
    """

    if not isinstance(old, tuple):
        old = tuple(old.split())

    if not isinstance(new, tuple):
        new = tuple(new.split())

    lenold = len(old)

    for k, v in renpy.display.image.images.items():
        if len(k) < lenold:
            continue

        if k[:lenold] == old:
            renpy.display.image.register_image(new + k[lenold:], v)


def default_layer(layer, tag, expression=False):
    """
    :undocumented:

    If layer is not None, returns it. Otherwise, interprets `tag` as a name
    or tag, then looks up what the default layer for that tag is, and returns
    the result.
    """

    if layer is not None:
        return layer

    if (tag is None) or expression:
        return renpy.config.default_tag_layer

    if isinstance(tag, tuple):
        tag = tag[0]
    elif " " in tag:
        tag = tag.split()[0]

    return scene_lists().sticky_tags.get(tag, None) or \
           renpy.config.tag_layer.get(tag, renpy.config.default_tag_layer)

def can_show(name, layer=None, tag=None):
    """
    :doc: image_func

    Determines if `name` can be used to show an image. This interprets `name`
    as a tag and attributes. This is combined with the attributes of the
    currently-showing image with `tag` on `layer` to try to determine a unique image
    to show. If a unique image can be show, returns the name of that image as
    a tuple. Otherwise, returns None.

    `tag`
        The image tag to get attributes from. If not given, defaults to the first
        component of `name`.

    `layer`
        The layer to check. If None, uses the default layer for `tag`.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    if tag is None:
        tag = name[0]

    layer = default_layer(layer, tag)

    try:
        return renpy.game.context().images.apply_attributes(layer, tag, name)
    except Exception:
        return None


def showing(name, layer=None):
    """
    :doc: image_func

    Returns true if an image with the same tag as `name` is showing on
    `layer`.

    `image`
        May be a string giving the image name or a tuple giving each
        component of the image name. It may also be a string giving
        only the image tag.

    `layer`
        The layer to check. If None, uses the default layer for `tag`.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    layer = default_layer(layer, name)

    return renpy.game.context().images.showing(layer, name)


def get_showing_tags(layer='master', sort=False):
    """
    :doc: image_func

    Returns the set of image tags that are currently being shown on `layer`. If
    sort is true, returns a list of the tags from back to front.
    """

    if sort:
        return scene_lists().get_sorted_tags(layer)

    return renpy.game.context().images.get_showing_tags(layer)


def get_hidden_tags(layer='master'):
    """
    :doc: image_func

    Returns the set of image tags on `layer` that are currently hidden, but
    still have attribute information associated with them.
    """

    return renpy.game.context().images.get_hidden_tags(layer)


def get_attributes(tag, layer=None, if_hidden=None):
    """
    :doc: image_func

    Return a tuple giving the image attributes for the image `tag`. If
    the image tag has not had any attributes associated since the last
    time it was hidden, returns `if_hidden`.

    `layer`
        The layer to check. If None, uses the default layer for `tag`.
    """

    layer = default_layer(layer, tag)
    return renpy.game.context().images.get_attributes(layer, tag, if_hidden)


def clear_attributes(tag, layer=None):
    """
    :doc: image_func

    Clears all image attributes for the `tag` image.
    If the tag had no attached image attributes, this does nothing.

    `layer`
        The layer to check. If None, uses the default layer for `tag`.
    """

    current = get_attributes(tag, layer, None)

    if not current:
        # either shown with no attributes to remove, or not showing
        return

    shown = showing(tag, default_layer(layer, tag))

    current = tuple('-'+a for a in current)
    set_tag_attributes((tag,)+current, layer)

    if shown:
        show(tag, layer=layer)


def _find_image(layer, key, name, what):
    """
    :undocumented:

    Finds an image to show.
    """

    # If a specific image is requested, use it.
    if what is not None:

        if isinstance(what, basestring):
            what = tuple(what.split())

        return name, what

    if renpy.config.image_attributes:

        new_image = renpy.game.context().images.apply_attributes(layer, key, name)
        if new_image is not None:
            image = new_image
            name = (key,) + new_image[1:]
            return name, new_image

    f = renpy.config.adjust_attributes.get(name[0], None) or renpy.config.adjust_attributes.get(None, None)
    if f is not None:
        new_image = f(name)
        name = (key,) + new_image[1:]
        return name, new_image

    return name, name


def predict_show(name, layer=None, what=None, tag=None, at_list=[ ]):
    """
    :undocumented:

    Predicts a scene or show statement.

    `name`
        The name of the image to show, a string.

    `layer`
        The layer the image is being shown on.

    `what`
        What is being show - if given, overrides `name`.

    `tag`
        The tag of the thing being shown.

    `at_list`
        A list of transforms to apply to the displayable.
    """

    key = tag or name[0]

    layer = default_layer(layer, key)

    if isinstance(what, renpy.display.displayable.Displayable):
        base = img = what

    else:

        name, what = _find_image(layer, key, name, what)
        base = img = renpy.display.image.ImageReference(what, style='image_placement')

        if not base.find_target():
            return

    for i in at_list:
        if isinstance(i, renpy.display.motion.Transform):
            img = i(child=img)
        else:
            img = i(img)

        img._unique()

    renpy.game.context().images.predict_show(layer, name, True)
    renpy.display.predict.displayable(img)


def set_tag_attributes(name, layer=None):
    """
    :doc: side

    This sets the attributes associated with an image tag when that image
    tag is not showing. The main use of this would be to directly set the
    attributes used by a side image.

    For example::

        $ renpy.set_tag_attributes("lucy mad")
        $ renpy.say(l, "I'm rather cross.")

    and::

        l mad "I'm rather cross."

    are equivalent.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    tag = name[0]
    name = renpy.game.context().images.apply_attributes(layer, tag, name)

    if name is not None:
        renpy.game.context().images.predict_show(layer, name, False)


def show(name, at_list=[ ], layer=None, what=None, zorder=None, tag=None, behind=[ ], atl=None, transient=False, munge_name=True):
    """
    :doc: se_images
    :args: (name, at_list=[], layer=None, what=None, zorder=0, tag=None, behind=[], atl=None, **kwargs)

    Shows an image on a layer. This is the programmatic equivalent of the show
    statement.

    `name`
        The name of the image to show, a string.

    `at_list`
        A list of transforms that are applied to the image.
        The equivalent of the ``at`` property.

    `layer`
        A string, giving the name of the layer on which the image will be shown.
        The equivalent of the ``onlayer`` property. If None, uses the default
        layer associated with the tag.

    `what`
        If not None, this is a displayable that will be shown in lieu of
        looking on the image. (This is the equivalent of the show expression
        statement.) When a `what` parameter is given, `name` can be used to
        associate a tag with the image.

    `zorder`
        An integer, the equivalent of the ``zorder`` property. If None, the
        zorder is preserved if it exists, and is otherwise set to 0.

    `tag`
        A string, used to specify the image tag of the shown image. The
        equivalent of the ``as`` property.

    `behind`
        A list of strings, giving image tags that this image is shown behind.
        The equivalent of the ``behind`` property.

    `atl`
        If not None, an ATL Transform that will be applied. This takes only the ATL itself,
        it does not apply prior state.

    ::

        show a
        $ renpy.show("a")

        show expression w
        # anonymous show expression : no equivalent

        show expression w as a
        $ renpy.show("a", what=w)
        $ renpy.show("y", what=w, tag="a") # in this case, name is ignored

        show a at T, T2
        $ renpy.show("a", at_list=(T, T2))

        show a onlayer b behind c zorder d as e
        $ renpy.show("a", layer="b", behind=["c"], zorder="d", tag="e")
    """

    if isinstance(atl, renpy.display.transform.ATLTransform):
        atl = atl.atl

    default_transform = renpy.config.default_transform

    if renpy.game.context().init_phase:
        raise Exception("Show may not run while in init phase.")

    if not isinstance(name, tuple):
        name = tuple(name.split())

    if zorder is None and not renpy.config.preserve_zorder:
        zorder = 0

    sls = scene_lists()
    key = tag or name[0]

    layer = default_layer(layer, key)

    if renpy.config.sticky_positions:
        if not at_list and key in sls.at_list[layer]:
            at_list = sls.at_list[layer][key]

    if not at_list:
        tt = renpy.config.tag_transform.get(key, None)
        if tt is not None:
            at_list = renpy.easy.to_list(tt, copy=True)

    if isinstance(what, renpy.display.displayable.Displayable):

        if renpy.config.wrap_shown_transforms and isinstance(what, renpy.display.motion.Transform):
            base = img = renpy.display.image.ImageReference(what, style='image_placement')

            # Semi-principled, but mimics pre-6.99.6 behavior - if `what` is
            # already a transform, do not apply the default transform to it.
            default_transform = None

        else:
            base = img = what

    else:
        name, what = _find_image(layer, key, name, what)
        base = img = renpy.display.image.ImageReference(what, style='image_placement')

        if not base.find_target() and renpy.config.missing_show:
            result = renpy.config.missing_show(name, what, layer)

            if isinstance(result, renpy.display.displayable.Displayable):
                base = img = result
            elif result:
                return

    for i in at_list:
        if isinstance(i, renpy.display.motion.Transform):
            img = i(child=img)
        else:
            img = i(img) # type: ignore

        # Mark the newly created images unique.
        img._unique()

    # Update the list of images we have ever seen.
    renpy.game.persistent._seen_images[tuple(str(i) for i in name)] = True

    if tag and munge_name:
        name = (tag,) + name[1:]

    if renpy.config.missing_hide:
        renpy.config.missing_hide(name, layer)

    sls.add(layer, img, key, zorder, behind, at_list=at_list, name=name, atl=atl, default_transform=default_transform, transient=transient)


def hide(name, layer=None):
    """
    :doc: se_images

    Hides an image from a layer. The Python equivalent of the hide statement.

    `name`
        The name of the image to hide. Only the image tag is used, and
        any image with the tag is hidden (the precise name does not matter).

    `layer`
        The layer on which this function operates. If None, uses the default
        layer associated with the tag.
    """

    if renpy.game.context().init_phase:
        raise Exception("Hide may not run while in init phase.")

    if not isinstance(name, tuple):
        name = tuple(name.split())

    sls = scene_lists()
    key = name[0]

    layer = default_layer(layer, key)

    sls.remove(layer, key)

    if renpy.config.missing_hide:
        renpy.config.missing_hide(name, layer)


def scene(layer='master'):
    """
    :doc: se_images

    Removes all displayables from `layer`. This is equivalent to the scene
    statement, when the scene statement is not given an image to show.

    A full scene statement is equivalent to a call to renpy.scene followed by a
    call to :func:`renpy.show`. For example::

        scene bg beach

    is equivalent to::

        $ renpy.scene()
        $ renpy.show("bg beach")
    """

    if layer is None:
        layer = 'master'

    if renpy.game.context().init_phase:
        raise Exception("Scene may not run while in init phase.")

    sls = scene_lists()
    sls.clear(layer)

    if renpy.config.missing_scene:
        renpy.config.missing_scene(layer)

    # End a transition that's affecting layer.
    renpy.display.interface.ongoing_transition.pop(layer, None)

    for i in renpy.config.scene_callbacks:
        i(layer)
