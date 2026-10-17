# By Sebulsik <sebulsik.dev@gmail.com>

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

ctypedef spine_skin (*spine_skin_createType)(const char*)

ctypedef void (*spine_skin_add_skinType)(spine_skin, spine_skin)

ctypedef void (*spine_skin_disposeType)(spine_skin)


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

ctypedef spine_array_physics_constraint (*spine_skeleton_get_physics_constraintsType)(spine_skeleton)

ctypedef size_t (*spine_array_physics_constraint_sizeType)(spine_array_physics_constraint)

ctypedef spine_physics_constraint* (*spine_array_physics_constraint_bufferType)(spine_array_physics_constraint)

ctypedef uint8_t (*spine_physics_constraint_is_activeType)(spine_physics_constraint)

ctypedef spine_physics_constraint_pose (*spine_physics_constraint_get_applied_poseType)(spine_physics_constraint)

ctypedef float (*spine_physics_constraint_pose_get_mixType)(spine_physics_constraint_pose)


cdef struct SpineApi:
    spine_major_versionType spine_major_version
    spine_minor_versionType spine_minor_version
    spine_atlas_loadType spine_atlas_load
    spine_atlas_result_get_errorType spine_atlas_result_get_error
    spine_atlas_result_get_atlasType spine_atlas_result_get_atlas
    spine_atlas_result_disposeType spine_atlas_result_dispose
    spine_atlas_disposeType spine_atlas_dispose
    spine_atlas_get_pagesType spine_atlas_get_pages
    spine_array_atlas_page_sizeType spine_array_atlas_page_size
    spine_array_atlas_page_bufferType spine_array_atlas_page_buffer
    spine_atlas_page_get_nameType spine_atlas_page_get_name
    spine_atlas_page_get_indexType spine_atlas_page_get_index
    spine_atlas_page_get_min_filterType spine_atlas_page_get_min_filter
    spine_atlas_page_get_mag_filterType spine_atlas_page_get_mag_filter
    spine_atlas_page_get_u_wrapType spine_atlas_page_get_u_wrap
    spine_atlas_page_get_v_wrapType spine_atlas_page_get_v_wrap
    spine_atlas_page_get_pmaType spine_atlas_page_get_pma
    spine_skeleton_data_load_jsonType spine_skeleton_data_load_json
    spine_skeleton_data_load_binaryType spine_skeleton_data_load_binary
    spine_skeleton_data_result_get_errorType spine_skeleton_data_result_get_error
    spine_skeleton_data_result_get_dataType spine_skeleton_data_result_get_data
    spine_skeleton_data_result_disposeType spine_skeleton_data_result_dispose
    spine_skeleton_data_disposeType spine_skeleton_data_dispose
    spine_skeleton_data_find_animationType spine_skeleton_data_find_animation
    spine_skeleton_data_get_animationsType spine_skeleton_data_get_animations
    spine_skeleton_data_find_skinType spine_skeleton_data_find_skin
    spine_skeleton_data_get_skinsType spine_skeleton_data_get_skins
    spine_skeleton_data_get_xType spine_skeleton_data_get_x
    spine_skeleton_data_get_yType spine_skeleton_data_get_y
    spine_skeleton_data_get_widthType spine_skeleton_data_get_width
    spine_skeleton_data_get_heightType spine_skeleton_data_get_height
    spine_array_animation_sizeType spine_array_animation_size
    spine_array_animation_bufferType spine_array_animation_buffer
    spine_array_skin_sizeType spine_array_skin_size
    spine_array_skin_bufferType spine_array_skin_buffer
    spine_animation_get_nameType spine_animation_get_name
    spine_animation_get_durationType spine_animation_get_duration
    spine_skin_get_nameType spine_skin_get_name
    spine_skin_createType spine_skin_create
    spine_skin_add_skinType spine_skin_add_skin
    spine_skin_disposeType spine_skin_dispose
    spine_skeleton_drawable_createType spine_skeleton_drawable_create
    spine_skeleton_drawable_updateType spine_skeleton_drawable_update
    spine_skeleton_drawable_renderType spine_skeleton_drawable_render
    spine_skeleton_drawable_disposeType spine_skeleton_drawable_dispose
    spine_skeleton_drawable_get_skeletonType spine_skeleton_drawable_get_skeleton
    spine_skeleton_drawable_get_animation_stateType spine_skeleton_drawable_get_animation_state
    spine_skeleton_set_scaleType spine_skeleton_set_scale
    spine_skeleton_setup_poseType spine_skeleton_setup_pose
    spine_skeleton_setup_pose_slotsType spine_skeleton_setup_pose_slots
    spine_skeleton_set_skin_1Type spine_skeleton_set_skin_1
    spine_skeleton_set_skin_2Type spine_skeleton_set_skin_2
    spine_skeleton_update_world_transformType spine_skeleton_update_world_transform
    spine_skeleton_get_skinType spine_skeleton_get_skin
    spine_skeleton_get_bounds_1Type spine_skeleton_get_bounds_1
    spine_animation_state_set_animation_1Type spine_animation_state_set_animation_1
    spine_animation_state_clear_tracksType spine_animation_state_clear_tracks
    spine_animation_state_get_dataType spine_animation_state_get_data
    spine_animation_state_data_set_default_mixType spine_animation_state_data_set_default_mix
    spine_animation_state_data_set_mix_2Type spine_animation_state_data_set_mix_2
    spine_track_entry_set_mix_duration_1Type spine_track_entry_set_mix_duration_1
    spine_animation_state_add_animation_1Type spine_animation_state_add_animation_1
    spine_animation_state_set_empty_animationType spine_animation_state_set_empty_animation
    spine_animation_state_clear_trackType spine_animation_state_clear_track
    spine_track_entry_get_alphaType spine_track_entry_get_alpha
    spine_track_entry_set_alphaType spine_track_entry_set_alpha
    spine_track_entry_get_additiveType spine_track_entry_get_additive
    spine_track_entry_set_additiveType spine_track_entry_set_additive
    spine_animation_state_get_tracksType spine_animation_state_get_tracks
    spine_array_track_entry_sizeType spine_array_track_entry_size
    spine_array_track_entry_bufferType spine_array_track_entry_buffer
    spine_track_entry_is_completeType spine_track_entry_is_complete
    spine_track_entry_get_loopType spine_track_entry_get_loop
    spine_track_entry_set_loopType spine_track_entry_set_loop
    spine_track_entry_get_mixing_fromType spine_track_entry_get_mixing_from
    spine_track_entry_get_nextType spine_track_entry_get_next
    spine_render_command_get_positionsType spine_render_command_get_positions
    spine_render_command_get_uvsType spine_render_command_get_uvs
    spine_render_command_get_colorsType spine_render_command_get_colors
    spine_render_command_get_dark_colorsType spine_render_command_get_dark_colors
    spine_render_command_get_num_verticesType spine_render_command_get_num_vertices
    spine_render_command_get_indicesType spine_render_command_get_indices
    spine_render_command_get_num_indicesType spine_render_command_get_num_indices
    spine_render_command_get_blend_modeType spine_render_command_get_blend_mode
    spine_render_command_get_textureType spine_render_command_get_texture
    spine_render_command_get_nextType spine_render_command_get_next
    spine_skeleton_get_physics_constraintsType spine_skeleton_get_physics_constraints
    spine_array_physics_constraint_sizeType spine_array_physics_constraint_size
    spine_array_physics_constraint_bufferType spine_array_physics_constraint_buffer
    spine_physics_constraint_is_activeType spine_physics_constraint_is_active
    spine_physics_constraint_get_applied_poseType spine_physics_constraint_get_applied_pose
    spine_physics_constraint_pose_get_mixType spine_physics_constraint_pose_get_mix


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


