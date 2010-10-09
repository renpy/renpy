cdef extern from "pygame/pygame.h":
    struct SDL_Surface:
        int w
        int h
        int pitch
        void *pixels
 
    SDL_Surface *PySurface_AsSurface(object)
