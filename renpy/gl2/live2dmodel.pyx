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

from libc.stdint cimport intptr_t
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from libc.stdio cimport printf

from renpy.gl2.gl2mesh import TEXTURE_LAYOUT
from renpy.gl2.gl2mesh2 cimport Mesh2
from renpy.gl2.gl2physics cimport FloatView
from renpy.gl2.gl2physics import ParameterBuffer

from renpy.display.matrix cimport Matrix
from renpy.display.render cimport Render

from renpy.uguu.gl cimport GL_ZERO, GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_FUNC_ADD, GL_DST_COLOR, GL_DST_ALPHA

import renpy
import renpy.gl2.live2dblend as live2dblend
from renpy.gl2.live2dblend import BlendAnalysis, flags_blend_mode

# C versions of the live2dblend constants used while rendering.
cdef enum:
    KIND_NORMAL = 0
    KIND_ADD_COMPATIBLE = 1
    KIND_MULTIPLY_COMPATIBLE = 2
    KIND_ADVANCED = 3
    ALPHA_ATOP = 1
    ALPHA_OUT = 2

if (KIND_NORMAL, KIND_ADD_COMPATIBLE, KIND_MULTIPLY_COMPATIBLE, KIND_ADVANCED, ALPHA_ATOP, ALPHA_OUT) != (
        live2dblend.KIND_NORMAL, live2dblend.KIND_ADD_COMPATIBLE, live2dblend.KIND_MULTIPLY_COMPATIBLE,
        live2dblend.KIND_ADVANCED, live2dblend.ALPHA_ATOP, live2dblend.ALPHA_OUT):
    raise Exception("The constants in live2dmodel.pyx do not match live2dblend.py.")

cdef extern from "live2dcsm.h" nogil:
    void* load_live2d_object(const char* sofile)
    void* load_live2d_function(void* handle, const char* name)
    void deallocate_live2d_moc(void *moc)
    void deallocate_live2d_model(void *model)


cdef extern from "Live2DCubismCore.h":

    ctypedef struct csmMoc
    ctypedef struct csmModel
    ctypedef unsigned int csmVersion

    enum:
        csmAlignofMoc
        csmAlignofModel

    enum:
        csmBlendAdditive
        csmBlendMultiplicative
        csmIsDoubleSided
        csmIsInvertedMask

    enum:
        csmIsVisible
        csmVisibilityDidChange
        csmOpacityDidChange
        csmDrawOrderDidChange
        csmRenderOrderDidChange
        csmVertexPositionsDidChange

    ctypedef unsigned char csmFlags

    enum:
        csmMocVersion_Unknown
        csmMocVersion_30
        csmMocVersion_33
        csmMocVersion_40

    ctypedef unsigned int csmMocVersion

    ctypedef struct csmVector2:
        float X
        float Y

    ctypedef struct csmVector4:
        float X
        float Y
        float Z
        float W

    ctypedef void (__stdcall *csmLogFunction)(const char* message)

include "live2dcsm.pxi"


# Enable logging.
cdef void __stdcall log_function(const char *message) noexcept:
    print(message)

def post_init():
    csmSetLogFunction(log_function)

cdef class AlignedMemory:
    """
    This represents a region of aligned memory. The actual region of
    aligned memory is available through the .data pointer.
    """

    cdef void *base
    cdef void *data
    cdef int size

    def __init__(self, int size, intptr_t alignment, bytes data):
        self.base = malloc(size + alignment)
        self.data = <void *> (((<intptr_t> self.base) + alignment) & ~(alignment-1))
        self.size = size

        memcpy(self.data, <void *> <unsigned char *> data, len(data))

    def __dealloc__(self):
        free(self.base)

class Parameter(object):
    """
    Represents the information known about a parameter.
    """

    def __init__(self, index, name, minimum, maximum, default):
        self.index = index
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.remaining = 1.0

class Part(object):

    def __init__(self, index, name, default_opacity):
        self.index = index
        self.name = name
        self.default_opacity = default_opacity
        self.remaining = 1.0


