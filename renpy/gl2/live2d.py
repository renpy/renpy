# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *

import renpy.display
import renpy.gl2.live2dmotion
from renpy.gl2.gl2shadercache import register_shader

try:
    import renpy.gl2.live2dmodel as live2dmodel
except ImportError:
    live2dmodel = None

import json
import collections

did_onetime_init = False


def onetime_init():
    global did_onetime_init

    if did_onetime_init:
        return

    did_onetime_init = True

    if renpy.windows:
        dll = "Live2DCubismCore.dll"
    elif renpy.macintosh:
        dll = "libLive2DCubismCore.dylib"
    else:
        dll = "libLive2DCubismCore.so"

    if not renpy.gl2.live2dmodel.load(dll):
        raise Exception("Could not load Live2D. {} was not found.".format(dll))


did_init = False


def init():
    """
    Called to initialize Live2D, if needed.
    """

    global did_init

    if did_init:
        return

    if live2dmodel is None:
        raise Exception("Live2D has not been built.")

    if not renpy.config.gl2:
        raise Exception("Live2D requires that config.gl2 be True.")

    onetime_init()

    register_shader("live2d.mask", variables="""
        uniform sampler2D uTex0;
        uniform sampler2D uTex1;
        attribute vec4 vPosition;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
        varying vec2 vMaskCoord;
    """, vertex_110="""
        vTexCoord = aTexCoord;
        vMaskCoord = vec2(aPosition.x / 2 + .5, -aPosition.y / 2 + .5);
    """, fragment_110="""
        vec4 color = texture2D(uTex0, vTexCoord);
        vec4 mask = texture2D(uTex1, vMaskCoord);
        gl_FragColor = color * mask.a;
    """)

    register_shader("live2d.inverted_mask", variables="""
        uniform sampler2D uTex0;
        uniform sampler2D uTex1;
        attribute vec4 vPosition;
        attribute vec2 aTexCoord;
        varying vec2 vTexCoord;
        varying vec2 vMaskCoord;
    """, vertex_110="""
        vTexCoord = aTexCoord;
        vMaskCoord = vec2(aPosition.x / 2 + .5, -aPosition.y / 2 + .5);
    """, fragment_110="""
        vec4 color = texture2D(uTex0, vTexCoord);
        vec4 mask = texture2D(uTex1, vMaskCoord);
        gl_FragColor = color * (1.0 - mask.a);
    """)

    register_shader("live2d.flip_texture", variables="""
        varying vec2 vTexCoord;
    """, vertex_120="""
        vTexCoord.y = 1.0 - vTexCoord.y;
    """)

    renpy.config.interact_callbacks.append(update_states)

    did_init = True


def reset():
    """
    Resets this module when Ren'Py restarts.
    """

    global did_init
    did_init = False

    common_cache.clear()
    states.clear()


