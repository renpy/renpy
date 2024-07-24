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

import gc
import time
import os

import renpy
import pygame_sdl2

from renpy.exports.commonexports import renpy_pure

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


def toggle_fullscreen():
    """
    :undocumented:
    Toggles the fullscreen mode.
    """

    renpy.game.preferences.fullscreen = not renpy.game.preferences.fullscreen # type: ignore


def take_screenshot(scale=None, background=False):
    """
    :doc: loadsave
    :args: ()

    Causes a screenshot to be taken. This screenshot will be saved as part of
    a saved game.
    """

    if scale is None:
        scale = (renpy.config.thumbnail_width, renpy.config.thumbnail_height)

    renpy.game.interface.take_screenshot(scale, background=background)


def screenshot(filename):
    """
    :doc: screenshot

    Saves a screenshot in `filename`.

    Returns True if the screenshot was saved successfully, False if saving
    failed for some reason.

    The :var:`config.screenshot_pattern` and :var:`_screenshot_pattern`
    variables control the file the screenshot is saved in.
    """

    return renpy.game.interface.save_screenshot(filename)


def screenshot_to_bytes(size):
    """
    :doc: screenshot

    Returns a screenshot as a bytes object, that can be passed to im.Data().
    The bytes will be a png-format image, such that::

        $ data = renpy.screenshot_to_bytes((640, 360))
        show expression im.Data(data, "screenshot.png"):
            align (0, 0)

    Will show the image. The bytes objects returned can be stored in save
    files and persistent data. However, these may be large, and care should
    be taken to not include too many.

    `size`
        The size the screenshot will be resized to. If None, the screenshot
        will be resized, and hence will be the size of the player's window,
        without any letterbars.

    This function may be slow, and so it's intended for save-like screenshots,
    and not realtime effects.
    """

    return renpy.game.interface.screenshot_to_bytes(size)



def transition(trans, layer=None, always=False, force=False):
    """
    :doc: other
    :args: (trans, layer=None, always=False)

    Sets the transition that will be used during the next interaction.

    `layer`
        The layer the transition applies to. If None, the transition
        applies to the entire scene.

    `always`
        If false, this respects the transition preference. If true, the
        transition is always run.
    """

    if isinstance(trans, dict):
        for ly, t in trans.items():
            transition(t, layer=ly, always=always, force=force)
        return

    if (not always) and not renpy.game.preferences.transitions: # type: ignore
        trans = None

    if renpy.config.skipping:
        trans = None

    renpy.game.interface.set_transition(trans, layer, force=force)


def get_transition(layer=None):
    """
    :doc: other

    Gets the transition for `layer`, or the entire scene if
    `layer` is None. This returns the transition that is queued up
    to run during the next interaction, or None if no such
    transition exists.

    Use :func:`renpy.get_ongoing_transition` to get the transition that is
    in progress.
    """

    return renpy.game.interface.transition.get(layer, None)


def get_ongoing_transition(layer=None):
    """
    :doc: other

    Returns the transition that is currently ongoing.

    `layer`
        If None, the top-level transition is returned. Otherwise, this should be a string giving a layer name,
        in which case the transition for that layer is returned.
    """

    return renpy.display.interface.get_ongoing_transition(layer)



def restart_interaction():
    """
    :doc: other

    Restarts the current interaction. Among other things, this displays
    images added to the scene, re-evaluates screens, and starts any
    queued transitions.

    This only does anything when called from within an interaction (for
    example, from an action). Outside an interaction, this function has
    no effect.
    """

    try:
        renpy.game.interface.restart_interaction = True
    except Exception:
        pass


def force_full_redraw():
    """
    :undocumented:

    Forces the screen to be redrawn in full. Call this after using pygame
    to redraw the screen directly.
    """

    # This had been used for the software renderer, but gl rendering redraws
    # the screen every frame, so it's removed.
    return


def image_size(im):
    """
    :doc: file_rare

    Given an image manipulator, loads it and returns a (``width``,
    ``height``) tuple giving its size.

    This reads the image in from disk and decompresses it, without
    using the image cache. This can be slow.
    """

    # Index the archives, if we haven't already.
    renpy.loader.index_archives()

    im = renpy.easy.displayable(im)

    if not isinstance(im, renpy.display.im.Image):
        raise Exception("renpy.image_size expects it's argument to be an image.")

    surf = im.load()
    return surf.get_size()


