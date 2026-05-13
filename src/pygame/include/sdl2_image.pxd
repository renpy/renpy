from sdl2 cimport *

cdef extern from "pygame/sdl_image_compat.h" nogil:
    ctypedef enum IMG_InitFlags:
        IMG_INIT_JPG
        IMG_INIT_PNG
        IMG_INIT_TIF
        IMG_INIT_WEBP
        IMG_INIT_JXL
        IMG_INIT_AVIF

    int IMG_Init(int flags)
    void IMG_Quit()

    SDL_Surface *IMG_Load(const char *file)
    SDL_Surface *IMG_Load_RW(SDL_RWops *src, int freesrc)
    SDL_Surface *IMG_LoadTyped_RW(SDL_RWops *src, int freesrc, const char *type)

    SDL_Surface *IMG_LoadSizedSVG_RW(SDL_RWops *src, int width, int height)

    SDL_Texture *IMG_LoadTexture(SDL_Renderer *renderer, const char *file)
    SDL_Texture *IMG_LoadTexture_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc)
    SDL_Texture *IMG_LoadTextureTyped_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc, const char *type)

    int IMG_SavePNG(SDL_Surface *surface, const char *file)
    int IMG_SavePNG_RW(SDL_Surface *surface, SDL_RWops *dst, int freedst)
