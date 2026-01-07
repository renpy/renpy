# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from .sdl cimport *
from .sdl3_gfx cimport *
from libc.stdlib cimport malloc, free
from .surface cimport Surface
from .color cimport Color

from .error import error
from .rect import Rect

cdef class GFXCanvas:
    cdef Surface surface
    cdef SDL_Renderer* renderer

    def __init__(self, Surface surface):
        self.surface = surface
        self.renderer = SDL_CreateSoftwareRenderer(surface.surface)
        if self.renderer == NULL:
            raise error("Could not create software renderer for surface")

    def __dealloc__(self):
        if self.renderer != NULL:
            SDL_RenderPresent(self.renderer)
            SDL_DestroyRenderer(self.renderer)

    def pixel(self, x, y, color):
        cdef Color c = Color(color)
        pixelRGBA(self.renderer, x, y, c.r, c.g, c.b, c.a)

    def hline(self, x1, x2, y, color):
        cdef Color c = Color(color)
        hlineRGBA(self.renderer, x1, x2, y, c.r, c.g, c.b, c.a)

    def vline(self, x, y1, y2, color):
        cdef Color c = Color(color)
        vlineRGBA(self.renderer, x, y1, y2, c.r, c.g, c.b, c.a)

    def rectangle(self, rect, color):
        cdef Color c = Color(color)
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        rectangleRGBA(self.renderer, rect.x, rect.y, rect.x + rect.w, rect.y + rect.h, c.r, c.g, c.b, c.a)

    def rounded_rectangle(self, rect, rad, color):
        cdef Color c = Color(color)
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        roundedRectangleRGBA(self.renderer, rect.x, rect.y, rect.x + rect.w, rect.y + rect.h, rad, c.r, c.g, c.b, c.a)

    def box(self, rect, color):
        cdef Color c = Color(color)
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        boxRGBA(self.renderer, rect.x, rect.y, rect.x + rect.w, rect.y + rect.h, c.r, c.g, c.b, c.a)

    def rounded_box(self, rect, rad, color):
        cdef Color c = Color(color)
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        roundedBoxRGBA(self.renderer, rect.x, rect.y, rect.x + rect.w, rect.y + rect.h, rad, c.r, c.g, c.b, c.a)

    def line(self, x1, y1, x2, y2, color):
        cdef Color c = Color(color)
        lineRGBA(self.renderer, x1, y1, x2, y2, c.r, c.g, c.b, c.a)

    def aaline(self, x1, y1, x2, y2, color):
        cdef Color c = Color(color)
        aalineRGBA(self.renderer, x1, y1, x2, y2, c.r, c.g, c.b, c.a)

    def thick_line(self, x1, y1, x2, y2, width, color):
        cdef Color c = Color(color)

        # This locks up in c code when trying to draw a zero-length line. So make
        # sure that doesn't happen.
        cdef int x1int, y1int, x2int, y2int
        x1int = x1
        y1int = y1
        x2int = x2
        y2int = y2

        if x1int == x2int and y1int == y2int:
            return

        thickLineRGBA(self.renderer, x1int, y1int, x2int, y2int, width, c.r, c.g, c.b, c.a)

    def circle(self, x, y, r, color):
        cdef Color c = Color(color)
        circleRGBA(self.renderer, x, y, r, c.r, c.g, c.b, c.a)

    def arc(self, x, y, r, start, end, color):
        cdef Color c = Color(color)
        arcRGBA(self.renderer, x, y, r, start, end, c.r, c.g, c.b, c.a)

    def aacircle(self, x, y, r, color):
        cdef Color c = Color(color)
        aacircleRGBA(self.renderer, x, y, r, c.r, c.g, c.b, c.a)

    def filled_circle(self, x, y, r, color):
        cdef Color c = Color(color)
        filledCircleRGBA(self.renderer, x, y, r, c.r, c.g, c.b, c.a)

    def ellipse(self, x, y, rx, ry, color):
        cdef Color c = Color(color)
        ellipseRGBA(self.renderer, x, y, rx, ry, c.r, c.g, c.b, c.a)

    def aaellipse(self, x, y, rx, ry, color):
        cdef Color c = Color(color)
        aaellipseRGBA(self.renderer, x, y, rx, ry, c.r, c.g, c.b, c.a)

    def filled_ellipse(self, x, y, rx, ry, color):
        cdef Color c = Color(color)
        filledEllipseRGBA(self.renderer, x, y, rx, ry, c.r, c.g, c.b, c.a)

    def pie(self, x, y, r, start, end, color):
        cdef Color c = Color(color)
        pieRGBA(self.renderer, x, y, r, start, end, c.r, c.g, c.b, c.a)

    def filled_pie(self, x, y, r, start, end, color):
        cdef Color c = Color(color)
        filledPieRGBA(self.renderer, x, y, r, start, end, c.r, c.g, c.b, c.a)

    def trigon(self, x1, y1, x2, y2, x3, y3, color):
        cdef Color c = Color(color)
        trigonRGBA(self.renderer, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

    def aatrigon(self, x1, y1, x2, y2, x3, y3, color):
        cdef Color c = Color(color)
        aatrigonRGBA(self.renderer, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

    def filled_trigon(self, x1, y1, x2, y2, x3, y3, color):
        cdef Color c = Color(color)
        filledTrigonRGBA(self.renderer, x1, y1, x2, y2, x3, y3, c.r, c.g, c.b, c.a)

    def polygon(self, points, color):
        cdef Color c = Color(color)
        cdef float *vx
        cdef float *vy
        cdef size_t num_points = len(points)
        vx = <float*>malloc(num_points * sizeof(float))
        vy = <float*>malloc(num_points * sizeof(float))
        for n, pt in zip(range(num_points), points):
            vx[n], vy[n] = points[n]
        polygonRGBA(self.renderer, vx, vy, num_points, c.r, c.g, c.b, c.a)
        free(vx)
        free(vy)

    def aapolygon(self, points, color):
        cdef Color c = Color(color)
        cdef float *vx
        cdef float *vy
        cdef size_t num_points = len(points)
        vx = <float*>malloc(num_points * sizeof(float))
        vy = <float*>malloc(num_points * sizeof(float))
        for n, pt in zip(range(num_points), points):
            vx[n], vy[n] = points[n]
        aapolygonRGBA(self.renderer, vx, vy, num_points, c.r, c.g, c.b, c.a)
        free(vx)
        free(vy)

    def filled_polygon(self, points, color):
        cdef Color c = Color(color)
        cdef float *vx
        cdef float *vy
        cdef size_t num_points = len(points)
        vx = <float*>malloc(num_points * sizeof(float))
        vy = <float*>malloc(num_points * sizeof(float))
        for n, pt in zip(range(num_points), points):
            vx[n], vy[n] = points[n]
        filledPolygonRGBA(self.renderer, vx, vy, num_points, c.r, c.g, c.b, c.a)
        free(vx)
        free(vy)

    def textured_polygon(self, points, Surface texture not None, tx, ty):
        cdef float *vx
        cdef float *vy
        cdef size_t num_points = len(points)
        vx = <float*>malloc(num_points * sizeof(float))
        vy = <float*>malloc(num_points * sizeof(float))
        for n, pt in zip(range(num_points), points):
            vx[n], vy[n] = points[n]
        texturedPolygon(self.renderer, vx, vy, num_points, texture.surface, tx, ty)
        free(vx)
        free(vy)

    def bezier(self, points, steps, color):
        cdef Color c = Color(color)
        cdef float *vx
        cdef float *vy
        cdef size_t num_points = len(points)
        vx = <float*>malloc(num_points * sizeof(float))
        vy = <float*>malloc(num_points * sizeof(float))
        for n, pt in zip(range(num_points), points):
            vx[n], vy[n] = points[n]
        bezierRGBA(self.renderer, vx, vy, num_points, steps, c.r, c.g, c.b, c.a)
        free(vx)
        free(vy)

def pixel(Surface surface, x, y, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.pixel(x, y, color)


def hline(Surface surface, x1, x2, y, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.hline(x1, x2, y, color)

def vline(Surface surface, x, y1, y2, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.vline(x, y1, y2, color)

def rectangle(Surface surface, rect, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.rectangle(rect, color)

def rounded_rectangle(Surface surface, rect, rad, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.rounded_rectangle(rect, rad, color)

def box(Surface surface, rect, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.box(rect, color)

def rounded_box(Surface surface, rect, rad, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.rounded_box(rect, rad, color)

def line(Surface surface, x1, y1, x2, y2, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.line(x1, y1, x2, y2, color)

def aaline(Surface surface, x1, y1, x2, y2, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.aaline(x1, y1, x2, y2, color)

def thick_line(Surface surface, x1, y1, x2, y2, width, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.thick_line(x1, y1, x2, y2, width, color)

def circle(Surface surface, x, y, r, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.circle(x, y, r, color)

def arc(Surface surface, x, y, r, start, end, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.arc(x, y, r, start, end, color)

def aacircle(Surface surface, x, y, r, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.aacircle(x, y, r, color)

def filled_circle(Surface surface, x, y, r, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.filled_circle(x, y, r, color)

def ellipse(Surface surface, x, y, rx, ry, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.ellipse(x, y, rx, ry, color)

def aaellipse(Surface surface, x, y, rx, ry, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.aaellipse(x, y, rx, ry, color)

def filled_ellipse(Surface surface, x, y, rx, ry, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.filled_ellipse(x, y, rx, ry, color)

def pie(Surface surface, x, y, r, start, end, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.pie(x, y, r, start, end, color)

def filled_pie(Surface surface, x, y, r, start, end, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.filled_pie(x, y, r, start, end, color)

def trigon(Surface surface, x1, y1, x2, y2, x3, y3, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.trigon(x1, y1, x2, y2, x3, y3, color)

def aatrigon(Surface surface, x1, y1, x2, y2, x3, y3, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.aatrigon(x1, y1, x2, y2, x3, y3, color)

def filled_trigon(Surface surface, x1, y1, x2, y2, x3, y3, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.filled_trigon(x1, y1, x2, y2, x3, y3, color)

def polygon(Surface surface, points, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.polygon(points, color)

def aapolygon(Surface surface, points, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.aapolygon(points, color)

def filled_polygon(Surface surface, points, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.filled_polygon(points, color)

def textured_polygon(Surface surface, points, Surface texture not None, tx, ty):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.textured_polygon(points, texture, tx, ty)

def bezier(Surface surface, points, steps, color):
    cdef GFXCanvas canvas = GFXCanvas(surface)
    canvas.bezier(points, steps, color)
