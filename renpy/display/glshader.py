# This file contains GLSL shader code, and code to load shaders.

import array
import _renpy_tegl as gl

VERTEX_SHADER = """
void main() {
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_TexCoord[1] = gl_MultiTexCoord1;
    gl_TexCoord[2] = gl_MultiTexCoord2;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

BLIT_SHADER = """
uniform sampler2D tex0;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);

    gl_FragColor = color0;
}
"""

BLEND_SHADER = """
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform float done;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);
    vec4 color1 = texture2D(tex1, gl_TexCoord[1].st);

    gl_FragColor = mix(color0, color1, done);
}
"""

IMAGEBLEND_SHADER = """
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float offset;
uniform float multiplier;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);
    vec4 color1 = texture2D(tex1, gl_TexCoord[1].st);
    vec4 color2 = texture2D(tex2, gl_TexCoord[2].st);

    float a = clamp((color2.a + offset) * multiplier, 0.0, 1.0);

     

    gl_FragColor = mix(color0, color1, a);
}
"""

def check_status(handle, type):
    """
    Checks the status of a shader or program. If it fails, then an
    exception is raised.
    """
    
    status = [ 0 ]    
    gl.GetObjectParameterivARB(handle, type, status)

    if status[0] == 0:

        log_length_list = [ 0 ]
        gl.GetObjectParameterivARB(handle, gl.OBJECT_INFO_LOG_LENGTH_ARB, log_length_list)
        log_length = log_length_list[0]

        log = array.array('c', ' ' * log_length)
        
        gl.GetInfoLogARB(handle, log_length, [ 0 ], log)

        raise Exception("Shader error: %s" % log.tostring())
        

def compile_shader(kind, source):
    """
    Allocates and compiles a shader.
    """

    
    handle = gl.CreateShaderObjectARB(kind)
    gl.ShaderSourceARB(handle, 1, [ source ], [ len(source) ])
    gl.CompileShaderARB(handle)

    check_status(handle, gl.OBJECT_COMPILE_STATUS_ARB)

    return handle


def compile_program(vertex, fragment):
    """
    Compiles a pair of shaders into a program.
    """

    
    vertex_shader = compile_shader(gl.VERTEX_SHADER_ARB, vertex)
    fragment_shader = compile_shader(gl.FRAGMENT_SHADER_ARB, fragment)
    
    program = gl.CreateProgramObjectARB()

    gl.AttachObjectARB(program, vertex_shader)
    gl.AttachObjectARB(program, fragment_shader)

    gl.LinkProgramARB(program)

    check_status(program, gl.OBJECT_LINK_STATUS_ARB)

    gl.UseProgramObjectARB(program)
    
    gl.DeleteObjectARB(vertex_shader)
    gl.DeleteObjectARB(fragment_shader)
    
    return program


# These return the standard programs, compiled and ready to use.

def blit_program():
    return compile_program(VERTEX_SHADER, BLIT_SHADER)

def blend_program():
    return compile_program(VERTEX_SHADER, BLEND_SHADER)

def imageblend_program():
    return compile_program(VERTEX_SHADER, IMAGEBLEND_SHADER)


    
    
    
    
    
