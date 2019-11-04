# tegl.c  -*- coding: utf-8 -*-

# Copyright (c) 2008 Carl Banks
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Author nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

from __future__ import print_function

# Modified in 2010,2014 by PyTom to generate Cython code that uses glew.

VERSION = "0.1"

import os
import re

#-----------------------------------------------------------------------
# Options

# Module names (you can specify the same name to put gl and glu
# functions in the same module).

# Enable or disable extensions

OPENGL_1_2 = True
OPENGL_1_3 = True
OPENGL_1_4 = False
OPENGL_1_5 = False
OPENGL_2_0 = False
OPENGL_2_1 = False
GL_ARB_IMAGING = False
GL_ARB_MULTITEXTURE = True
GL_ARB_WINDOW_POS = False
GL_ARB_TRANSPOSE_MATRIX = False
GL_ARB_MULTISAMPLE = False
GL_ARB_TEXTURE_CUBE_MAP = False
GL_ARB_TEXTURE_COMPRESSION = False
GL_ARB_TEXTURE_BORDER_CLAMP = False
GL_ARB_POINT_PARAMETERS = False
GL_ARB_VERTEX_BLEND = False
GL_ARB_MATRIX_PALETTE = False
GL_ARB_TEXTURE_ENV_COMBINE = True
GL_ARB_TEXTURE_ENV_DOT3 = False
GL_ARB_TEXTURE_MIRRORED_REPEAT = False
GL_ARB_DEPTH_TEXTURE = False
GL_ARB_SHADOW = False
GL_ARB_SHADOW_AMBIENT = False
GL_ARB_VERTEX_PROGRAM = True
GL_ARB_FRAGMENT_PROGRAM = True
GL_ARB_VERTEX_BUFFER_OBJECT = True
GL_ARB_OCCLUSION_QUERY = False
GL_ARB_SHADER_OBJECTS = True
GL_ARB_VERTEX_SHADER = True
GL_ARB_FRAGMENT_SHADER = True
GL_ARB_SHADING_LANGUAGE_100 = True
GL_ARB_POINT_SPRITE = False
GL_ARB_DRAW_BUFFERS = False
GL_ARB_TEXTURE_RECTANGLE = False
GL_ARB_COLOR_BUFFER_FLOAT = False
GL_ARB_HALF_FLOAT_PIXEL = False
GL_ARB_TEXTURE_FLOAT = False
GL_ARB_PIXEL_BUFFER_OBJECT = False

GL_EXT_FRAMEBUFFER_OBJECT = True


#-----------------------------------------------------------------------
# generate tegl.c

