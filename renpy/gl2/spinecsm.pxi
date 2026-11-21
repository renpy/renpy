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

# Spine-C 4.3 opaque handles and dynamically resolved function pointers.


from libc.stdint cimport uint8_t, uint16_t, uint32_t, int32_t, intptr_t

# Blend mode constants (matching spine_blend_mode)
cdef enum:
    SPINE_BLEND_MODE_NORMAL = 0
    SPINE_BLEND_MODE_ADDITIVE = 1
    SPINE_BLEND_MODE_MULTIPLY = 2
    SPINE_BLEND_MODE_SCREEN = 3

# Physics constants (matching spine_physics)
cdef enum:
    SPINE_PHYSICS_NONE = 0
    SPINE_PHYSICS_RESET = 1
    SPINE_PHYSICS_UPDATE = 2
    SPINE_PHYSICS_POSE = 3

# Atlas page sampling (matching spine_texture_filter / spine_texture_wrap)
cdef enum:
    SPINE_TEXTURE_FILTER_UNKNOWN = 0
    SPINE_TEXTURE_FILTER_NEAREST = 1
    SPINE_TEXTURE_FILTER_LINEAR = 2
    SPINE_TEXTURE_FILTER_MIP_MAP = 3
    SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_NEAREST = 4
    SPINE_TEXTURE_FILTER_MIP_MAP_LINEAR_NEAREST = 5
    SPINE_TEXTURE_FILTER_MIP_MAP_NEAREST_LINEAR = 6
    SPINE_TEXTURE_FILTER_MIP_MAP_LINEAR_LINEAR = 7

cdef enum:
    SPINE_TEXTURE_WRAP_MIRRORED_REPEAT = 0
    SPINE_TEXTURE_WRAP_CLAMP_TO_EDGE = 1
    SPINE_TEXTURE_WRAP_REPEAT = 2

# Opaque handle types. The real types are pointers to C++ objects; only the
# spine-c API ever looks inside them.
ctypedef void* spine_atlas
ctypedef void* spine_atlas_result
ctypedef void* spine_atlas_page
ctypedef void* spine_array_atlas_page
ctypedef void* spine_skeleton_data
ctypedef void* spine_skeleton_data_result
ctypedef void* spine_skeleton
ctypedef void* spine_skeleton_drawable
ctypedef void* spine_animation_state
ctypedef void* spine_animation_state_data
ctypedef void* spine_animation
ctypedef void* spine_array_animation
ctypedef void* spine_skin
ctypedef void* spine_array_skin
ctypedef void* spine_track_entry
ctypedef void* spine_array_track_entry
ctypedef void* spine_render_command
ctypedef void* spine_physics_constraint
ctypedef void* spine_array_physics_constraint
ctypedef void* spine_physics_constraint_pose


# Version
ctypedef int32_t (*spine_major_versionType)()

ctypedef int32_t (*spine_minor_versionType)()

# Atlas
ctypedef spine_atlas_result (*spine_atlas_loadType)(const char*)

ctypedef const char* (*spine_atlas_result_get_errorType)(spine_atlas_result)

ctypedef spine_atlas (*spine_atlas_result_get_atlasType)(spine_atlas_result)

ctypedef void (*spine_atlas_result_disposeType)(spine_atlas_result)

ctypedef void (*spine_atlas_disposeType)(spine_atlas)

ctypedef spine_array_atlas_page (*spine_atlas_get_pagesType)(spine_atlas)

ctypedef size_t (*spine_array_atlas_page_sizeType)(spine_array_atlas_page)

ctypedef spine_atlas_page* (*spine_array_atlas_page_bufferType)(spine_array_atlas_page)

ctypedef const char* (*spine_atlas_page_get_nameType)(spine_atlas_page)

ctypedef int (*spine_atlas_page_get_indexType)(spine_atlas_page)

# Filter/wrap values use spine_texture_* enums.
ctypedef int (*spine_atlas_page_get_min_filterType)(spine_atlas_page)
ctypedef int (*spine_atlas_page_get_mag_filterType)(spine_atlas_page)
ctypedef int (*spine_atlas_page_get_u_wrapType)(spine_atlas_page)
ctypedef int (*spine_atlas_page_get_v_wrapType)(spine_atlas_page)
ctypedef uint8_t (*spine_atlas_page_get_pmaType)(spine_atlas_page)


# Skeleton data loading
ctypedef spine_skeleton_data_result (*spine_skeleton_data_load_jsonType)(spine_atlas, const char*, const char*)

ctypedef spine_skeleton_data_result (*spine_skeleton_data_load_binaryType)(spine_atlas, const uint8_t*, int32_t, const char*)

ctypedef const char* (*spine_skeleton_data_result_get_errorType)(spine_skeleton_data_result)

ctypedef spine_skeleton_data (*spine_skeleton_data_result_get_dataType)(spine_skeleton_data_result)

