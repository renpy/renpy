# Copyright 2025-2046 Sebulsik <sebulsik.dev@gmail.com>
#
# All rights reserved.
#
# This source code and its associated files are the property of
# Sebulsik. Unauthorized copying, modification, distribution,
# sublicensing, or use of this software, in whole or in part, is
# prohibited without prior written permission from the copyright holder.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OF THIS SOFTWARE.

# Spine 4.3 native resource ownership and mesh construction.


from enum import IntEnum


class SpineLoadError(IntEnum):
    OK = 0
    PREDICTION_DEFERRED = 1
    UNEXPECTED_ERROR = 2

    ATLAS_NOT_FOUND = 10
    ATLAS_READ_FAILED = 11
    ATLAS_EMPTY = 12
    ATLAS_INVALID_TYPE = 13
    ATLAS_PARSE_FAILED = 14
    ATLAS_CREATE_FAILED = 15

    SKELETON_NOT_FOUND = 20
    SKELETON_READ_FAILED = 21
    SKELETON_EMPTY = 22
    SKELETON_INVALID_TYPE = 23
    SKELETON_UNSUPPORTED_FORMAT = 24
    SKELETON_PARSE_FAILED = 25
    SKELETON_CREATE_FAILED = 26

    SHARED_DATA_NOT_LOADED = 30
    DRAWABLE_CREATE_FAILED = 31
    DRAWABLE_STATE_UNAVAILABLE = 32
    MODEL_INITIALIZATION_FAILED = 33


include "spinecsm.pxi"

import renpy
import os
import sys
import traceback
from pathlib import Path
from libc.math cimport fmin, fmax

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void free(void* ptr)

cdef extern from "string.h":
    void* memcpy(void* dest, const void* src, size_t n)

cdef extern from "limits.h":
    int INT_MAX

cdef extern from "spinecsm.h":
    void* load_spine_function(void* handle, const char* name)
    void* load_spine_object(const char* sofile)

from renpy.uguu.gl cimport GL_ZERO, GL_ONE, GL_ONE_MINUS_SRC_ALPHA, \
    GL_ONE_MINUS_SRC_COLOR, GL_FUNC_ADD, GL_DST_COLOR, GL_DST_ALPHA, \
    GL_CLAMP_TO_EDGE, GL_REPEAT, GL_MIRRORED_REPEAT


# Shared by the Python and Cython Spine modules.
SPINE_DEBUG = os.environ.get("SPINE_DEBUG", "0") == "1"


def spine_log(message: object, *args: object, debug: bool = True) -> None:
    """Write a Spine diagnostic. Use debug=False for warnings and errors."""
    if debug and not SPINE_DEBUG:
        return

    message = " ".join(str(part) for part in (message,) + args)
    renpy.log.open("spine", flush=True).write("%s", message)


from renpy.gl2.gl2mesh import AttributeLayout
from renpy.gl2.gl2mesh2 cimport Mesh2
from renpy.display.render cimport Render

# Both tints are per-vertex because one batch can combine differently tinted slots.
SPINE_LAYOUT = AttributeLayout()
SPINE_LAYOUT.add_attribute("a_tex_coord", 2)
SPINE_LAYOUT.add_attribute("a_color", 4)
SPINE_LAYOUT.add_attribute("a_dark_color", 3)

# Floats per vertex in SPINE_LAYOUT.attribute.
cdef enum:
    SPINE_STRIDE = 9


def sampling_properties(min_filter, mag_filter, u_wrap, v_wrap):
    """Translate atlas filtering and wrapping into Ren’Py texture settings.
    Atlas textures have no mipmaps, so mipmapped filters use ordinary sampling."""
    rv = {}

    nearest_mag = (mag_filter == SPINE_TEXTURE_FILTER_NEAREST)
    nearest_min = min_filter in (SPINE_TEXTURE_FILTER_NEAREST,
                                 SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_NEAREST,
                                 SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_LINEAR)
    if nearest_mag or (nearest_min and mag_filter == SPINE_TEXTURE_FILTER_UNKNOWN):
        rv["texture_scaling"] = "nearest"

    wraps = {
        SPINE_TEXTURE_WRAP_CLAMP_TO_EDGE: GL_CLAMP_TO_EDGE,
        SPINE_TEXTURE_WRAP_REPEAT: GL_REPEAT,
        SPINE_TEXTURE_WRAP_MIRRORED_REPEAT: GL_MIRRORED_REPEAT,
    }
    wrap_s = wraps.get(u_wrap, GL_CLAMP_TO_EDGE)
    wrap_t = wraps.get(v_wrap, GL_CLAMP_TO_EDGE)
    if wrap_s != GL_CLAMP_TO_EDGE or wrap_t != GL_CLAMP_TO_EDGE:
        rv["texture_wrap"] = (wrap_s, wrap_t)

    return rv


def filter_is_mipmapped(f):
    return f in (SPINE_TEXTURE_FILTER_MIP_MAP,
                 SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_NEAREST,
                 SPINE_TEXTURE_FILTER_MIP_MAP_LINEAR_NEAREST,
                 SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_LINEAR,
                 SPINE_TEXTURE_FILTER_MIP_MAP_LINEAR_LINEAR)


class SpineRun:
    """A drawable mesh sharing one texture and blend mode.
    It owns its data so retained frames remain valid as animation advances."""

    __slots__ = ("page_index", "page_key", "blend_mode", "mesh", "vertices", "triangles", "commands")

    def __init__(self, page_index, page_key, blend_mode, mesh, vertices, triangles, commands):
        self.page_index = page_index    # atlas page index (texture pointer from spine-c)
        self.page_key = page_key        # atlas page texture name
        self.blend_mode = blend_mode    # spine blend mode shared by the run
        self.mesh = mesh                # Mesh2 in SPINE_LAYOUT
        self.vertices = vertices        # points in the mesh
        self.triangles = triangles      # triangles in the mesh
        self.commands = commands        # native commands merged into this run


