from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from libc.math cimport pi, sqrtf, cosf, sinf, atan2f, fminf, fmaxf, isfinite

from renpy.gl2.gl2physics cimport Vec2, Normalization, SubRigData, Options, Particle, InputData, OutputData, PendulumPhysics

DEF TYPE_X = 0
DEF TYPE_Y = 1
DEF TYPE_ANGLE = 2

cdef float air_resistance = 5.0
cdef float maximum_weight = 100.0
cdef float movement_threshold = 0.001
cdef float max_delta_time = 5.0

cdef class PendulumPhysics:
    """
    Pendulum-chain physics for parameter-driven 2D models.

    This implements the Live2D Cubism physics algorithm but consumes a neutral rig format and has no dependency on the Cubism SDK.
    """

    def __init__(PendulumPhysics self):
        self.parameter_count = 0
        self.parameter_values = NULL
        self.parameter_minimum_values = NULL
        self.parameter_maximum_values = NULL
        self.parameter_default_values = NULL
        self.parameter_indices = None

        self.sub_rig_count = 0
        self.settings = NULL
        self.inputs = NULL
        self.input_count = 0
        self.outputs = NULL
        self.output_count = 0
        self.particles = NULL
        self.fps = 0.0

        vec2_set(&self.options.gravity, 0.0, -1.0)
        vec2_zero(&self.options.wind)

        self.current_remain_time = 0.0

        self.current_rig_outputs = NULL
        self.previous_rig_outputs = NULL
        self.parameter_caches = NULL
        self.parameter_input_caches = NULL

        self.involved_indices = NULL
        self.involved_count = 0

        self.last_update = 0.0

    def __dealloc__(PendulumPhysics self):
        if self.settings != NULL:
            free(self.settings)

        if self.inputs != NULL:
            free(self.inputs)

        if self.outputs != NULL:
            free(self.outputs)

        if self.particles != NULL:
            free(self.particles)

        if self.current_rig_outputs != NULL:
            free(self.current_rig_outputs)

        if self.previous_rig_outputs != NULL:
            free(self.previous_rig_outputs)

        if self.parameter_caches != NULL:
            free(self.parameter_caches)

        if self.parameter_input_caches != NULL:
            free(self.parameter_input_caches)

        if self.involved_indices != NULL:
            free(self.involved_indices)

    cdef void initialize(PendulumPhysics self, int parameter_count, float *parameter_values, const float *parameter_minimum_values, const float *parameter_maximum_values, const float *parameter_default_values, dict parameter_indices, dict rig):
        self.parameter_count = parameter_count
        self.parameter_values = parameter_values
        self.parameter_minimum_values = parameter_minimum_values
        self.parameter_maximum_values = parameter_maximum_values
        self.parameter_default_values = parameter_default_values
        self.parameter_indices = parameter_indices

        self.parse_physics(rig)

        self.initialize_physics()

        self.evaluate(max_delta_time)

    cdef void initialize_physics(PendulumPhysics self) noexcept nogil:
        cdef int i
        cdef int setting_index
        cdef int base_index
        cdef Particle *particle
        cdef Particle *prev_particle
        cdef Particle *base_particle

        for setting_index in range(self.sub_rig_count):
            base_index = self.settings[setting_index].base_particle_index

            base_particle = &self.particles[base_index]
            vec2_zero(&base_particle.initial_position)
            base_particle.last_position = base_particle.initial_position
            vec2_set(&base_particle.last_gravity, 0.0, 1.0)
            vec2_zero(&base_particle.velocity)
            vec2_zero(&base_particle.force)

            for i in range(1, self.settings[setting_index].particle_count):
                particle = &self.particles[base_index + i]
                prev_particle = &self.particles[base_index + i - 1]

                vec2_set(&particle.initial_position, prev_particle.initial_position.x, prev_particle.initial_position.y + particle.radius)
                particle.position = particle.initial_position
                particle.last_position = particle.initial_position
                vec2_set(&particle.last_gravity, 0.0, 1.0)
                vec2_zero(&particle.velocity)
                vec2_zero(&particle.force)

    cdef void reset_physics(PendulumPhysics self):
        vec2_set(&self.options.gravity, 0.0, -1.0)
        vec2_zero(&self.options.wind)

        with nogil:
            self.initialize_physics()

    cdef void parse_physics(PendulumPhysics self, dict rig):
        """
        Fill the flat C rig arrays from a rig dict.

        Counts are implied by the strand lists; parameter names are resolved to indices here so evaluate_c never touches Python objects.
        """

        cdef int i, j
        cdef int input_index, output_index, particle_index
        cdef list strands = rig["strands"]
        cdef dict strand
        cdef str type_
        cdef set involved = set()
        cdef list involved_list

        self.sub_rig_count = len(strands)

        self.fps = rig["fps"]

        self.input_count = 0
        self.output_count = 0
        self.particle_count = 0

        for strand in strands:
            self.input_count += len(strand["inputs"])
            self.output_count += len(strand["outputs"])
            self.particle_count += len(strand["vertices"])

        if self.settings != NULL:
            free(self.settings)
            self.settings = NULL

        if self.inputs != NULL:
            free(self.inputs)
            self.inputs = NULL

        if self.outputs != NULL:
            free(self.outputs)
            self.outputs = NULL

        if self.particles != NULL:
            free(self.particles)
            self.particles = NULL

        if self.current_rig_outputs != NULL:
            free(self.current_rig_outputs)
            self.current_rig_outputs = NULL

        if self.previous_rig_outputs != NULL:
            free(self.previous_rig_outputs)
            self.previous_rig_outputs = NULL

        if self.parameter_caches != NULL:
            free(self.parameter_caches)
            self.parameter_caches = NULL

        if self.parameter_input_caches != NULL:
            free(self.parameter_input_caches)
            self.parameter_input_caches = NULL

        if self.involved_indices != NULL:
            free(self.involved_indices)
            self.involved_indices = NULL
            self.involved_count = 0

        self.settings = <SubRigData *> malloc(sizeof(SubRigData) * self.sub_rig_count)

        if self.settings == NULL:
            raise MemoryError()

        self.inputs = <InputData *> malloc(sizeof(InputData) * self.input_count)

        if self.inputs == NULL:
            raise MemoryError()

        self.outputs = <OutputData *> malloc(sizeof(OutputData) * self.output_count)

        if self.outputs == NULL:
            raise MemoryError()

        # allocate flat C arrays for rig outputs
        self.current_rig_outputs = <float *> malloc(sizeof(float) * self.output_count)

        if self.current_rig_outputs == NULL:
            raise MemoryError()

        self.previous_rig_outputs = <float *> malloc(sizeof(float) * self.output_count)

        if self.previous_rig_outputs == NULL:
            raise MemoryError()

        # initialize output arrays
        for i in range(self.output_count):
            self.current_rig_outputs[i] = 1.0
            self.previous_rig_outputs[i] = 1.0

        # parameter caches (parameter_count and parameter_values are set by initialize before parsing)
        self.parameter_caches = <float *> malloc(sizeof(float) * self.parameter_count)

        if self.parameter_caches == NULL:
            raise MemoryError()

        self.parameter_input_caches = <float *> malloc(sizeof(float) * self.parameter_count)

        if self.parameter_input_caches == NULL:
            raise MemoryError()

        for i in range(self.parameter_count):
            self.parameter_caches[i] = 0.0
            self.parameter_input_caches[i] = self.parameter_values[i]

        self.particles = <Particle *> malloc(sizeof(Particle) * self.particle_count)

        if self.particles == NULL:
            raise MemoryError()

        input_index = 0
        output_index = 0
        particle_index = 0

        for i in range(self.sub_rig_count):
            strand = strands[i]

            normalization_position = strand["normalization_position"]
            normalization_angle = strand["normalization_angle"]

            self.settings[i].normalization_position.minimum = normalization_position[0]
            self.settings[i].normalization_position.maximum = normalization_position[1]
            self.settings[i].normalization_position.default = normalization_position[2]

            self.settings[i].normalization_angle.minimum = normalization_angle[0]
            self.settings[i].normalization_angle.maximum = normalization_angle[1]
            self.settings[i].normalization_angle.default = normalization_angle[2]

            # input
            inputs = strand["inputs"]

            self.settings[i].input_count = len(inputs)
            self.settings[i].base_input_index = input_index

            for j in range(self.settings[i].input_count):
                source, weight, type_, reflect = inputs[j]

                # resolve the source name now so evaluate_c never touches Python objects
                self.inputs[input_index + j].source_parameter_index = self.parameter_indices[source]
                involved.add(self.inputs[input_index + j].source_parameter_index)

                self.inputs[input_index + j].weight = weight / maximum_weight
                self.inputs[input_index + j].reflect = reflect

                if type_ == "x":
                    self.inputs[input_index + j].type = TYPE_X
                elif type_ == "y":
                    self.inputs[input_index + j].type = TYPE_Y
                elif type_ == "angle":
                    self.inputs[input_index + j].type = TYPE_ANGLE
                else:
                    raise Exception(f"Unknown physics input type {type_!r}")

            input_index += self.settings[i].input_count

            # output
            outputs = strand["outputs"]

            self.settings[i].output_count = len(outputs)
            self.settings[i].base_output_index = output_index

            for j in range(self.settings[i].output_count):
                destination, vertex_index, scale, weight, type_, reflect = outputs[j]

                # resolve the destination name now so evaluate_c never touches Python objects
                self.outputs[output_index + j].destination_parameter_index = self.parameter_indices[destination]
                involved.add(self.outputs[output_index + j].destination_parameter_index)

                self.outputs[output_index + j].vertex_index = vertex_index
                self.outputs[output_index + j].scale = scale
                self.outputs[output_index + j].weight = weight / maximum_weight

                if type_ == "x":
                    self.outputs[output_index + j].type = TYPE_X
                elif type_ == "y":
                    self.outputs[output_index + j].type = TYPE_Y
                elif type_ == "angle":
                    self.outputs[output_index + j].type = TYPE_ANGLE
                else:
                    raise Exception(f"Unknown physics output type {type_!r}")

                self.outputs[output_index + j].reflect = reflect

            output_index += self.settings[i].output_count

            # particle
            vertices = strand["vertices"]

            self.settings[i].particle_count = len(vertices)
            self.settings[i].base_particle_index = particle_index

            for j in range(self.settings[i].particle_count):
                mobility, delay, acceleration, radius, x, y = vertices[j]

                self.particles[particle_index + j].mobility = mobility
                self.particles[particle_index + j].delay = delay
                self.particles[particle_index + j].acceleration = acceleration
                self.particles[particle_index + j].radius = radius
                self.particles[particle_index + j].position.x = x
                self.particles[particle_index + j].position.y = y

            particle_index += self.settings[i].particle_count

        # sorted union of the parameter indices physics reads or writes - evaluate_c interpolates only these
        involved_list = sorted(involved)
        self.involved_count = len(involved_list)

        if self.involved_count > 0:
            self.involved_indices = <int *> malloc(sizeof(int) * self.involved_count)

            if self.involved_indices == NULL:
                raise MemoryError()

            for i in range(self.involved_count):
                self.involved_indices[i] = involved_list[i]

        with nogil:
            self.initialize_physics()

    cpdef void evaluate(PendulumPhysics self, float delta) noexcept:
        """
        Evaluate one step of the physics simulation.

        Updates particle positions based on input parameters, gravity, and wind, then writes results to output parameters.

        Args:
            delta: Time delta in seconds since last evaluation.
        """

        if 0.0 >= delta:
            return

        with nogil:
            self.evaluate_c(delta)

    cdef void evaluate_c(PendulumPhysics self, float delta) noexcept nogil:
        """
        Run the substep loop and write interpolated outputs.
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

        while self.current_remain_time >= physics_delta_time:
            memcpy(self.previous_rig_outputs, self.current_rig_outputs, sizeof(float) * self.output_count) # copy current_rig_outputs to previous_rig_outputs (flat array)

            # calculate the input at the timing to UpdateParticles by linear interpolation with the parameter_input_caches and parameter_values
            # parameter_caches needs to be separated from parameter_input_caches because of its role in propagating values between groups
            # only the parameters physics reads or writes are interpolated - the other cache entries are never read
            input_weight = physics_delta_time / self.current_remain_time

            for k in range(self.involved_count):
                i = self.involved_indices[k]
                self.parameter_caches[i] = self.parameter_input_caches[i] * (1.0 - input_weight) + self.parameter_values[i] * input_weight
                self.parameter_input_caches[i] = self.parameter_caches[i]

            for setting_index in range(self.sub_rig_count):
                setting = &self.settings[setting_index]
                total_angle = 0.0
                total_translation_x = 0.0
                total_translation_y = 0.0

                # load input parameters
                for i in range(setting.base_input_index, setting.base_input_index + setting.input_count):
                    physics_input = &self.inputs[i]

                    total_angle = input_get_normalized_parameter_value(
                        physics_input,
                        &total_translation_x,
                        &total_translation_y,
                        total_angle,
                        self.parameter_caches[physics_input.source_parameter_index],
                        self.parameter_minimum_values[physics_input.source_parameter_index],
                        self.parameter_maximum_values[physics_input.source_parameter_index],
                        self.parameter_default_values[physics_input.source_parameter_index],
                        &setting.normalization_position,
                        &setting.normalization_angle,
                        physics_input.weight,
                    )

                rad_angle = degrees_to_radian(-total_angle)

                original_x = total_translation_x
                total_translation_x = (original_x * cosf(rad_angle) - total_translation_y * sinf(rad_angle))
                total_translation_y = (original_x * sinf(rad_angle) + total_translation_y * cosf(rad_angle))

                # calculate particles position
                self.update_particles(
                    setting_index,
                    total_translation_x,
                    total_translation_y,
                    total_angle,
                    self.options.wind.x,
                    self.options.wind.y,
                    movement_threshold * setting.normalization_position.maximum,
                    physics_delta_time,
                )

                # update output parameters
                base_index = setting.base_particle_index

                for i in range(setting.base_output_index, setting.base_output_index + setting.output_count):
                    physics_output = &self.outputs[i]
                    particle_index = physics_output.vertex_index

                    if particle_index < 1 or particle_index >= setting.particle_count:
                        continue

                    translation_x = self.particles[base_index + particle_index].position.x - self.particles[base_index + particle_index - 1].position.x
                    translation_y = self.particles[base_index + particle_index].position.y - self.particles[base_index + particle_index - 1].position.y

                    output_value = output_get_value(
                        physics_output,
                        translation_x,
                        translation_y,
                        self.particles,
                        base_index,
                        particle_index,
                        self.options.gravity.x,
                        self.options.gravity.y,
                    )

                    # use flat array index
                    self.current_rig_outputs[i] = output_value

                    self.parameter_caches[physics_output.destination_parameter_index] = update_output_parameter_value_struct(
                        self.parameter_caches[physics_output.destination_parameter_index],
                        self.parameter_minimum_values[physics_output.destination_parameter_index],
                        self.parameter_maximum_values[physics_output.destination_parameter_index],
                        output_value,
                        physics_output,
                    )

            self.current_remain_time -= physics_delta_time

        self.interpolate_physics(self.current_remain_time / physics_delta_time)

    cdef void update_particles(PendulumPhysics self, int setting_index, float total_translation_x, float total_translation_y, float total_angle, float wind_x, float wind_y, float threshold_value, float st) noexcept nogil:
        """
        Update particle positions for a single physics strand.

        Simulates pendulum physics by applying gravity, wind, and constraints to each particle in the strand chain.
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

        total_radian = degrees_to_radian(total_angle)
        current_gravity.x = sinf(total_radian)
        current_gravity.y = cosf(total_radian)
        vec2_normalize(&current_gravity)

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

            radian = direction_to_radian(particle.last_gravity.x, particle.last_gravity.y, current_gravity.x, current_gravity.y) / air_resistance

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
            vec2_normalize(&new_direction)

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

    cdef void interpolate_physics(PendulumPhysics self, float weight) noexcept nogil:
        """
        Interpolate physics output parameters between previous and current values.

        Called after the physics loop to smooth parameter values based on the remaining time fraction.
        """

        cdef int i
        cdef int setting_index, dest_index

        cdef float interpolated_value
        cdef float new_value

        cdef SubRigData *setting

        cdef OutputData *physics_output

        # interpolate output parameters
        for setting_index in range(self.sub_rig_count):
            setting = &self.settings[setting_index]

            for i in range(setting.base_output_index, setting.base_output_index + setting.output_count):
                physics_output = &self.outputs[i]

                dest_index = physics_output.destination_parameter_index

                # use flat array indexing
                interpolated_value = self.previous_rig_outputs[i] * (1.0 - weight) + self.current_rig_outputs[i] * weight

                new_value = update_output_parameter_value_struct(
                    self.parameter_values[dest_index],
                    self.parameter_minimum_values[dest_index],
                    self.parameter_maximum_values[dest_index],
                    interpolated_value,
                    physics_output,
                )

                # a NaN should never escape
                if isfinite(new_value):
                    self.parameter_values[dest_index] = new_value