cdef class Live2DModel:
    """
    Represents a Live2D model, generated from a MOC.
    """

    cdef AlignedMemory moc_data
    cdef csmMoc *moc
    cdef public csmMocVersion moc_version


    cdef AlignedMemory model_data
    cdef csmModel *model

    cdef csmVector2 pixel_size
    cdef csmVector2 pixel_origin
    cdef float pixels_per_unit

    cdef int parameter_count
    cdef const char **parameter_ids
    cdef const float *parameter_minimum_values
    cdef const float *parameter_maximum_values
    cdef const float *parameter_default_values
    cdef float *parameter_values

    cdef int part_count
    cdef const char **part_ids
    cdef float *part_opacities
    cdef const int *part_parent_part_indices

    cdef int drawable_count
    cdef const char **drawable_ids
    cdef const csmFlags *drawable_constant_flags
    cdef const csmFlags *drawable_dynamic_flags
    cdef const int *drawable_texture_indices
    cdef const int *drawable_draw_orders
    cdef const int *render_orders
    cdef const float *drawable_opacities
    cdef const int *drawable_mask_counts
    cdef const int **drawable_masks
    cdef const int *drawable_vertex_counts
    cdef const csmVector2 **drawable_vertex_positions
    cdef const csmVector2 **drawable_vertex_uvs
    cdef const int *drawable_index_counts
    cdef const unsigned short **drawable_indices
    cdef const csmVector4 *drawable_multiply_colors
    cdef const csmVector4 *drawable_screen_colors

    # The BlendAnalysis of the model.
    cdef object analysis

    # The KIND_*, color blend and alpha blend types of each member, where
    # drawable i is member i, and offscreen j is member drawable_count + j.
    cdef int *member_kinds
    cdef int *member_colors
    cdef int *member_alphas

    # Scratch space used to put the drawables in render order.
    cdef int *render_slots

    # These are only set if the model has offscreens.
    cdef int offscreen_count
    cdef const float *offscreen_opacities
    cdef const csmVector4 *offscreen_multiply_colors
    cdef const csmVector4 *offscreen_screen_colors
    cdef const int *offscreen_mask_counts
    cdef const int **offscreen_masks
    cdef const csmFlags *offscreen_constant_flags

    cdef public dict parameters
    cdef public dict parts

    cdef public dict parameter_groups
    cdef public dict opacity_groups

    cdef list meshes

    cdef object filename

    _types = """
        parameters : dict[str, Parameter]
        parts : dict[str, Part]
        parameter_groups : dict
        opacity_groups : dict
        """


    def __dealloc__(self):
        """
        Deallocates the model, and the MOC.
        """

        if self.model is not NULL:
            deallocate_live2d_model(self.model)

        if self.moc is not NULL:
            deallocate_live2d_moc(self.moc)

        free(self.member_kinds)
        free(self.member_colors)
        free(self.member_alphas)
        free(self.render_slots)

    def __init__(self, fn):
        """
        Loads the Live2D model.
        """

        cdef int i

        self.filename = fn

        with renpy.loader.load(self.filename, directory="images") as f:
            data = f.read()

        # Load the MOC.
        self.moc_data = AlignedMemory(len(data), csmAlignofMoc, data)
        self.moc = csmReviveMocInPlace(self.moc_data.data, self.moc_data.size)

        if self.moc is NULL:
            raise Exception("Could not revive Live2D MOC.")

        self.moc_version = csmGetMocVersion(self.moc_data.data, self.moc_data.size)

        # Make a model.

        cdef unsigned int model_size = csmGetSizeofModel(self.moc)
        self.model_data = AlignedMemory(model_size, csmAlignofModel, b'')
        self.model = csmInitializeModelInPlace(self.moc, self.model_data.data, self.model_data.size)

        if self.model is NULL:
            raise Exception("Could not initialize Live2D Model.")

        csmReadCanvasInfo(self.model, &(self.pixel_size), &(self.pixel_origin), &(self.pixels_per_unit))

        # Query the model for pointers to all the things.

        self.parameter_count = csmGetParameterCount(self.model)
        self.parameter_ids = csmGetParameterIds(self.model)
        self.parameter_minimum_values = csmGetParameterMinimumValues(self.model)
        self.parameter_maximum_values = csmGetParameterMaximumValues(self.model)
        self.parameter_default_values = csmGetParameterDefaultValues(self.model)
        self.parameter_values = csmGetParameterValues(self.model)

        self.part_count = csmGetPartCount(self.model)
        self.part_ids = csmGetPartIds(self.model)
        self.part_opacities = csmGetPartOpacities(self.model)
        self.part_parent_part_indices = csmGetPartParentPartIndices(self.model)

        self.drawable_count = csmGetDrawableCount(self.model)
        self.drawable_ids = csmGetDrawableIds(self.model)
        self.drawable_constant_flags = csmGetDrawableConstantFlags(self.model)
        self.drawable_dynamic_flags = csmGetDrawableDynamicFlags(self.model)
        self.drawable_texture_indices = csmGetDrawableTextureIndices(self.model)
        self.drawable_draw_orders = csmGetDrawableDrawOrders(self.model)
        self.render_orders = csmGetRenderOrders(self.model)
        self.drawable_opacities = csmGetDrawableOpacities(self.model)
        self.drawable_mask_counts = csmGetDrawableMaskCounts(self.model)
        self.drawable_masks = csmGetDrawableMasks(self.model)
        self.drawable_vertex_counts = csmGetDrawableVertexCounts(self.model)
        self.drawable_vertex_positions = csmGetDrawableVertexPositions(self.model)
        self.drawable_vertex_uvs = csmGetDrawableVertexUvs(self.model)
        self.drawable_index_counts = csmGetDrawableIndexCounts(self.model)
        self.drawable_indices = csmGetDrawableIndices(self.model)
        self.drawable_multiply_colors = csmGetDrawableMultiplyColors(self.model)
        self.drawable_screen_colors = csmGetDrawableScreenColors(self.model)

        self.offscreen_count = 0
        self.init_analysis()

        self.parameters = { }

        for i in range(self.parameter_count):
            name = self.parameter_ids[i].decode("utf-8")
            self.parameters[name] = Parameter(
                i, name,
                self.parameter_minimum_values[i],
                self.parameter_maximum_values[i],
                self.parameter_default_values[i],
                )

        self.parts = { }

        for i in range(self.part_count):
            name = self.part_ids[i].decode("utf-8")
            self.parts[name] = Part(i, name, self.part_opacities[i])

        self.opacity_groups = { }
        self.parameter_groups = { }

        csmUpdateModel(self.model)

    cdef void init_analysis(self):
        """
        Analyzes how the model's drawables and offscreens are blended. If the
        Cubism Core is too old to report the Cubism 5.3 blend modes and
        offscreens, the blend flags of Cubism 5.2 are used.
        """

        cdef int i
        cdef int drawable_count = self.drawable_count
        cdef int part_count = self.part_count
        cdef int offscreen_count = 0
        cdef int member_count

        cdef const int *drawable_blend_modes = NULL
        cdef const int *drawable_parents = NULL
        cdef const int *part_offscreens = NULL
        cdef const int *offscreen_blend_modes = NULL
        cdef const int *offscreen_owners = NULL
        cdef const int *offscreen_mask_counts = NULL

        cdef bint core_blend = not (
            csmGetDrawableBlendModes is NULL or csmGetDrawableParentPartIndices is NULL or
            csmGetPartOffscreenIndices is NULL or csmGetOffscreenCount is NULL or
            csmGetOffscreenBlendModes is NULL or csmGetOffscreenOpacities is NULL or
            csmGetOffscreenOwnerIndices is NULL or csmGetOffscreenMultiplyColors is NULL or
            csmGetOffscreenScreenColors is NULL or csmGetOffscreenMaskCounts is NULL or
            csmGetOffscreenMasks is NULL or csmGetOffscreenConstantFlags is NULL)

        if core_blend:
            drawable_blend_modes = csmGetDrawableBlendModes(self.model)
            drawable_parents = csmGetDrawableParentPartIndices(self.model)
            part_offscreens = csmGetPartOffscreenIndices(self.model)

            offscreen_count = max(csmGetOffscreenCount(self.model), 0)
            offscreen_blend_modes = csmGetOffscreenBlendModes(self.model)
            offscreen_owners = csmGetOffscreenOwnerIndices(self.model)
            offscreen_mask_counts = csmGetOffscreenMaskCounts(self.model)

            if drawable_blend_modes is NULL or drawable_parents is NULL or part_offscreens is NULL:
                core_blend = False

            elif offscreen_count and (offscreen_blend_modes is NULL or offscreen_owners is NULL or offscreen_mask_counts is NULL):
                core_blend = False

        if core_blend:
            analysis = BlendAnalysis(
                [ drawable_blend_modes[i] for i in range(drawable_count) ],
                [ drawable_parents[i] for i in range(drawable_count) ],
                [ self.part_parent_part_indices[i] for i in range(part_count) ],
                [ part_offscreens[i] for i in range(part_count) ],
                [ offscreen_blend_modes[i] for i in range(offscreen_count) ],
                [ offscreen_owners[i] for i in range(offscreen_count) ],
                [ offscreen_mask_counts[i] for i in range(offscreen_count) ],
                )

        else:
            offscreen_count = 0

            analysis = BlendAnalysis(
                [
                    flags_blend_mode(
                        self.drawable_constant_flags[i] & csmBlendAdditive != 0,
                        self.drawable_constant_flags[i] & csmBlendMultiplicative != 0)
                    for i in range(drawable_count)
                ],
                [ -1 ] * drawable_count,
                [ -1 ] * part_count,
                [ -1 ] * part_count,
                [ ], [ ], [ ],
                )

        self.analysis = analysis

        member_count = drawable_count + offscreen_count

        self.member_kinds = <int *> malloc(sizeof(int) * max(member_count, 1))
        self.member_colors = <int *> malloc(sizeof(int) * max(member_count, 1))
        self.member_alphas = <int *> malloc(sizeof(int) * max(member_count, 1))
        self.render_slots = <int *> malloc(sizeof(int) * max(drawable_count, 1))

        for i in range(drawable_count):
            self.member_kinds[i] = analysis.drawable_kinds[i]
            self.member_colors[i] = analysis.drawable_colors[i]
            self.member_alphas[i] = analysis.drawable_alphas[i]

        for i in range(offscreen_count):
            self.member_kinds[drawable_count + i] = analysis.offscreen_kinds[i]
            self.member_colors[drawable_count + i] = analysis.offscreen_colors[i]
            self.member_alphas[drawable_count + i] = analysis.offscreen_alphas[i]

        if offscreen_count == 0:
            return

        self.offscreen_count = offscreen_count
        self.offscreen_opacities = csmGetOffscreenOpacities(self.model)
        self.offscreen_multiply_colors = csmGetOffscreenMultiplyColors(self.model)
        self.offscreen_screen_colors = csmGetOffscreenScreenColors(self.model)
        self.offscreen_mask_counts = offscreen_mask_counts
        self.offscreen_masks = csmGetOffscreenMasks(self.model)
        self.offscreen_constant_flags = csmGetOffscreenConstantFlags(self.model)

    cdef Mesh2 drawable_mesh(self, int i):
        """
        Returns a mesh containing the current geometry of drawable `i`.
        """

        cdef int j

        cdef Mesh2 mesh = Mesh2(TEXTURE_LAYOUT, self.drawable_vertex_counts[i], self.drawable_index_counts[i] // 3)

        mesh.points = self.drawable_vertex_counts[i]
        memcpy(mesh.point_data, self.drawable_vertex_positions[i], sizeof(float) * mesh.points * 2)
        memcpy(mesh.attribute, self.drawable_vertex_uvs[i], sizeof(float) * mesh.points * 2)

        mesh.triangles = self.drawable_index_counts[i] // 3

        for j in range(mesh.triangles * 3):
            mesh.triangle[j] = self.drawable_indices[i][j]

        mesh.point_version = 1
        mesh.attribute_version = 1
        mesh.triangle_version = 1

        return mesh

    def __repr__(self):
        """
        Returns a string representation of the model.
        """

        return f"<Live2DModel {self.filename}>"

    def reset_parameters(self):
        """
        Resets the parameters, and resets the remaining weight to 1.0.
        """

        for i in self.parameters.values():
            self.parameter_values[i.index] = 0.0
            i.remaining = 1.0

        for i in self.parts.values():
            self.part_opacities[i.index] = 0.0
            i.remaining = 1.0


    def set_part_opacity(self, name, value):
        part = self.parts.get(name, None)

        if part is None:
            for i in self.opacity_groups.get(name, [ ]):
                self.set_part_opacity(i, value)
            return

        self.part_opacities[part.index] += value * part.remaining
        part.remaining = 0.0

    def set_parameter(self, name, value, weight=1.0):
        parameter = self.parameters.get(name, None)

        if parameter is None:
            for i in self.parameter_groups.get(name, [ ]):
                self.set_parameter(i, value, weight=weight)
            return

        weight = min(weight, parameter.remaining)

        old = self.parameter_values[parameter.index]
        self.parameter_values[parameter.index] += weight * value
        parameter.remaining -= weight

    def finish_parameters(self):
        for i in self.parameters.values():
            self.parameter_values[i.index] += i.default * i.remaining
            i.remaining = 0.0

        for i in self.parts.values():
            self.part_opacities[i.index] += i.default_opacity * i.remaining
            i.remaining = 0.0

    def blend_parameter(self, name, blend, value, weight=1.0):

        parameter = self.parameters.get(name, None)

        if parameter is None:
            for i in self.parameter_groups.get(name, [ ]):
                self.blend_parameter(i, blend, value, weight=weight)
            return

        old = self.parameter_values[parameter.index]

        if blend == "Multiply":
            value = old * value
        elif blend == "Add":
            value = old + value
        elif blend == "Overwrite":
            value = value

        self.parameter_values[parameter.index] = old + weight * (value - old)

    def blend_opacity(self, name, blend, value, weight=1.0):

        part = self.parts.get(name, None)

        if part is None:
            for i in self.opacity_groups.get(name, [ ]):
                self.blend_opacity(i, blend, value, weight=weight)
            return

        old = self.part_opacities[part.index]

        if blend == "Multiply":
            value = old * value
        elif blend == "Add":
            value = old + value
        elif blend == "Overwrite":
            value = value

        self.part_opacities[part.index] = old + weight * (value - old)


    def get_size(self):
        return (self.pixel_size.X, self.pixel_size.Y)

    def render(self, textures, zoom):

        csmUpdateModel(self.model)

        # Render the model.
        w = self.pixel_size.X * zoom
        h = self.pixel_size.Y * zoom

        offset_x = self.pixel_origin.X * zoom
        offset_y = self.pixel_origin.Y * zoom

        ppu = self.pixels_per_unit * zoom

        reverse = Matrix.offset(offset_x, offset_y, 0.0) * Matrix.scale(ppu, -ppu, 1.0)
        forward = reverse.inverse()

        return ModelRenderer(self, textures, w, h, offset_x, offset_y, ppu, reverse, forward).render()

    def get_physics_parameters(self):
        cdef int count = self.parameter_count

        return ParameterBuffer(
            FloatView.create(self, self.parameter_values, count, False),
            FloatView.create(self, self.parameter_minimum_values, count, True),
            FloatView.create(self, self.parameter_maximum_values, count, True),
            FloatView.create(self, self.parameter_default_values, count, True),
            {name: parameter.index for name, parameter in self.parameters.items()},
        )


# Blend functions used when rendering models.
REPLACE_BLEND = (GL_FUNC_ADD, GL_ONE, GL_ZERO, GL_FUNC_ADD, GL_ONE, GL_ZERO)
ADDITIVE_BLEND = (GL_FUNC_ADD, GL_ONE, GL_ONE, GL_FUNC_ADD, GL_ZERO, GL_ONE)
MULTIPLICATIVE_BLEND = (GL_FUNC_ADD, GL_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA, GL_FUNC_ADD, GL_ZERO, GL_ONE)


cdef class ModelRenderer:
    """
    Renders a single frame of a model.

    The model and each offscreen is a container, which is drawn into its own
    Render. Members using the normal or compatible blend modes are drawn into
    the container with fixed-function blending. When a member uses one of the
    other blend modes, what has been drawn into the container so far becomes
    the backdrop texture of the live2d.blend shader, and a new Render is
    started, containing a copy of the backdrop with the member drawn over it
    replacing the pixels it covers.

    A model without offscreens or blend modes is a single container whose
    drawables are drawn directly, in render order.
    """

    cdef Live2DModel model
    cdef object analysis
    cdef object textures

    # The size of the model's renders. These are Python objects, as they are
    # passed to every Render created.
    cdef object w
    cdef object h

    cdef double offset_x
    cdef double offset_y
    cdef double ppu
    cdef Matrix reverse
    cdef Matrix forward

    # A mesh, in model coordinates, that covers the model's canvas. This is
    # created when the first offscreen is composited.
    cdef Mesh2 canvas_mesh

    # Caches of renders used as masks.
    cdef dict mask_renders
    cdef dict multi_masks

    def __init__(self, Live2DModel model, textures, w, h, double offset_x, double offset_y, double ppu, Matrix reverse, Matrix forward):
        self.model = model
        self.analysis = model.analysis
        self.textures = textures
        self.w = w
        self.h = h
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ppu = ppu
        self.reverse = reverse
        self.forward = forward

        self.mask_renders = { }
        self.multi_masks = { }

    def render(self):
        """
        Returns a Render containing the model.
        """

        cdef Render rv

        acc, replaced = self.container(0)

        if acc is None:
            return Render(self.w, self.h)

        if not replaced:
            return acc

        # The model has to be drawn to a texture, so that the replacing blend
        # function doesn't affect what's behind the model.
        rv = Render(self.w, self.h)
        rv.mesh = True
        rv.add_shader("renpy.texture")
        rv.blit(acc, (0, 0))

        return rv

    cdef Render model_render(self, mesh, multiply_tuple, screen_tuple):
        """
        Creates a render with the model's coordinate system, that draws
        `mesh` with the given multiply and screen colors.
        """

        cdef Render r = Render(self.w, self.h)
        r.reverse = self.reverse
        r.forward = self.forward
        r.mesh = mesh

        r.add_uniform("u_multiply", multiply_tuple)
        r.add_uniform("u_screen", screen_tuple)

        return r

    cdef void add_position_uniforms(self, Render r):
        """
        Adds the uniforms the mask and blend shaders use to find the pixel
        a vertex is drawn to.
        """

        r.add_uniform("u_live2d_ppu", self.ppu)
        r.add_uniform("u_live2d_offset", (self.offset_x, self.offset_y))

    cdef Render drawable_render(self, int i, bint is_mask):
        """
        Returns a render that draws drawable `i`. If `is_mask` is true, the
        render is intended for use as a mask, so opacity and masks are
        ignored.
        """

        cdef Live2DModel model = self.model
        cdef csmVector4 multiply = model.drawable_multiply_colors[i]
        cdef csmVector4 screen = model.drawable_screen_colors[i]
        cdef float alpha = model.drawable_opacities[i]
        cdef Render r

        r = self.model_render(
            model.drawable_mesh(i),
            (multiply.X, multiply.Y, multiply.Z, multiply.W),
            (screen.X, screen.Y, screen.Z, screen.W))

        r.add_shader("renpy.texture")
        r.add_shader("live2d.flip_texture")
        r.add_shader("live2d.colors")

        r.blit(self.textures[model.drawable_texture_indices[i]], (0, 0))

        if is_mask:
            return r

        if alpha != 1.0:
            r.add_shader("renpy.alpha")
            r.add_uniform("u_renpy_alpha", alpha)
            r.add_uniform("u_renpy_over", 1.0)

        if model.drawable_mask_counts[i]:
            self.apply_mask(
                r,
                model.drawable_mask_counts[i],
                model.drawable_masks[i],
                model.drawable_constant_flags[i] & csmIsInvertedMask)

        return r

    cdef Render mask_render(self, int i):
        """
        Returns the cached render of drawable `i` for use as a mask.
        """

        cdef Render rv = self.mask_renders.get(i, None)

        if rv is None:
            rv = self.mask_renders[i] = self.drawable_render(i, True)

        return rv

    cdef void apply_mask(self, Render r, int count, const int *masks, bint inverted):
        """
        Masks `r` with the union of the `count` drawables in `masks`.
        """

        cdef int j
        cdef Render m

        if count == 1:
            m = self.mask_render(masks[0])

        else:
            key = tuple([ masks[j] for j in range(count) ])

            m = self.multi_masks.get(key, None)

            if m is None:
                m = Render(self.w, self.h)

                for j in key:
                    m.blit(self.mask_render(j), (0, 0))

                self.multi_masks[key] = m

        r.add_shader("-renpy.texture")

        if inverted:
            r.add_shader("live2d.inverted_mask")
        else:
            r.add_shader("live2d.mask")

        self.add_position_uniforms(r)

        # Correct the mesh oversample estimate for model coordinates.
        r.add_property("mesh_oversample_scale", 1.0 / self.ppu)

        r.blit(m, (0, 0))

    cdef bint is_flat(self, int j):
        """
        Returns true if offscreen `j` can be drawn by drawing its members
        directly into its parent.
        """

        cdef Live2DModel model = self.model
        cdef csmVector4 multiply
        cdef csmVector4 screen

        if not self.analysis.can_flatten[j]:
            return False

        if model.offscreen_opacities[j] != 1.0:
            return False

        multiply = model.offscreen_multiply_colors[j]

        if multiply.X != 1.0 or multiply.Y != 1.0 or multiply.Z != 1.0:
            return False

        screen = model.offscreen_screen_colors[j]

        if screen.X != 0.0 or screen.Y != 0.0 or screen.Z != 0.0:
            return False

        return True

    cdef list members(self, int c):
        """
        Returns the visible members of container `c`, in render order. The
        members of flattened offscreens are included in place of the
        offscreen.
        """

        cdef Live2DModel model = self.model
        cdef int drawable_count = model.drawable_count
        cdef int m
        cdef int j

        cdef int *slots = model.render_slots
        cdef int order

        # Without offscreens, the model is one container of every drawable,
        # and the render orders are a permutation of the drawables, which
        # can be inverted rather than sorted.
        if model.offscreen_count == 0:
            for m in range(drawable_count):
                slots[m] = -1

            for m in range(drawable_count):
                if model.drawable_dynamic_flags[m] & csmIsVisible == 0 or model.drawable_opacities[m] == 0.0:
                    continue

                order = model.render_orders[m]

                if order < 0 or order >= drawable_count or slots[order] != -1:
                    break

                slots[order] = m

            else:
                return [ slots[m] for m in range(drawable_count) if slots[m] != -1 ]

        ordered = [ ]

        for m in self.analysis.containers[c]:
            if m < drawable_count:
                if model.drawable_dynamic_flags[m] & csmIsVisible == 0 or model.drawable_opacities[m] == 0.0:
                    continue

            elif model.offscreen_opacities[m - drawable_count] <= 0.0:
                continue

            ordered.append((model.render_orders[m], m))

        ordered.sort()

        rv = [ ]

        for _, m in ordered:
            j = m - drawable_count

            if j >= 0 and self.is_flat(j):
                rv.extend(self.members(j + 1))
            else:
                rv.append(m)

        return rv

    cdef Render offscreen_render(self, int j, Render contents):
        """
        Returns a render that composites offscreen `j`, which has been drawn
        into `contents`, with the offscreen's opacity, colors and masks.
        """

        cdef Live2DModel model = self.model
        cdef csmVector4 multiply = model.offscreen_multiply_colors[j]
        cdef csmVector4 screen = model.offscreen_screen_colors[j]
        cdef float alpha = model.offscreen_opacities[j]
        cdef double ppu = self.ppu
        cdef Render r

        if self.canvas_mesh is None:
            self.canvas_mesh = Mesh2.texture_rectangle(
                -self.offset_x / ppu, self.offset_y / ppu, (self.w - self.offset_x) / ppu, (self.offset_y - self.h) / ppu,
                0.0, 0.0, 1.0, 1.0,
                )

        r = self.model_render(
            self.canvas_mesh,
            (multiply.X, multiply.Y, multiply.Z, multiply.W),
            (screen.X, screen.Y, screen.Z, screen.W))

        r.add_shader("renpy.texture")
        r.add_shader("live2d.colors")
        r.add_property("mesh_oversample_scale", 1.0 / ppu)

        r.blit(contents, (0, 0))

        if alpha != 1.0:
            r.add_shader("renpy.alpha")
            r.add_uniform("u_renpy_alpha", alpha)
            r.add_uniform("u_renpy_over", 1.0)

        if model.offscreen_mask_counts[j]:
            self.apply_mask(
                r,
                model.offscreen_mask_counts[j],
                model.offscreen_masks[j],
                model.offscreen_constant_flags[j] & csmIsInvertedMask)

        return r

    cdef tuple container(self, int c):
        """
        Draws container `c`. Returns a (render, replaced) tuple, where render
        is None if nothing was drawn, and replaced is true if a member was
        drawn with a blend function that replaces what's beneath it.
        """

        cdef Live2DModel model = self.model
        cdef int drawable_count = model.drawable_count
        cdef int m
        cdef int kind
        cdef int alpha
        cdef Render r
        cdef Render acc = None
        cdef Render backdrop
        cdef bint replaced = False

        for m in self.members(c):

            if m < drawable_count:
                r = self.drawable_render(m, False)

            else:
                contents, _ = self.container(m - drawable_count + 1)

                if contents is None:
                    continue

                r = self.offscreen_render(m - drawable_count, contents)

            kind = model.member_kinds[m]

            if kind == KIND_ADVANCED and acc is None:
                alpha = model.member_alphas[m]

                # With nothing beneath, Atop and Out produce nothing, and
                # the over modes produce the source.
                if alpha == ALPHA_ATOP or alpha == ALPHA_OUT:
                    continue

                kind = KIND_NORMAL

            if kind == KIND_ADVANCED:
                backdrop = Render(self.w, self.h)
                backdrop.mesh = True
                backdrop.add_shader("renpy.texture")
                backdrop.blit(acc, (0, 0))

                r.add_shader("live2d.blend")
                r.add_uniform("u_live2d_backdrop", acc)
                r.add_uniform("u_live2d_color_blend", model.member_colors[m])
                r.add_uniform("u_live2d_alpha_blend", model.member_alphas[m])
                r.add_property("blend_func", REPLACE_BLEND)
                self.add_position_uniforms(r)

                acc = Render(self.w, self.h)
                acc.blit(backdrop, (0, 0))
                acc.subpixel_blit(r, (0, 0))

                replaced = True
                continue

            if kind == KIND_ADD_COMPATIBLE:
                r.add_property("blend_func", ADDITIVE_BLEND)
            elif kind == KIND_MULTIPLY_COMPATIBLE:
                r.add_property("blend_func", MULTIPLICATIVE_BLEND)

            if acc is None:
                acc = Render(self.w, self.h)

            acc.subpixel_blit(r, (0, 0))

        return acc, replaced
