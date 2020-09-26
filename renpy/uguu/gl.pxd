from libc.stdint cimport int64_t, uint64_t
from libc.stddef cimport ptrdiff_t


cdef extern from "renpygl.h":

    ctypedef unsigned int GLenum
    ctypedef unsigned char GLboolean
    ctypedef unsigned int GLbitfield
    ctypedef void GLvoid
    ctypedef signed char GLbyte
    ctypedef short GLshort
    ctypedef int GLint
    ctypedef int GLclampx
    ctypedef unsigned char GLubyte
    ctypedef unsigned short GLushort
    ctypedef unsigned int GLuint
    ctypedef int GLsizei
    ctypedef float GLfloat
    ctypedef float GLclampf
    ctypedef double GLdouble
    ctypedef double GLclampd
    ctypedef void *GLeglClientBufferEXT
    ctypedef void *GLeglImageOES
    ctypedef char GLchar
    ctypedef char GLcharARB
    ctypedef unsigned short GLhalfARB
    ctypedef unsigned short GLhalf
    ctypedef GLint GLfixed
    ctypedef ptrdiff_t GLintptr
    ctypedef ptrdiff_t GLsizeiptr
    ctypedef int64_t GLint64
    ctypedef uint64_t GLuint64
    ctypedef ptrdiff_t GLintptrARB
    ctypedef ptrdiff_t GLsizeiptrARB
    ctypedef int64_t GLint64EXT
    ctypedef uint64_t GLuint64EXT

    GLenum GL_FALSE
    GLenum GL_NONE
    GLenum GL_NO_ERROR
    GLenum GL_POINTS
    GLenum GL_ZERO
    GLenum GL_LINES
    GLenum GL_MAP_READ_BIT
    GLenum GL_ONE
    GLenum GL_TRUE
    GLenum GL_LINE_LOOP
    GLenum GL_MAP_WRITE_BIT
    GLenum GL_LINE_STRIP
    GLenum GL_MAP_INVALIDATE_RANGE_BIT
    GLenum GL_TRIANGLES
    GLenum GL_TRIANGLE_STRIP
    GLenum GL_TRIANGLE_FAN
    GLenum GL_MAP_INVALIDATE_BUFFER_BIT
    GLenum GL_MAP_FLUSH_EXPLICIT_BIT
    GLenum GL_MAP_UNSYNCHRONIZED_BIT
    GLenum GL_DEPTH_BUFFER_BIT
    GLenum GL_NEVER
    GLenum GL_LESS
    GLenum GL_EQUAL
    GLenum GL_LEQUAL
    GLenum GL_GREATER
    GLenum GL_NOTEQUAL
    GLenum GL_GEQUAL
    GLenum GL_ALWAYS
    GLenum GL_SRC_COLOR
    GLenum GL_ONE_MINUS_SRC_COLOR
    GLenum GL_SRC_ALPHA
    GLenum GL_ONE_MINUS_SRC_ALPHA
    GLenum GL_DST_ALPHA
    GLenum GL_ONE_MINUS_DST_ALPHA
    GLenum GL_DST_COLOR
    GLenum GL_ONE_MINUS_DST_COLOR
    GLenum GL_SRC_ALPHA_SATURATE
    GLenum GL_STENCIL_BUFFER_BIT
    GLenum GL_FRONT
    GLenum GL_BACK
    GLenum GL_FRONT_AND_BACK
    GLenum GL_INVALID_ENUM
    GLenum GL_INVALID_VALUE
    GLenum GL_INVALID_OPERATION
    GLenum GL_OUT_OF_MEMORY
    GLenum GL_INVALID_FRAMEBUFFER_OPERATION
    GLenum GL_CW
    GLenum GL_CCW
    GLenum GL_LINE_WIDTH
    GLenum GL_CULL_FACE
    GLenum GL_CULL_FACE_MODE
    GLenum GL_FRONT_FACE
    GLenum GL_DEPTH_RANGE
    GLenum GL_DEPTH_TEST
    GLenum GL_DEPTH_WRITEMASK
    GLenum GL_DEPTH_CLEAR_VALUE
    GLenum GL_DEPTH_FUNC
    GLenum GL_STENCIL_TEST
    GLenum GL_STENCIL_CLEAR_VALUE
    GLenum GL_STENCIL_FUNC
    GLenum GL_STENCIL_VALUE_MASK
    GLenum GL_STENCIL_FAIL
    GLenum GL_STENCIL_PASS_DEPTH_FAIL
    GLenum GL_STENCIL_PASS_DEPTH_PASS
    GLenum GL_STENCIL_REF
    GLenum GL_STENCIL_WRITEMASK
    GLenum GL_VIEWPORT
    GLenum GL_DITHER
    GLenum GL_BLEND
    GLenum GL_READ_BUFFER
    GLenum GL_SCISSOR_BOX
    GLenum GL_SCISSOR_TEST
    GLenum GL_COLOR_CLEAR_VALUE
    GLenum GL_COLOR_WRITEMASK
    GLenum GL_UNPACK_ROW_LENGTH
    GLenum GL_UNPACK_SKIP_ROWS
    GLenum GL_UNPACK_SKIP_PIXELS
    GLenum GL_UNPACK_ALIGNMENT
    GLenum GL_PACK_ROW_LENGTH
    GLenum GL_PACK_SKIP_ROWS
    GLenum GL_PACK_SKIP_PIXELS
    GLenum GL_PACK_ALIGNMENT
    GLenum GL_MAX_TEXTURE_SIZE
    GLenum GL_MAX_VIEWPORT_DIMS
    GLenum GL_SUBPIXEL_BITS
    GLenum GL_RED_BITS
    GLenum GL_GREEN_BITS
    GLenum GL_BLUE_BITS
    GLenum GL_ALPHA_BITS
    GLenum GL_DEPTH_BITS
    GLenum GL_STENCIL_BITS
    GLenum GL_TEXTURE_2D
    GLenum GL_DONT_CARE
    GLenum GL_FASTEST
    GLenum GL_NICEST
    GLenum GL_BYTE
    GLenum GL_UNSIGNED_BYTE
    GLenum GL_SHORT
    GLenum GL_UNSIGNED_SHORT
    GLenum GL_INT
    GLenum GL_UNSIGNED_INT
    GLenum GL_FLOAT
    GLenum GL_HALF_FLOAT
    GLenum GL_INVERT
    GLenum GL_TEXTURE
    GLenum GL_COLOR
    GLenum GL_DEPTH
    GLenum GL_STENCIL
    GLenum GL_DEPTH_COMPONENT
    GLenum GL_RED
    GLenum GL_GREEN
    GLenum GL_BLUE
    GLenum GL_ALPHA
    GLenum GL_RGB
    GLenum GL_RGBA
    GLenum GL_LUMINANCE
    GLenum GL_LUMINANCE_ALPHA
    GLenum GL_KEEP
    GLenum GL_REPLACE
    GLenum GL_INCR
    GLenum GL_DECR
    GLenum GL_VENDOR
    GLenum GL_RENDERER
    GLenum GL_VERSION
    GLenum GL_EXTENSIONS
    GLenum GL_NEAREST
    GLenum GL_LINEAR
    GLenum GL_NEAREST_MIPMAP_NEAREST
    GLenum GL_LINEAR_MIPMAP_NEAREST
    GLenum GL_NEAREST_MIPMAP_LINEAR
    GLenum GL_LINEAR_MIPMAP_LINEAR
    GLenum GL_TEXTURE_MAG_FILTER
    GLenum GL_TEXTURE_MIN_FILTER
    GLenum GL_TEXTURE_WRAP_S
    GLenum GL_TEXTURE_WRAP_T
    GLenum GL_REPEAT
    GLenum GL_POLYGON_OFFSET_UNITS
    GLenum GL_COLOR_BUFFER_BIT
    GLenum GL_CONSTANT_COLOR
    GLenum GL_ONE_MINUS_CONSTANT_COLOR
    GLenum GL_CONSTANT_ALPHA
    GLenum GL_ONE_MINUS_CONSTANT_ALPHA
    GLenum GL_BLEND_COLOR
    GLenum GL_FUNC_ADD
    GLenum GL_MIN
    GLenum GL_MAX
    GLenum GL_BLEND_EQUATION
    GLenum GL_BLEND_EQUATION_RGB
    GLenum GL_FUNC_SUBTRACT
    GLenum GL_FUNC_REVERSE_SUBTRACT
    GLenum GL_UNSIGNED_SHORT_4_4_4_4
    GLenum GL_UNSIGNED_SHORT_5_5_5_1
    GLenum GL_POLYGON_OFFSET_FILL
    GLenum GL_POLYGON_OFFSET_FACTOR
    GLenum GL_RGB8
    GLenum GL_RGBA4
    GLenum GL_RGB5_A1
    GLenum GL_RGBA8
    GLenum GL_RGB10_A2
    GLenum GL_TEXTURE_BINDING_2D
    GLenum GL_TEXTURE_BINDING_3D
    GLenum GL_UNPACK_SKIP_IMAGES
    GLenum GL_UNPACK_IMAGE_HEIGHT
    GLenum GL_TEXTURE_3D
    GLenum GL_TEXTURE_WRAP_R
    GLenum GL_MAX_3D_TEXTURE_SIZE
    GLenum GL_SAMPLE_ALPHA_TO_COVERAGE
    GLenum GL_SAMPLE_COVERAGE
    GLenum GL_SAMPLE_BUFFERS
    GLenum GL_SAMPLES
    GLenum GL_SAMPLE_COVERAGE_VALUE
    GLenum GL_SAMPLE_COVERAGE_INVERT
    GLenum GL_BLEND_DST_RGB
    GLenum GL_BLEND_SRC_RGB
    GLenum GL_BLEND_DST_ALPHA
    GLenum GL_BLEND_SRC_ALPHA
    GLenum GL_MAX_ELEMENTS_VERTICES
    GLenum GL_MAX_ELEMENTS_INDICES
    GLenum GL_CLAMP_TO_EDGE
    GLenum GL_TEXTURE_MIN_LOD
    GLenum GL_TEXTURE_MAX_LOD
    GLenum GL_TEXTURE_BASE_LEVEL
    GLenum GL_TEXTURE_MAX_LEVEL
    GLenum GL_GENERATE_MIPMAP_HINT
    GLenum GL_DEPTH_COMPONENT16
    GLenum GL_DEPTH_COMPONENT24
    GLenum GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING
    GLenum GL_FRAMEBUFFER_ATTACHMENT_COMPONENT_TYPE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_STENCIL_SIZE
    GLenum GL_FRAMEBUFFER_DEFAULT
    GLenum GL_FRAMEBUFFER_UNDEFINED
    GLenum GL_DEPTH_STENCIL_ATTACHMENT
    GLenum GL_MAJOR_VERSION
    GLenum GL_MINOR_VERSION
    GLenum GL_NUM_EXTENSIONS
    GLenum GL_RG
    GLenum GL_RG_INTEGER
    GLenum GL_R8
    GLenum GL_RG8
    GLenum GL_R16F
    GLenum GL_R32F
    GLenum GL_RG16F
    GLenum GL_RG32F
    GLenum GL_R8I
    GLenum GL_R8UI
    GLenum GL_R16I
    GLenum GL_R16UI
    GLenum GL_R32I
    GLenum GL_R32UI
    GLenum GL_RG8I
    GLenum GL_RG8UI
    GLenum GL_RG16I
    GLenum GL_RG16UI
    GLenum GL_RG32I
    GLenum GL_RG32UI
    GLenum GL_UNSIGNED_SHORT_5_6_5
    GLenum GL_UNSIGNED_INT_2_10_10_10_REV
    GLenum GL_MIRRORED_REPEAT
    GLenum GL_ALIASED_POINT_SIZE_RANGE
    GLenum GL_ALIASED_LINE_WIDTH_RANGE
    GLenum GL_TEXTURE0
    GLenum GL_TEXTURE1
    GLenum GL_TEXTURE2
    GLenum GL_TEXTURE3
    GLenum GL_TEXTURE4
    GLenum GL_TEXTURE5
    GLenum GL_TEXTURE6
    GLenum GL_TEXTURE7
    GLenum GL_TEXTURE8
    GLenum GL_TEXTURE9
    GLenum GL_TEXTURE10
    GLenum GL_TEXTURE11
    GLenum GL_TEXTURE12
    GLenum GL_TEXTURE13
    GLenum GL_TEXTURE14
    GLenum GL_TEXTURE15
    GLenum GL_TEXTURE16
    GLenum GL_TEXTURE17
    GLenum GL_TEXTURE18
    GLenum GL_TEXTURE19
    GLenum GL_TEXTURE20
    GLenum GL_TEXTURE21
    GLenum GL_TEXTURE22
    GLenum GL_TEXTURE23
    GLenum GL_TEXTURE24
    GLenum GL_TEXTURE25
    GLenum GL_TEXTURE26
    GLenum GL_TEXTURE27
    GLenum GL_TEXTURE28
    GLenum GL_TEXTURE29
    GLenum GL_TEXTURE30
    GLenum GL_TEXTURE31
    GLenum GL_ACTIVE_TEXTURE
    GLenum GL_MAX_RENDERBUFFER_SIZE
    GLenum GL_DEPTH_STENCIL
    GLenum GL_UNSIGNED_INT_24_8
    GLenum GL_MAX_TEXTURE_LOD_BIAS
    GLenum GL_INCR_WRAP
    GLenum GL_DECR_WRAP
    GLenum GL_TEXTURE_CUBE_MAP
    GLenum GL_TEXTURE_BINDING_CUBE_MAP
    GLenum GL_TEXTURE_CUBE_MAP_POSITIVE_X
    GLenum GL_TEXTURE_CUBE_MAP_NEGATIVE_X
    GLenum GL_TEXTURE_CUBE_MAP_POSITIVE_Y
    GLenum GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
    GLenum GL_TEXTURE_CUBE_MAP_POSITIVE_Z
    GLenum GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
    GLenum GL_MAX_CUBE_MAP_TEXTURE_SIZE
    GLenum GL_VERTEX_ARRAY_BINDING
    GLenum GL_VERTEX_ATTRIB_ARRAY_ENABLED
    GLenum GL_VERTEX_ATTRIB_ARRAY_SIZE
    GLenum GL_VERTEX_ATTRIB_ARRAY_STRIDE
    GLenum GL_VERTEX_ATTRIB_ARRAY_TYPE
    GLenum GL_CURRENT_VERTEX_ATTRIB
    GLenum GL_VERTEX_ATTRIB_ARRAY_POINTER
    GLenum GL_NUM_COMPRESSED_TEXTURE_FORMATS
    GLenum GL_COMPRESSED_TEXTURE_FORMATS
    GLenum GL_BUFFER_SIZE
    GLenum GL_BUFFER_USAGE
    GLenum GL_STENCIL_BACK_FUNC
    GLenum GL_STENCIL_BACK_FAIL
    GLenum GL_STENCIL_BACK_PASS_DEPTH_FAIL
    GLenum GL_STENCIL_BACK_PASS_DEPTH_PASS
    GLenum GL_RGBA32F
    GLenum GL_RGB32F
    GLenum GL_RGBA16F
    GLenum GL_RGB16F
    GLenum GL_MAX_DRAW_BUFFERS
    GLenum GL_DRAW_BUFFER0
    GLenum GL_DRAW_BUFFER1
    GLenum GL_DRAW_BUFFER2
    GLenum GL_DRAW_BUFFER3
    GLenum GL_DRAW_BUFFER4
    GLenum GL_DRAW_BUFFER5
    GLenum GL_DRAW_BUFFER6
    GLenum GL_DRAW_BUFFER7
    GLenum GL_DRAW_BUFFER8
    GLenum GL_DRAW_BUFFER9
    GLenum GL_DRAW_BUFFER10
    GLenum GL_DRAW_BUFFER11
    GLenum GL_DRAW_BUFFER12
    GLenum GL_DRAW_BUFFER13
    GLenum GL_DRAW_BUFFER14
    GLenum GL_DRAW_BUFFER15
    GLenum GL_BLEND_EQUATION_ALPHA
    GLenum GL_TEXTURE_COMPARE_MODE
    GLenum GL_TEXTURE_COMPARE_FUNC
    GLenum GL_COMPARE_REF_TO_TEXTURE
    GLenum GL_CURRENT_QUERY
    GLenum GL_QUERY_RESULT
    GLenum GL_QUERY_RESULT_AVAILABLE
    GLenum GL_MAX_VERTEX_ATTRIBS
    GLenum GL_VERTEX_ATTRIB_ARRAY_NORMALIZED
    GLenum GL_MAX_TEXTURE_IMAGE_UNITS
    GLenum GL_ARRAY_BUFFER
    GLenum GL_ELEMENT_ARRAY_BUFFER
    GLenum GL_ARRAY_BUFFER_BINDING
    GLenum GL_ELEMENT_ARRAY_BUFFER_BINDING
    GLenum GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING
    GLenum GL_BUFFER_MAPPED
    GLenum GL_BUFFER_MAP_POINTER
    GLenum GL_STREAM_DRAW
    GLenum GL_STREAM_READ
    GLenum GL_STREAM_COPY
    GLenum GL_STATIC_DRAW
    GLenum GL_STATIC_READ
    GLenum GL_STATIC_COPY
    GLenum GL_DYNAMIC_DRAW
    GLenum GL_DYNAMIC_READ
    GLenum GL_DYNAMIC_COPY
    GLenum GL_PIXEL_PACK_BUFFER
    GLenum GL_PIXEL_UNPACK_BUFFER
    GLenum GL_PIXEL_PACK_BUFFER_BINDING
    GLenum GL_PIXEL_UNPACK_BUFFER_BINDING
    GLenum GL_DEPTH24_STENCIL8
    GLenum GL_VERTEX_ATTRIB_ARRAY_INTEGER
    GLenum GL_MAX_ARRAY_TEXTURE_LAYERS
    GLenum GL_MIN_PROGRAM_TEXEL_OFFSET
    GLenum GL_MAX_PROGRAM_TEXEL_OFFSET
    GLenum GL_FRAGMENT_SHADER
    GLenum GL_VERTEX_SHADER
    GLenum GL_MAX_FRAGMENT_UNIFORM_COMPONENTS
    GLenum GL_MAX_VERTEX_UNIFORM_COMPONENTS
    GLenum GL_MAX_VARYING_COMPONENTS
    GLenum GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS
    GLenum GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS
    GLenum GL_SHADER_TYPE
    GLenum GL_FLOAT_VEC2
    GLenum GL_FLOAT_VEC3
    GLenum GL_FLOAT_VEC4
    GLenum GL_INT_VEC2
    GLenum GL_INT_VEC3
    GLenum GL_INT_VEC4
    GLenum GL_BOOL
    GLenum GL_BOOL_VEC2
    GLenum GL_BOOL_VEC3
    GLenum GL_BOOL_VEC4
    GLenum GL_FLOAT_MAT2
    GLenum GL_FLOAT_MAT3
    GLenum GL_FLOAT_MAT4
    GLenum GL_SAMPLER_2D
    GLenum GL_SAMPLER_3D
    GLenum GL_SAMPLER_CUBE
    GLenum GL_SAMPLER_2D_SHADOW
    GLenum GL_FLOAT_MAT2x3
    GLenum GL_FLOAT_MAT2x4
    GLenum GL_FLOAT_MAT3x2
    GLenum GL_FLOAT_MAT3x4
    GLenum GL_FLOAT_MAT4x2
    GLenum GL_FLOAT_MAT4x3
    GLenum GL_DELETE_STATUS
    GLenum GL_COMPILE_STATUS
    GLenum GL_LINK_STATUS
    GLenum GL_VALIDATE_STATUS
    GLenum GL_INFO_LOG_LENGTH
    GLenum GL_ATTACHED_SHADERS
    GLenum GL_ACTIVE_UNIFORMS
    GLenum GL_ACTIVE_UNIFORM_MAX_LENGTH
    GLenum GL_SHADER_SOURCE_LENGTH
    GLenum GL_ACTIVE_ATTRIBUTES
    GLenum GL_ACTIVE_ATTRIBUTE_MAX_LENGTH
    GLenum GL_FRAGMENT_SHADER_DERIVATIVE_HINT
    GLenum GL_SHADING_LANGUAGE_VERSION
    GLenum GL_CURRENT_PROGRAM
    GLenum GL_UNSIGNED_NORMALIZED
    GLenum GL_TEXTURE_2D_ARRAY
    GLenum GL_TEXTURE_BINDING_2D_ARRAY
    GLenum GL_R11F_G11F_B10F
    GLenum GL_UNSIGNED_INT_10F_11F_11F_REV
    GLenum GL_RGB9_E5
    GLenum GL_UNSIGNED_INT_5_9_9_9_REV
    GLenum GL_SRGB
    GLenum GL_SRGB8
    GLenum GL_SRGB8_ALPHA8
    GLenum GL_TRANSFORM_FEEDBACK_VARYING_MAX_LENGTH
    GLenum GL_TRANSFORM_FEEDBACK_BUFFER_MODE
    GLenum GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS
    GLenum GL_TRANSFORM_FEEDBACK_VARYINGS
    GLenum GL_TRANSFORM_FEEDBACK_BUFFER_START
    GLenum GL_TRANSFORM_FEEDBACK_BUFFER_SIZE
    GLenum GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN
    GLenum GL_RASTERIZER_DISCARD
    GLenum GL_MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS
    GLenum GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS
    GLenum GL_INTERLEAVED_ATTRIBS
    GLenum GL_SEPARATE_ATTRIBS
    GLenum GL_TRANSFORM_FEEDBACK_BUFFER
    GLenum GL_TRANSFORM_FEEDBACK_BUFFER_BINDING
    GLenum GL_STENCIL_BACK_REF
    GLenum GL_STENCIL_BACK_VALUE_MASK
    GLenum GL_STENCIL_BACK_WRITEMASK
    GLenum GL_DRAW_FRAMEBUFFER_BINDING
    GLenum GL_FRAMEBUFFER_BINDING
    GLenum GL_RENDERBUFFER_BINDING
    GLenum GL_READ_FRAMEBUFFER
    GLenum GL_DRAW_FRAMEBUFFER
    GLenum GL_READ_FRAMEBUFFER_BINDING
    GLenum GL_RENDERBUFFER_SAMPLES
    GLenum GL_DEPTH_COMPONENT32F
    GLenum GL_DEPTH32F_STENCIL8
    GLenum GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME
    GLenum GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL
    GLenum GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE
    GLenum GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER
    GLenum GL_FRAMEBUFFER_COMPLETE
    GLenum GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT
    GLenum GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT
    GLenum GL_FRAMEBUFFER_UNSUPPORTED
    GLenum GL_MAX_COLOR_ATTACHMENTS
    GLenum GL_COLOR_ATTACHMENT0
    GLenum GL_COLOR_ATTACHMENT1
    GLenum GL_COLOR_ATTACHMENT2
    GLenum GL_COLOR_ATTACHMENT3
    GLenum GL_COLOR_ATTACHMENT4
    GLenum GL_COLOR_ATTACHMENT5
    GLenum GL_COLOR_ATTACHMENT6
    GLenum GL_COLOR_ATTACHMENT7
    GLenum GL_COLOR_ATTACHMENT8
    GLenum GL_COLOR_ATTACHMENT9
    GLenum GL_COLOR_ATTACHMENT10
    GLenum GL_COLOR_ATTACHMENT11
    GLenum GL_COLOR_ATTACHMENT12
    GLenum GL_COLOR_ATTACHMENT13
    GLenum GL_COLOR_ATTACHMENT14
    GLenum GL_COLOR_ATTACHMENT15
    GLenum GL_COLOR_ATTACHMENT16
    GLenum GL_COLOR_ATTACHMENT17
    GLenum GL_COLOR_ATTACHMENT18
    GLenum GL_COLOR_ATTACHMENT19
    GLenum GL_COLOR_ATTACHMENT20
    GLenum GL_COLOR_ATTACHMENT21
    GLenum GL_COLOR_ATTACHMENT22
    GLenum GL_COLOR_ATTACHMENT23
    GLenum GL_COLOR_ATTACHMENT24
    GLenum GL_COLOR_ATTACHMENT25
    GLenum GL_COLOR_ATTACHMENT26
    GLenum GL_COLOR_ATTACHMENT27
    GLenum GL_COLOR_ATTACHMENT28
    GLenum GL_COLOR_ATTACHMENT29
    GLenum GL_COLOR_ATTACHMENT30
    GLenum GL_COLOR_ATTACHMENT31
    GLenum GL_DEPTH_ATTACHMENT
    GLenum GL_STENCIL_ATTACHMENT
    GLenum GL_FRAMEBUFFER
    GLenum GL_RENDERBUFFER
    GLenum GL_RENDERBUFFER_WIDTH
    GLenum GL_RENDERBUFFER_HEIGHT
    GLenum GL_RENDERBUFFER_INTERNAL_FORMAT
    GLenum GL_STENCIL_INDEX8
    GLenum GL_RENDERBUFFER_RED_SIZE
    GLenum GL_RENDERBUFFER_GREEN_SIZE
    GLenum GL_RENDERBUFFER_BLUE_SIZE
    GLenum GL_RENDERBUFFER_ALPHA_SIZE
    GLenum GL_RENDERBUFFER_DEPTH_SIZE
    GLenum GL_RENDERBUFFER_STENCIL_SIZE
    GLenum GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE
    GLenum GL_MAX_SAMPLES
    GLenum GL_RGBA32UI
    GLenum GL_RGB32UI
    GLenum GL_RGBA16UI
    GLenum GL_RGB16UI
    GLenum GL_RGBA8UI
    GLenum GL_RGB8UI
    GLenum GL_RGBA32I
    GLenum GL_RGB32I
    GLenum GL_RGBA16I
    GLenum GL_RGB16I
    GLenum GL_RGBA8I
    GLenum GL_RGB8I
    GLenum GL_RED_INTEGER
    GLenum GL_RGB_INTEGER
    GLenum GL_RGBA_INTEGER
    GLenum GL_FLOAT_32_UNSIGNED_INT_24_8_REV
    GLenum GL_SAMPLER_2D_ARRAY
    GLenum GL_SAMPLER_2D_ARRAY_SHADOW
    GLenum GL_SAMPLER_CUBE_SHADOW
    GLenum GL_UNSIGNED_INT_VEC2
    GLenum GL_UNSIGNED_INT_VEC3
    GLenum GL_UNSIGNED_INT_VEC4
    GLenum GL_INT_SAMPLER_2D
    GLenum GL_INT_SAMPLER_3D
    GLenum GL_INT_SAMPLER_CUBE
    GLenum GL_INT_SAMPLER_2D_ARRAY
    GLenum GL_UNSIGNED_INT_SAMPLER_2D
    GLenum GL_UNSIGNED_INT_SAMPLER_3D
    GLenum GL_UNSIGNED_INT_SAMPLER_CUBE
    GLenum GL_UNSIGNED_INT_SAMPLER_2D_ARRAY
    GLenum GL_BUFFER_ACCESS_FLAGS
    GLenum GL_BUFFER_MAP_LENGTH
    GLenum GL_BUFFER_MAP_OFFSET

