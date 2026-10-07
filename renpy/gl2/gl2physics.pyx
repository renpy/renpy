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

from libc.limits cimport INT_MAX
from libc.stdint cimport SIZE_MAX, uintptr_t
from libc.string cimport memcpy, strcmp
from libc.math cimport pi, sqrtf, cosf, sinf, atan2f, fminf, fmaxf, isfinite, fabsf

from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.buffer cimport PyBuffer_IsContiguous, PyBUF_FORMAT, PyBUF_ND, PyBUF_STRIDES, PyBUF_WRITABLE
from cpython.memoryview cimport PyMemoryView_GET_BUFFER

cimport cython

from renpy.gl2.gl2physics cimport (
    Vec2, Normalization, SubRigData, Options, Particle, InputData, OutputData, ParameterBuffer, PendulumPhysics
)

import operator

cdef enum:
    TYPE_X = 0
    TYPE_Y = 1
    TYPE_ANGLE = 2

cdef float air_resistance = 5.0
cdef float maximum_weight = 100.0
cdef float movement_threshold = 0.001
cdef float max_delta_time = 5.0

cdef float settle_tolerance = 1e-7

cdef void* _allocate(size_t count, size_t item_size) except? NULL:
    cdef void* result

    if count == 0:
        return NULL

    if count > SIZE_MAX / item_size:
        raise MemoryError("Physics allocation is too large.")

    result = PyMem_Malloc(count * item_size)

    if result == NULL:
        raise MemoryError()

    return result

cdef float _get_finite_float(object value) except *:
    cdef float result = value

    if not isfinite(result):
        raise ValueError(f"Physics value must be a finite float, not {value!r}.")

    return result

cdef inline void _normalize_vec2(Vec2 *v) noexcept nogil:
    cdef float length = sqrtf(v.x * v.x + v.y * v.y)

    if length > 0.0:
        v.x /= length
        v.y /= length

cdef inline void _zero_vec2(Vec2 *v) noexcept nogil:
    v.x = 0.0
    v.y = 0.0

cdef inline void _set_vec2(Vec2 *v, float x, float y) noexcept nogil:
    v.x = x
    v.y = y

cdef inline float _degrees_to_radian(float degrees) noexcept nogil:
    return pi * degrees / 180.0

cdef inline float _direction_to_radian(float from_x, float from_y, float to_x, float to_y) noexcept nogil:
    """
    Calculate the signed angle from one direction vector to another.
    """

    return atan2f(from_x * to_y - from_y * to_x, from_x * to_x + from_y * to_y)

cdef inline float _get_normalized_input(
    InputData *inp,
    float *translation_x,
    float *translation_y,
    float target_angle,
    float value,
    float minimum,
    float maximum,
    float default,
    Normalization *normalization_position,
    Normalization *normalization_angle,
    float weight
) noexcept nogil:
    """
    Calculate the normalized parameter value, and update the translation or
    angle based on the input type.
    """

    if inp.type == TYPE_X:
        translation_x[0] += weight * _normalize_parameter(
            value,
            minimum,
            maximum,
            default,
            normalization_position.minimum,
            normalization_position.maximum,
            normalization_position.default,
            inp.reflect,
            )
    elif inp.type == TYPE_Y:
        translation_y[0] += weight * _normalize_parameter(
            value,
            minimum,
            maximum,
            default,
            normalization_position.minimum,
            normalization_position.maximum,
            normalization_position.default,
            inp.reflect,
            )
    elif inp.type == TYPE_ANGLE:
        target_angle += weight * _normalize_parameter(
            value,
            minimum,
            maximum,
            default,
            normalization_angle.minimum,
            normalization_angle.maximum,
            normalization_angle.default,
            inp.reflect,
            )

    return target_angle

