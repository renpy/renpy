
from libc.stdint cimport uint8_t, uint32_t

# Basic Functions
ctypedef void* (__cdecl *in_retain_t)()
cdef in_retain_t in_retain
ctypedef void* (__cdecl *in_release_t)(void*)
cdef in_release_t in_release
ctypedef const char *(__cdecl *in_get_last_error_t)()
cdef in_get_last_error_t in_get_last_error

# Puppet
ctypedef in_puppet_t* (__cdecl *in_puppet_load_t)(const char *file)
cdef in_puppet_load_t in_puppet_load
ctypedef in_puppet_t* (__cdecl *in_puppet_load_from_memory_t)(const uint8_t* data, uint32_t length)
cdef in_puppet_load_from_memory_t in_puppet_load_from_memory
ctypedef void (__cdecl *in_puppet_free_t)(in_puppet_t* obj)
cdef in_puppet_free_t in_puppet_free
ctypedef const char* (__cdecl *in_puppet_get_name_t)(in_puppet_t* obj)
cdef in_puppet_get_name_t in_puppet_get_name
ctypedef bint (__cdecl *in_puppet_get_physics_enabled_t)(in_puppet_t* obj)
cdef in_puppet_get_physics_enabled_t in_puppet_get_physics_enabled
ctypedef void (__cdecl *in_puppet_set_physics_enabled_t)(in_puppet_t* obj, bint value)
cdef in_puppet_set_physics_enabled_t in_puppet_set_physics_enabled
ctypedef float (__cdecl *in_puppet_get_pixels_per_meter_t)(in_puppet_t* obj)
cdef in_puppet_get_pixels_per_meter_t in_puppet_get_pixels_per_meter
ctypedef void (__cdecl *in_puppet_set_pixels_per_meter_t)(in_puppet_t* obj, float value)
cdef in_puppet_set_pixels_per_meter_t in_puppet_set_pixels_per_meter
ctypedef float (__cdecl *in_puppet_get_gravity_t)(in_puppet_t* obj)
cdef in_puppet_get_gravity_t in_puppet_get_gravity
ctypedef void (__cdecl *in_puppet_set_gravity_t)(in_puppet_t* obj, float value)
cdef in_puppet_set_gravity_t in_puppet_set_gravity
ctypedef void (__cdecl *in_puppet_update_t)(in_puppet_t* obj, float delta)
cdef in_puppet_update_t in_puppet_update
ctypedef void (__cdecl *in_puppet_draw_t)(in_puppet_t* obj, float delta)
cdef in_puppet_draw_t in_puppet_draw
ctypedef void (__cdecl *in_puppet_reset_drivers_t)(in_puppet_t* obj)
cdef in_puppet_reset_drivers_t in_puppet_reset_drivers
ctypedef in_texture_cache_t* (__cdecl *in_puppet_get_texture_cache_t)(in_puppet_t* obj)
cdef in_puppet_get_texture_cache_t in_puppet_get_texture_cache
ctypedef in_parameter_t** (__cdecl *in_puppet_get_parameters_t)(in_puppet_t* obj, uint32_t* count)
cdef in_puppet_get_parameters_t in_puppet_get_parameters
ctypedef in_drawlist_t* (__cdecl *in_puppet_get_drawlist_t)(in_puppet_t* obj)
cdef in_puppet_get_drawlist_t in_puppet_get_drawlist

# Parameter
ctypedef const char* (__cdecl *in_parameter_get_name_t)(in_parameter_t* obj)
cdef in_parameter_get_name_t in_parameter_get_name
ctypedef bint (__cdecl *in_parameter_get_active_t)(in_parameter_t* obj)
cdef in_parameter_get_active_t in_parameter_get_active
ctypedef uint32_t (__cdecl *in_parameter_get_dimensions_t)(in_parameter_t* obj)
cdef in_parameter_get_dimensions_t in_parameter_get_dimensions
ctypedef in_vec2_t (__cdecl *in_parameter_get_min_value_t)(in_parameter_t* obj)
cdef in_parameter_get_min_value_t in_parameter_get_min_value
ctypedef in_vec2_t (__cdecl *in_parameter_get_max_value_t)(in_parameter_t* obj)
cdef in_parameter_get_max_value_t in_parameter_get_max_value
ctypedef in_vec2_t (__cdecl *in_parameter_get_value_t)(in_parameter_t* obj)
cdef in_parameter_get_value_t in_parameter_get_value
ctypedef void (__cdecl *in_parameter_set_value_t)(in_parameter_t* obj, in_vec2_t value)
cdef in_parameter_set_value_t in_parameter_set_value
ctypedef in_vec2_t (__cdecl *in_parameter_get_normalized_value_t)(in_parameter_t* obj)
cdef in_parameter_get_normalized_value_t in_parameter_get_normalized_value
ctypedef void (__cdecl *in_parameter_set_normalized_value_t)(in_parameter_t* obj, in_vec2_t value)
cdef in_parameter_set_normalized_value_t in_parameter_set_normalized_value

