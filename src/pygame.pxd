cdef extern from "pygame/pygame.h":
    struct SDL_Surface:
        int w
        int h
        int pitch
        int flags
        void *pixels

    struct SDL_Rect:
        int x
        int y
        int w
        int h

    SDL_Surface *PySurface_AsSurface(object)
    int SDL_SetAlpha(SDL_Surface *surface, unsigned int flag, char alpha)

    enum:
        SDL_SRCALPHA

cdef extern int SDL_BlitSurface(SDL_Surface *src, SDL_Rect *srcrect, SDL_Surface *dst, SDL_Rect *dstrect) nogil