ctypedef void (*spine_skeleton_data_result_disposeType)(spine_skeleton_data_result)

ctypedef void (*spine_skeleton_data_disposeType)(spine_skeleton_data)

# Skeleton data access
ctypedef spine_animation (*spine_skeleton_data_find_animationType)(spine_skeleton_data, const char*)

ctypedef spine_array_animation (*spine_skeleton_data_get_animationsType)(spine_skeleton_data)

ctypedef spine_skin (*spine_skeleton_data_find_skinType)(spine_skeleton_data, const char*)

ctypedef spine_array_skin (*spine_skeleton_data_get_skinsType)(spine_skeleton_data)

# Setup-pose AABB authored by the Spine editor, in skeleton coordinates.
ctypedef float (*spine_skeleton_data_get_xType)(spine_skeleton_data)

ctypedef float (*spine_skeleton_data_get_yType)(spine_skeleton_data)

ctypedef float (*spine_skeleton_data_get_widthType)(spine_skeleton_data)

ctypedef float (*spine_skeleton_data_get_heightType)(spine_skeleton_data)

ctypedef size_t (*spine_array_animation_sizeType)(spine_array_animation)

ctypedef spine_animation* (*spine_array_animation_bufferType)(spine_array_animation)

ctypedef size_t (*spine_array_skin_sizeType)(spine_array_skin)

ctypedef spine_skin* (*spine_array_skin_bufferType)(spine_array_skin)

ctypedef const char* (*spine_animation_get_nameType)(spine_animation)

ctypedef float (*spine_animation_get_durationType)(spine_animation)

ctypedef const char* (*spine_skin_get_nameType)(spine_skin)

# Composed skins are owned; merged attachments are shared and refcounted.
# Later skins override earlier attachments for the same slot.
ctypedef spine_skin (*spine_skin_createType)(const char*)

ctypedef void (*spine_skin_add_skinType)(spine_skin, spine_skin)

ctypedef void (*spine_skin_disposeType)(spine_skin)


# Skeleton drawable (owns skeleton + animation state + renderer)
ctypedef spine_skeleton_drawable (*spine_skeleton_drawable_createType)(spine_skeleton_data)

ctypedef void (*spine_skeleton_drawable_updateType)(spine_skeleton_drawable, float)

ctypedef spine_render_command (*spine_skeleton_drawable_renderType)(spine_skeleton_drawable)

ctypedef void (*spine_skeleton_drawable_disposeType)(spine_skeleton_drawable)

ctypedef spine_skeleton (*spine_skeleton_drawable_get_skeletonType)(spine_skeleton_drawable)

ctypedef spine_animation_state (*spine_skeleton_drawable_get_animation_stateType)(spine_skeleton_drawable)

# Skeleton
ctypedef void (*spine_skeleton_set_scaleType)(spine_skeleton, float, float)

ctypedef void (*spine_skeleton_setup_poseType)(spine_skeleton)

ctypedef void (*spine_skeleton_setup_pose_slotsType)(spine_skeleton)

ctypedef void (*spine_skeleton_set_skin_1Type)(spine_skeleton, const char*)

ctypedef void (*spine_skeleton_set_skin_2Type)(spine_skeleton, spine_skin)

ctypedef void (*spine_skeleton_update_world_transformType)(spine_skeleton, int)

ctypedef spine_skin (*spine_skeleton_get_skinType)(spine_skeleton)

# Computes the current-pose AABB in world (post scale/flip) coordinates.
ctypedef void (*spine_skeleton_get_bounds_1Type)(spine_skeleton, float*, float*, float*, float*)


# Animation state
ctypedef spine_track_entry (*spine_animation_state_set_animation_1Type)(spine_animation_state, size_t, const char*, uint8_t)

ctypedef void (*spine_animation_state_clear_tracksType)(spine_animation_state)

# Per-entry mix duration overrides the data-level default.
ctypedef spine_animation_state_data (*spine_animation_state_get_dataType)(spine_animation_state)

ctypedef void (*spine_animation_state_data_set_default_mixType)(spine_animation_state_data, float)

ctypedef void (*spine_animation_state_data_set_mix_2Type)(spine_animation_state_data, const char*, const char*, float)

ctypedef void (*spine_track_entry_set_mix_duration_1Type)(spine_track_entry, float)

ctypedef spine_track_entry (*spine_animation_state_add_animation_1Type)(spine_animation_state, size_t, const char*, uint8_t, float)

ctypedef spine_track_entry (*spine_animation_state_set_empty_animationType)(spine_animation_state, size_t, float)

ctypedef void (*spine_animation_state_clear_trackType)(spine_animation_state, size_t)

ctypedef float (*spine_track_entry_get_alphaType)(spine_track_entry)

ctypedef void (*spine_track_entry_set_alphaType)(spine_track_entry, float)

