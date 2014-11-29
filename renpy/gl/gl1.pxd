cdef extern from "glcompat.h":
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


    enum:
        GL_2D
        GL_2_BYTES
        GL_3D
        GL_3D_COLOR
        GL_3D_COLOR_TEXTURE
        GL_3_BYTES
        GL_4D_COLOR_TEXTURE
        GL_4_BYTES
        GL_ACCUM
        GL_ACCUM_ALPHA_BITS
        GL_ACCUM_BLUE_BITS
        GL_ACCUM_BUFFER_BIT
        GL_ACCUM_CLEAR_VALUE
        GL_ACCUM_GREEN_BITS
        GL_ACCUM_RED_BITS
        GL_ACTIVE_TEXTURE
        GL_ACTIVE_TEXTURE_ARB
        GL_ADD
        GL_ADD_SIGNED
        GL_ADD_SIGNED_ARB
        GL_ALIASED_LINE_WIDTH_RANGE
        GL_ALIASED_POINT_SIZE_RANGE
        GL_ALL_ATTRIB_BITS
        GL_ALPHA
        GL_ALPHA12
        GL_ALPHA16
        GL_ALPHA4
        GL_ALPHA8
        GL_ALPHA_BIAS
        GL_ALPHA_BITS
        GL_ALPHA_SCALE
        GL_ALPHA_TEST
        GL_ALPHA_TEST_FUNC
        GL_ALPHA_TEST_REF
        GL_ALWAYS
        GL_AMBIENT
        GL_AMBIENT_AND_DIFFUSE
        GL_AND
        GL_AND_INVERTED
        GL_AND_REVERSE
        GL_ARRAY_BUFFER_ARB
        GL_ARRAY_BUFFER_BINDING_ARB
        GL_ATTRIB_STACK_DEPTH
        GL_AUTO_NORMAL
        GL_AUX0
        GL_AUX1
        GL_AUX2
        GL_AUX3
        GL_AUX_BUFFERS
        GL_BACK
        GL_BACK_LEFT
        GL_BACK_RIGHT
        GL_BGR
        GL_BGRA
        GL_BGRA
        GL_BITMAP
        GL_BITMAP_TOKEN
        GL_BLEND
        GL_BLEND_DST
        GL_BLEND_SRC
        GL_BLUE
        GL_BLUE_BIAS
        GL_BLUE_BITS
        GL_BLUE_SCALE
        GL_BOOL_ARB
        GL_BOOL_VEC2_ARB
        GL_BOOL_VEC3_ARB
        GL_BOOL_VEC4_ARB
        GL_BUFFER_ACCESS_ARB
        GL_BUFFER_MAPPED_ARB
        GL_BUFFER_MAP_POINTER_ARB
        GL_BUFFER_SIZE_ARB
        GL_BUFFER_USAGE_ARB
        GL_BYTE
        GL_C3F_V3F
        GL_C4F_N3F_V3F
        GL_C4UB_V2F
        GL_C4UB_V3F
        GL_CCW
        GL_CLAMP
        GL_CLAMP_TO_BORDER
        GL_CLAMP_TO_EDGE
        GL_CLEAR
        GL_CLIENT_ACTIVE_TEXTURE
        GL_CLIENT_ACTIVE_TEXTURE_ARB
        GL_CLIENT_ALL_ATTRIB_BITS
        GL_CLIENT_ATTRIB_STACK_DEPTH
        GL_CLIENT_PIXEL_STORE_BIT
        GL_CLIENT_VERTEX_ARRAY_BIT
        GL_CLIP_PLANE0
        GL_CLIP_PLANE1
        GL_CLIP_PLANE2
        GL_CLIP_PLANE3
        GL_CLIP_PLANE4
        GL_CLIP_PLANE5
        GL_COEFF
        GL_COLOR
        GL_COLOR_ARRAY
        GL_COLOR_ARRAY_BUFFER_BINDING_ARB
        GL_COLOR_ARRAY_POINTER
        GL_COLOR_ARRAY_SIZE
        GL_COLOR_ARRAY_STRIDE
        GL_COLOR_ARRAY_TYPE
        GL_COLOR_ATTACHMENT0_EXT
        GL_COLOR_ATTACHMENT10_EXT
        GL_COLOR_ATTACHMENT11_EXT
        GL_COLOR_ATTACHMENT12_EXT
        GL_COLOR_ATTACHMENT13_EXT
        GL_COLOR_ATTACHMENT14_EXT
        GL_COLOR_ATTACHMENT15_EXT
        GL_COLOR_ATTACHMENT1_EXT
        GL_COLOR_ATTACHMENT2_EXT
        GL_COLOR_ATTACHMENT3_EXT
        GL_COLOR_ATTACHMENT4_EXT
        GL_COLOR_ATTACHMENT5_EXT
        GL_COLOR_ATTACHMENT6_EXT
        GL_COLOR_ATTACHMENT7_EXT
        GL_COLOR_ATTACHMENT8_EXT
        GL_COLOR_ATTACHMENT9_EXT
        GL_COLOR_BUFFER_BIT
        GL_COLOR_CLEAR_VALUE
        GL_COLOR_INDEX
        GL_COLOR_INDEXES
        GL_COLOR_LOGIC_OP
        GL_COLOR_MATERIAL
        GL_COLOR_MATERIAL_FACE
        GL_COLOR_MATERIAL_PARAMETER
        GL_COLOR_SUM_ARB
        GL_COLOR_WRITEMASK
        GL_COMBINE
        GL_COMBINE_ALPHA
        GL_COMBINE_ALPHA_ARB
        GL_COMBINE_ARB
        GL_COMBINE_RGB
        GL_COMBINE_RGB_ARB
        GL_COMPILE
        GL_COMPILE_AND_EXECUTE
        GL_COMPRESSED_ALPHA
        GL_COMPRESSED_INTENSITY
        GL_COMPRESSED_LUMINANCE
        GL_COMPRESSED_LUMINANCE_ALPHA
        GL_COMPRESSED_RGB
        GL_COMPRESSED_RGBA
        GL_COMPRESSED_TEXTURE_FORMATS
        GL_CONSTANT
        GL_CONSTANT_ARB
        GL_CONSTANT_ATTENUATION
        GL_COPY
        GL_COPY_INVERTED
        GL_COPY_PIXEL_TOKEN
        GL_CULL_FACE
        GL_CULL_FACE_MODE
        GL_CURRENT_BIT
        GL_CURRENT_COLOR
        GL_CURRENT_INDEX
        GL_CURRENT_MATRIX_ARB
        GL_CURRENT_MATRIX_STACK_DEPTH_ARB
        GL_CURRENT_NORMAL
        GL_CURRENT_RASTER_COLOR
        GL_CURRENT_RASTER_DISTANCE
        GL_CURRENT_RASTER_INDEX
        GL_CURRENT_RASTER_POSITION
        GL_CURRENT_RASTER_POSITION_VALID
        GL_CURRENT_RASTER_TEXTURE_COORDS
        GL_CURRENT_TEXTURE_COORDS
        GL_CURRENT_VERTEX_ATTRIB_ARB
        GL_CW
        GL_DECAL
        GL_DECR
        GL_DEPTH
        GL_DEPTH_ATTACHMENT_EXT
        GL_DEPTH_BIAS
        GL_DEPTH_BITS
        GL_DEPTH_BUFFER_BIT
        GL_DEPTH_CLEAR_VALUE
        GL_DEPTH_COMPONENT
        GL_DEPTH_FUNC
        GL_DEPTH_RANGE
        GL_DEPTH_SCALE
        GL_DEPTH_TEST
        GL_DEPTH_WRITEMASK
        GL_DIFFUSE
        GL_DITHER
        GL_DOMAIN
        GL_DONT_CARE
        GL_DOT3_RGB
        GL_DOT3_RGBA
        GL_DOUBLE
        GL_DOUBLEBUFFER
        GL_DRAW_BUFFER
        GL_DRAW_PIXEL_TOKEN
        GL_DST_ALPHA
        GL_DST_COLOR
        GL_DYNAMIC_COPY_ARB
        GL_DYNAMIC_DRAW_ARB
        GL_DYNAMIC_READ_ARB
        GL_EDGE_FLAG
        GL_EDGE_FLAG_ARRAY
        GL_EDGE_FLAG_ARRAY_BUFFER_BINDING_ARB
        GL_EDGE_FLAG_ARRAY_POINTER
        GL_EDGE_FLAG_ARRAY_STRIDE
        GL_ELEMENT_ARRAY_BUFFER_ARB
        GL_ELEMENT_ARRAY_BUFFER_BINDING_ARB
        GL_EMISSION
        GL_ENABLE_BIT
        GL_EQUAL
        GL_EQUIV
        GL_EVAL_BIT
        GL_EXP
        GL_EXP2
        GL_EXTENSIONS
        GL_EYE_LINEAR
        GL_EYE_PLANE
        GL_FALSE
        GL_FASTEST
        GL_FEEDBACK
        GL_FEEDBACK_BUFFER_POINTER
        GL_FEEDBACK_BUFFER_SIZE
        GL_FEEDBACK_BUFFER_TYPE
        GL_FILL
        GL_FLAT
        GL_FLOAT
        GL_FLOAT_MAT2_ARB
        GL_FLOAT_MAT3_ARB
        GL_FLOAT_MAT4_ARB
        GL_FLOAT_VEC2_ARB
        GL_FLOAT_VEC3_ARB
        GL_FLOAT_VEC4_ARB
        GL_FOG
        GL_FOG_BIT
        GL_FOG_COLOR
        GL_FOG_COORDINATE_ARRAY_BUFFER_BINDING_ARB
        GL_FOG_DENSITY
        GL_FOG_END
        GL_FOG_HINT
        GL_FOG_INDEX
        GL_FOG_MODE
        GL_FOG_START
        GL_FRAGMENT_PROGRAM_ARB
        GL_FRAGMENT_SHADER_ARB
        GL_FRAGMENT_SHADER_DERIVATIVE_HINT_ARB
        GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME_EXT
        GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_3D_ZOFFSET_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE_EXT
        GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL_EXT
        GL_FRAMEBUFFER_BINDING_EXT
        GL_FRAMEBUFFER_COMPLETE_EXT
        GL_FRAMEBUFFER_EXT
        GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT
        GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT
        GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT
        GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT
        GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT
        GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT
        GL_FRAMEBUFFER_UNSUPPORTED_EXT
        GL_FRONT
        GL_FRONT_AND_BACK
        GL_FRONT_FACE
        GL_FRONT_LEFT
        GL_FRONT_RIGHT
        GL_GEQUAL
        GL_GREATER
        GL_GREEN
        GL_GREEN_BIAS
        GL_GREEN_BITS
        GL_GREEN_SCALE
        GL_HINT_BIT
        GL_INCR
        GL_INDEX_ARRAY
        GL_INDEX_ARRAY_BUFFER_BINDING_ARB
        GL_INDEX_ARRAY_POINTER
        GL_INDEX_ARRAY_STRIDE
        GL_INDEX_ARRAY_TYPE
        GL_INDEX_BITS
        GL_INDEX_CLEAR_VALUE
        GL_INDEX_LOGIC_OP
        GL_INDEX_MODE
        GL_INDEX_OFFSET
        GL_INDEX_SHIFT
        GL_INDEX_WRITEMASK
        GL_INFO_LOG_LENGTH
        GL_INT
        GL_INTENSITY
        GL_INTENSITY12
        GL_INTENSITY16
        GL_INTENSITY4
        GL_INTENSITY8
        GL_INTERPOLATE
        GL_INTERPOLATE_ARB
        GL_INT_VEC2_ARB
        GL_INT_VEC3_ARB
        GL_INT_VEC4_ARB
        GL_INVALID_ENUM
        GL_INVALID_OPERATION
        GL_INVALID_VALUE
        GL_INVERT
        GL_KEEP
        GL_LEFT
        GL_LEQUAL
        GL_LESS
        GL_LIGHT0
        GL_LIGHT1
        GL_LIGHT2
        GL_LIGHT3
        GL_LIGHT4
        GL_LIGHT5
        GL_LIGHT6
        GL_LIGHT7
        GL_LIGHTING
        GL_LIGHTING_BIT
        GL_LIGHT_MODEL_AMBIENT
        GL_LIGHT_MODEL_COLOR_CONTROL
        GL_LIGHT_MODEL_LOCAL_VIEWER
        GL_LIGHT_MODEL_TWO_SIDE
        GL_LINE
        GL_LINEAR
        GL_LINEAR_ATTENUATION
        GL_LINEAR_MIPMAP_LINEAR
        GL_LINEAR_MIPMAP_NEAREST
        GL_LINES
        GL_LINE_BIT
        GL_LINE_LOOP
        GL_LINE_RESET_TOKEN
        GL_LINE_SMOOTH
        GL_LINE_SMOOTH_HINT
        GL_LINE_STIPPLE
        GL_LINE_STIPPLE_PATTERN
        GL_LINE_STIPPLE_REPEAT
        GL_LINE_STRIP
        GL_LINE_TOKEN
        GL_LINE_WIDTH
        GL_LINE_WIDTH_GRANULARITY
        GL_LINE_WIDTH_RANGE
        GL_LIST_BASE
        GL_LIST_BIT
        GL_LIST_INDEX
        GL_LIST_MODE
        GL_LOAD
        GL_LOGIC_OP
        GL_LOGIC_OP_MODE
        GL_LUMINANCE
        GL_LUMINANCE12
        GL_LUMINANCE12_ALPHA12
        GL_LUMINANCE12_ALPHA4
        GL_LUMINANCE16
        GL_LUMINANCE16_ALPHA16
        GL_LUMINANCE4
        GL_LUMINANCE4_ALPHA4
        GL_LUMINANCE6_ALPHA2
        GL_LUMINANCE8
        GL_LUMINANCE8_ALPHA8
        GL_LUMINANCE_ALPHA
        GL_MAP1_COLOR_4
        GL_MAP1_GRID_DOMAIN
        GL_MAP1_GRID_SEGMENTS
        GL_MAP1_INDEX
        GL_MAP1_NORMAL
        GL_MAP1_TEXTURE_COORD_1
        GL_MAP1_TEXTURE_COORD_2
        GL_MAP1_TEXTURE_COORD_3
        GL_MAP1_TEXTURE_COORD_4
        GL_MAP1_VERTEX_3
        GL_MAP1_VERTEX_4
        GL_MAP2_COLOR_4
        GL_MAP2_GRID_DOMAIN
        GL_MAP2_GRID_SEGMENTS
        GL_MAP2_INDEX
        GL_MAP2_NORMAL
        GL_MAP2_TEXTURE_COORD_1
        GL_MAP2_TEXTURE_COORD_2
        GL_MAP2_TEXTURE_COORD_3
        GL_MAP2_TEXTURE_COORD_4
        GL_MAP2_VERTEX_3
        GL_MAP2_VERTEX_4
        GL_MAP_COLOR
        GL_MAP_STENCIL
        GL_MATRIX0_ARB
        GL_MATRIX10_ARB
        GL_MATRIX11_ARB
        GL_MATRIX12_ARB
        GL_MATRIX13_ARB
        GL_MATRIX14_ARB
        GL_MATRIX15_ARB
        GL_MATRIX16_ARB
        GL_MATRIX17_ARB
        GL_MATRIX18_ARB
        GL_MATRIX19_ARB
        GL_MATRIX1_ARB
        GL_MATRIX20_ARB
        GL_MATRIX21_ARB
        GL_MATRIX22_ARB
        GL_MATRIX23_ARB
        GL_MATRIX24_ARB
        GL_MATRIX25_ARB
        GL_MATRIX26_ARB
        GL_MATRIX27_ARB
        GL_MATRIX28_ARB
        GL_MATRIX29_ARB
        GL_MATRIX2_ARB
        GL_MATRIX30_ARB
        GL_MATRIX31_ARB
        GL_MATRIX3_ARB
        GL_MATRIX4_ARB
        GL_MATRIX5_ARB
        GL_MATRIX6_ARB
        GL_MATRIX7_ARB
        GL_MATRIX8_ARB
        GL_MATRIX9_ARB
        GL_MATRIX_MODE
        GL_MAX_3D_TEXTURE_SIZE
        GL_MAX_ATTRIB_STACK_DEPTH
        GL_MAX_CLIENT_ATTRIB_STACK_DEPTH
        GL_MAX_CLIP_PLANES
        GL_MAX_COLOR_ATTACHMENTS_EXT
        GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_CUBE_MAP_TEXTURE_SIZE
        GL_MAX_ELEMENTS_INDICES
        GL_MAX_ELEMENTS_VERTICES
        GL_MAX_EVAL_ORDER
        GL_MAX_FRAGMENT_UNIFORM_COMPONENTS_ARB
        GL_MAX_LIGHTS
        GL_MAX_LIST_NESTING
        GL_MAX_MODELVIEW_STACK_DEPTH
        GL_MAX_NAME_STACK_DEPTH
        GL_MAX_PIXEL_MAP_TABLE
        GL_MAX_PROGRAM_ADDRESS_REGISTERS_ARB
        GL_MAX_PROGRAM_ALU_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_ATTRIBS_ARB
        GL_MAX_PROGRAM_ENV_PARAMETERS_ARB
        GL_MAX_PROGRAM_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB
        GL_MAX_PROGRAM_MATRICES_ARB
        GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB
        GL_MAX_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB
        GL_MAX_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB
        GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB
        GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB
        GL_MAX_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB
        GL_MAX_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB
        GL_MAX_PROGRAM_PARAMETERS_ARB
        GL_MAX_PROGRAM_TEMPORARIES_ARB
        GL_MAX_PROGRAM_TEX_INDIRECTIONS_ARB
        GL_MAX_PROGRAM_TEX_INSTRUCTIONS_ARB
        GL_MAX_PROJECTION_STACK_DEPTH
        GL_MAX_RENDERBUFFER_SIZE_EXT
        GL_MAX_TEXTURE_COORDS_ARB
        GL_MAX_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_TEXTURE_SIZE
        GL_MAX_TEXTURE_STACK_DEPTH
        GL_MAX_TEXTURE_UNITS
        GL_MAX_TEXTURE_UNITS_ARB
        GL_MAX_VARYING_FLOATS_ARB
        GL_MAX_VERTEX_ATTRIBS_ARB
        GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB
        GL_MAX_VERTEX_UNIFORM_COMPONENTS_ARB
        GL_MAX_VIEWPORT_DIMS
        GL_MODELVIEW
        GL_MODELVIEW_MATRIX
        GL_MODELVIEW_STACK_DEPTH
        GL_MODULATE
        GL_MULT
        GL_MULTISAMPLE
        GL_MULTISAMPLE_BIT
        GL_N3F_V3F
        GL_NAME_STACK_DEPTH
        GL_NAND
        GL_NEAREST
        GL_NEAREST_MIPMAP_LINEAR
        GL_NEAREST_MIPMAP_NEAREST
        GL_NEVER
        GL_NICEST
        GL_NONE
        GL_NOOP
        GL_NOR
        GL_NORMALIZE
        GL_NORMAL_ARRAY
        GL_NORMAL_ARRAY_BUFFER_BINDING_ARB
        GL_NORMAL_ARRAY_POINTER
        GL_NORMAL_ARRAY_STRIDE
        GL_NORMAL_ARRAY_TYPE
        GL_NORMAL_MAP
        GL_NOTEQUAL
        GL_NO_ERROR
        GL_NUM_COMPRESSED_TEXTURE_FORMATS
        GL_OBJECT_ACTIVE_ATTRIBUTES_ARB
        GL_OBJECT_ACTIVE_ATTRIBUTE_MAX_LENGTH_ARB
        GL_OBJECT_ACTIVE_UNIFORMS_ARB
        GL_OBJECT_ACTIVE_UNIFORM_MAX_LENGTH_ARB
        GL_OBJECT_ATTACHED_OBJECTS_ARB
        GL_OBJECT_COMPILE_STATUS_ARB
        GL_OBJECT_DELETE_STATUS_ARB
        GL_OBJECT_INFO_LOG_LENGTH_ARB
        GL_OBJECT_LINEAR
        GL_OBJECT_LINK_STATUS_ARB
        GL_OBJECT_PLANE
        GL_OBJECT_SHADER_SOURCE_LENGTH_ARB
        GL_OBJECT_SUBTYPE_ARB
        GL_OBJECT_TYPE_ARB
        GL_OBJECT_VALIDATE_STATUS_ARB
        GL_ONE
        GL_ONE_MINUS_DST_ALPHA
        GL_ONE_MINUS_DST_COLOR
        GL_ONE_MINUS_SRC_ALPHA
        GL_ONE_MINUS_SRC_COLOR
        GL_OPERAND0_ALPHA
        GL_OPERAND0_ALPHA_ARB
        GL_OPERAND0_RGB
        GL_OPERAND0_RGB_ARB
        GL_OPERAND1_ALPHA
        GL_OPERAND1_ALPHA_ARB
        GL_OPERAND1_RGB
        GL_OPERAND1_RGB_ARB
        GL_OPERAND2_ALPHA
        GL_OPERAND2_ALPHA_ARB
        GL_OPERAND2_RGB
        GL_OPERAND2_RGB_ARB
        GL_OR
        GL_ORDER
        GL_OR_INVERTED
        GL_OR_REVERSE
        GL_OUT_OF_MEMORY
        GL_PACK_ALIGNMENT
        GL_PACK_IMAGE_HEIGHT
        GL_PACK_LSB_FIRST
        GL_PACK_ROW_LENGTH
        GL_PACK_SKIP_IMAGES
        GL_PACK_SKIP_PIXELS
        GL_PACK_SKIP_ROWS
        GL_PACK_SWAP_BYTES
        GL_PASS_THROUGH_TOKEN
        GL_PERSPECTIVE_CORRECTION_HINT
        GL_PIXEL_MAP_A_TO_A
        GL_PIXEL_MAP_A_TO_A_SIZE
        GL_PIXEL_MAP_B_TO_B
        GL_PIXEL_MAP_B_TO_B_SIZE
        GL_PIXEL_MAP_G_TO_G
        GL_PIXEL_MAP_G_TO_G_SIZE
        GL_PIXEL_MAP_I_TO_A
        GL_PIXEL_MAP_I_TO_A_SIZE
        GL_PIXEL_MAP_I_TO_B
        GL_PIXEL_MAP_I_TO_B_SIZE
        GL_PIXEL_MAP_I_TO_G
        GL_PIXEL_MAP_I_TO_G_SIZE
        GL_PIXEL_MAP_I_TO_I
        GL_PIXEL_MAP_I_TO_I_SIZE
        GL_PIXEL_MAP_I_TO_R
        GL_PIXEL_MAP_I_TO_R_SIZE
        GL_PIXEL_MAP_R_TO_R
        GL_PIXEL_MAP_R_TO_R_SIZE
        GL_PIXEL_MAP_S_TO_S
        GL_PIXEL_MAP_S_TO_S_SIZE
        GL_PIXEL_MODE_BIT
        GL_POINT
        GL_POINTS
        GL_POINT_BIT
        GL_POINT_SIZE
        GL_POINT_SIZE_GRANULARITY
        GL_POINT_SIZE_RANGE
        GL_POINT_SMOOTH
        GL_POINT_SMOOTH_HINT
        GL_POINT_TOKEN
        GL_POLYGON
        GL_POLYGON_BIT
        GL_POLYGON_MODE
        GL_POLYGON_OFFSET_FACTOR
        GL_POLYGON_OFFSET_FILL
        GL_POLYGON_OFFSET_LINE
        GL_POLYGON_OFFSET_POINT
        GL_POLYGON_OFFSET_UNITS
        GL_POLYGON_SMOOTH
        GL_POLYGON_SMOOTH_HINT
        GL_POLYGON_STIPPLE
        GL_POLYGON_STIPPLE_BIT
        GL_POLYGON_TOKEN
        GL_POSITION
        GL_PREVIOUS
        GL_PREVIOUS_ARB
        GL_PRIMARY_COLOR
        GL_PRIMARY_COLOR_ARB
        GL_PROGRAM_ADDRESS_REGISTERS_ARB
        GL_PROGRAM_ALU_INSTRUCTIONS_ARB
        GL_PROGRAM_ATTRIBS_ARB
        GL_PROGRAM_BINDING_ARB
        GL_PROGRAM_ERROR_POSITION_ARB
        GL_PROGRAM_ERROR_STRING_ARB
        GL_PROGRAM_FORMAT_ARB
        GL_PROGRAM_FORMAT_ASCII_ARB
        GL_PROGRAM_INSTRUCTIONS_ARB
        GL_PROGRAM_LENGTH_ARB
        GL_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB
        GL_PROGRAM_NATIVE_ALU_INSTRUCTIONS_ARB
        GL_PROGRAM_NATIVE_ATTRIBS_ARB
        GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB
        GL_PROGRAM_NATIVE_PARAMETERS_ARB
        GL_PROGRAM_NATIVE_TEMPORARIES_ARB
        GL_PROGRAM_NATIVE_TEX_INDIRECTIONS_ARB
        GL_PROGRAM_NATIVE_TEX_INSTRUCTIONS_ARB
        GL_PROGRAM_OBJECT_ARB
        GL_PROGRAM_PARAMETERS_ARB
        GL_PROGRAM_STRING_ARB
        GL_PROGRAM_TEMPORARIES_ARB
        GL_PROGRAM_TEX_INDIRECTIONS_ARB
        GL_PROGRAM_TEX_INSTRUCTIONS_ARB
        GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB
        GL_PROJECTION
        GL_PROJECTION_MATRIX
        GL_PROJECTION_STACK_DEPTH
        GL_PROXY_TEXTURE_1D
        GL_PROXY_TEXTURE_2D
        GL_PROXY_TEXTURE_3D
        GL_PROXY_TEXTURE_CUBE_MAP
        GL_Q
        GL_QUADRATIC_ATTENUATION
        GL_QUADS
        GL_QUAD_STRIP
        GL_R
        GL_R3_G3_B2
        GL_READ_BUFFER
        GL_READ_ONLY_ARB
        GL_READ_WRITE_ARB
        GL_RED
        GL_RED_BIAS
        GL_RED_BITS
        GL_RED_SCALE
        GL_REFLECTION_MAP
        GL_RENDER
        GL_RENDERBUFFER_ALPHA_SIZE_EXT
        GL_RENDERBUFFER_BINDING_EXT
        GL_RENDERBUFFER_BLUE_SIZE_EXT
        GL_RENDERBUFFER_DEPTH_SIZE_EXT
        GL_RENDERBUFFER_EXT
        GL_RENDERBUFFER_GREEN_SIZE_EXT
        GL_RENDERBUFFER_HEIGHT_EXT
        GL_RENDERBUFFER_INTERNAL_FORMAT_EXT
        GL_RENDERBUFFER_RED_SIZE_EXT
        GL_RENDERBUFFER_STENCIL_SIZE_EXT
        GL_RENDERBUFFER_WIDTH_EXT
        GL_RENDERER
        GL_RENDER_MODE
        GL_REPEAT
        GL_REPLACE
        GL_RESCALE_NORMAL
        GL_RETURN
        GL_RGB
        GL_RGB10
        GL_RGB10_A2
        GL_RGB12
        GL_RGB16
        GL_RGB4
        GL_RGB5
        GL_RGB5_A1
        GL_RGB8
        GL_RGBA
        GL_RGBA12
        GL_RGBA16
        GL_RGBA2
        GL_RGBA4
        GL_RGBA8
        GL_RGBA_MODE
        GL_RGB_SCALE
        GL_RGB_SCALE_ARB
        GL_RIGHT
        GL_S
        GL_SAMPLER_1D_ARB
        GL_SAMPLER_1D_SHADOW_ARB
        GL_SAMPLER_2D_ARB
        GL_SAMPLER_2D_RECT_ARB
        GL_SAMPLER_2D_RECT_SHADOW_ARB
        GL_SAMPLER_2D_SHADOW_ARB
        GL_SAMPLER_3D_ARB
        GL_SAMPLER_CUBE_ARB
        GL_SAMPLES
        GL_SAMPLE_ALPHA_TO_COVERAGE
        GL_SAMPLE_ALPHA_TO_ONE
        GL_SAMPLE_BUFFERS
        GL_SAMPLE_COVERAGE
        GL_SAMPLE_COVERAGE_INVERT
        GL_SAMPLE_COVERAGE_VALUE
        GL_SCISSOR_BIT
        GL_SCISSOR_BOX
        GL_SCISSOR_TEST
        GL_SECONDARY_COLOR_ARRAY_BUFFER_BINDING_ARB
        GL_SELECT
        GL_SELECTION_BUFFER_POINTER
        GL_SELECTION_BUFFER_SIZE
        GL_SEPARATE_SPECULAR_COLOR
        GL_SET
        GL_SHADER_OBJECT_ARB
        GL_SHADE_MODEL
        GL_SHADING_LANGUAGE_VERSION_ARB
        GL_SHININESS
        GL_SHORT
        GL_SINGLE_COLOR
        GL_SMOOTH
        GL_SMOOTH_LINE_WIDTH_GRANULARITY
        GL_SMOOTH_LINE_WIDTH_RANGE
        GL_SMOOTH_POINT_SIZE_GRANULARITY
        GL_SMOOTH_POINT_SIZE_RANGE
        GL_SOURCE0_ALPHA
        GL_SOURCE0_ALPHA_ARB
        GL_SOURCE0_RGB
        GL_SOURCE0_RGB_ARB
        GL_SOURCE1_ALPHA
        GL_SOURCE1_ALPHA_ARB
        GL_SOURCE1_RGB
        GL_SOURCE1_RGB_ARB
        GL_SOURCE2_ALPHA
        GL_SOURCE2_ALPHA_ARB
        GL_SOURCE2_RGB
        GL_SOURCE2_RGB_ARB
        GL_SPECULAR
        GL_SPHERE_MAP
        GL_SPOT_CUTOFF
        GL_SPOT_DIRECTION
        GL_SPOT_EXPONENT
        GL_SRC_ALPHA
        GL_SRC_ALPHA_SATURATE
        GL_SRC_COLOR
        GL_STACK_OVERFLOW
        GL_STACK_UNDERFLOW
        GL_STATIC_COPY_ARB
        GL_STATIC_DRAW_ARB
        GL_STATIC_READ_ARB
        GL_STENCIL
        GL_STENCIL_ATTACHMENT_EXT
        GL_STENCIL_BITS
        GL_STENCIL_BUFFER_BIT
        GL_STENCIL_CLEAR_VALUE
        GL_STENCIL_FAIL
        GL_STENCIL_FUNC
        GL_STENCIL_INDEX
        GL_STENCIL_INDEX16_EXT
        GL_STENCIL_INDEX1_EXT
        GL_STENCIL_INDEX4_EXT
        GL_STENCIL_INDEX8_EXT
        GL_STENCIL_PASS_DEPTH_FAIL
        GL_STENCIL_PASS_DEPTH_PASS
        GL_STENCIL_REF
        GL_STENCIL_TEST
        GL_STENCIL_VALUE_MASK
        GL_STENCIL_WRITEMASK
        GL_STEREO
        GL_STREAM_COPY_ARB
        GL_STREAM_DRAW_ARB
        GL_STREAM_READ_ARB
        GL_SUBPIXEL_BITS
        GL_SUBTRACT
        GL_SUBTRACT_ARB
        GL_T
        GL_T2F_C3F_V3F
        GL_T2F_C4F_N3F_V3F
        GL_T2F_C4UB_V3F
        GL_T2F_N3F_V3F
        GL_T2F_V3F
        GL_T4F_C4F_N3F_V4F
        GL_T4F_V4F
        GL_TEXTURE
        GL_TEXTURE0
        GL_TEXTURE0_ARB
        GL_TEXTURE1
        GL_TEXTURE10
        GL_TEXTURE10_ARB
        GL_TEXTURE11
        GL_TEXTURE11_ARB
        GL_TEXTURE12
        GL_TEXTURE12_ARB
        GL_TEXTURE13
        GL_TEXTURE13_ARB
        GL_TEXTURE14
        GL_TEXTURE14_ARB
        GL_TEXTURE15
        GL_TEXTURE15_ARB
        GL_TEXTURE16
        GL_TEXTURE16_ARB
        GL_TEXTURE17
        GL_TEXTURE17_ARB
        GL_TEXTURE18
        GL_TEXTURE18_ARB
        GL_TEXTURE19
        GL_TEXTURE19_ARB
        GL_TEXTURE1_ARB
        GL_TEXTURE2
        GL_TEXTURE20
        GL_TEXTURE20_ARB
        GL_TEXTURE21
        GL_TEXTURE21_ARB
        GL_TEXTURE22
        GL_TEXTURE22_ARB
        GL_TEXTURE23
        GL_TEXTURE23_ARB
        GL_TEXTURE24
        GL_TEXTURE24_ARB
        GL_TEXTURE25
        GL_TEXTURE25_ARB
        GL_TEXTURE26
        GL_TEXTURE26_ARB
        GL_TEXTURE27
        GL_TEXTURE27_ARB
        GL_TEXTURE28
        GL_TEXTURE28_ARB
        GL_TEXTURE29
        GL_TEXTURE29_ARB
        GL_TEXTURE2_ARB
        GL_TEXTURE3
        GL_TEXTURE30
        GL_TEXTURE30_ARB
        GL_TEXTURE31
        GL_TEXTURE31_ARB
        GL_TEXTURE3_ARB
        GL_TEXTURE4
        GL_TEXTURE4_ARB
        GL_TEXTURE5
        GL_TEXTURE5_ARB
        GL_TEXTURE6
        GL_TEXTURE6_ARB
        GL_TEXTURE7
        GL_TEXTURE7_ARB
        GL_TEXTURE8
        GL_TEXTURE8_ARB
        GL_TEXTURE9
        GL_TEXTURE9_ARB
        GL_TEXTURE_1D
        GL_TEXTURE_2D
        GL_TEXTURE_3D
        GL_TEXTURE_ALPHA_SIZE
        GL_TEXTURE_BASE_LEVEL
        GL_TEXTURE_BINDING_1D
        GL_TEXTURE_BINDING_2D
        GL_TEXTURE_BINDING_3D
        GL_TEXTURE_BINDING_CUBE_MAP
        GL_TEXTURE_BIT
        GL_TEXTURE_BLUE_SIZE
        GL_TEXTURE_BORDER
        GL_TEXTURE_BORDER_COLOR
        GL_TEXTURE_COMPONENTS
        GL_TEXTURE_COMPRESSED
        GL_TEXTURE_COMPRESSED_IMAGE_SIZE
        GL_TEXTURE_COMPRESSION_HINT
        GL_TEXTURE_COORD_ARRAY
        GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING_ARB
        GL_TEXTURE_COORD_ARRAY_POINTER
        GL_TEXTURE_COORD_ARRAY_SIZE
        GL_TEXTURE_COORD_ARRAY_STRIDE
        GL_TEXTURE_COORD_ARRAY_TYPE
        GL_TEXTURE_CUBE_MAP
        GL_TEXTURE_CUBE_MAP_NEGATIVE_X
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
        GL_TEXTURE_CUBE_MAP_POSITIVE_X
        GL_TEXTURE_CUBE_MAP_POSITIVE_Y
        GL_TEXTURE_CUBE_MAP_POSITIVE_Z
        GL_TEXTURE_DEPTH
        GL_TEXTURE_ENV
        GL_TEXTURE_ENV_COLOR
        GL_TEXTURE_ENV_MODE
        GL_TEXTURE_GEN_MODE
        GL_TEXTURE_GEN_Q
        GL_TEXTURE_GEN_R
        GL_TEXTURE_GEN_S
        GL_TEXTURE_GEN_T
        GL_TEXTURE_GREEN_SIZE
        GL_TEXTURE_HEIGHT
        GL_TEXTURE_INTENSITY_SIZE
        GL_TEXTURE_INTERNAL_FORMAT
        GL_TEXTURE_LUMINANCE_SIZE
        GL_TEXTURE_MAG_FILTER
        GL_TEXTURE_MATRIX
        GL_TEXTURE_MAX_LEVEL
        GL_TEXTURE_MAX_LOD
        GL_TEXTURE_MIN_FILTER
        GL_TEXTURE_MIN_LOD
        GL_TEXTURE_PRIORITY
        GL_TEXTURE_RED_SIZE
        GL_TEXTURE_RESIDENT
        GL_TEXTURE_STACK_DEPTH
        GL_TEXTURE_WIDTH
        GL_TEXTURE_WRAP_R
        GL_TEXTURE_WRAP_S
        GL_TEXTURE_WRAP_T
        GL_TRANSFORM_BIT
        GL_TRANSPOSE_COLOR_MATRIX
        GL_TRANSPOSE_CURRENT_MATRIX_ARB
        GL_TRANSPOSE_MODELVIEW_MATRIX
        GL_TRANSPOSE_PROJECTION_MATRIX
        GL_TRANSPOSE_TEXTURE_MATRIX
        GL_TRIANGLES
        GL_TRIANGLE_FAN
        GL_TRIANGLE_STRIP
        GL_TRUE
        GL_UNPACK_ALIGNMENT
        GL_UNPACK_IMAGE_HEIGHT
        GL_UNPACK_LSB_FIRST
        GL_UNPACK_ROW_LENGTH
        GL_UNPACK_SKIP_IMAGES
        GL_UNPACK_SKIP_PIXELS
        GL_UNPACK_SKIP_ROWS
        GL_UNPACK_SWAP_BYTES
        GL_UNSIGNED_BYTE
        GL_UNSIGNED_BYTE_2_3_3_REV
        GL_UNSIGNED_BYTE_3_3_2
        GL_UNSIGNED_INT
        GL_UNSIGNED_INT_10_10_10_2
        GL_UNSIGNED_INT_2_10_10_10_REV
        GL_UNSIGNED_INT_8_8_8_8
        GL_UNSIGNED_INT_8_8_8_8_REV
        GL_UNSIGNED_SHORT
        GL_UNSIGNED_SHORT_1_5_5_5_REV
        GL_UNSIGNED_SHORT_4_4_4_4
        GL_UNSIGNED_SHORT_4_4_4_4_REV
        GL_UNSIGNED_SHORT_5_5_5_1
        GL_UNSIGNED_SHORT_5_6_5
        GL_UNSIGNED_SHORT_5_6_5_REV
        GL_V2F
        GL_V3F
        GL_VENDOR
        GL_VERSION
        GL_VERTEX_ARRAY
        GL_VERTEX_ARRAY_BUFFER_BINDING_ARB
        GL_VERTEX_ARRAY_POINTER
        GL_VERTEX_ARRAY_SIZE
        GL_VERTEX_ARRAY_STRIDE
        GL_VERTEX_ARRAY_TYPE
        GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING_ARB
        GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB
        GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB
        GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB
        GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB
        GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB
        GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB
        GL_VERTEX_PROGRAM_ARB
        GL_VERTEX_PROGRAM_POINT_SIZE_ARB
        GL_VERTEX_PROGRAM_TWO_SIDE_ARB
        GL_VERTEX_SHADER_ARB
        GL_VIEWPORT
        GL_VIEWPORT_BIT
        GL_WEIGHT_ARRAY_BUFFER_BINDING_ARB
        GL_WRITE_ONLY_ARB
        GL_XOR
        GL_ZERO
        GL_ZOOM_X
        GL_ZOOM_Y
        RENPY_THIRD_TEXTURE

    GLvoid realGlClearIndex "glClearIndex" (GLfloat)
    GLvoid realGlClearColor "glClearColor" (GLclampf, GLclampf, GLclampf, GLclampf)
    GLvoid realGlClear "glClear" (GLbitfield)
    GLvoid realGlIndexMask "glIndexMask" (GLuint)
    GLvoid realGlColorMask "glColorMask" (GLboolean, GLboolean, GLboolean, GLboolean)
    GLvoid realGlAlphaFunc "glAlphaFunc" (GLenum, GLclampf)
    GLvoid realGlBlendFunc "glBlendFunc" (GLenum, GLenum)
    GLvoid realGlLogicOp "glLogicOp" (GLenum)
    GLvoid realGlCullFace "glCullFace" (GLenum)
    GLvoid realGlFrontFace "glFrontFace" (GLenum)
    GLvoid realGlPointSize "glPointSize" (GLfloat)
    GLvoid realGlLineWidth "glLineWidth" (GLfloat)
    GLvoid realGlLineStipple "glLineStipple" (GLint, GLushort)
    GLvoid realGlPolygonMode "glPolygonMode" (GLenum, GLenum)
    GLvoid realGlPolygonOffset "glPolygonOffset" (GLfloat, GLfloat)
    GLvoid realGlPolygonStipple "glPolygonStipple" (GLubyte *)
    GLvoid realGlGetPolygonStipple "glGetPolygonStipple" (GLubyte *)
    GLvoid realGlEdgeFlag "glEdgeFlag" (GLboolean)
    GLvoid realGlEdgeFlagv "glEdgeFlagv" (GLboolean *)
    GLvoid realGlScissor "glScissor" (GLint, GLint, GLsizei, GLsizei)
    GLvoid realGlClipPlane "glClipPlane" (GLenum, GLdouble *)
    GLvoid realGlGetClipPlane "glGetClipPlane" (GLenum, GLdouble *)
    GLvoid realGlDrawBuffer "glDrawBuffer" (GLenum)
    GLvoid realGlReadBuffer "glReadBuffer" (GLenum)
    GLvoid realGlEnable "glEnable" (GLenum)
    GLvoid realGlDisable "glDisable" (GLenum)
    GLboolean realGlIsEnabled "glIsEnabled" (GLenum)
    GLvoid realGlEnableClientState "glEnableClientState" (GLenum)
    GLvoid realGlDisableClientState "glDisableClientState" (GLenum)
    GLvoid realGlGetBooleanv "glGetBooleanv" (GLenum, GLboolean *)
    GLvoid realGlGetDoublev "glGetDoublev" (GLenum, GLdouble *)
    GLvoid realGlGetFloatv "glGetFloatv" (GLenum, GLfloat *)
    GLvoid realGlGetIntegerv "glGetIntegerv" (GLenum, GLint *)
    GLvoid realGlPushAttrib "glPushAttrib" (GLbitfield)
    GLvoid realGlPopAttrib "glPopAttrib" ()
    GLvoid realGlPushClientAttrib "glPushClientAttrib" (GLbitfield)
    GLvoid realGlPopClientAttrib "glPopClientAttrib" ()
    GLint realGlRenderMode "glRenderMode" (GLenum)
    GLenum realGlGetError "glGetError" ()
    GLchar * realGlGetString "glGetString" (GLenum)
    GLvoid realGlFinish "glFinish" ()
    GLvoid realGlFlush "glFlush" ()
    GLvoid realGlHint "glHint" (GLenum, GLenum)
    GLvoid realGlClearDepth "glClearDepth" (GLclampd)
    GLvoid realGlDepthFunc "glDepthFunc" (GLenum)
    GLvoid realGlDepthMask "glDepthMask" (GLboolean)
    GLvoid realGlDepthRange "glDepthRange" (GLclampd, GLclampd)
    GLvoid realGlClearAccum "glClearAccum" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlAccum "glAccum" (GLenum, GLfloat)
    GLvoid realGlMatrixMode "glMatrixMode" (GLenum)
    GLvoid realGlOrtho "glOrtho" (GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlFrustum "glFrustum" (GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlViewport "glViewport" (GLint, GLint, GLsizei, GLsizei)
    GLvoid realGlPushMatrix "glPushMatrix" ()
    GLvoid realGlPopMatrix "glPopMatrix" ()
    GLvoid realGlLoadIdentity "glLoadIdentity" ()
    GLvoid realGlLoadMatrixd "glLoadMatrixd" (GLdouble *)
    GLvoid realGlLoadMatrixf "glLoadMatrixf" (GLfloat *)
    GLvoid realGlMultMatrixd "glMultMatrixd" (GLdouble *)
    GLvoid realGlMultMatrixf "glMultMatrixf" (GLfloat *)
    GLvoid realGlRotated "glRotated" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlRotatef "glRotatef" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlScaled "glScaled" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlScalef "glScalef" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlTranslated "glTranslated" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlTranslatef "glTranslatef" (GLfloat, GLfloat, GLfloat)
    GLboolean realGlIsList "glIsList" (GLuint)
    GLvoid realGlDeleteLists "glDeleteLists" (GLuint, GLsizei)
    GLuint realGlGenLists "glGenLists" (GLsizei)
    GLvoid realGlNewList "glNewList" (GLuint, GLenum)
    GLvoid realGlEndList "glEndList" ()
    GLvoid realGlCallList "glCallList" (GLuint)
    GLvoid realGlCallLists "glCallLists" (GLsizei, GLenum, GLubyte *)
    GLvoid realGlListBase "glListBase" (GLuint)
    GLvoid realGlBegin "glBegin" (GLenum)
    GLvoid realGlEnd "glEnd" ()
    GLvoid realGlVertex2d "glVertex2d" (GLdouble, GLdouble)
    GLvoid realGlVertex2f "glVertex2f" (GLfloat, GLfloat)
    GLvoid realGlVertex2i "glVertex2i" (GLint, GLint)
    GLvoid realGlVertex2s "glVertex2s" (GLshort, GLshort)
    GLvoid realGlVertex3d "glVertex3d" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlVertex3f "glVertex3f" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlVertex3i "glVertex3i" (GLint, GLint, GLint)
    GLvoid realGlVertex3s "glVertex3s" (GLshort, GLshort, GLshort)
    GLvoid realGlVertex4d "glVertex4d" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlVertex4f "glVertex4f" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlVertex4i "glVertex4i" (GLint, GLint, GLint, GLint)
    GLvoid realGlVertex4s "glVertex4s" (GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlVertex2dv "glVertex2dv" (GLdouble *)
    GLvoid realGlVertex2fv "glVertex2fv" (GLfloat *)
    GLvoid realGlVertex2iv "glVertex2iv" (GLint *)
    GLvoid realGlVertex2sv "glVertex2sv" (GLshort *)
    GLvoid realGlVertex3dv "glVertex3dv" (GLdouble *)
    GLvoid realGlVertex3fv "glVertex3fv" (GLfloat *)
    GLvoid realGlVertex3iv "glVertex3iv" (GLint *)
    GLvoid realGlVertex3sv "glVertex3sv" (GLshort *)
    GLvoid realGlVertex4dv "glVertex4dv" (GLdouble *)
    GLvoid realGlVertex4fv "glVertex4fv" (GLfloat *)
    GLvoid realGlVertex4iv "glVertex4iv" (GLint *)
    GLvoid realGlVertex4sv "glVertex4sv" (GLshort *)
    GLvoid realGlNormal3b "glNormal3b" (GLbyte, GLbyte, GLbyte)
    GLvoid realGlNormal3d "glNormal3d" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlNormal3f "glNormal3f" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlNormal3i "glNormal3i" (GLint, GLint, GLint)
    GLvoid realGlNormal3s "glNormal3s" (GLshort, GLshort, GLshort)
    GLvoid realGlNormal3bv "glNormal3bv" (GLbyte *)
    GLvoid realGlNormal3dv "glNormal3dv" (GLdouble *)
    GLvoid realGlNormal3fv "glNormal3fv" (GLfloat *)
    GLvoid realGlNormal3iv "glNormal3iv" (GLint *)
    GLvoid realGlNormal3sv "glNormal3sv" (GLshort *)
    GLvoid realGlIndexd "glIndexd" (GLdouble)
    GLvoid realGlIndexf "glIndexf" (GLfloat)
    GLvoid realGlIndexi "glIndexi" (GLint)
    GLvoid realGlIndexs "glIndexs" (GLshort)
    GLvoid realGlIndexub "glIndexub" (GLubyte)
    GLvoid realGlIndexdv "glIndexdv" (GLdouble *)
    GLvoid realGlIndexfv "glIndexfv" (GLfloat *)
    GLvoid realGlIndexiv "glIndexiv" (GLint *)
    GLvoid realGlIndexsv "glIndexsv" (GLshort *)
    GLvoid realGlIndexubv "glIndexubv" (GLubyte *)
    GLvoid realGlColor3b "glColor3b" (GLbyte, GLbyte, GLbyte)
    GLvoid realGlColor3d "glColor3d" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlColor3f "glColor3f" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlColor3i "glColor3i" (GLint, GLint, GLint)
    GLvoid realGlColor3s "glColor3s" (GLshort, GLshort, GLshort)
    GLvoid realGlColor3ub "glColor3ub" (GLubyte, GLubyte, GLubyte)
    GLvoid realGlColor3ui "glColor3ui" (GLuint, GLuint, GLuint)
    GLvoid realGlColor3us "glColor3us" (GLushort, GLushort, GLushort)
    GLvoid realGlColor4b "glColor4b" (GLbyte, GLbyte, GLbyte, GLbyte)
    GLvoid realGlColor4d "glColor4d" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlColor4f "glColor4f" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlColor4i "glColor4i" (GLint, GLint, GLint, GLint)
    GLvoid realGlColor4s "glColor4s" (GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlColor4ub "glColor4ub" (GLubyte, GLubyte, GLubyte, GLubyte)
    GLvoid realGlColor4ui "glColor4ui" (GLuint, GLuint, GLuint, GLuint)
    GLvoid realGlColor4us "glColor4us" (GLushort, GLushort, GLushort, GLushort)
    GLvoid realGlColor3bv "glColor3bv" (GLbyte *)
    GLvoid realGlColor3dv "glColor3dv" (GLdouble *)
    GLvoid realGlColor3fv "glColor3fv" (GLfloat *)
    GLvoid realGlColor3iv "glColor3iv" (GLint *)
    GLvoid realGlColor3sv "glColor3sv" (GLshort *)
    GLvoid realGlColor3ubv "glColor3ubv" (GLubyte *)
    GLvoid realGlColor3uiv "glColor3uiv" (GLuint *)
    GLvoid realGlColor3usv "glColor3usv" (GLushort *)
    GLvoid realGlColor4bv "glColor4bv" (GLbyte *)
    GLvoid realGlColor4dv "glColor4dv" (GLdouble *)
    GLvoid realGlColor4fv "glColor4fv" (GLfloat *)
    GLvoid realGlColor4iv "glColor4iv" (GLint *)
    GLvoid realGlColor4sv "glColor4sv" (GLshort *)
    GLvoid realGlColor4ubv "glColor4ubv" (GLubyte *)
    GLvoid realGlColor4uiv "glColor4uiv" (GLuint *)
    GLvoid realGlColor4usv "glColor4usv" (GLushort *)
    GLvoid realGlTexCoord1d "glTexCoord1d" (GLdouble)
    GLvoid realGlTexCoord1f "glTexCoord1f" (GLfloat)
    GLvoid realGlTexCoord1i "glTexCoord1i" (GLint)
    GLvoid realGlTexCoord1s "glTexCoord1s" (GLshort)
    GLvoid realGlTexCoord2d "glTexCoord2d" (GLdouble, GLdouble)
    GLvoid realGlTexCoord2f "glTexCoord2f" (GLfloat, GLfloat)
    GLvoid realGlTexCoord2i "glTexCoord2i" (GLint, GLint)
    GLvoid realGlTexCoord2s "glTexCoord2s" (GLshort, GLshort)
    GLvoid realGlTexCoord3d "glTexCoord3d" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlTexCoord3f "glTexCoord3f" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlTexCoord3i "glTexCoord3i" (GLint, GLint, GLint)
    GLvoid realGlTexCoord3s "glTexCoord3s" (GLshort, GLshort, GLshort)
    GLvoid realGlTexCoord4d "glTexCoord4d" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlTexCoord4f "glTexCoord4f" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlTexCoord4i "glTexCoord4i" (GLint, GLint, GLint, GLint)
    GLvoid realGlTexCoord4s "glTexCoord4s" (GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlTexCoord1dv "glTexCoord1dv" (GLdouble *)
    GLvoid realGlTexCoord1fv "glTexCoord1fv" (GLfloat *)
    GLvoid realGlTexCoord1iv "glTexCoord1iv" (GLint *)
    GLvoid realGlTexCoord1sv "glTexCoord1sv" (GLshort *)
    GLvoid realGlTexCoord2dv "glTexCoord2dv" (GLdouble *)
    GLvoid realGlTexCoord2fv "glTexCoord2fv" (GLfloat *)
    GLvoid realGlTexCoord2iv "glTexCoord2iv" (GLint *)
    GLvoid realGlTexCoord2sv "glTexCoord2sv" (GLshort *)
    GLvoid realGlTexCoord3dv "glTexCoord3dv" (GLdouble *)
    GLvoid realGlTexCoord3fv "glTexCoord3fv" (GLfloat *)
    GLvoid realGlTexCoord3iv "glTexCoord3iv" (GLint *)
    GLvoid realGlTexCoord3sv "glTexCoord3sv" (GLshort *)
    GLvoid realGlTexCoord4dv "glTexCoord4dv" (GLdouble *)
    GLvoid realGlTexCoord4fv "glTexCoord4fv" (GLfloat *)
    GLvoid realGlTexCoord4iv "glTexCoord4iv" (GLint *)
    GLvoid realGlTexCoord4sv "glTexCoord4sv" (GLshort *)
    GLvoid realGlRasterPos2d "glRasterPos2d" (GLdouble, GLdouble)
    GLvoid realGlRasterPos2f "glRasterPos2f" (GLfloat, GLfloat)
    GLvoid realGlRasterPos2i "glRasterPos2i" (GLint, GLint)
    GLvoid realGlRasterPos2s "glRasterPos2s" (GLshort, GLshort)
    GLvoid realGlRasterPos3d "glRasterPos3d" (GLdouble, GLdouble, GLdouble)
    GLvoid realGlRasterPos3f "glRasterPos3f" (GLfloat, GLfloat, GLfloat)
    GLvoid realGlRasterPos3i "glRasterPos3i" (GLint, GLint, GLint)
    GLvoid realGlRasterPos3s "glRasterPos3s" (GLshort, GLshort, GLshort)
    GLvoid realGlRasterPos4d "glRasterPos4d" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlRasterPos4f "glRasterPos4f" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlRasterPos4i "glRasterPos4i" (GLint, GLint, GLint, GLint)
    GLvoid realGlRasterPos4s "glRasterPos4s" (GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlRasterPos2dv "glRasterPos2dv" (GLdouble *)
    GLvoid realGlRasterPos2fv "glRasterPos2fv" (GLfloat *)
    GLvoid realGlRasterPos2iv "glRasterPos2iv" (GLint *)
    GLvoid realGlRasterPos2sv "glRasterPos2sv" (GLshort *)
    GLvoid realGlRasterPos3dv "glRasterPos3dv" (GLdouble *)
    GLvoid realGlRasterPos3fv "glRasterPos3fv" (GLfloat *)
    GLvoid realGlRasterPos3iv "glRasterPos3iv" (GLint *)
    GLvoid realGlRasterPos3sv "glRasterPos3sv" (GLshort *)
    GLvoid realGlRasterPos4dv "glRasterPos4dv" (GLdouble *)
    GLvoid realGlRasterPos4fv "glRasterPos4fv" (GLfloat *)
    GLvoid realGlRasterPos4iv "glRasterPos4iv" (GLint *)
    GLvoid realGlRasterPos4sv "glRasterPos4sv" (GLshort *)
    GLvoid realGlRectd "glRectd" (GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlRectf "glRectf" (GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlRecti "glRecti" (GLint, GLint, GLint, GLint)
    GLvoid realGlRects "glRects" (GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlRectdv "glRectdv" (GLdouble *, GLdouble *)
    GLvoid realGlRectfv "glRectfv" (GLfloat *, GLfloat *)
    GLvoid realGlRectiv "glRectiv" (GLint *, GLint *)
    GLvoid realGlRectsv "glRectsv" (GLshort *, GLshort *)
    GLvoid realGlVertexPointer "glVertexPointer" (GLint, GLenum, GLsizei, GLubyte *)
    GLvoid realGlNormalPointer "glNormalPointer" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlColorPointer "glColorPointer" (GLint, GLenum, GLsizei, GLubyte *)
    GLvoid realGlIndexPointer "glIndexPointer" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlTexCoordPointer "glTexCoordPointer" (GLint, GLenum, GLsizei, GLubyte *)
    GLvoid realGlEdgeFlagPointer "glEdgeFlagPointer" (GLsizei, GLubyte *)
    GLvoid realGlArrayElement "glArrayElement" (GLint)
    GLvoid realGlDrawArrays "glDrawArrays" (GLenum, GLint, GLsizei)
    GLvoid realGlDrawElements "glDrawElements" (GLenum, GLsizei, GLenum, GLubyte *)
    GLvoid realGlInterleavedArrays "glInterleavedArrays" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlShadeModel "glShadeModel" (GLenum)
    GLvoid realGlLightf "glLightf" (GLenum, GLenum, GLfloat)
    GLvoid realGlLighti "glLighti" (GLenum, GLenum, GLint)
    GLvoid realGlLightfv "glLightfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlLightiv "glLightiv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetLightfv "glGetLightfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlGetLightiv "glGetLightiv" (GLenum, GLenum, GLint *)
    GLvoid realGlLightModelf "glLightModelf" (GLenum, GLfloat)
    GLvoid realGlLightModeli "glLightModeli" (GLenum, GLint)
    GLvoid realGlLightModelfv "glLightModelfv" (GLenum, GLfloat *)
    GLvoid realGlLightModeliv "glLightModeliv" (GLenum, GLint *)
    GLvoid realGlMaterialf "glMaterialf" (GLenum, GLenum, GLfloat)
    GLvoid realGlMateriali "glMateriali" (GLenum, GLenum, GLint)
    GLvoid realGlMaterialfv "glMaterialfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlMaterialiv "glMaterialiv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetMaterialfv "glGetMaterialfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlGetMaterialiv "glGetMaterialiv" (GLenum, GLenum, GLint *)
    GLvoid realGlColorMaterial "glColorMaterial" (GLenum, GLenum)
    GLvoid realGlPixelZoom "glPixelZoom" (GLfloat, GLfloat)
    GLvoid realGlPixelStoref "glPixelStoref" (GLenum, GLfloat)
    GLvoid realGlPixelStorei "glPixelStorei" (GLenum, GLint)
    GLvoid realGlPixelTransferf "glPixelTransferf" (GLenum, GLfloat)
    GLvoid realGlPixelTransferi "glPixelTransferi" (GLenum, GLint)
    GLvoid realGlPixelMapfv "glPixelMapfv" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlPixelMapuiv "glPixelMapuiv" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlPixelMapusv "glPixelMapusv" (GLenum, GLsizei, GLubyte *)
    GLvoid realGlGetPixelMapfv "glGetPixelMapfv" (GLenum, GLubyte *)
    GLvoid realGlGetPixelMapuiv "glGetPixelMapuiv" (GLenum, GLubyte *)
    GLvoid realGlGetPixelMapusv "glGetPixelMapusv" (GLenum, GLubyte *)
    GLvoid realGlBitmap "glBitmap" (GLsizei, GLsizei, GLfloat, GLfloat, GLfloat, GLfloat, GLubyte *)
    GLvoid realGlReadPixels "glReadPixels" (GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    GLvoid realGlDrawPixels "glDrawPixels" (GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    GLvoid realGlCopyPixels "glCopyPixels" (GLint, GLint, GLsizei, GLsizei, GLenum)
    GLvoid realGlStencilFunc "glStencilFunc" (GLenum, GLint, GLuint)
    GLvoid realGlStencilMask "glStencilMask" (GLuint)
    GLvoid realGlStencilOp "glStencilOp" (GLenum, GLenum, GLenum)
    GLvoid realGlClearStencil "glClearStencil" (GLint)
    GLvoid realGlTexGend "glTexGend" (GLenum, GLenum, GLdouble)
    GLvoid realGlTexGenf "glTexGenf" (GLenum, GLenum, GLfloat)
    GLvoid realGlTexGeni "glTexGeni" (GLenum, GLenum, GLint)
    GLvoid realGlTexGendv "glTexGendv" (GLenum, GLenum, GLdouble *)
    GLvoid realGlTexGenfv "glTexGenfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlTexGeniv "glTexGeniv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetTexGendv "glGetTexGendv" (GLenum, GLenum, GLdouble *)
    GLvoid realGlGetTexGenfv "glGetTexGenfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlGetTexGeniv "glGetTexGeniv" (GLenum, GLenum, GLint *)
    GLvoid realGlTexEnvf "glTexEnvf" (GLenum, GLenum, GLfloat)
    GLvoid realGlTexEnvi "glTexEnvi" (GLenum, GLenum, GLint)
    GLvoid realGlTexEnvfv "glTexEnvfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlTexEnviv "glTexEnviv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetTexEnvfv "glGetTexEnvfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlGetTexEnviv "glGetTexEnviv" (GLenum, GLenum, GLint *)
    GLvoid realGlTexParameterf "glTexParameterf" (GLenum, GLenum, GLfloat)
    GLvoid realGlTexParameteri "glTexParameteri" (GLenum, GLenum, GLint)
    GLvoid realGlTexParameterfv "glTexParameterfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlTexParameteriv "glTexParameteriv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetTexParameterfv "glGetTexParameterfv" (GLenum, GLenum, GLfloat *)
    GLvoid realGlGetTexParameteriv "glGetTexParameteriv" (GLenum, GLenum, GLint *)
    GLvoid realGlGetTexLevelParameterfv "glGetTexLevelParameterfv" (GLenum, GLint, GLenum, GLfloat *)
    GLvoid realGlGetTexLevelParameteriv "glGetTexLevelParameteriv" (GLenum, GLint, GLenum, GLint *)
    GLvoid realGlTexImage1D "glTexImage1D" (GLenum, GLint, GLint, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    GLvoid realGlTexImage2D "glTexImage2D" (GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    GLvoid realGlGetTexImage "glGetTexImage" (GLenum, GLint, GLenum, GLenum, GLubyte *)
    GLvoid realGlBindTexture "glBindTexture" (GLenum, GLuint)
    GLboolean realGlIsTexture "glIsTexture" (GLuint)
    GLvoid realGlTexSubImage1D "glTexSubImage1D" (GLenum, GLint, GLint, GLsizei, GLenum, GLenum, GLubyte *)
    GLvoid realGlTexSubImage2D "glTexSubImage2D" (GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    GLvoid realGlCopyTexImage1D "glCopyTexImage1D" (GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLint)
    GLvoid realGlCopyTexImage2D "glCopyTexImage2D" (GLenum, GLint, GLenum, GLint, GLint, GLsizei, GLsizei, GLint)
    GLvoid realGlCopyTexSubImage1D "glCopyTexSubImage1D" (GLenum, GLint, GLint, GLint, GLint, GLsizei)
    GLvoid realGlCopyTexSubImage2D "glCopyTexSubImage2D" (GLenum, GLint, GLint, GLint, GLint, GLint, GLsizei, GLsizei)
    GLvoid realGlGenTextures "glGenTextures" (GLsizei, GLuint *)
    GLvoid realGlDeleteTextures "glDeleteTextures" (GLsizei, GLuint *)
    GLvoid realGlPrioritizeTextures "glPrioritizeTextures" (GLsizei, GLuint *, GLclampf *)
    GLboolean realGlAreTexturesResident "glAreTexturesResident" (GLsizei, GLuint *, GLboolean *)
    GLvoid realGlMap1d "glMap1d" (GLenum, GLdouble, GLdouble, GLint, GLint, GLubyte *)
    GLvoid realGlMap1f "glMap1f" (GLenum, GLfloat, GLfloat, GLint, GLint, GLubyte *)
    GLvoid realGlMap2d "glMap2d" (GLenum, GLdouble, GLdouble, GLint, GLint, GLdouble, GLdouble, GLint, GLint, GLubyte *)
    GLvoid realGlMap2f "glMap2f" (GLenum, GLfloat, GLfloat, GLint, GLint, GLfloat, GLfloat, GLint, GLint, GLubyte *)
    GLvoid realGlGetMapdv "glGetMapdv" (GLenum, GLenum, GLubyte *)
    GLvoid realGlGetMapfv "glGetMapfv" (GLenum, GLenum, GLubyte *)
    GLvoid realGlGetMapiv "glGetMapiv" (GLenum, GLenum, GLubyte *)
    GLvoid realGlEvalCoord1d "glEvalCoord1d" (GLdouble)
    GLvoid realGlEvalCoord1f "glEvalCoord1f" (GLfloat)
    GLvoid realGlEvalCoord1dv "glEvalCoord1dv" (GLdouble *)
    GLvoid realGlEvalCoord1fv "glEvalCoord1fv" (GLfloat *)
    GLvoid realGlEvalCoord2d "glEvalCoord2d" (GLdouble, GLdouble)
    GLvoid realGlEvalCoord2f "glEvalCoord2f" (GLfloat, GLfloat)
    GLvoid realGlEvalCoord2dv "glEvalCoord2dv" (GLdouble *)
    GLvoid realGlEvalCoord2fv "glEvalCoord2fv" (GLfloat *)
    GLvoid realGlMapGrid1d "glMapGrid1d" (GLint, GLdouble, GLdouble)
    GLvoid realGlMapGrid1f "glMapGrid1f" (GLint, GLfloat, GLfloat)
    GLvoid realGlMapGrid2d "glMapGrid2d" (GLint, GLdouble, GLdouble, GLint, GLdouble, GLdouble)
    GLvoid realGlMapGrid2f "glMapGrid2f" (GLint, GLfloat, GLfloat, GLint, GLfloat, GLfloat)
    GLvoid realGlEvalPoint1 "glEvalPoint1" (GLint)
    GLvoid realGlEvalPoint2 "glEvalPoint2" (GLint, GLint)
    GLvoid realGlEvalMesh1 "glEvalMesh1" (GLenum, GLint, GLint)
    GLvoid realGlEvalMesh2 "glEvalMesh2" (GLenum, GLint, GLint, GLint, GLint)
    GLvoid realGlFogf "glFogf" (GLenum, GLfloat)
    GLvoid realGlFogi "glFogi" (GLenum, GLint)
    GLvoid realGlFogfv "glFogfv" (GLenum, GLfloat *)
    GLvoid realGlFogiv "glFogiv" (GLenum, GLint *)
    GLvoid realGlFeedbackBuffer "glFeedbackBuffer" (GLsizei, GLenum, GLubyte *)
    GLvoid realGlPassThrough "glPassThrough" (GLfloat)
    GLvoid realGlSelectBuffer "glSelectBuffer" (GLsizei, GLubyte *)
    GLvoid realGlInitNames "glInitNames" ()
    GLvoid realGlLoadName "glLoadName" (GLuint)
    GLvoid realGlPushName "glPushName" (GLuint)
    GLvoid realGlPopName "glPopName" ()
    GLvoid realGlDrawRangeElements "glDrawRangeElements" (GLenum, GLuint, GLuint, GLsizei, GLenum, GLubyte *)
    GLvoid realGlTexImage3D "glTexImage3D" (GLenum, GLint, GLint, GLsizei, GLsizei, GLsizei, GLint, GLenum, GLenum, GLubyte *)
    GLvoid realGlTexSubImage3D "glTexSubImage3D" (GLenum, GLint, GLint, GLint, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLenum, GLubyte *)
    GLvoid realGlCopyTexSubImage3D "glCopyTexSubImage3D" (GLenum, GLint, GLint, GLint, GLint, GLint, GLint, GLsizei, GLsizei)
    GLvoid realGlActiveTexture "glActiveTexture" (GLenum)
    GLvoid realGlClientActiveTexture "glClientActiveTexture" (GLenum)
    GLvoid realGlCompressedTexImage1D "glCompressedTexImage1D" (GLenum, GLint, GLenum, GLsizei, GLint, GLsizei, GLubyte *)
    GLvoid realGlCompressedTexImage2D "glCompressedTexImage2D" (GLenum, GLint, GLenum, GLsizei, GLsizei, GLint, GLsizei, GLubyte *)
    GLvoid realGlCompressedTexImage3D "glCompressedTexImage3D" (GLenum, GLint, GLenum, GLsizei, GLsizei, GLsizei, GLint, GLsizei, GLubyte *)
    GLvoid realGlCompressedTexSubImage1D "glCompressedTexSubImage1D" (GLenum, GLint, GLint, GLsizei, GLenum, GLsizei, GLubyte *)
    GLvoid realGlCompressedTexSubImage2D "glCompressedTexSubImage2D" (GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLsizei, GLubyte *)
    GLvoid realGlCompressedTexSubImage3D "glCompressedTexSubImage3D" (GLenum, GLint, GLint, GLint, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLsizei, GLubyte *)
    GLvoid realGlGetCompressedTexImage "glGetCompressedTexImage" (GLenum, GLint, GLubyte *)
    GLvoid realGlMultiTexCoord1d "glMultiTexCoord1d" (GLenum, GLdouble)
    GLvoid realGlMultiTexCoord1dv "glMultiTexCoord1dv" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord1f "glMultiTexCoord1f" (GLenum, GLfloat)
    GLvoid realGlMultiTexCoord1fv "glMultiTexCoord1fv" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord1i "glMultiTexCoord1i" (GLenum, GLint)
    GLvoid realGlMultiTexCoord1iv "glMultiTexCoord1iv" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord1s "glMultiTexCoord1s" (GLenum, GLshort)
    GLvoid realGlMultiTexCoord1sv "glMultiTexCoord1sv" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord2d "glMultiTexCoord2d" (GLenum, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord2dv "glMultiTexCoord2dv" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord2f "glMultiTexCoord2f" (GLenum, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord2fv "glMultiTexCoord2fv" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord2i "glMultiTexCoord2i" (GLenum, GLint, GLint)
    GLvoid realGlMultiTexCoord2iv "glMultiTexCoord2iv" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord2s "glMultiTexCoord2s" (GLenum, GLshort, GLshort)
    GLvoid realGlMultiTexCoord2sv "glMultiTexCoord2sv" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord3d "glMultiTexCoord3d" (GLenum, GLdouble, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord3dv "glMultiTexCoord3dv" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord3f "glMultiTexCoord3f" (GLenum, GLfloat, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord3fv "glMultiTexCoord3fv" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord3i "glMultiTexCoord3i" (GLenum, GLint, GLint, GLint)
    GLvoid realGlMultiTexCoord3iv "glMultiTexCoord3iv" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord3s "glMultiTexCoord3s" (GLenum, GLshort, GLshort, GLshort)
    GLvoid realGlMultiTexCoord3sv "glMultiTexCoord3sv" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord4d "glMultiTexCoord4d" (GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord4dv "glMultiTexCoord4dv" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord4f "glMultiTexCoord4f" (GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord4fv "glMultiTexCoord4fv" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord4i "glMultiTexCoord4i" (GLenum, GLint, GLint, GLint, GLint)
    GLvoid realGlMultiTexCoord4iv "glMultiTexCoord4iv" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord4s "glMultiTexCoord4s" (GLenum, GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlMultiTexCoord4sv "glMultiTexCoord4sv" (GLenum, GLshort *)
    GLvoid realGlLoadTransposeMatrixd "glLoadTransposeMatrixd" (GLdouble *)
    GLvoid realGlLoadTransposeMatrixf "glLoadTransposeMatrixf" (GLfloat *)
    GLvoid realGlMultTransposeMatrixd "glMultTransposeMatrixd" (GLdouble *)
    GLvoid realGlMultTransposeMatrixf "glMultTransposeMatrixf" (GLfloat *)
    GLvoid realGlSampleCoverage "glSampleCoverage" (GLclampf, GLboolean)
    GLvoid realGlActiveTextureARB "glActiveTextureARB" (GLenum)
    GLvoid realGlClientActiveTextureARB "glClientActiveTextureARB" (GLenum)
    GLvoid realGlMultiTexCoord1dARB "glMultiTexCoord1dARB" (GLenum, GLdouble)
    GLvoid realGlMultiTexCoord1dvARB "glMultiTexCoord1dvARB" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord1fARB "glMultiTexCoord1fARB" (GLenum, GLfloat)
    GLvoid realGlMultiTexCoord1fvARB "glMultiTexCoord1fvARB" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord1iARB "glMultiTexCoord1iARB" (GLenum, GLint)
    GLvoid realGlMultiTexCoord1ivARB "glMultiTexCoord1ivARB" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord1sARB "glMultiTexCoord1sARB" (GLenum, GLshort)
    GLvoid realGlMultiTexCoord1svARB "glMultiTexCoord1svARB" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord2dARB "glMultiTexCoord2dARB" (GLenum, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord2dvARB "glMultiTexCoord2dvARB" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord2fARB "glMultiTexCoord2fARB" (GLenum, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord2fvARB "glMultiTexCoord2fvARB" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord2iARB "glMultiTexCoord2iARB" (GLenum, GLint, GLint)
    GLvoid realGlMultiTexCoord2ivARB "glMultiTexCoord2ivARB" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord2sARB "glMultiTexCoord2sARB" (GLenum, GLshort, GLshort)
    GLvoid realGlMultiTexCoord2svARB "glMultiTexCoord2svARB" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord3dARB "glMultiTexCoord3dARB" (GLenum, GLdouble, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord3dvARB "glMultiTexCoord3dvARB" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord3fARB "glMultiTexCoord3fARB" (GLenum, GLfloat, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord3fvARB "glMultiTexCoord3fvARB" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord3iARB "glMultiTexCoord3iARB" (GLenum, GLint, GLint, GLint)
    GLvoid realGlMultiTexCoord3ivARB "glMultiTexCoord3ivARB" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord3sARB "glMultiTexCoord3sARB" (GLenum, GLshort, GLshort, GLshort)
    GLvoid realGlMultiTexCoord3svARB "glMultiTexCoord3svARB" (GLenum, GLshort *)
    GLvoid realGlMultiTexCoord4dARB "glMultiTexCoord4dARB" (GLenum, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlMultiTexCoord4dvARB "glMultiTexCoord4dvARB" (GLenum, GLdouble *)
    GLvoid realGlMultiTexCoord4fARB "glMultiTexCoord4fARB" (GLenum, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlMultiTexCoord4fvARB "glMultiTexCoord4fvARB" (GLenum, GLfloat *)
    GLvoid realGlMultiTexCoord4iARB "glMultiTexCoord4iARB" (GLenum, GLint, GLint, GLint, GLint)
    GLvoid realGlMultiTexCoord4ivARB "glMultiTexCoord4ivARB" (GLenum, GLint *)
    GLvoid realGlMultiTexCoord4sARB "glMultiTexCoord4sARB" (GLenum, GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlMultiTexCoord4svARB "glMultiTexCoord4svARB" (GLenum, GLshort *)
    GLvoid realGlVertexAttrib1dARB "glVertexAttrib1dARB" (GLuint, GLdouble)
    GLvoid realGlVertexAttrib1dvARB "glVertexAttrib1dvARB" (GLuint, GLdouble *)
    GLvoid realGlVertexAttrib1fARB "glVertexAttrib1fARB" (GLuint, GLfloat)
    GLvoid realGlVertexAttrib1fvARB "glVertexAttrib1fvARB" (GLuint, GLfloat *)
    GLvoid realGlVertexAttrib1sARB "glVertexAttrib1sARB" (GLuint, GLshort)
    GLvoid realGlVertexAttrib1svARB "glVertexAttrib1svARB" (GLuint, GLshort *)
    GLvoid realGlVertexAttrib2dARB "glVertexAttrib2dARB" (GLuint, GLdouble, GLdouble)
    GLvoid realGlVertexAttrib2dvARB "glVertexAttrib2dvARB" (GLuint, GLdouble *)
    GLvoid realGlVertexAttrib2fARB "glVertexAttrib2fARB" (GLuint, GLfloat, GLfloat)
    GLvoid realGlVertexAttrib2fvARB "glVertexAttrib2fvARB" (GLuint, GLfloat *)
    GLvoid realGlVertexAttrib2sARB "glVertexAttrib2sARB" (GLuint, GLshort, GLshort)
    GLvoid realGlVertexAttrib2svARB "glVertexAttrib2svARB" (GLuint, GLshort *)
    GLvoid realGlVertexAttrib3dARB "glVertexAttrib3dARB" (GLuint, GLdouble, GLdouble, GLdouble)
    GLvoid realGlVertexAttrib3dvARB "glVertexAttrib3dvARB" (GLuint, GLdouble *)
    GLvoid realGlVertexAttrib3fARB "glVertexAttrib3fARB" (GLuint, GLfloat, GLfloat, GLfloat)
    GLvoid realGlVertexAttrib3fvARB "glVertexAttrib3fvARB" (GLuint, GLfloat *)
    GLvoid realGlVertexAttrib3sARB "glVertexAttrib3sARB" (GLuint, GLshort, GLshort, GLshort)
    GLvoid realGlVertexAttrib3svARB "glVertexAttrib3svARB" (GLuint, GLshort *)
    GLvoid realGlVertexAttrib4NbvARB "glVertexAttrib4NbvARB" (GLuint, GLbyte *)
    GLvoid realGlVertexAttrib4NivARB "glVertexAttrib4NivARB" (GLuint, GLint *)
    GLvoid realGlVertexAttrib4NsvARB "glVertexAttrib4NsvARB" (GLuint, GLshort *)
    GLvoid realGlVertexAttrib4NubARB "glVertexAttrib4NubARB" (GLuint, GLubyte, GLubyte, GLubyte, GLubyte)
    GLvoid realGlVertexAttrib4NubvARB "glVertexAttrib4NubvARB" (GLuint, GLubyte *)
    GLvoid realGlVertexAttrib4NuivARB "glVertexAttrib4NuivARB" (GLuint, GLuint *)
    GLvoid realGlVertexAttrib4NusvARB "glVertexAttrib4NusvARB" (GLuint, GLushort *)
    GLvoid realGlVertexAttrib4bvARB "glVertexAttrib4bvARB" (GLuint, GLbyte *)
    GLvoid realGlVertexAttrib4dARB "glVertexAttrib4dARB" (GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlVertexAttrib4dvARB "glVertexAttrib4dvARB" (GLuint, GLdouble *)
    GLvoid realGlVertexAttrib4fARB "glVertexAttrib4fARB" (GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlVertexAttrib4fvARB "glVertexAttrib4fvARB" (GLuint, GLfloat *)
    GLvoid realGlVertexAttrib4ivARB "glVertexAttrib4ivARB" (GLuint, GLint *)
    GLvoid realGlVertexAttrib4sARB "glVertexAttrib4sARB" (GLuint, GLshort, GLshort, GLshort, GLshort)
    GLvoid realGlVertexAttrib4svARB "glVertexAttrib4svARB" (GLuint, GLshort *)
    GLvoid realGlVertexAttrib4ubvARB "glVertexAttrib4ubvARB" (GLuint, GLubyte *)
    GLvoid realGlVertexAttrib4uivARB "glVertexAttrib4uivARB" (GLuint, GLuint *)
    GLvoid realGlVertexAttrib4usvARB "glVertexAttrib4usvARB" (GLuint, GLushort *)
    GLvoid realGlVertexAttribPointerARB "glVertexAttribPointerARB" (GLuint, GLint, GLenum, GLboolean, GLsizei, GLubyte *)
    GLvoid realGlEnableVertexAttribArrayARB "glEnableVertexAttribArrayARB" (GLuint)
    GLvoid realGlDisableVertexAttribArrayARB "glDisableVertexAttribArrayARB" (GLuint)
    GLvoid realGlProgramStringARB "glProgramStringARB" (GLenum, GLenum, GLsizei, GLubyte *)
    GLvoid realGlBindProgramARB "glBindProgramARB" (GLenum, GLuint)
    GLvoid realGlDeleteProgramsARB "glDeleteProgramsARB" (GLsizei, GLuint *)
    GLvoid realGlGenProgramsARB "glGenProgramsARB" (GLsizei, GLuint *)
    GLvoid realGlProgramEnvParameter4dARB "glProgramEnvParameter4dARB" (GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlProgramEnvParameter4dvARB "glProgramEnvParameter4dvARB" (GLenum, GLuint, GLdouble *)
    GLvoid realGlProgramEnvParameter4fARB "glProgramEnvParameter4fARB" (GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlProgramEnvParameter4fvARB "glProgramEnvParameter4fvARB" (GLenum, GLuint, GLfloat *)
    GLvoid realGlProgramLocalParameter4dARB "glProgramLocalParameter4dARB" (GLenum, GLuint, GLdouble, GLdouble, GLdouble, GLdouble)
    GLvoid realGlProgramLocalParameter4dvARB "glProgramLocalParameter4dvARB" (GLenum, GLuint, GLdouble *)
    GLvoid realGlProgramLocalParameter4fARB "glProgramLocalParameter4fARB" (GLenum, GLuint, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlProgramLocalParameter4fvARB "glProgramLocalParameter4fvARB" (GLenum, GLuint, GLfloat *)
    GLvoid realGlGetProgramEnvParameterdvARB "glGetProgramEnvParameterdvARB" (GLenum, GLuint, GLdouble *)
    GLvoid realGlGetProgramEnvParameterfvARB "glGetProgramEnvParameterfvARB" (GLenum, GLuint, GLfloat *)
    GLvoid realGlGetProgramLocalParameterdvARB "glGetProgramLocalParameterdvARB" (GLenum, GLuint, GLdouble *)
    GLvoid realGlGetProgramLocalParameterfvARB "glGetProgramLocalParameterfvARB" (GLenum, GLuint, GLfloat *)
    GLvoid realGlGetProgramivARB "glGetProgramivARB" (GLenum, GLenum, GLint *)
    GLvoid realGlGetProgramStringARB "glGetProgramStringARB" (GLenum, GLenum, GLchar *)
    GLvoid realGlGetVertexAttribdvARB "glGetVertexAttribdvARB" (GLuint, GLenum, GLdouble *)
    GLvoid realGlGetVertexAttribfvARB "glGetVertexAttribfvARB" (GLuint, GLenum, GLfloat *)
    GLvoid realGlGetVertexAttribivARB "glGetVertexAttribivARB" (GLuint, GLenum, GLint *)
    GLboolean realGlIsProgramARB "glIsProgramARB" (GLuint)
    GLvoid realGlBindBufferARB "glBindBufferARB" (GLenum, GLuint)
    GLboolean realGlIsBufferARB "glIsBufferARB" (GLuint)
    GLvoid realGlBufferDataARB "glBufferDataARB" (GLenum, GLsizeiptrARB, GLubyte *, GLenum)
    GLvoid realGlBufferSubDataARB "glBufferSubDataARB" (GLenum, GLintptrARB, GLsizeiptrARB, GLubyte *)
    GLvoid realGlGetBufferSubDataARB "glGetBufferSubDataARB" (GLenum, GLintptrARB, GLsizeiptrARB, GLubyte *)
    GLvoid * realGlMapBufferARB "glMapBufferARB" (GLenum, GLenum)
    GLboolean realGlUnmapBufferARB "glUnmapBufferARB" (GLenum)
    GLvoid realGlGetBufferParameterivARB "glGetBufferParameterivARB" (GLenum, GLenum, GLint *)
    GLvoid realGlDeleteObjectARB "glDeleteObjectARB" (GLhandleARB)
    GLhandleARB realGlGetHandleARB "glGetHandleARB" (GLenum)
    GLvoid realGlDetachObjectARB "glDetachObjectARB" (GLhandleARB, GLhandleARB)
    GLhandleARB realGlCreateShaderObjectARB "glCreateShaderObjectARB" (GLenum)
    GLvoid realGlShaderSourceARB "glShaderSourceARB" (GLhandleARB, GLsizei, GLchar * *, GLint *)
    GLvoid realGlCompileShaderARB "glCompileShaderARB" (GLhandleARB)
    GLhandleARB realGlCreateProgramObjectARB "glCreateProgramObjectARB" ()
    GLvoid realGlAttachObjectARB "glAttachObjectARB" (GLhandleARB, GLhandleARB)
    GLvoid realGlLinkProgramARB "glLinkProgramARB" (GLhandleARB)
    GLvoid realGlUseProgramObjectARB "glUseProgramObjectARB" (GLhandleARB)
    GLvoid realGlValidateProgramARB "glValidateProgramARB" (GLhandleARB)
    GLvoid realGlUniform1fARB "glUniform1fARB" (GLint, GLfloat)
    GLvoid realGlUniform2fARB "glUniform2fARB" (GLint, GLfloat, GLfloat)
    GLvoid realGlUniform3fARB "glUniform3fARB" (GLint, GLfloat, GLfloat, GLfloat)
    GLvoid realGlUniform4fARB "glUniform4fARB" (GLint, GLfloat, GLfloat, GLfloat, GLfloat)
    GLvoid realGlUniform1iARB "glUniform1iARB" (GLint, GLint)
    GLvoid realGlUniform2iARB "glUniform2iARB" (GLint, GLint, GLint)
    GLvoid realGlUniform3iARB "glUniform3iARB" (GLint, GLint, GLint, GLint)
    GLvoid realGlUniform4iARB "glUniform4iARB" (GLint, GLint, GLint, GLint, GLint)
    GLvoid realGlUniform1fvARB "glUniform1fvARB" (GLint, GLsizei, GLfloat *)
    GLvoid realGlUniform2fvARB "glUniform2fvARB" (GLint, GLsizei, GLfloat *)
    GLvoid realGlUniform3fvARB "glUniform3fvARB" (GLint, GLsizei, GLfloat *)
    GLvoid realGlUniform4fvARB "glUniform4fvARB" (GLint, GLsizei, GLfloat *)
    GLvoid realGlUniform1ivARB "glUniform1ivARB" (GLint, GLsizei, GLint *)
    GLvoid realGlUniform2ivARB "glUniform2ivARB" (GLint, GLsizei, GLint *)
    GLvoid realGlUniform3ivARB "glUniform3ivARB" (GLint, GLsizei, GLint *)
    GLvoid realGlUniform4ivARB "glUniform4ivARB" (GLint, GLsizei, GLint *)
    GLvoid realGlUniformMatrix2fvARB "glUniformMatrix2fvARB" (GLint, GLsizei, GLboolean, GLfloat *)
    GLvoid realGlUniformMatrix3fvARB "glUniformMatrix3fvARB" (GLint, GLsizei, GLboolean, GLfloat *)
    GLvoid realGlUniformMatrix4fvARB "glUniformMatrix4fvARB" (GLint, GLsizei, GLboolean, GLfloat *)
    GLvoid realGlGetObjectParameterfvARB "glGetObjectParameterfvARB" (GLhandleARB, GLenum, GLfloat *)
    GLvoid realGlGetObjectParameterivARB "glGetObjectParameterivARB" (GLhandleARB, GLenum, GLint *)
    GLvoid realGlGetInfoLogARB "glGetInfoLogARB" (GLhandleARB, GLsizei, GLsizei *, GLchar *)
    GLvoid realGlGetAttachedObjectsARB "glGetAttachedObjectsARB" (GLhandleARB, GLsizei, GLsizei *, GLubyte *)
    GLint realGlGetUniformLocationARB "glGetUniformLocationARB" (GLhandleARB, GLchar *)
    GLvoid realGlGetActiveUniformARB "glGetActiveUniformARB" (GLhandleARB, GLuint, GLsizei, GLsizei *, GLint *, GLenum *, GLchar *)
    GLvoid realGlGetUniformfvARB "glGetUniformfvARB" (GLhandleARB, GLint, GLfloat *)
    GLvoid realGlGetUniformivARB "glGetUniformivARB" (GLhandleARB, GLint, GLint *)
    GLvoid realGlGetShaderSourceARB "glGetShaderSourceARB" (GLhandleARB, GLsizei, GLsizei *, GLchar *)
    GLvoid realGlBindAttribLocationARB "glBindAttribLocationARB" (GLhandleARB, GLuint, GLchar *)
    GLvoid realGlGetActiveAttribARB "glGetActiveAttribARB" (GLhandleARB, GLuint, GLsizei, GLsizei *, GLint *, GLenum *, GLchar *)
    GLint realGlGetAttribLocationARB "glGetAttribLocationARB" (GLhandleARB, GLchar *)
    GLvoid realGlGetProgramiv "glGetProgramiv" (GLuint, GLenum, GLint *)
    GLvoid realGlGetShaderiv "glGetShaderiv" (GLuint, GLenum, GLint *)
    GLvoid realGlDeleteProgram "glDeleteProgram" (GLuint)
    GLvoid realGlDeleteShader "glDeleteShader" (GLuint)
    GLvoid realGlGetProgramInfoLog "glGetProgramInfoLog" (GLhandleARB, GLsizei, GLsizei *, GLchar *)
    GLvoid realGlGetShaderInfoLog "glGetShaderInfoLog" (GLhandleARB, GLsizei, GLsizei *, GLchar *)
    GLboolean realGlIsRenderbufferEXT "glIsRenderbufferEXT" (GLuint)
    GLvoid realGlBindRenderbufferEXT "glBindRenderbufferEXT" (GLenum, GLuint)
    GLvoid realGlDeleteRenderbuffersEXT "glDeleteRenderbuffersEXT" (GLsizei, GLuint *)
    GLvoid realGlGenRenderbuffersEXT "glGenRenderbuffersEXT" (GLsizei, GLuint *)
    GLvoid realGlRenderbufferStorageEXT "glRenderbufferStorageEXT" (GLenum, GLenum, GLsizei, GLsizei)
    GLvoid realGlGetRenderbufferParameterivEXT "glGetRenderbufferParameterivEXT" (GLenum, GLenum, GLint *)
    GLboolean realGlIsFramebufferEXT "glIsFramebufferEXT" (GLuint)
    GLvoid realGlBindFramebufferEXT "glBindFramebufferEXT" (GLenum, GLuint)
    GLvoid realGlDeleteFramebuffersEXT "glDeleteFramebuffersEXT" (GLsizei, GLuint *)
    GLvoid realGlGenFramebuffersEXT "glGenFramebuffersEXT" (GLsizei, GLuint *)
    GLenum realGlCheckFramebufferStatusEXT "glCheckFramebufferStatusEXT" (GLenum)
    GLvoid realGlFramebufferTexture1DEXT "glFramebufferTexture1DEXT" (GLenum, GLenum, GLenum, GLuint, GLint)
    GLvoid realGlFramebufferTexture2DEXT "glFramebufferTexture2DEXT" (GLenum, GLenum, GLenum, GLuint, GLint)
    GLvoid realGlFramebufferTexture3DEXT "glFramebufferTexture3DEXT" (GLenum, GLenum, GLenum, GLuint, GLint, GLint)
    GLvoid realGlFramebufferRenderbufferEXT "glFramebufferRenderbufferEXT" (GLenum, GLenum, GLenum, GLuint)
    GLvoid realGlGetFramebufferAttachmentParameterivEXT "glGetFramebufferAttachmentParameterivEXT" (GLenum, GLenum, GLenum, GLint *)
    GLvoid realGlGenerateMipmapEXT "glGenerateMipmapEXT" (GLenum)

cdef int glActiveTextureARB(GLenum) except? 0
cdef int glClientActiveTextureARB(GLenum) except? 0
cdef int glClipPlane(GLenum, GLdouble *) except? 0
cdef int glColor4f(GLfloat, GLfloat, GLfloat, GLfloat) except? 0
cdef int glDisable(GLenum) except? 0
cdef int glDisableClientState(GLenum) except? 0
cdef int glEnable(GLenum) except? 0
cdef int glEnableClientState(GLenum) except? 0
cdef int glLoadIdentity() except? 0
cdef int glMatrixMode(GLenum) except? 0
cdef int glOrtho(GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble) except? 0
cdef int glScissor(GLint, GLint, GLsizei, GLsizei) except? 0
cdef int glTexCoordPointer(GLint, GLenum, GLsizei, GLubyte *) except? 0
cdef int glTexEnvf(GLenum, GLenum, GLfloat) except? 0
cdef int glTexEnvfv(GLenum, GLenum, GLfloat *) except? 0
cdef int glTexEnvi(GLenum, GLenum, GLint) except? 0
cdef int glVertexPointer(GLint, GLenum, GLsizei, GLubyte *) except? 0
cdef int glViewport(GLint, GLint, GLsizei, GLsizei) except? 0