# Texture Cache
ctypedef uint32_t (__cdecl *in_texture_cache_get_size_t)(in_texture_cache_t* obj)
cdef in_texture_cache_get_size_t in_texture_cache_get_size
ctypedef in_texture_t* (__cdecl *in_texture_cache_get_texture_t)(in_texture_cache_t* obj, uint32_t slot)
cdef in_texture_cache_get_texture_t in_texture_cache_get_texture
ctypedef in_texture_t** (__cdecl *in_texture_cache_get_textures_t)(in_texture_cache_t* obj, uint32_t* count)
cdef in_texture_cache_get_textures_t in_texture_cache_get_textures
ctypedef void (__cdecl *in_texture_cache_prune_t)(in_texture_cache_t* obj)
cdef in_texture_cache_prune_t in_texture_cache_prune

# Resources
ctypedef uint32_t (__cdecl *in_resource_get_length_t)(in_resource_t* obj)
cdef in_resource_get_length_t in_resource_get_length
ctypedef void* (__cdecl *in_resource_get_id_t)(in_resource_t* obj)
cdef in_resource_get_id_t in_resource_get_id
ctypedef void (__cdecl *in_resource_set_id_t)(in_resource_t* obj, void* value)
cdef in_resource_set_id_t in_resource_set_id

# Textures
ctypedef in_texture_t* (__cdecl *in_texture_from_resource_t)(in_resource_t* obj)
cdef in_texture_from_resource_t in_texture_from_resource
ctypedef uint32_t (__cdecl *in_texture_get_width_t)(in_texture_t* obj)
cdef in_texture_get_width_t in_texture_get_width
ctypedef uint32_t (__cdecl *in_texture_get_height_t)(in_texture_t* obj)
cdef in_texture_get_height_t in_texture_get_height
ctypedef uint32_t (__cdecl *in_texture_get_channels_t)(in_texture_t* obj)
cdef in_texture_get_channels_t in_texture_get_channels
ctypedef void (__cdecl *in_texture_flip_vertically_t)(in_texture_t* obj)
cdef in_texture_flip_vertically_t in_texture_flip_vertically
ctypedef void (__cdecl *in_texture_premultiply_t)(in_texture_t* obj)
cdef in_texture_premultiply_t in_texture_premultiply
ctypedef void (__cdecl *in_texture_unpremultiply_t)(in_texture_t* obj)
cdef in_texture_unpremultiply_t in_texture_unpremultiply
ctypedef void (__cdecl *in_texture_pad_t)(in_texture_t* obj, uint32_t thickness)
cdef in_texture_pad_t in_texture_pad
ctypedef void* (__cdecl *in_texture_get_pixels_t)(in_texture_t* obj)
cdef in_texture_get_pixels_t in_texture_get_pixels

# DrawList
ctypedef bint (__cdecl *in_drawlist_get_use_base_vertex_t)(in_drawlist_t* obj)
cdef in_drawlist_get_use_base_vertex_t in_drawlist_get_use_base_vertex
ctypedef void (__cdecl *in_drawlist_set_use_base_vertex_t)(in_drawlist_t* obj, bint value)
cdef in_drawlist_set_use_base_vertex_t in_drawlist_set_use_base_vertex
ctypedef in_drawcmd_t* (__cdecl *in_drawlist_get_commands_t)(in_drawlist_t* obj, uint32_t* count)
cdef in_drawlist_get_commands_t in_drawlist_get_commands
ctypedef in_vtxdata_t* (__cdecl *in_drawlist_get_vertex_data_t)(in_drawlist_t* obj, uint32_t* bytes)
cdef in_drawlist_get_vertex_data_t in_drawlist_get_vertex_data
ctypedef void* (__cdecl *in_drawlist_get_index_data_t)(in_drawlist_t* obj, uint32_t* bytes)
cdef in_drawlist_get_index_data_t in_drawlist_get_index_data
ctypedef in_drawalloc_t* (__cdecl *in_drawlist_get_allocations_t)(in_drawlist_t* obj, uint32_t* count)
cdef in_drawlist_get_allocations_t in_drawlist_get_allocations