# Set additive before apply(); C ABI bool is uint8_t.
ctypedef uint8_t (*spine_track_entry_get_additiveType)(spine_track_entry)

ctypedef void (*spine_track_entry_set_additiveType)(spine_track_entry, uint8_t)

# C ABI bool returns occupy one byte.
ctypedef spine_array_track_entry (*spine_animation_state_get_tracksType)(spine_animation_state)

ctypedef size_t (*spine_array_track_entry_sizeType)(spine_array_track_entry)

ctypedef spine_track_entry* (*spine_array_track_entry_bufferType)(spine_array_track_entry)

ctypedef uint8_t (*spine_track_entry_is_completeType)(spine_track_entry)

ctypedef uint8_t (*spine_track_entry_get_loopType)(spine_track_entry)

ctypedef void (*spine_track_entry_set_loopType)(spine_track_entry, uint8_t)

ctypedef spine_track_entry (*spine_track_entry_get_mixing_fromType)(spine_track_entry)

ctypedef spine_track_entry (*spine_track_entry_get_nextType)(spine_track_entry)


# Render commands
ctypedef float* (*spine_render_command_get_positionsType)(spine_render_command)

ctypedef float* (*spine_render_command_get_uvsType)(spine_render_command)

ctypedef uint32_t* (*spine_render_command_get_colorsType)(spine_render_command)

# Per-vertex dark (tint black) colors, packed 0xff000000 | r<<16 | g<<8 | b by
# spine-cpp's SkeletonRenderer; rgb 0 for slots without a dark color.
ctypedef uint32_t* (*spine_render_command_get_dark_colorsType)(spine_render_command)

ctypedef int32_t (*spine_render_command_get_num_verticesType)(spine_render_command)

ctypedef uint16_t* (*spine_render_command_get_indicesType)(spine_render_command)

ctypedef int32_t (*spine_render_command_get_num_indicesType)(spine_render_command)

ctypedef int (*spine_render_command_get_blend_modeType)(spine_render_command)

ctypedef void* (*spine_render_command_get_textureType)(spine_render_command)

ctypedef spine_render_command (*spine_render_command_get_nextType)(spine_render_command)


# Active constraints with positive applied mix keep frames running.
# This tests participation, not settling; arrays and poses borrow skeleton lifetime.
ctypedef spine_array_physics_constraint (*spine_skeleton_get_physics_constraintsType)(spine_skeleton)

ctypedef size_t (*spine_array_physics_constraint_sizeType)(spine_array_physics_constraint)

ctypedef spine_physics_constraint* (*spine_array_physics_constraint_bufferType)(spine_array_physics_constraint)

ctypedef uint8_t (*spine_physics_constraint_is_activeType)(spine_physics_constraint)

ctypedef spine_physics_constraint_pose (*spine_physics_constraint_get_applied_poseType)(spine_physics_constraint)

ctypedef float (*spine_physics_constraint_pose_get_mixType)(spine_physics_constraint_pose)