cdef class SpineLibrary:
    """
    A loaded spine-c library: the resolved API table plus its identity and
    version. Created by load() and held by the Python runtime object; passed to
    SpineData, and through it to every SpineModel, so native calls go through
    an object rather than module state.
    """

    cdef SpineApi api
    cdef void* handle
    cdef readonly object name
    cdef readonly int major
    cdef readonly int minor

    def __cinit__(self):
        self.handle = NULL
        self.name = None
        self.major = 0
        self.minor = 0

    def version(self):
        """(major, minor) of the loaded runtime."""
        return (self.major, self.minor)


def load(dll):
    cdef void* handle = NULL
    cdef SpineLibrary lib

    if not dll:
        return None

    handle = load_spine_object(dll)
    if handle == NULL:
        return None

    lib = SpineLibrary()
    lib.handle = handle
    lib.name = dll.decode("utf-8")

    # ---- begin resolve ----
    lib.api.spine_major_version = <spine_major_versionType> load_required(handle, lib.name, "spine_major_version")
    lib.api.spine_minor_version = <spine_minor_versionType> load_required(handle, lib.name, "spine_minor_version")
    lib.api.spine_atlas_load = <spine_atlas_loadType> load_required(handle, lib.name, "spine_atlas_load")
    lib.api.spine_atlas_result_get_error = <spine_atlas_result_get_errorType> load_required(handle, lib.name, "spine_atlas_result_get_error")
    lib.api.spine_atlas_result_get_atlas = <spine_atlas_result_get_atlasType> load_required(handle, lib.name, "spine_atlas_result_get_atlas")
    lib.api.spine_atlas_result_dispose = <spine_atlas_result_disposeType> load_required(handle, lib.name, "spine_atlas_result_dispose")
    lib.api.spine_atlas_dispose = <spine_atlas_disposeType> load_required(handle, lib.name, "spine_atlas_dispose")
    lib.api.spine_atlas_get_pages = <spine_atlas_get_pagesType> load_required(handle, lib.name, "spine_atlas_get_pages")
    lib.api.spine_array_atlas_page_size = <spine_array_atlas_page_sizeType> load_required(handle, lib.name, "spine_array_atlas_page_size")
    lib.api.spine_array_atlas_page_buffer = <spine_array_atlas_page_bufferType> load_required(handle, lib.name, "spine_array_atlas_page_buffer")
    lib.api.spine_atlas_page_get_name = <spine_atlas_page_get_nameType> load_required(handle, lib.name, "spine_atlas_page_get_name")
    lib.api.spine_atlas_page_get_index = <spine_atlas_page_get_indexType> load_required(handle, lib.name, "spine_atlas_page_get_index")
    lib.api.spine_atlas_page_get_min_filter = <spine_atlas_page_get_min_filterType> load_required(handle, lib.name, "spine_atlas_page_get_min_filter")
    lib.api.spine_atlas_page_get_mag_filter = <spine_atlas_page_get_mag_filterType> load_required(handle, lib.name, "spine_atlas_page_get_mag_filter")
    lib.api.spine_atlas_page_get_u_wrap = <spine_atlas_page_get_u_wrapType> load_required(handle, lib.name, "spine_atlas_page_get_u_wrap")
    lib.api.spine_atlas_page_get_v_wrap = <spine_atlas_page_get_v_wrapType> load_required(handle, lib.name, "spine_atlas_page_get_v_wrap")
    lib.api.spine_atlas_page_get_pma = <spine_atlas_page_get_pmaType> load_required(handle, lib.name, "spine_atlas_page_get_pma")
    lib.api.spine_skeleton_data_load_json = <spine_skeleton_data_load_jsonType> load_required(handle, lib.name, "spine_skeleton_data_load_json")
    lib.api.spine_skeleton_data_load_binary = <spine_skeleton_data_load_binaryType> load_required(handle, lib.name, "spine_skeleton_data_load_binary")
    lib.api.spine_skeleton_data_result_get_error = <spine_skeleton_data_result_get_errorType> load_required(handle, lib.name, "spine_skeleton_data_result_get_error")
    lib.api.spine_skeleton_data_result_get_data = <spine_skeleton_data_result_get_dataType> load_required(handle, lib.name, "spine_skeleton_data_result_get_data")
    lib.api.spine_skeleton_data_result_dispose = <spine_skeleton_data_result_disposeType> load_required(handle, lib.name, "spine_skeleton_data_result_dispose")
    lib.api.spine_skeleton_data_dispose = <spine_skeleton_data_disposeType> load_required(handle, lib.name, "spine_skeleton_data_dispose")
    lib.api.spine_skeleton_data_find_animation = <spine_skeleton_data_find_animationType> load_required(handle, lib.name, "spine_skeleton_data_find_animation")
    lib.api.spine_skeleton_data_get_animations = <spine_skeleton_data_get_animationsType> load_required(handle, lib.name, "spine_skeleton_data_get_animations")
    lib.api.spine_skeleton_data_find_skin = <spine_skeleton_data_find_skinType> load_required(handle, lib.name, "spine_skeleton_data_find_skin")
    lib.api.spine_skeleton_data_get_skins = <spine_skeleton_data_get_skinsType> load_required(handle, lib.name, "spine_skeleton_data_get_skins")
    lib.api.spine_skeleton_data_get_x = <spine_skeleton_data_get_xType> load_required(handle, lib.name, "spine_skeleton_data_get_x")
    lib.api.spine_skeleton_data_get_y = <spine_skeleton_data_get_yType> load_required(handle, lib.name, "spine_skeleton_data_get_y")
    lib.api.spine_skeleton_data_get_width = <spine_skeleton_data_get_widthType> load_required(handle, lib.name, "spine_skeleton_data_get_width")
    lib.api.spine_skeleton_data_get_height = <spine_skeleton_data_get_heightType> load_required(handle, lib.name, "spine_skeleton_data_get_height")
    lib.api.spine_array_animation_size = <spine_array_animation_sizeType> load_required(handle, lib.name, "spine_array_animation_size")
    lib.api.spine_array_animation_buffer = <spine_array_animation_bufferType> load_required(handle, lib.name, "spine_array_animation_buffer")
    lib.api.spine_array_skin_size = <spine_array_skin_sizeType> load_required(handle, lib.name, "spine_array_skin_size")
    lib.api.spine_array_skin_buffer = <spine_array_skin_bufferType> load_required(handle, lib.name, "spine_array_skin_buffer")
    lib.api.spine_animation_get_name = <spine_animation_get_nameType> load_required(handle, lib.name, "spine_animation_get_name")
    lib.api.spine_animation_get_duration = <spine_animation_get_durationType> load_required(handle, lib.name, "spine_animation_get_duration")
    lib.api.spine_skin_get_name = <spine_skin_get_nameType> load_required(handle, lib.name, "spine_skin_get_name")
    lib.api.spine_skin_create = <spine_skin_createType> load_required(handle, lib.name, "spine_skin_create")
    lib.api.spine_skin_add_skin = <spine_skin_add_skinType> load_required(handle, lib.name, "spine_skin_add_skin")
    lib.api.spine_skin_dispose = <spine_skin_disposeType> load_required(handle, lib.name, "spine_skin_dispose")
    lib.api.spine_skeleton_drawable_create = <spine_skeleton_drawable_createType> load_required(handle, lib.name, "spine_skeleton_drawable_create")
    lib.api.spine_skeleton_drawable_update = <spine_skeleton_drawable_updateType> load_required(handle, lib.name, "spine_skeleton_drawable_update")
    lib.api.spine_skeleton_drawable_render = <spine_skeleton_drawable_renderType> load_required(handle, lib.name, "spine_skeleton_drawable_render")
    lib.api.spine_skeleton_drawable_dispose = <spine_skeleton_drawable_disposeType> load_required(handle, lib.name, "spine_skeleton_drawable_dispose")
    lib.api.spine_skeleton_drawable_get_skeleton = <spine_skeleton_drawable_get_skeletonType> load_required(handle, lib.name, "spine_skeleton_drawable_get_skeleton")
    lib.api.spine_skeleton_drawable_get_animation_state = <spine_skeleton_drawable_get_animation_stateType> load_required(handle, lib.name, "spine_skeleton_drawable_get_animation_state")
    lib.api.spine_skeleton_set_scale = <spine_skeleton_set_scaleType> load_required(handle, lib.name, "spine_skeleton_set_scale")
    lib.api.spine_skeleton_setup_pose = <spine_skeleton_setup_poseType> load_required(handle, lib.name, "spine_skeleton_setup_pose")
    lib.api.spine_skeleton_setup_pose_slots = <spine_skeleton_setup_pose_slotsType> load_required(handle, lib.name, "spine_skeleton_setup_pose_slots")
    lib.api.spine_skeleton_set_skin_1 = <spine_skeleton_set_skin_1Type> load_required(handle, lib.name, "spine_skeleton_set_skin_1")
    lib.api.spine_skeleton_set_skin_2 = <spine_skeleton_set_skin_2Type> load_required(handle, lib.name, "spine_skeleton_set_skin_2")
    lib.api.spine_skeleton_update_world_transform = <spine_skeleton_update_world_transformType> load_required(handle, lib.name, "spine_skeleton_update_world_transform")
    lib.api.spine_skeleton_get_skin = <spine_skeleton_get_skinType> load_required(handle, lib.name, "spine_skeleton_get_skin")
    lib.api.spine_skeleton_get_bounds_1 = <spine_skeleton_get_bounds_1Type> load_required(handle, lib.name, "spine_skeleton_get_bounds_1")
    lib.api.spine_animation_state_set_animation_1 = <spine_animation_state_set_animation_1Type> load_required(handle, lib.name, "spine_animation_state_set_animation_1")
    lib.api.spine_animation_state_clear_tracks = <spine_animation_state_clear_tracksType> load_required(handle, lib.name, "spine_animation_state_clear_tracks")
    lib.api.spine_animation_state_get_data = <spine_animation_state_get_dataType> load_required(handle, lib.name, "spine_animation_state_get_data")
    lib.api.spine_animation_state_data_set_default_mix = <spine_animation_state_data_set_default_mixType> load_required(handle, lib.name, "spine_animation_state_data_set_default_mix")
    lib.api.spine_animation_state_data_set_mix_2 = <spine_animation_state_data_set_mix_2Type> load_required(handle, lib.name, "spine_animation_state_data_set_mix_2")
    lib.api.spine_track_entry_set_mix_duration_1 = <spine_track_entry_set_mix_duration_1Type> load_required(handle, lib.name, "spine_track_entry_set_mix_duration_1")
    lib.api.spine_animation_state_add_animation_1 = <spine_animation_state_add_animation_1Type> load_required(handle, lib.name, "spine_animation_state_add_animation_1")
    lib.api.spine_animation_state_set_empty_animation = <spine_animation_state_set_empty_animationType> load_required(handle, lib.name, "spine_animation_state_set_empty_animation")
    lib.api.spine_animation_state_clear_track = <spine_animation_state_clear_trackType> load_required(handle, lib.name, "spine_animation_state_clear_track")
    lib.api.spine_track_entry_get_alpha = <spine_track_entry_get_alphaType> load_required(handle, lib.name, "spine_track_entry_get_alpha")
    lib.api.spine_track_entry_set_alpha = <spine_track_entry_set_alphaType> load_required(handle, lib.name, "spine_track_entry_set_alpha")
    lib.api.spine_track_entry_get_additive = <spine_track_entry_get_additiveType> load_required(handle, lib.name, "spine_track_entry_get_additive")
    lib.api.spine_track_entry_set_additive = <spine_track_entry_set_additiveType> load_required(handle, lib.name, "spine_track_entry_set_additive")
    lib.api.spine_animation_state_get_tracks = <spine_animation_state_get_tracksType> load_required(handle, lib.name, "spine_animation_state_get_tracks")
    lib.api.spine_array_track_entry_size = <spine_array_track_entry_sizeType> load_required(handle, lib.name, "spine_array_track_entry_size")
    lib.api.spine_array_track_entry_buffer = <spine_array_track_entry_bufferType> load_required(handle, lib.name, "spine_array_track_entry_buffer")
    lib.api.spine_track_entry_is_complete = <spine_track_entry_is_completeType> load_required(handle, lib.name, "spine_track_entry_is_complete")
    lib.api.spine_track_entry_get_loop = <spine_track_entry_get_loopType> load_required(handle, lib.name, "spine_track_entry_get_loop")
    lib.api.spine_track_entry_set_loop = <spine_track_entry_set_loopType> load_required(handle, lib.name, "spine_track_entry_set_loop")
    lib.api.spine_track_entry_get_mixing_from = <spine_track_entry_get_mixing_fromType> load_required(handle, lib.name, "spine_track_entry_get_mixing_from")
    lib.api.spine_track_entry_get_next = <spine_track_entry_get_nextType> load_required(handle, lib.name, "spine_track_entry_get_next")
    lib.api.spine_render_command_get_positions = <spine_render_command_get_positionsType> load_required(handle, lib.name, "spine_render_command_get_positions")
    lib.api.spine_render_command_get_uvs = <spine_render_command_get_uvsType> load_required(handle, lib.name, "spine_render_command_get_uvs")
    lib.api.spine_render_command_get_colors = <spine_render_command_get_colorsType> load_required(handle, lib.name, "spine_render_command_get_colors")
    lib.api.spine_render_command_get_dark_colors = <spine_render_command_get_dark_colorsType> load_required(handle, lib.name, "spine_render_command_get_dark_colors")
    lib.api.spine_render_command_get_num_vertices = <spine_render_command_get_num_verticesType> load_required(handle, lib.name, "spine_render_command_get_num_vertices")
    lib.api.spine_render_command_get_indices = <spine_render_command_get_indicesType> load_required(handle, lib.name, "spine_render_command_get_indices")
    lib.api.spine_render_command_get_num_indices = <spine_render_command_get_num_indicesType> load_required(handle, lib.name, "spine_render_command_get_num_indices")
    lib.api.spine_render_command_get_blend_mode = <spine_render_command_get_blend_modeType> load_required(handle, lib.name, "spine_render_command_get_blend_mode")
    lib.api.spine_render_command_get_texture = <spine_render_command_get_textureType> load_required(handle, lib.name, "spine_render_command_get_texture")
    lib.api.spine_render_command_get_next = <spine_render_command_get_nextType> load_required(handle, lib.name, "spine_render_command_get_next")
    lib.api.spine_skeleton_get_physics_constraints = <spine_skeleton_get_physics_constraintsType> load_required(handle, lib.name, "spine_skeleton_get_physics_constraints")
    lib.api.spine_array_physics_constraint_size = <spine_array_physics_constraint_sizeType> load_required(handle, lib.name, "spine_array_physics_constraint_size")
    lib.api.spine_array_physics_constraint_buffer = <spine_array_physics_constraint_bufferType> load_required(handle, lib.name, "spine_array_physics_constraint_buffer")
    lib.api.spine_physics_constraint_is_active = <spine_physics_constraint_is_activeType> load_required(handle, lib.name, "spine_physics_constraint_is_active")
    lib.api.spine_physics_constraint_get_applied_pose = <spine_physics_constraint_get_applied_poseType> load_required(handle, lib.name, "spine_physics_constraint_get_applied_pose")
    lib.api.spine_physics_constraint_pose_get_mix = <spine_physics_constraint_pose_get_mixType> load_required(handle, lib.name, "spine_physics_constraint_pose_get_mix")
    # ---- end resolve ----

    lib.major = lib.api.spine_major_version()
    lib.minor = lib.api.spine_minor_version()
    spine_log("Spine: loaded {} (spine-c {}.{})".format(lib.name, lib.major, lib.minor), debug=False)

    if lib.major != 4 or lib.minor != 3:
        spine_log("Spine: Warning - expected spine-c 4.3, but loaded {}.{}".format(lib.major, lib.minor), debug=False)

    return lib
