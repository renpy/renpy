from sdl2 cimport SDL_Surface, SDL_RWops

cdef extern from "pygame_sdl2/pygame_sdl2.rwobject_api.h":
    void import_pygame_sdl2__rwobject()
    SDL_RWops* RWopsFromPython(object obj)

cdef extern from "pygame_sdl2/pygame_sdl2.surface_api.h":
    int import_pygame_sdl2__surface()
    SDL_Surface *PySurface_AsSurface(object)