# Generated by sebulsik-spine/gen_api.py.
# Module-level spine-c entry points, resolved by load().
cdef spine_major_versionType spine_major_version
cdef spine_minor_versionType spine_minor_version
cdef spine_atlas_loadType spine_atlas_load
cdef spine_atlas_result_get_errorType spine_atlas_result_get_error
cdef spine_atlas_result_get_atlasType spine_atlas_result_get_atlas
cdef spine_atlas_result_disposeType spine_atlas_result_dispose
cdef spine_atlas_disposeType spine_atlas_dispose
cdef spine_atlas_get_pagesType spine_atlas_get_pages
cdef spine_array_atlas_page_sizeType spine_array_atlas_page_size
cdef spine_array_atlas_page_bufferType spine_array_atlas_page_buffer
cdef spine_atlas_page_get_nameType spine_atlas_page_get_name
cdef spine_atlas_page_get_indexType spine_atlas_page_get_index
cdef spine_atlas_page_get_min_filterType spine_atlas_page_get_min_filter
cdef spine_atlas_page_get_mag_filterType spine_atlas_page_get_mag_filter
cdef spine_atlas_page_get_u_wrapType spine_atlas_page_get_u_wrap
cdef spine_atlas_page_get_v_wrapType spine_atlas_page_get_v_wrap
cdef spine_atlas_page_get_pmaType spine_atlas_page_get_pma
cdef spine_skeleton_data_load_jsonType spine_skeleton_data_load_json
cdef spine_skeleton_data_load_binaryType spine_skeleton_data_load_binary
cdef spine_skeleton_data_result_get_errorType spine_skeleton_data_result_get_error
cdef spine_skeleton_data_result_get_dataType spine_skeleton_data_result_get_data
cdef spine_skeleton_data_result_disposeType spine_skeleton_data_result_dispose
cdef spine_skeleton_data_disposeType spine_skeleton_data_dispose
cdef spine_skeleton_data_find_animationType spine_skeleton_data_find_animation
cdef spine_skeleton_data_get_animationsType spine_skeleton_data_get_animations
cdef spine_skeleton_data_find_skinType spine_skeleton_data_find_skin
cdef spine_skeleton_data_get_skinsType spine_skeleton_data_get_skins
cdef spine_skeleton_data_get_xType spine_skeleton_data_get_x
cdef spine_skeleton_data_get_yType spine_skeleton_data_get_y
cdef spine_skeleton_data_get_widthType spine_skeleton_data_get_width
cdef spine_skeleton_data_get_heightType spine_skeleton_data_get_height
cdef spine_array_animation_sizeType spine_array_animation_size
cdef spine_array_animation_bufferType spine_array_animation_buffer
cdef spine_array_skin_sizeType spine_array_skin_size
cdef spine_array_skin_bufferType spine_array_skin_buffer
cdef spine_animation_get_nameType spine_animation_get_name
cdef spine_animation_get_durationType spine_animation_get_duration
cdef spine_skin_get_nameType spine_skin_get_name
cdef spine_skin_createType spine_skin_create
cdef spine_skin_add_skinType spine_skin_add_skin
cdef spine_skin_disposeType spine_skin_dispose
cdef spine_skeleton_drawable_createType spine_skeleton_drawable_create
cdef spine_skeleton_drawable_updateType spine_skeleton_drawable_update
cdef spine_skeleton_drawable_renderType spine_skeleton_drawable_render
cdef spine_skeleton_drawable_disposeType spine_skeleton_drawable_dispose
cdef spine_skeleton_drawable_get_skeletonType spine_skeleton_drawable_get_skeleton
cdef spine_skeleton_drawable_get_animation_stateType spine_skeleton_drawable_get_animation_state
cdef spine_skeleton_set_scaleType spine_skeleton_set_scale
cdef spine_skeleton_setup_poseType spine_skeleton_setup_pose
cdef spine_skeleton_setup_pose_slotsType spine_skeleton_setup_pose_slots
cdef spine_skeleton_set_skin_1Type spine_skeleton_set_skin_1
cdef spine_skeleton_set_skin_2Type spine_skeleton_set_skin_2
cdef spine_skeleton_update_world_transformType spine_skeleton_update_world_transform
cdef spine_skeleton_get_skinType spine_skeleton_get_skin
cdef spine_skeleton_get_bounds_1Type spine_skeleton_get_bounds_1
cdef spine_animation_state_set_animation_1Type spine_animation_state_set_animation_1
cdef spine_animation_state_clear_tracksType spine_animation_state_clear_tracks
cdef spine_animation_state_get_dataType spine_animation_state_get_data
cdef spine_animation_state_data_set_default_mixType spine_animation_state_data_set_default_mix
cdef spine_animation_state_data_set_mix_2Type spine_animation_state_data_set_mix_2
cdef spine_track_entry_set_mix_duration_1Type spine_track_entry_set_mix_duration_1
cdef spine_animation_state_add_animation_1Type spine_animation_state_add_animation_1
cdef spine_animation_state_set_empty_animationType spine_animation_state_set_empty_animation
cdef spine_animation_state_clear_trackType spine_animation_state_clear_track
cdef spine_track_entry_get_alphaType spine_track_entry_get_alpha
cdef spine_track_entry_set_alphaType spine_track_entry_set_alpha
cdef spine_track_entry_get_additiveType spine_track_entry_get_additive
cdef spine_track_entry_set_additiveType spine_track_entry_set_additive
cdef spine_animation_state_get_tracksType spine_animation_state_get_tracks
cdef spine_array_track_entry_sizeType spine_array_track_entry_size
cdef spine_array_track_entry_bufferType spine_array_track_entry_buffer
cdef spine_track_entry_is_completeType spine_track_entry_is_complete
cdef spine_track_entry_get_loopType spine_track_entry_get_loop
cdef spine_track_entry_set_loopType spine_track_entry_set_loop
cdef spine_track_entry_get_mixing_fromType spine_track_entry_get_mixing_from
cdef spine_track_entry_get_nextType spine_track_entry_get_next
cdef spine_render_command_get_positionsType spine_render_command_get_positions
cdef spine_render_command_get_uvsType spine_render_command_get_uvs
cdef spine_render_command_get_colorsType spine_render_command_get_colors
cdef spine_render_command_get_dark_colorsType spine_render_command_get_dark_colors
cdef spine_render_command_get_num_verticesType spine_render_command_get_num_vertices
cdef spine_render_command_get_indicesType spine_render_command_get_indices
cdef spine_render_command_get_num_indicesType spine_render_command_get_num_indices
cdef spine_render_command_get_blend_modeType spine_render_command_get_blend_mode
cdef spine_render_command_get_textureType spine_render_command_get_texture
cdef spine_render_command_get_nextType spine_render_command_get_next
cdef spine_skeleton_get_physics_constraintsType spine_skeleton_get_physics_constraints
cdef spine_array_physics_constraint_sizeType spine_array_physics_constraint_size
cdef spine_array_physics_constraint_bufferType spine_array_physics_constraint_buffer
cdef spine_physics_constraint_is_activeType spine_physics_constraint_is_active
cdef spine_physics_constraint_get_applied_poseType spine_physics_constraint_get_applied_pose
cdef spine_physics_constraint_pose_get_mixType spine_physics_constraint_pose_get_mix