ctypedef void (__stdcall *glActiveTexture_type)(GLenum  texture) nogil
cdef glActiveTexture_type glActiveTexture

ctypedef void (__stdcall *glAttachShader_type)(GLuint  program, GLuint  shader) nogil
cdef glAttachShader_type glAttachShader

ctypedef void (__stdcall *glBeginQuery_type)(GLenum  target, GLuint  id) nogil
cdef glBeginQuery_type glBeginQuery

ctypedef void (__stdcall *glBeginTransformFeedback_type)(GLenum  primitiveMode) nogil
cdef glBeginTransformFeedback_type glBeginTransformFeedback

ctypedef void (__stdcall *glBindAttribLocation_type)(GLuint  program, GLuint  index, const GLchar * name) nogil
cdef glBindAttribLocation_type glBindAttribLocation

ctypedef void (__stdcall *glBindBuffer_type)(GLenum  target, GLuint  buffer) nogil
cdef glBindBuffer_type glBindBuffer

ctypedef void (__stdcall *glBindBufferBase_type)(GLenum  target, GLuint  index, GLuint  buffer) nogil
cdef glBindBufferBase_type glBindBufferBase

ctypedef void (__stdcall *glBindBufferRange_type)(GLenum  target, GLuint  index, GLuint  buffer, GLintptr  offset, GLsizeiptr  size) nogil
cdef glBindBufferRange_type glBindBufferRange

