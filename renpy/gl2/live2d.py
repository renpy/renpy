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

import sys
import os
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

    fn = os.path.join(os.path.dirname(sys.executable), dll)
    if os.path.exists(fn):
        dll = fn

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
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        attribute vec4 a_position;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        varying vec2 v_mask_coord;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
        v_mask_coord = vec2(a_position.x / 2.0 + .5, -a_position.y / 2.0 + .5);
    """, fragment_200="""
        vec4 color = texture2D(tex0, v_tex_coord);
        vec4 mask = texture2D(tex1, v_mask_coord);
        gl_FragColor = color * mask.a;
    """)

    register_shader("live2d.inverted_mask", variables="""
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        attribute vec4 a_position;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        varying vec2 v_mask_coord;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
        v_mask_coord = vec2(a_position.x / 2.0 + .5, -a_position.y / 2.0 + .5);
    """, fragment_200="""
        vec4 color = texture2D(tex0, v_tex_coord);
        vec4 mask = texture2D(tex1, v_mask_coord);
        gl_FragColor = color * (1.0 - mask.a);
    """)

    register_shader("live2d.flip_texture", variables="""
        varying vec2 v_tex_coord;
    """, vertex_250="""
        v_tex_coord.y = 1.0 - v_tex_coord.y;
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
        with renpy.loader.load(filename) as f:
            self.model_json = json.load(f)

        # The model created from the moc3 file.
        self.model = renpy.gl2.live2dmodel.Live2DModel(self.base + self.model_json["FileReferences"]["Moc"])

        # The texture images.
        self.textures = [ ]

        for i in self.model_json["FileReferences"]["Textures"]:
            self.textures.append(renpy.easy.displayable(self.base + i))

        # A map from the motion file name to the information about it.
        motion_files = { }

        # A map from the expression name to the information about it.
        expression_files = { }

        motions_dir = self.base + "motions/"
        expressions_dir = self.base + "expressions/"

        for i in renpy.exports.list_files():
            if i.startswith(motions_dir):
                i = i[len(self.base):]
                motion_files[i] = { "File" : i }

            elif i.startswith(expressions_dir):
                i = i[len(self.base):]
                expression_files[i] = { "File" : i }

        def walk_json_files(o, d):
            if isinstance(o, list):
                for i in o:
                    walk_json_files(i, d)
                return

            if "File" in o:
                d[o["File"]] = o
                return

            for i in o.values():
                walk_json_files(i, d)

        walk_json_files(self.model_json["FileReferences"].get("Motions", { }), motion_files)
        walk_json_files(self.model_json["FileReferences"].get("Expressions", { }), expression_files)

        # A list of attributes that are known.
        self.attributes = set([ "still", "null" ])

        # A map from a motion name to a motion identifier.
        self.motions = { "still" : renpy.gl2.live2dmotion.NullMotion() }

        for i in motion_files.values():
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

        # A map from an expression to that expression's parameter list.
        self.expressions = { "null" : [ ] }

        for i in expression_files.values():
            name = i["File"].lower().rpartition("/")[2].partition(".")[0]

            prefix, _, suffix = name.partition("_")

            if prefix == model_name:
                name = suffix

            if renpy.loader.loadable(self.base + i["File"]):
                renpy.display.log.write(" - expression %s -> %s", name, i["File"])

                if name in self.attributes:
                    raise Exception("Name {!r} is already specified as a motion.".format(name))

                with renpy.loader.load(self.base + i["File"]) as f:
                    expression_json = json.load(f)

                self.expressions[name] = expression_json.get("Parameters", [ ])

                self.attributes.add(name)

        for i in self.model_json.get("Groups", [ ]):
            name = i["Name"]
            ids = i["Ids"]

            if i["Target"] == "Parameter":
                self.model.parameter_groups[name] = ids
            elif i["Target"] == "Opacity":
                self.model.opacity_groups[name] = ids

        self.nonexclusive = { }

    def apply_aliases(self, aliases):

        for k, v in aliases.items():
            target = None

            if v in self.motions:
                target = self.motions

            elif v in self.expressions:
                target = self.expressions

            elif v in self.nonexclusive:
                target = self.expressions

            else:
                raise Exception("Name {!r} is not a known motion or expression.".fromat(v))

            if k in target:
                raise Exception("Name {!r} is already specified as a motion or expression.".fromat(k))

            target[k] = target[v]

    def apply_nonexclusive(self, nonexclusive):
        for i in nonexclusive:
            if i not in self.expressions:
                raise Exception("Name {!r} is not a known expression.".fromat(i))

            self.nonexclusive[i] = self.expressions.pop(i)


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
    used_nonexclusive = None

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
    def __init__(self, filename, zoom=None, top=0.0, base=1.0, height=1.0, loop=False, aliases={}, fade=None, motions=None, expression=None, nonexclusive=None, used_nonexclusive=None, **properties):

        super(Live2D, self).__init__(**properties)

        self.filename = filename
        self.motions = motions
        self.expression = expression
        self.used_nonexclusive = used_nonexclusive

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

        if nonexclusive:
            common.apply_nonexclusive(nonexclusive)

        if aliases:
            common.apply_aliases(aliases)

    def _duplicate(self, args):

        if not self._duplicatable:
            return self

        if not args:
            return self

        common = self.common
        motions = [ ]
        used_nonexclusive = [ ]

        expression = None

        for i in args.args:

            if i in common.motions:
                motions.append(i)
                continue

            if i in common.nonexclusive:
                used_nonexclusive.append(i)
                continue

            if i in common.expressions:
                if expression is not None:
                    raise Exception("When showing {}, {} and {} are both live2d expressions.".format(" ".join(args.name), i, expression))

                expression = i
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
            fade=self.fade,
            expression=expression,
            used_nonexclusive=used_nonexclusive)

        rv.name = args.name
        rv._duplicatable = False

        return rv

    def _list_attributes(self, tag, attributes):

        common = self.common

        available = set(common.attributes)

        for i in attributes:
            if i in common.expressions:
                available -= set(common.expressions)

        available |= set(attributes)

        return [ i for i in common.attributes if i in available ]

    def _choose_attributes(self, tag, attributes, optional):

        common = self.common

        # Chose all motions.
        rv = [ i for i in attributes if i in common.motions ]

        # If there are no motions, choose the last one from the optional attributes.
        if not rv:
            rv = [ i for i in optional if i in common.motions ][:-1]

        # Choose the first expression.
        for i in list(attributes) + list(optional):
            if i in common.expressions:
                rv.insert(0, i)
                break

        # Choose all possible nonexclusive attributes.
        for i in list(attributes) + list(optional):
            if i in common.nonexclusive:
                rv.append(i)

        return tuple(rv)

    def update(self, common, st, st_fade):
        """
        This updates the common model with the information taken from the
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

            if kind == "PartOpacity":
                common.model.set_part_opacity(key, value)
            elif kind == "Parameter":
                common.model.set_parameter(key, value, factor)
            elif kind == "Model":
                common.model.set_parameter(key, value, factor)

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

        if self.used_nonexclusive:
            for e in self.used_nonexclusive:
                for i in common.nonexclusive[e]:
                    common.model.blend_parameter(i["Id"], i["Blend"], i["Value"])

        if self.expression:
            for i in common.expressions[self.expression]:
                common.model.blend_parameter(i["Id"], i["Blend"], i["Value"])

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