def get_at_list(name, layer=None):
    """
    :doc: se_images

    Returns the list of transforms being applied to the image with tag `name`
    on `layer`. Returns an empty list if no transforms are being applied, or
    None if the image is not shown.

    If `layer` is None, uses the default layer for the given tag.
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    tag = name[0]
    layer = default_layer(layer, tag)

    transforms = renpy.game.context().scene_lists.at_list[layer].get(tag, None)

    if transforms is None:
        return None

    return list(transforms)


def show_layer_at(at_list, layer='master', reset=True, camera=False):
    """
    :doc: se_images
    :name: renpy.show_layer_at

    The Python equivalent of the ``show layer`` `layer` ``at`` `at_list`
    statement. If `camera` is True, the equivalent of the ``camera`` statement.

    `reset`
        If true, the transform state is reset to the start when it is shown.
        If false, the transform state is persisted, allowing the new transform
        to update that state.
    """

    at_list = renpy.easy.to_list(at_list)

    renpy.game.context().scene_lists.set_layer_at_list(layer, at_list, reset=reset, camera=camera)


layer_at_list = show_layer_at


def free_memory():
    """
    :doc: other

    Attempts to free some memory. Useful before running a renpygame-based
    minigame.
    """

    force_full_redraw()
    renpy.display.interface.kill_textures()
    renpy.display.interface.kill_surfaces()
    renpy.text.font.free_memory()

    gc.collect(2)

    if gc.garbage:
        del gc.garbage[:]


def flush_cache_file(fn):
    """
    :doc: image_func

    This flushes all image cache entries that refer to the file `fn`.  This
    may be called when an image file changes on disk to force Ren'Py to
    use the new version.
    """

    renpy.display.im.cache.flush_file(fn)


@renpy_pure
def easy_displayable(d, none=False):
    """
    :undocumented:
    """

    if none:
        return renpy.easy.displayable(d)
    else:
        return renpy.easy.displayable_or_none(d)


def quit_event():
    """
    :doc: other

    Triggers a quit event, as if the player clicked the quit button in the
    window chrome.
    """

    renpy.game.interface.quit_event()


def iconify():
    """
    :doc: other

    Iconifies the game.
    """

    renpy.game.interface.iconify()


def timeout(seconds):
    """
    :doc: udd_utility

    Causes an event to be generated before `seconds` seconds have elapsed.
    This ensures that the event method of a user-defined displayable will be
    called.
    """

    renpy.game.interface.timeout(seconds)


def end_interaction(value):
    """
    :doc: udd_utility

    If `value` is not None, immediately ends the current interaction, causing
    the interaction to return `value`. If `value` is None, does nothing.

    This can be called from inside the render and event methods of a
    creator-defined displayable.
    """

    if value is None:
        return

    raise renpy.display.core.EndInteraction(value)


def shown_window():
    """
    :doc: other

    Call this to indicate that the window has been shown. This interacts
    with the "window show" statement, which shows an empty window whenever
    this functions has not been called during an interaction.
    """

    renpy.game.context().scene_lists.shown_window = True


class placement(renpy.revertable.RevertableObject):

    def __init__(self, p):
        super(placement, self).__init__()

        self.xpos = p[0]
        self.ypos = p[1]
        self.xanchor = p[2]
        self.yanchor = p[3]
        self.xoffset = p[4]
        self.yoffset = p[5]
        self.subpixel = p[6]

    @property
    def pos(self):
        return self.xpos, self.ypos

    @property
    def anchor(self):
        return self.xanchor, self.yanchor

    @property
    def offset(self):
        return self.xoffset, self.yoffset


def get_placement(d):
    """
    :doc: image_func

    This gets the placement of displayable d. There's very little warranty on this
    information, as it might change when the displayable is rendered, and might not
    exist until the displayable is first rendered.

    This returns an object with the following fields, each corresponding to a style
    property:

    * pos
    * xpos
    * ypos
    * anchor
    * xanchor
    * yanchor
    * offset
    * xoffset
    * yoffset
    * subpixel
    """
    p = d.get_placement()

    return placement(p)


def get_image_bounds(tag, width=None, height=None, layer=None):
    """
    :doc: image_func

    If an image with `tag` exists on `layer`, returns the bounding box of
    that image. Returns None if the image is not found.

    The bounding box is an (x, y, width, height) tuple. The components of
    the tuples are expressed in pixels, and may be floating point numbers.

    `width`, `height`
        The width and height of the area that contains the image. If None,
        defaults the width and height of the screen, respectively.

    `layer`
        If None, uses the default layer for `tag`.
    """

    tag = tag.split()[0]
    layer = default_layer(layer, tag)

    if width is None:
        width = renpy.config.screen_width
    if height is None:
        height = renpy.config.screen_height

    return scene_lists().get_image_bounds(layer, tag, width, height)

# User-Defined Displayable stuff.


Render = renpy.display.render.Render
render = renpy.display.render.render
IgnoreEvent = renpy.display.core.IgnoreEvent
redraw = renpy.display.render.redraw

def is_pixel_opaque(d, width, height, st, at, x, y):
    """
    :doc: udd_utility

    Returns whether the pixel at (x, y) is opaque when this displayable
    is rendered by ``renpy.render(d, width, height, st, at)``.
    """

    # Uses the caching features of renpy.render, as opposed to d.render.
    return bool(render(renpy.easy.displayable(d), width, height, st, at).is_pixel_opaque(x, y))


class Displayable(renpy.display.displayable.Displayable, renpy.revertable.RevertableObject):
    pass


class Container(renpy.display.layout.Container, renpy.revertable.RevertableObject):
    _list_type = renpy.revertable.RevertableList


def get_renderer_info():
    """
    :doc: other

    Returns a dictionary, giving information about the renderer Ren'Py is
    currently using. Defined keys are:

    ``"renderer"``
        A string giving the name of the renderer that is in use.

    ``"resizable"``
        True if and only if the window is resizable.

    ``"additive"``
        True if and only if the renderer supports additive blending.

    ``"model"``
        Present and true if model-based rendering is supported.

    Other, renderer-specific, keys may also exist. The dictionary should
    be treated as immutable. This should only be called once the display
    has been started (that is, after the init phase has finished).
    """

    return renpy.display.draw.info


def display_reset():
    """
    :undocumented: Used internally.

    Causes the display to be restarted at the start of the next interaction.
    """

    renpy.display.interface.display_reset = True


def get_physical_size():
    """
    :doc: other

    Returns the size of the physical window.
    """

    return renpy.display.draw.get_physical_size()


def set_physical_size(size):
    """
    :doc: other

    Attempts to set the size of the physical window to `size`. This has the
    side effect of taking the screen out of fullscreen mode.
    """

    width = int(size[0])
    height = int(size[1])

    renpy.game.preferences.fullscreen = False # type: ignore

    if get_renderer_info()["resizable"]:

        renpy.game.preferences.physical_size = (width, height) # type: ignore

        if renpy.display.draw is not None:
            renpy.display.draw.resize()


def reset_physical_size():
    """
    :doc: other

    Attempts to set the size of the physical window to the size specified
    using :var:`renpy.config.physical_height` and :var:`renpy.config.physical_width`,
    or the size set using :var:`renpy.config.screen_width` and :var:`renpy.config.screen_height`
    if not set.
    """

    set_physical_size((renpy.config.physical_width or renpy.config.screen_width, renpy.config.physical_height or renpy.config.screen_height))


def get_image_load_log(age=None):
    """
    :doc: other

    A generator that yields a log of image loading activity. For the last 100
    image loads, this returns:

    * The time the image was loaded (in seconds since the epoch).
    * The filename of the image that was loaded.
    * A boolean that is true if the image was preloaded, and false if the
      game stalled to load it.

    The entries are ordered from newest to oldest.

    `age`
        If not None, only images that have been loaded in the past `age`
        seconds are included.

    The image load log is only kept if config.developer = True.
    """

    if age is not None:
        deadline = time.time() - age
    else:
        deadline = 0

    for i in renpy.display.im.cache.load_log:
        if i[0] < deadline:
            break

        yield i


def get_mouse_pos():
    """
    :doc: other

    Returns an (x, y) tuple giving the location of the mouse pointer or the
    current touch location. If the device does not support a mouse and is not
    currently being touched, x and y are numbers, but not meaningful.
    """
    return renpy.display.draw.get_mouse_pos()


def set_mouse_pos(x, y, duration=0):
    """
    :doc: other

    Jump the mouse pointer to the location given by arguments x and y.
    If the device does not have a mouse pointer, this does nothing.

    `duration`
        The time it will take to perform the move, in seconds.
        During this time, the mouse may be unresponsive.
    """

    renpy.display.interface.set_mouse_pos(x, y, duration)


def cancel_gesture():
    """
    :doc: gesture

    Cancels the current gesture, preventing the gesture from being recognized.
    This should be called by displayables that have gesture-like behavior.
    """

    renpy.display.gesture.recognizer.cancel() # @UndefinedVariable


def add_layer(layer, above=None, below=None, menu_clear=True, sticky=None):
    """
    :doc: image_func

    Adds a new layer to the screen. If the layer already exists, this
    function does nothing.

    One of `behind` or `above` must be given.

    `layer`
        A string giving the name of the new layer to add.

    `above`
        If not None, a string giving the name of a layer the new layer will
        be placed above.

    `below`
        If not None, a string giving the name of a layer the new layer will
        be placed below.

    `menu_clear`
        If true, this layer will be cleared when entering the game menu
        context, and restored when leaving it.

    `sticky`
        If true, any tags added to this layer will have it become their
        default layer until they are hidden. If None, this layer will be
        sticky only if other sticky layers already exist.
    """

    layers = renpy.config.layers

    if layer in renpy.config.layers:
        return

    if (above is not None) and (below is not None):
        raise Exception("The above and below arguments to renpy.add_layer are mutually exclusive.")

    elif above is not None:
        try:
            index = layers.index(above) + 1
        except ValueError:
            raise Exception("Layer '%s' does not exist." % above)

    elif below is not None:
        try:
            index = layers.index(below)
        except ValueError:
            raise Exception("Layer '%s' does not exist." % below)

    else:
        raise Exception("The renpy.add_layer function requires either the above or below argument.")

    layers.insert(index, layer)

    if menu_clear:
        renpy.config.menu_clear_layers.append(layer) # type: ignore # Set in 00gamemenu.rpy.

    if sticky or sticky is None and renpy.config.sticky_layers:
        renpy.config.sticky_layers.append(layer)


def maximum_framerate(t):
    """
    :doc: other

    Forces Ren'Py to draw the screen at the maximum framerate for `t` seconds.
    If `t` is None, cancels the maximum framerate request.
    """

    if renpy.display.interface is not None:
        renpy.display.interface.maximum_framerate(t)
    else:
        if t is None:
            renpy.display.core.initial_maximum_framerate = 0
        else:
            renpy.display.core.initial_maximum_framerate = max(renpy.display.core.initial_maximum_framerate, t)


def is_start_interact():
    """
    :doc: other

    Returns true if restart_interaction has not been called during the current
    interaction. This can be used to determine if the interaction is just being
    started, or has been restarted.
    """

    return renpy.display.interface.start_interact


def get_refresh_rate(precision=5):
    """
    :doc: other

    Returns the refresh rate of the current screen, as a floating-point
    number of frames per second.

    `precision`
        The raw data Ren'Py gets is the number of frames per second rounded down
        to the nearest integer. This means that a monitor that runs at 59.95
        frames per second will be reported at 59 fps. The precision argument
        then further reduces the precision of this reading, such that the only valid
        readings are multiples of the precision.

        Since all monitor framerates tend to be multiples of 5 (25, 30, 60,
        75, and 120), this likely will improve accuracy. Setting precision
        to 1 disables this.
    """

    if PY2:
        precision = float(precision)

    info = renpy.display.get_info()
    rv = info.refresh_rate # type: ignore
    rv = round(rv / precision) * precision

    return rv


def get_adjustment(bar_value):
    """
    :doc: screens

    Given `bar_value`, a :class:`BarValue`, returns the :func:`ui.adjustment`
    it uses. The adjustment has the following attributes defined:

    .. attribute:: value

        The current value of the bar.

    .. attribute:: range

        The current range of the bar.
    """

    return bar_value.get_adjustment()


def get_texture_size():
    """
    :undocumented:

    Returns the number of bytes of memory locked up in OpenGL textures and the
    number of textures that are defined.
    """

    return renpy.display.draw.get_texture_size()


def get_zorder_list(layer):
    """
    :doc: image_func

    Returns a list of (tag, zorder) pairs for `layer`.
    """

    return scene_lists().get_zorder_list(layer)


def change_zorder(layer, tag, zorder):
    """
    :doc: image_func

    Changes the zorder of `tag` on `layer` to `zorder`.
    """

    return scene_lists().change_zorder(layer, tag, zorder)


def is_mouse_visible():
    """
    :doc: other

    Returns True if the mouse cursor is visible, False otherwise.
    """

    if not renpy.display.interface:
        return True

    if not renpy.display.interface.mouse_focused:
        return False

    return renpy.display.interface.is_mouse_visible()


def get_mouse_name(interaction=False):
    """
    :doc: other

    Returns the name of the mouse that should be shown.


    `interaction`
        If true, get a mouse name that is based on the type of interaction
        occuring. (This is rarely useful.)
    """

    if not renpy.display.interface:
        return 'default'

    return renpy.display.interface.get_mouse_name(interaction=interaction)


def set_focus(screen, id, layer="screens"): # @ReservedAssignment
    """
    :doc: screens

    This attempts to focus the displayable with `id` in the screen `screen`.
    Focusing will fail if the displayable isn't found, the window isn't
    focused, or something else is grabbing focus.

    The focus may change if the mouse moves, even slightly, after this call
    is processed.
    """

    renpy.display.focus.override = (screen, id, layer)
    renpy.display.interface.last_event = None
    restart_interaction()


def clear_retain(layer="screens", prefix="_retain"):
    """
    :doc: other

    Clears all retained screens
    """

    for i in get_showing_tags(layer):
        if i.startswith(prefix):
            renpy.exports.hide_screen(i)


def can_fullscreen():
    """
    :doc: other

    Returns True if the current platform supports fullscreen mode, False
    otherwise.
    """

    return renpy.display.can_fullscreen


def render_to_surface(d, width=None, height=None, st=0.0, at=None, resize=False):
    """
    :doc: screenshot

    This takes a displayable or Render, and returns a pygame_sdl2 surface. The render is performed by
    Ren'Py's display system, such that if the window is upscaled the render will be upscaled as well.

    `d`
        The displayable or Render to render. If a Render, `width`, `height`, `st`, and `at` are ignored.

    `width`
        The width to offer `d`, in virtual pixesl. If None, :var:`config.screen_width`.

    `height`
        The height to offer `d`, in virtual pixels. If None, :var:`config.screen_height`.

    `st`
        The time of the render, in the shown timebase.

    `at`
        The time of the rendem in the animation timebase. If None, `st` is used.

    `resize`
        If True, the surface will be resized to the virtual size of the displayable or render. This
        may lower the quality of the result.

    This function may only be called after the Ren'Py display system has started, so it can't be
    called during the init phase or before the first interaction.
    """

    if width is None:
        width = renpy.config.screen_width

    if height is None:
        height = renpy.config.screen_height

    if at is None:
        at = st


    if not isinstance(d, Render):
        d = renpy.easy.displayable(d)
        d = renpy.display.render.render(d, width, height, st, at)

    rv = renpy.display.draw.screenshot(d)

    if resize:
        return renpy.display.scale.smoothscale(rv, (d.width, d.height))
    else:
        return rv


def render_to_file(d, filename, width=None, height=None, st=0.0, at=None, resize=False):
    """
    :doc: screenshot

    Renders a displayable or Render, and saves the result of that render to a file. The render is performed by
    Ren'Py's display system, such that if the window is upscaled the render will be upscaled as well.

    `d`
        The displayable or Render to render. If a Render, `width`, `height`, `st`, and `at` are ignored.

    `filename`
        A string, giving the name of the file to save the render to. This is interpreted as relative
        to the base directory. This must end with .png.

    `width`
        The width to offer `d`, in virtual pixesl. If None, :var:`config.screen_width`.

    `height`
        The height to offer `d`, in virtual pixels. If None, :var:`config.screen_height`.

    `st`
        The time of the render, in the shown timebase.

    `at`
        The time of the rendem in the animation timebase. If None, `st` is used.

    `resize`
        If True, the image will be resized to the virtual size of the displayable or render. This
        may lower the quality of the result.

    This function may only be called after the Ren'Py display system has started, so it can't be
    called during the init phase or before the first interaction.

    Ren'Py not rescan files while the game is running, so this shouldn't be used to sythesize
    assets that are used as part of the game.
    """

    filename = os.path.join(renpy.config.basedir, filename)
    surface = render_to_surface(d, width, height, st, at, resize)
    pygame_sdl2.image.save(surface, filename)