ctypedef void (__stdcall *glBindFramebuffer_type)(GLenum  target, GLuint  framebuffer) nogil
cdef glBindFramebuffer_type glBindFramebuffer

ctypedef void (__stdcall *glBindRenderbuffer_type)(GLenum  target, GLuint  renderbuffer) nogil
cdef glBindRenderbuffer_type glBindRenderbuffer

ctypedef void (__stdcall *glBindTexture_type)(GLenum  target, GLuint  texture) nogil
cdef glBindTexture_type glBindTexture

ctypedef void (__stdcall *glBindVertexArray_type)(GLuint  array) nogil
cdef glBindVertexArray_type glBindVertexArray

ctypedef void (__stdcall *glBlendColor_type)(GLfloat  red, GLfloat  green, GLfloat  blue, GLfloat  alpha) nogil
cdef glBlendColor_type glBlendColor

ctypedef void (__stdcall *glBlendEquation_type)(GLenum  mode) nogil
cdef glBlendEquation_type glBlendEquation

ctypedef void (__stdcall *glBlendEquationSeparate_type)(GLenum  modeRGB, GLenum  modeAlpha) nogil
cdef glBlendEquationSeparate_type glBlendEquationSeparate

ctypedef void (__stdcall *glBlendFunc_type)(GLenum  sfactor, GLenum  dfactor) nogil
cdef glBlendFunc_type glBlendFunc