class SpineTextureManager:
    """Find and cache atlas textures through Ren’Py’s resource loader,
    so packaged games use the same paths as loose files."""

    def __init__(self, atlas_dir=None):
        self.page_cache = {}  # page name -> renpy displayable
        self.atlas_dir = None  # Directory containing the atlas file
        if atlas_dir:
            self.atlas_dir = Path(atlas_dir).as_posix()

    def candidate_paths(self, path):
        """Return possible resource paths for an atlas page, in search order."""
        candidates = []

        if self.atlas_dir:
            candidates.append((Path(self.atlas_dir) / path).as_posix())

        candidates.append(Path(path).as_posix())
        candidates.append((Path("images") / path).as_posix())

        if self.atlas_dir and self.atlas_dir.startswith("images/"):
            candidates.append((Path("images") / self.atlas_dir[7:] / path).as_posix())

        seen = set()
        unique = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                unique.append(c)
        return unique

    def load_atlas_page(self, path):
        """Find an atlas texture, using a visible magenta placeholder if it is missing."""
        if path in self.page_cache:
            return self.page_cache[path]

        candidates = self.candidate_paths(path)

        for candidate in candidates:
            if not renpy.loader.loadable(candidate, directory="images"):
                continue

            displayable = renpy.easy.displayable(candidate)
            # UnoptimizedTexture lets render_for_texture reuse the engine texture cache.
            # Seems "renpy" analagous even though supposedly im isn't supported. Couldn't figure out alternative tbh
            # Tom did say im is still used internally so should be fine?
            displayable = renpy.display.im.unoptimized_texture(displayable)
            self.page_cache[path] = displayable
            spine_log(f"Spine: atlas page {path!r} -> {candidate}")
            return displayable

        spine_log(f"Spine: atlas page texture {path!r} was not found through the loader; tried {candidates}. Rendering a magenta placeholder.", debug=False)

        fallback = renpy.display.image.Solid((255, 0, 255), xysize=(64, 64))
        self.page_cache[path] = fallback
        return fallback

    def dispose_texture(self, path):
        """Forget a page so the next request resolves it again. Ren'Py's
        image cache owns the texture itself."""
        self.page_cache.pop(path, None)


