# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.display.matrix cimport Matrix
from renpy.display.render cimport Render

import renpy

cdef extern from "SDL.h" nogil:
    void* SDL_LoadObject(const char* sofile)
    void* SDL_LoadFunction(void* handle, const char* name)

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

    ctypedef void (__stdcall *csmLogFunction)(const char* message)

include "live2dcsm.pxi"


# Enable logging.
cdef void __stdcall log_function(const char *message):
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

class Part(object):

    def __init__(self, index, name):
        self.index = index
        self.name = name

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
    cdef const int *drawable_render_orders
    cdef const float *drawable_opacities
    cdef const int *drawable_mask_counts
    cdef const int **drawable_masks
    cdef const int *drawable_vertex_counts
    cdef const csmVector2 **drawable_vertex_positions
    cdef const csmVector2 **drawable_vertex_uvs
    cdef const int *drawable_index_counts
    cdef const unsigned short **drawable_indices

    cdef public dict parameters
    cdef public dict parts

    cdef public dict parameter_groups
    cdef public dict opacity_groups

    cdef list meshes

    def __init__(self, fn):
        """
        Loads the Live2D model.
        """

        cdef int i

        with renpy.loader.load(fn) as f:
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
        self.drawable_render_orders = csmGetDrawableRenderOrders(self.model)
        self.drawable_opacities = csmGetDrawableOpacities(self.model)
        self.drawable_mask_counts = csmGetDrawableMaskCounts(self.model)
        self.drawable_masks = csmGetDrawableMasks(self.model)
        self.drawable_vertex_counts = csmGetDrawableVertexCounts(self.model)
        self.drawable_vertex_positions = csmGetDrawableVertexPositions(self.model)
        self.drawable_vertex_uvs = csmGetDrawableVertexUvs(self.model)
        self.drawable_index_counts = csmGetDrawableIndexCounts(self.model)
        self.drawable_indices = csmGetDrawableIndices(self.model)

        self.parameters = { }

        for 0 <= i < self.parameter_count:
            name = self.parameter_ids[i]
            self.parameters[name] = Parameter(
                i, name,
                self.parameter_minimum_values[i],
                self.parameter_maximum_values[i],
                self.parameter_default_values[i],
                )

        self.parts = { }

        for 0 <= i < self.part_count:
            name = self.part_ids[i]
            self.parts[name] = Part(i, name)

        self.opacity_groups = { }
        self.parameter_groups = { }


        csmUpdateModel(self.model)

    def reset_parameters(self):
        for i in self.parameters.values():
            self.parameter_values[i.index] = i.default

    def set_part_opacity(self, name, value):
        part = self.parts.get(name, None)

        if part is None:
            for i in self.opacity_groups.get(name, [ ]):
                self.set_part_opacity(i, value)
            return

        self.part_opacities[part.index] = value

    def set_parameter(self, name, value, weight=1.0):
        parameter = self.parameters.get(name, None)

        if parameter is None:
            for i in self.parameter_groups.get(name, [ ]):
                self.set_parameter(i, value, weight=weight)
            return

        old = self.parameter_values[parameter.index]
        self.parameter_values[parameter.index] = old + weight * (value - old)

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

    def get_size(self):
        return (self.pixel_size.X, self.pixel_size.Y)

    def render(self, textures, zoom):

        cdef int i
        cdef int j

        cdef Render r
        cdef Render m
        cdef Render rv

        shaders = ("renpy.texture", "live2d.flip_texture")
        mask_shaders = ("live2d.mask", "live2d.flip_texture")
        inverted_mask_shaders = ("live2d.inverted_mask", "live2d.flip_texture")

        csmUpdateModel(self.model)

        # Render the model.

#         w = self.pixel_size.X
#         h = self.pixel_size.Y
        w = int(zoom * self.pixel_size.X)
        h = int(zoom * self.pixel_size.Y)

        ppu = self.pixels_per_unit * zoom

        if ppu:
            invppu = 1 / ppu
        else:
            invppu = 0

        offset = (w / 2.0 - ppu, h / 2.0 - ppu)

        reverse = Matrix([
            ppu, 0, 0, ppu,
            0, -ppu, 0, ppu,
            0, 0, 1, 0,
            0, 0, 0, 1, ])

        forward = Matrix([
            invppu, 0, 0, invppu,
            0, -invppu, 0, invppu,
            0, 0, 1, 0,
            0, 0, 0, 1, ])

        rv = Render(w, h)
        renders = [ ]
        raw_renders = [ ]

        for 0 <= i < self.drawable_count:

            mesh = Mesh2(TEXTURE_LAYOUT, self.drawable_vertex_counts[i], self.drawable_index_counts[i] // 3)

            mesh.points = self.drawable_vertex_counts[i]
            memcpy(mesh.point_data, self.drawable_vertex_positions[i], sizeof(float) * mesh.points * 2)
            memcpy(mesh.attribute, self.drawable_vertex_uvs[i], sizeof(float) * mesh.points * 2)

            mesh.triangles = self.drawable_index_counts[i] // 3
            memcpy(mesh.triangle, self.drawable_indices[i],  sizeof(unsigned short) * mesh.triangles * 3)
            r = Render(ppu * 2, ppu * 2)
            r.reverse = reverse
            r.forward = forward
            r.mesh = mesh

            for s in shaders:
                r.add_shader(s)

            r.blit(textures[self.drawable_texture_indices[i]], (0, 0))

            raw_renders.append(r)

            if self.drawable_dynamic_flags[i] & csmIsVisible:

                alpha = self.drawable_opacities[i]

                if alpha != 1.0:

                    ar = renpy.display.render.Render(r.width, r.height)
                    ar.blit(r, (0, 0))

                    ar.add_shader("renpy.alpha")
                    ar.add_uniform("u_renpy_alpha", alpha)
                    ar.add_uniform("u_renpy_over", 1.0)

                    r = ar

                renders.append((self.drawable_render_orders[i], r))


        multi_masks = { }

        for 0 <= i < self.drawable_count:

            if self.drawable_mask_counts[i] == 0:
                continue

            r = raw_renders[i]

            if self.drawable_mask_counts[i] == 1:
                m = raw_renders[self.drawable_masks[i][0]]
            else:

                key = [ ]

                for 0 <= j < self.drawable_mask_counts[i]:
                    key.append(self.drawable_masks[i][j])

                key = tuple(key)

                m = multi_masks.get(key, None)

                if m is None:
                    m = renpy.display.render.Render(ppu * 2, ppu * 2)

                    for j in key:
                        m.blit(raw_renders[j], (0, 0))

                    multi_masks[key] = m

            if self.drawable_constant_flags[i] & csmIsInvertedMask:

                shaders = inverted_mask_shaders
            else:
                shaders = mask_shaders

            for s in shaders:
                r.add_shader(s)

            r.blit(m, (0, 0))

        renders.sort()

        for t in renders:
            rv.subpixel_blit(t[1], offset)

        return rv