ctypedef void (__stdcall *glBlendFuncSeparate_type)(GLenum  sfactorRGB, GLenum  dfactorRGB, GLenum  sfactorAlpha, GLenum  dfactorAlpha) nogil
cdef glBlendFuncSeparate_type glBlendFuncSeparate

ctypedef void (__stdcall *glBlitFramebuffer_type)(GLint  srcX0, GLint  srcY0, GLint  srcX1, GLint  srcY1, GLint  dstX0, GLint  dstY0, GLint  dstX1, GLint  dstY1, GLbitfield  mask, GLenum  filter) nogil
cdef glBlitFramebuffer_type glBlitFramebuffer

ctypedef void (__stdcall *glBufferData_type)(GLenum  target, GLsizeiptr  size, const void * data, GLenum  usage) nogil
cdef glBufferData_type glBufferData

ctypedef void (__stdcall *glBufferSubData_type)(GLenum  target, GLintptr  offset, GLsizeiptr  size, const void * data) nogil
cdef glBufferSubData_type glBufferSubData

ctypedef GLenum (__stdcall *glCheckFramebufferStatus_type)(GLenum  target) nogil
cdef glCheckFramebufferStatus_type glCheckFramebufferStatus

ctypedef void (__stdcall *glClear_type)(GLbitfield  mask) nogil
cdef glClear_type glClear

ctypedef void (__stdcall *glClearBufferfi_type)(GLenum  buffer, GLint  drawbuffer, GLfloat  depth, GLint  stencil) nogil
cdef glClearBufferfi_type glClearBufferfi