cdef inline float _get_output(
    OutputData *out,
    float translation_x,
    float translation_y,
    Particle *particles,
    int particle_base_index,
    int particle_index,
    float parent_gravity_x,
    float parent_gravity_y
) noexcept nogil:
    """
    Calculate the output value based on the particle positions and the output
    type.
    """

    cdef float output = 0.0
    cdef float gravity_x, gravity_y

    if out.type == TYPE_X:
        output = translation_x
    elif out.type == TYPE_Y:
        output = translation_y
    elif out.type == TYPE_ANGLE:
        if particle_index >= 2:
            particle_index += particle_base_index
            gravity_x = particles[particle_index - 1].position.x - particles[particle_index - 2].position.x
            gravity_y = particles[particle_index - 1].position.y - particles[particle_index - 2].position.y
        else:
            gravity_x = -1.0 * parent_gravity_x
            gravity_y = -1.0 * parent_gravity_y

        output = _direction_to_radian(gravity_x, gravity_y, translation_x, translation_y)

    if out.reflect:
        return -output

    return output

cdef inline float _update_output(
    float parameter_value,
    float minimum,
    float maximum,
    float translation,
    OutputData *output
) noexcept nogil:
    """
    Update an output parameter value, with clamping and weight blending.
    """

    cdef float value = translation * output.scale

    if value < minimum:
        value = minimum
    elif value > maximum:
        value = maximum

    if output.weight >= 1.0:
        return value

    return parameter_value * (1.0 - output.weight) + value * output.weight

cdef inline float _normalize_parameter(
    float value,
    float minimum,
    float maximum,
    float default,
    float normalized_minimum,
    float normalized_maximum,
    float normalized_default,
    bint is_inverted
) noexcept nogil:
    """
    Normalize a parameter value from its source range to the target normalized
    range.
    """

    cdef float result = 0.0
    cdef float max_value = fmaxf(minimum, maximum)
    cdef float min_value
    cdef float min_norm_value, max_norm_value, middle_norm_value
    cdef float middle_value, param_value
    cdef float n_length, p_length

    if max_value < value:
        value = max_value

    min_value = fminf(minimum, maximum)

    if min_value > value:
        value = min_value

    min_norm_value = fminf(normalized_minimum, normalized_maximum)
    max_norm_value = fmaxf(normalized_minimum, normalized_maximum)
    middle_norm_value = normalized_default

    middle_value = 0.5 * (fminf(min_value, max_value) + fmaxf(min_value, max_value))
    param_value = value - middle_value

    if param_value > 0:
        n_length = max_norm_value - middle_norm_value
        p_length = max_value - middle_value

        if p_length != 0.0:
            result = param_value * (n_length / p_length)
            result += middle_norm_value
    elif param_value < 0:
        n_length = min_norm_value - middle_norm_value
        p_length = min_value - middle_value

        if p_length != 0.0:
            result = param_value * (n_length / p_length)
            result += middle_norm_value
    else:
        result = middle_norm_value

    if is_inverted:
        return result

    return -result

@cython.final
cdef class FloatView:
    """
    Export borrowed floats while keeping their storage owner alive.
    """

    def __init__(self, *args, **kwargs):
        raise TypeError("FloatView must be created from an owner and a C pointer.")

    @staticmethod
    cdef FloatView create(object owner, const float* data, int count, bint readonly):
        cdef FloatView view

        if owner is None or count < 0 or (count and data == NULL):
            raise ValueError("A float view requires an owner and a valid pointer.")

        view = FloatView.__new__(FloatView)
        view.owner = owner
        view.data = data
        view.length = count
        view.stride = sizeof(float)
        view.readonly = readonly

        return view

    def __getbuffer__(self, Py_buffer* info, int flags):
        if self.owner is None:
            raise BufferError("Float view is not initialized.")

        if self.readonly and (flags & PyBUF_WRITABLE):
            raise BufferError("Buffer is read-only.")

        info.buf = <void*> self.data
        info.obj = self
        info.len = self.length * sizeof(float)
        info.itemsize = sizeof(float)
        info.readonly = self.readonly
        info.ndim = 1
        info.format = <char*> "f" if (flags & PyBUF_FORMAT) else NULL
        info.shape = &self.length if (flags & PyBUF_ND) else NULL
        info.strides = &self.stride if ((flags & PyBUF_STRIDES) == PyBUF_STRIDES) else NULL
        info.suboffsets = NULL
        info.internal = NULL

