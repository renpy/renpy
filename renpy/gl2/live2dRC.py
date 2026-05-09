from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import os
import re
import sys
import json
import time

from typing import Any

import renpy

from renpy.compat import str
from renpy.display.core import absolute
from renpy.gl2.gl2shadercache import register_shader

try:
    import renpy.gl2.live2dmodelRC as live2dmodel
except ImportError:
    live2dmodel = None

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

    dll = dll.encode("utf-8")

    if not renpy.gl2.live2dmodelRC.load(dll): # type: ignore
        raise Exception(f"Could not load Live2D. {dll} was not found.")

    did_onetime_init = True

did_init = False

def init():
    global did_init

    if did_init:
        return

    if live2dmodel is None:
        raise Exception("Live2D has not been built.")

    if renpy.emscripten:
        raise Exception("Live2D is not supported the web platform.")

    onetime_init()

    register_shader("live2d.coord_base", variables="""
        uniform vec2 u_coord_scale;
        uniform vec2 u_coord_offset;
        attribute vec4 a_position;
        varying vec2 v_live2d_coord;
    """, vertex_190="""
        v_live2d_coord = a_position.xy * u_coord_scale + u_coord_offset;
    """)

    register_shader("live2d.texture", variables="""
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_200="""
        gl_FragColor = texture2D(tex0, v_tex_coord);
    """)

    register_shader("live2d.brightness", variables="""
        uniform float u_brightness;
    """, fragment_247="""
        gl_FragColor.rgb += gl_FragColor.a * u_brightness;
    """)

    register_shader("live2d.contrast", variables="""
        uniform float u_contrast;
    """, fragment_248="""
        gl_FragColor.rgb *= u_contrast;
        gl_FragColor.rgb += step(0.999, gl_FragColor.a) * 0.5 * (1.0 - gl_FragColor.a);
    """)

    register_shader("live2d.saturate", variables="""
        uniform vec3 u_saturate_r;
        uniform vec3 u_saturate_g;
        uniform vec3 u_saturate_b;
    """, fragment_249="""
        gl_FragColor.rgb = vec3(
            dot(gl_FragColor.rgb, u_saturate_r),
            dot(gl_FragColor.rgb, u_saturate_g),
            dot(gl_FragColor.rgb, u_saturate_b)
        );
    """)

    register_shader("live2d.multiply", variables="""
        uniform vec3 u_multiply;
    """, fragment_250="""
        gl_FragColor.rgb *= u_multiply;
    """)

    register_shader("live2d.screen", variables="""
        uniform vec3 u_screen;
        uniform vec3 u_screen_complement;
    """, fragment_250="""
        gl_FragColor.rgb = gl_FragColor.rgb * u_screen_complement + gl_FragColor.a * u_screen;
    """)

    register_shader("live2d.mask", variables="""
        varying float v_mask_alpha;
    """, fragment_399="""
        gl_FragColor *= v_mask_alpha;
    """)

    register_shader("live2d.inverted_mask", variables="""
        varying float v_mask_alpha;
    """, fragment_399="""
        gl_FragColor *= 1.0 - v_mask_alpha;
    """)

    # generate combine_mask shader with 24 mask slots dynamically
    mask_count = 24

    varying_decls = "\n".join(f"        varying float v_mask_alpha_{i};" for i in range(mask_count))
    vertex_inits = "\n".join(f"        v_mask_alpha_{i} = 0.0;" for i in range(mask_count))
    mix_ops = "\n".join(
        f"        v_mask_alpha = mix(v_mask_alpha, v_mask_alpha_{i} + v_mask_alpha * (1.0 - v_mask_alpha_{i}), step({i + 1}.0, mask_count));"
        for i in range(mask_count)
    )

    register_shader("live2d.combine_mask", variables=f"""
        uniform int u_live2d_mask_count;
{varying_decls}
    """, vertex_190=f"""
{vertex_inits}
    """, fragment_349=f"""
        float v_mask_alpha = 0.0;
        float mask_count = float(u_live2d_mask_count);

{mix_ops}
    """)

    def _register_effect_shader(name, i, matrix_idx, row, swizzle, frag_priority, fragment_code):
        accessor = f"a_{name}_coords_{matrix_idx}[{row}]{swizzle}"

        register_shader(f"live2d.{name}_{i}", variables=f"""
            uniform sampler2D u_live2d_{name}_{i};
            attribute mat4 a_{name}_coords_{matrix_idx};
            varying vec2 v_{name}_coord_{i};
            varying vec2 v_live2d_coord;
        """, vertex_191=f"""
            v_{name}_coord_{i} = v_live2d_coord + {accessor};
        """, **{f"fragment_{frag_priority}": fragment_code})

    for i in range(24):
        matrix_idx = i // 8
        in_matrix_idx = i % 8
        row = in_matrix_idx // 2
        swizzle = ".zw" if (in_matrix_idx % 2) else ".xy"

        # mask_part shader - extracts alpha for masking
        _register_effect_shader("mask", i, matrix_idx, row, swizzle, 325, f"""
            float v_mask_alpha_{i} = texture2D(u_live2d_mask_{i}, v_mask_coord_{i}).a;
        """)

        # shadow shader - multiplies RGB based on shadow texture
        _register_effect_shader("shadow", i, matrix_idx, row, swizzle, 398, f"""
            vec4 shadow_{i} = texture2D(u_live2d_shadow_{i}, v_shadow_coord_{i});

            gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * ((1.0 - shadow_{i}.a) + shadow_{i}.rgb), step(0.001, gl_FragColor.a * shadow_{i}.a));
        """)

        # darken shader - subtracts from RGB based on darken texture
        _register_effect_shader("darken", i, matrix_idx, row, swizzle, 398, f"""
            vec4 darken_{i} = texture2D(u_live2d_darken_{i}, v_darken_coord_{i});

            gl_FragColor.rgb -= max(vec3(0.0), gl_FragColor.rgb * darken_{i}.a - darken_{i}.rgb) * step(0.001, gl_FragColor.a * darken_{i}.a);
        """)

        # squish shader - composites over base drawable
        _register_effect_shader("squish", i, matrix_idx, row, swizzle, 397, f"""
            vec4 squish_{i} = texture2D(u_live2d_squish_{i}, v_squish_coord_{i});

            vec4 result_{i} = squish_{i} + gl_FragColor * (1.0 - squish_{i}.a);

            gl_FragColor = mix(gl_FragColor, result_{i}, step(0.0001, result_{i}.a));
        """)

    register_shader("live2d.alpha", variables="""
        uniform float u_live2d_alpha;
    """, fragment_500="""
        gl_FragColor *= u_live2d_alpha;
    """)
    
    did_init = True

def reset():
    """
    Resets this module when Ren'Py reloads the script.
    """

    global did_init
    did_init = False

    common_cache.clear()

class Live2DCommon:
    """
    This object stores information that is common to all of the Live2D
    displayables that use the same .model3.json file, so this information
    only needs to be loaded once. This should not leak into the save games,
    but is loaded at init time.
    """

    def __init__(self, filename):
        init()

        # if a directory is given rather than a json file, expand it
        if not filename.endswith(".json"):
            suffix = filename.rpartition("/")[2]
            filename = filename + "/" + suffix + ".model3.json"

        if renpy.config.log_live2d_loading:
            renpy.display.log.write("Loading Live2D from %r.", filename)

        if not renpy.loader.loadable(filename, directory="images"):
            raise Exception(f"Live2D model {filename} does not exist.")

        # path to where the files used are stored
        self.base = filename.rpartition("/")[0]

        if self.base:
            self.base += "/"

        # contents of the .model3.json file
        with renpy.loader.load(filename, directory="images") as f:
            self.model_json = json.load(f)

        # texture images
        self.textures = []

        for i in self.model_json["FileReferences"]["Textures"]:
            m = re.search(r'\.(\d+)/', i)

            if m:
                size = int(m.group(1))
                renpy.config.max_texture_size = (
                    max(renpy.config.max_texture_size[0], size),
                    max(renpy.config.max_texture_size[1], size),
                )

            im = renpy.easy.displayable(self.base + i)
            self.textures.append(im)

        # shared texture alpha data cache
        self.texture_alpha_data = {}

        self.low_res = False

        # check if explicit LowResTextures are specified in the model JSON
        low_res_paths = self.model_json["FileReferences"].get("LowResTextures", None)

        if low_res_paths is not None: # use explicitly specified low-res texture files
            for t, i in enumerate(low_res_paths):
                m = re.search(r'\.(\d+)/', i)

                if m:
                    size = int(m.group(1))
                    renpy.config.max_texture_size = (
                        max(renpy.config.max_texture_size[0], size),
                        max(renpy.config.max_texture_size[1], size),
                    )

                im = renpy.easy.displayable(self.base + i)
                
                self.textures[t] = im
        elif renpy.config.live2d_resolution is not None: # auto-generate low-res textures by scaling full-res textures
            for t, texture in enumerate(self.textures):
                non_caching_source = renpy.display.im.Image(texture.filename, cache = False) # use cache = False so the full-res source is NOT cached (memory efficient)
                scaled = renpy.display.im.MipmapScale(non_caching_source, renpy.config.live2d_resolution) # MipmapScale preserves blend modes

                self.textures[t] = scaled

        # model created from the moc3 file
        self.model = renpy.gl2.live2dmodelRC.Live2DModel(self) # type: ignore

        self._test_model = None

        for i in self.model_json.get("Groups", [ ]):
            name = i["Name"]
            ids = i["Ids"]

            if i["Target"] == "Parameter":
                self.model.parameter_groups[name] = ids
            elif i["Target"] == "Opacity":
                self.model.opacity_groups[name] = ids

        # if not None, a function that can blend parameters itself after applying expressions
        self.update_function = None # type: Any

        self.refresh_function = None

        self.lite = False

        self.thread_allocated = False

        self.matrix_color = None
    
    @property
    def test_model(self):
        if self._test_model is None:
            self._test_model = renpy.gl2.live2dmodelRC.Live2DModel(self) # type: ignore

            # test models force texture loading for visibility checks (hypothetical outfits need accurate results)
            self._test_model.force_texture_load = True

        return self._test_model

# this maps a filename to a Live2DCommon object
common_cache = { }

ALL_LIVE2DS = set()

class Live2D(renpy.display.displayable.Displayable):
    """
    A structural name for this displayable, consisting of the layer, tag, and a count. This is used to
    match the displayable to its state in a previous interaction.
    """

    name: tuple[str, str, int] | None = None

    nosave = ["common_cache"]

    common_cache = None
    properties = {}

    def create_common(self):
        rv = common_cache.get(self.filename, None)

        if rv is None:
            rv = Live2DCommon(self.filename)

            common_cache[self.filename] = rv

        self.common_cache = rv

        return rv

    @property
    def common(self):
        if self.common_cache is not None:
            return self.common_cache

        return self.create_common()

    def __init__(
            self,
            filename,
            zoom=None,
            top=0.0,
            base=1.0,
            height=1.0,
            update_function=None,
            refresh_function=None,
            tag=None,
            **properties):

        super().__init__(**properties)

        self.filename = filename

        self.zoom = zoom
        self.top = top
        self.base = base
        self.height = height

        # the name of this displayable
        self.name = None

        self.properties = properties

        # load the common data
        common = self.common

        if update_function is not None:
            common.update_function = update_function

        if refresh_function is not None:
            common.refresh_function = refresh_function
        elif update_function is not None:
            common.refresh_function = update_function

        self.hideable_parts = set()
        self.visible_parts = set()

        self.toggles = set()
        self.overridden_toggles = set()
        self.manually_set_toggles = dict()

        self.preload = True
        self.displayed = False
        self.rendered = False
        self.tag = tag

        self.color_changed = False

        self.last_update = 0.0

        # for adaptive polling
        self.tau_max = 1.0 / 30.0
        self.tau_min = 1.0 / 60.0
        self.tau = self.tau_min
        self.alpha = 2.0
        self.rho = 0.1
        self.m = 2
        self.fast_left = 0

        ALL_LIVE2DS.add(self)

    def set_visibility(self, name, flag, test = False):
        if flag not in {True, False}:
            raise Exception("Unknown flag {!r}".format(flag))
        
        if test:
            self.common.test_model.set_visibility(name, flag)
        else:
            self.common.model.set_visibility(name, flag)

    def set_mask(self, name, flag, test = False):
        if flag not in {True, False}:
            raise Exception("Unknown flag {!r}".format(flag))
        
        if test:
            self.common.test_model.set_mask(name, flag)
        else:
            self.common.model.set_mask(name, flag)
            
    def blend_parameter(self, name, blend, value, weight = 1.0, override = True, test = False):
        if blend not in {"Add", "Multiply", "Overwrite"}:
            raise Exception("Unknown blend mode {!r}".format(blend))

        if test:
            self.common.test_model.blend_parameter(name, blend, value, weight)
        else:
            self.common.model.blend_parameter(name, blend, value, weight)
        
            if override and name in self.toggles:
                self.overridden_toggles.add((name, value))

    def blend_opacity(self, name, blend, value, weight = 1.0, test = False):
        if blend not in {"Add", "Multiply", "Overwrite"}:
            raise Exception("Unknown blend mode {!r}".format(blend))

        if test:
            self.common.test_model.blend_opacity(name, blend, value, weight)
        else:
            self.common.model.blend_opacity(name, blend, value, weight)

    def change_visibility(self, pattern, flag, exclude = tuple(), test = False):
        if flag not in {True, False}:
            raise Exception("Unknown flag {!r}".format(flag))
        
        if test:
            self.common.test_model.change_visibility(pattern, flag, exclude)
        else:
            self.common.model.change_visibility(pattern, flag, exclude)

    def change_mask(self, pattern, flag, exclude = tuple(), test = False):
        if flag not in {True, False}:
            raise Exception("Unknown flag {!r}".format(flag))
        
        if test:
            self.common.test_model.change_mask(pattern, flag, exclude)
        else:
            self.common.model.change_mask(pattern, flag, exclude)

    def change_parameter(self, pattern, value, blend = "Overwrite", exclude = tuple(), test = False):
        if blend not in {"Add", "Multiply", "Overwrite"}:
            raise Exception("Unknown blend mode {!r}".format(blend))

        if test:
            self.common.test_model.change_parameter(pattern, value, blend, exclude)
        else:
            self.common.model.change_parameter(pattern, value, blend, exclude)

    def change_color(self, pattern, value, color_type = "multiply", exclude = tuple(), test = False):
        if color_type not in {"brightness", "contrast", "saturation", "multiply", "screen"}:
            raise Exception("Unknown color type {!r}".format(color_type))

        if test:
            self.common.test_model.change_color(pattern, value, color_type, exclude)
        else:
            self.common.model.change_color(pattern, value, color_type, exclude)

    def is_visible(self, pattern, exclude = tuple(), coverage_exclude = tuple(), alpha_threshold = -1.0, fraction_threshold = 0.5, vertex_threshold = 0, skip_boundary_layers = 2, test = False, fast = False):
        if test:
            return self.common.test_model.is_visible(pattern, exclude, coverage_exclude, alpha_threshold, fraction_threshold, vertex_threshold, skip_boundary_layers, fast)
        else:
            return self.common.model.is_visible(pattern, exclude, coverage_exclude, alpha_threshold, fraction_threshold, vertex_threshold, skip_boundary_layers, fast)
        
    def is_uncovered(self, pattern, exclude = tuple(), coverage_exclude = tuple(), alpha_threshold = -1.0, fraction_threshold = 0.5, vertex_threshold = 0, skip_boundary_layers = 2, test = False, fast = False):
        if test:
            return self.common.test_model.is_uncovered(pattern, exclude, coverage_exclude, alpha_threshold, fraction_threshold, vertex_threshold, skip_boundary_layers, fast)
        else:
            return self.common.model.is_uncovered(pattern, exclude, coverage_exclude, alpha_threshold, fraction_threshold, vertex_threshold, skip_boundary_layers, fast)
    
    def update_model(self, st, update_function = True, physics = True, refresh = False, changed = False):
        if not update_function and not physics and not refresh:
            return False

        common = self.common
        model = common.model

        if refresh or update_function:
            visible_parts = self.visible_parts.copy()
            overridden_toggles = self.overridden_toggles.copy()
                    
            if refresh and common.refresh_function:
                self.visible_parts.clear()
                self.overridden_toggles.clear()

                common.refresh_function(self, 0.0)

                for part in self.hideable_parts - self.visible_parts:
                    model.blend_opacity(part, "Overwrite", 0.0, 1.0)

                for part in self.visible_parts:
                    model.blend_opacity(part, "Overwrite", 1.0, 1.0)
            elif update_function and common.update_function:
                self.visible_parts.clear()
                self.overridden_toggles.clear()

                changed = common.update_function(self, st) or changed

            # only update things that have changed
            previously_visible_parts = visible_parts - self.visible_parts
            visible_parts = self.visible_parts - visible_parts
            previously_overridden_toggles = overridden_toggles - self.overridden_toggles
            overridden_toggles = self.overridden_toggles - overridden_toggles

            if previously_visible_parts or visible_parts or previously_overridden_toggles:
                for part in visible_parts:
                    model.blend_opacity(part, "Overwrite", 1.0, 1.0)

                for part in previously_visible_parts:
                    model.blend_opacity(part, "Overwrite", 0.0, 1.0)

                current_toggle_names = {t[0] for t in overridden_toggles}

                for toggle, _ in previously_overridden_toggles:
                    if toggle not in current_toggle_names:
                        model.blend_parameter(toggle, "Overwrite", model.parameter_defaults[toggle], 1.0)

                changed = True
            elif overridden_toggles:
                changed = True

            for key, value in self.manually_set_toggles.items():
                model.blend_parameter(key, "Overwrite", value)

            if refresh:
                return self.update_model(st, changed = True)

        if physics and not common.lite:
            changed = model.evaluate_physics(st) or changed

        changed = model.update(changed)

        if self.preload:
            textures = common.textures

            for i in model.used_textures:
                renpy.display.im.cache.preload_image(textures[i])

        return changed

    def render(self, width, height, st, at):
        common = self.common
        model = common.model

        if not self.rendered:
            self.update_model(time.perf_counter(), refresh = True)

            self.rendered = True

        sw, sh = model.get_size()

        zoom = self.zoom

        if zoom is None:
            top = absolute.compute_raw(self.top, sh)
            base = absolute.compute_raw(self.base, sh)

            size = max(base - top, 1.0)

            zoom = self.height * renpy.config.screen_height / size
        else:
            size = sh
            top = 0

        # render the model
        rend = model.render(zoom)

        # apply scaling as needed
        rv = renpy.exports.Render(sw * zoom, size * zoom)
        rv.blit(rend, (0, -top * zoom))

        if common.matrix_color:
            rv.add_shader("renpy.matrixcolor")
            rv.add_uniform("u_renpy_matrixcolor", common.matrix_color)
        
        return rv

    def visit(self):
        return [] # this leads to less hitching