# Copyright (c) 2025, Kitsunebi Games EMV.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from libc.stdint cimport intptr_t, uint32_t
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from libc.stdio cimport printf

from renpy.gl2.gl2mesh import TEXTURE_LAYOUT
from renpy.gl2.gl2mesh2 cimport Mesh2

from renpy.display.matrix cimport Matrix
from renpy.display.render cimport Render

from renpy.uguu.gl cimport GL_ZERO, GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_FUNC_ADD, GL_DST_COLOR, GL_DST_ALPHA

import renpy

cdef extern from "inochi2d_ldr.h" nogil:
    void* load_inochi2d_object(const char* sofile)
    void* load_inochi2d_function(void* handle, const char* name)

cdef extern from "inochi2d.h":

    # Opaque types.
    ctypedef struct in_puppet_t
    ctypedef struct in_texture_cache_t
    ctypedef struct in_parameter_t
    ctypedef struct in_resource_t
    ctypedef struct in_texture_t
    ctypedef struct in_drawlist_t

    # Enumerations.
    enum in_drawstate_t:
        IN_DRAW_STATE_NORMAL            = 0
        IN_DRAW_STATE_DEFINE_MASK       = 1
        IN_DRAW_STATE_MASKED_DRAW       = 2
        IN_DRAW_STATE_COMPOSITE_BEGIN   = 3
        IN_DRAW_STATE_COMPOSITE_END     = 4
        IN_DRAW_STATE_COMPOSITE_BLIT    = 5
    
    enum in_mask_mode_t:
        IN_MASK_MODE_MASK   = 0
        IN_MASK_MODE_DODGE  = 1

    enum in_blend_mode_t:
        IN_BLEND_MODE_NORMAL            = 0x00
        IN_BLEND_MODE_MULTIPLY          = 0x01
        IN_BLEND_MODE_SCREEN            = 0x02
        IN_BLEND_MODE_OVERLAY           = 0x03
        IN_BLEND_MODE_DARKEN            = 0x04
        IN_BLEND_MODE_LIGHTEN           = 0x05
        IN_BLEND_MODE_COLOR_DODGE       = 0x06
        IN_BLEND_MODE_LINEAR_DODGE      = 0x07
        IN_BLEND_MODE_ADD_GLOW          = 0x08
        IN_BLEND_MODE_COLOR_BURN        = 0x09
        IN_BLEND_MODE_HARD_LIGHT        = 0x0A
        IN_BLEND_MODE_SOFT_LIGHT        = 0x0B
        IN_BLEND_MODE_DIFFERENCE        = 0x0C
        IN_BLEND_MODE_EXCLUSION         = 0x0D
        IN_BLEND_MODE_SUBTRACT          = 0x0E
        IN_BLEND_MODE_INVERSE           = 0x0F
        IN_BLEND_MODE_DESTINATION_IN    = 0x10
        IN_BLEND_MODE_SOURCE_IN         = 0x11
        IN_BLEND_MODE_SOURCE_OUT        = 0x12

    ctypedef struct in_vec2_t:
        float x
        float y
    
    ctypedef struct in_vtx_t:
        float x
        float y
    
    ctypedef struct in_vtxdata_t:
        in_vtx_t vtx
        in_vec2_t uv
    
    ctypedef struct in_drawcmd_t:
        (in_texture_t *)[8] sources
        in_drawstate_t      state
        in_blend_mode_t     blendMode
        in_mask_mode_t      maskMode
        uint32_t            allocId
        uint32_t            vtxOffset
        uint32_t            idxOffset
        uint32_t            elemCount
        uint32_t            type_
        unsigned char[64]   vars_

    ctypedef struct in_drawalloc_t:
        uint32_t vtxOffset
        uint32_t idxOffset
        uint32_t idxCount
        uint32_t vtxCount
        uint32_t allocId

include "inochi2d.pxi"

cdef class Parameter:
    """
    Represents an Inochi2D Parameter, modifying the parameter
    animates it.
    """
    cdef str name
    cdef in_parameter_t *handle

    def get_name(self):
        """
        Gets the name of a parameter.
        """
        return self.name

    def get_active(self):
        """
        Gets whether the parameter is active.
        """
        return in_parameter_get_active(self.handle)

    def get_dimensions(self):
        """
        Gets the number of dimensions the parameter has.
        """
        return in_parameter_get_dimensions(self.handle)

    def get_min_value(self):
        """
        Gets the minimum values of the parameter.
        """
        return in_parameter_get_min_value(self.handle)

    def get_max_value(self):
        """
        Gets the maximum values of the parameter.
        """
        return in_parameter_get_max_value(self.handle)

    def get_value(self):
        """
        Gets the current values of the parameter.
        """
        return in_parameter_get_value(self.handle)

    def get_value_norm(self):
        """
        Gets the current normalized values of the parameter.
        """
        return in_parameter_get_normalized_value(self.handle)

    def set_value(self, in_vec2_t value):
        """
        Sets the current values of the parameter.
        """
        return in_parameter_set_value(self.handle, value)

    def set_value_norm(self, in_vec2_t value):
        """
        Sets the current normalized values of the parameter.
        """
        return in_parameter_set_normalized_value(self.handle, value)

    @staticmethod
    cdef Parameter from_ptr(in_parameter_t* handle):
        """
        Creates a new Inochi2D Parameter from its handle
        """
        cdef Parameter __self = Parameter.__new__(Parameter)
        __self.handle = handle
        __self.name = in_parameter_get_name(__self.handle).decode("utf-8")
        return __self


cdef class DrawList:
    """
    Represents an Inochi2D Draw List
    """
    cdef in_drawlist_t *handle
    
    @staticmethod
    cdef DrawList from_ptr(in_drawlist_t* handle):
        """
        Creates Inochi2D DrawList from its handle.
        """
        cdef DrawList __self = DrawList.__new__(DrawList)
        __self.handle = handle
        return __self

cdef class Inochi2DModel:
    cdef in_puppet_t *handle
    cdef public list parameters
    cdef public object drawlist

    cdef str name
    cdef object filename

    """
    Represents an Inochi2D Model
    """
    def __dealloc__(self):
        in_puppet_free(self.handle)

    def __init__(self, path):
        """
        Loads an Inochi2D Model from file.
        """
        self.filename = path
        with renpy.loader.load(path, directory="images") as f:
            data = f.read()
        
        self.handle = in_puppet_load_from_memory(<const uint8_t *>data, len(data))
        if self.handle is NULL:
            raise Exception(in_get_last_error())

        # Get Parameters
        cdef int i
        cdef in_parameter_t** params
        cdef uint32_t param_count
        params = in_puppet_get_parameters(self.handle, &param_count)
        for i in range(param_count):
            self.parameters.append(Parameter.from_ptr(params[i]))
        
        # Get DrawList
        self.drawlist = DrawList.from_ptr(in_puppet_get_drawlist(self.handle))
        self.name = in_puppet_get_name(self.handle).decode("utf-8")
        
    def get_name(self) -> str:
        """
        Gets the name of the puppet
        """
        return self.name
    
    def update(self, float delta):
        """
        Updates the model and refills its drawlist.
        """
        in_puppet_update(self.handle, delta)
        in_puppet_draw(self.handle, delta)