class Live2DCommon(object):
    """
    This object stores information that is common to all of the Live2D
    displayables that use the same .model3.json file, so this information
    only needs to be loaded once. This should not leak into the save games,
    but is loaded at init time.
    """

    def __init__(self, filename):

        init()

        # If a directory is given rather than a json file, expand it.
        if not filename.endswith(".json"):
            suffix = filename.rpartition("/")[2]
            filename = filename + "/" + suffix + ".model3.json"

        renpy.display.log.write("Loading Live2D from %r.", filename)

        if not renpy.loader.loadable(filename):
            raise Exception("Live2D model {} does not exist.".format(filename))

        # A short name for the model.
        model_name = filename.rpartition("/")[2].partition(".")[0].lower()

        # The path to where the files used are stored.
        self.base = filename.rpartition("/")[0]

        if self.base:
            self.base += "/"

        # The contents of the .model3.json file.
        self.model_json = json.load(renpy.loader.load(filename))

        # The model created from the moc3 file.
        self.model = renpy.gl2.live2dmodel.Live2DModel(self.base + self.model_json["FileReferences"]["Moc"])

        # The texture images.
        self.textures = [ ]

        for i in self.model_json["FileReferences"]["Textures"]:
            self.textures.append(renpy.easy.displayable(self.base + i))

        # The motion information.
        self.motions = { }

        def walk_json_files(o, l):
            if isinstance(o, list):
                for i in o:
                    walk_json_files(i, l)
                return

            if "File" in o:
                l.append(o)
                return

            for i in o.values():
                walk_json_files(i, l)

        motion_files = [ ]
        walk_json_files(self.model_json["FileReferences"].get("Motions", { }), motion_files)

        # A list of attributes that are known.
        self.attributes = set()

        # A map from a motion name to a motion identifier.
        self.motions = { "still" : renpy.gl2.live2dmotion.NullMotion() }

        for i in motion_files:
            name = i["File"].lower().rpartition("/")[2].partition(".")[0]

            prefix, _, suffix = name.partition("_")

            if prefix == model_name:
                name = suffix

            if renpy.loader.loadable(self.base + i["File"]):
                renpy.display.log.write(" - motion %s -> %s", name, i["File"])

                self.motions[name] = renpy.gl2.live2dmotion.Motion(
                    self.base + i["File"],
                    i.get("FadeInTime", 0.0),
                    i.get("FadeOutTime", 0.0))

                self.attributes.add(name)

    def apply_aliases(self, aliases):

        for k, v in aliases.items():
            if v in self.motions:
                self.motions[k] = self.motions[v]


# This maps a filename to a Live2DCommon object.
common_cache = { }


class Live2DState(object):

    def __init__(self):

        # Used to mark this state as having been seen in the current
        # iteration.
        self.mark = False

        # Should we cycle new into old?
        self.cycle_new = False

        # The displayable in the old and new state. Both can be None if
        # it's not being shown.
        self.old = None
        self.new = None

        # The time at which the old and new displayables were last updated.
        self.old_base_time = 0
        self.new_base_time = 0


# A map from name to Live2DState object.
states = collections.defaultdict(Live2DState)


def update_states():
    """
    Called once per interact to walk the tree of
    """

    def visit(d):
        if not isinstance(d, Live2D):
            return

        if d.name is None:
            return

        state = states[d.name]

        if state.mark:
            return

        state.mark = True

        if state.new is d:
            return

        # Shouldn't happen, but stop thrashing if it does.
        if state.old is d:
            return

        if state.cycle_new:
            state.old = state.new
            state.old_base_time = state.new_base_time
        else:
            state.old = None
            state.old_base_time = None

        state.new = d
        state.new_base_time = None
        state.cycle_new = True

    sls = renpy.display.core.scene_lists()

    for d in sls.get_all_displayables(current=True):
        if d is not None:
            d.visit_all(visit)

    for s in states.values():
        if not s.mark:
            s.cycle_new = False

        s.mark = False


