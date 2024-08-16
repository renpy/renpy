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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Any


import renpy
import renpy.gl2.live2dmotion
from renpy.gl2.gl2shadercache import register_shader
from renpy.display.core import absolute

try:
    import renpy.gl2.live2dmodel as live2dmodel
except ImportError:
    live2dmodel = None

import sys
import os
import json
import collections
import re

did_onetime_init = False


def onetime_init():
    global did_onetime_init

    if did_onetime_init:
        return

    if renpy.windows:
        dll = "Live2DCubismCore.dll"
    elif renpy.macintosh:
        dll = "libLive2DCubismCore.dylib"
    elif renpy.ios:
        dll = sys.executable
    else:
        dll = "libLive2DCubismCore.so"

    fn = os.path.join(os.path.dirname(sys.executable), dll)
    if os.path.exists(fn):
        dll = fn

    if not PY2:
        dll = dll.encode("utf-8")

    if not renpy.gl2.live2dmodel.load(dll): # type: ignore
        raise Exception("Could not load Live2D. {} was not found.".format(dll))

    did_onetime_init = True


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

    if renpy.emscripten:
        raise Exception("Live2D is not supported the web platform.")

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

    register_shader("live2d.colors", variables="""
        uniform vec4 u_multiply;
        uniform vec4 u_screen;
    """, fragment_250="""
        gl_FragColor.rgb = gl_FragColor.rgb * u_multiply.rgb;
        gl_FragColor.rgb = (gl_FragColor.rgb + u_screen.rgb * gl_FragColor.a) - (gl_FragColor.rgb * u_screen.rgb);
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
    Resets this module when Ren'Py reloads the script.
    """

    global did_init
    did_init = False

    common_cache.clear()


def reset_states():
    """
    Resets the Live2D states when Ren'Py restarts the game.
    """

    states.clear()


class Live2DExpression(object):
    """
    The data corresponding to an expression.
    """

    def __init__(self, parameters, fadein, fadeout):
        self.parameters = parameters
        self.fadein = fadein
        self.fadeout = fadeout


class Live2DCommon(object):
    """
    This object stores information that is common to all of the Live2D
    displayables that use the same .model3.json file, so this information
    only needs to be loaded once. This should not leak into the save games,
    but is loaded at init time.
    """

    def __init__(self, filename, default_fade):

        init()

        # If a directory is given rather than a json file, expand it.
        if not filename.endswith(".json"):
            suffix = filename.rpartition("/")[2]
            filename = filename + "/" + suffix + ".model3.json"

        if renpy.config.log_live2d_loading:
            renpy.display.log.write("Loading Live2D from %r.", filename)

        if not renpy.loader.loadable(filename, directory="images"):
            raise Exception("Live2D model {} does not exist.".format(filename))

        # A short name for the model.
        model_name = filename.rpartition("/")[2].partition(".")[0].lower()

        # The path to where the files used are stored.
        self.base = filename.rpartition("/")[0]

        if self.base:
            self.base += "/"

        # The contents of the .model3.json file.
        with renpy.loader.load(filename, directory="images") as f:
            self.model_json = json.load(f)

        # The model created from the moc3 file.
        self.model = renpy.gl2.live2dmodel.Live2DModel(self.base + self.model_json["FileReferences"]["Moc"]) # type: ignore

        # The texture images.
        self.textures = [ ]

        for i in self.model_json["FileReferences"]["Textures"]:

            m = re.search(r'\.(\d+)/', i)
            if m:
                size = int(m.group(1))
                renpy.config.max_texture_size = (
                    max(renpy.config.max_texture_size[0], size),
                    max(renpy.config.max_texture_size[1], size),
                )

            im = renpy.easy.displayable(self.base + i)
            im = renpy.display.im.unoptimized_texture(im)
            self.textures.append(im)

        # A map from the motion file name to the information about it.
        motion_files = { }

        # A map from the expression name to the information about it.
        expression_files = { }

        for i in renpy.exports.list_files():

            if not i.startswith(self.base):
                continue

            if i.endswith("motion3.json"):
                i = i[len(self.base):]
                motion_files[i] = { "File" : i }
            elif i.endswith(".exp3.json"):
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
        self.motions = { "still" : renpy.gl2.live2dmotion.NullMotion() } # type: dict[str, renpy.gl2.live2dmotion.Motion|renpy.gl2.live2dmotion.NullMotion]

        for i in motion_files.values():
            name = i["File"].lower().rpartition("/")[2].partition(".")[0]

            prefix, _, suffix = name.partition("_")

            if prefix == model_name:
                name = suffix

            if renpy.loader.loadable(self.base + i["File"], directory="images"):
                if renpy.config.log_live2d_loading:
                    renpy.display.log.write(" - motion %s -> %s", name, i["File"])

                self.motions[name] = renpy.gl2.live2dmotion.Motion(
                    self.base + i["File"],
                    i.get("FadeInTime", default_fade),
                    i.get("FadeOutTime", default_fade))

                self.attributes.add(name)

        # A map from an expression to a Live2DExpression object.
        self.expressions = { "null" : Live2DExpression([ ], 0.0, 0.0) }

        for i in expression_files.values():
            name = i["File"].lower().rpartition("/")[2].partition(".")[0]

            prefix, _, suffix = name.partition("_")

            if prefix == model_name:
                name = suffix

            if renpy.loader.loadable(self.base + i["File"], directory="images"):
                if renpy.config.log_live2d_loading:
                    renpy.display.log.write(" - expression %s -> %s", name, i["File"])

                if name in self.attributes:
                    raise Exception("Name {!r} is already specified as a motion.".format(name))

                with renpy.loader.load(self.base + i["File"], directory="images") as f:
                    expression_json = json.load(f)

                self.expressions[name] = Live2DExpression(
                    expression_json.get("Parameters", [ ]),
                    expression_json.get("FadeInTime", default_fade),
                    expression_json.get("FadeOutTime", default_fade),
                    )

                self.attributes.add(name)

        for i in self.model_json.get("Groups", [ ]):
            name = i["Name"]
            ids = i["Ids"]

            if i["Target"] == "Parameter":
                self.model.parameter_groups[name] = ids
            elif i["Target"] == "Opacity":
                self.model.opacity_groups[name] = ids

        # All expressions, non-exclusive and exclusive, and its aliases.
        self.all_expressions = dict(self.expressions)

        # Nonexcusive expressions.
        self.nonexclusive = { } # type: dict[str, Live2DExpression]

        # This may be True, False, or a set of motion names.
        self.seamless = False # type: bool|set[str]

        # If not None, a function that takes a tuple of attributes, and returns
        # a tuple of attributes.
        self.attribute_function = None # type: Any

        # Same.
        self.attribute_filter = None # type: Any

        # If not None, a function that can blend parameters itself after applying expressions.
        self.update_function = None # type: Any

    def apply_aliases(self, aliases):

        for k, v in aliases.items():
            target = None
            expression = False

            if v in self.motions:
                target = self.motions

            elif v in self.expressions:
                target = self.expressions
                expression = True

            elif v in self.nonexclusive:
                target = self.nonexclusive
                expression = True

            else:
                raise Exception("Name {!r} is not a known motion or expression.".format(v))

            if k in target:
                raise Exception("Name {!r} is already specified as a motion or expression.".format(k))

            target[k] = target[v] # type: ignore

            if expression:
                self.all_expressions[k] = target[v] # type: ignore

    def apply_nonexclusive(self, nonexclusive):
        for i in nonexclusive:
            if i not in self.expressions:
                raise Exception("Name {!r} is not a known expression.".format(i))

            self.nonexclusive[i] = self.expressions.pop(i)

    def apply_seamless(self, value):
        self.seamless = value

    def is_seamless(self, motion):
        if self.seamless is True:
            return True
        elif self.seamless is False:
            return False
        else:
            return (motion in self.seamless)


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
        self.old = None # type: Live2D|None
        self.new = None # type: Live2D|None

        # The time at which the old and new displayables were last updated.
        self.old_base_time = 0 # type: float|None
        self.new_base_time = 0 # type: float|None

        # A list of (expression_name, time_shown) tuples.
        self.expressions = [ ]

        # A list of (expression_name, time_shown, time_hidden) tuples.
        self.old_expressions = [ ]

    def update_expressions(self, expressions, now):
        """
        Updates the lists of new and old expressions.

        `expressions`
            A list of strings giving expression names.

        `now`
            The time the current displayable started showing.
        """

        current = set(name for name, _ in self.expressions)

        self.old_expressions = \
            [ (name, shown, hidden) for name, shown, hidden in self.old_expressions if name not in expressions  ] + \
            [ (name, shown, now) for name, shown in self.expressions if name not in expressions ]

        self.expressions = [ (name, shown) for (name, shown) in self.expressions if name in expressions ]
        self.expressions += [ (name, now) for name in expressions if name not in current ]


# A map from name to Live2DState object.
states = collections.defaultdict(Live2DState)


def update_states():
    """
    Called once per interact to walk the tree of displayables and find
    the old and new live2d states.
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
            state.expressions = [ ]
            state.old_expressions = [ ]

        state.new = d

        if d.sustain:
            state.new_base_time = state.old_base_time
        else:
            state.new_base_time = None

        state.cycle_new = True

    sls = renpy.display.scenelists.scene_lists()

    for d in sls.get_all_displayables(current=True):
        if d is not None:
            d.visit_all(visit)

    for s in states.values():
        if not s.mark:
            s.cycle_new = False

        s.mark = False


class Live2D(renpy.display.displayable.Displayable):

    nosave = [ "common_cache" ]

    common_cache = None
    _duplicatable = True
    used_nonexclusive = None
    properties = {}

    default_fade = 1.0

    def create_common(self):
        key = (self.filename, self.default_fade)
        rv = common_cache.get(key, None)

        if rv is None:
            rv = Live2DCommon(self.filename, self.default_fade)
            common_cache[key] = rv

        self.common_cache = rv

        return rv

    @property
    def common(self):
        if self.common_cache is not None:
            return self.common_cache

        return self.create_common()

    # Note: When adding new parameters, make sure to add them to _duplicate, too.
    def __init__(
            self,
            filename,
            zoom=None,
            top=0.0,
            base=1.0,
            height=1.0,
            loop=False,
            aliases={},
            fade=None,
            motions=None,
            expression=None,
            nonexclusive=None,
            used_nonexclusive=None,
            seamless=None,
            sustain=False,
            attribute_function=None,
            attribute_filter=None,
            update_function=None,
            default_fade=1.0,
            **properties):


        super(Live2D, self).__init__(**properties)

        self.filename = filename
        self.motions = motions
        self.expression = expression
        self.used_nonexclusive = used_nonexclusive # type: list[str]|None

        self.zoom = zoom
        self.top = top
        self.base = base
        self.height = height
        self.loop = loop
        self.fade = fade
        self.sustain = sustain

        # The name of this displayable.
        self.name = None

        self.default_fade = default_fade

        self.properties = properties

        # Load the common data. Needed!
        common = self.common

        if nonexclusive:
            common.apply_nonexclusive(nonexclusive)

        if aliases:
            common.apply_aliases(aliases)

        if seamless is not None:
            common.apply_seamless(seamless)

        if attribute_function is not None:
            common.attribute_function = attribute_function

        if attribute_filter is not None:
            common.attribute_filter = attribute_filter

        if update_function is not None:
            common.update_function = update_function

    def _duplicate(self, args):

        if not self._duplicatable:
            return self

        if not args:
            return self

        common = self.common
        motions = [ ]
        used_nonexclusive = [ ]

        expression = None
        sustain = False

        if "_sustain" in args.args:
            attributes = tuple(i for i in args.args if i != "_sustain")
            sustain = True
        else:
            attributes = args.args


        if common.attribute_filter:
            attributes = common.attribute_filter(attributes)
            if not isinstance(attributes, tuple):
                attributes = tuple(attributes)

        if common.attribute_function is not None:
            attributes = common.attribute_function(attributes)

        for i in attributes:

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
            used_nonexclusive=used_nonexclusive,
            sustain=sustain,
            default_fade=self.default_fade,
            **self.properties)

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

        # Filter out _sustain.
        attributes = [ i for i in attributes if i != "_sustain" ]

        common = self.common

        # Chose all motions.
        rv = [ i for i in attributes if i in common.motions ]

        # Choose the first expression.
        for i in list(attributes) + list(optional):
            if i in common.expressions:
                rv.insert(0, i)
                break

        # Choose all possible nonexclusive attributes.
        for i in sorted(list(attributes)):
            if i in common.nonexclusive:
                rv.append(i)

        for i in sorted(list(optional)):
            if i in common.nonexclusive:
                rv.append(i)

        if set(attributes) - set(rv):
            return None

        rv = tuple(rv)

        if common.attribute_filter:
            rv = common.attribute_filter(rv)
            if not isinstance(rv, tuple):
                rv = tuple(rv)

        # If there are no motions, take the optional motions and sustain those.
        if not any(i in common.motions for i in rv):
            rv = ( "_sustain", ) + tuple(i for i in optional if i in common.motions) + rv

        return rv

    def update(self, common, st, st_fade):
        """
        This updates the common model with the information taken from the
        motions associated with this object. It returns the delay until
        Ren'Py needs to cause a redraw to occur, or None if no delay
        should occur.
        """

        if not self.motions:
            return

        # True if the motion should be faded in.
        do_fade_in = True

        # True if the motion should be faded out.
        do_fade_out = True

        # True if this is the last frame of a series of motions.
        last_frame = False

        # The index of the current motion in self.motions.
        current_index = 0

        # The motion object to display.
        motion = None

        # Determine the current motion.

        motion_st = st

        if st_fade is not None:
            motion_st = st - st_fade

        for m in self.motions:
            motion = common.motions.get(m, None)

            if motion is None:
                continue

            if motion.duration > st:
                break

            elif (motion.duration > motion_st) and not common.is_seamless(m):
                break

            motion_st -= motion.duration
            st -= motion.duration
            current_index += 1

        else:

            if motion is None:
                return None

            m = self.motions[-1]

            if (not self.loop) or (not motion.duration):
                st = motion.duration
                last_frame = True

            elif (st_fade is not None) and not common.is_seamless(m):
                # This keeps a motion from being restarted after it would have
                # been faded out.
                motion_start = motion_st - motion_st % motion.duration

                if (st - motion_start) > motion.duration:
                    st = motion.duration
                    last_frame = True

        if motion is None:
            return None

        # Determine the name of the current, last, and next motions. These are
        # None if there is no motion.

        if current_index < len(self.motions):
            current_name = self.motions[current_index]
        else:
            current_name = self.motions[-1]

        if current_index > 0:
            last_name = self.motions[current_index - 1]
        else:
            last_name = None

        if current_index < len(self.motions) - 1:
            next_name = self.motions[current_index + 1]
        elif self.loop:
            next_name = self.motions[-1]
        else:
            next_name = None

        # Handle seamless.

        if (last_name == current_name) and common.is_seamless(current_name):
            do_fade_in = False

        if (next_name == current_name) and common.is_seamless(current_name) and (st_fade is None):
            do_fade_out = False

        # Apply the motion.

        motion_data = motion.get(st, st_fade, do_fade_in, do_fade_out)

        for k, v in motion_data.items():

            kind, key = k
            factor, value = v

            if kind == "PartOpacity":
                common.model.set_part_opacity(key, value)
            elif kind == "Parameter":
                common.model.set_parameter(key, value, factor)
            elif kind == "Model":
                common.model.set_parameter(key, value, factor)

        if last_frame:
            return None
        else:
            return motion.wait(st, st_fade, do_fade_in, do_fade_out)

    def update_expressions(self, st):

        common = self.common
        model = common.model
        state = states[self.name]

        now = renpy.display.interface.frame_time

        # Reap obsolete old_expressions.
        state.old_expressions = [ (name, shown, hidden) for (name, shown, hidden) in state.old_expressions if (now - hidden) < common.all_expressions[name].fadeout ]

        # Determine the list of expressions that are being shown by this displayable.
        expressions = list(self.used_nonexclusive) # type: ignore
        if self.expression:
            expressions.append(self.expression)

        # Use them to update old_expressions and expressions in the frame.
        state.update_expressions(expressions, now - st)

        # Actually blend.
        redraw = None

        for name, shown, hidden in state.old_expressions:
            weight = 1.0
            e = common.all_expressions[name]

            if (e.fadein > 0) and (now - shown) < e.fadein:
                weight = min(weight, (now - shown) / e.fadein)
                redraw = 0

            if (e.fadeout > 0) and (now - hidden) < e.fadeout:
                weight = min(weight, 1.0 - (now - hidden) / e.fadeout)
                redraw = 0

            for i in e.parameters:
                model.blend_parameter(i["Id"], i["Blend"], i["Value"], weight=weight)

        for name, shown in state.expressions:
            weight = 1.0
            e = common.all_expressions[name]

            if (e.fadein > 0) and (now - shown) < e.fadein:
                weight = min(weight, (now - shown) / e.fadein)
                redraw = 0

            for i in e.parameters:
                model.blend_parameter(i["Id"], i["Blend"], i["Value"], weight=weight)

        return redraw

    def blend_parameter(self, name, blend, value, weight=1.0):
        if blend not in ("Add", "Multiply", "Overwrite"):
            raise Exception("Unknown blend mode {!r}".format(blend))

        self.common.model.blend_parameter(name, blend, value, weight)

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

            if state.new_base_time is None:
                state.new_base_time = renpy.display.interface.frame_time - st

            if state.old is None:
                fade = False
            elif state.old_base_time is None:
                fade = False
            elif state.old.common is not self.common:
                fade = False

        # Reset the parameter, and update.
        model.reset_parameters()

        if fade:
            t = renpy.display.interface.frame_time - state.new_base_time # type: ignore
        else:
            t = st

        new_redraw = self.update(common, t, None)

        if fade:
            old_redraw = state.old.update(common, renpy.display.interface.frame_time - state.old_base_time, st) # type: ignore
        else:
            old_redraw = None

        model.finish_parameters()

        # Apply the expressions.
        expression_redraw = self.update_expressions(st)

        # Apply the user-defined update.
        if common.update_function is None:
            user_redraw = None
        else:
            user_redraw = common.update_function(self, st)

        # Determine when to redraw.
        redraws = [ new_redraw, old_redraw, expression_redraw, user_redraw ]
        redraws = [ i for i in redraws if i is not None ]

        if redraws:
            renpy.display.render.redraw(self, min(redraws))

        # Get the textures.
        textures = [ renpy.display.im.render_for_texture(d, width, height, st, at) for d in common.textures ]

        sw, sh = model.get_size()

        zoom = self.zoom

        if zoom is None:
            top = absolute.compute_raw(self.top, sh)
            base = absolute.compute_raw(self.base, sh)

            size = max(base - top, 1.0)

            zoom = 1.0 * self.height * renpy.config.screen_height / size
        else:
            size = sh
            top = 0

        # Render the model.
        rend = model.render(textures, zoom)

        # Apply scaling as needed.
        rv = renpy.exports.Render(sw * zoom, size * zoom)
        rv.blit(rend, (0, -top * zoom))

        return rv

    def visit(self):
        return self.common.textures


# Caches the result of has_live2d.
_has_live2d = None


def has_live2d():
    """
    :doc: live2d

    Returns True if Live2d is supported on the current platform, and
    False otherwise.
    """

    global _has_live2d

    if _has_live2d is None:

        try:
            init()
            _has_live2d = True
        except Exception:
            _has_live2d = False

    return _has_live2d