cdef class ParameterBuffer:
    """
    Bind contiguous float parameters without copying their values.

    Buffer exports stay pinned for this object's lifetime. Bounds and defaults must remain unchanged while bound.
    """

    def __cinit__(ParameterBuffer self, values, minimum, maximum, defaults, dict indices not None):
        cdef int i
        cdef Py_buffer* view
        cdef object index

        self._views = (memoryview(values), memoryview(minimum), memoryview(maximum), memoryview(defaults))

        for i in range(4):
            view = PyMemoryView_GET_BUFFER(self._views[i])

            if i == 0 and view.readonly:
                raise BufferError("Physics parameter values must be writable.")

            if not PyBuffer_IsContiguous(view, "C"):
                raise BufferError("Physics parameters require contiguous buffers.")

            if view.ndim != 1 or view.itemsize != sizeof(float) or view.format == NULL:
                raise ValueError("Physics parameters require one-dimensional native float buffers.")

            if strcmp(view.format, "f") != 0 and strcmp(view.format, "@f") != 0:
                raise ValueError("Physics parameters require native float buffers.")

            if view.len and <uintptr_t> view.buf % sizeof(float) != 0:
                raise ValueError("Physics parameter buffers must be float-aligned.")

            if view.len != PyMemoryView_GET_BUFFER(self._views[0]).len:
                raise ValueError("Physics parameter buffers must have matching lengths.")

        if PyMemoryView_GET_BUFFER(self._views[0]).shape[0] > INT_MAX:
            raise ValueError("Physics parameter count exceeds the supported range.")

        self.count = PyMemoryView_GET_BUFFER(self._views[0]).shape[0]
        self.indices = indices.copy()
        self.values = <float*> PyMemoryView_GET_BUFFER(self._views[0]).buf
        self.minima = <const float*> PyMemoryView_GET_BUFFER(self._views[1]).buf
        self.maxima = <const float*> PyMemoryView_GET_BUFFER(self._views[2]).buf
        self.defaults = <const float*> PyMemoryView_GET_BUFFER(self._views[3]).buf

        for name, index in self.indices.items():
            index = operator.index(index)

            if not 0 <= index < self.count:
                raise ValueError(f"Physics parameter {name!r} index {index} is outside [0, {self.count}).")

            self.indices[name] = index

        for i in range(self.count):
            if not (isfinite(self.values[i]) and isfinite(self.minima[i])
                    and isfinite(self.maxima[i]) and isfinite(self.defaults[i])):
                raise ValueError(f"Physics parameter {i} contains a non-finite value.")

            if not self.minima[i] <= self.defaults[i] <= self.maxima[i]:
                raise ValueError(f"Physics parameter {i} default is outside its bounds.")

    def __len__(ParameterBuffer self):
        return self.count