# Shared atlas and skeleton data; each model owns a separate drawable.
cdef class SpineData:
    """Parsed skeleton/atlas data, loaded once and shared across SpineModels.
    Requires load() to have resolved the spine-c library first."""

    cdef spine_atlas atlas
    cdef spine_skeleton_data skeleton_data

    cdef object page_names  # list of atlas page texture names, by page index

    # Per-page (min_filter, mag_filter, u_wrap, v_wrap, pma).
    cdef object page_sampling
    cdef object atlas_path
    cdef object skeleton_path
    cdef bint loaded
    cdef readonly object last_error

    # Owned composed-skin handles, keyed by ordered source names; freed with this data.
    cdef object combined_skins

    cdef float data_x
    cdef float data_y
    cdef float data_w
    cdef float data_h

    def __cinit__(self):
        if not spine_library_loaded:
            raise RuntimeError("SpineData needs the spine-c library; call load() first")
        self.atlas = NULL
        self.skeleton_data = NULL
        self.page_names = []
        self.page_sampling = []
        self.atlas_path = None
        self.skeleton_path = None
        self.loaded = False
        self.last_error = None
        self.combined_skins = {}
        self.data_x = 0.0
        self.data_y = 0.0
        self.data_w = 0.0
        self.data_h = 0.0

    def __dealloc__(self):
        # Models retain this object until their drawables are freed.
        self._dispose()

    # Private cleanup prevents callers from freeing data still used by models.
    cdef void _dispose(self):
        # Composed skins must be freed before the skeleton data they reference.
        if self.combined_skins:
            for ptr in self.combined_skins.values():
                if ptr:
                    spine_skin_dispose(<spine_skin><intptr_t> ptr)
            self.combined_skins = {}

        if self.skeleton_data != NULL:
            spine_skeleton_data_dispose(self.skeleton_data)
            self.skeleton_data = NULL

        if self.atlas != NULL:
            spine_atlas_dispose(self.atlas)
            self.atlas = NULL

        self.page_names = []
        self.page_sampling = []
        self.loaded = False

    def is_loaded(self):
        """Check if the shared data is loaded"""
        return self.loaded

    def get_page_names(self):
        """Returns the list of atlas page texture names."""
        return list(self.page_names)

    def get_page_sampling(self):
        """Per page, by index: (min_filter, mag_filter, u_wrap, v_wrap, pma)."""
        return list(self.page_sampling)

    def page_render_properties(self, page_index):
        """Ren'Py render properties for the page's sampling, or {}."""
        if 0 <= page_index < len(self.page_sampling):
            mn, mg, uw, vw, pma = self.page_sampling[page_index]
            return sampling_properties(mn, mg, uw, vw)
        return {}

    def get_setup_bounds(self):
        """Return the unscaled bounds stored in the skeleton export.
        Zero bounds indicate that the live model must be measured instead."""
        if not self.loaded:
            return (0.0, 0.0, 0.0, 0.0)
        return (self.data_x, self.data_y, self.data_w, self.data_h)

    def get_animation_names(self):
        """List animations from shared data without creating a live model."""
        if not self.loaded or self.skeleton_data == NULL:
            return []

        cdef list names = []
        cdef spine_array_animation animations
        cdef spine_animation* buffer
        cdef spine_animation animation
        cdef size_t count, i
        cdef const char* name

        animations = spine_skeleton_data_get_animations(self.skeleton_data)
        if animations == NULL:
            return []

        count = spine_array_animation_size(animations)
        buffer = spine_array_animation_buffer(animations)
        if count == 0 or buffer == NULL:
            return []

        for i in range(count):
            animation = buffer[i]
            if animation != NULL:
                name = spine_animation_get_name(animation)
                if name != NULL:
                    names.append(name.decode('utf-8'))

        return names

    def get_skin_names(self):
        """List skins from shared skeleton data."""
        if not self.loaded or self.skeleton_data == NULL:
            return []

        cdef list names = []
        cdef spine_array_skin skins
        cdef spine_skin* buffer
        cdef spine_skin skin
        cdef size_t count, i
        cdef const char* name

        skins = spine_skeleton_data_get_skins(self.skeleton_data)
        if skins == NULL:
            return []

        count = spine_array_skin_size(skins)
        buffer = spine_array_skin_buffer(skins)
        if count == 0 or buffer == NULL:
            return []

        for i in range(count):
            skin = buffer[i]
            if skin != NULL:
                name = spine_skin_get_name(skin)
                if name != NULL:
                    names.append(name.decode('utf-8'))

        return names

    cdef spine_skin _get_combined_skin(self, names):
        """Combine two or more skins, reusing a cached result when available.
        The shared data owns the result; callers must not free it. Return NULL on failure."""
        cdef spine_skin combined
        cdef spine_skin part

        if not self.loaded or self.skeleton_data == NULL:
            return NULL

        key = tuple(names)
        ptr = self.combined_skins.get(key)
        if ptr is not None:
            return <spine_skin><intptr_t> ptr

        combined = spine_skin_create(b"__renpy_combined__")
        if combined == NULL:
            return NULL

        # Order-sensitive merge: later adds override earlier for the same slot,
        # so the tuple must be in show order.
        for n in key:
            part = spine_skeleton_data_find_skin(self.skeleton_data, n.encode('utf-8'))
            if part != NULL:
                spine_skin_add_skin(combined, part)

        self.combined_skins[key] = <intptr_t> combined
        return combined

    def load(self, atlas_path, skeleton_path):
        """Return a SpineLoadError; retain diagnostics in last_error.
        Failed loads dispose partial native state before returning."""
        self.last_error = None
        if self.loaded:
            return SpineLoadError.OK

        try:
            status = self._load_impl(atlas_path, skeleton_path)
        except Exception as e:
            self.last_error = f"Spine: Error in SpineData.load: {e}"
            status = SpineLoadError.UNEXPECTED_ERROR

        if status != SpineLoadError.OK:
            self._dispose()

        return status

    def _load_impl(self, atlas_path, skeleton_path):
        """Load atlas and skeleton resources. The caller cleans up if loading fails."""
        cdef spine_atlas_result atlas_result
        cdef spine_skeleton_data_result skeleton_result
        cdef const char* error
        cdef spine_array_atlas_page pages
        cdef spine_atlas_page* page_buffer
        cdef size_t page_count, page_index
        cdef const char* page_name
        cdef spine_atlas_page page
        cdef int min_filter, mag_filter, u_wrap, v_wrap
        cdef bint pma

        self.atlas_path = atlas_path
        self.skeleton_path = skeleton_path

        spine_log(f"Spine: Loading atlas: {atlas_path}")

        import renpy.loader

        try:
            atlas_file = renpy.loader.load(atlas_path, directory="images")
        except FileNotFoundError as read_error:
            self.last_error = f"Spine: Atlas file not found: {atlas_path}: {read_error}"
            return SpineLoadError.ATLAS_NOT_FOUND
        except Exception as loader_error:
            # Prediction defers resource loading; retry outside prediction.
            error_str = str(loader_error)
            if "predicting" in error_str:
                spine_log(f"Spine: Skipping load during prediction mode: {loader_error}")
                self.last_error = f"Spine: Skipping load during prediction mode: {loader_error}"
                return SpineLoadError.PREDICTION_DEFERRED
            self.last_error = f"Spine: Could not load atlas {atlas_path}: {error_str}"
            return SpineLoadError.ATLAS_READ_FAILED

        if atlas_file is None:
            self.last_error = f"Spine: Atlas file not found: {atlas_path}"
            return SpineLoadError.ATLAS_NOT_FOUND

        try:
            if hasattr(atlas_file, 'read'):
                try:
                    atlas_data = atlas_file.read()
                finally:
                    atlas_file.close()
            else:
                atlas_data = atlas_file
        except Exception as read_error:
            self.last_error = f"Spine: Could not read atlas {atlas_path}: {read_error}"
            return SpineLoadError.ATLAS_READ_FAILED

        if not atlas_data:
            self.last_error = f"Spine: No atlas data loaded from {atlas_path}"
            return SpineLoadError.ATLAS_EMPTY

        if isinstance(atlas_data, str):
            atlas_data = atlas_data.encode('utf-8')
        elif not isinstance(atlas_data, bytes):
            self.last_error = f"Spine: Unexpected atlas data type: {type(atlas_data)}"
            return SpineLoadError.ATLAS_INVALID_TYPE

        # spine_atlas_load expects a null-terminated string.
        if not atlas_data.endswith(b'\0'):
            atlas_data = atlas_data + b'\0'

        atlas_result = spine_atlas_load(<const char*> atlas_data)

        if atlas_result == NULL:
            self.last_error = f"Spine: Failed to load atlas from data: {atlas_path}"
            return SpineLoadError.ATLAS_CREATE_FAILED

        error = spine_atlas_result_get_error(atlas_result)
        if error != NULL:
            error_message = error.decode('utf-8', 'replace')
            spine_atlas_result_dispose(atlas_result)
            self.last_error = f"Spine: Failed to parse atlas {atlas_path}: {error_message}"
            return SpineLoadError.ATLAS_PARSE_FAILED

        self.atlas = spine_atlas_result_get_atlas(atlas_result)
        spine_atlas_result_dispose(atlas_result)

        if self.atlas == NULL:
            self.last_error = f"Spine: Failed to create atlas from data: {atlas_path}"
            return SpineLoadError.ATLAS_CREATE_FAILED

        spine_log(f"Spine: Atlas created successfully from data: {atlas_path}")

        # Native texture pointers encode page indices, not texture addresses.
        self.page_names = []
        self.page_sampling = []
        pages = spine_atlas_get_pages(self.atlas)
        if pages != NULL:
            page_count = spine_array_atlas_page_size(pages)
            page_buffer = spine_array_atlas_page_buffer(pages)
            if page_buffer != NULL:
                for page_index in range(page_count):
                    page = page_buffer[page_index]
                    page_name = spine_atlas_page_get_name(page)
                    if page_name != NULL:
                        name = page_name.decode('utf-8')
                    else:
                        name = None
                    self.page_names.append(name)

                    min_filter = spine_atlas_page_get_min_filter(page)
                    mag_filter = spine_atlas_page_get_mag_filter(page)
                    u_wrap = spine_atlas_page_get_u_wrap(page)
                    v_wrap = spine_atlas_page_get_v_wrap(page)
                    pma = spine_atlas_page_get_pma(page) != 0
                    self.page_sampling.append((min_filter, mag_filter, u_wrap, v_wrap, pma))

                    if filter_is_mipmapped(min_filter):
                        spine_log(f"Spine: atlas page {name!r} asks for a mipmapped minification filter; Ren'Py samples atlas pages without mipmaps, using {'nearest' if mag_filter == SPINE_TEXTURE_FILTER_NEAREST else 'linear'} instead.")
                    if pma:
                        spine_log(f"Spine: atlas page {name!r} of {atlas_path} is exported with premultiplied alpha. Ren'Py premultiplies on load, so edges will darken; re-export the atlas without 'Premultiply alpha'.", debug=False)

        spine_log(f"Spine: Atlas has {len(self.page_names)} pages: {self.page_names}")

        spine_log(f"Spine: Loading skeleton: {skeleton_path}")

        if skeleton_path.endswith(".skel"):
            file_type = "skel"
        elif skeleton_path.endswith(".json"):
            file_type = "json"
        else:
            self.last_error = f"Spine: Unknown skeleton file format: {skeleton_path}"
            return SpineLoadError.SKELETON_UNSUPPORTED_FORMAT

        try:
            skeleton_file = renpy.loader.load(skeleton_path, directory="images")
        except FileNotFoundError as read_error:
            self.last_error = f"Spine: Skeleton file not found: {skeleton_path}: {read_error}"
            return SpineLoadError.SKELETON_NOT_FOUND
        except IOError as io_error:
            self.last_error = f"Spine: Skeleton path was: {skeleton_path} and IOError was {io_error}"
            return SpineLoadError.SKELETON_READ_FAILED
        except Exception as load_err:
            self.last_error = f"Spine: Exception loading skeleton file: {load_err}"
            return SpineLoadError.SKELETON_READ_FAILED

        if skeleton_file is None:
            self.last_error = f"Spine: Skeleton file not found {skeleton_path}"
            return SpineLoadError.SKELETON_NOT_FOUND

        try:
            if hasattr(skeleton_file, 'read'):
                try:
                    skeleton_data_bytes = skeleton_file.read()
                finally:
                    skeleton_file.close()
            else:
                skeleton_data_bytes = skeleton_file
        except Exception as read_error:
            self.last_error = f"Spine: Could not read skeleton {skeleton_path}: {read_error}"
            return SpineLoadError.SKELETON_READ_FAILED

        if not skeleton_data_bytes:
            self.last_error = f"Spine: No skeleton data loaded from {skeleton_path}"
            return SpineLoadError.SKELETON_EMPTY

        if isinstance(skeleton_data_bytes, str):
            skeleton_data_bytes = skeleton_data_bytes.encode('utf-8')
        elif not isinstance(skeleton_data_bytes, bytes):
            self.last_error = f"Spine: Unexpected skeleton data type: {type(skeleton_data_bytes)}"
            return SpineLoadError.SKELETON_INVALID_TYPE

        skeleton_path_bytes = skeleton_path.encode('utf-8')

        if file_type == "json":
            # JSON loader expects a null-terminated string.
            if not skeleton_data_bytes.endswith(b'\0'):
                skeleton_data_bytes = skeleton_data_bytes + b'\0'
            skeleton_result = spine_skeleton_data_load_json(
                self.atlas, <const char*> skeleton_data_bytes, skeleton_path_bytes)
        else:
            skeleton_result = spine_skeleton_data_load_binary(
                self.atlas, <const uint8_t*><char*> skeleton_data_bytes,
                len(skeleton_data_bytes), skeleton_path_bytes)

        if skeleton_result == NULL:
            self.last_error = f"Spine: Failed to load skeleton: {skeleton_path}"
            return SpineLoadError.SKELETON_CREATE_FAILED

        error = spine_skeleton_data_result_get_error(skeleton_result)
        if error != NULL:
            error_message = error.decode('utf-8', 'replace')
            spine_skeleton_data_result_dispose(skeleton_result)
            self.last_error = f"Spine: Failed to parse skeleton {skeleton_path}: {error_message}"
            return SpineLoadError.SKELETON_PARSE_FAILED

        self.skeleton_data = spine_skeleton_data_result_get_data(skeleton_result)
        spine_skeleton_data_result_dispose(skeleton_result)

        if self.skeleton_data == NULL:
            self.last_error = f"Spine: Failed to load skeleton: {skeleton_path}"
            return SpineLoadError.SKELETON_CREATE_FAILED

        spine_log(f"Spine: Skeleton data loaded successfully: {skeleton_path}")

        self.data_x = spine_skeleton_data_get_x(self.skeleton_data)
        self.data_y = spine_skeleton_data_get_y(self.skeleton_data)
        self.data_w = spine_skeleton_data_get_width(self.skeleton_data)
        self.data_h = spine_skeleton_data_get_height(self.skeleton_data)

        self.loaded = True
        return SpineLoadError.OK


