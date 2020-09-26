from sdl2 cimport SDL_GL_GetProcAddress

cdef void *find_gl_command(names):

    cdef void *rv = NULL

    for i in names:
        rv = SDL_GL_GetProcAddress(i)

        if rv != NULL:
            return rv

    raise Exception("{} not found.".format(names[0]))