cdef class PendulumPhysics:
    """
    Pendulum-chain physics for parameter-driven models.

    Primarily derived from the Live2D Cubism physics algorithm.
    """

    def __cinit__(PendulumPhysics self, ParameterBuffer parameters not None, dict rig not None):
        cdef int i, j
        cdef int input_index, output_index, particle_index
        cdef list strands = rig["strands"]
        cdef dict strand
        cdef str type_
        cdef set involved = set()
        cdef list involved_list
        cdef object count

        self.parameters = parameters

        _set_vec2(&self.options.gravity, 0.0, -1.0)
        _zero_vec2(&self.options.wind)

        if len(strands) > INT_MAX:
            raise ValueError("Physics strand count exceeds the supported range.")

        self.sub_rig_count = len(strands)

        self.fps = rig["fps"]

        if not isfinite(self.fps) or not 0.0 <= self.fps <= 1000.0:
            raise ValueError(f"Physics fps must be finite and in [0, 1000], not {self.fps!r}.")

        self.input_count = 0
        self.output_count = 0
        self.particle_count = 0

        for strand in strands:
            if not strand["vertices"]:
                raise ValueError("Physics strands must contain a root vertex.")

            for key in ("inputs", "outputs", "vertices"):
                if len(strand[key]) > INT_MAX:
                    raise ValueError(f"Physics strand {key} count exceeds the supported range.")

            count = self.input_count + <object> len(strand["inputs"])

            if count > INT_MAX:
                raise ValueError("Physics input count exceeds the supported range.")

            self.input_count = count

            count = self.output_count + <object> len(strand["outputs"])

            if count > INT_MAX:
                raise ValueError("Physics output count exceeds the supported range.")

            self.output_count = count

            count = self.particle_count + <object> len(strand["vertices"])

            if count > INT_MAX:
                raise ValueError("Physics particle count exceeds the supported range.")

            self.particle_count = count

        self.settings = <SubRigData*> _allocate(self.sub_rig_count, sizeof(SubRigData))
        self.inputs = <InputData*> _allocate(self.input_count, sizeof(InputData))
        self.outputs = <OutputData*> _allocate(self.output_count, sizeof(OutputData))
        self.current_rig_outputs = <float*> _allocate(self.output_count, sizeof(float))
        self.previous_rig_outputs = <float*> _allocate(self.output_count, sizeof(float))
        self.parameter_caches = <float*> _allocate(self.parameters.count, sizeof(float))
        self.input_caches = <float*> _allocate(self.parameters.count, sizeof(float))
        self.particles = <Particle*> _allocate(self.particle_count, sizeof(Particle))

        input_index = 0
        output_index = 0
        particle_index = 0

        for i in range(self.sub_rig_count):
            strand = strands[i]

            normalization_position = strand["normalization_position"]
            normalization_angle = strand["normalization_angle"]

            for normalization in (normalization_position, normalization_angle):
                if len(normalization) != 3 or not all(isfinite(_get_finite_float(v)) for v in normalization):
                    raise ValueError(f"Physics normalization must contain three finite values: {normalization!r}.")

                if not normalization[0] <= normalization[2] <= normalization[1]:
                    raise ValueError(f"Physics normalization default is outside its bounds: {normalization!r}.")

            self.settings[i].normalization_position.minimum = normalization_position[0]
            self.settings[i].normalization_position.maximum = normalization_position[1]
            self.settings[i].normalization_position.default = normalization_position[2]

            self.settings[i].normalization_angle.minimum = normalization_angle[0]
            self.settings[i].normalization_angle.maximum = normalization_angle[1]
            self.settings[i].normalization_angle.default = normalization_angle[2]

            # The inputs.
            inputs = strand["inputs"]

            self.settings[i].input_count = len(inputs)
            self.settings[i].base_input_index = input_index

            for j in range(self.settings[i].input_count):
                source, weight, type_, reflect = inputs[j]

                # Resolve the source name.
                self.inputs[input_index + j].source_index = self.parameters.indices[source]
                involved.add(self.inputs[input_index + j].source_index)

                self.inputs[input_index + j].weight = weight / maximum_weight

                if not isfinite(self.inputs[input_index + j].weight):
                    raise ValueError(f"Physics input weight must be finite: {weight!r}.")

                self.inputs[input_index + j].reflect = reflect

                if type_ == "x":
                    self.inputs[input_index + j].type = TYPE_X
                elif type_ == "y":
                    self.inputs[input_index + j].type = TYPE_Y
                elif type_ == "angle":
                    self.inputs[input_index + j].type = TYPE_ANGLE
                else:
                    raise ValueError(f"Unknown physics input type {type_!r}")

            input_index += self.settings[i].input_count

            # The outputs.
            outputs = strand["outputs"]

            self.settings[i].output_count = len(outputs)
            self.settings[i].base_output_index = output_index

            for j in range(self.settings[i].output_count):
                if len(outputs[j]) != 6:
                    raise ValueError("Physics outputs must contain six fields.")

                destination, vertex_index, scale, weight, type_, reflect = outputs[j]
                vertex_index = operator.index(vertex_index)

                if not 1 <= vertex_index < len(strand["vertices"]):
                    raise ValueError(f"Physics output vertex {vertex_index} is outside the strand.")

                # Resolve the destination name.
                self.outputs[output_index + j].destination_index = self.parameters.indices[destination]
                involved.add(self.outputs[output_index + j].destination_index)

                self.outputs[output_index + j].vertex_index = vertex_index
                self.outputs[output_index + j].scale = scale
                self.outputs[output_index + j].weight = weight / maximum_weight

                if not (isfinite(self.outputs[output_index + j].scale)
                        and isfinite(self.outputs[output_index + j].weight)):
                    raise ValueError("Physics output scale and weight must be finite.")

                if type_ == "x":
                    self.outputs[output_index + j].type = TYPE_X
                elif type_ == "y":
                    self.outputs[output_index + j].type = TYPE_Y
                elif type_ == "angle":
                    self.outputs[output_index + j].type = TYPE_ANGLE
                else:
                    raise ValueError(f"Unknown physics output type {type_!r}")

                self.outputs[output_index + j].reflect = reflect

            output_index += self.settings[i].output_count

            # The particles.
            vertices = strand["vertices"]

            self.settings[i].particle_count = len(vertices)
            self.settings[i].base_particle_index = particle_index

            for j in range(self.settings[i].particle_count):
                mobility, delay, acceleration, radius, x, y = vertices[j]

                if not all(isfinite(_get_finite_float(v)) for v in vertices[j]):
                    raise ValueError(f"Physics vertex must contain finite values: {vertices[j]!r}.")

                if mobility < 0.0 or delay < 0.0 or radius < 0.0 or (j > 0 and radius == 0.0):
                    raise ValueError(f"Physics vertex has invalid mobility, delay, or radius: {vertices[j]!r}.")

                self.particles[particle_index + j].mobility = mobility
                self.particles[particle_index + j].delay = delay
                self.particles[particle_index + j].acceleration = acceleration
                self.particles[particle_index + j].radius = radius
                self.particles[particle_index + j].position.x = x
                self.particles[particle_index + j].position.y = y

            particle_index += self.settings[i].particle_count

        # The sorted union of the parameter indexes the physics reads or writes.
        involved_list = sorted(involved)
        self.involved_count = len(involved_list)

        if self.involved_count > 0:
            self.involved_indices = <int*> _allocate(self.involved_count, sizeof(int))

            for i in range(self.involved_count):
                self.involved_indices[i] = involved_list[i]

        PendulumPhysics.reset(self)

    def __dealloc__(PendulumPhysics self):
        PyMem_Free(self.settings)
        PyMem_Free(self.inputs)
        PyMem_Free(self.outputs)
        PyMem_Free(self.particles)
        PyMem_Free(self.current_rig_outputs)
        PyMem_Free(self.previous_rig_outputs)
        PyMem_Free(self.parameter_caches)
        PyMem_Free(self.input_caches)
        PyMem_Free(self.involved_indices)

    cdef void _initialize(PendulumPhysics self) noexcept nogil:
        cdef int i
        cdef int setting_index
        cdef int base_index
        cdef Particle *particle
        cdef Particle *prev_particle
        cdef Particle *base_particle

        for setting_index in range(self.sub_rig_count):
            base_index = self.settings[setting_index].base_particle_index

            base_particle = &self.particles[base_index]
            _zero_vec2(&base_particle.initial_position)
            base_particle.position = base_particle.initial_position
            base_particle.last_position = base_particle.initial_position
            _set_vec2(&base_particle.last_gravity, 0.0, 1.0)
            _zero_vec2(&base_particle.velocity)
            _zero_vec2(&base_particle.force)

            for i in range(1, self.settings[setting_index].particle_count):
                particle = &self.particles[base_index + i]
                prev_particle = &self.particles[base_index + i - 1]

                _set_vec2(
                    &particle.initial_position,
                    prev_particle.initial_position.x,
                    prev_particle.initial_position.y + particle.radius,
                    )

                particle.position = particle.initial_position
                particle.last_position = particle.initial_position
                _set_vec2(&particle.last_gravity, 0.0, 1.0)
                _zero_vec2(&particle.velocity)
                _zero_vec2(&particle.force)

    cpdef void reset(PendulumPhysics self) except *:
        """
        Reset all simulation history from the current parameters, preserving gravity and wind.
        """

        cdef int i

        self.current_remain_time = 0.0
        self._interpolation_weight = 0.0
        self._step_delta = 1.0 / self.fps if self.fps > 0.0 else 1.0 / 30.0

        for i in range(self.output_count):
            self.current_rig_outputs[i] = 1.0
            self.previous_rig_outputs[i] = 1.0

        for i in range(self.parameters.count):
            self.parameter_caches[i] = 0.0
            self.input_caches[i] = self.parameters.values[i]

        with nogil:
            self._initialize()

        PendulumPhysics.evaluate(self, max_delta_time)

    cpdef void set_environment(PendulumPhysics self, float gx, float gy, float wx, float wy) except *:
        """
        Set the reference gravity for angle outputs and the wind acting on the particles.
        """

        if not (isfinite(gx) and isfinite(gy) and isfinite(wx) and isfinite(wy)):
            raise ValueError("Physics gravity and wind must be finite.")

        if (gx != self.options.gravity.x or gy != self.options.gravity.y
                or wx != self.options.wind.x or wy != self.options.wind.y):
            self._environment_changed = True

        _set_vec2(&self.options.gravity, gx, gy)
        _set_vec2(&self.options.wind, wx, wy)

    cpdef tuple get_environment(PendulumPhysics self):
        return (self.options.gravity.x, self.options.gravity.y), (self.options.wind.x, self.options.wind.y)

    cpdef void evaluate(PendulumPhysics self, float delta) except *:
        """
        Evaluate one step of the physics simulation.

        Updates the particle positions based on the input parameters, gravity,
        and wind, then writes the results to the output parameters.

        `delta`
            The time delta, in seconds, since the last evaluation.
        """

        cdef int i, index
        cdef float tolerance

        if not isfinite(delta) or delta < 0.0:
            raise ValueError(f"Physics delta must be finite and nonnegative, not {delta!r}.")

        if self.output_count == 0:
            return

        self._pending_inputs = False

        # Shared input/output parameters must be checked before interpolation overwrites their authored values.
        for i in range(self.input_count):
            index = self.inputs[i].source_index
            tolerance = settle_tolerance * fmaxf(1.0, self.parameters.maxima[index]
                                                - self.parameters.minima[index])

            if fabsf(self.parameters.values[index] - self.input_caches[index]) > tolerance:
                self._pending_inputs = True

                break

        if delta == 0.0:
            self._interpolate(self._interpolation_weight)

            return

        with nogil:
            self._evaluate(delta)

    def is_active(PendulumPhysics self):
        """
        Return whether the last evaluation leaves motion or interpolation needing another frame.
        """

        cdef int i, j, index
        cdef float tolerance, delay
        cdef Particle* particle

        if self.output_count == 0:
            return False

        if self._pending_inputs or self._environment_changed:
            return True

        for i in range(self.sub_rig_count):
            for j in range(1, self.settings[i].particle_count):
                particle = &self.particles[self.settings[i].base_particle_index + j]
                tolerance = settle_tolerance * fmaxf(1.0, particle.radius)
                delay = particle.delay * self._step_delta * 30.0

                if (fabsf(particle.position.x - particle.last_position.x) > tolerance
                        or fabsf(particle.position.y - particle.last_position.y) > tolerance
                        or fabsf(particle.velocity.x * delay) > tolerance
                        or fabsf(particle.velocity.y * delay) > tolerance):
                    return True

        for i in range(self.output_count):
            index = self.outputs[i].destination_index
            tolerance = settle_tolerance * fmaxf(1.0, self.parameters.maxima[index]
                                                - self.parameters.minima[index])

            if fabsf((self.current_rig_outputs[i] - self.previous_rig_outputs[i]) * self.outputs[i].scale) > tolerance:
                return True

        return False

    cdef void _evaluate(PendulumPhysics self, float delta) noexcept nogil:
        """
        Runs the substep loop and writes the interpolated outputs.
        """

        cdef int i, k
        cdef int setting_index, particle_index, base_index

        cdef float physics_delta_time
        cdef float input_weight
        cdef float total_angle, rad_angle
        cdef float original_x
        cdef float output_value
        cdef float total_translation_x, total_translation_y
        cdef float translation_x, translation_y

        cdef SubRigData *setting

        cdef InputData *physics_input

        cdef OutputData *physics_output

        self.current_remain_time += delta

        if self.current_remain_time > max_delta_time:
            self.current_remain_time = 0.0

        if self.fps > 0.0:
            physics_delta_time = 1.0 / self.fps
        else:
            physics_delta_time = delta

        self._step_delta = physics_delta_time

        while self.current_remain_time >= physics_delta_time:
            self._environment_changed = False

            # Copy current_rig_outputs to previous_rig_outputs.
            memcpy(self.previous_rig_outputs, self.current_rig_outputs, sizeof(float) * self.output_count)

            # Calculate the input at the timing of _update_particles by linearly
            # interpolating between input_caches and parameter.values.
            # parameter_caches needs to be separate from input_caches
            # because of its role in propagating values between groups.
            input_weight = physics_delta_time / self.current_remain_time

            for k in range(self.involved_count):
                i = self.involved_indices[k]

                self.parameter_caches[i] = (
                    self.input_caches[i] * (1.0 - input_weight)
                    + self.parameters.values[i] * input_weight
                    )

                self.input_caches[i] = self.parameter_caches[i]

            for setting_index in range(self.sub_rig_count):
                setting = &self.settings[setting_index]
                total_angle = 0.0
                total_translation_x = 0.0
                total_translation_y = 0.0

                # Load the input parameters.
                for i in range(setting.base_input_index, setting.base_input_index + setting.input_count):
                    physics_input = &self.inputs[i]

                    total_angle = _get_normalized_input(
                        physics_input,
                        &total_translation_x,
                        &total_translation_y,
                        total_angle,
                        self.parameter_caches[physics_input.source_index],
                        self.parameters.minima[physics_input.source_index],
                        self.parameters.maxima[physics_input.source_index],
                        self.parameters.defaults[physics_input.source_index],
                        &setting.normalization_position,
                        &setting.normalization_angle,
                        physics_input.weight,
                        )

                rad_angle = _degrees_to_radian(-total_angle)

                original_x = total_translation_x
                total_translation_x = (original_x * cosf(rad_angle) - total_translation_y * sinf(rad_angle))
                total_translation_y = (original_x * sinf(rad_angle) + total_translation_y * cosf(rad_angle))

                # Calculate the particle positions.
                self._update_particles(
                    setting_index,
                    total_translation_x,
                    total_translation_y,
                    total_angle,
                    self.options.wind.x,
                    self.options.wind.y,
                    movement_threshold * setting.normalization_position.maximum,
                    physics_delta_time,
                    )

                # Update the output parameters.
                base_index = setting.base_particle_index

                for i in range(setting.base_output_index, setting.base_output_index + setting.output_count):
                    physics_output = &self.outputs[i]
                    particle_index = physics_output.vertex_index

                    translation_x = (
                        self.particles[base_index + particle_index].position.x
                        - self.particles[base_index + particle_index - 1].position.x
                        )

                    translation_y = (
                        self.particles[base_index + particle_index].position.y
                        - self.particles[base_index + particle_index - 1].position.y
                        )

                    output_value = _get_output(
                        physics_output,
                        translation_x,
                        translation_y,
                        self.particles,
                        base_index,
                        particle_index,
                        self.options.gravity.x,
                        self.options.gravity.y,
                        )

                    # Use the flat array index.
                    self.current_rig_outputs[i] = output_value

                    self.parameter_caches[physics_output.destination_index] = (
                        _update_output(
                            self.parameter_caches[physics_output.destination_index],
                            self.parameters.minima[physics_output.destination_index],
                            self.parameters.maxima[physics_output.destination_index],
                            output_value,
                            physics_output,
                            )
                        )

            self.current_remain_time -= physics_delta_time

        self._interpolation_weight = self.current_remain_time / physics_delta_time
        self._interpolate(self._interpolation_weight)

    cdef void _update_particles(
        PendulumPhysics self,
        int setting_index,
        float total_translation_x,
        float total_translation_y,
        float total_angle,
        float wind_x,
        float wind_y,
        float threshold_value,
        float st
    ) noexcept nogil:
        """
        Update the particle positions for a single physics strand.

        Simulates pendulum physics by applying gravity, wind, and constraints
        to each particle in the strand chain.
        """

        cdef int i
        cdef int base_index
        cdef int particle_count_for_setting

        cdef float total_radian, radian, cos_radian, sin_radian
        cdef float delay, delay_factor
        cdef float original_dir_x
        cdef float delay_squared

        cdef Vec2 direction, new_direction
        cdef Vec2 velocity, force
        cdef Vec2 current_gravity

        cdef Particle *particle
        cdef Particle *prev_particle

        base_index = self.settings[setting_index].base_particle_index
        particle_count_for_setting = self.settings[setting_index].particle_count

        self.particles[base_index].position.x = total_translation_x
        self.particles[base_index].position.y = total_translation_y

        total_radian = _degrees_to_radian(total_angle)
        current_gravity.x = sinf(total_radian)
        current_gravity.y = cosf(total_radian)
        _normalize_vec2(&current_gravity)

        delay_factor = st * 30.0

        for i in range(base_index + 1, base_index + particle_count_for_setting):
            particle = &self.particles[i]
            prev_particle = &self.particles[i - 1]

            particle.force.x = (current_gravity.x * particle.acceleration) + wind_x
            particle.force.y = (current_gravity.y * particle.acceleration) + wind_y

            particle.last_position.x = particle.position.x
            particle.last_position.y = particle.position.y

            delay = particle.delay * delay_factor

            direction.x = particle.position.x - prev_particle.position.x
            direction.y = particle.position.y - prev_particle.position.y

            radian = _direction_to_radian(
                particle.last_gravity.x,
                particle.last_gravity.y,
                current_gravity.x,
                current_gravity.y,
                ) / air_resistance

            cos_radian = cosf(radian)
            sin_radian = sinf(radian)
            original_dir_x = direction.x
            direction.x = (cos_radian * original_dir_x) - (direction.y * sin_radian)
            direction.y = (sin_radian * original_dir_x) + (direction.y * cos_radian)

            particle.position.x = prev_particle.position.x + direction.x
            particle.position.y = prev_particle.position.y + direction.y

            velocity.x = particle.velocity.x * delay
            velocity.y = particle.velocity.y * delay

            delay_squared = delay * delay
            force.x = particle.force.x * delay_squared
            force.y = particle.force.y * delay_squared

            particle.position.x = particle.position.x + velocity.x + force.x
            particle.position.y = particle.position.y + velocity.y + force.y

            new_direction.x = particle.position.x - prev_particle.position.x
            new_direction.y = particle.position.y - prev_particle.position.y
            _normalize_vec2(&new_direction)

            particle.position.x = prev_particle.position.x + (new_direction.x * particle.radius)
            particle.position.y = prev_particle.position.y + (new_direction.y * particle.radius)

            if particle.position.x < threshold_value and particle.position.x > -threshold_value:
                particle.position.x = 0.0

            if delay != 0.0:
                particle.velocity.x = (particle.position.x - particle.last_position.x) / delay * particle.mobility
                particle.velocity.y = (particle.position.y - particle.last_position.y) / delay * particle.mobility
            else:
                particle.velocity.x = 0.0
                particle.velocity.y = 0.0

            particle.force.x = 0.0
            particle.force.y = 0.0

            particle.last_gravity.x = current_gravity.x
            particle.last_gravity.y = current_gravity.y

    cdef void _interpolate(PendulumPhysics self, float weight) noexcept nogil:
        """
        Interpolate the physics output parameters between the previous and
        current values.

        Called after the physics loop, to smooth the parameter values based on
        the remaining time fraction.
        """

        cdef int i
        cdef int setting_index, dest_index

        cdef float interpolated_value
        cdef float new_value

        cdef SubRigData *setting

        cdef OutputData *physics_output

        # Interpolate the output parameters.
        for setting_index in range(self.sub_rig_count):
            setting = &self.settings[setting_index]

            for i in range(setting.base_output_index, setting.base_output_index + setting.output_count):
                physics_output = &self.outputs[i]

                dest_index = physics_output.destination_index

                # Use flat array indexing.
                interpolated_value = (
                    self.previous_rig_outputs[i] * (1.0 - weight)
                    + self.current_rig_outputs[i] * weight
                    )

                new_value = _update_output(
                    self.parameters.values[dest_index],
                    self.parameters.minima[dest_index],
                    self.parameters.maxima[dest_index],
                    interpolated_value,
                    physics_output,
                    )

                if isfinite(new_value):
                    self.parameters.values[dest_index] = new_value
