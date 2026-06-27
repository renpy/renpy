from .sdl cimport *

cdef extern from "pygame/SDL3_rotozoom.h" nogil:
    cdef enum:
        SMOOTHING_OFF
        SMOOTHING_ON

    SDL_Surface *rotozoomSurface(SDL_Surface * src, double angle, double zoom, int smooth)
    SDL_Surface *rotozoomSurfaceXY(SDL_Surface * src, double angle, double zoomx, double zoomy, int smooth)
    void rotozoomSurfaceSize(int width, int height, double angle, double zoom, int *dstwidth, int *dstheight)
    void rotozoomSurfaceSizeXY(int width, int height, double angle, double zoomx, double zoomy, int *dstwidth, int *dstheight)

    SDL_Surface *zoomSurface(SDL_Surface * src, double zoomx, double zoomy, int smooth)
    void zoomSurfaceSize(int width, int height, double zoomx, double zoomy, int *dstwidth, int *dstheight)

    SDL_Surface *shrinkSurface(SDL_Surface * src, int factorx, int factory)
    SDL_Surface* rotateSurface90Degrees(SDL_Surface* src, int numClockwiseTurns)


cdef extern from "pygame/SDL3_gfxPrimitives.h" nogil:
    int pixelRGBA(SDL_Renderer * dst, float x, float y, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int hlineRGBA(SDL_Renderer * dst, float x1, float x2, float y, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int vlineRGBA(SDL_Renderer * dst, float x, float y1, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int rectangleRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int roundedRectangleRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int boxRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int roundedBoxRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int lineRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int aalineRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int thickLineRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, Uint8 width, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int circleRGBA(SDL_Renderer * dst, float x, float y, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int arcRGBA(SDL_Renderer * dst, float x, float y, float rad, float start, float end, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int aacircleRGBA(SDL_Renderer * dst, float x, float y, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int filledCircleRGBA(SDL_Renderer * dst, float x, float y, float rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int ellipseRGBA(SDL_Renderer * dst, float x, float y, float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int aaellipseRGBA(SDL_Renderer * dst, float x, float y, float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int filledEllipseRGBA(SDL_Renderer * dst, float x, float y, float rx, float ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int pieRGBA(SDL_Renderer * dst, float x, float y, float rad, float start, float end, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int filledPieRGBA(SDL_Renderer * dst, float x, float y, float rad, float start, float end, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int trigonRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, float x3, float y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int aatrigonRGBA(SDL_Renderer * dst,  float x1, float y1, float x2, float y2, float x3, float y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int filledTrigonRGBA(SDL_Renderer * dst, float x1, float y1, float x2, float y2, float x3, float y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int polygonRGBA(SDL_Renderer * dst, const float * vx, const float * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int aapolygonRGBA(SDL_Renderer * dst, const float * vx, const float * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int filledPolygonRGBA(SDL_Renderer * dst, const float * vx, const float * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a)

    int texturedPolygon(SDL_Renderer * dst, const float * vx, const float * vy, int n, SDL_Surface * texture,int texture_dx,int texture_dy)

    int bezierRGBA(SDL_Renderer * dst, const float * vx, const float * vy, int n, int s, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