cdef bint did_load = False
def load(dll):
    global did_load
    if did_load:
        return True
    
    did_load = True
    
    cdef void* object = NULL
    if dll:
        object = load_inochi2d_object(dll)

        if not object:
            return False
    
    global in_retain
    in_retain = <in_retain_t> load_inochi2d_function(object, "in_retain")
    global in_release
    in_release = <in_release_t> load_inochi2d_function(object, "in_release")
    global in_get_last_error
    in_get_last_error = <in_get_last_error_t> load_inochi2d_function(object, "in_get_last_error")
    global in_puppet_load
    in_puppet_load = <in_puppet_load_t> load_inochi2d_function(object, "in_puppet_load")
    global in_puppet_load_from_memory
    in_puppet_load_from_memory = <in_puppet_load_from_memory_t> load_inochi2d_function(object, "in_puppet_load_from_memory")
    global in_puppet_free
    in_puppet_free = <in_puppet_free_t> load_inochi2d_function(object, "in_puppet_free")
    global in_puppet_get_name
    in_puppet_get_name = <in_puppet_get_name_t> load_inochi2d_function(object, "in_puppet_get_name")
    global in_puppet_get_physics_enabled
    in_puppet_get_physics_enabled = <in_puppet_get_physics_enabled_t> load_inochi2d_function(object, "in_puppet_get_physics_enabled")
    global in_puppet_set_physics_enabled
    in_puppet_set_physics_enabled = <in_puppet_set_physics_enabled_t> load_inochi2d_function(object, "in_puppet_set_physics_enabled")
    global in_puppet_get_pixels_per_meter
    in_puppet_get_pixels_per_meter = <in_puppet_get_pixels_per_meter_t> load_inochi2d_function(object, "in_puppet_get_pixels_per_meter")
    global in_puppet_set_pixels_per_meter
    in_puppet_set_pixels_per_meter = <in_puppet_set_pixels_per_meter_t> load_inochi2d_function(object, "in_puppet_set_pixels_per_meter")
    global in_puppet_get_gravity
    in_puppet_get_gravity = <in_puppet_get_gravity_t> load_inochi2d_function(object, "in_puppet_get_gravity")
    global in_puppet_set_gravity
    in_puppet_set_gravity = <in_puppet_set_gravity_t> load_inochi2d_function(object, "in_puppet_set_gravity")
    global in_puppet_update
    in_puppet_update = <in_puppet_update_t> load_inochi2d_function(object, "in_puppet_update")
    global in_puppet_draw
    in_puppet_draw = <in_puppet_draw_t> load_inochi2d_function(object, "in_puppet_draw")
    global in_puppet_reset_drivers
    in_puppet_reset_drivers = <in_puppet_reset_drivers_t> load_inochi2d_function(object, "in_puppet_reset_drivers")
    global in_puppet_get_texture_cache
    in_puppet_get_texture_cache = <in_puppet_get_texture_cache_t> load_inochi2d_function(object, "in_puppet_get_texture_cache")
    global in_puppet_get_parameters
    in_puppet_get_parameters = <in_puppet_get_parameters_t> load_inochi2d_function(object, "in_puppet_get_parameters")
    global in_puppet_get_drawlist
    in_puppet_get_drawlist = <in_puppet_get_drawlist_t> load_inochi2d_function(object, "in_puppet_get_drawlist")
    global in_parameter_get_name
    in_parameter_get_name = <in_parameter_get_name_t> load_inochi2d_function(object, "in_parameter_get_name")
    global in_parameter_get_active
    in_parameter_get_active = <in_parameter_get_active_t> load_inochi2d_function(object, "in_parameter_get_active")
    global in_parameter_get_dimensions
    in_parameter_get_dimensions = <in_parameter_get_dimensions_t> load_inochi2d_function(object, "in_parameter_get_dimensions")
    global in_parameter_get_min_value
    in_parameter_get_min_value = <in_parameter_get_min_value_t> load_inochi2d_function(object, "in_parameter_get_min_value")
    global in_parameter_get_max_value
    in_parameter_get_max_value = <in_parameter_get_max_value_t> load_inochi2d_function(object, "in_parameter_get_max_value")
    global in_parameter_get_value
    in_parameter_get_value = <in_parameter_get_value_t> load_inochi2d_function(object, "in_parameter_get_value")
    global AAAAAAAAin_parameter_set_valueAAA
    in_parameter_set_value = <in_parameter_set_value_t> load_inochi2d_function(object, "in_parameter_set_value")
    global in_parameter_get_normalized_value
    in_parameter_get_normalized_value = <in_parameter_get_normalized_value_t> load_inochi2d_function(object, "in_parameter_get_normalized_value")
    global in_parameter_set_normalized_value
    in_parameter_set_normalized_value = <in_parameter_set_normalized_value_t> load_inochi2d_function(object, "in_parameter_set_normalized_value")
    global in_texture_cache_get_size
    in_texture_cache_get_size = <in_texture_cache_get_size_t> load_inochi2d_function(object, "in_texture_cache_get_size")
    global in_texture_cache_get_texture
    in_texture_cache_get_texture = <in_texture_cache_get_texture_t> load_inochi2d_function(object, "in_texture_cache_get_texture")
    global in_texture_cache_get_textures
    in_texture_cache_get_textures = <in_texture_cache_get_textures_t> load_inochi2d_function(object, "in_texture_cache_get_textures")
    global in_texture_cache_prune
    in_texture_cache_prune = <in_texture_cache_prune_t> load_inochi2d_function(object, "in_texture_cache_prune")
    global in_resource_get_length
    in_resource_get_length = <in_resource_get_length_t> load_inochi2d_function(object, "in_resource_get_length")
    global in_resource_get_id
    in_resource_get_id = <in_resource_get_id_t> load_inochi2d_function(object, "in_resource_get_id")
    global in_resource_set_id
    in_resource_set_id = <in_resource_set_id_t> load_inochi2d_function(object, "in_resource_set_id")
    global in_texture_from_resource
    in_texture_from_resource = <in_texture_from_resource_t> load_inochi2d_function(object, "in_texture_from_resource")
    global in_texture_get_width
    in_texture_get_width = <in_texture_get_width_t> load_inochi2d_function(object, "in_texture_get_width")
    global in_texture_get_height
    in_texture_get_height = <in_texture_get_height_t> load_inochi2d_function(object, "in_texture_get_height")
    global in_texture_get_channels
    in_texture_get_channels = <in_texture_get_channels_t> load_inochi2d_function(object, "in_texture_get_channels")
    global in_texture_flip_vertically
    in_texture_flip_vertically = <in_texture_flip_vertically_t> load_inochi2d_function(object, "in_texture_flip_vertically")
    global in_texture_premultiply
    in_texture_premultiply = <in_texture_premultiply_t> load_inochi2d_function(object, "in_texture_premultiply")
    global in_texture_unpremultiply
    in_texture_unpremultiply = <in_texture_unpremultiply_t> load_inochi2d_function(object, "in_texture_unpremultiply")
    global in_texture_pad
    in_texture_pad = <in_texture_pad_t> load_inochi2d_function(object, "in_texture_pad")
    global in_texture_get_pixels
    in_texture_get_pixels = <in_texture_get_pixels_t> load_inochi2d_function(object, "in_texture_get_pixels")
    global in_drawlist_get_use_base_vertex
    in_drawlist_get_use_base_vertex = <in_drawlist_get_use_base_vertex_t> load_inochi2d_function(object, "in_drawlist_get_use_base_vertex")
    global in_drawlist_set_use_base_vertex
    in_drawlist_set_use_base_vertex = <in_drawlist_set_use_base_vertex_t> load_inochi2d_function(object, "in_drawlist_set_use_base_vertex")
    global in_drawlist_get_commands
    in_drawlist_get_commands = <in_drawlist_get_commands_t> load_inochi2d_function(object, "in_drawlist_get_commands")
    global in_drawlist_get_vertex_data
    in_drawlist_get_vertex_data = <in_drawlist_get_vertex_data_t> load_inochi2d_function(object, "in_drawlist_get_vertex_data")
    global in_drawlist_get_index_data
    in_drawlist_get_index_data = <in_drawlist_get_index_data_t> load_inochi2d_function(object, "in_drawlist_get_index_data")
    global in_drawlist_get_allocations
    in_drawlist_get_allocations = <in_drawlist_get_allocations_t> load_inochi2d_function(object, "in_drawlist_get_allocations")

    return True