def generate_tegl():

    # -------- GL Function Prototypes --------

    # Miscellaneous
    declare("ClearIndex", GLfloat)
    declare("ClearColor", GLclampf, GLclampf, GLclampf, GLclampf)
    declare("Clear", GLbitfield)
    declare("IndexMask", GLuint)
    declare("ColorMask", GLboolean, GLboolean, GLboolean, GLboolean)
    declare("AlphaFunc", GLenum, GLclampf)
    declare("BlendFunc", GLenum, GLenum)
    declare("LogicOp", GLenum)
    declare("CullFace", GLenum)
    declare("FrontFace", GLenum)
    declare("PointSize", GLfloat)
    declare("LineWidth", GLfloat)
    declare("LineStipple", GLint, GLushort)
    declare("PolygonMode", GLenum, GLenum)
    declare("PolygonOffset", GLfloat, GLfloat)
    declare("PolygonStipple", GLbuffer)
    declare("GetPolygonStipple", GLbuffer.asreturn())
    declare("EdgeFlag", GLboolean)
    declare("EdgeFlagv", GLboolean[1])
    declare("Scissor", GLint, GLint, GLsizei, GLsizei)
    declare("ClipPlane", GLenum, GLdouble[4])
    declare("GetClipPlane", GLenum, GLdouble[4].asreturn())
    declare("DrawBuffer", GLenum)
    declare("ReadBuffer", GLenum)
    declare("Enable", GLenum)
    declare("Disable", GLenum)
    declare(GLboolean, "IsEnabled", GLenum)
    declare("EnableClientState", GLenum)
    declare("DisableClientState", GLenum)
    declare("GetBooleanv", GLenum, GLboolean[4].asreturn())
    declare("GetDoublev", GLenum, GLdouble[4].asreturn())
    declare("GetFloatv", GLenum, GLfloat[4].asreturn())
    declare("GetIntegerv", GLenum, GLint[4].asreturn())
    declare("PushAttrib", GLbitfield)
    declare("PopAttrib")
    declare("PushClientAttrib", GLbitfield)
    declare("PopClientAttrib")
    declare(GLint, "RenderMode", GLenum)
    declare(GLenum, "GetError")
    declare(GLstring, "GetString", GLenum)
    declare("Finish")
    declare("Flush")
    declare("Hint", GLenum, GLenum)

    # Depth Buffer
    declare("ClearDepth", GLclampd)
    declare("DepthFunc", GLenum)
    declare("DepthMask", GLboolean)
    declare("DepthRange", GLclampd, GLclampd)

    # Accumulation Buffer
    declare("ClearAccum", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("Accum", GLenum, GLfloat)

    # Transformation
    declare("MatrixMode", GLenum)
    declare("Ortho", GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Frustum", GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Viewport", GLint, GLint, GLsizei, GLsizei)
    declare("PushMatrix")
    declare("PopMatrix")
    declare("LoadIdentity")
    declare("LoadMatrixd", GLdouble[16])
    declare("LoadMatrixf", GLfloat[16])
    declare("MultMatrixd", GLdouble[16])
    declare("MultMatrixf", GLfloat[16])
    declare("Rotated", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Rotatef", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("Scaled", GLdouble, GLdouble, GLdouble)
    declare("Scalef", GLfloat, GLfloat, GLfloat)
    declare("Translated", GLdouble, GLdouble, GLdouble)
    declare("Translatef", GLfloat, GLfloat, GLfloat)

    # Display Lists
    declare(GLboolean, "IsList", GLuint)
    declare("DeleteLists", GLuint, GLsizei)
    declare(GLuint, "GenLists", GLsizei)
    declare("NewList", GLuint, GLenum)
    declare("EndList")
    declare("CallList", GLuint)
    declare("CallLists", GLsizei, GLenum, GLbuffer)
    declare("ListBase", GLuint)

    # Drawing Functions
    declare("Begin", GLenum)
    declare("End")
    declare("Vertex2d", GLdouble, GLdouble)
    declare("Vertex2f", GLfloat, GLfloat)
    declare("Vertex2i", GLint, GLint)
    declare("Vertex2s", GLshort, GLshort)
    declare("Vertex3d", GLdouble, GLdouble, GLdouble)
    declare("Vertex3f", GLfloat, GLfloat, GLfloat)
    declare("Vertex3i", GLint, GLint, GLint)
    declare("Vertex3s", GLshort, GLshort, GLshort)
    declare("Vertex4d", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Vertex4f", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("Vertex4i", GLint, GLint, GLint, GLint)
    declare("Vertex4s", GLshort, GLshort, GLshort, GLshort)
    declare("Vertex2dv", GLdouble[2])
    declare("Vertex2fv", GLfloat[2])
    declare("Vertex2iv", GLint[2])
    declare("Vertex2sv", GLshort[2])
    declare("Vertex3dv", GLdouble[3])
    declare("Vertex3fv", GLfloat[3])
    declare("Vertex3iv", GLint[3])
    declare("Vertex3sv", GLshort[3])
    declare("Vertex4dv", GLdouble[4])
    declare("Vertex4fv", GLfloat[4])
    declare("Vertex4iv", GLint[4])
    declare("Vertex4sv", GLshort[4])
    declare("Normal3b", GLbyte, GLbyte, GLbyte)
    declare("Normal3d", GLdouble, GLdouble, GLdouble)
    declare("Normal3f", GLfloat, GLfloat, GLfloat)
    declare("Normal3i", GLint, GLint, GLint)
    declare("Normal3s", GLshort, GLshort, GLshort)
    declare("Normal3bv", GLbyte[3])
    declare("Normal3dv", GLdouble[3])
    declare("Normal3fv", GLfloat[3])
    declare("Normal3iv", GLint[3])
    declare("Normal3sv", GLshort[3])
    declare("Indexd", GLdouble)
    declare("Indexf", GLfloat)
    declare("Indexi", GLint)
    declare("Indexs", GLshort)
    declare("Indexub", GLubyte)
    declare("Indexdv", GLdouble[1])
    declare("Indexfv", GLfloat[1])
    declare("Indexiv", GLint[1])
    declare("Indexsv", GLshort[1])
    declare("Indexubv", GLubyte[1])
    declare("Color3b", GLbyte, GLbyte, GLbyte)
    declare("Color3d", GLdouble, GLdouble, GLdouble)
    declare("Color3f", GLfloat, GLfloat, GLfloat)
    declare("Color3i", GLint, GLint, GLint)
    declare("Color3s", GLshort, GLshort, GLshort)
    declare("Color3ub", GLubyte, GLubyte, GLubyte)
    declare("Color3ui", GLuint, GLuint, GLuint)
    declare("Color3us", GLushort, GLushort, GLushort)
    declare("Color4b", GLbyte, GLbyte, GLbyte, GLbyte)
    declare("Color4d", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Color4f", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("Color4i", GLint, GLint, GLint, GLint)
    declare("Color4s", GLshort, GLshort, GLshort, GLshort)
    declare("Color4ub", GLubyte, GLubyte, GLubyte, GLubyte)
    declare("Color4ui", GLuint, GLuint, GLuint, GLuint)
    declare("Color4us", GLushort, GLushort, GLushort, GLushort)
    declare("Color3bv", GLbyte[3])
    declare("Color3dv", GLdouble[3])
    declare("Color3fv", GLfloat[3])
    declare("Color3iv", GLint[3])
    declare("Color3sv", GLshort[3])
    declare("Color3ubv", GLubyte[3])
    declare("Color3uiv", GLuint[3])
    declare("Color3usv", GLushort[3])
    declare("Color4bv", GLbyte[4])
    declare("Color4dv", GLdouble[4])
    declare("Color4fv", GLfloat[4])
    declare("Color4iv", GLint[4])
    declare("Color4sv", GLshort[4])
    declare("Color4ubv", GLubyte[4])
    declare("Color4uiv", GLuint[4])
    declare("Color4usv", GLushort[4])
    declare("TexCoord1d", GLdouble)
    declare("TexCoord1f", GLfloat)
    declare("TexCoord1i", GLint)
    declare("TexCoord1s", GLshort)
    declare("TexCoord2d", GLdouble, GLdouble)
    declare("TexCoord2f", GLfloat, GLfloat)
    declare("TexCoord2i", GLint, GLint)
    declare("TexCoord2s", GLshort, GLshort)
    declare("TexCoord3d", GLdouble, GLdouble, GLdouble)
    declare("TexCoord3f", GLfloat, GLfloat, GLfloat)
    declare("TexCoord3i", GLint, GLint, GLint)
    declare("TexCoord3s", GLshort, GLshort, GLshort)
    declare("TexCoord4d", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("TexCoord4f", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("TexCoord4i", GLint, GLint, GLint, GLint)
    declare("TexCoord4s", GLshort, GLshort, GLshort, GLshort)
    declare("TexCoord1dv", GLdouble[1])
    declare("TexCoord1fv", GLfloat[1])
    declare("TexCoord1iv", GLint[1])
    declare("TexCoord1sv", GLshort[1])
    declare("TexCoord2dv", GLdouble[2])
    declare("TexCoord2fv", GLfloat[2])
    declare("TexCoord2iv", GLint[2])
    declare("TexCoord2sv", GLshort[2])
    declare("TexCoord3dv", GLdouble[3])
    declare("TexCoord3fv", GLfloat[3])
    declare("TexCoord3iv", GLint[3])
    declare("TexCoord3sv", GLshort[3])
    declare("TexCoord4dv", GLdouble[4])
    declare("TexCoord4fv", GLfloat[4])
    declare("TexCoord4iv", GLint[4])
    declare("TexCoord4sv", GLshort[4])
    declare("RasterPos2d", GLdouble, GLdouble)
    declare("RasterPos2f", GLfloat, GLfloat)
    declare("RasterPos2i", GLint, GLint)
    declare("RasterPos2s", GLshort, GLshort)
    declare("RasterPos3d", GLdouble, GLdouble, GLdouble)
    declare("RasterPos3f", GLfloat, GLfloat, GLfloat)
    declare("RasterPos3i", GLint, GLint, GLint)
    declare("RasterPos3s", GLshort, GLshort, GLshort)
    declare("RasterPos4d", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("RasterPos4f", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("RasterPos4i", GLint, GLint, GLint, GLint)
    declare("RasterPos4s", GLshort, GLshort, GLshort, GLshort)
    declare("RasterPos2dv", GLdouble[2])
    declare("RasterPos2fv", GLfloat[2])
    declare("RasterPos2iv", GLint[2])
    declare("RasterPos2sv", GLshort[2])
    declare("RasterPos3dv", GLdouble[3])
    declare("RasterPos3fv", GLfloat[3])
    declare("RasterPos3iv", GLint[3])
    declare("RasterPos3sv", GLshort[3])
    declare("RasterPos4dv", GLdouble[4])
    declare("RasterPos4fv", GLfloat[4])
    declare("RasterPos4iv", GLint[4])
    declare("RasterPos4sv", GLshort[4])
    declare("Rectd", GLdouble, GLdouble, GLdouble, GLdouble)
    declare("Rectf", GLfloat, GLfloat, GLfloat, GLfloat)
    declare("Recti", GLint, GLint, GLint, GLint)
    declare("Rects", GLshort, GLshort, GLshort, GLshort)
    declare("Rectdv", GLdouble[2], GLdouble[2])
    declare("Rectfv", GLfloat[2], GLfloat[2])
    declare("Rectiv", GLint[2], GLint[2])
    declare("Rectsv", GLshort[2], GLshort[2])

    # Vertex Arrays
    declare("VertexPointer", GLint, GLenum, GLsizei, GLbuffer)
    declare("NormalPointer", GLenum, GLsizei, GLbuffer)
    declare("ColorPointer", GLint, GLenum, GLsizei, GLbuffer)
    declare("IndexPointer", GLenum, GLsizei, GLbuffer)
    declare("TexCoordPointer", GLint, GLenum, GLsizei, GLbuffer)
    declare("EdgeFlagPointer", GLsizei, GLbuffer)
    #declare("GetPointerv",GLenum,GLvoid **params)
    declare("ArrayElement", GLint)
    declare("DrawArrays", GLenum, GLint, GLsizei)
    declare("DrawElements", GLenum, GLsizei, GLenum, GLbuffer)
    declare("InterleavedArrays", GLenum, GLsizei, GLbuffer)

    # Lighting
    declare("ShadeModel", GLenum)
    declare("Lightf", GLenum, GLenum, GLfloat)
    declare("Lighti", GLenum, GLenum, GLint)
    declare("Lightfv", GLenum, GLenum, GLfloat[4])
    declare("Lightiv", GLenum, GLenum, GLint[4])
    declare("GetLightfv", GLenum, GLenum, GLfloat[4].asreturn())
    declare("GetLightiv", GLenum, GLenum, GLint[4].asreturn())
    declare("LightModelf", GLenum, GLfloat)
    declare("LightModeli", GLenum, GLint)
    declare("LightModelfv", GLenum, GLfloat[4])
    declare("LightModeliv", GLenum, GLint[4])
    declare("Materialf", GLenum, GLenum, GLfloat)
    declare("Materiali", GLenum, GLenum, GLint)
    declare("Materialfv", GLenum, GLenum, GLfloat[4])
    declare("Materialiv", GLenum, GLenum, GLint[4])
    declare("GetMaterialfv", GLenum, GLenum, GLfloat[4].asreturn())
    declare("GetMaterialiv", GLenum, GLenum, GLint[4].asreturn())
    declare("ColorMaterial", GLenum, GLenum)

    # Raster functions
    declare("PixelZoom", GLfloat, GLfloat)
    declare("PixelStoref", GLenum, GLfloat)
    declare("PixelStorei", GLenum, GLint)
    declare("PixelTransferf", GLenum, GLfloat)
    declare("PixelTransferi", GLenum, GLint)
    declare("PixelMapfv", GLenum, GLsizei, GLbuffer)
    declare("PixelMapuiv", GLenum, GLsizei, GLbuffer)
    declare("PixelMapusv", GLenum, GLsizei, GLbuffer)
    declare("GetPixelMapfv", GLenum, GLbuffer.asreturn())
    declare("GetPixelMapuiv", GLenum, GLbuffer.asreturn())
    declare("GetPixelMapusv", GLenum, GLbuffer.asreturn())
    declare("Bitmap", GLsizei, GLsizei, GLfloat, GLfloat, GLfloat, GLfloat, GLbuffer)
    declare("ReadPixels", GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLbuffer.asreturn())
    declare("DrawPixels", GLsizei, GLsizei, GLenum, GLenum, GLbuffer)
    declare("CopyPixels", GLint, GLint, GLsizei, GLsizei, GLenum)

    # Stenciling
    declare("StencilFunc", GLenum, GLint, GLuint)
    declare("StencilMask", GLuint)
    declare("StencilOp", GLenum, GLenum, GLenum)
    declare("ClearStencil", GLint)

    # Texture mapping
    declare("TexGend", GLenum, GLenum, GLdouble)
    declare("TexGenf", GLenum, GLenum, GLfloat)
    declare("TexGeni", GLenum, GLenum, GLint)
    declare("TexGendv", GLenum, GLenum, GLdouble[4])
    declare("TexGenfv", GLenum, GLenum, GLfloat[4])
    declare("TexGeniv", GLenum, GLenum, GLint[4])
    declare("GetTexGendv", GLenum, GLenum, GLdouble[4].asreturn())
    declare("GetTexGenfv", GLenum, GLenum, GLfloat[4].asreturn())
    declare("GetTexGeniv", GLenum, GLenum, GLint[4].asreturn())
    declare("TexEnvf", GLenum, GLenum, GLfloat)
    declare("TexEnvi", GLenum, GLenum, GLint)
    declare("TexEnvfv", GLenum, GLenum, GLfloat[4])
    declare("TexEnviv", GLenum, GLenum, GLint[4])
    declare("GetTexEnvfv", GLenum, GLenum, GLfloat[4].asreturn())
    declare("GetTexEnviv", GLenum, GLenum, GLint[4].asreturn())
    declare("TexParameterf", GLenum, GLenum, GLfloat)
    declare("TexParameteri", GLenum, GLenum, GLint)
    declare("TexParameterfv", GLenum, GLenum, GLfloat[4])
    declare("TexParameteriv", GLenum, GLenum, GLint[4])
    declare("GetTexParameterfv", GLenum, GLenum, GLfloat[4].asreturn())
    declare("GetTexParameteriv", GLenum, GLenum, GLint[4].asreturn())
    declare("GetTexLevelParameterfv", GLenum, GLint, GLenum, GLfloat[4].asreturn())
    declare("GetTexLevelParameteriv", GLenum, GLint, GLenum, GLint[4].asreturn())
    declare("TexImage1D", GLenum, GLint, GLint, GLsizei, GLint, GLenum, GLenum, GLbuffer)
    declare("TexImage2D", GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, GLbuffer)
    declare("GetTexImage", GLenum, GLint, GLenum, GLenum, GLbuffer.asreturn())
    declare("BindTexture", GLenum, GLuint)
    declare(GLboolean, "IsTexture", GLuint)
    declare("TexSubImage1D", GLenum, GLint, GLint, GLsizei, GLenum, GLenum, GLbuffer)
    declare("TexSubImage2D", GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLbuffer)
    declare("CopyTexImage1D", GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLint)
    declare("CopyTexImage2D", GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLsizei, GLint)
    declare("CopyTexSubImage1D", GLenum, GLint, GLint, GLint, GLint, GLsizei)
    declare("CopyTexSubImage2D", GLenum, GLint, GLint, GLint, GLint, GLint, GLsizei, GLsizei)
    declare("GenTextures", GLsizei, GLuint[1].asreturn())  ### not a dynamic size
    declare("DeleteTextures", GLsizei, GLuint[1])  ### not a dynamic size
    declare("PrioritizeTextures", GLsizei, GLuint[1],
            GLclampf[1])  ### not a dynamic size
    declare(GLboolean, "AreTexturesResident", GLsizei, GLuint[1],
            GLboolean[1].asreturn())
    ### not a dynamic size

    # Evaluators
    declare("Map1d", GLenum, GLdouble, GLdouble, GLint, GLint, GLbuffer)
    declare("Map1f", GLenum, GLfloat, GLfloat, GLint, GLint, GLbuffer)
    declare("Map2d", GLenum, GLdouble, GLdouble, GLint, GLint, GLdouble, GLdouble, GLint, GLint, GLbuffer)
    declare("Map2f", GLenum, GLfloat, GLfloat, GLint, GLint, GLfloat, GLfloat, GLint, GLint, GLbuffer)
    declare("GetMapdv", GLenum, GLenum, GLbuffer.asreturn())
    declare("GetMapfv", GLenum, GLenum, GLbuffer.asreturn())
    declare("GetMapiv", GLenum, GLenum, GLbuffer.asreturn())
    declare("EvalCoord1d", GLdouble)
    declare("EvalCoord1f", GLfloat)
    declare("EvalCoord1dv", GLdouble[1])
    declare("EvalCoord1fv", GLfloat[1])
    declare("EvalCoord2d", GLdouble, GLdouble)
    declare("EvalCoord2f", GLfloat, GLfloat)
    declare("EvalCoord2dv", GLdouble[2])
    declare("EvalCoord2fv", GLfloat[2])
    declare("MapGrid1d", GLint, GLdouble, GLdouble)
    declare("MapGrid1f", GLint, GLfloat, GLfloat)
    declare("MapGrid2d", GLint, GLdouble, GLdouble, GLint, GLdouble, GLdouble)
    declare("MapGrid2f", GLint, GLfloat, GLfloat, GLint, GLfloat, GLfloat)
    declare("EvalPoint1", GLint)
    declare("EvalPoint2", GLint, GLint)
    declare("EvalMesh1", GLenum, GLint, GLint)
    declare("EvalMesh2", GLenum, GLint, GLint, GLint, GLint)

    # Fog
    declare("Fogf", GLenum, GLfloat)
    declare("Fogi", GLenum, GLint)
    declare("Fogfv", GLenum, GLfloat[4])
    declare("Fogiv", GLenum, GLint[4])

    # Selection and Feedback
    declare("FeedbackBuffer", GLsizei, GLenum, GLbuffer.asreturn())
    declare("PassThrough", GLfloat)
    declare("SelectBuffer", GLsizei, GLbuffer.asreturn())
    declare("InitNames")
    declare("LoadName", GLuint)
    declare("PushName", GLuint)
    declare("PopName")

    if OPENGL_1_2:
        declare("DrawRangeElements", GLenum, GLuint,
                GLuint, GLsizei, GLenum, GLbuffer)
        declare("TexImage3D", GLenum, GLint, GLint, GLsizei, GLsizei, GLsizei, GLint,
                GLenum, GLenum, GLbuffer)
        declare("TexSubImage3D", GLenum, GLint, GLint, GLint, GLint, GLsizei,
                GLsizei, GLsizei, GLenum, GLenum, GLbuffer)
        declare("CopyTexSubImage3D", GLenum, GLint, GLint, GLint, GLint, GLint,
                GLint, GLsizei, GLsizei)

    if GL_ARB_IMAGING:
        declare("ColorTable", GLenum, GLenum, GLsizei, GLenum, GLenum, GLbuffer)
        declare("ColorSubTable", GLenum, GLsizei, GLsizei, GLenum, GLenum, GLbuffer)
        declare("ColorTableParameteriv", GLenum, GLenum, GLint[4])
        declare("ColorTableParameterfv", GLenum, GLenum, GLfloat[4])
        declare("CopyColorSubTable", GLenum, GLsizei, GLint, GLint, GLsizei)
        declare("CopyColorTable", GLenum, GLenum, GLint, GLint, GLsizei)
        declare("GetColorTable", GLenum, GLenum, GLenum, GLbuffer.asreturn())
        declare("GetColorTableParameterfv", GLenum, GLenum, GLfloat[4].asreturn())
        declare("GetColorTableParameteriv", GLenum, GLenum, GLint[4].asreturn())
        declare("BlendEquation", GLenum)
        declare("BlendColor", GLclampf, GLclampf, GLclampf, GLclampf)
        declare("Histogram", GLenum, GLsizei, GLenum, GLboolean)
        declare("ResetHistogram", GLenum)
        declare("GetHistogram", GLenum, GLboolean, GLenum, GLenum, GLbuffer.asreturn())
        declare("GetHistogramParameterfv", GLenum, GLenum, GLfloat[1].asreturn())
        declare("GetHistogramParameteriv", GLenum, GLenum, GLint[1].asreturn())
        declare("Minmax", GLenum, GLenum, GLboolean)
        declare("ResetMinmax", GLenum)
        declare("GetMinmax", GLenum, GLboolean, GLenum, GLenum, GLbuffer.asreturn())
        declare("GetMinmaxParameterfv", GLenum, GLenum, GLfloat[1].asreturn())
        declare("GetMinmaxParameteriv", GLenum, GLenum, GLint[1].asreturn())
        declare("ConvolutionFilter1D", GLenum, GLenum, GLsizei, GLenum, GLenum, GLbuffer)
        declare("ConvolutionFilter2D", GLenum, GLenum, GLsizei, GLsizei, GLenum, GLenum, GLbuffer)
        declare("ConvolutionParameterf", GLenum, GLenum, GLfloat)
        declare("ConvolutionParameterfv", GLenum, GLenum, GLfloat[4])
        declare("ConvolutionParameteri", GLenum, GLenum, GLint)
        declare("ConvolutionParameteriv", GLenum, GLenum, GLint[4])
        declare("CopyConvolutionFilter1D", GLenum, GLenum, GLint, GLint, GLsizei)
        declare("CopyConvolutionFilter2D", GLenum, GLenum, GLint, GLint, GLsizei, GLsizei)
        declare("GetConvolutionFilter", GLenum, GLenum, GLenum, GLbuffer.asreturn())
        declare("GetConvolutionParameterfv", GLenum, GLenum, GLfloat[4].asreturn())
        declare("GetConvolutionParameteriv", GLenum, GLenum, GLint[4].asreturn())
        declare("SeparableFilter2D", GLenum, GLenum, GLsizei, GLsizei, GLenum, GLenum, GLbuffer, GLbuffer)
        declare("GetSeparableFilter", GLenum, GLenum, GLenum, GLbuffer.asreturn(), GLbuffer.asreturn(),
                GLbuffer.asreturn())

    if OPENGL_1_3:
        declare("ActiveTexture", GLenum)
        declare("ClientActiveTexture", GLenum)
        declare("CompressedTexImage1D", GLenum, GLint, GLenum, GLsizei, GLint, GLsizei, GLbuffer)
        declare("CompressedTexImage2D", GLenum, GLint, GLenum, GLsizei, GLsizei, GLint, GLsizei, GLbuffer)
        declare("CompressedTexImage3D", GLenum, GLint, GLenum, GLsizei, GLsizei, GLsizei, GLint,
                GLsizei, GLbuffer)
        declare("CompressedTexSubImage1D", GLenum, GLint, GLint, GLsizei, GLenum, GLsizei, GLbuffer)
        declare("CompressedTexSubImage2D", GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum,
                GLsizei, GLbuffer)
        declare("CompressedTexSubImage3D", GLenum, GLint, GLint, GLint, GLint, GLsizei, GLsizei,
                GLsizei, GLenum, GLsizei, GLbuffer)
        declare("GetCompressedTexImage", GLenum, GLint, GLbuffer.asreturn())
        declare("MultiTexCoord1d", GLenum, GLdouble)
        declare("MultiTexCoord1dv", GLenum, GLdouble[1])
        declare("MultiTexCoord1f", GLenum, GLfloat)
        declare("MultiTexCoord1fv", GLenum, GLfloat[1])
        declare("MultiTexCoord1i", GLenum, GLint)
        declare("MultiTexCoord1iv", GLenum, GLint[1])
        declare("MultiTexCoord1s", GLenum, GLshort)
        declare("MultiTexCoord1sv", GLenum, GLshort[1])
        declare("MultiTexCoord2d", GLenum, GLdouble, GLdouble)
        declare("MultiTexCoord2dv", GLenum, GLdouble[2])
        declare("MultiTexCoord2f", GLenum, GLfloat, GLfloat)
        declare("MultiTexCoord2fv", GLenum, GLfloat[2])
        declare("MultiTexCoord2i", GLenum, GLint, GLint)
        declare("MultiTexCoord2iv", GLenum, GLint[2])
        declare("MultiTexCoord2s", GLenum, GLshort, GLshort)
        declare("MultiTexCoord2sv", GLenum, GLshort[2])
        declare("MultiTexCoord3d", GLenum, GLdouble, GLdouble, GLdouble)
        declare("MultiTexCoord3dv", GLenum, GLdouble[3])
        declare("MultiTexCoord3f", GLenum, GLfloat, GLfloat, GLfloat)
        declare("MultiTexCoord3fv", GLenum, GLfloat[3])
        declare("MultiTexCoord3i", GLenum, GLint, GLint, GLint)
        declare("MultiTexCoord3iv", GLenum, GLint[3])
        declare("MultiTexCoord3s", GLenum, GLshort, GLshort, GLshort)
        declare("MultiTexCoord3sv", GLenum, GLshort[3])
        declare("MultiTexCoord4d", GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("MultiTexCoord4dv", GLenum, GLdouble[4])
        declare("MultiTexCoord4f", GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("MultiTexCoord4fv", GLenum, GLfloat[4])
        declare("MultiTexCoord4i", GLenum, GLint, GLint, GLint, GLint)
        declare("MultiTexCoord4iv", GLenum, GLint[4])
        declare("MultiTexCoord4s", GLenum, GLshort, GLshort, GLshort, GLshort)
        declare("MultiTexCoord4sv", GLenum, GLshort[4])
        declare("LoadTransposeMatrixd", GLdouble[16])
        declare("LoadTransposeMatrixf", GLfloat[16])
        declare("MultTransposeMatrixd", GLdouble[16])
        declare("MultTransposeMatrixf", GLfloat[16])
        declare("SampleCoverage", GLclampf, GLboolean)

    if GL_ARB_MULTITEXTURE:
        declare("ActiveTextureARB", GLenum)
        declare("ClientActiveTextureARB", GLenum)
        declare("MultiTexCoord1dARB", GLenum, GLdouble)
        declare("MultiTexCoord1dvARB", GLenum, GLdouble[1])
        declare("MultiTexCoord1fARB", GLenum, GLfloat)
        declare("MultiTexCoord1fvARB", GLenum, GLfloat[1])
        declare("MultiTexCoord1iARB", GLenum, GLint)
        declare("MultiTexCoord1ivARB", GLenum, GLint[1])
        declare("MultiTexCoord1sARB", GLenum, GLshort)
        declare("MultiTexCoord1svARB", GLenum, GLshort[1])
        declare("MultiTexCoord2dARB", GLenum, GLdouble, GLdouble)
        declare("MultiTexCoord2dvARB", GLenum, GLdouble[2])
        declare("MultiTexCoord2fARB", GLenum, GLfloat, GLfloat)
        declare("MultiTexCoord2fvARB", GLenum, GLfloat[2])
        declare("MultiTexCoord2iARB", GLenum, GLint, GLint)
        declare("MultiTexCoord2ivARB", GLenum, GLint[2])
        declare("MultiTexCoord2sARB", GLenum, GLshort, GLshort)
        declare("MultiTexCoord2svARB", GLenum, GLshort[2])
        declare("MultiTexCoord3dARB", GLenum, GLdouble, GLdouble, GLdouble)
        declare("MultiTexCoord3dvARB", GLenum, GLdouble[3])
        declare("MultiTexCoord3fARB", GLenum, GLfloat, GLfloat, GLfloat)
        declare("MultiTexCoord3fvARB", GLenum, GLfloat[3])
        declare("MultiTexCoord3iARB", GLenum, GLint, GLint, GLint)
        declare("MultiTexCoord3ivARB", GLenum, GLint[3])
        declare("MultiTexCoord3sARB", GLenum, GLshort, GLshort, GLshort)
        declare("MultiTexCoord3svARB", GLenum, GLshort[3])
        declare("MultiTexCoord4dARB", GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("MultiTexCoord4dvARB", GLenum, GLdouble[4])
        declare("MultiTexCoord4fARB", GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("MultiTexCoord4fvARB", GLenum, GLfloat[4])
        declare("MultiTexCoord4iARB", GLenum, GLint, GLint, GLint, GLint)
        declare("MultiTexCoord4ivARB", GLenum, GLint[4])
        declare("MultiTexCoord4sARB", GLenum, GLshort, GLshort, GLshort, GLshort)
        declare("MultiTexCoord4svARB", GLenum, GLshort[4])

    if OPENGL_1_4:
        declare("BlendFuncSeparate", GLenum, GLenum, GLenum, GLenum)
        declare("FogCoordf", GLfloat)
        declare("FogCoordfv", GLfloat[4])
        declare("FogCoordd", GLdouble)
        declare("FogCoorddv", GLdouble[4])
        declare("FogCoordPointer", GLenum, GLsizei, GLbuffer)
        #declare("MultiDrawArrays",GLenum,GLbuffer,GLbuffer,GLsizei)
        #declare("MultiDrawElements",GLenum,GLsizei[],GLenum, const GLvoid**,GLsizei)
        declare("PointParameterf", GLenum, GLfloat)
        declare("PointParameterfv", GLenum, GLfloat[1])
        declare("PointParameteri", GLenum, GLint)
        declare("PointParameteriv", GLenum, GLint[1])
        declare("SecondaryColor3b", GLbyte, GLbyte, GLbyte)
        declare("SecondaryColor3bv", GLbyte[3])
        declare("SecondaryColor3d", GLdouble, GLdouble, GLdouble)
        declare("SecondaryColor3dv", GLdouble[3])
        declare("SecondaryColor3f", GLfloat, GLfloat, GLfloat)
        declare("SecondaryColor3fv", GLfloat[3])
        declare("SecondaryColor3i", GLint, GLint, GLint)
        declare("SecondaryColor3iv", GLint[3])
        declare("SecondaryColor3s", GLshort, GLshort, GLshort)
        declare("SecondaryColor3sv", GLshort[3])
        declare("SecondaryColor3ub", GLubyte, GLubyte, GLubyte)
        declare("SecondaryColor3ubv", GLubyte[3])
        declare("SecondaryColor3ui", GLuint, GLuint, GLuint)
        declare("SecondaryColor3uiv", GLuint[3])
        declare("SecondaryColor3us", GLushort, GLushort, GLushort)
        declare("SecondaryColor3usv", GLushort[3])
        declare("SecondaryColorPointer", GLint, GLenum, GLsizei, GLbuffer)
        declare("WindowPos2d", GLdouble, GLdouble)
        declare("WindowPos2dv", GLdouble[2])
        declare("WindowPos2f", GLfloat, GLfloat)
        declare("WindowPos2fv", GLfloat[2])
        declare("WindowPos2i", GLint, GLint)
        declare("WindowPos2iv", GLint[2])
        declare("WindowPos2s", GLshort, GLshort)
        declare("WindowPos2sv", GLshort[2])
        declare("WindowPos3d", GLdouble, GLdouble, GLdouble)
        declare("WindowPos3dv", GLdouble[3])
        declare("WindowPos3f", GLfloat, GLfloat, GLfloat)
        declare("WindowPos3fv", GLfloat[3])
        declare("WindowPos3i", GLint, GLint, GLint)
        declare("WindowPos3iv", GLint[3])
        declare("WindowPos3s", GLshort, GLshort, GLshort)
        declare("WindowPos3sv", GLshort[3])

    if OPENGL_1_5:
        # declare("GenQueries",GLsizei,GLuint[MAX_QUERY_ARRAY_SIZE].asreturn())  ### not a dynamic size
        # declare("DeleteQueries",GLsizei,GLuint[MAX_QUERY_ARRAY_SIZE])  ### not a dynamic size
        declare(GLboolean, "IsQuery", GLuint)
        declare("BeginQuery", GLenum, GLuint)
        declare("EndQuery", GLenum)
        declare("GetQueryiv", GLenum, GLenum, GLint[1].asreturn())
        declare("GetQueryObjectiv", GLuint, GLenum, GLint[1].asreturn())
        declare("GetQueryObjectuiv", GLuint, GLenum, GLuint[1].asreturn())
        declare("BindBuffer", GLenum, GLuint)
        # declare("DeleteBuffers",GLsizei,GLuint[MAX_BUFFER_ARRAY_SIZE])  ### not a dynamic size
        # declare("GenBuffers",GLsizei,GLuint[MAX_BUFFER_ARRAY_SIZE].asreturn())  ### not a dynamic size
        declare(GLboolean, "IsBuffer", GLuint)
        #declare("BufferData",GLenum,GLsizeiptr,GLbuffer,GLenum)
        #declare("BufferSubData",GLenum,GLintptr,GLsizeiptr,GLbuffer)
        #declare("GetBufferSubData",GLenum,GLintptr,GLsizeiptr,GLbuffer.asreturn())
        declare(GLpointer, "MapBuffer", GLenum, GLenum)
        declare(GLboolean, "UnmapBuffer", GLenum)
        declare("GetBufferParameteriv", GLenum, GLenum, GLint[1].asreturn())
        #declare("GetBufferPointerv",GLenum,GLenum,GLvoid**)

    if OPENGL_2_0:
        declare("BlendEquationSeparate", GLenum, GLenum)
        declare("DrawBuffers", GLsizei, GLenum[16])  ### not a dynamic size
        declare("StencilOpSeparate", GLenum, GLenum, GLenum, GLenum)
        declare("StencilFuncSeparate", GLenum, GLenum, GLint, GLuint)
        declare("StencilMaskSeparate", GLenum, GLuint)
        declare("AttachShader", GLuint, GLuint)
        declare("BindAttribLocation", GLuint, GLuint, GLstring)
        declare("CompileShader", GLuint)
        declare(GLuint, "CreateProgram")
        declare(GLuint, "CreateShader", GLenum)
        declare("DeleteProgram", GLuint)
        declare("DeleteShader", GLuint)
        declare("DetachShader", GLuint, GLuint)
        declare("DisableVertexAttribArray", GLuint)
        declare("EnableVertexAttribArray", GLuint)
        declare("GetActiveAttrib", GLuint, GLuint, GLsizei, GLsizei[1].asreturn(),
                GLint[1].asreturn(), GLenum[1].asreturn(), GLstring.asreturn())
        declare("GetActiveUniform", GLuint, GLuint, GLsizei, GLsizei[1].asreturn(),
                GLint[1].asreturn(), GLenum[1].asreturn(), GLstring.asreturn())
        declare("GetAttachedShaders", GLuint, GLsizei, GLsizei[1].asreturn(),
                GLbuffer.asreturn())
        declare(GLint, "GetAttribLocation", GLuint, GLstring)
        declare("GetProgramiv", GLuint, GLenum, GLint[1].asreturn())
        declare("GetProgramInfoLog", GLuint, GLsizei, GLsizei[1].asreturn(),
                GLstring.asreturn())
        declare("GetShaderiv", GLuint, GLenum, GLint[1].asreturn())
        declare("GetShaderInfoLog", GLuint, GLsizei, GLsizei[1].asreturn(),
                GLstring.asreturn())
        declare("GetShaderSource", GLuint, GLsizei, GLsizei[1].asreturn(),
                GLstring.asreturn())
        declare(GLint, "GetUniformLocation", GLuint, GLstring)
        declare("GetUniformfv", GLuint, GLint, GLfloat[16].asreturn())
        declare("GetUniformiv", GLuint, GLint, GLint[16].asreturn())
        declare("GetVertexAttribdv", GLuint, GLenum, GLdouble[1].asreturn())
        declare("GetVertexAttribfv", GLuint, GLenum, GLfloat[1].asreturn())
        declare("GetVertexAttribiv", GLuint, GLenum, GLint[1].asreturn())
        #declare("GetVertexAttribPointerv",GLuint,GLenum, GLvoid**)
        declare(GLboolean, "IsProgram", GLuint)
        declare(GLboolean, "IsShader", GLuint)
        declare("LinkProgram", GLuint)
        #declare("ShaderSource",GLuint,GLsizei,GLvoid**,GLint[])
        #handcoded("ShaderSource",4)
        declare("UseProgram", GLuint)
        declare("Uniform1f", GLint, GLfloat)
        declare("Uniform2f", GLint, GLfloat, GLfloat)
        declare("Uniform3f", GLint, GLfloat, GLfloat, GLfloat)
        declare("Uniform4f", GLint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("Uniform1i", GLint, GLint)
        declare("Uniform2i", GLint, GLint, GLint)
        declare("Uniform3i", GLint, GLint, GLint, GLint)
        declare("Uniform4i", GLint, GLint, GLint, GLint, GLint)
        declare("Uniform1fv", GLint, GLsizei, GLfloat[1])
        declare("Uniform2fv", GLint, GLsizei, GLfloat[2])
        declare("Uniform3fv", GLint, GLsizei, GLfloat[3])
        declare("Uniform4fv", GLint, GLsizei, GLfloat[4])
        declare("Uniform1iv", GLint, GLsizei, GLint[1])
        declare("Uniform2iv", GLint, GLsizei, GLint[2])
        declare("Uniform3iv", GLint, GLsizei, GLint[3])
        declare("Uniform4iv", GLint, GLsizei, GLint[4])
        declare("UniformMatrix2fv", GLint, GLsizei, GLboolean, GLfloat[4])
        declare("UniformMatrix3fv", GLint, GLsizei, GLboolean, GLfloat[9])
        declare("UniformMatrix4fv", GLint, GLsizei, GLboolean, GLfloat[16])
        declare("ValidateProgram", GLuint)
        declare("VertexAttrib1d", GLuint, GLdouble)
        declare("VertexAttrib1dv", GLuint, GLdouble[1])
        declare("VertexAttrib1f", GLuint, GLfloat)
        declare("VertexAttrib1fv", GLuint, GLfloat[1])
        declare("VertexAttrib1s", GLuint, GLshort)
        declare("VertexAttrib1sv", GLuint, GLshort[1])
        declare("VertexAttrib2d", GLuint, GLdouble, GLdouble)
        declare("VertexAttrib2dv", GLuint, GLdouble[2])
        declare("VertexAttrib2f", GLuint, GLfloat, GLfloat)
        declare("VertexAttrib2fv", GLuint, GLfloat[2])
        declare("VertexAttrib2s", GLuint, GLshort, GLshort)
        declare("VertexAttrib2sv", GLuint, GLshort[2])
        declare("VertexAttrib3d", GLuint, GLdouble, GLdouble, GLdouble)
        declare("VertexAttrib3dv", GLuint, GLdouble[3])
        declare("VertexAttrib3f", GLuint, GLfloat, GLfloat, GLfloat)
        declare("VertexAttrib3fv", GLuint, GLfloat[3])
        declare("VertexAttrib3s", GLuint, GLshort, GLshort, GLshort)
        declare("VertexAttrib3sv", GLuint, GLshort[3])
        declare("VertexAttrib4Nbv", GLuint, GLbyte[4])
        declare("VertexAttrib4Niv", GLuint, GLint[4])
        declare("VertexAttrib4Nsv", GLuint, GLshort[4])
        declare("VertexAttrib4Nub", GLuint, GLubyte, GLubyte, GLubyte, GLubyte)
        declare("VertexAttrib4Nubv", GLuint, GLubyte[4])
        declare("VertexAttrib4Nuiv", GLuint, GLuint[4])
        declare("VertexAttrib4Nusv", GLuint, GLushort[4])
        declare("VertexAttrib4bv", GLuint, GLbyte[4])
        declare("VertexAttrib4d", GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("VertexAttrib4dv", GLuint, GLdouble[4])
        declare("VertexAttrib4f", GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("VertexAttrib4fv", GLuint, GLfloat[4])
        declare("VertexAttrib4iv", GLuint, GLint[4])
        declare("VertexAttrib4s", GLuint, GLshort, GLshort, GLshort, GLshort)
        declare("VertexAttrib4sv", GLuint, GLshort[4])
        declare("VertexAttrib4ubv", GLuint, GLubyte[4])
        declare("VertexAttrib4uiv", GLuint, GLuint[4])
        declare("VertexAttrib4usv", GLuint, GLushort[4])
        declare("VertexAttribPointer", GLuint, GLint, GLenum, GLboolean, GLsizei, GLbuffer)

    if OPENGL_2_1:
        declare("UniformMatrix2x3fv", GLint, GLsizei, GLboolean, GLfloat[6])
        declare("UniformMatrix3x2fv", GLint, GLsizei, GLboolean, GLfloat[6])
        declare("UniformMatrix2x4fv", GLint, GLsizei, GLboolean, GLfloat[8])
        declare("UniformMatrix4x2fv", GLint, GLsizei, GLboolean, GLfloat[8])
        declare("UniformMatrix3x4fv", GLint, GLsizei, GLboolean, GLfloat[12])
        declare("UniformMatrix4x3fv", GLint, GLsizei, GLboolean, GLfloat[12])

    if GL_ARB_TRANSPOSE_MATRIX:
        declare("LoadTransposeMatrixfARB", GLfloat[16])
        declare("LoadTransposeMatrixdARB", GLdouble[16])
        declare("MultTransposeMatrixfARB", GLfloat[16])
        declare("MultTransposeMatrixdARB", GLdouble[16])

    if GL_ARB_MULTISAMPLE:
        declare("SampleCoverageARB", GLclampf, GLboolean)

    if GL_ARB_TEXTURE_COMPRESSION:
        declare("CompressedTexImage3DARB", GLenum, GLint, GLenum, GLsizei, GLsizei, GLsizei,
                GLint, GLsizei, GLbuffer)
        declare("CompressedTexImage2DARB", GLenum, GLint, GLenum, GLsizei, GLsizei, GLint,
                GLsizei, GLbuffer)
        declare("CompressedTexImage1DARB", GLenum, GLint, GLenum, GLsizei, GLint, GLsizei,
                GLbuffer)
        declare("CompressedTexSubImage3DARB", GLenum, GLint, GLint, GLint, GLint, GLsizei,
                GLsizei, GLsizei, GLenum, GLsizei, GLbuffer)
        declare("CompressedTexSubImage2DARB", GLenum, GLint, GLint, GLint, GLsizei, GLsizei,
                GLenum, GLsizei, GLbuffer)
        declare("CompressedTexSubImage1DARB", GLenum, GLint, GLint, GLsizei, GLenum, GLsizei,
                GLbuffer)
        declare("GetCompressedTexImageARB", GLenum, GLint, GLbuffer.asreturn())

    if GL_ARB_POINT_PARAMETERS:
        declare("PointParameterfARB", GLenum, GLfloat)
        declare("PointParameterfvARB", GLenum, GLfloat[1])

    if GL_ARB_VERTEX_BLEND:
        declare("WeightbvARB", GLint, GLbyte[32])  ### not a dynamic size
        declare("WeightsvARB", GLint, GLshort[32])  ### not a dynamic size
        declare("WeightivARB", GLint, GLint[32])  ### not a dynamic size
        declare("WeightfvARB", GLint, GLfloat[32])  ### not a dynamic size
        declare("WeightdvARB", GLint, GLdouble[32])  ### not a dynamic size
        declare("WeightubvARB", GLint, GLubyte[32])  ### not a dynamic size
        declare("WeightusvARB", GLint, GLushort[32])  ### not a dynamic size
        declare("WeightuivARB", GLint, GLuint[32])  ### not a dynamic size
        declare("WeightPointerARB", GLint, GLenum, GLsizei, GLbuffer)
        declare("VertexBlendARB", GLint)

    if GL_ARB_MATRIX_PALETTE:
        declare("CurrentPaletteMatrixARB", GLint)
        declare("MatrixIndexubvARB", GLint, GLubyte[32])  ### not a dynamic size
        declare("MatrixIndexusvARB", GLint, GLushort[32])  ### not a dynamic size
        declare("MatrixIndexuivARB", GLint, GLuint[32])  ### not a dynamic size
        declare("MatrixIndexPointerARB", GLint, GLenum, GLsizei, GLbuffer)

    if GL_ARB_WINDOW_POS:
        declare("WindowPos2dARB", GLdouble, GLdouble)
        declare("WindowPos2dvARB", GLdouble[2])
        declare("WindowPos2fARB", GLfloat, GLfloat)
        declare("WindowPos2fvARB", GLfloat[2])
        declare("WindowPos2iARB", GLint, GLint)
        declare("WindowPos2ivARB", GLint[2])
        declare("WindowPos2sARB", GLshort, GLshort)
        declare("WindowPos2svARB", GLshort[2])
        declare("WindowPos3dARB", GLdouble, GLdouble, GLdouble)
        declare("WindowPos3dvARB", GLdouble[3])
        declare("WindowPos3fARB", GLfloat, GLfloat, GLfloat)
        declare("WindowPos3fvARB", GLfloat[3])
        declare("WindowPos3iARB", GLint, GLint, GLint)
        declare("WindowPos3ivARB", GLint[3])
        declare("WindowPos3sARB", GLshort, GLshort, GLshort)
        declare("WindowPos3svARB", GLshort[3])

    if GL_ARB_FRAGMENT_PROGRAM or GL_ARB_VERTEX_PROGRAM:
        declare("VertexAttrib1dARB", GLuint, GLdouble)
        declare("VertexAttrib1dvARB", GLuint, GLdouble[1])
        declare("VertexAttrib1fARB", GLuint, GLfloat)
        declare("VertexAttrib1fvARB", GLuint, GLfloat[1])
        declare("VertexAttrib1sARB", GLuint, GLshort)
        declare("VertexAttrib1svARB", GLuint, GLshort[1])
        declare("VertexAttrib2dARB", GLuint, GLdouble, GLdouble)
        declare("VertexAttrib2dvARB", GLuint, GLdouble[2])
        declare("VertexAttrib2fARB", GLuint, GLfloat, GLfloat)
        declare("VertexAttrib2fvARB", GLuint, GLfloat[2])
        declare("VertexAttrib2sARB", GLuint, GLshort, GLshort)
        declare("VertexAttrib2svARB", GLuint, GLshort[2])
        declare("VertexAttrib3dARB", GLuint, GLdouble, GLdouble, GLdouble)
        declare("VertexAttrib3dvARB", GLuint, GLdouble[3])
        declare("VertexAttrib3fARB", GLuint, GLfloat, GLfloat, GLfloat)
        declare("VertexAttrib3fvARB", GLuint, GLfloat[3])
        declare("VertexAttrib3sARB", GLuint, GLshort, GLshort, GLshort)
        declare("VertexAttrib3svARB", GLuint, GLshort[3])
        declare("VertexAttrib4NbvARB", GLuint, GLbyte[4])
        declare("VertexAttrib4NivARB", GLuint, GLint[4])
        declare("VertexAttrib4NsvARB", GLuint, GLshort[4])
        declare("VertexAttrib4NubARB", GLuint, GLubyte, GLubyte, GLubyte, GLubyte)
        declare("VertexAttrib4NubvARB", GLuint, GLubyte[4])
        declare("VertexAttrib4NuivARB", GLuint, GLuint[4])
        declare("VertexAttrib4NusvARB", GLuint, GLushort[4])
        declare("VertexAttrib4bvARB", GLuint, GLbyte[4])
        declare("VertexAttrib4dARB", GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("VertexAttrib4dvARB", GLuint, GLdouble[4])
        declare("VertexAttrib4fARB", GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("VertexAttrib4fvARB", GLuint, GLfloat[4])
        declare("VertexAttrib4ivARB", GLuint, GLint[4])
        declare("VertexAttrib4sARB", GLuint, GLshort, GLshort, GLshort, GLshort)
        declare("VertexAttrib4svARB", GLuint, GLshort[4])
        declare("VertexAttrib4ubvARB", GLuint, GLubyte[4])
        declare("VertexAttrib4uivARB", GLuint, GLuint[4])
        declare("VertexAttrib4usvARB", GLuint, GLushort[4])
        declare("VertexAttribPointerARB", GLuint, GLint, GLenum, GLboolean, GLsizei, GLbuffer)
        declare("EnableVertexAttribArrayARB", GLuint)
        declare("DisableVertexAttribArrayARB", GLuint)
        declare("ProgramStringARB", GLenum, GLenum, GLsizei, GLbuffer)
        declare("BindProgramARB", GLenum, GLuint)
        declare("DeleteProgramsARB", GLsizei,
                GLuint[1])  ### not a dynamic size
        declare("GenProgramsARB", GLsizei,
                GLuint[1].asreturn())  ### not a dynamic size
        declare("ProgramEnvParameter4dARB", GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("ProgramEnvParameter4dvARB", GLenum, GLuint, GLdouble[4])
        declare("ProgramEnvParameter4fARB", GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("ProgramEnvParameter4fvARB", GLenum, GLuint, GLfloat[4])
        declare("ProgramLocalParameter4dARB", GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
        declare("ProgramLocalParameter4dvARB", GLenum, GLuint, GLdouble[4])
        declare("ProgramLocalParameter4fARB", GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("ProgramLocalParameter4fvARB", GLenum, GLuint, GLfloat[4])
        declare("GetProgramEnvParameterdvARB", GLenum, GLuint, GLdouble[4].asreturn())
        declare("GetProgramEnvParameterfvARB", GLenum, GLuint, GLfloat[4].asreturn())
        declare("GetProgramLocalParameterdvARB", GLenum, GLuint, GLdouble[4].asreturn())
        declare("GetProgramLocalParameterfvARB", GLenum, GLuint, GLfloat[4].asreturn())
        declare("GetProgramivARB", GLenum, GLenum, GLint[1].asreturn())
        declare("GetProgramStringARB", GLenum, GLenum, GLstring.asreturn())
        declare("GetVertexAttribdvARB", GLuint, GLenum, GLdouble[1].asreturn())
        declare("GetVertexAttribfvARB", GLuint, GLenum, GLfloat[1].asreturn())
        declare("GetVertexAttribivARB", GLuint, GLenum, GLint[1].asreturn())
        #declare("GetVertexAttribPointervARB",GLuint,GLenum,GLvoid**)
        declare(GLboolean, "IsProgramARB", GLuint)

    if GL_ARB_VERTEX_BUFFER_OBJECT:
        declare("BindBufferARB", GLenum, GLuint)
        # declare("DeleteBuffersARB",GLsizei,
        #         GLuint[MAX_BUFFER_ARRAY_SIZE])  ### not a dynamic size
        # declare("GenBuffersARB",GLsizei,
        #         GLuint[MAX_BUFFER_ARRAY_SIZE].asreturn())  ### not a dynamic size
        declare(GLboolean, "IsBufferARB", GLuint)
        declare("BufferDataARB", GLenum, GLsizeiptrARB, GLbuffer, GLenum)
        declare("BufferSubDataARB", GLenum, GLintptrARB, GLsizeiptrARB, GLbuffer)
        declare("GetBufferSubDataARB", GLenum, GLintptrARB, GLsizeiptrARB, GLbuffer.asreturn())
        declare(GLpointer, "MapBufferARB", GLenum, GLenum)
        declare(GLboolean, "UnmapBufferARB", GLenum)
        declare("GetBufferParameterivARB", GLenum, GLenum, GLint[1].asreturn())
        #declare("GetBufferPointervARB",GLenum,GLenum,GLvoid**)

    if GL_ARB_OCCLUSION_QUERY:
        # declare("GenQueriesARB",GLsizei,
        #         GLuint[MAX_QUERY_ARRAY_SIZE].asreturn())  ### not a dynamic size
        # declare("DeleteQueriesARB",GLsizei,
        #         GLuint[MAX_QUERY_ARRAY_SIZE])  ### not a dynamic size
        declare(GLboolean, "IsQueryARB", GLuint)
        declare("BeginQueryARB", GLenum, GLuint)
        declare("EndQueryARB", GLenum)
        declare("GetQueryivARB", GLenum, GLenum, GLint[1].asreturn())
        declare("GetQueryObjectivARB", GLuint, GLenum, GLint[1].asreturn())
        declare("GetQueryObjectuivARB", GLuint, GLenum, GLuint[1].asreturn())

    if GL_ARB_SHADER_OBJECTS:
        declare("DeleteObjectARB", GLhandleARB)
        declare(GLhandleARB, "GetHandleARB", GLenum)
        declare("DetachObjectARB", GLhandleARB, GLhandleARB)
        declare(GLhandleARB, "CreateShaderObjectARB", GLenum)
        # declare("ShaderSourceARB",GLhandleARB,GLsizei, const GLcharARB**,GLint[])
        #handcoded("ShaderSourceARB",4)
        declare("ShaderSourceARB", GLhandleARB, GLsizei, GLcharARB[1][1], GLint[1])
        declare("CompileShaderARB", GLhandleARB)
        declare(GLhandleARB, "CreateProgramObjectARB")
        declare("AttachObjectARB", GLhandleARB, GLhandleARB)
        declare("LinkProgramARB", GLhandleARB)
        declare("UseProgramObjectARB", GLhandleARB)
        declare("ValidateProgramARB", GLhandleARB)
        declare("Uniform1fARB", GLint, GLfloat)
        declare("Uniform2fARB", GLint, GLfloat, GLfloat)
        declare("Uniform3fARB", GLint, GLfloat, GLfloat, GLfloat)
        declare("Uniform4fARB", GLint, GLfloat, GLfloat, GLfloat, GLfloat)
        declare("Uniform1iARB", GLint, GLint)
        declare("Uniform2iARB", GLint, GLint, GLint)
        declare("Uniform3iARB", GLint, GLint, GLint, GLint)
        declare("Uniform4iARB", GLint, GLint, GLint, GLint, GLint)
        declare("Uniform1fvARB", GLint, GLsizei, GLfloat[1])
        declare("Uniform2fvARB", GLint, GLsizei, GLfloat[2])
        declare("Uniform3fvARB", GLint, GLsizei, GLfloat[3])
        declare("Uniform4fvARB", GLint, GLsizei, GLfloat[4])
        declare("Uniform1ivARB", GLint, GLsizei, GLint[1])
        declare("Uniform2ivARB", GLint, GLsizei, GLint[2])
        declare("Uniform3ivARB", GLint, GLsizei, GLint[3])
        declare("Uniform4ivARB", GLint, GLsizei, GLint[4])
        declare("UniformMatrix2fvARB", GLint, GLsizei, GLboolean, GLfloat[4])
        declare("UniformMatrix3fvARB", GLint, GLsizei, GLboolean, GLfloat[9])
        declare("UniformMatrix4fvARB", GLint, GLsizei, GLboolean, GLfloat[16])
        declare("GetObjectParameterfvARB", GLhandleARB, GLenum, GLfloat[1].asreturn())
        declare("GetObjectParameterivARB", GLhandleARB, GLenum, GLint[1].asreturn())
        declare("GetInfoLogARB", GLhandleARB, GLsizei, GLsizei[1].asreturn(), GLstring.asreturn())
        declare("GetAttachedObjectsARB", GLhandleARB, GLsizei, GLsizei[1].asreturn(),
                GLbuffer.asreturn())
        declare(GLint, "GetUniformLocationARB", GLhandleARB, GLstring)
        declare("GetActiveUniformARB", GLhandleARB, GLuint, GLsizei, GLsizei[1].asreturn(),
                GLint[1].asreturn(), GLenum[1].asreturn(), GLstring.asreturn())
        declare("GetUniformfvARB", GLhandleARB, GLint, GLfloat[16].asreturn())
        declare("GetUniformivARB", GLhandleARB, GLint, GLint[16].asreturn())
        declare("GetShaderSourceARB", GLhandleARB, GLsizei, GLsizei[1].asreturn(),
                GLstring.asreturn())

    if GL_ARB_VERTEX_SHADER:
        declare("BindAttribLocationARB", GLhandleARB, GLuint, GLstring)
        declare("GetActiveAttribARB", GLhandleARB, GLuint, GLsizei, GLsizei[1].asreturn(),
                GLint[1].asreturn(), GLenum[1].asreturn(), GLstring.asreturn())
        declare(GLint, "GetAttribLocationARB", GLhandleARB, GLstring)

    if GL_ARB_DRAW_BUFFERS:
        declare("DrawBuffersARB", GLsizei, GLenum[16])  ### not a dynamic size

    if GL_ARB_COLOR_BUFFER_FLOAT:
        declare("ClampColorARB", GLenum, GLenum)

    # Things we force to exist via GL trickery.
    declare("GetProgramiv", GLuint, GLenum, GLint[1].asreturn())
    declare("GetShaderiv", GLuint, GLenum, GLint[1].asreturn())
    declare("DeleteProgram", GLuint)
    declare("DeleteShader", GLuint)
    declare("GetProgramInfoLog", GLhandleARB, GLsizei, GLsizei[1].asreturn(), GLstring.asreturn())
    declare("GetShaderInfoLog", GLhandleARB, GLsizei, GLsizei[1].asreturn(), GLstring.asreturn())

    # -------- GL Constants --------

    # Boolean values
    constant("FALSE")
    constant("TRUE")

    # Data types
    constant("BYTE")
    constant("UNSIGNED_BYTE")
    constant("SHORT")
    constant("UNSIGNED_SHORT")
    constant("INT")
    constant("UNSIGNED_INT")
    constant("FLOAT")
    constant("2_BYTES")
    constant("3_BYTES")
    constant("4_BYTES")
    constant("DOUBLE")

    # Primitives
    constant("POINTS")
    constant("LINES")
    constant("LINE_LOOP")
    constant("LINE_STRIP")
    constant("TRIANGLES")
    constant("TRIANGLE_STRIP")
    constant("TRIANGLE_FAN")
    constant("QUADS")
    constant("QUAD_STRIP")
    constant("POLYGON")

    # Vertex Arrays
    constant("VERTEX_ARRAY")
    constant("NORMAL_ARRAY")
    constant("COLOR_ARRAY")
    constant("INDEX_ARRAY")
    constant("TEXTURE_COORD_ARRAY")
    constant("EDGE_FLAG_ARRAY")
    constant("VERTEX_ARRAY_SIZE")
    constant("VERTEX_ARRAY_TYPE")
    constant("VERTEX_ARRAY_STRIDE")
    constant("NORMAL_ARRAY_TYPE")
    constant("NORMAL_ARRAY_STRIDE")
    constant("COLOR_ARRAY_SIZE")
    constant("COLOR_ARRAY_TYPE")
    constant("COLOR_ARRAY_STRIDE")
    constant("INDEX_ARRAY_TYPE")
    constant("INDEX_ARRAY_STRIDE")
    constant("TEXTURE_COORD_ARRAY_SIZE")
    constant("TEXTURE_COORD_ARRAY_TYPE")
    constant("TEXTURE_COORD_ARRAY_STRIDE")
    constant("EDGE_FLAG_ARRAY_STRIDE")
    constant("VERTEX_ARRAY_POINTER")
    constant("NORMAL_ARRAY_POINTER")
    constant("COLOR_ARRAY_POINTER")
    constant("INDEX_ARRAY_POINTER")
    constant("TEXTURE_COORD_ARRAY_POINTER")
    constant("EDGE_FLAG_ARRAY_POINTER")
    constant("V2F")
    constant("V3F")
    constant("C4UB_V2F")
    constant("C4UB_V3F")
    constant("C3F_V3F")
    constant("N3F_V3F")
    constant("C4F_N3F_V3F")
    constant("T2F_V3F")
    constant("T4F_V4F")
    constant("T2F_C4UB_V3F")
    constant("T2F_C3F_V3F")
    constant("T2F_N3F_V3F")
    constant("T2F_C4F_N3F_V3F")
    constant("T4F_C4F_N3F_V4F")

    # Matrix Mode
    constant("MATRIX_MODE")
    constant("MODELVIEW")
    constant("PROJECTION")
    constant("TEXTURE")

    # Points
    constant("POINT_SMOOTH")
    constant("POINT_SIZE")
    constant("POINT_SIZE_GRANULARITY")
    constant("POINT_SIZE_RANGE")

    # Lines
    constant("LINE_SMOOTH")
    constant("LINE_STIPPLE")
    constant("LINE_STIPPLE_PATTERN")
    constant("LINE_STIPPLE_REPEAT")
    constant("LINE_WIDTH")
    constant("LINE_WIDTH_GRANULARITY")
    constant("LINE_WIDTH_RANGE")

    # Polygons
    constant("POINT")
    constant("LINE")
    constant("FILL")
    constant("CW")
    constant("CCW")
    constant("FRONT")
    constant("BACK")
    constant("POLYGON_MODE")
    constant("POLYGON_SMOOTH")
    constant("POLYGON_STIPPLE")
    constant("EDGE_FLAG")
    constant("CULL_FACE")
    constant("CULL_FACE_MODE")
    constant("FRONT_FACE")
    constant("POLYGON_OFFSET_FACTOR")
    constant("POLYGON_OFFSET_UNITS")
    constant("POLYGON_OFFSET_POINT")
    constant("POLYGON_OFFSET_LINE")
    constant("POLYGON_OFFSET_FILL")

    # Display Lists
    constant("COMPILE")
    constant("COMPILE_AND_EXECUTE")
    constant("LIST_BASE")
    constant("LIST_INDEX")
    constant("LIST_MODE")

    # Depth buffer
    constant("NEVER")
    constant("LESS")
    constant("EQUAL")
    constant("LEQUAL")
    constant("GREATER")
    constant("NOTEQUAL")
    constant("GEQUAL")
    constant("ALWAYS")
    constant("DEPTH_TEST")
    constant("DEPTH_BITS")
    constant("DEPTH_CLEAR_VALUE")
    constant("DEPTH_FUNC")
    constant("DEPTH_RANGE")
    constant("DEPTH_WRITEMASK")
    constant("DEPTH_COMPONENT")

    # Lighting
    constant("LIGHTING")
    constant("LIGHT0")
    constant("LIGHT1")
    constant("LIGHT2")
    constant("LIGHT3")
    constant("LIGHT4")
    constant("LIGHT5")
    constant("LIGHT6")
    constant("LIGHT7")
    constant("SPOT_EXPONENT")
    constant("SPOT_CUTOFF")
    constant("CONSTANT_ATTENUATION")
    constant("LINEAR_ATTENUATION")
    constant("QUADRATIC_ATTENUATION")
    constant("AMBIENT")
    constant("DIFFUSE")
    constant("SPECULAR")
    constant("SHININESS")
    constant("EMISSION")
    constant("POSITION")
    constant("SPOT_DIRECTION")
    constant("AMBIENT_AND_DIFFUSE")
    constant("COLOR_INDEXES")
    constant("LIGHT_MODEL_TWO_SIDE")
    constant("LIGHT_MODEL_LOCAL_VIEWER")
    constant("LIGHT_MODEL_AMBIENT")
    constant("FRONT_AND_BACK")
    constant("SHADE_MODEL")
    constant("FLAT")
    constant("SMOOTH")
    constant("COLOR_MATERIAL")
    constant("COLOR_MATERIAL_FACE")
    constant("COLOR_MATERIAL_PARAMETER")
    constant("NORMALIZE")

    # User clipping planes
    constant("CLIP_PLANE0")
    constant("CLIP_PLANE1")
    constant("CLIP_PLANE2")
    constant("CLIP_PLANE3")
    constant("CLIP_PLANE4")
    constant("CLIP_PLANE5")

    # Accumulation buffer
    constant("ACCUM_RED_BITS")
    constant("ACCUM_GREEN_BITS")
    constant("ACCUM_BLUE_BITS")
    constant("ACCUM_ALPHA_BITS")
    constant("ACCUM_CLEAR_VALUE")
    constant("ACCUM")
    constant("ADD")
    constant("LOAD")
    constant("MULT")
    constant("RETURN")

    # Alpha testing
    constant("ALPHA_TEST")
    constant("ALPHA_TEST_REF")
    constant("ALPHA_TEST_FUNC")

    # Blending
    constant("BLEND")
    constant("BLEND_SRC")
    constant("BLEND_DST")
    constant("ZERO")
    constant("ONE")
    constant("SRC_COLOR")
    constant("ONE_MINUS_SRC_COLOR")
    constant("SRC_ALPHA")
    constant("ONE_MINUS_SRC_ALPHA")
    constant("DST_ALPHA")
    constant("ONE_MINUS_DST_ALPHA")
    constant("DST_COLOR")
    constant("ONE_MINUS_DST_COLOR")
    constant("SRC_ALPHA_SATURATE")

    # Render Mode
    constant("FEEDBACK")
    constant("RENDER")
    constant("SELECT")

    # Feedback
    constant("2D")
    constant("3D")
    constant("3D_COLOR")
    constant("3D_COLOR_TEXTURE")
    constant("4D_COLOR_TEXTURE")
    constant("POINT_TOKEN")
    constant("LINE_TOKEN")
    constant("LINE_RESET_TOKEN")
    constant("POLYGON_TOKEN")
    constant("BITMAP_TOKEN")
    constant("DRAW_PIXEL_TOKEN")
    constant("COPY_PIXEL_TOKEN")
    constant("PASS_THROUGH_TOKEN")
    constant("FEEDBACK_BUFFER_POINTER")
    constant("FEEDBACK_BUFFER_SIZE")
    constant("FEEDBACK_BUFFER_TYPE")

    # Selection
    constant("SELECTION_BUFFER_POINTER")
    constant("SELECTION_BUFFER_SIZE")

    # Fog
    constant("FOG")
    constant("FOG_MODE")
    constant("FOG_DENSITY")
    constant("FOG_COLOR")
    constant("FOG_INDEX")
    constant("FOG_START")
    constant("FOG_END")
    constant("LINEAR")
    constant("EXP")
    constant("EXP2")

    # Logic Ops
    constant("LOGIC_OP")
    constant("INDEX_LOGIC_OP")
    constant("COLOR_LOGIC_OP")
    constant("LOGIC_OP_MODE")
    constant("CLEAR")
    constant("SET")
    constant("COPY")
    constant("COPY_INVERTED")
    constant("NOOP")
    constant("INVERT")
    constant("AND")
    constant("NAND")
    constant("OR")
    constant("NOR")
    constant("XOR")
    constant("EQUIV")
    constant("AND_REVERSE")
    constant("AND_INVERTED")
    constant("OR_REVERSE")
    constant("OR_INVERTED")

    # Stencil
    constant("STENCIL_BITS")
    constant("STENCIL_TEST")
    constant("STENCIL_CLEAR_VALUE")
    constant("STENCIL_FUNC")
    constant("STENCIL_VALUE_MASK")
    constant("STENCIL_FAIL")
    constant("STENCIL_PASS_DEPTH_FAIL")
    constant("STENCIL_PASS_DEPTH_PASS")
    constant("STENCIL_REF")
    constant("STENCIL_WRITEMASK")
    constant("STENCIL_INDEX")
    constant("KEEP")
    constant("REPLACE")
    constant("INCR")
    constant("DECR")

    # Buffers, Pixel Drawing/Reading
    constant("NONE")
    constant("LEFT")
    constant("RIGHT")
    constant("FRONT_LEFT")
    constant("FRONT_RIGHT")
    constant("BACK_LEFT")
    constant("BACK_RIGHT")
    constant("AUX0")
    constant("AUX1")
    constant("AUX2")
    constant("AUX3")
    constant("COLOR_INDEX")
    constant("RED")
    constant("GREEN")
    constant("BLUE")
    constant("ALPHA")
    constant("LUMINANCE")
    constant("LUMINANCE_ALPHA")
    constant("ALPHA_BITS")
    constant("RED_BITS")
    constant("GREEN_BITS")
    constant("BLUE_BITS")
    constant("INDEX_BITS")
    constant("SUBPIXEL_BITS")
    constant("AUX_BUFFERS")
    constant("READ_BUFFER")
    constant("DRAW_BUFFER")
    constant("DOUBLEBUFFER")
    constant("STEREO")
    constant("BITMAP")
    constant("COLOR")
    constant("DEPTH")
    constant("STENCIL")
    constant("DITHER")
    constant("RGB")
    constant("RGBA")

    # Implementation limits
    constant("MAX_LIST_NESTING")
    constant("MAX_EVAL_ORDER")
    constant("MAX_LIGHTS")
    constant("MAX_CLIP_PLANES")
    constant("MAX_TEXTURE_SIZE")
    constant("MAX_PIXEL_MAP_TABLE")
    constant("MAX_ATTRIB_STACK_DEPTH")
    constant("MAX_MODELVIEW_STACK_DEPTH")
    constant("MAX_NAME_STACK_DEPTH")
    constant("MAX_PROJECTION_STACK_DEPTH")
    constant("MAX_TEXTURE_STACK_DEPTH")
    constant("MAX_VIEWPORT_DIMS")
    constant("MAX_CLIENT_ATTRIB_STACK_DEPTH")

    # Gets
    constant("ATTRIB_STACK_DEPTH")
    constant("CLIENT_ATTRIB_STACK_DEPTH")
    constant("COLOR_CLEAR_VALUE")
    constant("COLOR_WRITEMASK")
    constant("CURRENT_INDEX")
    constant("CURRENT_COLOR")
    constant("CURRENT_NORMAL")
    constant("CURRENT_RASTER_COLOR")
    constant("CURRENT_RASTER_DISTANCE")
    constant("CURRENT_RASTER_INDEX")
    constant("CURRENT_RASTER_POSITION")
    constant("CURRENT_RASTER_TEXTURE_COORDS")
    constant("CURRENT_RASTER_POSITION_VALID")
    constant("CURRENT_TEXTURE_COORDS")
    constant("INDEX_CLEAR_VALUE")
    constant("INDEX_MODE")
    constant("INDEX_WRITEMASK")
    constant("MODELVIEW_MATRIX")
    constant("MODELVIEW_STACK_DEPTH")
    constant("NAME_STACK_DEPTH")
    constant("PROJECTION_MATRIX")
    constant("PROJECTION_STACK_DEPTH")
    constant("RENDER_MODE")
    constant("RGBA_MODE")
    constant("TEXTURE_MATRIX")
    constant("TEXTURE_STACK_DEPTH")
    constant("VIEWPORT")

    # Evaluators
    constant("AUTO_NORMAL")
    constant("MAP1_COLOR_4")
    constant("MAP1_INDEX")
    constant("MAP1_NORMAL")
    constant("MAP1_TEXTURE_COORD_1")
    constant("MAP1_TEXTURE_COORD_2")
    constant("MAP1_TEXTURE_COORD_3")
    constant("MAP1_TEXTURE_COORD_4")
    constant("MAP1_VERTEX_3")
    constant("MAP1_VERTEX_4")
    constant("MAP2_COLOR_4")
    constant("MAP2_INDEX")
    constant("MAP2_NORMAL")
    constant("MAP2_TEXTURE_COORD_1")
    constant("MAP2_TEXTURE_COORD_2")
    constant("MAP2_TEXTURE_COORD_3")
    constant("MAP2_TEXTURE_COORD_4")
    constant("MAP2_VERTEX_3")
    constant("MAP2_VERTEX_4")
    constant("MAP1_GRID_DOMAIN")
    constant("MAP1_GRID_SEGMENTS")
    constant("MAP2_GRID_DOMAIN")
    constant("MAP2_GRID_SEGMENTS")
    constant("COEFF")
    constant("ORDER")
    constant("DOMAIN")

    # Hints
    constant("PERSPECTIVE_CORRECTION_HINT")
    constant("POINT_SMOOTH_HINT")
    constant("LINE_SMOOTH_HINT")
    constant("POLYGON_SMOOTH_HINT")
    constant("FOG_HINT")
    constant("DONT_CARE")
    constant("FASTEST")
    constant("NICEST")

    # Scissor box
    constant("SCISSOR_BOX")
    constant("SCISSOR_TEST")

    # Pixel Mode / Transfer
    constant("MAP_COLOR")
    constant("MAP_STENCIL")
    constant("INDEX_SHIFT")
    constant("INDEX_OFFSET")
    constant("RED_SCALE")
    constant("RED_BIAS")
    constant("GREEN_SCALE")
    constant("GREEN_BIAS")
    constant("BLUE_SCALE")
    constant("BLUE_BIAS")
    constant("ALPHA_SCALE")
    constant("ALPHA_BIAS")
    constant("DEPTH_SCALE")
    constant("DEPTH_BIAS")
    constant("PIXEL_MAP_S_TO_S_SIZE")
    constant("PIXEL_MAP_I_TO_I_SIZE")
    constant("PIXEL_MAP_I_TO_R_SIZE")
    constant("PIXEL_MAP_I_TO_G_SIZE")
    constant("PIXEL_MAP_I_TO_B_SIZE")
    constant("PIXEL_MAP_I_TO_A_SIZE")
    constant("PIXEL_MAP_R_TO_R_SIZE")
    constant("PIXEL_MAP_G_TO_G_SIZE")
    constant("PIXEL_MAP_B_TO_B_SIZE")
    constant("PIXEL_MAP_A_TO_A_SIZE")
    constant("PIXEL_MAP_S_TO_S")
    constant("PIXEL_MAP_I_TO_I")
    constant("PIXEL_MAP_I_TO_R")
    constant("PIXEL_MAP_I_TO_G")
    constant("PIXEL_MAP_I_TO_B")
    constant("PIXEL_MAP_I_TO_A")
    constant("PIXEL_MAP_R_TO_R")
    constant("PIXEL_MAP_G_TO_G")
    constant("PIXEL_MAP_B_TO_B")
    constant("PIXEL_MAP_A_TO_A")
    constant("PACK_ALIGNMENT")
    constant("PACK_LSB_FIRST")
    constant("PACK_ROW_LENGTH")
    constant("PACK_SKIP_PIXELS")
    constant("PACK_SKIP_ROWS")
    constant("PACK_SWAP_BYTES")
    constant("UNPACK_ALIGNMENT")
    constant("UNPACK_LSB_FIRST")
    constant("UNPACK_ROW_LENGTH")
    constant("UNPACK_SKIP_PIXELS")
    constant("UNPACK_SKIP_ROWS")
    constant("UNPACK_SWAP_BYTES")
    constant("ZOOM_X")
    constant("ZOOM_Y")

    # Texture mapping
    constant("TEXTURE_ENV")
    constant("TEXTURE_ENV_MODE")
    constant("TEXTURE_1D")
    constant("TEXTURE_2D")
    constant("TEXTURE_WRAP_S")
    constant("TEXTURE_WRAP_T")
    constant("TEXTURE_MAG_FILTER")
    constant("TEXTURE_MIN_FILTER")
    constant("TEXTURE_ENV_COLOR")
    constant("TEXTURE_GEN_S")
    constant("TEXTURE_GEN_T")
    constant("TEXTURE_GEN_MODE")
    constant("TEXTURE_BORDER_COLOR")
    constant("TEXTURE_WIDTH")
    constant("TEXTURE_HEIGHT")
    constant("TEXTURE_BORDER")
    constant("TEXTURE_COMPONENTS")
    constant("TEXTURE_RED_SIZE")
    constant("TEXTURE_GREEN_SIZE")
    constant("TEXTURE_BLUE_SIZE")
    constant("TEXTURE_ALPHA_SIZE")
    constant("TEXTURE_LUMINANCE_SIZE")
    constant("TEXTURE_INTENSITY_SIZE")
    constant("NEAREST_MIPMAP_NEAREST")
    constant("NEAREST_MIPMAP_LINEAR")
    constant("LINEAR_MIPMAP_NEAREST")
    constant("LINEAR_MIPMAP_LINEAR")
    constant("OBJECT_LINEAR")
    constant("OBJECT_PLANE")
    constant("EYE_LINEAR")
    constant("EYE_PLANE")
    constant("SPHERE_MAP")
    constant("DECAL")
    constant("MODULATE")
    constant("NEAREST")
    constant("REPEAT")
    constant("CLAMP")
    constant("S")
    constant("T")
    constant("R")
    constant("Q")
    constant("TEXTURE_GEN_R")
    constant("TEXTURE_GEN_Q")

    # Utility
    constant("VENDOR")
    constant("RENDERER")
    constant("VERSION")
    constant("EXTENSIONS")

    # Errors
    constant("NO_ERROR")
    constant("INVALID_ENUM")
    constant("INVALID_VALUE")
    constant("INVALID_OPERATION")
    constant("STACK_OVERFLOW")
    constant("STACK_UNDERFLOW")
    constant("OUT_OF_MEMORY")

    # glPush/PopAttrib bits
    constant("CURRENT_BIT")
    constant("POINT_BIT")
    constant("LINE_BIT")
    constant("POLYGON_BIT")
    constant("POLYGON_STIPPLE_BIT")
    constant("PIXEL_MODE_BIT")
    constant("LIGHTING_BIT")
    constant("FOG_BIT")
    constant("DEPTH_BUFFER_BIT")
    constant("ACCUM_BUFFER_BIT")
    constant("STENCIL_BUFFER_BIT")
    constant("VIEWPORT_BIT")
    constant("TRANSFORM_BIT")
    constant("ENABLE_BIT")
    constant("COLOR_BUFFER_BIT")
    constant("HINT_BIT")
    constant("EVAL_BIT")
    constant("LIST_BIT")
    constant("TEXTURE_BIT")
    constant("SCISSOR_BIT")
    constant("ALL_ATTRIB_BITS")

    # OpenGL 1.1
    constant("PROXY_TEXTURE_1D")
    constant("PROXY_TEXTURE_2D")
    constant("TEXTURE_PRIORITY")
    constant("TEXTURE_RESIDENT")
    constant("TEXTURE_BINDING_1D")
    constant("TEXTURE_BINDING_2D")
    constant("TEXTURE_INTERNAL_FORMAT")
    constant("ALPHA4")
    constant("ALPHA8")
    constant("ALPHA12")
    constant("ALPHA16")
    constant("LUMINANCE4")
    constant("LUMINANCE8")
    constant("LUMINANCE12")
    constant("LUMINANCE16")
    constant("LUMINANCE4_ALPHA4")
    constant("LUMINANCE6_ALPHA2")
    constant("LUMINANCE8_ALPHA8")
    constant("LUMINANCE12_ALPHA4")
    constant("LUMINANCE12_ALPHA12")
    constant("LUMINANCE16_ALPHA16")
    constant("INTENSITY")
    constant("INTENSITY4")
    constant("INTENSITY8")
    constant("INTENSITY12")
    constant("INTENSITY16")
    constant("R3_G3_B2")
    constant("RGB4")
    constant("RGB5")
    constant("RGB8")
    constant("RGB10")
    constant("RGB12")
    constant("RGB16")
    constant("RGBA2")
    constant("RGBA4")
    constant("RGB5_A1")
    constant("RGBA8")
    constant("RGB10_A2")
    constant("RGBA12")
    constant("RGBA16")
    constant("CLIENT_PIXEL_STORE_BIT")
    constant("CLIENT_VERTEX_ARRAY_BIT")
    # constant("ALL_CLIENT_ATTRIB_BITS")
    constant("CLIENT_ALL_ATTRIB_BITS")

    if OPENGL_1_2:
        constant("RESCALE_NORMAL")
        constant("CLAMP_TO_EDGE")
        constant("MAX_ELEMENTS_VERTICES")
        constant("MAX_ELEMENTS_INDICES")
        constant("BGR")
        constant("BGRA")
        constant("UNSIGNED_BYTE_3_3_2")
        constant("UNSIGNED_BYTE_2_3_3_REV")
        constant("UNSIGNED_SHORT_5_6_5")
        constant("UNSIGNED_SHORT_5_6_5_REV")
        constant("UNSIGNED_SHORT_4_4_4_4")
        constant("UNSIGNED_SHORT_4_4_4_4_REV")
        constant("UNSIGNED_SHORT_5_5_5_1")
        constant("UNSIGNED_SHORT_1_5_5_5_REV")
        constant("UNSIGNED_INT_8_8_8_8")
        constant("UNSIGNED_INT_8_8_8_8_REV")
        constant("UNSIGNED_INT_10_10_10_2")
        constant("UNSIGNED_INT_2_10_10_10_REV")
        constant("LIGHT_MODEL_COLOR_CONTROL")
        constant("SINGLE_COLOR")
        constant("SEPARATE_SPECULAR_COLOR")
        constant("TEXTURE_MIN_LOD")
        constant("TEXTURE_MAX_LOD")
        constant("TEXTURE_BASE_LEVEL")
        constant("TEXTURE_MAX_LEVEL")
        constant("SMOOTH_POINT_SIZE_RANGE")
        constant("SMOOTH_POINT_SIZE_GRANULARITY")
        constant("SMOOTH_LINE_WIDTH_RANGE")
        constant("SMOOTH_LINE_WIDTH_GRANULARITY")
        constant("ALIASED_POINT_SIZE_RANGE")
        constant("ALIASED_LINE_WIDTH_RANGE")
        constant("PACK_SKIP_IMAGES")
        constant("PACK_IMAGE_HEIGHT")
        constant("UNPACK_SKIP_IMAGES")
        constant("UNPACK_IMAGE_HEIGHT")
        constant("TEXTURE_3D")
        constant("PROXY_TEXTURE_3D")
        constant("TEXTURE_DEPTH")
        constant("TEXTURE_WRAP_R")
        constant("MAX_3D_TEXTURE_SIZE")
        constant("TEXTURE_BINDING_3D")

    if GL_ARB_IMAGING:
        constant("CONSTANT_COLOR")
        constant("ONE_MINUS_CONSTANT_COLOR")
        constant("CONSTANT_ALPHA")
        constant("ONE_MINUS_CONSTANT_ALPHA")
        constant("COLOR_TABLE")
        constant("POST_CONVOLUTION_COLOR_TABLE")
        constant("POST_COLOR_MATRIX_COLOR_TABLE")
        constant("PROXY_COLOR_TABLE")
        constant("PROXY_POST_CONVOLUTION_COLOR_TABLE")
        constant("PROXY_POST_COLOR_MATRIX_COLOR_TABLE")
        constant("COLOR_TABLE_SCALE")
        constant("COLOR_TABLE_BIAS")
        constant("COLOR_TABLE_FORMAT")
        constant("COLOR_TABLE_WIDTH")
        constant("COLOR_TABLE_RED_SIZE")
        constant("COLOR_TABLE_GREEN_SIZE")
        constant("COLOR_TABLE_BLUE_SIZE")
        constant("COLOR_TABLE_ALPHA_SIZE")
        constant("COLOR_TABLE_LUMINANCE_SIZE")
        constant("COLOR_TABLE_INTENSITY_SIZE")
        constant("CONVOLUTION_1D")
        constant("CONVOLUTION_2D")
        constant("SEPARABLE_2D")
        constant("CONVOLUTION_BORDER_MODE")
        constant("CONVOLUTION_FILTER_SCALE")
        constant("CONVOLUTION_FILTER_BIAS")
        constant("REDUCE")
        constant("CONVOLUTION_FORMAT")
        constant("CONVOLUTION_WIDTH")
        constant("CONVOLUTION_HEIGHT")
        constant("MAX_CONVOLUTION_WIDTH")
        constant("MAX_CONVOLUTION_HEIGHT")
        constant("POST_CONVOLUTION_RED_SCALE")
        constant("POST_CONVOLUTION_GREEN_SCALE")
        constant("POST_CONVOLUTION_BLUE_SCALE")
        constant("POST_CONVOLUTION_ALPHA_SCALE")
        constant("POST_CONVOLUTION_RED_BIAS")
        constant("POST_CONVOLUTION_GREEN_BIAS")
        constant("POST_CONVOLUTION_BLUE_BIAS")
        constant("POST_CONVOLUTION_ALPHA_BIAS")
        constant("CONSTANT_BORDER")
        constant("REPLICATE_BORDER")
        constant("CONVOLUTION_BORDER_COLOR")
        constant("COLOR_MATRIX")
        constant("COLOR_MATRIX_STACK_DEPTH")
        constant("MAX_COLOR_MATRIX_STACK_DEPTH")
        constant("POST_COLOR_MATRIX_RED_SCALE")
        constant("POST_COLOR_MATRIX_GREEN_SCALE")
        constant("POST_COLOR_MATRIX_BLUE_SCALE")
        constant("POST_COLOR_MATRIX_ALPHA_SCALE")
        constant("POST_COLOR_MATRIX_RED_BIAS")
        constant("POST_COLOR_MATRIX_GREEN_BIAS")
        constant("POST_COLOR_MATRIX_BLUE_BIAS")
        constant("POST_COLOR_MATRIX_ALPHA_BIAS")
        constant("HISTOGRAM")
        constant("PROXY_HISTOGRAM")
        constant("HISTOGRAM_WIDTH")
        constant("HISTOGRAM_FORMAT")
        constant("HISTOGRAM_RED_SIZE")
        constant("HISTOGRAM_GREEN_SIZE")
        constant("HISTOGRAM_BLUE_SIZE")
        constant("HISTOGRAM_ALPHA_SIZE")
        constant("HISTOGRAM_LUMINANCE_SIZE")
        constant("HISTOGRAM_SINK")
        constant("MINMAX")
        constant("MINMAX_FORMAT")
        constant("MINMAX_SINK")
        constant("TABLE_TOO_LARGE")
        constant("BLEND_EQUATION")
        constant("MIN")
        constant("MAX")
        constant("FUNC_ADD")
        constant("FUNC_SUBTRACT")
        constant("FUNC_REVERSE_SUBTRACT")
        constant("BLEND_COLOR")

    if OPENGL_1_3:
        constant("TEXTURE0")
        constant("TEXTURE1")
        constant("TEXTURE2")
        constant("TEXTURE3")
        constant("TEXTURE4")
        constant("TEXTURE5")
        constant("TEXTURE6")
        constant("TEXTURE7")
        constant("TEXTURE8")
        constant("TEXTURE9")
        constant("TEXTURE10")
        constant("TEXTURE11")
        constant("TEXTURE12")
        constant("TEXTURE13")
        constant("TEXTURE14")
        constant("TEXTURE15")
        constant("TEXTURE16")
        constant("TEXTURE17")
        constant("TEXTURE18")
        constant("TEXTURE19")
        constant("TEXTURE20")
        constant("TEXTURE21")
        constant("TEXTURE22")
        constant("TEXTURE23")
        constant("TEXTURE24")
        constant("TEXTURE25")
        constant("TEXTURE26")
        constant("TEXTURE27")
        constant("TEXTURE28")
        constant("TEXTURE29")
        constant("TEXTURE30")
        constant("TEXTURE31")
        constant("ACTIVE_TEXTURE")
        constant("CLIENT_ACTIVE_TEXTURE")
        constant("MAX_TEXTURE_UNITS")
        constant("NORMAL_MAP")
        constant("REFLECTION_MAP")
        constant("TEXTURE_CUBE_MAP")
        constant("TEXTURE_BINDING_CUBE_MAP")
        constant("TEXTURE_CUBE_MAP_POSITIVE_X")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_X")
        constant("TEXTURE_CUBE_MAP_POSITIVE_Y")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_Y")
        constant("TEXTURE_CUBE_MAP_POSITIVE_Z")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_Z")
        constant("PROXY_TEXTURE_CUBE_MAP")
        constant("MAX_CUBE_MAP_TEXTURE_SIZE")
        constant("COMPRESSED_ALPHA")
        constant("COMPRESSED_LUMINANCE")
        constant("COMPRESSED_LUMINANCE_ALPHA")
        constant("COMPRESSED_INTENSITY")
        constant("COMPRESSED_RGB")
        constant("COMPRESSED_RGBA")
        constant("TEXTURE_COMPRESSION_HINT")
        constant("TEXTURE_COMPRESSED_IMAGE_SIZE")
        constant("TEXTURE_COMPRESSED")
        constant("NUM_COMPRESSED_TEXTURE_FORMATS")
        constant("COMPRESSED_TEXTURE_FORMATS")
        constant("MULTISAMPLE")
        constant("SAMPLE_ALPHA_TO_COVERAGE")
        constant("SAMPLE_ALPHA_TO_ONE")
        constant("SAMPLE_COVERAGE")
        constant("SAMPLE_BUFFERS")
        constant("SAMPLES")
        constant("SAMPLE_COVERAGE_VALUE")
        constant("SAMPLE_COVERAGE_INVERT")
        constant("MULTISAMPLE_BIT")
        constant("TRANSPOSE_MODELVIEW_MATRIX")
        constant("TRANSPOSE_PROJECTION_MATRIX")
        constant("TRANSPOSE_TEXTURE_MATRIX")
        constant("TRANSPOSE_COLOR_MATRIX")
        constant("COMBINE")
        constant("COMBINE_RGB")
        constant("COMBINE_ALPHA")
        constant("SOURCE0_RGB")
        constant("SOURCE1_RGB")
        constant("SOURCE2_RGB")
        constant("SOURCE0_ALPHA")
        constant("SOURCE1_ALPHA")
        constant("SOURCE2_ALPHA")
        constant("OPERAND0_RGB")
        constant("OPERAND1_RGB")
        constant("OPERAND2_RGB")
        constant("OPERAND0_ALPHA")
        constant("OPERAND1_ALPHA")
        constant("OPERAND2_ALPHA")
        constant("RGB_SCALE")
        constant("ADD_SIGNED")
        constant("INTERPOLATE")
        constant("SUBTRACT")
        constant("CONSTANT")
        constant("PRIMARY_COLOR")
        constant("PREVIOUS")
        constant("DOT3_RGB")
        constant("DOT3_RGBA")
        constant("CLAMP_TO_BORDER")

    if GL_ARB_MULTITEXTURE:
        constant("TEXTURE0_ARB")
        constant("TEXTURE1_ARB")
        constant("TEXTURE2_ARB")
        constant("TEXTURE3_ARB")
        constant("TEXTURE4_ARB")
        constant("TEXTURE5_ARB")
        constant("TEXTURE6_ARB")
        constant("TEXTURE7_ARB")
        constant("TEXTURE8_ARB")
        constant("TEXTURE9_ARB")
        constant("TEXTURE10_ARB")
        constant("TEXTURE11_ARB")
        constant("TEXTURE12_ARB")
        constant("TEXTURE13_ARB")
        constant("TEXTURE14_ARB")
        constant("TEXTURE15_ARB")
        constant("TEXTURE16_ARB")
        constant("TEXTURE17_ARB")
        constant("TEXTURE18_ARB")
        constant("TEXTURE19_ARB")
        constant("TEXTURE20_ARB")
        constant("TEXTURE21_ARB")
        constant("TEXTURE22_ARB")
        constant("TEXTURE23_ARB")
        constant("TEXTURE24_ARB")
        constant("TEXTURE25_ARB")
        constant("TEXTURE26_ARB")
        constant("TEXTURE27_ARB")
        constant("TEXTURE28_ARB")
        constant("TEXTURE29_ARB")
        constant("TEXTURE30_ARB")
        constant("TEXTURE31_ARB")
        constant("ACTIVE_TEXTURE_ARB")
        constant("CLIENT_ACTIVE_TEXTURE_ARB")
        constant("MAX_TEXTURE_UNITS_ARB")

    if OPENGL_1_4:
        constant("BLEND_DST_RGB")
        constant("BLEND_SRC_RGB")
        constant("BLEND_DST_ALPHA")
        constant("BLEND_SRC_ALPHA")
        constant("POINT_SIZE_MIN")
        constant("POINT_SIZE_MAX")
        constant("POINT_FADE_THRESHOLD_SIZE")
        constant("POINT_DISTANCE_ATTENUATION")
        constant("GENERATE_MIPMAP")
        constant("GENERATE_MIPMAP_HINT")
        constant("DEPTH_COMPONENT16")
        constant("DEPTH_COMPONENT24")
        constant("DEPTH_COMPONENT32")
        constant("MIRRORED_REPEAT")
        constant("FOG_COORDINATE_SOURCE")
        constant("FOG_COORDINATE")
        constant("FRAGMENT_DEPTH")
        constant("CURRENT_FOG_COORDINATE")
        constant("FOG_COORDINATE_ARRAY_TYPE")
        constant("FOG_COORDINATE_ARRAY_STRIDE")
        constant("FOG_COORDINATE_ARRAY_POINTER")
        constant("FOG_COORDINATE_ARRAY")
        constant("COLOR_SUM")
        constant("CURRENT_SECONDARY_COLOR")
        constant("SECONDARY_COLOR_ARRAY_SIZE")
        constant("SECONDARY_COLOR_ARRAY_TYPE")
        constant("SECONDARY_COLOR_ARRAY_STRIDE")
        constant("SECONDARY_COLOR_ARRAY_POINTER")
        constant("SECONDARY_COLOR_ARRAY")
        constant("MAX_TEXTURE_LOD_BIAS")
        constant("TEXTURE_FILTER_CONTROL")
        constant("TEXTURE_LOD_BIAS")
        constant("INCR_WRAP")
        constant("DECR_WRAP")
        constant("TEXTURE_DEPTH_SIZE")
        constant("DEPTH_TEXTURE_MODE")
        constant("TEXTURE_COMPARE_MODE")
        constant("TEXTURE_COMPARE_FUNC")
        constant("COMPARE_R_TO_TEXTURE")

    if OPENGL_1_5:
        constant("BUFFER_SIZE")
        constant("BUFFER_USAGE")
        constant("QUERY_COUNTER_BITS")
        constant("CURRENT_QUERY")
        constant("QUERY_RESULT")
        constant("QUERY_RESULT_AVAILABLE")
        constant("ARRAY_BUFFER")
        constant("ELEMENT_ARRAY_BUFFER")
        constant("ARRAY_BUFFER_BINDING")
        constant("ELEMENT_ARRAY_BUFFER_BINDING")
        constant("VERTEX_ARRAY_BUFFER_BINDING")
        constant("NORMAL_ARRAY_BUFFER_BINDING")
        constant("COLOR_ARRAY_BUFFER_BINDING")
        constant("INDEX_ARRAY_BUFFER_BINDING")
        constant("TEXTURE_COORD_ARRAY_BUFFER_BINDING")
        constant("EDGE_FLAG_ARRAY_BUFFER_BINDING")
        constant("SECONDARY_COLOR_ARRAY_BUFFER_BINDING")
        constant("FOG_COORDINATE_ARRAY_BUFFER_BINDING")
        constant("WEIGHT_ARRAY_BUFFER_BINDING")
        constant("VERTEX_ATTRIB_ARRAY_BUFFER_BINDING")
        constant("READ_ONLY")
        constant("WRITE_ONLY")
        constant("READ_WRITE")
        constant("BUFFER_ACCESS")
        constant("BUFFER_MAPPED")
        constant("BUFFER_MAP_POINTER")
        constant("STREAM_DRAW")
        constant("STREAM_READ")
        constant("STREAM_COPY")
        constant("STATIC_DRAW")
        constant("STATIC_READ")
        constant("STATIC_COPY")
        constant("DYNAMIC_DRAW")
        constant("DYNAMIC_READ")
        constant("DYNAMIC_COPY")
        constant("SAMPLES_PASSED")
        constant("FOG_COORD_SRC")
        constant("FOG_COORD")
        constant("CURRENT_FOG_COORD")
        constant("FOG_COORD_ARRAY_TYPE")
        constant("FOG_COORD_ARRAY_STRIDE")
        constant("FOG_COORD_ARRAY_POINTER")
        constant("FOG_COORD_ARRAY")
        constant("FOG_COORD_ARRAY_BUFFER_BINDING")
        constant("SRC0_RGB")
        constant("SRC1_RGB")
        constant("SRC2_RGB")
        constant("SRC0_ALPHA")
        constant("SRC1_ALPHA")
        constant("SRC2_ALPHA")

    if OPENGL_2_0:
        constant("BLEND_EQUATION_RGB")
        constant("VERTEX_ATTRIB_ARRAY_ENABLED")
        constant("VERTEX_ATTRIB_ARRAY_SIZE")
        constant("VERTEX_ATTRIB_ARRAY_STRIDE")
        constant("VERTEX_ATTRIB_ARRAY_TYPE")
        constant("CURRENT_VERTEX_ATTRIB")
        constant("VERTEX_PROGRAM_POINT_SIZE")
        constant("VERTEX_PROGRAM_TWO_SIDE")
        constant("VERTEX_ATTRIB_ARRAY_POINTER")
        constant("STENCIL_BACK_FUNC")
        constant("STENCIL_BACK_FAIL")
        constant("STENCIL_BACK_PASS_DEPTH_FAIL")
        constant("STENCIL_BACK_PASS_DEPTH_PASS")
        constant("MAX_DRAW_BUFFERS")
        constant("DRAW_BUFFER0")
        constant("DRAW_BUFFER1")
        constant("DRAW_BUFFER2")
        constant("DRAW_BUFFER3")
        constant("DRAW_BUFFER4")
        constant("DRAW_BUFFER5")
        constant("DRAW_BUFFER6")
        constant("DRAW_BUFFER7")
        constant("DRAW_BUFFER8")
        constant("DRAW_BUFFER9")
        constant("DRAW_BUFFER10")
        constant("DRAW_BUFFER11")
        constant("DRAW_BUFFER12")
        constant("DRAW_BUFFER13")
        constant("DRAW_BUFFER14")
        constant("DRAW_BUFFER15")
        constant("BLEND_EQUATION_ALPHA")
        constant("POINT_SPRITE")
        constant("COORD_REPLACE")
        constant("MAX_VERTEX_ATTRIBS")
        constant("VERTEX_ATTRIB_ARRAY_NORMALIZED")
        constant("MAX_TEXTURE_COORDS")
        constant("MAX_TEXTURE_IMAGE_UNITS")
        constant("FRAGMENT_SHADER")
        constant("VERTEX_SHADER")
        constant("MAX_FRAGMENT_UNIFORM_COMPONENTS")
        constant("MAX_VERTEX_UNIFORM_COMPONENTS")
        constant("MAX_VARYING_FLOATS")
        constant("MAX_VERTEX_TEXTURE_IMAGE_UNITS")
        constant("MAX_COMBINED_TEXTURE_IMAGE_UNITS")
        constant("SHADER_TYPE")
        constant("FLOAT_VEC2")
        constant("FLOAT_VEC3")
        constant("FLOAT_VEC4")
        constant("INT_VEC2")
        constant("INT_VEC3")
        constant("INT_VEC4")
        constant("BOOL")
        constant("BOOL_VEC2")
        constant("BOOL_VEC3")
        constant("BOOL_VEC4")
        constant("FLOAT_MAT2")
        constant("FLOAT_MAT3")
        constant("FLOAT_MAT4")
        constant("SAMPLER_1D")
        constant("SAMPLER_2D")
        constant("SAMPLER_3D")
        constant("SAMPLER_CUBE")
        constant("SAMPLER_1D_SHADOW")
        constant("SAMPLER_2D_SHADOW")
        constant("DELETE_STATUS")
        constant("COMPILE_STATUS")
        constant("LINK_STATUS")
        constant("VALIDATE_STATUS")
        constant("INFO_LOG_LENGTH")
        constant("ATTACHED_SHADERS")
        constant("ACTIVE_UNIFORMS")
        constant("ACTIVE_UNIFORM_MAX_LENGTH")
        constant("SHADER_SOURCE_LENGTH")
        constant("ACTIVE_ATTRIBUTES")
        constant("ACTIVE_ATTRIBUTE_MAX_LENGTH")
        constant("FRAGMENT_SHADER_DERIVATIVE_HINT")
        constant("SHADING_LANGUAGE_VERSION")
        constant("CURRENT_PROGRAM")
        constant("POINT_SPRITE_COORD_ORIGIN")
        constant("LOWER_LEFT")
        constant("UPPER_LEFT")
        constant("STENCIL_BACK_REF")
        constant("STENCIL_BACK_VALUE_MASK")
        constant("STENCIL_BACK_WRITEMASK")

    if OPENGL_2_1:
        constant("CURRENT_RASTER_SECONDARY_COLOR")
        constant("PIXEL_PACK_BUFFER")
        constant("PIXEL_UNPACK_BUFFER")
        constant("PIXEL_PACK_BUFFER_BINDING")
        constant("PIXEL_UNPACK_BUFFER_BINDING")
        constant("FLOAT_MAT2")
        constant("FLOAT_MAT2")
        constant("FLOAT_MAT3")
        constant("FLOAT_MAT3")
        constant("FLOAT_MAT4")
        constant("FLOAT_MAT4")
        constant("SRGB")
        constant("SRGB8")
        constant("SRGB_ALPHA")
        constant("SRGB8_ALPHA8")
        constant("SLUMINANCE_ALPHA")
        constant("SLUMINANCE8_ALPHA8")
        constant("SLUMINANCE")
        constant("SLUMINANCE8")
        constant("COMPRESSED_SRGB")
        constant("COMPRESSED_SRGB_ALPHA")
        constant("COMPRESSED_SLUMINANCE")
        constant("COMPRESSED_SLUMINANCE_ALPHA")

    if GL_ARB_TRANSPOSE_MATRIX:
        constant("TRANSPOSE_MODELVIEW_MATRIX_ARB")
        constant("TRANSPOSE_PROJECTION_MATRIX_ARB")
        constant("TRANSPOSE_TEXTURE_MATRIX_ARB")
        constant("TRANSPOSE_COLOR_MATRIX_ARB")

    if GL_ARB_MULTISAMPLE:
        constant("MULTISAMPLE_ARB")
        constant("SAMPLE_ALPHA_TO_COVERAGE_ARB")
        constant("SAMPLE_ALPHA_TO_ONE_ARB")
        constant("SAMPLE_COVERAGE_ARB")
        constant("SAMPLE_BUFFERS_ARB")
        constant("SAMPLES_ARB")
        constant("SAMPLE_COVERAGE_VALUE_ARB")
        constant("SAMPLE_COVERAGE_INVERT_ARB")
        constant("MULTISAMPLE_BIT_ARB")

    if GL_ARB_TEXTURE_CUBE_MAP:
        constant("NORMAL_MAP_ARB")
        constant("REFLECTION_MAP_ARB")
        constant("TEXTURE_CUBE_MAP_ARB")
        constant("TEXTURE_BINDING_CUBE_MAP_ARB")
        constant("TEXTURE_CUBE_MAP_POSITIVE_X_ARB")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_X_ARB")
        constant("TEXTURE_CUBE_MAP_POSITIVE_Y_ARB")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_Y_ARB")
        constant("TEXTURE_CUBE_MAP_POSITIVE_Z_ARB")
        constant("TEXTURE_CUBE_MAP_NEGATIVE_Z_ARB")
        constant("PROXY_TEXTURE_CUBE_MAP_ARB")
        constant("MAX_CUBE_MAP_TEXTURE_SIZE_ARB")

    if GL_ARB_TEXTURE_COMPRESSION:
        constant("COMPRESSED_ALPHA_ARB")
        constant("COMPRESSED_LUMINANCE_ARB")
        constant("COMPRESSED_LUMINANCE_ALPHA_ARB")
        constant("COMPRESSED_INTENSITY_ARB")
        constant("COMPRESSED_RGB_ARB")
        constant("COMPRESSED_RGBA_ARB")
        constant("TEXTURE_COMPRESSION_HINT_ARB")
        constant("TEXTURE_COMPRESSED_IMAGE_SIZE_ARB")
        constant("TEXTURE_COMPRESSED_ARB")
        constant("NUM_COMPRESSED_TEXTURE_FORMATS_ARB")
        constant("COMPRESSED_TEXTURE_FORMATS_ARB")

    if GL_ARB_TEXTURE_BORDER_CLAMP:
        constant("CLAMP_TO_BORDER_ARB")

    if GL_ARB_POINT_PARAMETERS:
        constant("POINT_SIZE_MIN_ARB")
        constant("POINT_SIZE_MAX_ARB")
        constant("POINT_FADE_THRESHOLD_SIZE_ARB")
        constant("POINT_DISTANCE_ATTENUATION_ARB")

    if GL_ARB_VERTEX_BLEND:
        constant("MAX_VERTEX_UNITS_ARB")
        constant("ACTIVE_VERTEX_UNITS_ARB")
        constant("WEIGHT_SUM_UNITY_ARB")
        constant("VERTEX_BLEND_ARB")
        constant("CURRENT_WEIGHT_ARB")
        constant("WEIGHT_ARRAY_TYPE_ARB")
        constant("WEIGHT_ARRAY_STRIDE_ARB")
        constant("WEIGHT_ARRAY_SIZE_ARB")
        constant("WEIGHT_ARRAY_POINTER_ARB")
        constant("WEIGHT_ARRAY_ARB")
        constant("MODELVIEW0_ARB")
        constant("MODELVIEW1_ARB")
        constant("MODELVIEW2_ARB")
        constant("MODELVIEW3_ARB")
        constant("MODELVIEW4_ARB")
        constant("MODELVIEW5_ARB")
        constant("MODELVIEW6_ARB")
        constant("MODELVIEW7_ARB")
        constant("MODELVIEW8_ARB")
        constant("MODELVIEW9_ARB")
        constant("MODELVIEW10_ARB")
        constant("MODELVIEW11_ARB")
        constant("MODELVIEW12_ARB")
        constant("MODELVIEW13_ARB")
        constant("MODELVIEW14_ARB")
        constant("MODELVIEW15_ARB")
        constant("MODELVIEW16_ARB")
        constant("MODELVIEW17_ARB")
        constant("MODELVIEW18_ARB")
        constant("MODELVIEW19_ARB")
        constant("MODELVIEW20_ARB")
        constant("MODELVIEW21_ARB")
        constant("MODELVIEW22_ARB")
        constant("MODELVIEW23_ARB")
        constant("MODELVIEW24_ARB")
        constant("MODELVIEW25_ARB")
        constant("MODELVIEW26_ARB")
        constant("MODELVIEW27_ARB")
        constant("MODELVIEW28_ARB")
        constant("MODELVIEW29_ARB")
        constant("MODELVIEW30_ARB")
        constant("MODELVIEW31_ARB")

    if GL_ARB_MATRIX_PALETTE:
        constant("MATRIX_PALETTE_ARB")
        constant("MAX_MATRIX_PALETTE_STACK_DEPTH_ARB")
        constant("MAX_PALETTE_MATRICES_ARB")
        constant("CURRENT_PALETTE_MATRIX_ARB")
        constant("MATRIX_INDEX_ARRAY_ARB")
        constant("CURRENT_MATRIX_INDEX_ARB")
        constant("MATRIX_INDEX_ARRAY_SIZE_ARB")
        constant("MATRIX_INDEX_ARRAY_TYPE_ARB")
        constant("MATRIX_INDEX_ARRAY_STRIDE_ARB")
        constant("MATRIX_INDEX_ARRAY_POINTER_ARB")

    if GL_ARB_TEXTURE_ENV_COMBINE:
        constant("COMBINE_ARB")
        constant("COMBINE_RGB_ARB")
        constant("COMBINE_ALPHA_ARB")
        constant("SOURCE0_RGB_ARB")
        constant("SOURCE1_RGB_ARB")
        constant("SOURCE2_RGB_ARB")
        constant("SOURCE0_ALPHA_ARB")
        constant("SOURCE1_ALPHA_ARB")
        constant("SOURCE2_ALPHA_ARB")
        constant("OPERAND0_RGB_ARB")
        constant("OPERAND1_RGB_ARB")
        constant("OPERAND2_RGB_ARB")
        constant("OPERAND0_ALPHA_ARB")
        constant("OPERAND1_ALPHA_ARB")
        constant("OPERAND2_ALPHA_ARB")
        constant("RGB_SCALE_ARB")
        constant("ADD_SIGNED_ARB")
        constant("INTERPOLATE_ARB")
        constant("SUBTRACT_ARB")
        constant("CONSTANT_ARB")
        constant("PRIMARY_COLOR_ARB")
        constant("PREVIOUS_ARB")

    if GL_ARB_TEXTURE_ENV_DOT3:
        constant("DOT3_RGB_ARB")
        constant("DOT3_RGBA_ARB")

    if GL_ARB_TEXTURE_MIRRORED_REPEAT:
        constant("MIRRORED_REPEAT_ARB")

    if GL_ARB_DEPTH_TEXTURE:
        constant("DEPTH_COMPONENT16_ARB")
        constant("DEPTH_COMPONENT24_ARB")
        constant("DEPTH_COMPONENT32_ARB")
        constant("TEXTURE_DEPTH_SIZE_ARB")
        constant("DEPTH_TEXTURE_MODE_ARB")

    if GL_ARB_SHADOW:
        constant("TEXTURE_COMPARE_MODE_ARB")
        constant("TEXTURE_COMPARE_FUNC_ARB")
        constant("COMPARE_R_TO_TEXTURE_ARB")

    if GL_ARB_SHADOW_AMBIENT:
        constant("TEXTURE_COMPARE_FAIL_VALUE_ARB")

    if GL_ARB_VERTEX_PROGRAM:
        constant("COLOR_SUM_ARB")
        constant("VERTEX_PROGRAM_ARB")
        constant("VERTEX_ATTRIB_ARRAY_ENABLED_ARB")
        constant("VERTEX_ATTRIB_ARRAY_SIZE_ARB")
        constant("VERTEX_ATTRIB_ARRAY_STRIDE_ARB")
        constant("VERTEX_ATTRIB_ARRAY_TYPE_ARB")
        constant("CURRENT_VERTEX_ATTRIB_ARB")
        constant("PROGRAM_LENGTH_ARB")
        constant("PROGRAM_STRING_ARB")
        constant("MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB")
        constant("MAX_PROGRAM_MATRICES_ARB")
        constant("CURRENT_MATRIX_STACK_DEPTH_ARB")
        constant("CURRENT_MATRIX_ARB")
        constant("VERTEX_PROGRAM_POINT_SIZE_ARB")
        constant("VERTEX_PROGRAM_TWO_SIDE_ARB")
        constant("VERTEX_ATTRIB_ARRAY_POINTER_ARB")
        constant("PROGRAM_ERROR_POSITION_ARB")
        constant("PROGRAM_BINDING_ARB")
        constant("MAX_VERTEX_ATTRIBS_ARB")
        constant("VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB")
        constant("PROGRAM_ERROR_STRING_ARB")
        constant("PROGRAM_FORMAT_ASCII_ARB")
        constant("PROGRAM_FORMAT_ARB")
        constant("PROGRAM_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_INSTRUCTIONS_ARB")
        constant("PROGRAM_NATIVE_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB")
        constant("PROGRAM_TEMPORARIES_ARB")
        constant("MAX_PROGRAM_TEMPORARIES_ARB")
        constant("PROGRAM_NATIVE_TEMPORARIES_ARB")
        constant("MAX_PROGRAM_NATIVE_TEMPORARIES_ARB")
        constant("PROGRAM_PARAMETERS_ARB")
        constant("MAX_PROGRAM_PARAMETERS_ARB")
        constant("PROGRAM_NATIVE_PARAMETERS_ARB")
        constant("MAX_PROGRAM_NATIVE_PARAMETERS_ARB")
        constant("PROGRAM_ATTRIBS_ARB")
        constant("MAX_PROGRAM_ATTRIBS_ARB")
        constant("PROGRAM_NATIVE_ATTRIBS_ARB")
        constant("MAX_PROGRAM_NATIVE_ATTRIBS_ARB")
        constant("PROGRAM_ADDRESS_REGISTERS_ARB")
        constant("MAX_PROGRAM_ADDRESS_REGISTERS_ARB")
        constant("PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB")
        constant("MAX_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB")
        constant("MAX_PROGRAM_LOCAL_PARAMETERS_ARB")
        constant("MAX_PROGRAM_ENV_PARAMETERS_ARB")
        constant("PROGRAM_UNDER_NATIVE_LIMITS_ARB")
        constant("TRANSPOSE_CURRENT_MATRIX_ARB")
        constant("MATRIX0_ARB")
        constant("MATRIX1_ARB")
        constant("MATRIX2_ARB")
        constant("MATRIX3_ARB")
        constant("MATRIX4_ARB")
        constant("MATRIX5_ARB")
        constant("MATRIX6_ARB")
        constant("MATRIX7_ARB")
        constant("MATRIX8_ARB")
        constant("MATRIX9_ARB")
        constant("MATRIX10_ARB")
        constant("MATRIX11_ARB")
        constant("MATRIX12_ARB")
        constant("MATRIX13_ARB")
        constant("MATRIX14_ARB")
        constant("MATRIX15_ARB")
        constant("MATRIX16_ARB")
        constant("MATRIX17_ARB")
        constant("MATRIX18_ARB")
        constant("MATRIX19_ARB")
        constant("MATRIX20_ARB")
        constant("MATRIX21_ARB")
        constant("MATRIX22_ARB")
        constant("MATRIX23_ARB")
        constant("MATRIX24_ARB")
        constant("MATRIX25_ARB")
        constant("MATRIX26_ARB")
        constant("MATRIX27_ARB")
        constant("MATRIX28_ARB")
        constant("MATRIX29_ARB")
        constant("MATRIX30_ARB")
        constant("MATRIX31_ARB")

    if GL_ARB_FRAGMENT_PROGRAM:
        constant("FRAGMENT_PROGRAM_ARB")
        constant("PROGRAM_ALU_INSTRUCTIONS_ARB")
        constant("PROGRAM_TEX_INSTRUCTIONS_ARB")
        constant("PROGRAM_TEX_INDIRECTIONS_ARB")
        constant("PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB")
        constant("PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB")
        constant("PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB")
        constant("MAX_PROGRAM_ALU_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_TEX_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_TEX_INDIRECTIONS_ARB")
        constant("MAX_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB")
        constant("MAX_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB")
        constant("MAX_TEXTURE_COORDS_ARB")
        constant("MAX_TEXTURE_IMAGE_UNITS_ARB")

    if GL_ARB_VERTEX_BUFFER_OBJECT:
        constant("BUFFER_SIZE_ARB")
        constant("BUFFER_USAGE_ARB")
        constant("ARRAY_BUFFER_ARB")
        constant("ELEMENT_ARRAY_BUFFER_ARB")
        constant("ARRAY_BUFFER_BINDING_ARB")
        constant("ELEMENT_ARRAY_BUFFER_BINDING_ARB")
        constant("VERTEX_ARRAY_BUFFER_BINDING_ARB")
        constant("NORMAL_ARRAY_BUFFER_BINDING_ARB")
        constant("COLOR_ARRAY_BUFFER_BINDING_ARB")
        constant("INDEX_ARRAY_BUFFER_BINDING_ARB")
        constant("TEXTURE_COORD_ARRAY_BUFFER_BINDING_ARB")
        constant("EDGE_FLAG_ARRAY_BUFFER_BINDING_ARB")
        constant("SECONDARY_COLOR_ARRAY_BUFFER_BINDING_ARB")
        constant("FOG_COORDINATE_ARRAY_BUFFER_BINDING_ARB")
        constant("WEIGHT_ARRAY_BUFFER_BINDING_ARB")
        constant("VERTEX_ATTRIB_ARRAY_BUFFER_BINDING_ARB")
        constant("READ_ONLY_ARB")
        constant("WRITE_ONLY_ARB")
        constant("READ_WRITE_ARB")
        constant("BUFFER_ACCESS_ARB")
        constant("BUFFER_MAPPED_ARB")
        constant("BUFFER_MAP_POINTER_ARB")
        constant("STREAM_DRAW_ARB")
        constant("STREAM_READ_ARB")
        constant("STREAM_COPY_ARB")
        constant("STATIC_DRAW_ARB")
        constant("STATIC_READ_ARB")
        constant("STATIC_COPY_ARB")
        constant("DYNAMIC_DRAW_ARB")
        constant("DYNAMIC_READ_ARB")
        constant("DYNAMIC_COPY_ARB")

    if GL_ARB_OCCLUSION_QUERY:
        constant("QUERY_COUNTER_BITS_ARB")
        constant("CURRENT_QUERY_ARB")
        constant("QUERY_RESULT_ARB")
        constant("QUERY_RESULT_AVAILABLE_ARB")
        constant("SAMPLES_PASSED_ARB")

    if GL_ARB_SHADER_OBJECTS:
        constant("PROGRAM_OBJECT_ARB")
        constant("SHADER_OBJECT_ARB")
        constant("OBJECT_TYPE_ARB")
        constant("OBJECT_SUBTYPE_ARB")
        constant("FLOAT_VEC2_ARB")
        constant("FLOAT_VEC3_ARB")
        constant("FLOAT_VEC4_ARB")
        constant("INT_VEC2_ARB")
        constant("INT_VEC3_ARB")
        constant("INT_VEC4_ARB")
        constant("BOOL_ARB")
        constant("BOOL_VEC2_ARB")
        constant("BOOL_VEC3_ARB")
        constant("BOOL_VEC4_ARB")
        constant("FLOAT_MAT2_ARB")
        constant("FLOAT_MAT3_ARB")
        constant("FLOAT_MAT4_ARB")
        constant("SAMPLER_1D_ARB")
        constant("SAMPLER_2D_ARB")
        constant("SAMPLER_3D_ARB")
        constant("SAMPLER_CUBE_ARB")
        constant("SAMPLER_1D_SHADOW_ARB")
        constant("SAMPLER_2D_SHADOW_ARB")
        constant("SAMPLER_2D_RECT_ARB")
        constant("SAMPLER_2D_RECT_SHADOW_ARB")
        constant("OBJECT_DELETE_STATUS_ARB")
        constant("OBJECT_COMPILE_STATUS_ARB")
        constant("OBJECT_LINK_STATUS_ARB")
        constant("OBJECT_VALIDATE_STATUS_ARB")
        constant("OBJECT_INFO_LOG_LENGTH_ARB")
        constant("OBJECT_ATTACHED_OBJECTS_ARB")
        constant("OBJECT_ACTIVE_UNIFORMS_ARB")
        constant("OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB")
        constant("OBJECT_SHADER_SOURCE_LENGTH_ARB")

    if GL_ARB_VERTEX_SHADER:
        constant("VERTEX_SHADER_ARB")
        constant("MAX_VERTEX_UNIFORM_COMPONENTS_ARB")
        constant("MAX_VARYING_FLOATS_ARB")
        constant("MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB")
        constant("MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB")
        constant("OBJECT_ACTIVE_ATTRIBUTES_ARB")
        constant("OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB")

    if GL_ARB_FRAGMENT_SHADER:
        constant("FRAGMENT_SHADER_ARB")
        constant("MAX_FRAGMENT_UNIFORM_COMPONENTS_ARB")
        constant("FRAGMENT_SHADER_DERIVATIVE_HINT_ARB")

    if GL_ARB_SHADING_LANGUAGE_100:
        constant("SHADING_LANGUAGE_VERSION_ARB")

    if GL_ARB_POINT_SPRITE:
        constant("POINT_SPRITE_ARB")
        constant("COORD_REPLACE_ARB")

    if GL_ARB_DRAW_BUFFERS:
        constant("MAX_DRAW_BUFFERS_ARB")
        constant("DRAW_BUFFER0_ARB")
        constant("DRAW_BUFFER1_ARB")
        constant("DRAW_BUFFER2_ARB")
        constant("DRAW_BUFFER3_ARB")
        constant("DRAW_BUFFER4_ARB")
        constant("DRAW_BUFFER5_ARB")
        constant("DRAW_BUFFER6_ARB")
        constant("DRAW_BUFFER7_ARB")
        constant("DRAW_BUFFER8_ARB")
        constant("DRAW_BUFFER9_ARB")
        constant("DRAW_BUFFER10_ARB")
        constant("DRAW_BUFFER11_ARB")
        constant("DRAW_BUFFER12_ARB")
        constant("DRAW_BUFFER13_ARB")
        constant("DRAW_BUFFER14_ARB")
        constant("DRAW_BUFFER15_ARB")

    if GL_ARB_TEXTURE_RECTANGLE:
        constant("TEXTURE_RECTANGLE_ARB")
        constant("TEXTURE_BINDING_RECTANGLE_ARB")
        constant("PROXY_TEXTURE_RECTANGLE_ARB")
        constant("MAX_RECTANGLE_TEXTURE_SIZE_ARB")

    if GL_ARB_COLOR_BUFFER_FLOAT:
        constant("RGBA_FLOAT_MODE_ARB")
        constant("CLAMP_VERTEX_COLOR_ARB")
        constant("CLAMP_FRAGMENT_COLOR_ARB")
        constant("CLAMP_READ_COLOR_ARB")
        constant("FIXED_ONLY_ARB")

    if GL_ARB_HALF_FLOAT_PIXEL:
        constant("HALF_FLOAT_ARB")

    if GL_ARB_TEXTURE_FLOAT:
        constant("TEXTURE_RED_TYPE_ARB")
        constant("TEXTURE_GREEN_TYPE_ARB")
        constant("TEXTURE_BLUE_TYPE_ARB")
        constant("TEXTURE_ALPHA_TYPE_ARB")
        constant("TEXTURE_LUMINANCE_TYPE_ARB")
        constant("TEXTURE_INTENSITY_TYPE_ARB")
        constant("TEXTURE_DEPTH_TYPE_ARB")
        constant("UNSIGNED_NORMALIZED_ARB")
        constant("RGBA32F_ARB")
        constant("RGB32F_ARB")
        constant("ALPHA32F_ARB")
        constant("INTENSITY32F_ARB")
        constant("LUMINANCE32F_ARB")
        constant("LUMINANCE_ALPHA32F_ARB")
        constant("RGBA16F_ARB")
        constant("RGB16F_ARB")
        constant("ALPHA16F_ARB")
        constant("INTENSITY16F_ARB")
        constant("LUMINANCE16F_ARB")
        constant("LUMINANCE_ALPHA16F_ARB")

    if GL_ARB_PIXEL_BUFFER_OBJECT:
        constant("PIXEL_PACK_BUFFER_ARB")
        constant("PIXEL_UNPACK_BUFFER_ARB")
        constant("PIXEL_PACK_BUFFER_BINDING_ARB")
        constant("PIXEL_UNPACK_BUFFER_BINDING_ARB")

    if GL_EXT_FRAMEBUFFER_OBJECT:
        declare(GLboolean, "IsRenderbufferEXT", GLuint)
        declare("BindRenderbufferEXT", GLenum, GLuint)
        declare("DeleteRenderbuffersEXT", GLsizei, GLuint[1])
        declare("GenRenderbuffersEXT", GLsizei, GLuint[1].asreturn())
        declare("RenderbufferStorageEXT", GLenum, GLenum, GLsizei, GLsizei)
        declare("GetRenderbufferParameterivEXT", GLenum, GLenum, GLint[1].asreturn())
        declare(GLboolean, "IsFramebufferEXT", GLuint)
        declare("BindFramebufferEXT", GLenum, GLuint)
        declare("DeleteFramebuffersEXT", GLsizei, GLuint[1])
        declare("GenFramebuffersEXT", GLsizei, GLuint[1].asreturn())
        declare(GLenum, "CheckFramebufferStatusEXT", GLenum)
        declare("FramebufferTexture1DEXT", GLenum, GLenum, GLenum, GLuint, GLint)
        declare("FramebufferTexture2DEXT", GLenum, GLenum, GLenum, GLuint, GLint)
        declare("FramebufferTexture3DEXT", GLenum, GLenum, GLenum, GLuint, GLint, GLint)
        declare("FramebufferRenderbufferEXT", GLenum, GLenum, GLenum, GLuint)
        declare("GetFramebufferAttachmentParameterivEXT", GLenum, GLenum, GLenum, GLint[1].asreturn())
        declare("GenerateMipmapEXT", GLenum)
        constant("FRAMEBUFFER_EXT")
        constant("RENDERBUFFER_EXT")
        constant("STENCIL_INDEX1_EXT")
        constant("STENCIL_INDEX4_EXT")
        constant("STENCIL_INDEX8_EXT")
        constant("STENCIL_INDEX16_EXT")
        constant("RENDERBUFFER_WIDTH_EXT")
        constant("RENDERBUFFER_HEIGHT_EXT")
        constant("RENDERBUFFER_INTERNAL_FORMAT_EXT")
        constant("RENDERBUFFER_RED_SIZE_EXT")
        constant("RENDERBUFFER_GREEN_SIZE_EXT")
        constant("RENDERBUFFER_BLUE_SIZE_EXT")
        constant("RENDERBUFFER_ALPHA_SIZE_EXT")
        constant("RENDERBUFFER_DEPTH_SIZE_EXT")
        constant("RENDERBUFFER_STENCIL_SIZE_EXT")
        constant("FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE_EXT")
        constant("FRAMEBUFFER_ATTACHMENT_OBJECT_NAME_EXT")
        constant("FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL_EXT")
        constant("FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE_EXT")
        constant("FRAMEBUFFER_ATTACHMENT_TEXTURE_3D_ZOFFSET_EXT")
        constant("COLOR_ATTACHMENT0_EXT")
        constant("COLOR_ATTACHMENT1_EXT")
        constant("COLOR_ATTACHMENT2_EXT")
        constant("COLOR_ATTACHMENT3_EXT")
        constant("COLOR_ATTACHMENT4_EXT")
        constant("COLOR_ATTACHMENT5_EXT")
        constant("COLOR_ATTACHMENT6_EXT")
        constant("COLOR_ATTACHMENT7_EXT")
        constant("COLOR_ATTACHMENT8_EXT")
        constant("COLOR_ATTACHMENT9_EXT")
        constant("COLOR_ATTACHMENT10_EXT")
        constant("COLOR_ATTACHMENT11_EXT")
        constant("COLOR_ATTACHMENT12_EXT")
        constant("COLOR_ATTACHMENT13_EXT")
        constant("COLOR_ATTACHMENT14_EXT")
        constant("COLOR_ATTACHMENT15_EXT")
        constant("DEPTH_ATTACHMENT_EXT")
        constant("STENCIL_ATTACHMENT_EXT")
        constant("FRAMEBUFFER_COMPLETE_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_FORMATS_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT")
        constant("FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT")
        constant("FRAMEBUFFER_UNSUPPORTED_EXT")
        constant("FRAMEBUFFER_BINDING_EXT")
        constant("RENDERBUFFER_BINDING_EXT")
        constant("MAX_COLOR_ATTACHMENTS_EXT")
        constant("MAX_RENDERBUFFER_SIZE_EXT")

    constant("INFO_LOG_LENGTH")


class gltype(object):

    def __init__(self, s):
        self.type = s

    def __getitem__(self, n):
        return gltype(self.type + " *")

    def asreturn(self):
        return self

    def __str__(self):
        return self.type


GLenum = gltype("GLenum")
GLboolean = gltype("GLboolean")
GLbitfield = gltype("GLbitfield")
GLvoid = gltype("GLvoid")
GLbyte = gltype("GLbyte")
GLshort = gltype("GLshort")
GLint = gltype("GLint")
GLubyte = gltype("GLubyte")
GLushort = gltype("GLushort")
GLuint = gltype("GLuint")
GLsizei = gltype("GLsizei")
GLfloat = gltype("GLfloat")
GLclampf = gltype("GLclampf")
GLdouble = gltype("GLdouble")
GLclampd = gltype("GLclampd")
GLbuffer = gltype("GLubyte *")
GLsizeiptrARB = gltype("GLsizeiptrARB")
GLintptrARB = gltype("GLintptrARB")
GLpointer = gltype("GLvoid *")
GLhandleARB = gltype("GLhandleARB")
GLstring = gltype("GLchar *")
GLcharARB = gltype("GLchar")


def exception_return(t):
    if "*" in str(t):
        return "NULL"
    else:
        return "0"


class GLFunction(object):

    def __init__(self, _type, name, args):
        self.type = _type
        self.name = name
        self.args = args

    def declare_external(self, f):

        print('    %s realGl%s "gl%s\" (%s)' % (
            self.type,
            self.name,
            self.name,
            ", ".join(str(i) for i in self.args)
            ), file=f)

    def declare_wrapper(self, f):
        t = self.type

        if t == GLvoid:
            t = "int"

        print('cdef %s gl%s(%s) except? %s' % (
            t,
            self.name,
            ", ".join(str(i) for i in self.args),
            exception_return(self.type),
            ), file=f)

    def define_wrapper(self, f):
        t = self.type

        if t == GLvoid:
            t = "int"

        print('cdef %s gl%s(%s) except? %s:' % (
            t,
            self.name,
            ", ".join(("%s a%d" % (t, i)) for i, t in enumerate(self.args)),
            exception_return(self.type),
            ), file=f)

        print("    if check_errors & 4:", file=f)
        print("        renpy.display.log.write('gl%s')" % self.name, file=f)

        print("    cdef GLenum error", file=f)

        if self.type == GLvoid:

            if self.name == "Clear":
                print("    with nogil:", file=f)
                prefix = "    "
            else:
                prefix = ""

            print(prefix + "    realGl%s(%s)" % (
                self.name,
                ", ".join(("a%d" % i) for i in range(len(self.args)))
                ), file=f)
        else:

            print("    cdef %s rv = realGl%s(%s)" % (
                self.type,
                self.name,
                ", ".join(("a%d" % i) for i in range(len(self.args)))
                ), file=f)

        print("    if check_errors:", file=f)
        print("        error = realGlGetError()", file=f)
        print("        if error:", file=f)
        print("            message = 'GL error %%x in gl%s' %% error" % self.name, file=f)
        print("            if check_errors & 1:", file=f)
        print("                renpy.display.log.write('%s', message)", file=f)
        print("            if check_errors & 2:", file=f)
        print("                raise Exception(message)", file=f)

        if self.type == GLvoid:
            print("    return 1", file=f)
        else:
            print("    return rv", file=f)


declarations = [ ]


def declare(*args):
    global is_enum
    is_enum = False

    args = list(args)

    if isinstance(args[0], gltype):
        type = args.pop(0)  # @ReservedAssignment
    else:
        type = GLvoid  # @ReservedAssignment

    name = args.pop(0)

    declarations.append(GLFunction(type, name, args))


constants = [ ]


def constant(name):
    constants.append("GL_" + name)


PXD_HEADER = """\
cdef extern from "glcompat.h" nogil:
    ctypedef unsigned int    GLenum
    ctypedef unsigned char   GLboolean
    ctypedef unsigned int    GLbitfield
    ctypedef void            GLvoid
    ctypedef signed char     GLbyte
    ctypedef short           GLshort
    ctypedef int             GLint
    ctypedef unsigned char   GLubyte
    ctypedef unsigned short  GLushort
    ctypedef unsigned int    GLuint
    ctypedef int             GLsizei
    ctypedef float           GLfloat
    ctypedef float           GLclampf
    ctypedef double          GLdouble
    ctypedef double          GLclampd
    ctypedef long int        GLsizeiptrARB
    ctypedef long int        GLintptrARB
    ctypedef unsigned int    GLhandleARB
    ctypedef unsigned int    GLhandle
    ctypedef char            GLchar
    ctypedef char            GLcharARB
"""

PYX_HEADER = """\
import os
import renpy

cdef int check_errors
check_errors = int(os.environ.get("RENPY_GL_CHECK_ERRORS", 0))
"""


def find_gl_names(dirname, gl1):

    names = set()

    for i in os.listdir(dirname):
        if not i.endswith('.pyx'):
            continue

        if i in [ "gl.pyx", "gl1.pyx" ]:
            continue

        GL1_FILES = [ "glenviron_fixed.pyx", "glenviron_limited.pyx" ]

        if gl1:
            if i not in GL1_FILES:
                continue
        else:
            if i in GL1_FILES:
                continue

        fn = os.path.join(dirname, i)

        with open(fn, "r") as f:
            data = f.read()

        for m in re.finditer(r'gl([A-Z]\w+)', data):
            names.add(m.group(1))

    rv = list(names)
    rv.sort()

    for i in rv:
        print(i)

    return rv


def generate(dirname, gl1):

    if gl1:
        prefix = "gl1"
    else:
        prefix = "gl"

    names = find_gl_names(dirname, gl1)

    global constants
    constants = [ ]

    global declarations
    declarations = [ ]

    generate_tegl()

    constant("BGRA")
    constants.sort()
    constants.append("RENPY_THIRD_TEXTURE")

    decl_by_name = dict((i.name, i) for i in declarations)

    with open(os.path.join(dirname, prefix + ".pxd"), "w") as f:
        print(PXD_HEADER, file=f)

        print(file=f)
        print("    enum:", file=f)
        for i in constants:
            print("        %s" % i, file=f)

        print(file=f)
        for i in declarations:
            i.declare_external(f)

        print(file=f)
        for i in names:
            decl_by_name[i].declare_wrapper(f)

    with open(os.path.join(dirname, prefix + ".pyx"), "w") as f:
        print(PYX_HEADER, file=f)

        for i in names:
            print(file=f)
            decl_by_name[i].define_wrapper(f)


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    generate(os.path.join(root, "renpy", "gl"), False)
    generate(os.path.join(root, "renpy", "gl"), True)
    generate(os.path.join(root, "renpy", "angle"), False)
