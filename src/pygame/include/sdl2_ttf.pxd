from sdl2 cimport *

cdef extern from "SDL_ttf.h" nogil:
    cdef enum:
        SDL_TTF_MAJOR_VERSION
        SDL_TTF_MINOR_VERSION
        SDL_TTF_PATCHLEVEL

    const SDL_version * TTF_Linked_Version()

    cdef enum:
        UNICODE_BOM_NATIVE
        UNICODE_BOM_SWAPPED

    void TTF_ByteSwappedUNICODE(int swapped)

    ctypedef struct _TTF_Font
    ctypedef _TTF_Font TTF_Font

    int TTF_Init()

    TTF_Font * TTF_OpenFont(const char *file, int ptsize)
    TTF_Font * TTF_OpenFontIndex(const char *file, int ptsize, long index)
    TTF_Font * TTF_OpenFontRW(SDL_RWops *src, int freesrc, int ptsize)
    TTF_Font * TTF_OpenFontIndexRW(SDL_RWops *src, int freesrc, int ptsize, long index)

    cdef enum:
        TTF_STYLE_NORMAL
        TTF_STYLE_BOLD
        TTF_STYLE_ITALIC
        TTF_STYLE_UNDERLINE
        TTF_STYLE_STRIKETHROUGH

    int TTF_GetFontStyle(const TTF_Font *font)
    void TTF_SetFontStyle(TTF_Font *font, int style)
    int TTF_GetFontOutline(const TTF_Font *font)
    void TTF_SetFontOutline(TTF_Font *font, int outline)

    cdef enum:
        TTF_HINTING_NORMAL
        TTF_HINTING_LIGHT
        TTF_HINTING_MONO
        TTF_HINTING_NONE

    int TTF_GetFontHinting(const TTF_Font *font)
    void TTF_SetFontHinting(TTF_Font *font, int hinting)
    int TTF_FontHeight(const TTF_Font *font)
    int TTF_FontAscent(const TTF_Font *font)
    int TTF_FontDescent(const TTF_Font *font)
    int TTF_FontLineSkip(const TTF_Font *font)
    int TTF_GetFontKerning(const TTF_Font *font)
    void TTF_SetFontKerning(TTF_Font *font, int allowed)

    long TTF_FontFaces(const TTF_Font *font)

    int TTF_FontFaceIsFixedWidth(const TTF_Font *font)
    char * TTF_FontFaceFamilyName(const TTF_Font *font)
    char * TTF_FontFaceStyleName(const TTF_Font *font)

    int TTF_GlyphIsProvided(const TTF_Font *font, Uint16 ch)

    int TTF_GlyphMetrics(TTF_Font *font, Uint16 ch,
                         int *minx, int *maxx,
                         int *miny, int *maxy, int *advance)

    int TTF_SizeText(TTF_Font *font, const char *text, int *w, int *h)
    int TTF_SizeUTF8(TTF_Font *font, const char *text, int *w, int *h)
    int TTF_SizeUNICODE(TTF_Font *font, const Uint16 *text, int *w, int *h)

    SDL_Surface * TTF_RenderText_Solid(TTF_Font *font,
                    const char *text, SDL_Color fg)
    SDL_Surface * TTF_RenderUTF8_Solid(TTF_Font *font,
                    const char *text, SDL_Color fg)
    SDL_Surface * TTF_RenderUNICODE_Solid(TTF_Font *font,
                    const Uint16 *text, SDL_Color fg)

    SDL_Surface * TTF_RenderGlyph_Solid(TTF_Font *font,
                        Uint16 ch, SDL_Color fg)

    SDL_Surface * TTF_RenderText_Shaded(TTF_Font *font,
                    const char *text, SDL_Color fg, SDL_Color bg)
    SDL_Surface * TTF_RenderUTF8_Shaded(TTF_Font *font,
                    const char *text, SDL_Color fg, SDL_Color bg)
    SDL_Surface * TTF_RenderUNICODE_Shaded(TTF_Font *font,
                    const Uint16 *text, SDL_Color fg, SDL_Color bg)

    SDL_Surface * TTF_RenderGlyph_Shaded(TTF_Font *font,
                    Uint16 ch, SDL_Color fg, SDL_Color bg)

    SDL_Surface * TTF_RenderText_Blended(TTF_Font *font,
                    const char *text, SDL_Color fg)
    SDL_Surface * TTF_RenderUTF8_Blended(TTF_Font *font,
                    const char *text, SDL_Color fg)
    SDL_Surface * TTF_RenderUNICODE_Blended(TTF_Font *font,
                    const Uint16 *text, SDL_Color fg)

    SDL_Surface * TTF_RenderText_Blended_Wrapped(TTF_Font *font,
                    const char *text, SDL_Color fg, Uint32 wrapLength)
    SDL_Surface * TTF_RenderUTF8_Blended_Wrapped(TTF_Font *font,
                    const char *text, SDL_Color fg, Uint32 wrapLength)
    SDL_Surface * TTF_RenderUNICODE_Blended_Wrapped(TTF_Font *font,
                    const Uint16 *text, SDL_Color fg, Uint32 wrapLength)

    SDL_Surface * TTF_RenderGlyph_Blended(TTF_Font *font,
                            Uint16 ch, SDL_Color fg)

    void TTF_CloseFont(TTF_Font *font)
    void TTF_Quit()
    int TTF_WasInit()

    int TTF_GetFontKerningSize(TTF_Font *font, int prev_index, int index)