cdef extern from "SDL3/SDL.h":
    void* SDL_LoadObject(const char* sofile)
    void* SDL_LoadFunction(void* handle, const char* name)


cdef void* load_required(void* handle, object dll_name, const char* name) except NULL:
    """
    Loads `name` from the spine-c library, raising if it's missing. A missing
    symbol means the library does not provide the spine-c 4.3 contract this
    integration is written against; the error names the symbol and library.
    """
    cdef void* rv = load_spine_function(handle, name)
    if rv == NULL:
        raise Exception("{} not found in Spine-C library {}".format(
            name.decode("utf-8"), dll_name))
    return rv


# True once load() has resolved every entry point. The spine_* function
# pointers above are NULL until then, so SpineData refuses to exist earlier.
cdef bint spine_library_loaded = False


def load(dll):
    """Load the Spine library and return its version, or None if it cannot open.
    Raise an error if a required library function is missing."""
    global spine_library_loaded

    cdef void* handle = NULL
    cdef int major, minor

    if not dll:
        return None

    handle = load_spine_object(dll)
    if handle == NULL:
        return None

    dll_name = dll.decode("utf-8")

    # ---- begin resolve ----
    global spine_major_version
    spine_major_version = <spine_major_versionType> load_required(handle, dll_name, "spine_major_version")
    global spine_minor_version
    spine_minor_version = <spine_minor_versionType> load_required(handle, dll_name, "spine_minor_version")
    global spine_atlas_load
    spine_atlas_load = <spine_atlas_loadType> load_required(handle, dll_name, "spine_atlas_load")
    global spine_atlas_result_get_error
    spine_atlas_result_get_error = <spine_atlas_result_get_errorType> load_required(handle, dll_name, "spine_atlas_result_get_error")
    global spine_atlas_result_get_atlas
    spine_atlas_result_get_atlas = <spine_atlas_result_get_atlasType> load_required(handle, dll_name, "spine_atlas_result_get_atlas")
    global spine_atlas_result_dispose
    spine_atlas_result_dispose = <spine_atlas_result_disposeType> load_required(handle, dll_name, "spine_atlas_result_dispose")
    global spine_atlas_dispose
    spine_atlas_dispose = <spine_atlas_disposeType> load_required(handle, dll_name, "spine_atlas_dispose")
    global spine_atlas_get_pages
    spine_atlas_get_pages = <spine_atlas_get_pagesType> load_required(handle, dll_name, "spine_atlas_get_pages")
    global spine_array_atlas_page_size
    spine_array_atlas_page_size = <spine_array_atlas_page_sizeType> load_required(handle, dll_name, "spine_array_atlas_page_size")
    global spine_array_atlas_page_buffer
    spine_array_atlas_page_buffer = <spine_array_atlas_page_bufferType> load_required(handle, dll_name, "spine_array_atlas_page_buffer")
    global spine_atlas_page_get_name
    spine_atlas_page_get_name = <spine_atlas_page_get_nameType> load_required(handle, dll_name, "spine_atlas_page_get_name")
    global spine_atlas_page_get_index
    spine_atlas_page_get_index = <spine_atlas_page_get_indexType> load_required(handle, dll_name, "spine_atlas_page_get_index")
    global spine_atlas_page_get_min_filter
    spine_atlas_page_get_min_filter = <spine_atlas_page_get_min_filterType> load_required(handle, dll_name, "spine_atlas_page_get_min_filter")
    global spine_atlas_page_get_mag_filter
    spine_atlas_page_get_mag_filter = <spine_atlas_page_get_mag_filterType> load_required(handle, dll_name, "spine_atlas_page_get_mag_filter")
    global spine_atlas_page_get_u_wrap
    spine_atlas_page_get_u_wrap = <spine_atlas_page_get_u_wrapType> load_required(handle, dll_name, "spine_atlas_page_get_u_wrap")
    global spine_atlas_page_get_v_wrap
    spine_atlas_page_get_v_wrap = <spine_atlas_page_get_v_wrapType> load_required(handle, dll_name, "spine_atlas_page_get_v_wrap")
    global spine_atlas_page_get_pma
    spine_atlas_page_get_pma = <spine_atlas_page_get_pmaType> load_required(handle, dll_name, "spine_atlas_page_get_pma")
    global spine_skeleton_data_load_json
    spine_skeleton_data_load_json = <spine_skeleton_data_load_jsonType> load_required(handle, dll_name, "spine_skeleton_data_load_json")
    global spine_skeleton_data_load_binary
    spine_skeleton_data_load_binary = <spine_skeleton_data_load_binaryType> load_required(handle, dll_name, "spine_skeleton_data_load_binary")
    global spine_skeleton_data_result_get_error
    spine_skeleton_data_result_get_error = <spine_skeleton_data_result_get_errorType> load_required(handle, dll_name, "spine_skeleton_data_result_get_error")
    global spine_skeleton_data_result_get_data
    spine_skeleton_data_result_get_data = <spine_skeleton_data_result_get_dataType> load_required(handle, dll_name, "spine_skeleton_data_result_get_data")
    global spine_skeleton_data_result_dispose
    spine_skeleton_data_result_dispose = <spine_skeleton_data_result_disposeType> load_required(handle, dll_name, "spine_skeleton_data_result_dispose")
    global spine_skeleton_data_dispose
    spine_skeleton_data_dispose = <spine_skeleton_data_disposeType> load_required(handle, dll_name, "spine_skeleton_data_dispose")
    global spine_skeleton_data_find_animation
    spine_skeleton_data_find_animation = <spine_skeleton_data_find_animationType> load_required(handle, dll_name, "spine_skeleton_data_find_animation")
    global spine_skeleton_data_get_animations
    spine_skeleton_data_get_animations = <spine_skeleton_data_get_animationsType> load_required(handle, dll_name, "spine_skeleton_data_get_animations")
    global spine_skeleton_data_find_skin
    spine_skeleton_data_find_skin = <spine_skeleton_data_find_skinType> load_required(handle, dll_name, "spine_skeleton_data_find_skin")
    global spine_skeleton_data_get_skins
    spine_skeleton_data_get_skins = <spine_skeleton_data_get_skinsType> load_required(handle, dll_name, "spine_skeleton_data_get_skins")
    global spine_skeleton_data_get_x
    spine_skeleton_data_get_x = <spine_skeleton_data_get_xType> load_required(handle, dll_name, "spine_skeleton_data_get_x")
    global spine_skeleton_data_get_y
    spine_skeleton_data_get_y = <spine_skeleton_data_get_yType> load_required(handle, dll_name, "spine_skeleton_data_get_y")
    global spine_skeleton_data_get_width
    spine_skeleton_data_get_width = <spine_skeleton_data_get_widthType> load_required(handle, dll_name, "spine_skeleton_data_get_width")
    global spine_skeleton_data_get_height
    spine_skeleton_data_get_height = <spine_skeleton_data_get_heightType> load_required(handle, dll_name, "spine_skeleton_data_get_height")
    global spine_array_animation_size
    spine_array_animation_size = <spine_array_animation_sizeType> load_required(handle, dll_name, "spine_array_animation_size")
    global spine_array_animation_buffer
    spine_array_animation_buffer = <spine_array_animation_bufferType> load_required(handle, dll_name, "spine_array_animation_buffer")
    global spine_array_skin_size
    spine_array_skin_size = <spine_array_skin_sizeType> load_required(handle, dll_name, "spine_array_skin_size")
    global spine_array_skin_buffer
    spine_array_skin_buffer = <spine_array_skin_bufferType> load_required(handle, dll_name, "spine_array_skin_buffer")
    global spine_animation_get_name
    spine_animation_get_name = <spine_animation_get_nameType> load_required(handle, dll_name, "spine_animation_get_name")
    global spine_animation_get_duration
    spine_animation_get_duration = <spine_animation_get_durationType> load_required(handle, dll_name, "spine_animation_get_duration")
    global spine_skin_get_name
    spine_skin_get_name = <spine_skin_get_nameType> load_required(handle, dll_name, "spine_skin_get_name")
    global spine_skin_create
    spine_skin_create = <spine_skin_createType> load_required(handle, dll_name, "spine_skin_create")
    global spine_skin_add_skin
    spine_skin_add_skin = <spine_skin_add_skinType> load_required(handle, dll_name, "spine_skin_add_skin")
    global spine_skin_dispose
    spine_skin_dispose = <spine_skin_disposeType> load_required(handle, dll_name, "spine_skin_dispose")
    global spine_skeleton_drawable_create
    spine_skeleton_drawable_create = <spine_skeleton_drawable_createType> load_required(handle, dll_name, "spine_skeleton_drawable_create")
    global spine_skeleton_drawable_update
    spine_skeleton_drawable_update = <spine_skeleton_drawable_updateType> load_required(handle, dll_name, "spine_skeleton_drawable_update")
    global spine_skeleton_drawable_render
    spine_skeleton_drawable_render = <spine_skeleton_drawable_renderType> load_required(handle, dll_name, "spine_skeleton_drawable_render")
    global spine_skeleton_drawable_dispose
    spine_skeleton_drawable_dispose = <spine_skeleton_drawable_disposeType> load_required(handle, dll_name, "spine_skeleton_drawable_dispose")
    global spine_skeleton_drawable_get_skeleton
    spine_skeleton_drawable_get_skeleton = <spine_skeleton_drawable_get_skeletonType> load_required(handle, dll_name, "spine_skeleton_drawable_get_skeleton")
    global spine_skeleton_drawable_get_animation_state
    spine_skeleton_drawable_get_animation_state = <spine_skeleton_drawable_get_animation_stateType> load_required(handle, dll_name, "spine_skeleton_drawable_get_animation_state")
    global spine_skeleton_set_scale
    spine_skeleton_set_scale = <spine_skeleton_set_scaleType> load_required(handle, dll_name, "spine_skeleton_set_scale")
    global spine_skeleton_setup_pose
    spine_skeleton_setup_pose = <spine_skeleton_setup_poseType> load_required(handle, dll_name, "spine_skeleton_setup_pose")
    global spine_skeleton_setup_pose_slots
    spine_skeleton_setup_pose_slots = <spine_skeleton_setup_pose_slotsType> load_required(handle, dll_name, "spine_skeleton_setup_pose_slots")
    global spine_skeleton_set_skin_1
    spine_skeleton_set_skin_1 = <spine_skeleton_set_skin_1Type> load_required(handle, dll_name, "spine_skeleton_set_skin_1")
    global spine_skeleton_set_skin_2
    spine_skeleton_set_skin_2 = <spine_skeleton_set_skin_2Type> load_required(handle, dll_name, "spine_skeleton_set_skin_2")
    global spine_skeleton_update_world_transform
    spine_skeleton_update_world_transform = <spine_skeleton_update_world_transformType> load_required(handle, dll_name, "spine_skeleton_update_world_transform")
    global spine_skeleton_get_skin
    spine_skeleton_get_skin = <spine_skeleton_get_skinType> load_required(handle, dll_name, "spine_skeleton_get_skin")
    global spine_skeleton_get_bounds_1
    spine_skeleton_get_bounds_1 = <spine_skeleton_get_bounds_1Type> load_required(handle, dll_name, "spine_skeleton_get_bounds_1")
    global spine_animation_state_set_animation_1
    spine_animation_state_set_animation_1 = <spine_animation_state_set_animation_1Type> load_required(handle, dll_name, "spine_animation_state_set_animation_1")
    global spine_animation_state_clear_tracks
    spine_animation_state_clear_tracks = <spine_animation_state_clear_tracksType> load_required(handle, dll_name, "spine_animation_state_clear_tracks")
    global spine_animation_state_get_data
    spine_animation_state_get_data = <spine_animation_state_get_dataType> load_required(handle, dll_name, "spine_animation_state_get_data")
    global spine_animation_state_data_set_default_mix
    spine_animation_state_data_set_default_mix = <spine_animation_state_data_set_default_mixType> load_required(handle, dll_name, "spine_animation_state_data_set_default_mix")
    global spine_animation_state_data_set_mix_2
    spine_animation_state_data_set_mix_2 = <spine_animation_state_data_set_mix_2Type> load_required(handle, dll_name, "spine_animation_state_data_set_mix_2")
    global spine_track_entry_set_mix_duration_1
    spine_track_entry_set_mix_duration_1 = <spine_track_entry_set_mix_duration_1Type> load_required(handle, dll_name, "spine_track_entry_set_mix_duration_1")
    global spine_animation_state_add_animation_1
    spine_animation_state_add_animation_1 = <spine_animation_state_add_animation_1Type> load_required(handle, dll_name, "spine_animation_state_add_animation_1")
    global spine_animation_state_set_empty_animation
    spine_animation_state_set_empty_animation = <spine_animation_state_set_empty_animationType> load_required(handle, dll_name, "spine_animation_state_set_empty_animation")
    global spine_animation_state_clear_track
    spine_animation_state_clear_track = <spine_animation_state_clear_trackType> load_required(handle, dll_name, "spine_animation_state_clear_track")
    global spine_track_entry_get_alpha
    spine_track_entry_get_alpha = <spine_track_entry_get_alphaType> load_required(handle, dll_name, "spine_track_entry_get_alpha")
    global spine_track_entry_set_alpha
    spine_track_entry_set_alpha = <spine_track_entry_set_alphaType> load_required(handle, dll_name, "spine_track_entry_set_alpha")
    global spine_track_entry_get_additive
    spine_track_entry_get_additive = <spine_track_entry_get_additiveType> load_required(handle, dll_name, "spine_track_entry_get_additive")
    global spine_track_entry_set_additive
    spine_track_entry_set_additive = <spine_track_entry_set_additiveType> load_required(handle, dll_name, "spine_track_entry_set_additive")
    global spine_animation_state_get_tracks
    spine_animation_state_get_tracks = <spine_animation_state_get_tracksType> load_required(handle, dll_name, "spine_animation_state_get_tracks")
    global spine_array_track_entry_size
    spine_array_track_entry_size = <spine_array_track_entry_sizeType> load_required(handle, dll_name, "spine_array_track_entry_size")
    global spine_array_track_entry_buffer
    spine_array_track_entry_buffer = <spine_array_track_entry_bufferType> load_required(handle, dll_name, "spine_array_track_entry_buffer")
    global spine_track_entry_is_complete
    spine_track_entry_is_complete = <spine_track_entry_is_completeType> load_required(handle, dll_name, "spine_track_entry_is_complete")
    global spine_track_entry_get_loop
    spine_track_entry_get_loop = <spine_track_entry_get_loopType> load_required(handle, dll_name, "spine_track_entry_get_loop")
    global spine_track_entry_set_loop
    spine_track_entry_set_loop = <spine_track_entry_set_loopType> load_required(handle, dll_name, "spine_track_entry_set_loop")
    global spine_track_entry_get_mixing_from
    spine_track_entry_get_mixing_from = <spine_track_entry_get_mixing_fromType> load_required(handle, dll_name, "spine_track_entry_get_mixing_from")
    global spine_track_entry_get_next
    spine_track_entry_get_next = <spine_track_entry_get_nextType> load_required(handle, dll_name, "spine_track_entry_get_next")
    global spine_render_command_get_positions
    spine_render_command_get_positions = <spine_render_command_get_positionsType> load_required(handle, dll_name, "spine_render_command_get_positions")
    global spine_render_command_get_uvs
    spine_render_command_get_uvs = <spine_render_command_get_uvsType> load_required(handle, dll_name, "spine_render_command_get_uvs")
    global spine_render_command_get_colors
    spine_render_command_get_colors = <spine_render_command_get_colorsType> load_required(handle, dll_name, "spine_render_command_get_colors")
    global spine_render_command_get_dark_colors
    spine_render_command_get_dark_colors = <spine_render_command_get_dark_colorsType> load_required(handle, dll_name, "spine_render_command_get_dark_colors")
    global spine_render_command_get_num_vertices
    spine_render_command_get_num_vertices = <spine_render_command_get_num_verticesType> load_required(handle, dll_name, "spine_render_command_get_num_vertices")
    global spine_render_command_get_indices
    spine_render_command_get_indices = <spine_render_command_get_indicesType> load_required(handle, dll_name, "spine_render_command_get_indices")
    global spine_render_command_get_num_indices
    spine_render_command_get_num_indices = <spine_render_command_get_num_indicesType> load_required(handle, dll_name, "spine_render_command_get_num_indices")
    global spine_render_command_get_blend_mode
    spine_render_command_get_blend_mode = <spine_render_command_get_blend_modeType> load_required(handle, dll_name, "spine_render_command_get_blend_mode")
    global spine_render_command_get_texture
    spine_render_command_get_texture = <spine_render_command_get_textureType> load_required(handle, dll_name, "spine_render_command_get_texture")
    global spine_render_command_get_next
    spine_render_command_get_next = <spine_render_command_get_nextType> load_required(handle, dll_name, "spine_render_command_get_next")
    global spine_skeleton_get_physics_constraints
    spine_skeleton_get_physics_constraints = <spine_skeleton_get_physics_constraintsType> load_required(handle, dll_name, "spine_skeleton_get_physics_constraints")
    global spine_array_physics_constraint_size
    spine_array_physics_constraint_size = <spine_array_physics_constraint_sizeType> load_required(handle, dll_name, "spine_array_physics_constraint_size")
    global spine_array_physics_constraint_buffer
    spine_array_physics_constraint_buffer = <spine_array_physics_constraint_bufferType> load_required(handle, dll_name, "spine_array_physics_constraint_buffer")
    global spine_physics_constraint_is_active
    spine_physics_constraint_is_active = <spine_physics_constraint_is_activeType> load_required(handle, dll_name, "spine_physics_constraint_is_active")
    global spine_physics_constraint_get_applied_pose
    spine_physics_constraint_get_applied_pose = <spine_physics_constraint_get_applied_poseType> load_required(handle, dll_name, "spine_physics_constraint_get_applied_pose")
    global spine_physics_constraint_pose_get_mix
    spine_physics_constraint_pose_get_mix = <spine_physics_constraint_pose_get_mixType> load_required(handle, dll_name, "spine_physics_constraint_pose_get_mix")
    # ---- end resolve ----

    major = spine_major_version()
    minor = spine_minor_version()
    spine_library_loaded = True
    spine_log("Spine: loaded {} (spine-c {}.{})".format(dll_name, major, minor), debug=False)

    if major != 4 or minor != 3:
        spine_log("Spine: Warning - expected spine-c 4.3, but loaded {}.{}".format(major, minor), debug=False)

    return (major, minor)
