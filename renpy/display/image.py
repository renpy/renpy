# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains some miscellaneous displayables that involve images.
# Most of the guts of this file have been moved into im.py, with only some
# of the stuff thar uses images remaining.

import renpy.display
import renpy.text
from renpy.display.render import render, Render

import collections

# A map from image name to the displayable object corresponding to that
# image.
images = { }

# A map from image tag to lists of possible attributes for images with that
# tag.
image_attributes = collections.defaultdict(list)


def register_image(name, d):
    """
    Registers the existence of an image with `name`, and that the image
    used displayable d.

    `name`
        A tuple of strings.
    """

    tag = name[0]
    rest = name[1:]

    images[name] = d
    image_attributes[tag].append(rest)


def image_exists(name, exact=False):
    """
    :doc: image_func
    :name: renpy.has_image

    Return true if an image with `name` exists, and false if no such image
    exists.

    `name`
        Either a string giving an image name, or a tuple of strings giving
        the name components.

    `exact`
        Returns true if and only if an image with the exact name exists -
        parameterized matches are not included.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    while name:
        if name in images:
            return True

        if exact:
            return False

        name = name[:-1]

    return False


def wrap_render(child, w, h, st, at):
    rend = render(child, w, h, st, at)
    rv = Render(rend.width, rend.height)
    rv.blit(rend, (0, 0))
    return rv


class ImageReference(renpy.display.core.Displayable):
    """
    ImageReference objects are used to reference images by their name,
    which is a tuple of strings corresponding to the name used to define
    the image in an image statment.
    """

    nosave = [ 'target', 'param_target' ]
    target = None
    param_target = None

    def __init__(self, name, **properties):
        """
        @param name: A tuple of strings, the name of the image. Or else
        a displayable, containing the image directly.
        """

        super(ImageReference, self).__init__(**properties)

        self.name = name

    def __unicode__(self):
        return u"<ImageReference {!r}>".format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o):
        if self is o:
            return True

        if not self._equals(o):
            return False

        if self.name != o.name:
            return False

        return True

    def _get_parameterized(self):
        if self.param_target:
            return self.param_target._get_parameterized()

        return self

    def find_target(self):

        if self.param_target:
            self.target = self.param_target
            return None

        name = self.name

        if isinstance(name, renpy.display.core.Displayable):
            self.target = name
            return True

        if not isinstance(name, tuple):
            name = tuple(name.split())

        parameters = [ ]

        def error(msg):
            self.target = renpy.text.text.Text(msg, color=(255, 0, 0, 255), xanchor=0, xpos=0, yanchor=0, ypos=0)

            if renpy.config.debug:
                raise Exception(msg)


        # Scan through, searching for an image (defined with an
        # input statement) that is a prefix of the given name.
        while name:
            if name in images:
                target = images[name]

                try:
                    self.target = target.parameterize(name, parameters)
                    if self.target is not target:
                        self.param_target = self.target

                except Exception, e:
                    if renpy.config.debug:
                        raise

                    error(str(e))

                return True

            else:
                parameters.insert(0, name[-1])
                name = name[:-1]

        error("Image '%s' not found." % ' '.join(self.name))
        return False

    def parameterize(self, name, parameters):
        if not self.target:
            self.find_target()

        return self.target.parameterize(name, parameters)

    def _hide(self, st, at, kind):
        if not self.target:
            self.find_target()

        return self.target._hide(st, at, kind)

    def set_transform_event(self, event):
        if not self.target:
            self.find_target()

        return self.target.set_transform_event(event)

    def event(self, ev, x, y, st):
        if not self.target:
            self.find_target()

        return self.target.event(ev, x, y, st)

    def render(self, width, height, st, at):
        if not self.target:
            self.find_target()

        return wrap_render(self.target, width, height, st, at)

    def get_placement(self):
        if not self.target:
            self.find_target()

        if not renpy.config.imagereference_respects_position:
            return self.target.get_placement()

        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = self.target.get_placement()

        if xpos is None:
            xpos = self.style.xpos

        if ypos is None:
            ypos = self.style.ypos

        if xanchor is None:
            xanchor = self.style.xanchor

        if yanchor is None:
            yanchor = self.style.yanchor

        return xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel

    def visit(self):
        if not self.target:
            self.find_target()

        return [ self.target ]


class DynamicImage(renpy.display.core.Displayable):
    """
    :doc: disp_imagelike
    :args: (name)

    A DynamicImage is a displayable that has text interpolation performed
    on it to yield a string giving a new displayable. Such interpolation is
    performed at the start of each iteraction.
    """

    nosave = [ 'target', 'raw_target' ]

    # The target that this image currently resolves to.
    target = None

    # The raw target that the image resolves to, before it has been parameterized.
    raw_target = None

    def __init__(self, name, scope=None, **properties):
        super(DynamicImage, self).__init__(**properties)

        self.name = name

        if scope is not None:
            self.find_target(scope)
            self._uses_scope = True
        else:
            self._uses_scope = False

    def _scope(self, scope, update):
        return self.find_target(scope, update)

    def __unicode__(self):
        return u"DynamicImage {!r}".format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o):
        if self is o:
            return True

        if not self._equals(o):
            return False

        if self.name != o.name:
            return False

        return True

    def _get_parameterized(self):
        if self.target:
            return self.target._get_parameterized()
        else:
            return self

    def find_target(self, scope=None, update=True):

        try:
            target = renpy.easy.dynamic_image(self.name, scope)
        except Exception as e:
            raise Exception("In DynamicImage %r: %r" % (self.name, e))

        if self.raw_target == target:
            return False

        if not update:
            return True

        renpy.display.render.redraw(self, 0)
        self.raw_target = target

        target = target.parameterize('displayable', ())
        old_target = self.target
        self.target = target

        if not old_target:
            return True

        if isinstance(old_target, renpy.display.motion.Transform):
            return True

        if not isinstance(target, renpy.display.motion.Transform):
            self.target = target = renpy.display.motion.Transform(child=target)

        target.take_state(old_target)

        return True

    def _hide(self, st, at, kind):
        if not self.target:
            self.find_target()

        return self.target._hide(st, at, kind)

    def set_transform_event(self, event):
        if not self.target:
            self.find_target()

        return self.target.set_transform_event(event)

    def event(self, ev, x, y, st):
        if not self.target:
            self.find_target()

        return self.target.event(ev, x, y, st)

    def render(self, width, height, st, at):
        if not self.target:
            self.find_target()

        return wrap_render(self.target, width, height, st, at)

    def get_placement(self):
        if not self.target:
            self.find_target()

        return self.target.get_placement()

    def visit(self):
        if not self.target:
            self.find_target()

        return [ self.target ]

    def per_interact(self):
        old_target = self.target

        if not self._uses_scope:
            self.find_target()

        if old_target is not self.target:
            self.target.visit_all(lambda i : i.per_interact())


class ShownImageInfo(renpy.object.Object):
    """
    This class keeps track of which images are being shown right now,
    and what the attributes of those images are. (It's used for a similar
    purpose during prediction, regarding the state in the future.)
    """

    __version__ = 2

    def __init__(self, old=None):
        """
        Creates a new object. If `old` is given, copies the default state
        from old, otherwise initializes the object to a default state.
        """

        if old is None:

            # A map from (layer, tag) -> tuple of attributes
            # This doesn't necessarily correspond to something that is
            # currently showing, as we can remember the state of a tag
            # for use in SideImage.
            self.attributes = { }

            # A set of (layer, tag) pairs that are being shown on the
            # screen right now.
            self.shown = set()

        else:
            self.attributes = old.attributes.copy()
            self.shown = old.shown.copy()


    def after_upgrade(self, version):
        if version < 2:

            self.attributes = { }
            self.shown = set()

            for layer in self.images:
                for tag in self.images[layer]:
                    self.attributes[layer, tag] = self.images[layer][tag][1:]
                    self.shown.add((layer, tag))

    def get_attributes(self, layer, tag):
        """
        Get the attributes associated the image with tag on the given
        layer.
        """

        return self.attributes.get((layer, tag), ())

    def showing(self, layer, name):
        """
        Returns true if name is the prefix of an image that is showing
        on layer, or false otherwise.
        """

        tag = name[0]
        rest = name[1:]

        if (layer, tag) not in self.shown:
            return None

        shown = self.attributes[layer, tag]

        if len(shown) < len(rest):
            return False

        for a, b in zip(shown, rest):
            if a != b:
                return False

        return True

    def get_showing_tags(self, layer):
        """
        Returns the set of tags being shown on `layer`.
        """

        return { t for l, t in self.shown if l == layer }

    def predict_scene(self, layer):
        """
        Predicts the scene statement being called on layer.
        """

        for l, t in self.attributes.keys():
            if l == layer:
                del self.attributes[l, t]

        self.shown = set((l, t) for l, t in self.shown if l != layer)

    def predict_show(self, layer, name, show=True):
        """
        Predicts name being shown on layer.

        `show`
            If True, the image will be flagged as being shown to the user. If
            False, only the attributes will be updated.
        """

        tag = name[0]
        rest = name[1:]

        self.attributes[layer, tag] = rest

        if show:
            self.shown.add((layer, tag))

    def predict_hide(self, layer, name):
        tag = name[0]

        if (layer, tag) in self.attributes:
            del self.attributes[layer, tag]

        self.shown.discard((layer, tag))


    def apply_attributes(self, layer, tag, name):
        """
        Given a layer, tag, and an image name (with attributes),
        returns the canonical name of an image, if one exists. Raises
        an exception if it's ambiguious, and returns None if an image
        with that name couldn't be found.
        """

        # If the name matches one that exactly exists, return it.
        if name in images:
            return name

        nametag = name[0]

        # The set of attributes a matching image must have.
        required = set(name[1:])

        # The set of attributes a matching image may have.
        optional = set(self.attributes.get((layer, tag), [ ]))

        # Deal with banned attributes..
        for i in name[1:]:
            if i[0] == "-":
                optional.discard(i[1:])
                required.discard(i)

        return self.choose_image(nametag, required, optional, name)

    def choose_image(self, tag, required, optional, exception_name):
        """
        """

        # The longest length of an image that matches.
        max_len = 0

        # The list of matching images.
        matches = None

        for attrs in image_attributes[tag]:

            num_required = 0

            for i in attrs:
                if i in required:
                    num_required += 1
                    continue

                elif i not in optional:
                    break

            else:

                # We don't have any not-found attributes. But we might not
                # have all of the attributes.

                if num_required != len(required):
                    continue

                len_attrs = len(set(attrs))

                if len_attrs < max_len:
                    continue

                if len_attrs > max_len:
                    max_len = len_attrs
                    matches = [ ]

                matches.append((tag, ) + attrs)

        if matches is None:
            return None

        if len(matches) == 1:
            return matches[0]

        if exception_name:
            raise Exception("Showing '" + " ".join(exception_name) + "' is ambiguous, possible images include: " + ", ".join(" ".join(i) for i in matches))
        else:
            return None

renpy.display.core.ImagePredictInfo = ShownImageInfo


# Functions that have moved from this module to other modules,
# that live here for the purpose of backward-compatibility.
Image = renpy.display.im.image
Solid = renpy.display.imagelike.Solid
Frame = renpy.display.imagelike.Frame
ImageButton = renpy.display.behavior.ImageButton

