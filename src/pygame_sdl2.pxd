from sdl2 cimport SDL_Surface, SDL_RWops, SDL_Window

cdef extern from "pygame_sdl2/pygame_sdl2.h":
    int import_pygame_sdl2()
    SDL_RWops* RWopsFromPython(object obj)
    SDL_Surface *PySurface_AsSurface(object)
    SDL_Window *PyWindow_AsWindow(object)

