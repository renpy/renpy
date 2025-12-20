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

from pygame.sdl cimport *
from pygame.surface cimport Surface

import renpy.pygame.gfxdraw as gfxdraw
from renpy.pygame.rect import Rect
from renpy.pygame.error import error

def rect(Surface surface, color, rect, width=0):
    if not isinstance(rect, Rect):
        rect = Rect(rect)

    if width == 0:
        gfxdraw.box(surface, rect, color)
    else:
        gfxdraw.rectangle(surface, rect, color)
        n = 1
        while n < width:
            r = Rect(rect.x - n, rect.y - n, rect.w + (n*2), rect.h + (n*2))
            gfxdraw.rectangle(surface, r, color)
            r = Rect(rect.x + n, rect.y + n, rect.w - (n*2), rect.h - (n*2))
            gfxdraw.rectangle(surface, r, color)
            n += 1
    dirty = Rect(rect.x - width, rect.y - width, rect.w + (width*2), rect.h + (width*2))
    return dirty.clip(surface.get_rect())

def polygon(Surface surface, color, pointlist, width=0):
    if width == 0:
        gfxdraw.filled_polygon(surface, pointlist, color)
        dirty = Rect(pointlist[0], (1, 1))
        n = 1
        while n < len(pointlist):
            dirty.union_ip(Rect(pointlist[n], (1,1)))
            n += 1
        return dirty.clip(surface.get_rect())
    else:
        return lines(surface, color, True, pointlist, width)

def circle(Surface surface, color, pos, radius, width=0):
    x, y = pos
    if width == 0:
        gfxdraw.filled_circle(surface, x, y, radius, color)
        dirty = Rect((x - radius, y - radius), (radius*2, radius*2))
        return dirty.clip(surface.get_rect())
    else:
        gfxdraw.circle(surface, x, y, radius, color)
        n = 1
        while n < width:
            gfxdraw.circle(surface, x, y, radius - n, color)
            gfxdraw.circle(surface, x + 1, y, radius - n, color)
            gfxdraw.circle(surface, x - 1, y, radius - n, color)
            n += 1
        dirty = Rect(x - radius - width, y - radius - width, (radius*2) + width, (radius*2) + width)
        return dirty.clip(surface.get_rect())

def ellipse(Surface surface, color, rect, width=0):
    x, y, rx, ry = rect
    if width == 0:
        gfxdraw.filled_ellipse(surface, x, y, rx, ry, color)
        dirty = Rect((x - rx, y - ry), (rx*2, ry*2))
    else:
        gfxdraw.ellipse(surface, x, y, rx, ry, color)
        n = 1
        while n < width:
            gfxdraw.ellipse(surface, x, y, rx - n, ry - n, color)
            gfxdraw.ellipse(surface, x + 1, y, rx - n, ry - n, color)
            gfxdraw.ellipse(surface, x - 1, y, rx - n, ry - n, color)
            n += 1
        dirty = Rect(x - rx - width, y - ry - width, (rx*2) + width, (ry*2) + width)
    return dirty.clip(surface.get_rect())

def arc(Surface surface, color, rect, start_angle, stop_angle, width=1):
    raise error("Not implemented.")

def line(Surface surface, color, start_pos, end_pos, width=1):
    gfxdraw.thick_line(surface, start_pos[0], start_pos[1],
                       end_pos[0], end_pos[1], width, color)
    dirty = Rect(start_pos, (width, width))
    dirty.union_ip(Rect(end_pos, (width, width)))
    return dirty.clip(surface.get_rect())

def lines(Surface surface, color, closed, pointlist, width=1):
    n = 0
    dirty = Rect(pointlist[0], (width, width))
    while n < len(pointlist) - 1:
        line(surface, color, pointlist[n], pointlist[n+1], width)
        dirty.union_ip(Rect(pointlist[n+1], (width, width)))
        n += 1
    if closed:
        line(surface, color, pointlist[n], pointlist[0], width)
    return dirty.clip(surface.get_rect())

def aaline(Surface surface, color, startpos, endpos, blend=1):
    x1, y1 = startpos
    x2, y2 = endpos
    gfxdraw.aaline(surface, x1, y1, x2, y2, color)
    dirty = Rect(x1, y1, x2 - x1, y2 - y1)
    return dirty.clip(surface.get_rect())

def aalines(Surface surface, color, closed, pointlist, blend=1):
    n = 0
    dirty = Rect(pointlist[0], (1,1))
    while n < len(pointlist) - 1:
        r = aaline(surface, color, pointlist[n], pointlist[n+1])
        dirty.union_ip(r)
        n += 1
    if closed:
        aaline(surface, color, pointlist[n], pointlist[0])
    return dirty.clip(surface.get_rect())