cdef inline void vec2_normalize(Vec2 *v) noexcept nogil:
    cdef float length = sqrtf(v.x * v.x + v.y * v.y)

    if length > 0.0:
        v.x /= length
        v.y /= length

cdef inline void vec2_zero(Vec2 *v) noexcept nogil:
    v.x = 0.0
    v.y = 0.0

cdef inline void vec2_set(Vec2 *v, float x, float y) noexcept nogil:
    v.x = x
    v.y = y

cdef inline float input_get_normalized_parameter_value(InputData *inp, float *translation_x, float *translation_y, float target_angle, float value, float parameter_minimum, float parameter_maximum, float parameter_default, Normalization *normalization_position, Normalization *normalization_angle, float weight) noexcept nogil:
    """
    Calculate normalized parameter value and update translation/angle based on input type.
    """

    if inp.type == TYPE_X:
        translation_x[0] += weight * normalize_parameter_value(
            value, parameter_minimum, parameter_maximum, parameter_default,
            normalization_position.minimum, normalization_position.maximum,
            normalization_position.default, inp.reflect)
    elif inp.type == TYPE_Y:
        translation_y[0] += weight * normalize_parameter_value(
            value, parameter_minimum, parameter_maximum, parameter_default,
            normalization_position.minimum, normalization_position.maximum,
            normalization_position.default, inp.reflect)
    elif inp.type == TYPE_ANGLE:
        target_angle += weight * normalize_parameter_value(
            value, parameter_minimum, parameter_maximum, parameter_default,
            normalization_angle.minimum, normalization_angle.maximum,
            normalization_angle.default, inp.reflect)

    return target_angle