ctypedef void (__stdcall *glClearBufferfv_type)(GLenum  buffer, GLint  drawbuffer, const GLfloat * value) nogil
cdef glClearBufferfv_type glClearBufferfv

ctypedef void (__stdcall *glClearBufferiv_type)(GLenum  buffer, GLint  drawbuffer, const GLint * value) nogil
cdef glClearBufferiv_type glClearBufferiv

ctypedef void (__stdcall *glClearBufferuiv_type)(GLenum  buffer, GLint  drawbuffer, const GLuint * value) nogil
cdef glClearBufferuiv_type glClearBufferuiv

ctypedef void (__stdcall *glClearColor_type)(GLfloat  red, GLfloat  green, GLfloat  blue, GLfloat  alpha) nogil
cdef glClearColor_type glClearColor

ctypedef void (__stdcall *glClearStencil_type)(GLint  s) nogil
cdef glClearStencil_type glClearStencil

ctypedef void (__stdcall *glColorMask_type)(GLboolean  red, GLboolean  green, GLboolean  blue, GLboolean  alpha) nogil
cdef glColorMask_type glColorMask

ctypedef void (__stdcall *glCompileShader_type)(GLuint  shader) nogil
cdef glCompileShader_type glCompileShader

ctypedef void (__stdcall *glCompressedTexImage2D_type)(GLenum  target, GLint  level, GLenum  internalformat, GLsizei  width, GLsizei  height, GLint  border, GLsizei  imageSize, const void * data) nogil
cdef glCompressedTexImage2D_type glCompressedTexImage2D

ctypedef void (__stdcall *glCompressedTexImage3D_type)(GLenum  target, GLint  level, GLenum  internalformat, GLsizei  width, GLsizei  height, GLsizei  depth, GLint  border, GLsizei  imageSize, const void * data) nogil
cdef glCompressedTexImage3D_type glCompressedTexImage3D

ctypedef void (__stdcall *glCompressedTexSubImage2D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLsizei  width, GLsizei  height, GLenum  format, GLsizei  imageSize, const void * data) nogil
cdef glCompressedTexSubImage2D_type glCompressedTexSubImage2D

ctypedef void (__stdcall *glCompressedTexSubImage3D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLint  zoffset, GLsizei  width, GLsizei  height, GLsizei  depth, GLenum  format, GLsizei  imageSize, const void * data) nogil
cdef glCompressedTexSubImage3D_type glCompressedTexSubImage3D

ctypedef void (__stdcall *glCopyTexImage2D_type)(GLenum  target, GLint  level, GLenum  internalformat, GLint  x, GLint  y, GLsizei  width, GLsizei  height, GLint  border) nogil
cdef glCopyTexImage2D_type glCopyTexImage2D

