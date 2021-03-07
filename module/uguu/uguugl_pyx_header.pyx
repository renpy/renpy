from sdl2 cimport SDL_GL_GetProcAddress, SDL_GetError

found_functions = set()

cdef void *find_gl_command(names):

    cdef void *rv = NULL

    for i in names:
        rv = SDL_GL_GetProcAddress(i)

        if rv != NULL:
            found_functions.add(names[0].decode("utf-8"))
            return rv

    import renpy
    renpy.display.log.write("UGUU couldn't find {}: {}".format(names[0], SDL_GetError()))

    return NULL

def clear_missing_functions():
    global found_functions
    found_functions = set()

def check_missing_functions(required):
    import renpy

    required = set(required)

    missing_required = list(required - found_functions)
    missing_required.sort()

    if missing_required:

        renpy.display.log.write("The following gl functions are missing:")
        for i in missing_required:
            renpy.display.log.write("- %s", i)

        return True
    else:
        return False