class Live2D(renpy.display.core.Displayable):

    nosave = [ "common_cache" ]

    common_cache = None
    _duplicatable = True

    @property
    def common(self):
        if self.common_cache is not None:
            return self.common_cache

        rv = common_cache.get(self.filename, None)

        if rv is None:
            rv = Live2DCommon(self.filename)
            common_cache[self.filename] = rv

        self.common_cache = rv
        return rv

    # Note: When adding new parameters, make sure to add them to _duplicate, too.
    def __init__(self, filename, zoom=None, top=0.0, base=1.0, height=1.0, loop=False, aliases={}, fade=None, motions=None, **properties):

        super(Live2D, self).__init__(**properties)

        self.filename = filename
        self.motions = motions

        self.zoom = zoom
        self.top = top
        self.base = base
        self.height = height
        self.loop = loop
        self.fade = fade

        # The name of this displayable.
        self.name = None

        # Load the common data. Needed!
        common = self.common

        if aliases:
            common.apply_aliases(aliases)

    def _duplicate(self, args):

        if not self._duplicatable:
            return self

        common = self.common
        motions = [ ]

        for i in args.args:

            if i in common.motions:
                motions.append(i)
                continue

            raise Exception("When showing {}, {} is not a known attribute.".format(" ".join(args.name), i))

        rv = Live2D(
            self.filename,
            motions=motions,
            zoom=self.zoom,
            top=self.top,
            base=self.base,
            height=self.height,
            loop=self.loop,
            fade=self.fade)

        rv._duplicatable = False
        rv.name = args.name
        return rv

    def _list_attributes(self, tag, attributes):

        common = self.common

        available = set(common.attributes)

        # Todo: Expressions

        available |= set(attributes)

        return [ i for i in common.attributes if i in available ]

    def _choose_attributes(self, tag, attributes, optional):

        common = self.common

        motions = [ i for i in optional if i in common.motions ]

        if not motions:
            motions = [ i for i in optional if i in common.motions ][:-1]

        return tuple(motions)

    def update(self, common, st, st_fade):
        """
        This updates the common model with the infromation taken from the
        motions associated with this object. It returns the delay until
        Ren'Py needs to cause a redraw to occur, or None if no delay
        should occur.
        """

        if not self.motions:
            return

        for m in self.motions:
            motion = common.motions.get(m, None)

            if motion.duration > st:
                break

            st -= motion.duration

        else:
            if not self.loop:
                st = motion.duration

        if motion is None:
            return None

        motion_data = motion.get(st, st_fade)

        for k, v in motion_data.items():

            kind, key = k
            factor, value = v

            if kind == "Parameter":
                common.model.set_parameter(key, value, factor)
            else:
                common.model.set_part_opacity(key, value)

        return motion.wait(st, st_fade)

    def render(self, width, height, st, at):

        common = self.common
        model = common.model

        # Determine if we should fade.
        fade = self.fade if (self.fade is not None) else renpy.store._live2d_fade

        if not self.name:
            fade = False

        if fade:

            state = states[self.name]

            if state.new is not self:
                fade = False

            state.new_base_time = renpy.display.interface.frame_time - st

            if state.old is None:
                fade = False

            if state.old_base_time is None:
                fade = False

        if fade:

            if state.old.common is not self.common:
                fade = False

        # Reset the parameter, and update.
        common.model.reset_parameters()

        if fade:
            old_redraw = state.old.update(common, renpy.display.interface.frame_time - state.old_base_time, st)
        else:
            old_redraw = None

        new_redraw = self.update(common, st, None)

        # Apply the redraws.
        if (new_redraw is not None) and (old_redraw is not None):
            renpy.display.render.redraw(self, min(new_redraw, old_redraw))
        elif new_redraw is not None:
            renpy.display.render.redraw(self, new_redraw)
        elif old_redraw is not None:
            renpy.display.render.redraw(self, old_redraw)

        # Render the textures.
        textures = [ renpy.display.render.render(d, width, height, st, at) for d in common.textures ]

        # Render the model.
        rend = model.render(textures)

        # Figure out zoom.
        sw, sh = rend.get_size()

        zoom = self.zoom

        def s(n):
            if isinstance(n, float):
                return n * sh
            else:
                return n

        if zoom is None:
            top = s(self.top)
            base = s(self.base)

            size = max(base - top, 1.0)
            zoom = 1.0 * self.height * renpy.config.screen_height / size
        else:
            size = sh
            top = 0

        # Apply scaling as needed.
        rv = renpy.exports.Render(sw * zoom, size * zoom)
        rv.blit(rend, (0, -top * zoom))

        if zoom != 1.0:
            rv.reverse = renpy.display.matrix.Matrix.scale(zoom, zoom, 1.0)
            rv.forward = renpy.display.matrix.Matrix.scale(1 / zoom, 1 / zoom, 1.0)

        return rv

    def visit(self):
        return self.common.textures


def has_live2d():
    """
    :doc: live2d

    Returns True if Live2d is supported on the current platform, and
    False otherwise.
    """

    try:
        init()
        return True
    except:
        return False