ctypedef void (__stdcall *glCopyTexSubImage2D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil
cdef glCopyTexSubImage2D_type glCopyTexSubImage2D

ctypedef void (__stdcall *glCopyTexSubImage3D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLint  zoffset, GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil
cdef glCopyTexSubImage3D_type glCopyTexSubImage3D

ctypedef GLuint (__stdcall *glCreateProgram_type)() nogil
cdef glCreateProgram_type glCreateProgram

ctypedef GLuint (__stdcall *glCreateShader_type)(GLenum  type) nogil
cdef glCreateShader_type glCreateShader

ctypedef void (__stdcall *glCullFace_type)(GLenum  mode) nogil
cdef glCullFace_type glCullFace

ctypedef void (__stdcall *glDeleteBuffers_type)(GLsizei  n, const GLuint * buffers) nogil
cdef glDeleteBuffers_type glDeleteBuffers

ctypedef void (__stdcall *glDeleteFramebuffers_type)(GLsizei  n, const GLuint * framebuffers) nogil
cdef glDeleteFramebuffers_type glDeleteFramebuffers

ctypedef void (__stdcall *glDeleteProgram_type)(GLuint  program) nogil
cdef glDeleteProgram_type glDeleteProgram

ctypedef void (__stdcall *glDeleteQueries_type)(GLsizei  n, const GLuint * ids) nogil
cdef glDeleteQueries_type glDeleteQueries

ctypedef void (__stdcall *glDeleteRenderbuffers_type)(GLsizei  n, const GLuint * renderbuffers) nogil
cdef glDeleteRenderbuffers_type glDeleteRenderbuffers

ctypedef void (__stdcall *glDeleteShader_type)(GLuint  shader) nogil
cdef glDeleteShader_type glDeleteShader

ctypedef void (__stdcall *glDeleteTextures_type)(GLsizei  n, const GLuint * textures) nogil
cdef glDeleteTextures_type glDeleteTextures

ctypedef void (__stdcall *glDeleteVertexArrays_type)(GLsizei  n, const GLuint * arrays) nogil
cdef glDeleteVertexArrays_type glDeleteVertexArrays

ctypedef void (__stdcall *glDepthFunc_type)(GLenum  func) nogil
cdef glDepthFunc_type glDepthFunc

ctypedef void (__stdcall *glDepthMask_type)(GLboolean  flag) nogil
cdef glDepthMask_type glDepthMask

ctypedef void (__stdcall *glDetachShader_type)(GLuint  program, GLuint  shader) nogil
cdef glDetachShader_type glDetachShader

ctypedef void (__stdcall *glDisable_type)(GLenum  cap) nogil
cdef glDisable_type glDisable

ctypedef void (__stdcall *glDisableVertexAttribArray_type)(GLuint  index) nogil
cdef glDisableVertexAttribArray_type glDisableVertexAttribArray

ctypedef void (__stdcall *glDrawArrays_type)(GLenum  mode, GLint  first, GLsizei  count) nogil
cdef glDrawArrays_type glDrawArrays

ctypedef void (__stdcall *glDrawBuffers_type)(GLsizei  n, const GLenum * bufs) nogil
cdef glDrawBuffers_type glDrawBuffers

ctypedef void (__stdcall *glDrawElements_type)(GLenum  mode, GLsizei  count, GLenum  type, const void * indices) nogil
cdef glDrawElements_type glDrawElements

ctypedef void (__stdcall *glDrawRangeElements_type)(GLenum  mode, GLuint  start, GLuint  end, GLsizei  count, GLenum  type, const void * indices) nogil
cdef glDrawRangeElements_type glDrawRangeElements

ctypedef void (__stdcall *glEnable_type)(GLenum  cap) nogil
cdef glEnable_type glEnable

ctypedef void (__stdcall *glEnableVertexAttribArray_type)(GLuint  index) nogil
cdef glEnableVertexAttribArray_type glEnableVertexAttribArray

ctypedef void (__stdcall *glEndQuery_type)(GLenum  target) nogil
cdef glEndQuery_type glEndQuery

ctypedef void (__stdcall *glEndTransformFeedback_type)() nogil
cdef glEndTransformFeedback_type glEndTransformFeedback

ctypedef void (__stdcall *glFinish_type)() nogil
cdef glFinish_type glFinish

ctypedef void (__stdcall *glFlush_type)() nogil
cdef glFlush_type glFlush

ctypedef void (__stdcall *glFlushMappedBufferRange_type)(GLenum  target, GLintptr  offset, GLsizeiptr  length) nogil
cdef glFlushMappedBufferRange_type glFlushMappedBufferRange

ctypedef void (__stdcall *glFramebufferRenderbuffer_type)(GLenum  target, GLenum  attachment, GLenum  renderbuffertarget, GLuint  renderbuffer) nogil
cdef glFramebufferRenderbuffer_type glFramebufferRenderbuffer

ctypedef void (__stdcall *glFramebufferTexture2D_type)(GLenum  target, GLenum  attachment, GLenum  textarget, GLuint  texture, GLint  level) nogil
cdef glFramebufferTexture2D_type glFramebufferTexture2D

ctypedef void (__stdcall *glFramebufferTextureLayer_type)(GLenum  target, GLenum  attachment, GLuint  texture, GLint  level, GLint  layer) nogil
cdef glFramebufferTextureLayer_type glFramebufferTextureLayer

ctypedef void (__stdcall *glFrontFace_type)(GLenum  mode) nogil
cdef glFrontFace_type glFrontFace

ctypedef void (__stdcall *glGenBuffers_type)(GLsizei  n, GLuint * buffers) nogil
cdef glGenBuffers_type glGenBuffers

ctypedef void (__stdcall *glGenFramebuffers_type)(GLsizei  n, GLuint * framebuffers) nogil
cdef glGenFramebuffers_type glGenFramebuffers

ctypedef void (__stdcall *glGenQueries_type)(GLsizei  n, GLuint * ids) nogil
cdef glGenQueries_type glGenQueries

ctypedef void (__stdcall *glGenRenderbuffers_type)(GLsizei  n, GLuint * renderbuffers) nogil
cdef glGenRenderbuffers_type glGenRenderbuffers

ctypedef void (__stdcall *glGenTextures_type)(GLsizei  n, GLuint * textures) nogil
cdef glGenTextures_type glGenTextures

ctypedef void (__stdcall *glGenVertexArrays_type)(GLsizei  n, GLuint * arrays) nogil
cdef glGenVertexArrays_type glGenVertexArrays

ctypedef void (__stdcall *glGenerateMipmap_type)(GLenum  target) nogil
cdef glGenerateMipmap_type glGenerateMipmap

ctypedef void (__stdcall *glGetActiveAttrib_type)(GLuint  program, GLuint  index, GLsizei  bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name) nogil
cdef glGetActiveAttrib_type glGetActiveAttrib

ctypedef void (__stdcall *glGetActiveUniform_type)(GLuint  program, GLuint  index, GLsizei  bufSize, GLsizei * length, GLint * size, GLenum * type, GLchar * name) nogil
cdef glGetActiveUniform_type glGetActiveUniform

ctypedef void (__stdcall *glGetAttachedShaders_type)(GLuint  program, GLsizei  maxCount, GLsizei * count, GLuint * shaders) nogil
cdef glGetAttachedShaders_type glGetAttachedShaders

ctypedef GLint (__stdcall *glGetAttribLocation_type)(GLuint  program, const GLchar * name) nogil
cdef glGetAttribLocation_type glGetAttribLocation

ctypedef void (__stdcall *glGetBooleanv_type)(GLenum  pname, GLboolean * data) nogil
cdef glGetBooleanv_type glGetBooleanv

ctypedef void (__stdcall *glGetBufferParameteriv_type)(GLenum  target, GLenum  pname, GLint * params) nogil
cdef glGetBufferParameteriv_type glGetBufferParameteriv

ctypedef void (__stdcall *glGetBufferPointerv_type)(GLenum  target, GLenum  pname, void ** params) nogil
cdef glGetBufferPointerv_type glGetBufferPointerv

ctypedef GLenum (__stdcall *glGetError_type)() nogil
cdef glGetError_type glGetError

ctypedef void (__stdcall *glGetFloatv_type)(GLenum  pname, GLfloat * data) nogil
cdef glGetFloatv_type glGetFloatv

ctypedef GLint (__stdcall *glGetFragDataLocation_type)(GLuint  program, const GLchar * name) nogil
cdef glGetFragDataLocation_type glGetFragDataLocation

ctypedef void (__stdcall *glGetFramebufferAttachmentParameteriv_type)(GLenum  target, GLenum  attachment, GLenum  pname, GLint * params) nogil
cdef glGetFramebufferAttachmentParameteriv_type glGetFramebufferAttachmentParameteriv

ctypedef void (__stdcall *glGetIntegeri_v_type)(GLenum  target, GLuint  index, GLint * data) nogil
cdef glGetIntegeri_v_type glGetIntegeri_v

ctypedef void (__stdcall *glGetIntegerv_type)(GLenum  pname, GLint * data) nogil
cdef glGetIntegerv_type glGetIntegerv

ctypedef void (__stdcall *glGetProgramInfoLog_type)(GLuint  program, GLsizei  bufSize, GLsizei * length, GLchar * infoLog) nogil
cdef glGetProgramInfoLog_type glGetProgramInfoLog

ctypedef void (__stdcall *glGetProgramiv_type)(GLuint  program, GLenum  pname, GLint * params) nogil
cdef glGetProgramiv_type glGetProgramiv

ctypedef void (__stdcall *glGetQueryObjectuiv_type)(GLuint  id, GLenum  pname, GLuint * params) nogil
cdef glGetQueryObjectuiv_type glGetQueryObjectuiv

ctypedef void (__stdcall *glGetQueryiv_type)(GLenum  target, GLenum  pname, GLint * params) nogil
cdef glGetQueryiv_type glGetQueryiv

ctypedef void (__stdcall *glGetRenderbufferParameteriv_type)(GLenum  target, GLenum  pname, GLint * params) nogil
cdef glGetRenderbufferParameteriv_type glGetRenderbufferParameteriv

ctypedef void (__stdcall *glGetShaderInfoLog_type)(GLuint  shader, GLsizei  bufSize, GLsizei * length, GLchar * infoLog) nogil
cdef glGetShaderInfoLog_type glGetShaderInfoLog

ctypedef void (__stdcall *glGetShaderSource_type)(GLuint  shader, GLsizei  bufSize, GLsizei * length, GLchar * source) nogil
cdef glGetShaderSource_type glGetShaderSource

ctypedef void (__stdcall *glGetShaderiv_type)(GLuint  shader, GLenum  pname, GLint * params) nogil
cdef glGetShaderiv_type glGetShaderiv

ctypedef const GLubyte * (__stdcall *glGetString_type)(GLenum  name) nogil
cdef glGetString_type glGetString

ctypedef const GLubyte * (__stdcall *glGetStringi_type)(GLenum  name, GLuint  index) nogil
cdef glGetStringi_type glGetStringi

ctypedef void (__stdcall *glGetTexParameterfv_type)(GLenum  target, GLenum  pname, GLfloat * params) nogil
cdef glGetTexParameterfv_type glGetTexParameterfv

ctypedef void (__stdcall *glGetTexParameteriv_type)(GLenum  target, GLenum  pname, GLint * params) nogil
cdef glGetTexParameteriv_type glGetTexParameteriv

ctypedef void (__stdcall *glGetTransformFeedbackVarying_type)(GLuint  program, GLuint  index, GLsizei  bufSize, GLsizei * length, GLsizei * size, GLenum * type, GLchar * name) nogil
cdef glGetTransformFeedbackVarying_type glGetTransformFeedbackVarying

ctypedef GLint (__stdcall *glGetUniformLocation_type)(GLuint  program, const GLchar * name) nogil
cdef glGetUniformLocation_type glGetUniformLocation

ctypedef void (__stdcall *glGetUniformfv_type)(GLuint  program, GLint  location, GLfloat * params) nogil
cdef glGetUniformfv_type glGetUniformfv

ctypedef void (__stdcall *glGetUniformiv_type)(GLuint  program, GLint  location, GLint * params) nogil
cdef glGetUniformiv_type glGetUniformiv

ctypedef void (__stdcall *glGetUniformuiv_type)(GLuint  program, GLint  location, GLuint * params) nogil
cdef glGetUniformuiv_type glGetUniformuiv

ctypedef void (__stdcall *glGetVertexAttribIiv_type)(GLuint  index, GLenum  pname, GLint * params) nogil
cdef glGetVertexAttribIiv_type glGetVertexAttribIiv

ctypedef void (__stdcall *glGetVertexAttribIuiv_type)(GLuint  index, GLenum  pname, GLuint * params) nogil
cdef glGetVertexAttribIuiv_type glGetVertexAttribIuiv

ctypedef void (__stdcall *glGetVertexAttribPointerv_type)(GLuint  index, GLenum  pname, void ** pointer) nogil
cdef glGetVertexAttribPointerv_type glGetVertexAttribPointerv

ctypedef void (__stdcall *glGetVertexAttribfv_type)(GLuint  index, GLenum  pname, GLfloat * params) nogil
cdef glGetVertexAttribfv_type glGetVertexAttribfv

ctypedef void (__stdcall *glGetVertexAttribiv_type)(GLuint  index, GLenum  pname, GLint * params) nogil
cdef glGetVertexAttribiv_type glGetVertexAttribiv

ctypedef void (__stdcall *glHint_type)(GLenum  target, GLenum  mode) nogil
cdef glHint_type glHint

ctypedef GLboolean (__stdcall *glIsBuffer_type)(GLuint  buffer) nogil
cdef glIsBuffer_type glIsBuffer

ctypedef GLboolean (__stdcall *glIsEnabled_type)(GLenum  cap) nogil
cdef glIsEnabled_type glIsEnabled

ctypedef GLboolean (__stdcall *glIsFramebuffer_type)(GLuint  framebuffer) nogil
cdef glIsFramebuffer_type glIsFramebuffer

ctypedef GLboolean (__stdcall *glIsProgram_type)(GLuint  program) nogil
cdef glIsProgram_type glIsProgram

ctypedef GLboolean (__stdcall *glIsQuery_type)(GLuint  id) nogil
cdef glIsQuery_type glIsQuery

ctypedef GLboolean (__stdcall *glIsRenderbuffer_type)(GLuint  renderbuffer) nogil
cdef glIsRenderbuffer_type glIsRenderbuffer

ctypedef GLboolean (__stdcall *glIsShader_type)(GLuint  shader) nogil
cdef glIsShader_type glIsShader

ctypedef GLboolean (__stdcall *glIsTexture_type)(GLuint  texture) nogil
cdef glIsTexture_type glIsTexture

ctypedef GLboolean (__stdcall *glIsVertexArray_type)(GLuint  array) nogil
cdef glIsVertexArray_type glIsVertexArray

ctypedef void (__stdcall *glLineWidth_type)(GLfloat  width) nogil
cdef glLineWidth_type glLineWidth

ctypedef void (__stdcall *glLinkProgram_type)(GLuint  program) nogil
cdef glLinkProgram_type glLinkProgram

ctypedef void * (__stdcall *glMapBufferRange_type)(GLenum  target, GLintptr  offset, GLsizeiptr  length, GLbitfield  access) nogil
cdef glMapBufferRange_type glMapBufferRange

ctypedef void (__stdcall *glPixelStorei_type)(GLenum  pname, GLint  param) nogil
cdef glPixelStorei_type glPixelStorei

ctypedef void (__stdcall *glPolygonOffset_type)(GLfloat  factor, GLfloat  units) nogil
cdef glPolygonOffset_type glPolygonOffset

ctypedef void (__stdcall *glReadBuffer_type)(GLenum  src) nogil
cdef glReadBuffer_type glReadBuffer

ctypedef void (__stdcall *glReadPixels_type)(GLint  x, GLint  y, GLsizei  width, GLsizei  height, GLenum  format, GLenum  type, void * pixels) nogil
cdef glReadPixels_type glReadPixels

ctypedef void (__stdcall *glRenderbufferStorage_type)(GLenum  target, GLenum  internalformat, GLsizei  width, GLsizei  height) nogil
cdef glRenderbufferStorage_type glRenderbufferStorage

ctypedef void (__stdcall *glRenderbufferStorageMultisample_type)(GLenum  target, GLsizei  samples, GLenum  internalformat, GLsizei  width, GLsizei  height) nogil
cdef glRenderbufferStorageMultisample_type glRenderbufferStorageMultisample

ctypedef void (__stdcall *glSampleCoverage_type)(GLfloat  value, GLboolean  invert) nogil
cdef glSampleCoverage_type glSampleCoverage

ctypedef void (__stdcall *glScissor_type)(GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil
cdef glScissor_type glScissor

ctypedef void (__stdcall *glShaderSource_type)(GLuint  shader, GLsizei  count, const GLchar *const* string, const GLint * length) nogil
cdef glShaderSource_type glShaderSource

ctypedef void (__stdcall *glStencilFunc_type)(GLenum  func, GLint  ref, GLuint  mask) nogil
cdef glStencilFunc_type glStencilFunc

ctypedef void (__stdcall *glStencilFuncSeparate_type)(GLenum  face, GLenum  func, GLint  ref, GLuint  mask) nogil
cdef glStencilFuncSeparate_type glStencilFuncSeparate

ctypedef void (__stdcall *glStencilMask_type)(GLuint  mask) nogil
cdef glStencilMask_type glStencilMask

ctypedef void (__stdcall *glStencilMaskSeparate_type)(GLenum  face, GLuint  mask) nogil
cdef glStencilMaskSeparate_type glStencilMaskSeparate

ctypedef void (__stdcall *glStencilOp_type)(GLenum  fail, GLenum  zfail, GLenum  zpass) nogil
cdef glStencilOp_type glStencilOp

ctypedef void (__stdcall *glStencilOpSeparate_type)(GLenum  face, GLenum  sfail, GLenum  dpfail, GLenum  dppass) nogil
cdef glStencilOpSeparate_type glStencilOpSeparate

ctypedef void (__stdcall *glTexImage2D_type)(GLenum  target, GLint  level, GLint  internalformat, GLsizei  width, GLsizei  height, GLint  border, GLenum  format, GLenum  type, const void * pixels) nogil
cdef glTexImage2D_type glTexImage2D

ctypedef void (__stdcall *glTexImage3D_type)(GLenum  target, GLint  level, GLint  internalformat, GLsizei  width, GLsizei  height, GLsizei  depth, GLint  border, GLenum  format, GLenum  type, const void * pixels) nogil
cdef glTexImage3D_type glTexImage3D

ctypedef void (__stdcall *glTexParameterf_type)(GLenum  target, GLenum  pname, GLfloat  param) nogil
cdef glTexParameterf_type glTexParameterf

ctypedef void (__stdcall *glTexParameterfv_type)(GLenum  target, GLenum  pname, const GLfloat * params) nogil
cdef glTexParameterfv_type glTexParameterfv

ctypedef void (__stdcall *glTexParameteri_type)(GLenum  target, GLenum  pname, GLint  param) nogil
cdef glTexParameteri_type glTexParameteri

ctypedef void (__stdcall *glTexParameteriv_type)(GLenum  target, GLenum  pname, const GLint * params) nogil
cdef glTexParameteriv_type glTexParameteriv

ctypedef void (__stdcall *glTexSubImage2D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLsizei  width, GLsizei  height, GLenum  format, GLenum  type, const void * pixels) nogil
cdef glTexSubImage2D_type glTexSubImage2D

ctypedef void (__stdcall *glTexSubImage3D_type)(GLenum  target, GLint  level, GLint  xoffset, GLint  yoffset, GLint  zoffset, GLsizei  width, GLsizei  height, GLsizei  depth, GLenum  format, GLenum  type, const void * pixels) nogil
cdef glTexSubImage3D_type glTexSubImage3D

ctypedef void (__stdcall *glTransformFeedbackVaryings_type)(GLuint  program, GLsizei  count, const GLchar *const* varyings, GLenum  bufferMode) nogil
cdef glTransformFeedbackVaryings_type glTransformFeedbackVaryings

ctypedef void (__stdcall *glUniform1f_type)(GLint  location, GLfloat  v0) nogil
cdef glUniform1f_type glUniform1f

ctypedef void (__stdcall *glUniform1fv_type)(GLint  location, GLsizei  count, const GLfloat * value) nogil
cdef glUniform1fv_type glUniform1fv

ctypedef void (__stdcall *glUniform1i_type)(GLint  location, GLint  v0) nogil
cdef glUniform1i_type glUniform1i

ctypedef void (__stdcall *glUniform1iv_type)(GLint  location, GLsizei  count, const GLint * value) nogil
cdef glUniform1iv_type glUniform1iv

ctypedef void (__stdcall *glUniform1ui_type)(GLint  location, GLuint  v0) nogil
cdef glUniform1ui_type glUniform1ui

ctypedef void (__stdcall *glUniform1uiv_type)(GLint  location, GLsizei  count, const GLuint * value) nogil
cdef glUniform1uiv_type glUniform1uiv

ctypedef void (__stdcall *glUniform2f_type)(GLint  location, GLfloat  v0, GLfloat  v1) nogil
cdef glUniform2f_type glUniform2f

ctypedef void (__stdcall *glUniform2fv_type)(GLint  location, GLsizei  count, const GLfloat * value) nogil
cdef glUniform2fv_type glUniform2fv

ctypedef void (__stdcall *glUniform2i_type)(GLint  location, GLint  v0, GLint  v1) nogil
cdef glUniform2i_type glUniform2i

ctypedef void (__stdcall *glUniform2iv_type)(GLint  location, GLsizei  count, const GLint * value) nogil
cdef glUniform2iv_type glUniform2iv

ctypedef void (__stdcall *glUniform2ui_type)(GLint  location, GLuint  v0, GLuint  v1) nogil
cdef glUniform2ui_type glUniform2ui

ctypedef void (__stdcall *glUniform2uiv_type)(GLint  location, GLsizei  count, const GLuint * value) nogil
cdef glUniform2uiv_type glUniform2uiv

ctypedef void (__stdcall *glUniform3f_type)(GLint  location, GLfloat  v0, GLfloat  v1, GLfloat  v2) nogil
cdef glUniform3f_type glUniform3f

ctypedef void (__stdcall *glUniform3fv_type)(GLint  location, GLsizei  count, const GLfloat * value) nogil
cdef glUniform3fv_type glUniform3fv

ctypedef void (__stdcall *glUniform3i_type)(GLint  location, GLint  v0, GLint  v1, GLint  v2) nogil
cdef glUniform3i_type glUniform3i

ctypedef void (__stdcall *glUniform3iv_type)(GLint  location, GLsizei  count, const GLint * value) nogil
cdef glUniform3iv_type glUniform3iv

ctypedef void (__stdcall *glUniform3ui_type)(GLint  location, GLuint  v0, GLuint  v1, GLuint  v2) nogil
cdef glUniform3ui_type glUniform3ui

ctypedef void (__stdcall *glUniform3uiv_type)(GLint  location, GLsizei  count, const GLuint * value) nogil
cdef glUniform3uiv_type glUniform3uiv

ctypedef void (__stdcall *glUniform4f_type)(GLint  location, GLfloat  v0, GLfloat  v1, GLfloat  v2, GLfloat  v3) nogil
cdef glUniform4f_type glUniform4f

ctypedef void (__stdcall *glUniform4fv_type)(GLint  location, GLsizei  count, const GLfloat * value) nogil
cdef glUniform4fv_type glUniform4fv

ctypedef void (__stdcall *glUniform4i_type)(GLint  location, GLint  v0, GLint  v1, GLint  v2, GLint  v3) nogil
cdef glUniform4i_type glUniform4i

ctypedef void (__stdcall *glUniform4iv_type)(GLint  location, GLsizei  count, const GLint * value) nogil
cdef glUniform4iv_type glUniform4iv

ctypedef void (__stdcall *glUniform4ui_type)(GLint  location, GLuint  v0, GLuint  v1, GLuint  v2, GLuint  v3) nogil
cdef glUniform4ui_type glUniform4ui

ctypedef void (__stdcall *glUniform4uiv_type)(GLint  location, GLsizei  count, const GLuint * value) nogil
cdef glUniform4uiv_type glUniform4uiv

ctypedef void (__stdcall *glUniformMatrix2fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix2fv_type glUniformMatrix2fv

ctypedef void (__stdcall *glUniformMatrix2x3fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix2x3fv_type glUniformMatrix2x3fv

ctypedef void (__stdcall *glUniformMatrix2x4fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix2x4fv_type glUniformMatrix2x4fv

ctypedef void (__stdcall *glUniformMatrix3fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix3fv_type glUniformMatrix3fv

ctypedef void (__stdcall *glUniformMatrix3x2fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix3x2fv_type glUniformMatrix3x2fv

ctypedef void (__stdcall *glUniformMatrix3x4fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix3x4fv_type glUniformMatrix3x4fv

ctypedef void (__stdcall *glUniformMatrix4fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix4fv_type glUniformMatrix4fv

ctypedef void (__stdcall *glUniformMatrix4x2fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix4x2fv_type glUniformMatrix4x2fv

ctypedef void (__stdcall *glUniformMatrix4x3fv_type)(GLint  location, GLsizei  count, GLboolean  transpose, const GLfloat * value) nogil
cdef glUniformMatrix4x3fv_type glUniformMatrix4x3fv

ctypedef GLboolean (__stdcall *glUnmapBuffer_type)(GLenum  target) nogil
cdef glUnmapBuffer_type glUnmapBuffer

ctypedef void (__stdcall *glUseProgram_type)(GLuint  program) nogil
cdef glUseProgram_type glUseProgram

ctypedef void (__stdcall *glValidateProgram_type)(GLuint  program) nogil
cdef glValidateProgram_type glValidateProgram

ctypedef void (__stdcall *glVertexAttrib1f_type)(GLuint  index, GLfloat  x) nogil
cdef glVertexAttrib1f_type glVertexAttrib1f

ctypedef void (__stdcall *glVertexAttrib1fv_type)(GLuint  index, const GLfloat * v) nogil
cdef glVertexAttrib1fv_type glVertexAttrib1fv

ctypedef void (__stdcall *glVertexAttrib2f_type)(GLuint  index, GLfloat  x, GLfloat  y) nogil
cdef glVertexAttrib2f_type glVertexAttrib2f

ctypedef void (__stdcall *glVertexAttrib2fv_type)(GLuint  index, const GLfloat * v) nogil
cdef glVertexAttrib2fv_type glVertexAttrib2fv

ctypedef void (__stdcall *glVertexAttrib3f_type)(GLuint  index, GLfloat  x, GLfloat  y, GLfloat  z) nogil
cdef glVertexAttrib3f_type glVertexAttrib3f

ctypedef void (__stdcall *glVertexAttrib3fv_type)(GLuint  index, const GLfloat * v) nogil
cdef glVertexAttrib3fv_type glVertexAttrib3fv

ctypedef void (__stdcall *glVertexAttrib4f_type)(GLuint  index, GLfloat  x, GLfloat  y, GLfloat  z, GLfloat  w) nogil
cdef glVertexAttrib4f_type glVertexAttrib4f

ctypedef void (__stdcall *glVertexAttrib4fv_type)(GLuint  index, const GLfloat * v) nogil
cdef glVertexAttrib4fv_type glVertexAttrib4fv

ctypedef void (__stdcall *glVertexAttribI4i_type)(GLuint  index, GLint  x, GLint  y, GLint  z, GLint  w) nogil
cdef glVertexAttribI4i_type glVertexAttribI4i

ctypedef void (__stdcall *glVertexAttribI4iv_type)(GLuint  index, const GLint * v) nogil
cdef glVertexAttribI4iv_type glVertexAttribI4iv

ctypedef void (__stdcall *glVertexAttribI4ui_type)(GLuint  index, GLuint  x, GLuint  y, GLuint  z, GLuint  w) nogil
cdef glVertexAttribI4ui_type glVertexAttribI4ui

ctypedef void (__stdcall *glVertexAttribI4uiv_type)(GLuint  index, const GLuint * v) nogil
cdef glVertexAttribI4uiv_type glVertexAttribI4uiv

ctypedef void (__stdcall *glVertexAttribIPointer_type)(GLuint  index, GLint  size, GLenum  type, GLsizei  stride, const void * pointer) nogil
cdef glVertexAttribIPointer_type glVertexAttribIPointer

ctypedef void (__stdcall *glVertexAttribPointer_type)(GLuint  index, GLint  size, GLenum  type, GLboolean  normalized, GLsizei  stride, const void * pointer) nogil
cdef glVertexAttribPointer_type glVertexAttribPointer

ctypedef void (__stdcall *glViewport_type)(GLint  x, GLint  y, GLsizei  width, GLsizei  height) nogil
cdef glViewport_type glViewport
