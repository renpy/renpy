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
    float scale
    float weight
    int type
    bint reflect

cdef class PendulumPhysics:
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
    cdef float fps

    cdef Options options

    cdef float current_remain_time

    # flat arrays indexed by global output index
    cdef float *current_rig_outputs
    cdef float *previous_rig_outputs

    cdef float *parameter_caches
    cdef float *parameter_input_caches

    # sorted union of the parameter indices referenced by any input or output
    cdef int *involved_indices
    cdef int involved_count

    cdef float last_update

    cdef void initialize(PendulumPhysics self, int parameter_count, float *parameter_values, const float *parameter_minimum_values, const float *parameter_maximum_values, const float *parameter_default_values, dict parameter_indices, dict rig)

    cpdef void evaluate(PendulumPhysics self, float delta) noexcept

    cdef void evaluate_c(PendulumPhysics self, float delta) noexcept nogil

    cdef void initialize_physics(PendulumPhysics self) noexcept nogil

    cdef void reset_physics(PendulumPhysics self)

    cdef void parse_physics(PendulumPhysics self, dict rig)

    cdef void update_particles(PendulumPhysics self, int setting_index, float total_translation_x, float total_translation_y, float total_angle, float wind_x, float wind_y, float threshold_value, float st) noexcept nogil

    cdef void interpolate_physics(PendulumPhysics self, float weight) noexcept nogil