cdef inline float output_get_value(OutputData *out, float translation_x, float translation_y, Particle *particles, int particle_base_index, int particle_index, float parent_gravity_x, float parent_gravity_y) noexcept nogil:
    """
    Calculate the output value based on particle positions and output type.
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

        output = direction_to_radian(gravity_x, gravity_y, translation_x, translation_y)

    if out.reflect:
        return -output

    return output

cdef inline float update_output_parameter_value_struct(float parameter_value, float parameter_value_minimum, float parameter_value_maximum, float translation, OutputData *output) noexcept nogil:
    """
    Update an output parameter value with clamping and weight blending.

    Applies the output scale to the translation, clamps to parameter bounds, and blends with the current value based on output weight.
    """

    cdef float value = translation * output.scale

    if value < parameter_value_minimum:
        value = parameter_value_minimum
    elif value > parameter_value_maximum:
        value = parameter_value_maximum

    if output.weight >= 1.0:
        return value

    return parameter_value * (1.0 - output.weight) + value * output.weight

cdef inline float degrees_to_radian(float degrees) noexcept nogil:
    return pi * degrees / 180.0

cdef inline float direction_to_radian(float from_x, float from_y, float to_x, float to_y) noexcept nogil:
    """
    Calculate the signed angle from one direction vector to another.
    """

    return atan2f(from_x * to_y - from_y * to_x, from_x * to_x + from_y * to_y)

cdef inline float normalize_parameter_value(float value, float parameter_minimum, float parameter_maximum, float parameter_default, float normalized_minimum, float normalized_maximum, float normalized_default, bint is_inverted) noexcept nogil:
    """
    Normalize a parameter value from source range to target normalized range.

    Maps a value from its parameter range to the physics normalization range, handling asymmetric ranges around the default value.
    """

    cdef float result = 0.0
    cdef float max_value = fmaxf(parameter_minimum, parameter_maximum)
    cdef float min_value
    cdef float min_norm_value, max_norm_value, middle_norm_value
    cdef float middle_value, param_value
    cdef float n_length, p_length

    if max_value < value:
        value = max_value

    min_value = fminf(parameter_minimum, parameter_maximum)

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