cdef class SpineModel:
    """A live character model with animation, physics, and rendering state."""

    # Retain shared native data for the drawable's lifetime.
    cdef SpineData data

    cdef spine_skeleton_drawable drawable
    cdef spine_skeleton skeleton
    cdef spine_animation_state animation_state

    cdef object page_names  # list of atlas page texture names, by page index
    cdef object texture_manager  # SpineTextureManager reference
    cdef bint loaded
    cdef readonly object last_error
    cdef object atlas_path
    cdef object skeleton_path
    cdef object current_skin
    cdef float scale
    cdef float scaleY
    cdef float scaleX

    # Translate model bounds to (0, 0) in render space.
    cdef bint has_bounds
    cdef float offset_x
    cdef float offset_y
    cdef float bounds_width
    cdef float bounds_height

    def __init__(self, scale=1.0, scaleX=None, scaleY=None):
        self.data = None
        self.drawable = NULL
        self.skeleton = NULL
        self.animation_state = NULL
        self.page_names = []
        self.texture_manager = None
        self.loaded = False
        self.last_error = None
        self.atlas_path = None
        self.skeleton_path = None
        self.current_skin = None
        self.scale = scale
        self.scaleX = scale if scaleX is None else scaleX
        self.scaleY = scale if scaleY is None else scaleY

        self.has_bounds = False
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.bounds_width = 0.0
        self.bounds_height = 0.0

    def __dealloc__(self):
        """Clean up Spine resources"""
        self.dispose()

    def dispose(self):
        """Dispose per-instance Spine resources"""

        # The drawable owns its skeleton, state, and renderer; SpineData owns shared data.
        if self.drawable != NULL:
            spine_skeleton_drawable_dispose(self.drawable)
            self.drawable = NULL
            self.skeleton = NULL
            self.animation_state = NULL

        self.data = None
        self.texture_manager = None
        self.page_names = []
        self.loaded = False

    def load_from_data(self, SpineData data, texture_manager):
        """Return a SpineLoadError; retain diagnostics in last_error."""
        cdef float sx_eff, sy_eff, x0, x1, y0, y1
        cdef float bx, by, bw, bh

        self.last_error = None
        if self.loaded:
            return SpineLoadError.OK

        if data is None or not data.loaded:
            self.last_error = "Spine: Shared skeleton data is not loaded"
            return SpineLoadError.SHARED_DATA_NOT_LOADED

        try:
            self.data = data
            self.texture_manager = texture_manager
            self.atlas_path = data.atlas_path
            self.skeleton_path = data.skeleton_path
            self.page_names = list(data.page_names)

            self.drawable = spine_skeleton_drawable_create(data.skeleton_data)
            if self.drawable == NULL:
                self.last_error = "Spine: Failed to create skeleton drawable"
                return SpineLoadError.DRAWABLE_CREATE_FAILED

            self.skeleton = spine_skeleton_drawable_get_skeleton(self.drawable)
            self.animation_state = spine_skeleton_drawable_get_animation_state(self.drawable)

            if self.skeleton == NULL or self.animation_state == NULL:
                self.last_error = "Spine: Failed to get skeleton or animation state from drawable"
                return SpineLoadError.DRAWABLE_STATE_UNAVAILABLE

            # Spine 4.3 already uses yDown; negating scaleY would cancel the flip.
            spine_skeleton_set_scale(self.skeleton, self.scaleX, self.scaleY)
            spine_skeleton_setup_pose(self.skeleton)
            spine_skeleton_update_world_transform(self.skeleton, SPINE_PHYSICS_RESET)

            # Use stable editor bounds; yDown maps Y to -Y * scaleY.
            # Min/max handles mirrored scales.
            if data.data_w > 0.0 and data.data_h > 0.0:
                sx_eff = self.scaleX
                sy_eff = self.scaleY * -1.0

                x0 = data.data_x * sx_eff
                x1 = (data.data_x + data.data_w) * sx_eff
                y0 = data.data_y * sy_eff
                y1 = (data.data_y + data.data_h) * sy_eff

                self.offset_x = -fmin(x0, x1)
                self.offset_y = -fmin(y0, y1)
                self.bounds_width = fmax(x0, x1) - fmin(x0, x1)
                self.bounds_height = fmax(y0, y1) - fmin(y0, y1)
                self.has_bounds = True
                spine_log(f"Spine: Using editor bounds: offset=({self.offset_x}, {self.offset_y}) size=({self.bounds_width}, {self.bounds_height})")
            else:
                # Older exports need measured setup bounds, already scaled and Y-flipped.
                bx = 0.0
                by = 0.0
                bw = 0.0
                bh = 0.0
                spine_skeleton_get_bounds_1(self.skeleton, &bx, &by, &bw, &bh)

                if bw > 0.0 and bh > 0.0:
                    self.offset_x = -bx
                    self.offset_y = -by
                    self.bounds_width = bw
                    self.bounds_height = bh
                    self.has_bounds = True
                    spine_log(f"Spine: Using computed bounds: offset=({self.offset_x}, {self.offset_y}) size=({self.bounds_width}, {self.bounds_height})")
                else:
                    self.has_bounds = False
                    spine_log("Spine: No usable bounds - rendering with the skeleton origin at (0, 0)")

            self.loaded = True
            return SpineLoadError.OK

        except Exception as e:
            spine_log(f"Spine: Error in load_from_data: {e}")
            self.last_error = f"Spine: Error in load_from_data: {e}"
            return SpineLoadError.MODEL_INITIALIZATION_FAILED
        finally:
            if not self.loaded:
                self.dispose()

    def is_loaded(self):
        """Check if model is loaded"""
        return self.loaded

    def get_size(self):
        """Returns the model's (width, height) in render space, or None if
        no usable bounds were found at load time."""
        if not self.loaded or not self.has_bounds:
            return None
        return (self.bounds_width, self.bounds_height)

    def get_offset(self):
        """Returns the (x, y) translation applied to rendered vertices so
        the model's bounding box starts at (0, 0)."""
        if not self.loaded or not self.has_bounds:
            return (0.0, 0.0)
        return (self.offset_x, self.offset_y)

    cdef int _find_animation_ok(self, animation_name_bytes) except -1:
        """1 if the animation exists, 0 otherwise. spine-cpp asserts (crashing
        the process) on an unknown name, so every set path guards with this."""
        if spine_skeleton_data_find_animation(self.data.skeleton_data, animation_name_bytes) == NULL:
            return 0
        return 1

    def apply_animation_reset(self, track_index, animation_name, loop):
        """Restart an animation from the setup pose and reset physics."""
        cdef spine_track_entry entry

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            animation_name_bytes = animation_name.encode('utf-8')
            if not self._find_animation_ok(animation_name_bytes):
                spine_log(f"Spine: Unknown animation '{animation_name}', ignoring.", debug=False)
                return False

            # Clear only this track to prevent automatic mixing while preserving overlays.
            spine_animation_state_clear_track(self.animation_state, track_index)
            spine_skeleton_setup_pose(self.skeleton)
            entry = spine_animation_state_set_animation_1(
                self.animation_state,
                track_index,
                animation_name_bytes,
                1 if loop else 0
            )
            # Reset physics explicitly; ordinary updates preserve velocities.
            spine_skeleton_update_world_transform(self.skeleton, SPINE_PHYSICS_RESET)
            return entry != NULL

        except Exception as e:
            spine_log(f"Spine: Error in apply_animation_reset: {e}")
            return False

    def apply_animation_mix(self, track_index, animation_name, loop, mix_time):
        """Blend into an animation while preserving ongoing motion.
        A negative mix_time uses the default blend duration."""
        cdef spine_track_entry entry
        cdef float mt

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            animation_name_bytes = animation_name.encode('utf-8')
            if not self._find_animation_ok(animation_name_bytes):
                spine_log(f"Spine: Unknown animation '{animation_name}', ignoring.", debug=False)
                return False

            entry = spine_animation_state_set_animation_1(
                self.animation_state,
                track_index,
                animation_name_bytes,
                1 if loop else 0
            )
            if entry == NULL:
                return False

            if mix_time is not None and mix_time >= 0.0:
                mt = mix_time
                spine_track_entry_set_mix_duration_1(entry, mt)

            return True

        except Exception as e:
            spine_log(f"Spine: Error in apply_animation_mix: {e}")
            return False

    def apply_overlay_animation(self, track_index, animation_name, loop, mix_time, alpha, additive):
        """Start a layered animation with its blend weight and playback settings."""
        cdef spine_track_entry entry
        cdef float mt, a

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            animation_name_bytes = animation_name.encode('utf-8')
            if not self._find_animation_ok(animation_name_bytes):
                spine_log(f"Spine: Unknown animation '{animation_name}', ignoring.", debug=False)
                return False

            entry = spine_animation_state_set_animation_1(
                self.animation_state,
                track_index,
                animation_name_bytes,
                1 if loop else 0
            )
            if entry == NULL:
                return False

            if mix_time is not None and mix_time >= 0.0:
                mt = mix_time
                spine_track_entry_set_mix_duration_1(entry, mt)

            a = alpha
            spine_track_entry_set_alpha(entry, a)
            spine_track_entry_set_additive(entry, 1 if additive else 0)
            return True

        except Exception as e:
            spine_log(f"Spine: Error in apply_overlay_animation: {e}")
            return False

    def update_track_settings(self, track_index, loop, alpha, additive):
        """Change playback settings without restarting the animation.
        Return False if the track cannot be updated."""
        cdef spine_array_track_entry tracks
        cdef spine_track_entry* buffer
        cdef spine_track_entry entry
        cdef size_t count, idx
        cdef float a

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            if track_index < 0:
                return False
            idx = track_index

            tracks = spine_animation_state_get_tracks(self.animation_state)
            if tracks == NULL:
                return False

            count = spine_array_track_entry_size(tracks)
            buffer = spine_array_track_entry_buffer(tracks)
            if buffer == NULL or idx >= count:
                return False

            entry = buffer[idx]
            if entry == NULL:
                return False

            spine_track_entry_set_loop(entry, 1 if loop else 0)
            a = alpha
            spine_track_entry_set_alpha(entry, a)
            spine_track_entry_set_additive(entry, 1 if additive else 0)
            return True

        except Exception as e:
            spine_log(f"Spine: Error in update_track_settings: {e}")
            return False

    def fade_track(self, track_index, mix_out):
        """Fade out a track over the requested duration."""
        cdef float mt

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            mt = mix_out if (mix_out is not None and mix_out >= 0.0) else 0.0
            spine_animation_state_set_empty_animation(self.animation_state, track_index, mt)
            return True
        except Exception as e:
            spine_log(f"Spine: Error in fade_track: {e}")
            return False

    def clear_track(self, track_index):
        """Immediately clear a single track (no fade)."""
        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            spine_animation_state_clear_track(self.animation_state, track_index)
            return True
        except Exception as e:
            spine_log(f"Spine: Error in clear_track: {e}")
            return False

    def set_default_mix(self, mix_time):
        """Set the fallback duration for animation blends."""
        cdef spine_animation_state_data data
        cdef float mt

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            data = spine_animation_state_get_data(self.animation_state)
            if data == NULL:
                return False
            mt = mix_time
            spine_animation_state_data_set_default_mix(data, mt)
            return True
        except Exception as e:
            spine_log(f"Spine: Error in set_default_mix: {e}")
            return False

    def set_pair_mix(self, from_name, to_name, mix_time):
        """Set the blend duration between two named animations."""
        cdef spine_animation_state_data data
        cdef float mt

        if not self.loaded or self.animation_state == NULL:
            return False

        try:
            data = spine_animation_state_get_data(self.animation_state)
            if data == NULL:
                return False
            from_bytes = from_name.encode('utf-8')
            to_bytes = to_name.encode('utf-8')
            mt = mix_time
            spine_animation_state_data_set_mix_2(data, <const char*> from_bytes, <const char*> to_bytes, mt)
            return True
        except Exception as e:
            spine_log(f"Spine: Error in set_pair_mix: {e}")
            return False

    def update_animation(self, delta_time):
        """Advance animation and physics by the elapsed time."""
        if not self.loaded or self.drawable == NULL:
            return

        try:
            spine_skeleton_drawable_update(self.drawable, delta_time)

        except Exception as e:
            spine_log(f"Spine: Error updating animation: {e}")

    def should_animate(self):
        """Return whether an animation is playing, blending, or waiting to play."""
        cdef spine_array_track_entry tracks
        cdef spine_track_entry* buffer
        cdef spine_track_entry entry
        cdef size_t count, i

        if not self.loaded or self.animation_state == NULL:
            return False

        tracks = spine_animation_state_get_tracks(self.animation_state)
        if tracks == NULL:
            return False

        count = spine_array_track_entry_size(tracks)
        buffer = spine_array_track_entry_buffer(tracks)
        if count == 0 or buffer == NULL:
            return False

        for i in range(count):
            entry = buffer[i]
            if entry == NULL:            # unset track slot - the array has NULL gaps
                continue
            if spine_track_entry_get_loop(entry) != 0:
                return True
            if spine_track_entry_is_complete(entry) == 0:
                return True
            if spine_track_entry_get_mixing_from(entry) != NULL:
                return True
            if spine_track_entry_get_next(entry) != NULL:
                return True

        return False

    def physics_active(self):
        """Return whether physics requires continued updates.
        Active constraints may need updates even when the character looks still."""
        cdef spine_array_physics_constraint constraints
        cdef spine_physics_constraint* buffer
        cdef spine_physics_constraint constraint
        cdef spine_physics_constraint_pose pose
        cdef size_t count, i

        if not self.loaded or self.skeleton == NULL:
            return False

        constraints = spine_skeleton_get_physics_constraints(self.skeleton)
        if constraints == NULL:
            return False

        count = spine_array_physics_constraint_size(constraints)
        buffer = spine_array_physics_constraint_buffer(constraints)
        if count == 0 or buffer == NULL:
            return False

        for i in range(count):
            constraint = buffer[i]
            if constraint == NULL:
                continue
            if spine_physics_constraint_is_active(constraint) == 0:
                continue
            pose = spine_physics_constraint_get_applied_pose(constraint)
            if pose == NULL:
                continue
            if spine_physics_constraint_pose_get_mix(pose) > 0.0:
                return True

        return False

    def needs_next_frame(self):
        """Return whether animation or physics needs another frame."""
        return self.should_animate() or self.physics_active()

    def render_runs(self):
        """Build drawable meshes for the current frame, preserving drawing order."""
        if not self.loaded or self.drawable == NULL:
            return []

        cdef spine_render_command command
        cdef int32_t num_vertices, num_indices
        cdef uint32_t* colors
        cdef int page_index, blend_mode
        cdef int j
        cdef bint visible
        cdef list commands = []     # (command as intptr, page_index, blend_mode, vertices, triangles)
        cdef list runs = []
        cdef list group

        try:
            command = spine_skeleton_drawable_render(self.drawable)

            while command != NULL:
                num_vertices = spine_render_command_get_num_vertices(command)
                num_indices = spine_render_command_get_num_indices(command)

                if (num_vertices <= 0 or num_indices < 3
                        or spine_render_command_get_positions(command) == NULL
                        or spine_render_command_get_uvs(command) == NULL
                        or spine_render_command_get_indices(command) == NULL):
                    command = spine_render_command_get_next(command)
                    continue

                # Native texture pointers encode page indices.
                page_index = <int><intptr_t> spine_render_command_get_texture(command)
                if not (0 <= page_index < len(self.page_names)) or not self.page_names[page_index]:
                    spine_log(f"Spine: render command has unknown page index {page_index}")
                    command = spine_render_command_get_next(command)
                    continue

                colors = spine_render_command_get_colors(command)
                visible = True
                if colors != NULL:
                    visible = False
                    for j in range(num_vertices):
                        if (colors[j] >> 24) & 0xff:
                            visible = True
                            break
                if not visible:
                    command = spine_render_command_get_next(command)
                    continue

                blend_mode = spine_render_command_get_blend_mode(command)
                commands.append((<intptr_t> command, page_index, blend_mode, <int> num_vertices, <int> (num_indices // 3)))
                command = spine_render_command_get_next(command)

            group = []
            for entry in commands:
                if group and (entry[1] != group[0][1] or entry[2] != group[0][2]):
                    runs.append(self._build_run(group))
                    group = []
                group.append(entry)
            if group:
                runs.append(self._build_run(group))

            return [r for r in runs if r is not None]

        except Exception as e:
            spine_log(f"Spine: error building render runs: {e}")
            traceback.print_exc()
            return []

    cdef object _build_run(self, list group):
        """Build an owned mesh for a group of compatible drawing commands.
        Return None if its size exceeds the mesh limits."""
        cdef Mesh2 mesh
        cdef spine_render_command command
        cdef float* positions
        cdef float* uvs
        cdef uint32_t* colors
        cdef uint32_t* dark_colors
        cdef uint16_t* indices
        cdef uint32_t packed
        cdef int32_t num_vertices, num_indices
        cdef int j, base, tri, v, a
        cdef long long total_vertices = 0
        cdef long long total_triangles = 0
        cdef float offset_x, offset_y

        for entry in group:
            total_vertices += entry[3]
            total_triangles += entry[4]

        if total_vertices < 3 or total_triangles < 1:
            return None
        if total_vertices > INT_MAX or total_triangles * 3 > INT_MAX:
            spine_log("Spine: render run too large for a mesh; dropping it")
            return None

        offset_x = self.offset_x if self.has_bounds else 0.0
        offset_y = self.offset_y if self.has_bounds else 0.0

        mesh = Mesh2(SPINE_LAYOUT, <int> total_vertices, <int> total_triangles)
        mesh.points = <int> total_vertices
        mesh.triangles = <int> total_triangles

        base = 0   # running vertex base, for rebasing each command's indices
        tri = 0    # running flat triangle-index cursor

        for entry in group:
            command = <spine_render_command><intptr_t> entry[0]
            num_vertices = spine_render_command_get_num_vertices(command)
            num_indices = spine_render_command_get_num_indices(command)
            positions = spine_render_command_get_positions(command)
            uvs = spine_render_command_get_uvs(command)
            colors = spine_render_command_get_colors(command)
            dark_colors = spine_render_command_get_dark_colors(command)
            indices = spine_render_command_get_indices(command)

            for j in range(num_vertices):
                v = (base + j) * 2
                a = (base + j) * SPINE_STRIDE

                mesh.point_data[v] = positions[j * 2] + offset_x
                mesh.point_data[v + 1] = positions[j * 2 + 1] + offset_y

                mesh.attribute[a] = uvs[j * 2]
                mesh.attribute[a + 1] = uvs[j * 2 + 1]

                # Light color, packed (a << 24) | (r << 16) | (g << 8) | b.
                if colors != NULL:
                    packed = colors[j]
                    mesh.attribute[a + 2] = ((packed >> 16) & 0xff) / 255.0
                    mesh.attribute[a + 3] = ((packed >> 8) & 0xff) / 255.0
                    mesh.attribute[a + 4] = (packed & 0xff) / 255.0
                    mesh.attribute[a + 5] = ((packed >> 24) & 0xff) / 255.0
                else:
                    mesh.attribute[a + 2] = 1.0
                    mesh.attribute[a + 3] = 1.0
                    mesh.attribute[a + 4] = 1.0
                    mesh.attribute[a + 5] = 1.0

                # Dark color, same rgb layout; the alpha byte is always 0xff
                # and carries no information. Zero rgb is the neutral tint.
                if dark_colors != NULL:
                    packed = dark_colors[j]
                    mesh.attribute[a + 6] = ((packed >> 16) & 0xff) / 255.0
                    mesh.attribute[a + 7] = ((packed >> 8) & 0xff) / 255.0
                    mesh.attribute[a + 8] = (packed & 0xff) / 255.0
                else:
                    mesh.attribute[a + 6] = 0.0
                    mesh.attribute[a + 7] = 0.0
                    mesh.attribute[a + 8] = 0.0

            # Rebase native 16-bit indices into owned 32-bit mesh storage.
            for j in range((num_indices // 3) * 3):
                mesh.triangle[tri] = <unsigned int> indices[j] + <unsigned int> base
                tri += 1

            base += num_vertices

        first = group[0]
        return SpineRun(first[1], self.page_names[first[1]], first[2], mesh,
                        <int> total_vertices, <int> total_triangles, len(group))

    def run_render(self, run, texture, width, height):
        """Prepare a mesh for drawing with its texture, tint, and blend settings."""
        cdef Render render

        try:
            render = Render(width, height)
            render.mesh = run.mesh

            render.add_shader("renpy.texture")
            render.add_shader("spine.colors")

            # Blend factors use Ren'Py's premultiplied-alpha convention.
            blend_mode = run.blend_mode
            if blend_mode == SPINE_BLEND_MODE_ADDITIVE:
                render.add_property("blend_func", (GL_FUNC_ADD, GL_ONE, GL_ONE, GL_FUNC_ADD, GL_ZERO, GL_ONE))
            elif blend_mode == SPINE_BLEND_MODE_MULTIPLY:
                render.add_property("blend_func", (GL_FUNC_ADD, GL_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA, GL_FUNC_ADD, GL_ZERO, GL_ONE))
            elif blend_mode == SPINE_BLEND_MODE_SCREEN:
                render.add_property("blend_func", (GL_FUNC_ADD, GL_ONE, GL_ONE_MINUS_SRC_COLOR, GL_FUNC_ADD, GL_ZERO, GL_ONE))

            # Sampling is constant within a single-page run.
            if self.data is not None:
                for name, value in self.data.page_render_properties(run.page_index).items():
                    render.add_property(name, value)

            render.blit(texture, (0, 0))
            return render

        except Exception as e:
            spine_log(f"Spine: error creating run render: {e}")
            traceback.print_exc()
            return None

    def debug_render_items(self):
        """Return the current drawing commands as Python data for diagnostics."""
        if not self.loaded or self.drawable == NULL:
            return []

        cdef spine_render_command command
        cdef int32_t num_vertices, num_indices
        cdef float* positions
        cdef float* uvs
        cdef uint32_t* colors
        cdef uint32_t* dark_colors
        cdef uint16_t* indices
        cdef uint32_t packed
        cdef int j, page_index
        cdef float offset_x, offset_y
        cdef list items = []

        offset_x = self.offset_x if self.has_bounds else 0.0
        offset_y = self.offset_y if self.has_bounds else 0.0

        command = spine_skeleton_drawable_render(self.drawable)
        while command != NULL:
            num_vertices = spine_render_command_get_num_vertices(command)
            num_indices = spine_render_command_get_num_indices(command)
            positions = spine_render_command_get_positions(command)
            uvs = spine_render_command_get_uvs(command)
            colors = spine_render_command_get_colors(command)
            dark_colors = spine_render_command_get_dark_colors(command)
            indices = spine_render_command_get_indices(command)
            page_index = <int><intptr_t> spine_render_command_get_texture(command)

            item = {
                "page_index": page_index,
                "page_key": self.page_names[page_index] if 0 <= page_index < len(self.page_names) else None,
                "blend_mode": spine_render_command_get_blend_mode(command),
                "positions": [], "uvs": [], "colors": [], "dark_colors": [], "indices": [],
            }
            if positions != NULL and uvs != NULL:
                for j in range(num_vertices):
                    item["positions"].extend((positions[j * 2] + offset_x, positions[j * 2 + 1] + offset_y))
                    item["uvs"].extend((uvs[j * 2], uvs[j * 2 + 1]))
            for j in range(num_vertices):
                packed = colors[j] if colors != NULL else 0xffffffff
                item["colors"].extend((((packed >> 16) & 0xff) / 255.0, ((packed >> 8) & 0xff) / 255.0,
                                       (packed & 0xff) / 255.0, ((packed >> 24) & 0xff) / 255.0))
                packed = dark_colors[j] if dark_colors != NULL else 0
                item["dark_colors"].extend((((packed >> 16) & 0xff) / 255.0, ((packed >> 8) & 0xff) / 255.0,
                                            (packed & 0xff) / 255.0))
            if indices != NULL:
                for j in range(num_indices):
                    item["indices"].append(indices[j])
            items.append(item)
            command = spine_render_command_get_next(command)

        return items

    def get_animation_names(self):
        """Get list of available animation names"""
        if not self.loaded or self.data is None:
            return []

        cdef list animation_names = []
        cdef spine_array_animation animations
        cdef spine_animation* animation_buffer
        cdef spine_animation animation
        cdef size_t count, i
        cdef const char* name

        try:
            animations = spine_skeleton_data_get_animations(self.data.skeleton_data)
            if animations == NULL:
                spine_log("Spine: No animations found in skeleton data")
                return []

            count = spine_array_animation_size(animations)
            animation_buffer = spine_array_animation_buffer(animations)

            if count <= 0 or animation_buffer == NULL:
                spine_log("Spine: No animations found in skeleton data")
                return []

            for i in range(count):
                animation = animation_buffer[i]
                if animation != NULL:
                    name = spine_animation_get_name(animation)
                    if name != NULL:
                        animation_names.append(name.decode('utf-8'))

            return animation_names
        except Exception as e:
            spine_log(f"Spine: Error getting animation names: {e}")
            return []

    def find_animation(self, animation_name):
        """Find animation by name"""
        if not self.loaded or self.data is None:
            return None

        cdef spine_animation animation
        cdef const char* name

        try:
            animation_name_bytes = animation_name.encode('utf-8')
            animation = spine_skeleton_data_find_animation(self.data.skeleton_data, animation_name_bytes)
            if animation == NULL:
                return None

            name = spine_animation_get_name(animation)
            return {
                "name": name.decode('utf-8') if name != NULL else "unknown",
                "duration": float(spine_animation_get_duration(animation))
            }
        except Exception as e:
            spine_log(f"Spine: Error finding animation '{animation_name}': {e}")
            return None

    def get_skin_names(self):
        """Get list of available skin names"""
        if not self.loaded or self.data is None:
            return []

        cdef list skin_names = []
        cdef spine_array_skin skins
        cdef spine_skin* skin_buffer
        cdef spine_skin skin
        cdef size_t count, i
        cdef const char* name

        try:
            skins = spine_skeleton_data_get_skins(self.data.skeleton_data)
            if skins == NULL:
                spine_log("Spine: No skins found in skeleton data")
                return []

            count = spine_array_skin_size(skins)
            skin_buffer = spine_array_skin_buffer(skins)

            if count <= 0 or skin_buffer == NULL:
                spine_log("Spine: No skins found in skeleton data")
                return []

            spine_log(f"Spine: Found {count} skins")

            for i in range(count):
                skin = skin_buffer[i]
                if skin != NULL:
                    name = spine_skin_get_name(skin)
                    if name != NULL:
                        skin_names.append(name.decode('utf-8'))

            return skin_names
        except Exception as e:
            spine_log(f"Spine: Error getting skin names: {e}")
            return []

    def find_skin(self, skin_name):
        """Find skin by name"""
        if not self.loaded or self.data is None:
            return None

        cdef spine_skin skin
        cdef const char* name

        try:
            skin_name_bytes = skin_name.encode('utf-8')
            skin = spine_skeleton_data_find_skin(self.data.skeleton_data, skin_name_bytes)
            if skin == NULL:
                return None

            name = spine_skin_get_name(skin)
            return {
                "name": name.decode('utf-8') if name != NULL else "unknown",
            }
        except Exception as e:
            spine_log(f"Spine: Error finding skin '{skin_name}': {e}")
            return None

    def apply_skin_combined(self, names, setup_slots):
        """Apply skins in order, with later skins taking precedence.
        Empty input restores the default skin. Animation and physics continue."""
        cdef spine_skin combined

        if not self.loaded or self.skeleton == NULL or self.data is None:
            return False

        try:
            # Unknown skin names assert inside spine-cpp.
            valid = []
            if names:
                for n in names:
                    if n is None:
                        continue
                    if spine_skeleton_data_find_skin(self.data.skeleton_data, n.encode('utf-8')) != NULL:
                        valid.append(n)
                    else:
                        spine_log(f"Spine: Unknown skin '{n}', ignoring.", debug=False)

            if not valid:
                spine_skeleton_set_skin_2(self.skeleton, NULL)
                self.current_skin = None
            elif len(valid) == 1:
                spine_skeleton_set_skin_1(self.skeleton, valid[0].encode('utf-8'))
                self.current_skin = valid[0]
            else:
                combined = self.data._get_combined_skin(tuple(valid))
                if combined == NULL:
                    return False
                spine_skeleton_set_skin_2(self.skeleton, combined)
                self.current_skin = tuple(valid)

            if setup_slots:
                spine_skeleton_setup_pose_slots(self.skeleton)

            return True
        except Exception as e:
            spine_log(f"Spine: Error in apply_skin_combined: {e}")
            return False

    def apply_skin(self, skin_name, setup_slots):
        """Change the skin while animation and physics continue.
        Optionally restore the new skin’s default attachments."""
        spine_log(f"Spine: apply_skin '{skin_name}' setup_slots={setup_slots} (from '{self.current_skin}')")

        if not self.loaded or self.skeleton == NULL or self.data is None:
            spine_log(f"Spine: Cannot set skin '{skin_name}' - model not loaded")
            return False
        try:
            if skin_name is None:
                spine_skeleton_set_skin_2(self.skeleton, NULL)
                if setup_slots:
                    spine_skeleton_setup_pose_slots(self.skeleton)
                self.current_skin = None
                spine_log("Spine: Reset to default skin")
                return True

            skin_name_bytes = skin_name.encode('utf-8')

            # Unknown skin names assert inside spine-cpp.
            if spine_skeleton_data_find_skin(self.data.skeleton_data, skin_name_bytes) == NULL:
                spine_log(f"Spine: Unknown skin '{skin_name}', ignoring.", debug=False)
                return False

            spine_skeleton_set_skin_1(self.skeleton, skin_name_bytes)
            if setup_slots:
                spine_skeleton_setup_pose_slots(self.skeleton)
            self.current_skin = skin_name
            spine_log(f"Spine: Skin set to '{skin_name}'")
            return True
        except Exception as e:
            spine_log(f"Spine: Error setting skin '{skin_name}': {e}")
            return False

    def get_current_skin_name(self):
        """Get the name of the currently applied skin"""
        if not self.loaded or self.skeleton == NULL:
            return None

        cdef spine_skin current_skin
        cdef const char* name

        try:
            current_skin = spine_skeleton_get_skin(self.skeleton)
            if current_skin == NULL:
                return None

            name = spine_skin_get_name(current_skin)
            if name == NULL:
                return None

            return name.decode('utf-8')
        except Exception as e:
            spine_log(f"Spine: Error getting current skin name: {e}")
            return None
