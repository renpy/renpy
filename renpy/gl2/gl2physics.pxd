# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
    int source_index
    float weight
    int type
    bint reflect

cdef struct OutputData:
    int destination_index
    int vertex_index
    float scale
    float weight
    int type
    bint reflect

cdef class FloatView:
    cdef object owner
    cdef const float* data
    cdef Py_ssize_t length
    cdef Py_ssize_t stride
    cdef bint readonly

    @staticmethod
    cdef FloatView create(object owner, const float* data, int count, bint readonly)

cdef class ParameterBuffer:
    cdef tuple _views
    cdef int count
    cdef float* values
    cdef const float* minima
    cdef const float* maxima
    cdef const float* defaults
    cdef dict indices

cdef class PendulumPhysics:

    # The parameters the physics reads from and writes to.
    cdef ParameterBuffer parameters
    cdef bint _pending_inputs
    cdef bint _environment_changed
    cdef float _interpolation_weight
    cdef float _step_delta

    # The rig data.
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

    # Flat arrays indexed by global output index.
    cdef float *current_rig_outputs
    cdef float *previous_rig_outputs

    cdef float *parameter_caches
    cdef float *input_caches

    # The sorted union of the parameter indexes referenced by any input or output.
    cdef int *involved_indices
    cdef int involved_count

    cpdef void set_environment(PendulumPhysics self, float gx, float gy, float wx, float wy) except *

    cpdef tuple get_environment(PendulumPhysics self)

    cpdef void evaluate(PendulumPhysics self, float delta) except *

    cdef void _evaluate(PendulumPhysics self, float delta) noexcept nogil

    cdef void _initialize(PendulumPhysics self) noexcept nogil

    cpdef void reset(PendulumPhysics self) except *

    cdef void _update_particles(
        PendulumPhysics self,
        int setting_index,
        float total_translation_x,
        float total_translation_y,
        float total_angle,
        float wind_x,
        float wind_y,
        float threshold_value,
        float st) noexcept nogil

    cdef void _interpolate(PendulumPhysics self, float weight) noexcept nogil
