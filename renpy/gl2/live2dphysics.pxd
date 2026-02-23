cdef struct Vec2:
    float x
    float y

cdef struct Normalization:
    float minimum
    float maximum
    float default

cdef struct SubRigData:
    int input_count
    int output_count
    int particle_count
    int base_input_index
    int base_output_index
    int base_particle_index
    Normalization normalization_position
    Normalization normalization_angle

cdef struct Options:
    Vec2 gravity
    Vec2 wind

cdef struct Particle:
    Vec2 initial_position
    float mobility
    float delay
    float acceleration
    float radius
    Vec2 position
    Vec2 last_position
    Vec2 last_gravity
    Vec2 force
    Vec2 velocity

cdef struct InputData:
    int source_parameter_index
    float weight
    int type
    bint reflect

cdef struct OutputData:
    int destination_parameter_index
    int vertex_index
    Vec2 translation_scale
    float angle_scale
    float weight
    int type
    bint reflect
    float value_below_minimum
    float value_exceeded_maximum

cdef class Live2DPhysics:
    cdef int parameter_count
    cdef float *parameter_values
    cdef const float *parameter_minimum_values
    cdef const float *parameter_maximum_values
    cdef const float *parameter_default_values
    cdef dict parameter_indices

    # rig data
    cdef int sub_rig_count
    cdef SubRigData *settings
    cdef InputData *inputs
    cdef int input_count
    cdef OutputData *outputs
    cdef int output_count
    cdef Particle *particles
    cdef int particle_count
    cdef Vec2 rig_gravity
    cdef Vec2 rig_wind
    cdef float fps

    cdef Options options

    cdef float current_remain_time

    # flat arrays indexed by global output index
    cdef float *current_rig_outputs
    cdef float *previous_rig_outputs

    cdef float *parameter_caches
    cdef float *parameter_input_caches
    cdef bint parameter_caches_initialized

    cdef list input_source_ids
    cdef list output_destination_ids

    cdef float last_update

    cdef void initialize(Live2DPhysics self, int parameter_count, float *parameter_values, const float *parameter_minimum_values, const float *parameter_maximum_values, const float *parameter_default_values, dict parameter_indices, object physics_json)

    cpdef void evaluate(Live2DPhysics self, float delta)

    cdef void initialize_physics(Live2DPhysics self) noexcept nogil

    cdef void reset_physics(Live2DPhysics self)

    cdef void parse_physics(Live2DPhysics self, object physics_json)

    cdef void update_particles(Live2DPhysics self, int setting_index, int strand_count, float total_translation_x, float total_translation_y, float total_angle, float wind_x, float wind_y, float threshold_value, float st) noexcept nogil

    cdef void interpolate_physics(Live2DPhysics self, float weight) noexcept nogil